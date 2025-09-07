from typing import Iterable, Dict, Set

from .cursor_db import CursorTaskRepository


class TerminalCompletionMonitor:
    """Cross-checks terminal signals against Cursor task entries."""

    def __init__(self, repo: CursorTaskRepository) -> None:
        self.repo = repo

    def check_signals(self, agent_id: str, detected_signals: Iterable[str]) -> Dict[str, Set[str]]:
        """Compare detected signals with DB records and return mismatches."""
        tasks = self.repo.get_tasks_by_agent(agent_id)
        expected = {task["signal"] for task in tasks}
        detected = set(detected_signals)
        unexpected = detected - expected
        missing = expected - detected
        return {"unexpected": unexpected, "missing": missing}
