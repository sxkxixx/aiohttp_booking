from typing import Optional

import peewee
from aiohttp.web import Application, Request, Response

from dto.user import UserAuthRequest, UserResponseDTO, TokenResponse
from endpoint import http_exceptions
from infrastructure.database.model import User
from response import PydanticJsonResponse
from service.hash_service import HashService
from service.jwt_service import JWTService
from storage.user.abstract_user_repository import AbstractUserRepository
from .abstract_router import AbstractRouter


class AuthRouter(AbstractRouter):
    def __init__(
            self,
            prefix: str,
            user_repository: AbstractUserRepository,
            hash_service: HashService,
            jwt_service: JWTService
    ):
        assert prefix.startswith('/'), 'Prefix path has to start with "/"'
        self.prefix: str = prefix
        self.user_repository: AbstractUserRepository = user_repository
        self._hasher: HashService = hash_service
        self._jwt_service: JWTService = jwt_service

    def setup_endpoints(self, app: Application):
        app.router.add_route('POST', f'{self.prefix}/register', self.handle_register)
        app.router.add_route('POST', f'{self.prefix}/login', self.handle_login)

    async def handle_register(self, request: Request) -> Response:
        """
        Обработчик POST-запроса для регистрации пользователя
        :param request:
        :return:
        """
        schema = UserAuthRequest.model_validate(
            await request.json(),
            from_attributes=True
        )
        schema.hashed_password = self._hasher.get_str_hash(schema.hashed_password)
        try:
            user: User = await self.user_repository.create_user(schema)
            return PydanticJsonResponse(
                body=UserResponseDTO.model_validate(user, from_attributes=True),
                status=200
            )
        except peewee.IntegrityError:
            raise http_exceptions.UniqueEmailException()

    async def handle_login(self, request: Request) -> Response:
        """
        Обработчик POST-запроса на аутентификацию пользователя
        :param request:
        :return:
        """
        schema = UserAuthRequest.model_validate(
            await request.json(), from_attributes=True
        )
        user: Optional[User] = await self.user_repository.get_user(**schema.model_dump())
        if not user:
            raise http_exceptions.NotFoundException()
        if self._hasher.equals(schema.hashed_password, user.hashed_password):
            raise http_exceptions.BadRequestException(message='Passwords don\'t match')
        jwt_token: str = self._jwt_service.get_access_token(user)
        token_schema = TokenResponse(
            access_token=jwt_token,
            token_type='Bearer',
            header='Authorization'
        )
        print(request.remote)
        response = PydanticJsonResponse(body=token_schema)
        response.set_cookie('refresh_token', 'refresh_token')
        return response
