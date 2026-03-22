import time
import base64
import logging
import jwt
import requests
from config import settings

logger = logging.getLogger("obsidian_workflow_bot")

VAULT_REPO = settings.VAULT_REPO


def _generate_jwt() -> str:
    now = int(time.time())
    payload = {
        "iat": now - 60,
        "exp": now + (10 * 60),
        "iss": settings.GITHUB_APP_ID,
    }
    private_key = settings.GITHUB_APP_PRIVATE_KEY.replace("\\n", "\n")
    return jwt.encode(payload, private_key, algorithm="RS256")


def get_installation_token() -> str:
    app_jwt = _generate_jwt()
    headers = {
        "Authorization": f"Bearer {app_jwt}",
        "Accept": "application/vnd.github+json",
    }

    resp = requests.get("https://api.github.com/app/installations", headers=headers)
    resp.raise_for_status()

    installations = resp.json()
    installation = next(
        (i for i in installations if i["account"]["login"] == "akshat-315"), None
    )
    if installation is None:
        raise ValueError("GitHub App installation not found for akshat-315")

    token_resp = requests.post(
        f"https://api.github.com/app/installations/{installation['id']}/access_tokens",
        headers=headers,
    )
    token_resp.raise_for_status()
    token = token_resp.json()["token"]
    logger.debug("GitHub installation token obtained")
    return token


def create_file(token: str, path: str, content: str, message: str) -> None:
    encoded = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json",
    }
    body = {"message": message, "content": encoded}

    resp = requests.put(
        f"https://api.github.com/repos/{VAULT_REPO}/contents/{path}",
        headers=headers,
        json=body,
    )
    resp.raise_for_status()
    logger.info(f"Created file in vault: {path}")
