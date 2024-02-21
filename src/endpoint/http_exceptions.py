from aiohttp.web_exceptions import HTTPException


class UnauthorizedException(HTTPException):
    status_code: int = 401


class NotFoundException(HTTPException):
    status_code: int = 404


class UniqueEmailException(HTTPException):
    status_code: int = 404
    message: str = "Email address must be unique"


class BadRequestException(HTTPException):
    status_code: int = 400
