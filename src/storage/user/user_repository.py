from typing import Optional

from peewee_async import Manager

from common.dto import UserRegisterRequest
from infrastructure.database.model import User
from storage.user.abstract_user_repository import AbstractUserRepository


class UserRepository(AbstractUserRepository):
    def __init__(
            self,
            manager: Manager,
    ) -> None:
        self._manager = manager

    async def create_user(self, user: UserRegisterRequest) -> User:
        return await self._manager.create(
            User, email=user.email, hashed_password=user.password
        )

    async def get_user(self, *filters) -> Optional[User]:
        return await self._manager.get_or_none(User, *filters)
