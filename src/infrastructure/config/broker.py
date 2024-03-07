import os

import dotenv

dotenv.load_dotenv()


class BrokerConfig:
    BROKER_HOST: str = os.getenv('BROKER_HOST')
    BROKER_PORT: int = int(os.getenv('BROKER_PORT'))
    BROKER_USER: str = os.getenv('BROKER_USER')
    BROKER_PASSWORD: str = os.getenv('BROKER_PASSWORD')
