import hashlib
import hmac
import secrets
import string
from datetime import datetime, timedelta, timezone

import argon2
import jwt
from argon2.low_level import Type


def hash_password(plain: str) -> str:
    hasher = argon2.PasswordHasher(type=Type.ID)
    return hasher.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    hasher = argon2.PasswordHasher(type=Type.ID)
    try:
        return hasher.verify(hashed, plain)
    except (argon2.exceptions.VerifyMismatchError, argon2.exceptions.InvalidHashError):
        return False


def create_access_token(
    user_id: str,
    org_id: str,
    role: str,
    expires_minutes: int = 60,
) -> str:
    from app.config import settings

    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=expires_minutes)
    payload = {
        "sub": user_id,
        "org_id": org_id,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int(expires.timestamp()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_access_token(token: str) -> dict:
    from app.config import settings

    return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


def generate_agent_api_key(pepper: str) -> tuple[str, str, str]:
    alphabet = string.ascii_lowercase + string.digits
    prefix_part = "".join(secrets.choice(alphabet) for _ in range(12))
    secret_part = secrets.token_hex(16)
    raw_key = f"tl_live_{prefix_part}_{secret_part}"

    key_hash = hmac.new(
        pepper.encode("utf-8"),
        raw_key.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    prefix = f"tl_live_{prefix_part}"
    return raw_key, prefix, key_hash


def verify_agent_api_key(raw_key: str, stored_hash: str, pepper: str) -> str:
    computed_hash = hmac.new(
        pepper.encode("utf-8"),
        raw_key.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(computed_hash, stored_hash)