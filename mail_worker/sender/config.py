import os
from typing import Optional

import dotenv

dotenv.load_dotenv()


class SMTPConfig:
    SMTP_EMAIL: Optional[str] = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD: Optional[str] = os.getenv("SMTP_PASSWORD")
    SMTP_SERVER: Optional[str] = os.getenv("SMTP_SERVER")
    SMTP_PORT: Optional[str] = os.getenv("SMTP_PORT")
