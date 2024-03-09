from pydantic import BaseModel

__all__ = [
    'AbstractMessage',
    'AbstractMessageData'
]


class AbstractMessageData(BaseModel):
    """"""


class AbstractMessage(BaseModel):
    type: str
    message_data: AbstractMessageData
