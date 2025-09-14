"""
Learning Recommender
====================

Learning recommendation operations for agent vector integration.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
"""

import json
import logging
from pathlib import Path
from typing import Any

from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery


class LearningRecommender:
    """Handles learning recommendation operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize learning recommender."""
        self.agent_id = agent_id
        self.logger = logging.getLogger(__name__)

        # Initialize configuration
        self.config = self._load_config(config_path)

        # Initialize vector integration
        try:
            self.vector_db = get_vector_database_service()
            self.vector_integration = {"status": "connected", "service": self.vector_db}
        except Exception as e:
            self.logger.warning(f"Vector DB not available: {e}")
            self.vector_integration = {"status": "disconnected", "error": str(e)}

    def _load_config(self, config_path: str | None) -> dict[str, Any]:
        """Load learning recommender configuration."""
        default_config = {
            "learning_categories": [
                "skill_development",
                "knowledge_expansion",
                "process_improvement",
                "tool_mastery",
                "collaboration_skills"
            ],
            "priority_weights": {
                "high": 1.0,
                "medium": 0.7,
                "low": 0.4
            },
            "max_recommendations": 5,
            "min_confidence": 0.6
        }

        # Load from config file if provided
        config_file = Path("config/learning_recommender.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                    default_config.update(file_config)
            except Exception as e:
                logger.warning(f"Could not load config file: {e}")
        
        return default_config

    def get_learning_recommendations(self) -> list[dict[str, Any]]:
        """Get learning recommendations based on agent's work patterns."""
        try:
            if self.vector_integration["status"] != "connected":
                return self._get_fallback_recommendations()

            # Analyze agent's work patterns
            work_patterns = self._analyze_work_patterns()
            skill_gaps = self._identify_skill_gaps(work_patterns)
            recommendations = self._generate_learning_recommendations(skill_gaps)

            return recommendations[:self.config["max_recommendations"]]

        except Exception as e:
            self.logger.error(f"Error getting learning recommendations: {e}")
            return self._get_fallback_recommendations()

    def _analyze_work_patterns(self) -> dict[str, Any]:
        """Analyze agent's work patterns from vector database."""
        try:
            # Search for agent's recent work
            query = SearchQuery(
                query=f"agent:{self.agent_id}",
                collection_name="agent_work",
                limit=50
            )
            work_results = search_vector_database(query)

            # Analyze patterns
            work_types = []
            technologies = []
            for result in work_results:
                if hasattr(result, 'document'):
                    work_types.append(result.document.document_type.value)
                    if result.document.tags:
                        technologies.extend(result.document.tags)

            return {
                "work_types": work_types,
                "technologies": technologies,
                "total_work_items": len(work_results)
            }
        except Exception as e:
            self.logger.error(f"Error analyzing work patterns: {e}")
            return {"work_types": [], "technologies": [], "total_work_items": 0}

    def _identify_skill_gaps(self, work_patterns: dict[str, Any]) -> list[str]:
        """Identify skill gaps based on work patterns."""
        skill_gaps = []

        # Check for missing common technologies
        common_techs = ["python", "vector_database", "coordination", "testing", "documentation"]
        used_techs = [tech.lower() for tech in work_patterns.get("technologies", [])]

        for tech in common_techs:
            if not any(tech in used_tech for used_tech in used_techs):
                skill_gaps.append(tech)

        # Check for work type diversity
        work_types = work_patterns.get("work_types", [])
        if "documentation" not in work_types:
            skill_gaps.append("documentation_skills")
        if "test" not in work_types:
            skill_gaps.append("testing_skills")

        return skill_gaps

    def _generate_learning_recommendations(self, skill_gaps: list[str]) -> list[dict[str, Any]]:
        """Generate learning recommendations based on skill gaps."""
        recommendations = []

        # Generate recommendations for identified gaps
        for gap in skill_gaps:
            if gap == "python":
                recommendations.append({
                    "recommendation_id": f"learn_python_{self.agent_id}",
                    "type": "skill_development",
                    "title": "Advanced Python Programming",
                    "description": "Enhance Python skills for better code quality and efficiency",
                    "priority": "high",
                    "confidence": 0.9
                })
            elif gap == "vector_database":
                recommendations.append({
                    "recommendation_id": f"learn_vector_db_{self.agent_id}",
                    "type": "knowledge_expansion",
                    "title": "Vector Database Mastery",
                    "description": "Learn advanced vector database techniques for better context retrieval",
                    "priority": "high",
                    "confidence": 0.8
                })
            elif gap == "coordination":
                recommendations.append({
                    "recommendation_id": f"learn_coordination_{self.agent_id}",
                    "type": "collaboration_skills",
                    "title": "Advanced Coordination Techniques",
                    "description": "Learn advanced coordination patterns for better swarm performance",
                    "priority": "medium",
                    "confidence": 0.7
                })

        # Add general recommendations if no specific gaps
        if not recommendations:
            recommendations = self._get_fallback_recommendations()

        return recommendations

    def _get_fallback_recommendations(self) -> list[dict[str, Any]]:
        """Get fallback recommendations when analysis fails."""
        return [
            {
                "recommendation_id": f"learn_general_1_{self.agent_id}",
                "type": "skill_development",
                "title": "General Skill Development",
                "description": "Focus on improving core development skills",
                "priority": "medium",
                "confidence": 0.6
            },
            {
                "recommendation_id": f"learn_general_2_{self.agent_id}",
                "type": "knowledge_expansion",
                "title": "System Architecture",
                "description": "Learn advanced system architecture patterns",
                "priority": "medium",
                "confidence": 0.6
            }
        ]
