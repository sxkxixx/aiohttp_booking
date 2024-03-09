import logging
from typing import Optional

from aiohttp.typedefs import Handler
from aiohttp.web import Request, StreamResponse
from aiohttp.web_middlewares import middleware
from jose import ExpiredSignatureError, JWTError

from common.service import JWTService
from endpoint import http_exceptions
from infrastructure.database.model import User
from storage.user import AbstractUserRepository

logger = logging.getLogger('Aiohttp Server')
logger.setLevel(logging.INFO)
logging.basicConfig(
    format=(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
)


@middleware
async def logging_middleware(request: Request, handler: Handler) -> StreamResponse:
    info = f'METHOD = {request.method}, {request.host}{request.path}'
    logger.info(f'Received request: {info}')
    response = await handler(request)
    logger.info(f'Response status code: {response.status}')
    return response


class AuthMiddleware:
    TOKEN_MISSING: str = 'Missing authorization token'
    TOKEN_EXPIRED: str = 'Authorization token is expired'
    INVALID_TOKEN: str = 'Invalid authorization token'

    def __init__(
            self,
            jwt_service: JWTService,
            user_repository: AbstractUserRepository
    ):
        self.jwt_service = jwt_service
        self.user_repository = user_repository

    @middleware
    async def __call__(self, request: Request, handler: Handler) -> StreamResponse:
        access_token: Optional[str] = request.headers.get('Authorization', None)
        if not access_token:
            raise http_exceptions.UnauthorizedException(text=self.TOKEN_MISSING)
        try:
            payload: Optional[dict] = self.jwt_service.get_token_payload(access_token)
        except ExpiredSignatureError:
            raise http_exceptions.UnauthorizedException(text=self.TOKEN_EXPIRED)
        except JWTError:
            raise http_exceptions.UnauthorizedException(text=self.INVALID_TOKEN)
        email: str = payload.get('email')
        user: Optional[User] = await self.user_repository.get_user(User.email == email)
        if not user:
            # TODO: Продумать момент, когда токен валидный, но пользователь не найден в БД
            raise http_exceptions.UnauthorizedException()
        request['user']: User = user
        return await handler(request)
