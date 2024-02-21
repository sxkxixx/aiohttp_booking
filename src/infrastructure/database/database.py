import aiopg
from peewee_async import PooledPostgresqlDatabase, Manager

from infrastructure.config import DatabaseConfig

database = PooledPostgresqlDatabase(
    database=DatabaseConfig.DATABASE_NAME,
    user=DatabaseConfig.DATABASE_USER,
    password=DatabaseConfig.DATABASE_PASSWORD,
    host=DatabaseConfig.DATABASE_HOST,
    port=DatabaseConfig.DATABASE_PORT,
    connection_timeout=aiopg.DEFAULT_TIMEOUT
)
manager = Manager(database)
