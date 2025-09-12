from __future__ import annotations
import logging
from typing import Dict, Any
from .models import UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority, UnifiedMessageTag, map_priority, map_tag
from .delivery.fallback import send_with_fallback
from .coordinates import list_agents as _list_agents, get_agent_coordinates
logger = logging.getLogger(__name__)

class MessagingService:
    """Thin orchestration facade; <200 LOC target."""
    def __init__(self, dry_run: bool=False):
        self.dry_run = bool(dry_run)

    def send(self, agent_id: str, content: str, priority: str="NORMAL", tag: str="GENERAL") -> bool:
        if self.dry_run:
            logger.info(f"[dry-run] send → {agent_id}: {content[:120]}")
            return True
        msg = UnifiedMessage(
            content=content,
            sender="ConsolidatedMessagingService",
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=map_priority(priority),
            tags=[map_tag(tag)]
        )
        return send_with_fallback(msg)

    def broadcast(self, content: str, sender: str="ConsolidatedMessagingService") -> Dict[str,bool]:
        results: Dict[str,bool] = {}
        for a in _list_agents():
            results[a] = self.send(a, content)
        return results

    # Surface helpers for other modules
    def coords(self, agent_id: str):
        return get_agent_coordinates(agent_id)
