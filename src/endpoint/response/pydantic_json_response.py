import json
from concurrent.futures import Executor
from typing import Optional

from aiohttp.typedefs import LooseHeaders
from aiohttp.web import Response
from pydantic import BaseModel


class PydanticJsonResponse(Response):
    def __init__(
            self,
            *,
            body: BaseModel,
            status: int = 200,
            reason: Optional[str] = None,
            text: Optional[str] = None,
            headers: Optional[LooseHeaders] = None,
            charset: Optional[str] = None,
            zlib_executor_size: Optional[int] = None,
            zlib_executor: Optional[Executor] = None,
    ) -> None:
        super().__init__(
            body=json.dumps(body.model_dump()),
            status=status,
            reason=reason,
            text=text,
            headers=headers,
            content_type="application/json",
            charset=charset,
            zlib_executor_size=zlib_executor_size,
            zlib_executor=zlib_executor,
        )
