import os

import dotenv

dotenv.load_dotenv()


class ApplicationConfig:
    SECRET_KEY: str = os.getenv("SECRET_KEY", os.urandom(24).hex())

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 5))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 15))
