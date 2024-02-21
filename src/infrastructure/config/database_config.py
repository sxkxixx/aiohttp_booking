import os
from typing import Optional

import dotenv

dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME: Optional[str] = os.getenv('DATABASE_NAME')
    DATABASE_HOST: Optional[str] = os.getenv('DATABASE_HOST')
    DATABASE_PORT: int = int(os.getenv('DATABASE_PORT', 5432))
    DATABASE_USER: Optional[str] = os.getenv('DATABASE_USER')
    DATABASE_PASSWORD: Optional[str] = os.getenv('DATABASE_PASSWORD')

    def url(self) -> str:
        return (
            f'postgresql+aiopg://'
            f'{self.DATABASE_USER}:{self.DATABASE_PASSWORD}'
            f'@{self.DATABASE_HOST}:{self.DATABASE_PORT}'
            f'/{self.DATABASE_NAME}'
        )
