"""Core planning utilities for AI agent tasks."""
from dataclasses import dataclass
from typing import List


@dataclass
class Plan:
    """Represents a high-level plan produced for an AI agent."""
    goal: str
    steps: List[str]


class PlannerCore:
    """Generates plans for AI agents based on a given goal."""

    def create_plan(self, goal: str) -> Plan:
        """Create a simple plan for the provided goal."""
        steps = [f"Analyze goal: {goal}", "Identify requirements", "Propose strategy"]
        return Plan(goal=goal, steps=steps)
