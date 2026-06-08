from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from jose import jwt

from app.core.config import settings


class JWTService:
    """
    JWT encode/decode service.
    """

    def __init__(
        self,
        secret_key: str | None = None,
        algorithm: str | None = None,
        access_token_expire_minutes: int | None = None,
    ) -> None:
        self.secret_key = secret_key or settings.SECRET_KEY
        self.algorithm = algorithm or settings.ALGORITHM
        self.access_token_expire_minutes = (
            access_token_expire_minutes
            or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    def create_access_token(
        self,
        subject: str,
        extra_claims: Dict[str, Any] | None = None,
    ) -> str:
        now = datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "sub": str(subject),
            "iat": int(now.timestamp()),
            "exp": int(
                (
                    now + timedelta(minutes=self.access_token_expire_minutes)
                ).timestamp()
            ),
        }
        if extra_claims:
            payload.update(extra_claims)

        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])