import os
from typing import Optional

import dotenv

dotenv.load_dotenv()


class RedisConfig:
    HOST: str = os.getenv('REDIS_HOST', 'localhost')
    PORT: int = int(os.getenv('REDIS_PORT', 6379))
    USERNAME: Optional[str] = os.getenv('REDIS_USERNAME')
    PASSWORD: Optional[str] = os.getenv('REDIS_PASSWORD')
