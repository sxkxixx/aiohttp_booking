from abc import ABC, abstractmethod

from aio_pika.abc import AbstractMessage

from .executors import AbstractExecutor


class AbstractHandler(ABC):
    @abstractmethod
    def register_executor(self, executor: AbstractExecutor) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def handle(self, message: AbstractMessage) -> None:
        raise NotImplementedError()
