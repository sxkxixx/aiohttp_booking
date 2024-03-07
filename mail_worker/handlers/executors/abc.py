from abc import ABC, abstractmethod

from sender.abstract_sender import AbstractSender


class AbstractExecutor(ABC):
    name: str

    def __init__(self, sender: AbstractSender):
        self.sender = sender

    @abstractmethod
    async def execute(self, *args, **kwargs):
        raise NotImplementedError()
