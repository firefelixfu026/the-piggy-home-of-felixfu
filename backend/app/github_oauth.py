import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from fastapi import HTTPException


GITHUB_AUTHORIZE_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_URL = "https://api.github.com/user"
GITHUB_EMAILS_URL = "https://api.github.com/user/emails"


def get_github_authorize_url(state: str) -> str:
    client_id = _required_env("GITHUB_CLIENT_ID")
    redirect_uri = _github_callback_url()
    params = urlencode(
        {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": "read:user user:email",
            "state": state,
        }
    )
    return f"{GITHUB_AUTHORIZE_URL}?{params}"


def fetch_github_identity(code: str) -> tuple[dict, str | None]:
    access_token = _exchange_code_for_token(code)
    user = _github_get(GITHUB_USER_URL, access_token)
    email = _fetch_primary_email(access_token) or user.get("email")
    return user, email


def _exchange_code_for_token(code: str) -> str:
    client_id = _required_env("GITHUB_CLIENT_ID")
    client_secret = _required_env("GITHUB_CLIENT_SECRET")
    payload = urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": _github_callback_url(),
        }
    ).encode("utf-8")
    request = Request(
        GITHUB_TOKEN_URL,
        data=payload,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "FelixFu-Blog",
        },
        method="POST",
    )
    response = _request_json(request)
    access_token = response.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail=response.get("error_description") or "GitHub token exchange failed")
    return access_token


def _fetch_primary_email(access_token: str) -> str | None:
    emails = _github_get(GITHUB_EMAILS_URL, access_token)
    if not isinstance(emails, list):
        return None

    verified = [item for item in emails if item.get("verified") and item.get("email")]
    primary = next((item for item in verified if item.get("primary")), None)
    selected = primary or (verified[0] if verified else None)
    if not selected:
        return None
    return selected["email"].strip().lower()


def _github_get(url: str, access_token: str) -> dict | list:
    request = Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}",
            "User-Agent": "FelixFu-Blog",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    return _request_json(request)


def _request_json(request: Request) -> dict | list:
    try:
        with urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore") or "GitHub request failed"
        raise HTTPException(status_code=400, detail=detail) from exc
    except (URLError, TimeoutError) as exc:
        raise HTTPException(status_code=502, detail="GitHub is not reachable") from exc


def _github_callback_url() -> str:
    return os.getenv("GITHUB_OAUTH_CALLBACK_URL", "http://127.0.0.1:8000/api/auth/github/callback").strip()


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value:
        raise HTTPException(status_code=503, detail=f"{name} is not configured")
    return value
