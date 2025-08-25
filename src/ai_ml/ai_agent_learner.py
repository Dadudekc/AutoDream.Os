"""Orchestrator for AI agent learning components."""

from .ai_agent_learner_core import LearningGoal, LearningProgress, LearnerCore
from .ai_agent_knowledge import KnowledgeBase, KnowledgeItem
from .ai_agent_skills import Skill, SkillManager


class AIAgentLearner:
    """High level façade combining learning, knowledge and skills."""

    def __init__(self) -> None:
        self.core = LearnerCore()
        self.knowledge = KnowledgeBase()
        self.skills = SkillManager()

    # Convenience wrappers -------------------------------------------------
    def learn_topic(self, topic: str, content: str, description: str = "") -> None:
        """Register new knowledge and a learning goal."""

        self.knowledge.add(topic, content)
        self.core.add_goal(LearningGoal(topic, description))

    def practise_skill(self, name: str, improvement: int = 1) -> int:
        """Improve a skill by the given ``improvement`` amount."""

        return self.skills.update_skill(name, improvement)

    def record_progress(self, topic: str, progress: float) -> float:
        """Update progress for a learning goal."""

        return self.core.update_progress(topic, progress)

    def overall_progress(self) -> float:
        """Return average progress across all goals."""

        return self.core.overall_progress()


__all__ = [
    "LearningGoal",
    "LearningProgress",
    "LearnerCore",
    "KnowledgeBase",
    "KnowledgeItem",
    "Skill",
    "SkillManager",
    "AIAgentLearner",
]
