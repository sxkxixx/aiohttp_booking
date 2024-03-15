import argparse
import asyncio
import logging

from jinja2 import Environment, FileSystemLoader

from consumer.consumer import Consumer
from handlers import MailHandler
from handlers.executors import *
from sender.config import SMTPConfig
from sender.smtp import SmtpSSLSender

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)s(%(lineno)d) - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_jinja2_environment() -> Environment:
    env = Environment(
        loader=FileSystemLoader('templates'),
        enable_async=True
    )
    return env


def parse_argv() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(
        prog='Worker service to consume mail message',
        add_help=False
    )
    arg_parser.add_argument('--host', '-h', required=True)
    arg_parser.add_argument('--port', '-p', required=True, type=int)
    arg_parser.add_argument('--user', '-u', required=False, default='guest')
    arg_parser.add_argument('--password', '-pw', required=False, default='guest')
    arg_parser.add_argument('--queue_name', '-q', required=True)
    args: argparse.Namespace = arg_parser.parse_args()
    logger.info('Argv is parsed correctly')
    return args


async def main(_loop: asyncio.AbstractEventLoop) -> None:
    args: argparse.Namespace = parse_argv()
    jinja_template_env = get_jinja2_environment()
    handler = MailHandler()
    sender = SmtpSSLSender(
        host=SMTPConfig.SMTP_SERVER,
        port=SMTPConfig.SMTP_PORT,
        user=SMTPConfig.SMTP_EMAIL,
        password=SMTPConfig.SMTP_PASSWORD,
    )
    handler.register_executor(VerifyEmailExecutor(sender, jinja_template_env))
    consumer = Consumer(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        queue_name=args.queue_name,
        handler=handler
    )
    try:
        await consumer.connect(loop)
        await consumer.open_channel()
        await consumer.start_consuming()
    except ConnectionError as e:
        print(e)
    except InterruptedError:
        await consumer.close_channel()
        await consumer.disconnect()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
