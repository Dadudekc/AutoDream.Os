from __future__ import annotations

"""Skill tracking utilities for the AI agent learner."""

from dataclasses import dataclass
from typing import Dict


@dataclass
class Skill:
    """Represents a skill and its proficiency level."""

    name: str
    level: int = 0  # 0-100 scale

    def adjust(self, delta: int) -> int:
        """Adjust the skill level by ``delta`` clamped to ``0-100``."""

        self.level = max(0, min(100, self.level + delta))
        return self.level


class SkillManager:
    """Manage a collection of :class:`Skill` instances."""

    def __init__(self) -> None:
        self._skills: Dict[str, Skill] = {}

    def add_skill(self, name: str, level: int = 0) -> Skill:
        skill = Skill(name, max(0, min(100, level)))
        self._skills[name] = skill
        return skill

    def update_skill(self, name: str, delta: int) -> int:
        skill = self._skills.get(name)
        if not skill:
            skill = self.add_skill(name)
        return skill.adjust(delta)

    def get_level(self, name: str) -> int:
        return self._skills.get(name, Skill(name)).level


__all__ = ["Skill", "SkillManager"]
