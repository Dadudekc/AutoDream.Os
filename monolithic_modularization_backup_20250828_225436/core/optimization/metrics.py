from typing import List

from __future__ import annotations
from dataclasses import dataclass


"""Simple metrics collection for assignment optimisation."""



@dataclass
class AssignmentRecord:
    contract_id: str
    agent_id: str
    score: float


class AssignmentMetrics:
    """Collects metrics about assignments."""

    def __init__(self) -> None:
        self.records: List[AssignmentRecord] = []

    def record(self, contract_id: str, agent_id: str, score: float) -> None:
        self.records.append(AssignmentRecord(contract_id, agent_id, score))

    def average_score(self) -> float:
        if not self.records:
            return 0.0
        return sum(r.score for r in self.records) / len(self.records)


__all__ = ["AssignmentMetrics", "AssignmentRecord"]
