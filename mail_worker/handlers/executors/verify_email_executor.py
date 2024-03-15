from email.message import EmailMessage
from typing import Any

from jinja2 import Environment, Template

from sender.abstract_sender import AbstractSender
from sender.config import SMTPConfig
from messages import VerificationMessage
from .abc import AbstractExecutor


class VerifyEmailExecutor(AbstractExecutor):
    name = 'verify_email'
    template_name = 'verify_email.html'
    subject = 'Подтверждение почты'

    def __init__(self, sender: AbstractSender, env: Environment):
        self.env = env
        super().__init__(sender)

    async def execute(self, kwargs: dict[str, Any]) -> None:
        message_schema = VerificationMessage.model_validate(
            kwargs, from_attributes=True
        )
        email_message: EmailMessage = self.__get_message(
            message_schema.message_data.receiver
        )
        context = {
            'link': f'http://localhost:8000?verify_token={message_schema.message_data.verify_token}'
        }
        template = await self.__get_rendered_template(context)
        email_message.set_content(template, subtype='html')
        self.sender.sendmail(email_message)

    async def __get_rendered_template(
            self,
            context: dict[str, Any]
    ) -> str:
        template: Template = self.env.get_template(self.template_name)
        return await template.render_async(**context)

    def __get_message(self, receiver: str) -> EmailMessage:
        message = EmailMessage()
        message['From'] = SMTPConfig.SMTP_EMAIL
        message['To'] = receiver
        message['Subject'] = self.subject
        return message
