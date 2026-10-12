"""Password hashing and JWT access token helpers shared across modules."""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from backend.core.config import settings
from backend.core.exceptions import AuthenticationError


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        # Hash malformado (p. ej. config de bootstrap vacía): nunca autentica.
        return False


@dataclass(frozen=True, slots=True)
class TokenPayload:
    user_id: int
    username: str
    roles: list[str]
    permissions: list[str]


def create_access_token(
    *, user_id: int, username: str, roles: list[str], permissions: list[str]
) -> str:
    now = datetime.now(UTC)
    payload = {
        "sub": str(user_id),
        "username": username,
        "roles": roles,
        "permissions": permissions,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt.access_token_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def decode_access_token(token: str) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
    except jwt.PyJWTError as exc:
        raise AuthenticationError("Invalid or expired access token") from exc
    return TokenPayload(
        user_id=int(payload["sub"]),
        username=payload.get("username", ""),
        roles=payload.get("roles", []),
        permissions=payload.get("permissions", []),
    )
