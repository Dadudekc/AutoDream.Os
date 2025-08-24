#!/usr/bin/env python3
"""SmartOrganizer module.

Provides lightweight work pattern detection and workflow optimization
suggestions. It is intentionally simple to keep within testing scope
while demonstrating how more sophisticated organization tools might be
structured."""

from collections import Counter
from typing import List


class SmartOrganizer:
    """Detects simple patterns in task lists and suggests optimizations."""

    def detect_pattern(self, tasks: List[str]) -> str:
        """Return a label describing task repetition patterns."""
        if not tasks:
            return "none"
        counts = Counter(tasks)
        if len(counts) == 1:
            return "repetition"
        if any(c > 1 for c in counts.values()):
            return "mixed"
        return "unique"

    def suggest_optimization(self, tasks: List[str]) -> str:
        """Provide a simple optimization suggestion based on detected pattern."""
        pattern = self.detect_pattern(tasks)
        if pattern == "repetition":
            return "Automate or batch repeated tasks"
        if pattern == "mixed":
            return "Group similar tasks to reduce context switching"
        if pattern == "unique":
            return "Prioritize tasks based on impact"
        return "No tasks provided"


__all__ = ["SmartOrganizer"]
