import logging
from datetime import timedelta

from aiohttp.web import Application, run_app, Request, Response

import middleware
from endpoint.rest import AuthRouter
from infrastructure.config import ApplicationConfig
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


def init_app() -> Application:
    app = Application(
        middlewares=[
            middleware.logging_middleware
        ]
    )
    hash_service = HashService()
    jwt_service = JWTService(
        access_token_timedelta=timedelta(minutes=ApplicationConfig.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=ApplicationConfig.SECRET_KEY,
    )
    user_repository = UserRepository(manager)
    auth_router = AuthRouter(
        user_repository,
        hash_service,
        jwt_service,
    )
    app.add_subapp('/api/v1/auth', auth_router.setup_router())
    return app


if __name__ == '__main__':
    app: Application = init_app()
    initialize_database_tables()

    app.router.add_route(
        'GET', '/', ping
    )
    run_app(app, host='localhost', port=8000)
