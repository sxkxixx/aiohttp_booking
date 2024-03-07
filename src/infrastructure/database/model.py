from datetime import datetime

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
    is_verified: bool = peewee.BooleanField(default=False)


class VerifyRecord(Entity):
    """Model for collecting data about user's verification"""

    class Meta:
        table_name = 'verification_records'

    token: str = peewee.CharField(max_length=128, index=True, unique=True)
    user: User = peewee.ForeignKeyField(User, field=User.id, unique=True, primary_key=True)
    created_at: datetime = peewee.DateTimeField(default=datetime.utcnow)
    verified_at: datetime = peewee.DateTimeField(null=True) 
