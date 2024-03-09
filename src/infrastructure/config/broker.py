import os

import dotenv

dotenv.load_dotenv()


class BrokerConfig:
    BROKER_HOST: str = os.getenv('BROKER_HOST', 'localhost')
    BROKER_PORT: int = int(os.getenv('BROKER_PORT', 5672))
    BROKER_USER: str = os.getenv('BROKER_USER', 'guest')
    BROKER_PASSWORD: str = os.getenv('BROKER_PASSWORD', 'guest')
