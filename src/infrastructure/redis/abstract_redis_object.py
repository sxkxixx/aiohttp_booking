from abc import ABC, abstractmethod


class AbstractRedisObject(ABC):
    @abstractmethod
    def json(self) -> dict[str, str]:
        raise NotImplemented()

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict[str, str]) -> 'AbstractRedisObject':
        raise NotImplemented()
