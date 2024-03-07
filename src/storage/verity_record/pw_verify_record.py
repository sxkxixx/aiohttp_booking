from peewee_async import Manager

from infrastructure.database.model import VerifyRecord
from .abstract_verify_record_repository import AbstractVerityRecordRepository


class PWVerifyRecordRepository(AbstractVerityRecordRepository):
    def __init__(self, manager: Manager):
        self.manager = manager

    async def create(self, *, token: str, user_id: int | str) -> VerifyRecord:
        verify_record: VerifyRecord = await self.manager.create(
            VerifyRecord, token=token, user_id=user_id
        )
        return verify_record

    async def get_verify_record_by_token(self, token: str) -> VerifyRecord:
        return await self.manager.get_or_none(
            VerifyRecord,
            VerifyRecord.token == token
        )
