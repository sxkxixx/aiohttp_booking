from typing import List, Union

from pydantic import BaseModel


class AbstractMessageData(BaseModel):
    """"""

    receiver: Union[str, List[str]]


class AbstractMessage(BaseModel):
    type: str
    message_data: AbstractMessageData
