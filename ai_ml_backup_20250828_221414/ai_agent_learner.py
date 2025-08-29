"""Orchestrator for AI agent learning components - MIGRATED TO UNIFIED LEARNING ENGINE."""

# MIGRATED: Using unified learning engine instead of local implementation
from ..core.learning import (
    LearningGoal, LearningProgress, UnifiedLearningEngine, LearningManager
)
from .ai_agent_knowledge import KnowledgeBase, KnowledgeItem
from .ai_agent_skills import Skill, SkillManager


class AIAgentLearner:
    """High level façade combining learning, knowledge and skills - MIGRATED TO UNIFIED ENGINE."""

    def __init__(self) -> None:
        # MIGRATED: Using unified learning engine instead of local LearnerCore
        self.learning_engine = UnifiedLearningEngine()
        self.learning_manager = LearningManager()
        self.knowledge = KnowledgeBase()
        self.skills = SkillManager()

    # Convenience wrappers -------------------------------------------------
    def learn_topic(self, topic: str, content: str, description: str = "") -> None:
        """Register new knowledge and a learning goal - MIGRATED TO UNIFIED ENGINE."""

        self.knowledge.add(topic, content)
        # MIGRATED: Using unified learning engine
        goal = LearningGoal(
            goal_id=topic,
            title=topic,
            description=description,
            target_skill_level=1.0,
            learning_mode="knowledge_acquisition"
        )
        self.learning_engine.add_learning_goal(goal)

    def practise_skill(self, name: str, improvement: int = 1) -> int:
        """Improve a skill by the given ``improvement`` amount."""

        return self.skills.update_skill(name, improvement)

    def record_progress(self, topic: str, progress: float) -> float:
        """Update progress for a learning goal - MIGRATED TO UNIFIED ENGINE."""

        # MIGRATED: Using unified learning engine
        return self.learning_engine.update_learning_progress(topic, progress)

    def overall_progress(self) -> float:
        """Return average progress across all goals - MIGRATED TO UNIFIED ENGINE."""

        # MIGRATED: Using unified learning engine
        return self.learning_engine.get_overall_learning_progress()


__all__ = [
    "LearningGoal",
    "LearningProgress", 
    "UnifiedLearningEngine",
    "LearningManager",
    "KnowledgeBase",
    "KnowledgeItem",
    "Skill",
    "SkillManager",
    "AIAgentLearner",
]
