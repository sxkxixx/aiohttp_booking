import json
import os
from datetime import datetime
from typing import Optional

import peewee
from aiohttp.web import Application, Request, Response

from application.user_session.user_session import UserSession
from dto.user import UserLoginRequest, UserResponseDTO, TokenResponse, UserRegisterRequest
from endpoint import http_exceptions
from endpoint.response import PydanticJsonResponse
from infrastructure.database.model import User
from infrastructure.redis import redis
from service.hash_service import HashService
from service.jwt_service import JWTService
from storage.user.abstract_user_repository import AbstractUserRepository
from .abstract_router import AbstractRouter


class AuthRouter(AbstractRouter):
    REFRESH_TOKEN_COOKIE_NAME = "refresh_token"

    def __init__(
            self,
            user_repository: AbstractUserRepository,
            hash_service: HashService,
            jwt_service: JWTService,
    ):
        self.user_repository: AbstractUserRepository = user_repository
        self._hasher: HashService = hash_service
        self._jwt_service: JWTService = jwt_service

    def setup_router(self) -> Application:
        router = Application()
        router.router.add_route('POST', f'/register', self.handle_register)
        router.router.add_route('POST', f'/login', self.handle_login)
        router.router.add_route('POST', f'/refresh', self.handle_refresh_session)
        return router

    async def handle_register(self, request: Request) -> Response:
        """
        Обработчик POST-запроса для регистрации пользователя
        :param request:
        :return:
        """
        schema = UserRegisterRequest.model_validate(
            await request.json(),
            from_attributes=True
        )
        schema.password = self._hasher.get_str_hash(schema.password)
        try:
            user: User = await self.user_repository.create_user(schema)
            return PydanticJsonResponse(
                body=UserResponseDTO.model_validate(user, from_attributes=True),
            )
        except peewee.IntegrityError:
            return http_exceptions.UniqueEmailException()

    async def handle_login(self, request: Request) -> Response:
        """
        Обработчик POST-запроса на аутентификацию пользователя
        :param request:
        :return:
        """
        schema = UserLoginRequest.model_validate(await request.json(), from_attributes=True)
        user: Optional[User] = await self.user_repository.get_user(User.email == schema.email)
        if not user:
            return http_exceptions.NotFoundException(text='User Not Found')
        if not self._hasher.equals(schema.password, user.hashed_password):
            return http_exceptions.BadRequestException(text="Passwords don't match")
        refresh_session = UserSession(
            user_id=user.id, ip_address=request.remote,
            fingerprint=schema.fingerprint, user_agent=request.headers.get('User-Agent')
        )
        return await self.__generate_token_response(user, refresh_session)

    async def handle_refresh_session(self, request: Request) -> Response:
        """
        request.body: {'fingerprint': str}
        :return:
        """
        fingerprint = (await request.json()).get('fingerprint')
        if not (refresh_token := request.cookies.get(self.REFRESH_TOKEN_COOKIE_NAME)):
            return http_exceptions.BadRequestException(text='Refresh token required in cookie')
        session_payload: Optional[str] = await redis.get(refresh_token)
        if not session_payload:
            return http_exceptions.UnauthorizedException(text='Session is expired')
        await redis.delete(refresh_token)
        session: UserSession = UserSession.from_json(json.loads(session_payload))
        user: Optional[User] = await self.user_repository.get_user(User.id == session.user_id)
        if not session.is_valid(
                ip_address=request.remote,
                fingerprint=fingerprint,
                user_agent=request.headers.get('User-Agent')):
            return http_exceptions.UnauthorizedException(text='Invalid session params')

        return await self.__generate_token_response(user, session)

    async def __generate_token_response(self, user: User, session: UserSession) -> Response:
        access_token = self._jwt_service.get_access_token(user)
        refresh_token = os.urandom(32).hex()
        await redis.setex(refresh_token, session.session_ttl, session.json_encoded())
        token_schema = TokenResponse(
            access_token=access_token,
            header='Authorization'
        )
        response = PydanticJsonResponse(body=token_schema)
        max_age = int((datetime.utcnow() + session.session_ttl).timestamp())
        response.set_cookie(
            self.REFRESH_TOKEN_COOKIE_NAME, refresh_token,
            max_age=max_age, path='/api/v1/auth', httponly=True
        )
        return response
