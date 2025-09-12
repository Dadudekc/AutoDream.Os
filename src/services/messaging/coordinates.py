from __future__ import annotations
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

def get_coordinate_loader():
    try:
        from src.core.coordinate_loader import get_coordinate_loader as _core
        return _core()
    except Exception as e:
        logger.warning(f"[coord] fallback loader: {e}")
        class Mock:
            def get_all_agents(self):
                return [f"Agent-{i}" for i in range(1,9)]
            def is_agent_active(self, a):
                return True
            def get_chat_coordinates(self, a):
                return (100,100)
        return Mock()

def list_agents() -> List[str]:
    loader = get_coordinate_loader()
    return [a for a in loader.get_all_agents() if loader.is_agent_active(a)]

def get_agent_coordinates(agent_id: str) -> Tuple[int,int] | None:
    try:
        return get_coordinate_loader().get_chat_coordinates(agent_id)
    except Exception as e:
        logger.error(f"[coord] failed for {agent_id}: {e}")
        return None

def load_all_active_coords() -> Dict[str, Tuple[int,int]]:
    loader = get_coordinate_loader()
    out: Dict[str, Tuple[int,int]] = {}
    for a in loader.get_all_agents():
        if loader.is_agent_active(a):
            try:
                out[a] = loader.get_chat_coordinates(a)
            except Exception:
                pass
    return out
