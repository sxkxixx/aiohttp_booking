import asyncio
import logging
from asyncio import AbstractEventLoop
from typing import Optional

from aio_pika import Connection, connect
from aio_pika.abc import AbstractChannel, AbstractQueue, AbstractConnection
from aio_pika.connection import make_url

from handlers.abc import AbstractHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Consumer:
    NO_CONNECTION_MESSAGE = "No connection"

    def __init__(
            self,
            *,
            host: str,
            port: int,
            user: str,
            password: str,
            queue_name: str,
            handler: AbstractHandler
    ):
        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._queue_name: str = queue_name
        self._handler: AbstractHandler = handler

        self.__connection: Optional[Connection] = None
        self.__channel: Optional[AbstractChannel] = None
        self.__queue: Optional[AbstractQueue] = None

    @property
    def is_opened(self) -> bool:
        return self.__connection and not self.__connection.is_closed

    async def start_consuming(self) -> None:
        if not self.is_opened or not self.__channel:
            logger.error(f'{self.is_opened=}, {self.__channel=} {self.__channel.is_closed=}')
            raise ConnectionError('You must connect and open chanel before consuming')
        await self.__channel.initialize()
        self.__queue: AbstractQueue = await self.__channel.declare_queue(self._queue_name)
        assert self.__queue.name == self._queue_name
        logger.info(f'Consuming queue {self.__queue.name}')
        await self.__queue.consume(callback=self._handler.handle)

    async def connect(self, loop: Optional[AbstractEventLoop] = None) -> None:
        """
        Connects to Broker (RabbitMQ)
        :param loop: Event Loop
        :return: None
        """
        if loop is None:
            loop = asyncio.get_running_loop()
        self.__connection: AbstractConnection = await connect(
            make_url(host=self._host, port=self._port, login=self._user, password=self._password),
            loop=loop
        )
        logger.info('Connection is opened')

    async def open_channel(self) -> None:
        """
        Opens channel to RabbitMQ
        :return: None
        :raises ConnectionError: If no connection
        """
        if not self.is_opened:
            logger.error('Connection was not initialized')
            raise ConnectionError('You must connect before opening channel')
        if self.__channel:
            await self.__channel.reopen()
            logger.info('Channel is reopened')
            return
        self.__channel: AbstractChannel = self.__connection.channel()
        logger.info(f'{self.__channel.is_closed=}')
        logger.info('Channel is opened')

    async def close_channel(self) -> None:
        """
        Closes the channel
        :return:
        """
        if not self.__channel:
            return
        await self.__channel.close()
        logger.info('Channel is closed')

    async def disconnect(self) -> None:
        """
        Close the connection
        :return:
        """
        if not self.is_opened:
            return
        await self.__connection.close()
        logger.info('Connection is closed')

    def __str__(self) -> str:
        return f"""Consumer(
            host={self._host}
            port={self._port}
            user={self._user}
            queue_name={self._queue_name}
        )"""

    def __repr__(self) -> str:
        return self.__str__()
