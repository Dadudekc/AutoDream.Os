#!/usr/bin/env python3
"""
Agent Context System - Agent Cellphone V2
=========================================

Personalized agent intelligence system that provides context-aware recommendations,
domain expertise extraction, and intelligent agent coordination.

V2 Compliance: < 300 lines, single responsibility, agent context management.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from datetime import datetime

# from ..services.vector_database_service import VectorDatabaseService
# from ..services.models.vector_models import DocumentType, SearchQuery


@dataclass
class AgentContext:
    """Comprehensive agent context information."""

    agent_id: str
    profile: Dict[str, Any] = field(default_factory=dict)
    communication_patterns: List[Dict[str, Any]] = field(default_factory=list)
    success_patterns: List[Dict[str, Any]] = field(default_factory=list)
    collaboration_history: List[Dict[str, Any]] = field(default_factory=list)
    domain_expertise: List[str] = field(default_factory=list)
    preferred_communication_style: str = "professional"
    optimal_task_types: List[str] = field(default_factory=list)
    performance_metrics: Dict[str, Any] = field(default_factory=dict)
    last_updated: datetime = field(default_factory=datetime.now)


@dataclass
class Recommendation:
    """Agent recommendation with context and confidence."""

    type: str  # "task", "communication", "collaboration", "optimization"
    description: str
    confidence: float  # 0.0 to 1.0
    reasoning: str
    metadata: Dict[str, Any] = field(default_factory=dict)


class AgentContextSystem:
    """
    Personalized agent intelligence system.

    Provides context-aware recommendations, domain expertise extraction,
    and intelligent agent coordination based on vector database analysis.
    """

    def __init__(self, agent_id: str, vector_db):
        """
        Initialize agent context system.

        Args:
            agent_id: Agent identifier
            vector_db: Vector database service instance
        """
        self.agent_id = agent_id
        self.vector_db = vector_db
        self.logger = logging.getLogger(__name__)
        self.context = self._build_agent_context()

    def _build_agent_context(self) -> AgentContext:
        """Build comprehensive agent context from vector database."""
        try:
            # Get agent profile
            profile = self._get_agent_profile()

            # Get communication patterns
            comm_patterns = self._get_communication_patterns()

            # Get task success patterns
            success_patterns = self._get_success_patterns()

            # Get collaboration history
            collaboration_history = self._get_collaboration_history()

            # Extract domain expertise
            domain_expertise = self._extract_domain_expertise(profile, success_patterns)

            # Extract communication style
            comm_style = self._extract_communication_style(comm_patterns)

            # Extract optimal task types
            optimal_tasks = self._extract_optimal_task_types(success_patterns)

            # Calculate performance metrics
            performance_metrics = self._calculate_performance_metrics(success_patterns)

            return AgentContext(
                agent_id=self.agent_id,
                profile=profile,
                communication_patterns=comm_patterns,
                success_patterns=success_patterns,
                collaboration_history=collaboration_history,
                domain_expertise=domain_expertise,
                preferred_communication_style=comm_style,
                optimal_task_types=optimal_tasks,
                performance_metrics=performance_metrics,
            )

        except Exception as e:
            self.get_logger(__name__).error(f"Error building agent context: {e}")
            return AgentContext(agent_id=self.agent_id)

    def _get_agent_profile(self) -> Dict[str, Any]:
        """Get agent profile from vector database."""
        try:
            profile_data = self.vector_db.search_documents(
                query=f"agent {self.agent_id} profile role domain capabilities",
                filters={"agent_id": self.agent_id, "document_type": "agent_profile"},
                limit=1,
            )

            if profile_data:
                return profile_data[0].get("metadata", {})

            # Fallback to basic profile
            return {
                "agent_id": self.agent_id,
                "role": "Specialist",
                "domain": "general",
                "capabilities": [],
                "experience_level": "intermediate",
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting agent profile: {e}")
            return {"agent_id": self.agent_id, "role": "Specialist"}

    def _get_communication_patterns(self) -> List[Dict[str, Any]]:
        """Get agent communication patterns."""
        try:
            comm_data = self.vector_db.search_documents(
                query=f"agent {self.agent_id} communication message",
                filters={"agent_id": self.agent_id, "document_type": "message"},
                limit=20,
            )

            return [item.get("metadata", {}) for item in comm_data]

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting communication patterns: {e}")
            return []

    def _get_success_patterns(self) -> List[Dict[str, Any]]:
        """Get agent success patterns from completed tasks."""
        try:
            success_data = self.vector_db.search_documents(
                query=f"agent {self.agent_id} successful completion",
                filters={
                    "agent_id": self.agent_id,
                    "document_type": "contract",
                    "status": "completed",
                },
                limit=15,
            )

            return [item.get("metadata", {}) for item in success_data]

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting success patterns: {e}")
            return []

    def _get_collaboration_history(self) -> List[Dict[str, Any]]:
        """Get agent collaboration history."""
        try:
            collab_data = self.vector_db.search_documents(
                query=f"agent {self.agent_id} collaboration coordination",
                filters={"agent_id": self.agent_id, "document_type": "collaboration"},
                limit=10,
            )

            return [item.get("metadata", {}) for item in collab_data]

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting collaboration history: {e}")
            return []

    def _extract_domain_expertise(
        self, profile: Dict[str, Any], success_patterns: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract domain expertise from profile and success patterns."""
        try:
            expertise = []

            # From profile
            if "domain" in profile:
                expertise.append(profile["domain"])

            if "capabilities" in profile:
                expertise.extend(profile["capabilities"])

            # From success patterns
            task_types = []
            for pattern in success_patterns:
                task_type = pattern.get("task_type", "")
                if task_type:
                    task_types.append(task_type)

            # Get most common task types
            if task_types:

                common_types = Counter(task_types).most_common(3)
                expertise.extend([task_type for task_type, count in common_types])

            return list(set(expertise))  # Remove duplicates

        except Exception as e:
            self.get_logger(__name__).error(f"Error extracting domain expertise: {e}")
            return []

    def _extract_communication_style(self, comm_patterns: List[Dict[str, Any]]) -> str:
        """Extract preferred communication style from patterns."""
        try:
            if not get_unified_validator().validate_required(comm_patterns):
                return "professional"

            # Analyze communication patterns
            styles = []
            for pattern in comm_patterns:
                style = pattern.get("communication_style", "professional")
                styles.append(style)

            # Get most common style
            if styles:

                most_common = Counter(styles).most_common(1)[0][0]
                return most_common

            return "professional"

        except Exception as e:
            self.get_logger(__name__).error(f"Error extracting communication style: {e}")
            return "professional"

    def _extract_optimal_task_types(
        self, success_patterns: List[Dict[str, Any]]
    ) -> List[str]:
        """Extract optimal task types from success patterns."""
        try:
            if not get_unified_validator().validate_required(success_patterns):
                return []

            # Analyze successful task types
            task_types = []
            for pattern in success_patterns:
                task_type = pattern.get("task_type", "")
                success_score = pattern.get("success_score", 0.5)

                if success_score > 0.7 and task_type:  # High success rate
                    task_types.append(task_type)

            # Get most successful task types
            if task_types:

                optimal_types = Counter(task_types).most_common(5)
                return [task_type for task_type, count in optimal_types]

            return []

        except Exception as e:
            self.get_logger(__name__).error(f"Error extracting optimal task types: {e}")
            return []

    def _calculate_performance_metrics(
        self, success_patterns: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate performance metrics from success patterns."""
        try:
            if not get_unified_validator().validate_required(success_patterns):
                return {"total_tasks": 0, "success_rate": 0.0}

            total_tasks = len(success_patterns)
            successful_tasks = len(
                [p for p in success_patterns if p.get("success_score", 0) > 0.7]
            )
            success_rate = successful_tasks / total_tasks if total_tasks > 0 else 0.0

            # Calculate average completion time
            completion_times = [
                p.get("completion_time_hours", 0)
                for p in success_patterns
                if p.get("completion_time_hours")
            ]
            avg_completion_time = (
                sum(completion_times) / len(completion_times) if completion_times else 0
            )

            return {
                "total_tasks": total_tasks,
                "successful_tasks": successful_tasks,
                "success_rate": success_rate,
                "average_completion_time_hours": avg_completion_time,
                "performance_level": self._get_performance_level(success_rate),
            }

        except Exception as e:
            self.get_logger(__name__).error(f"Error calculating performance metrics: {e}")
            return {"total_tasks": 0, "success_rate": 0.0}

    def _get_performance_level(self, success_rate: float) -> str:
        """Get performance level based on success rate."""
        if success_rate >= 0.9:
            return "excellent"
        elif success_rate >= 0.8:
            return "very_good"
        elif success_rate >= 0.7:
            return "good"
        elif success_rate >= 0.6:
            return "average"
        else:
            return "needs_improvement"

    def get_personalized_recommendations(
        self, current_task: str
    ) -> List[Recommendation]:
        """Get personalized recommendations based on agent context."""
        try:
            recommendations = []

            # Task-specific recommendations
            task_recs = self._get_task_recommendations(current_task)
            recommendations.extend(task_recs)

            # Communication recommendations
            comm_recs = self._get_communication_recommendations()
            recommendations.extend(comm_recs)

            # Collaboration recommendations
            collab_recs = self._get_collaboration_recommendations()
            recommendations.extend(collab_recs)

            # Performance optimization recommendations
            perf_recs = self._get_performance_recommendations()
            recommendations.extend(perf_recs)

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting personalized recommendations: {e}")
            return []

    def _get_task_recommendations(self, current_task: str) -> List[Recommendation]:
        """Get task-specific recommendations."""
        try:
            recommendations = []

            # Find similar successful tasks
            similar_tasks = self.vector_db.search_documents(
                query=current_task,
                filters={
                    "agent_id": self.agent_id,
                    "status": "completed",
                    "document_type": "contract",
                },
                limit=5,
            )

            if similar_tasks:
                # Extract success factors
                success_factors = []
                for task in similar_tasks:
                    factors = task.get("metadata", {}).get("success_factors", [])
                    success_factors.extend(factors)

                if success_factors:

                    top_factors = Counter(success_factors).most_common(3)

                    for factor, count in top_factors:
                        recommendations.append(
                            Recommendation(
                                type="task",
                                description=f"Apply success factor: {factor}",
                                confidence=min(count / len(similar_tasks), 1.0),
                                reasoning=f"Used successfully in {count} similar tasks",
                                metadata={
                                    "success_factor": factor,
                                    "usage_count": count,
                                },
                            )
                        )

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting task recommendations: {e}")
            return []

    def _get_communication_recommendations(self) -> List[Recommendation]:
        """Get communication recommendations."""
        try:
            recommendations = []

            # Analyze communication patterns
            if self.context.communication_patterns:
                # Check for communication issues
                issue_patterns = [
                    p
                    for p in self.context.communication_patterns
                    if p.get("issue_type")
                ]

                if issue_patterns:
                    recommendations.append(
                        Recommendation(
                            type="communication",
                            description="Improve communication clarity",
                            confidence=0.8,
                            reasoning="Communication issues detected in recent patterns",
                            metadata={"issue_count": len(issue_patterns)},
                        )
                    )

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting communication recommendations: {e}")
            return []

    def _get_collaboration_recommendations(self) -> List[Recommendation]:
        """Get collaboration recommendations."""
        try:
            recommendations = []

            # Analyze collaboration effectiveness
            if self.context.collaboration_history:
                effective_collabs = [
                    c
                    for c in self.context.collaboration_history
                    if c.get("effectiveness_score", 0) > 0.7
                ]

                if (
                    len(effective_collabs)
                    < len(self.context.collaboration_history) * 0.6
                ):
                    recommendations.append(
                        Recommendation(
                            type="collaboration",
                            description="Improve collaboration effectiveness",
                            confidence=0.7,
                            reasoning="Collaboration effectiveness below optimal level",
                            metadata={"effective_collabs": len(effective_collabs)},
                        )
                    )

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting collaboration recommendations: {e}")
            return []

    def _get_performance_recommendations(self) -> List[Recommendation]:
        """Get performance optimization recommendations."""
        try:
            recommendations = []

            # Check performance metrics
            success_rate = self.context.performance_metrics.get("success_rate", 0)
            performance_level = self.context.performance_metrics.get(
                "performance_level", "average"
            )

            if performance_level == "needs_improvement":
                recommendations.append(
                    Recommendation(
                        type="optimization",
                        description="Focus on improving task success rate",
                        confidence=0.9,
                        reasoning=f"Current success rate: {success_rate:.2f}",
                        metadata={"current_success_rate": success_rate},
                    )
                )

            return recommendations

        except Exception as e:
            self.get_logger(__name__).error(f"Error getting performance recommendations: {e}")
            return []

    def get_agent_summary(self) -> Dict[str, Any]:
        """Get comprehensive agent summary."""
        return {
            "agent_id": self.agent_id,
            "domain_expertise": self.context.domain_expertise,
            "communication_style": self.context.preferred_communication_style,
            "optimal_task_types": self.context.optimal_task_types,
            "performance_metrics": self.context.performance_metrics,
            "total_communications": len(self.context.communication_patterns),
            "total_successful_tasks": len(self.context.success_patterns),
            "collaboration_count": len(self.context.collaboration_history),
            "last_updated": self.context.last_updated.isoformat(),
        }

    def update_context(self):
        """Update agent context with latest data."""
        self.context = self._build_agent_context()


def create_agent_context_system(agent_id: str, vector_db) -> AgentContextSystem:
    """Factory function to create agent context system."""
    return AgentContextSystem(agent_id, vector_db)
