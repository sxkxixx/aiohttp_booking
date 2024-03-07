class ConsumingException(Exception):
    def __init__(self, message: str):
        self.message = message

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.message}>'


class InvalidMessageException(ConsumingException):
    """"""


class UnknownMessageException(ConsumingException):
    """"""
