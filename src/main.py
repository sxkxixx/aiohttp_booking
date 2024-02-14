import logging
from datetime import timedelta

from aiohttp.typedefs import Handler
from aiohttp.web import Application, run_app, Request, Response, middleware

from config import ApplicationConfig
from endpoint.rest import AbstractRouter, AuthRouter
from infrastructure.database.database import manager, database
from infrastructure.database.model import User
from service import HashService, JWTService
from storage.user import UserRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    format=(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
)


def setup_routers(_app: Application, *routers: AbstractRouter) -> None:
    for router in routers:
        router.setup_endpoints(_app)


async def ping(request: Request) -> Response:
    """
    ---
    description: This end-point allow to test that service is up.
    tags:
    - Health check
    produces:
    - text/plain
    responses:
        "200":
            description: successful operation. Return "pong" text
        "405":
            description: invalid HTTP Method
        """
    return Response(text='pong')


MODELS = [User]


def initialize_database_tables() -> None:
    with database:
        database.create_tables(MODELS)


@middleware
async def logging_middleware(request: Request, handler: Handler):
    info = f'METHOD = {request.method}, {request.host}{request.path}'
    logger.info(f'Received request: {info}')
    response = await handler(request)
    logger.info(f'Response status code: {response.status}')
    return response


def init_app() -> Application:
    app = Application()
    hash_service = HashService()
    jwt_service = JWTService(
        access_token_timedelta=timedelta(minutes=ApplicationConfig.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=ApplicationConfig.SECRET_KEY,
    )
    user_repository = UserRepository(manager)
    auth_router = AuthRouter('/api/v1/auth', user_repository, hash_service, jwt_service)
    setup_routers(app, auth_router)
    return app


if __name__ == '__main__':
    app: Application = init_app()
    initialize_database_tables()

    app.router.add_route(
        'GET', '/', ping
    )
    run_app(app, host='localhost', port=8000)
