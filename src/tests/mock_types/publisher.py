from common.messages import AbstractMessage
from common.publisher.publisher import BrokerPublisher


class MockPublisher(BrokerPublisher):
    async def connect(self) -> None:
        pass

    async def disconnect(self) -> None:
        pass

    async def publish_message(self, message: AbstractMessage, queue_name: str) -> None:
        pass

    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
