import os
from typing import Optional

import dotenv

dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME: Optional[str] = os.environ.get('DATABASE_NAME')
    DATABASE_HOST: Optional[str] = os.environ.get('DATABASE_HOST')
    DATABASE_PORT: int = int(os.environ.get('DATABASE_PORT', 8080))
    DATABASE_USER: Optional[str] = os.environ.get('DATABASE_USER')
    DATABASE_PASSWORD: Optional[str] = os.environ.get('DATABASE_PASSWORD')
