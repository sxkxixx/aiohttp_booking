import smtplib
from email.message import EmailMessage

from sender.abstract_sender import AbstractSender


class SmtpSSLSender(AbstractSender):
    def __init__(self, host: str, port: int, user: str, password: str):
        self.__host: str = host
        self.__port: int = port
        self.__user: str = user
        self.__password: str = password

    def sendmail(self, message: EmailMessage) -> None:
        with smtplib.SMTP_SSL(host=self.__host, port=self.__port) as connection:
            connection.login(
                user=self.__user,
                password=self.__password
            )
            connection.send_message(message)
