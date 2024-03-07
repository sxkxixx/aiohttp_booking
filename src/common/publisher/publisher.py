from abc import ABC, abstractmethod

from common.messages import AbstractMessage


class BrokerPublisher(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def publish_message(self, message: AbstractMessage, queue_name: str) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError()

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()
