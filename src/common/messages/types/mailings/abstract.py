from typing import List, Union

from common.messages.types.abstract import AbstractMessageData


class AbstractEmailMessageData(AbstractMessageData):
    receiver: Union[List[str], str]
