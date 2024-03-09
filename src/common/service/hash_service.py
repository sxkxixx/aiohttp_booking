from passlib.context import CryptContext


class HashService:
    pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def get_str_hash(self, secret: str) -> str:
        return self.pwd_context.hash(secret)

    def equals(self, plain: str, hashed_str: str) -> bool:
        return self.pwd_context.verify(plain, hashed_str)
