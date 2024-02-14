import peewee

from .database import Entity


class User(Entity):
    class Meta:
        table_name = 'users'

    id: int = peewee.BigAutoField(primary_key=True)
    email: str = peewee.CharField(max_length=128, unique=True, index=True, null=False)
    hashed_password: str = peewee.CharField(max_length=128, null=False)

