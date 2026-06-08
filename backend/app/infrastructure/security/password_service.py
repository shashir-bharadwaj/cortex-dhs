from passlib.context import CryptContext


class PasswordService:
    """
    Password hashing and verification service.
    """

    def __init__(self) -> None:
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        return self._pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str, password_hash: str) -> bool:
        return self._pwd_context.verify(plain_password, password_hash)