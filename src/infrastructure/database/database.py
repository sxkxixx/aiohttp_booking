import aiopg
from peewee import Model
from peewee_async import PooledPostgresqlDatabase, Manager

from config import DatabaseConfig

database = PooledPostgresqlDatabase(
    database=DatabaseConfig.DATABASE_NAME,
    user=DatabaseConfig.DATABASE_USER,
    password=DatabaseConfig.DATABASE_PASSWORD,
    host=DatabaseConfig.DATABASE_HOST,
    port=DatabaseConfig.DATABASE_PORT,
    connection_timeout=aiopg.DEFAULT_TIMEOUT
)
manager = Manager(database)


class Entity(Model):
    class Meta:
        database = database

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(primary_key={self._pk})'
