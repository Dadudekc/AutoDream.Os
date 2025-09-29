"""
Secret Store
============
Secure storage for webhook URLs outside the repository.
"""

import json
import os
from pathlib import Path
from typing import Any

# Default storage directory (Windows ProgramData)
DEFAULT_DIR = Path(os.getenv("V2_SWARM_SECRETS_DIR", r"C:\ProgramData\V2_SWARM"))
DEFAULT_DIR.mkdir(parents=True, exist_ok=True)
SECRET_FILE = DEFAULT_DIR / "webhooks.json"


class SecretStore:
    """Secure storage for webhook URLs and metadata."""

    @staticmethod
    def _load() -> dict[str, Any]:
        """Load secrets from file."""
        if SECRET_FILE.exists():
            try:
                return json.loads(SECRET_FILE.read_text(encoding="utf-8"))
            except Exception:
                return {}
        return {}

    @staticmethod
    def _save(data: dict[str, Any]) -> None:
        """Save secrets to file atomically."""
        tmp = SECRET_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2), encoding="utf-8")
        tmp.replace(SECRET_FILE)

    @classmethod
    def set_webhook(cls, agent_id: str, webhook_url: str, channel_id: int, webhook_id: int) -> None:
        """
        Store webhook information securely.

        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            webhook_url: Full webhook URL
            channel_id: Discord channel ID
            webhook_id: Discord webhook ID
        """
        data = cls._load()
        data[agent_id] = {"url": webhook_url, "channel_id": channel_id, "webhook_id": webhook_id}
        cls._save(data)

    @classmethod
    def get_webhook(cls, agent_id: str) -> dict[str, Any] | None:
        """
        Retrieve webhook information.

        Args:
            agent_id: Agent identifier

        Returns:
            Webhook data dict or None if not found
        """
        return cls._load().get(agent_id)

    @classmethod
    def delete_webhook(cls, agent_id: str) -> None:
        """
        Remove webhook information.

        Args:
            agent_id: Agent identifier
        """
        data = cls._load()
        if agent_id in data:
            del data[agent_id]
            cls._save(data)

    @classmethod
    def list_webhooks(cls) -> dict[str, dict[str, Any]]:
        """
        List all stored webhooks.

        Returns:
            Dict of agent_id -> webhook data
        """
        return cls._load()

    @classmethod
    def get_webhook_url(cls, agent_id: str) -> str | None:
        """
        Get just the webhook URL for an agent.

        Args:
            agent_id: Agent identifier

        Returns:
            Webhook URL or None if not found
        """
        webhook_data = cls.get_webhook(agent_id)
        return webhook_data.get("url") if webhook_data else None
