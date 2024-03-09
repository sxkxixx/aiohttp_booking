import json
import logging
from typing import Optional

from aio_pika.abc import AbstractMessage

from .abc import AbstractHandler
from .exceptions import InvalidMessageException, UnknownMessageException
from .executors import AbstractExecutor

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MailHandler(AbstractHandler):
    NO_TYPE_IN_MESSAGE = "The received message does not contain the type"
    NO_EXECUTOR_FOR_RECEIVED_MESSAGE = "No executor for received message"

    def __init__(self):
        self.__executors: dict[str, AbstractExecutor] = {}

    def register_executor(self, executor: AbstractExecutor) -> None:
        if self.__executors.get(executor.name):
            return
        self.__executors[executor.name] = executor

    async def handle(self, message: AbstractMessage) -> None:
        body: dict[str, str] = json.loads(message.body.decode('utf-8'))
        _type_ = body.get('type', None)
        if not _type_:
            logger.error('Message does not contains type')
            raise InvalidMessageException(message=self.NO_TYPE_IN_MESSAGE)
        logger.info('Handling message with type={ %s }' % _type_)
        executor: Optional[AbstractExecutor] = self.__executors.get(_type_, None)
        if not executor:
            logger.error('No executor to execute this message')
            raise UnknownMessageException(message=self.NO_EXECUTOR_FOR_RECEIVED_MESSAGE)
        await executor.execute(body)
