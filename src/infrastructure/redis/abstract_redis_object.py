from abc import ABC, abstractmethod


class AbstractRedisObject(ABC):
    @abstractmethod
    def json(self) -> dict[str, str]:
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_json(cls, json: dict[str, str]) -> 'AbstractRedisObject':
        raise NotImplementedError()

    @abstractmethod
    def json_encoded(self) -> str:
        raise NotImplementedError()
