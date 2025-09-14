"""
Agent Matching Utilities - V2 Compliant Agent Matching Logic
Focused utility for agent capability matching and scoring
V2 Compliance: Under 300-line limit with focused functionality

@Author: Agent-6 - Gaming & Entertainment Specialist (Coordination & Communication V2 Compliance)
@Version: 1.0.0 - Agent Matching Utilities
@License: MIT
"""

@dataclass
class AgentCapability:
    """Standard agent capability structure."""

    skills: List[str]
    specializations: List[str]
    performance_score: float
    availability: str


class AgentMatchingUtils:
    """Agent matching utilities for capability-based selection.

    Provides functionality for:
    - Agent capability scoring
    - Task-agent matching
    - Performance-based selection
    """

    @staticmethod
    def calculate_agent_match_score(
        task_requirements: Dict[str, Any], agent_capabilities: Dict[str, Any]
    ) -> float:
        """Calculate agent match score for task requirements.

        Args:
            task_requirements: Task requirements dictionary
            agent_capabilities: Agent capabilities dictionary

        Returns:
            Match score between 0.0 and 1.0
        """
        if not task_requirements or not agent_capabilities:
            return 0.0

        # Simple matching algorithm (can be enhanced with vector similarity)
        required_skills = task_requirements.get("required_skills", [])
        agent_skills = agent_capabilities.get("skills", [])

        if not get_unified_validator().validate_required(required_skills):
            return 0.5  # Default score if no specific requirements

        # Calculate skill overlap
        skill_matches = len(set(required_skills) & set(agent_skills))
        skill_score = skill_matches / len(required_skills) if required_skills else 0.0

        # Factor in performance score
        performance_score = agent_capabilities.get("performance_score", 0.0) / 100.0

        # Weighted combination
        match_score = (skill_score * 0.7) + (performance_score * 0.3)
        return min(1.0, max(0.0, match_score))

    @staticmethod
    def get_agent_type_match_score(
        task_requirements: Dict[str, Any], agent_type: str, metrics: Dict[str, Any]
    ) -> float:
        """Calculate agent type match score for task requirements.

        Args:
            task_requirements: Task requirements dictionary
            agent_type: Agent type string
            metrics: Agent metrics dictionary

        Returns:
            Match score between 0.0 and 1.0
        """
        if not get_unified_validator().validate_required(task_requirements):
            return 0.5  # Default score if no specific requirements

        # Calculate match based on task type and agent capabilities
        task_type = task_requirements.get("task_type", "general")

        # Agent type specific matching
        if task_type == "integration" and agent_type == "agent_1":
            return 0.9
        elif task_type == "coordination" and agent_type == "agent_6":
            return 0.9
        elif task_type == "web_development" and agent_type == "agent_7":
            return 0.9
        else:
            # Generic matching based on performance metrics
            performance_score = metrics.get("v2_compliance_score", 0) / 100.0
            return min(1.0, max(0.0, performance_score))

    @staticmethod
    def rank_agents_by_capability(
        task_requirements: Dict[str, Any], available_agents: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Rank available agents by their capability to handle the task.

        Args:
            task_requirements: Task requirements dictionary
            available_agents: Dictionary of available agents with their capabilities

        Returns:
            List of ranked agents with match scores
        """
        ranked_agents = []

        for agent_id, capabilities in available_agents.items():
            match_score = AgentMatchingUtils.calculate_agent_match_score(
                task_requirements, capabilities
            )

            ranked_agents.append(
                {
                    "agent_id": agent_id,
                    "match_score": match_score,
                    "capabilities": capabilities,
                }
            )

        # Sort by match score (highest first)
        ranked_agents.sort(key=lambda x: x["match_score"], reverse=True)
        return ranked_agents

    @staticmethod
    def get_best_agent_for_task(
        task_requirements: Dict[str, Any],
        available_agents: Dict[str, Dict[str, Any]],
        min_score: float = 0.7,
    ) -> Dict[str, Any]:
        """Get the best agent for a specific task.

        Args:
            task_requirements: Task requirements dictionary
            available_agents: Dictionary of available agents with their capabilities
            min_score: Minimum acceptable match score

        Returns:
            Best matching agent or None if no suitable agent found
        """
        ranked_agents = AgentMatchingUtils.rank_agents_by_capability(
            task_requirements, available_agents
        )

        if ranked_agents and ranked_agents[0]["match_score"] >= min_score:
            return ranked_agents[0]

        return None


# Export main interface
__all__ = ["AgentMatchingUtils", "AgentCapability"]
