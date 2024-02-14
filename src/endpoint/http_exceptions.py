from typing import Dict

from aiohttp import http_exceptions


class NotFoundException(http_exceptions.HttpProcessingError):
    code: int = 404

    def __init__(
            self,
            message: str = "Request object not found",
            headers: Dict = None
    ) -> None:
        super().__init__(code=self.code, message=message, headers=headers)


class UniqueEmailException(http_exceptions.HttpProcessingError):
    code: int = 404
    message: str = "Email address must be unique"

    def __init__(
            self,
            headers: Dict = None
    ):
        super().__init__(code=self.code, message=self.message, headers=headers)


class BadRequestException(http_exceptions.HttpProcessingError):
    code: int = 400

    def __init__(
            self,
            message: str = "Bad request",
            headers: Dict = None
    ) -> None:
        super().__init__(code=self.code, message=message, headers=headers)
