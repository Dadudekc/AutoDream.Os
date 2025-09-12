from __future__ import annotations
import logging
from typing import Dict, List
from ..models import UnifiedMessage
from ..coordinates import get_agent_coordinates, list_agents
from .pyautogui_delivery import deliver_message_pyautogui
from .inbox_delivery import send_message_inbox

logger = logging.getLogger(__name__)

def send_with_fallback(message: UnifiedMessage) -> bool:
    coords = get_agent_coordinates(message.recipient)
    if coords:
        try:
            if deliver_message_pyautogui(message, coords):
                return True
        except Exception as e:
            logger.warning(f"[fallback] pyautogui path failed: {e}")
    logger.info(f"[fallback] using inbox for {message.recipient}")
    return send_message_inbox(message)

def broadcast(content: str, sender: str) -> Dict[str, bool]:
    results: Dict[str,bool] = {}
    for agent in list_agents():
        m = UnifiedMessage(content=content, sender=sender, recipient=agent,
                           message_type=... # type: ignore
                           )
        # keep type minimal; delivery doesn’t depend on it
        ok = send_with_fallback(m)
        results[agent] = ok
    return results
