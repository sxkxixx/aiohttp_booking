from abc import ABC, abstractmethod
from email.message import EmailMessage


class AbstractSender(ABC):
    @abstractmethod
    def sendmail(self, message: EmailMessage) -> None:
        raise NotImplementedError()
