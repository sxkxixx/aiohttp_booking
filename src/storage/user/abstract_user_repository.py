from abc import ABC, abstractmethod
from typing import Optional

from common.dto import UserRegisterRequest
from infrastructure.database.model import User


class AbstractUserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: UserRegisterRequest) -> User:
        raise NotImplementedError()

    @abstractmethod
    async def get_user(self, *filters) -> Optional[User]:
        raise NotImplementedError()
