import json
from typing import Optional, Any

import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel

from common.messages import AbstractMessage
from .publisher import BrokerPublisher


class PikaPublisher(BrokerPublisher):
    def __init__(
            self,
            host: str,
            port: int,
            username: Optional[str],
            password: Optional[str],
    ):
        self.__host: str = host
        self.__port: int = port
        self.__username: str = username
        self.__password: str = password

        self.__connection: Optional[AbstractConnection] = None
        self.__channel: Optional[AbstractChannel] = None

    @property
    def is_opened(self) -> bool:
        return not self.__connection.is_closed

    async def connect(self) -> None:
        self.__connection = await aio_pika.connect(
            host=self.__host,
            port=self.__port,
            login=self.__username,
            password=self.__password,
        )
        await self.open_channel()

    async def open_channel(self) -> None:
        if not self.is_opened:
            raise ConnectionError()
        self.__channel = self.__connection.channel()

    async def close_channel(self) -> None:
        if self.__channel:
            await self.__channel.close()

    async def disconnect(self) -> None:
        if not self.is_opened:
            return
        await self.close_channel()
        await self.__connection.close()

    async def publish_message(self, message: AbstractMessage, queue_name: str):
        json_view: dict[str, Any] = message.model_dump()
        aio_pika_message: aio_pika.abc.AbstractMessage = aio_pika.Message(
            body=json.dumps(json_view, default=str).encode('utf-8')
        )
        await self.__channel.default_exchange.publish(aio_pika_message, routing_key=queue_name)

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
