"""Small client for the OpenRouter API (the same AI service used in the mobile app)."""

import json
import re

import requests
from django.conf import settings

API_URL = "https://openrouter.ai/api/v1/chat/completions"


class AIError(Exception):
    """Raised when the AI service can't be used (no key, no internet, bad answer)."""


def is_ready() -> bool:
    return bool(settings.OPENROUTER_API_KEY)


def ask_json(system_prompt: str, user_prompt: str, max_tokens: int = 500) -> dict:
    """Send a prompt and return the AI answer as a Python dictionary."""
    if not is_ready():
        raise AIError("OPENROUTER_API_KEY is not set in the .env file")

    try:
        response = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",
                "X-Title": "Ihdhar",
            },
            json={
                "model": settings.OPENROUTER_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "temperature": 0.1,
                "max_tokens": max_tokens,
                "response_format": {"type": "json_object"},
            },
            timeout=30,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
    except (requests.RequestException, KeyError, IndexError, ValueError) as error:
        raise AIError(str(error)) from error

    return parse_json(content)


def parse_json(text: str) -> dict:
    """Read JSON even if the AI wrapped it in ```json ... ``` or added extra words."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise AIError("The AI answer has no JSON")
    try:
        return json.loads(match.group())
    except json.JSONDecodeError as error:
        raise AIError("The AI answer is not valid JSON") from error
