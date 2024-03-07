from email.message import EmailMessage
from typing import Any

from sender.config import SMTPConfig
from .abc import AbstractExecutor


class VerifyEmailExecutor(AbstractExecutor):
    # TODO: Организовать работу с HTML шаблонами сообщений
    name = 'verify_email'
    subject = 'Подтверждение почты'

    async def execute(self, kwargs: dict[str, Any]) -> None:
        message = EmailMessage()
        message['From'] = SMTPConfig.SMTP_EMAIL
        message['To'] = kwargs.get('message_data').get('receiver')
        message['Subject'] = self.subject
        message.set_content(TEMPLATE, subtype='html')
        self.sender.sendmail(message)


TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap"
          rel="stylesheet">
    <style>
        body {
            font-family: "Roboto", sans-serif;
            font-weight: 400;
            font-style: normal;
        }
        .header {
            background-color: #33CCCC;
            padding: 10px 20px 40px;
            border-radius: 25px;
        }
    </style>
</head>
<body style="">
<div style="display: flex; justify-content: center">
    <div>
        <div class="header">
            <h1>Регистрация в сервисе бронирования</h1>
        </div>

    </div>
</div>
</body>
</html>
"""
