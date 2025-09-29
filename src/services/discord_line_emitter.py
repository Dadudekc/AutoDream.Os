"""
Discord Line Emitter
===================
Post single-line events to per-agent Discord webhooks (no discord.py dependency).
"""

import asyncio
from typing import Optional, Mapping
import aiohttp
from src.services.secret_store import SecretStore


class DiscordLineEmitter:
    """Post single-line events to per-agent Discord webhooks (no discord.py)."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def _get_webhook(self, agent_id: str) -> Optional[str]:
        """Get webhook URL for agent from secure storage."""
        return SecretStore.get_webhook_url(agent_id)

    async def emit_event(
        self,
        agent_id: str,
        line: str,
        username: Optional[str] = None,
        avatar_url: Optional[str] = None,
        extra_embeds: Optional[list] = None,
        max_retries: int = 5,
    ) -> bool:
        """
        Emit a single-line event to Discord webhook.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            line: Single-line message content
            username: Optional custom username
            avatar_url: Optional custom avatar
            extra_embeds: Optional Discord embeds
            max_retries: Maximum retry attempts
            
        Returns:
            True if successful, False otherwise
        """
        url = self._get_webhook(agent_id)
        if not url:
            return False

        payload: Mapping[str, object] = {"content": line}
        if username:
            payload["username"] = username
        if avatar_url:
            payload["avatar_url"] = avatar_url
        if extra_embeds:
            payload["embeds"] = extra_embeds

        backoff = 0.5
        for attempt in range(max_retries):
            try:
                async with aiohttp.ClientSession(
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as session:
                    async with session.post(url, json=payload) as response:
                        if response.status in (200, 204):
                            return True
                        if response.status == 429:
                            # Rate limited - wait and retry
                            data = await response.json()
                            retry_after = float(data.get("retry_after", backoff))
                            await asyncio.sleep(retry_after)
                        else:
                            # Other error - exponential backoff
                            await asyncio.sleep(backoff)
                            backoff = min(backoff * 2, 8.0)
            except Exception:
                # Network error - exponential backoff
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, 8.0)
        
        return False
