from __future__ import annotations
from typing import Any
import requests


class APIAdapter:
    """Simple HTTP API adapter."""

    def fetch(self, url: str) -> Any:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return response.text
