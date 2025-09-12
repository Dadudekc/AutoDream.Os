from __future__ import annotations
from typing import Dict
from .service import MessagingService
from .coordinates import list_agents


def broadcast(content: str, sender: str = "ConsolidatedMessagingService") -> Dict[str, bool]:
    svc = MessagingService()
    results = {}
    for a in list_agents():
        results[a] = svc.send(a, content)
    return results
