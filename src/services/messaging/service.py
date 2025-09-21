from __future__ import annotations

import logging

from .coordinates import get_agent_coordinates
from .coordinates import list_agents as _list_agents
from .delivery.fallback import send_with_fallback
from .models import (
    UnifiedMessage,
    UnifiedMessageType,
)
# Simple priority and tag mapping functions
def map_priority(priority: str):
    """Map priority string to enum."""
    from .models import UnifiedMessagePriority
    priority_map = {
        "low": UnifiedMessagePriority.LOW,
        "normal": UnifiedMessagePriority.NORMAL,
        "high": UnifiedMessagePriority.HIGH,
        "urgent": UnifiedMessagePriority.URGENT
    }
    return priority_map.get((priority or "normal").lower(), UnifiedMessagePriority.NORMAL)

def map_tag(tag: str):
    """Map tag string to enum."""
    from .models import UnifiedMessageTag
    tag_map = {
        "general": UnifiedMessageTag.GENERAL,
        "coordination": UnifiedMessageTag.COORDINATION,
        "task": UnifiedMessageTag.TASK,
        "status": UnifiedMessageTag.STATUS,
        "project_update": UnifiedMessageTag.PROJECT_UPDATE
    }
    return tag_map.get((tag or "general").lower(), UnifiedMessageTag.GENERAL)

logger = logging.getLogger(__name__)


class MessagingService:
    """Thin orchestration facade; <200 LOC target."""

    def __init__(self, dry_run: bool = False):
        self.dry_run = bool(dry_run)

    def send(
        self, agent_id: str, content: str, priority: str = "NORMAL", tag: str = "GENERAL", high_priority: bool = False
    ) -> bool:
        if self.dry_run:
            priority_indicator = "🚨 HIGH PRIORITY 🚨 " if high_priority else ""
            logger.info(f"[dry-run] send → {agent_id}: {priority_indicator}{content[:120]}")
            return True
        msg = UnifiedMessage(
            content=content,
            sender="ConsolidatedMessagingService",
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=map_priority(priority),
            tags=[map_tag(tag)],
        )
        return send_with_fallback(msg, high_priority=high_priority)

    def broadcast(
        self, content: str, sender: str = "ConsolidatedMessagingService"
    ) -> dict[str, bool]:
        results: dict[str, bool] = {}
        for a in _list_agents():
            results[a] = self.send(a, content)
        return results

    # Surface helpers for other modules
    def coords(self, agent_id: str):
        return get_agent_coordinates(agent_id)
