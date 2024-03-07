import logging
from datetime import timedelta

from aiohttp.web import Application, run_app

import middleware
from common.publisher import PikaPublisher
from common.service import HashService, JWTService
from endpoint.rest import AuthRouter
from infrastructure.config import ApplicationConfig
from infrastructure.config.broker import BrokerConfig
from infrastructure.database.database import manager, database
from infrastructure.database.model import User, VerifyRecord
from storage.user import UserRepository
from storage.verity_record.pw_verify_record import PWVerifyRecordRepository

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig(
    format=(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
)

MODELS = [User, VerifyRecord]


def initialize_database_tables() -> None:
    with database:
        database.create_tables(MODELS)


def init_app() -> Application:
    _app = Application(
        middlewares=[middleware.logging_middleware]
    )
    hash_service = HashService()
    jwt_service = JWTService(
        access_token_timedelta=timedelta(minutes=ApplicationConfig.ACCESS_TOKEN_EXPIRE_MINUTES),
        secret_key=ApplicationConfig.SECRET_KEY,
    )
    user_repository = UserRepository(manager)
    verify_record_repository = PWVerifyRecordRepository(manager)
    publisher = PikaPublisher(
        host=BrokerConfig.BROKER_HOST,
        port=BrokerConfig.BROKER_PORT,
        username=BrokerConfig.BROKER_USER,
        password=BrokerConfig.BROKER_PASSWORD
    )
    auth_router = AuthRouter(
        user_repository,
        verify_record_repository,
        publisher,
        hash_service,
        jwt_service,
    )
    _app.add_subapp('/api/v1/auth', auth_router.setup_router())
    return _app


if __name__ == '__main__':
    app: Application = init_app()
    initialize_database_tables()
    run_app(app, host='localhost', port=8000)
