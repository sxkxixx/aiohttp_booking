from abc import ABC, abstractmethod

from infrastructure.database.model import VerifyRecord


class AbstractVerityRecordRepository(ABC):
    @abstractmethod
    async def create(self, *, token: str, user_id: int | str) -> VerifyRecord:
        raise NotImplementedError()

    @abstractmethod
    async def get_verify_record_by_token(self, token: str) -> VerifyRecord:
        raise NotImplementedError()
