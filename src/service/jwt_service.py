from datetime import timedelta, datetime
from typing import Optional

from jose import jwt
from jose.constants import Algorithms

from dto.user import Token
from infrastructure.database.model import User


class JWTService:
    def __init__(
            self,
            access_token_timedelta: timedelta,
            secret_key: str
    ):
        """
        :param access_token_timedelta: Время жизни access токена
        :param secret_key: Секретный ключ
        """
        self._access_token_timedelta: timedelta = access_token_timedelta
        self.__secret_key = secret_key

    def get_access_token(self, user: User) -> str:
        """
        Возвращает закодированный JWT токен
        :param user: Пользователь
        :return: JWT Access Token
        """
        token: dict = Token(email=user.email, token_type="Access Token").model_dump()
        exp: datetime = datetime.utcnow() + self._access_token_timedelta
        token.update({'exp': exp})
        return jwt.encode(token, self.__secret_key, algorithm=Algorithms.HS256)

    def get_token_payload(self, jwt_token: str) -> Optional[dict]:
        """
        Возвращает payload токена или None если вылетело исключение
        :param jwt_token: Токен
        :return: Dict | None
        """
        try:
            return jwt.decode(jwt_token, self.__secret_key, algorithms=[Algorithms.HS256])
        except jwt.JWTError:
            return None
