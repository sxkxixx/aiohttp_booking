import json
from datetime import timedelta
from typing import Union
from uuid import UUID

from infrastructure.redis import AbstractRedisObject


class UserSession(AbstractRedisObject):
    def __init__(
            self,
            user_id: Union[int, str, UUID],
            ip_address: str,
            fingerprint: str,
            user_agent: str
    ) -> None:
        """
        :param user_id: ID пользователя
        :param ip_address: IP-адрес хоста, инициализировавшего запрос
        :param fingerprint: Подпись браузера
        :param user_agent: Заголовок User-Agent
        """
        self.user_id = user_id
        self.ip_address = ip_address
        self.fingerprint = fingerprint
        self.user_agent = user_agent

    def json(self) -> dict[str, str]:
        return dict(
            user_id=self.user_id,
            ip_address=self.ip_address,
            fingerprint=self.fingerprint,
            user_agent=self.user_agent
        )

    def json_encoded(self) -> str:
        return json.dumps(self.json(), default=str)

    @classmethod
    def from_json(cls, json: dict[str, str]) -> 'UserSession':
        return cls(**json)

    @property
    def session_ttl(self) -> timedelta:
        return timedelta(days=15)

    def is_valid(
            self,
            ip_address: str,
            fingerprint: str,
            user_agent: str
    ) -> bool:
        return (
                ip_address == self.ip_address
                and fingerprint == self.fingerprint
                and user_agent == self.user_agent
        )
