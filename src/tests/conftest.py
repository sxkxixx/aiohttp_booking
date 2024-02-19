import asyncio
import logging

import aiopg
import pytest_asyncio
from peewee_async import PooledPostgresqlDatabase, Manager

from infrastructure.config.database_config import DatabaseConfig
from main import MODELS

logging.basicConfig(
    format=(
        "%(asctime)s - [%(levelname)s] - %(name)s - "
        "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    )
)


@pytest_asyncio.fixture(scope='session', autouse=True)
async def event_loop():
    loop = asyncio.get_event_loop()
    yield loop


@pytest_asyncio.fixture(scope='session', autouse=True)
async def manager():
    database = PooledPostgresqlDatabase(
        database=DatabaseConfig.DATABASE_NAME,
        user=DatabaseConfig.DATABASE_USER,
        password=DatabaseConfig.DATABASE_PASSWORD,
        host=DatabaseConfig.DATABASE_HOST,
        port=DatabaseConfig.DATABASE_PORT,
        connection_timeout=aiopg.DEFAULT_TIMEOUT,
    )
    database._allow_sync = False
    manager = Manager(database)
    with manager.allow_sync():
        for model in MODELS:
            model._meta.database = database
            model.create_table(True)
    yield manager


@pytest_asyncio.fixture(scope='function', autouse=True)
async def truncate_tables(manager):
    yield
    with manager.allow_sync():
        for model in MODELS:
            model.truncate_table(cascade=True)
