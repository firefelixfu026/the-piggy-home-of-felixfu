import base64
import hashlib
import hmac
import json
import os
import secrets
import time

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


AUTH_SECRET = os.getenv("AUTH_SECRET", "felix-blog-local-dev-secret-change-me")
TOKEN_TTL_SECONDS = int(os.getenv("AUTH_TOKEN_TTL_SECONDS", str(7 * 24 * 60 * 60)))
OAUTH_STATE_TTL_SECONDS = int(os.getenv("OAUTH_STATE_TTL_SECONDS", "600"))
PASSWORD_ALGORITHM = "pbkdf2_sha256"
PASSWORD_ITERATIONS = 210_000


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        PASSWORD_ITERATIONS,
    ).hex()
    return f"{PASSWORD_ALGORITHM}${PASSWORD_ITERATIONS}${salt}${digest}"


def verify_password(password: str, stored_hash: str | None) -> bool:
    if not stored_hash:
        return False

    try:
        algorithm, iterations, salt, expected = stored_hash.split("$", 3)
    except ValueError:
        return False

    if algorithm != PASSWORD_ALGORITHM:
        return False

    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        int(iterations),
    ).hex()
    return hmac.compare_digest(digest, expected)


def create_access_token(user: User) -> str:
    now = int(time.time())
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.display_name,
        "role": user.role,
        "iat": now,
        "exp": now + TOKEN_TTL_SECONDS,
    }
    header = {"alg": "HS256", "typ": "JWT"}
    signing_input = f"{_b64_json(header)}.{_b64_json(payload)}"
    signature = hmac.new(AUTH_SECRET.encode("utf-8"), signing_input.encode("utf-8"), hashlib.sha256).digest()
    return f"{signing_input}.{_b64_encode(signature)}"


def create_oauth_state(next_path: str = "/") -> str:
    now = int(time.time())
    payload = {
        "nonce": secrets.token_urlsafe(16),
        "next": next_path,
        "iat": now,
        "exp": now + OAUTH_STATE_TTL_SECONDS,
    }
    payload_part = _b64_json(payload)
    signature = hmac.new(AUTH_SECRET.encode("utf-8"), payload_part.encode("utf-8"), hashlib.sha256).digest()
    return f"{payload_part}.{_b64_encode(signature)}"


def verify_oauth_state(state: str) -> dict:
    try:
        payload_part, signature_part = state.split(".", 1)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid OAuth state") from exc

    expected_signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        payload_part.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64_encode(expected_signature), signature_part):
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    try:
        payload = json.loads(_b64_decode(payload_part))
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Invalid OAuth state") from exc

    if int(payload.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=400, detail="OAuth state has expired")
    return payload


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authentication is required")

    payload = _decode_token(authorization.removeprefix("Bearer ").strip())
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        parsed_user_id = int(user_id)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    user = db.get(User, parsed_user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User no longer exists")
    return user


def get_optional_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
) -> User | None:
    if not authorization:
        return None
    try:
        return get_current_user(authorization=authorization, db=db)
    except HTTPException:
        return None


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin permission is required")
    return current_user


def _decode_token(token: str) -> dict:
    try:
        header_part, payload_part, signature_part = token.split(".", 2)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    signing_input = f"{header_part}.{payload_part}"
    expected_signature = hmac.new(
        AUTH_SECRET.encode("utf-8"),
        signing_input.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    if not hmac.compare_digest(_b64_encode(expected_signature), signature_part):
        raise HTTPException(status_code=401, detail="Invalid token")

    try:
        header = json.loads(_b64_decode(header_part))
        payload = json.loads(_b64_decode(payload_part))
    except Exception as exc:
        raise HTTPException(status_code=401, detail="Invalid token") from exc

    if header.get("alg") != "HS256":
        raise HTTPException(status_code=401, detail="Invalid token")

    if int(payload.get("exp", 0)) < int(time.time()):
        raise HTTPException(status_code=401, detail="Token has expired")
    return payload


def _b64_json(value: dict) -> str:
    return _b64_encode(json.dumps(value, separators=(",", ":"), ensure_ascii=False).encode("utf-8"))


def _b64_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).decode("ascii").rstrip("=")


def _b64_decode(value: str) -> str:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode(value + padding).decode("utf-8")
