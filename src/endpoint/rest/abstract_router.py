from abc import ABC, abstractmethod

from aiohttp.web import Application

__all__ = ['AbstractRouter']


class AbstractRouter(ABC):
    @abstractmethod
    def setup_endpoints(self, app: Application):
        raise NotImplementedError()
