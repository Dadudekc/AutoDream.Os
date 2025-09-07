"""Agent learning helpers."""

from typing import Dict, List

from .utils import current_time


class AgentLearning:
    """Stores simple experience logs for agents."""

    def __init__(self) -> None:
        self._experiences: Dict[str, List[str]] = {}

    def record(self, agent_id: str, experience: str) -> None:
        timestamp = current_time().isoformat()
        entry = f"{timestamp}: {experience}"
        self._experiences.setdefault(agent_id, []).append(entry)

    def get_experiences(self, agent_id: str) -> List[str]:
        return self._experiences.get(agent_id, [])
