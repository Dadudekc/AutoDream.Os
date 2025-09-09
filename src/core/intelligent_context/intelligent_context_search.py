#!/usr/bin/env python3
"""
Intelligent Context Search - V2 Compliance Module
================================================

Search operations for intelligent context retrieval.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time

from .intelligent_context_models import SearchResult


class IntelligentContextSearch:
    """Search operations for intelligent context retrieval."""

    def __init__(self, engine):
        """Initialize context search."""
        self.engine = engine

    def search_context(self, query: str, mission_id: str = None) -> list[SearchResult]:
        """Search for relevant context."""
        start_time = time.time()

        try:
            results = []

            # Search in mission contexts
            if mission_id and mission_id in self.engine.active_missions:
                mission = self.engine.active_missions[mission_id]
                if query.lower() in mission.mission_type.lower():
                    results.append(
                        SearchResult(
                            result_id=f"mission_{mission_id}",
                            content=f"Mission: {mission.mission_type}",
                            relevance_score=0.9,
                            source_type="mission",
                            source_id=mission_id,
                        )
                    )

            # Search in agent capabilities
            for agent_id, capability in self.engine.agent_capabilities.items():
                if query.lower() in capability.primary_role.lower():
                    results.append(
                        SearchResult(
                            result_id=f"agent_{agent_id}",
                            content=f"Agent: {capability.primary_role}",
                            relevance_score=0.8,
                            source_type="agent",
                            source_id=agent_id,
                        )
                    )

            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("search", True, execution_time)

            return results

        except Exception:
            execution_time = (time.time() - start_time) * 1000
            self.engine._update_metrics("search", False, execution_time)
            return []

    def search_missions(self, query: str) -> list[SearchResult]:
        """Search specifically in missions."""
        results = []
        for mission_id, mission in self.engine.active_missions.items():
            if query.lower() in mission.mission_type.lower():
                results.append(
                    SearchResult(
                        result_id=f"mission_{mission_id}",
                        content=f"Mission: {mission.mission_type}",
                        relevance_score=0.9,
                        source_type="mission",
                        source_id=mission_id,
                    )
                )
        return results

    def search_agents(self, query: str) -> list[SearchResult]:
        """Search specifically in agent capabilities."""
        results = []
        for agent_id, capability in self.engine.agent_capabilities.items():
            if query.lower() in capability.primary_role.lower():
                results.append(
                    SearchResult(
                        result_id=f"agent_{agent_id}",
                        content=f"Agent: {capability.primary_role}",
                        relevance_score=0.8,
                        source_type="agent",
                        source_id=agent_id,
                    )
                )
        return results

    def search_by_skills(self, skills: list[str]) -> list[SearchResult]:
        """Search agents by skills."""
        results = []
        for agent_id, capability in self.engine.agent_capabilities.items():
            for skill in skills:
                if skill.lower() in [s.lower() for s in capability.skills]:
                    results.append(
                        SearchResult(
                            result_id=f"agent_{agent_id}",
                            content=f"Agent: {capability.primary_role} (Skill: {skill})",
                            relevance_score=0.8,
                            source_type="agent",
                            source_id=agent_id,
                        )
                    )
                    break
        return results

    def search_by_mission_type(self, mission_type: str) -> list[SearchResult]:
        """Search missions by type."""
        results = []
        for mission_id, mission in self.engine.active_missions.items():
            if mission_type.lower() in mission.mission_type.lower():
                results.append(
                    SearchResult(
                        result_id=f"mission_{mission_id}",
                        content=f"Mission: {mission.mission_type}",
                        relevance_score=0.9,
                        source_type="mission",
                        source_id=mission_id,
                    )
                )
        return results
