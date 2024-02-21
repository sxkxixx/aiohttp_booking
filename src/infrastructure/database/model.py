import peewee

from .database import database


class Entity(peewee.Model):
    class Meta:
        database = database

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(primary_key={self._pk})'


class User(Entity):
    class Meta:
        table_name = 'users'

    id: int = peewee.BigAutoField(primary_key=True)
    email: str = peewee.CharField(max_length=128, unique=True, index=True, null=False)
    hashed_password: str = peewee.CharField(max_length=128, null=False)
