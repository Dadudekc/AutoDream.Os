"""Reporting utilities for auth integration tests."""
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict, Any
import json


@dataclass
class TestResult:
    name: str
    passed: bool
    duration: float
    details: Dict[str, Any]


@dataclass
class IntegrationReport:
    started: datetime
    ended: datetime
    results: List[TestResult]

    @property
    def summary(self) -> Dict[str, Any]:
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        return {"total": total, "passed": passed, "failed": total - passed}

    def to_json(self, path: str) -> str:
        payload = {
            "started": self.started.isoformat(),
            "ended": self.ended.isoformat(),
            "summary": self.summary,
            "results": [asdict(r) for r in self.results],
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        return path
