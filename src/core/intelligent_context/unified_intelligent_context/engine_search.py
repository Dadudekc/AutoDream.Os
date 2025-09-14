"""
Intelligent Context Engine Search
================================

Search functionality for intelligent context operations.
V2 Compliance: < 300 lines, single responsibility, search logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from datetime import datetime

from .models import ContextRetrievalResult, ContextType, SearchResult


class IntelligentContextEngineSearch:
    """Search functionality for intelligent context engine."""

    def __init__(self, base_engine, logger=None):
        """Initialize search with base engine reference."""
        self.base_engine = base_engine
        self.logger = logger

    async def retrieve_context(
        self, query: str, context_type: ContextType = None
    ) -> ContextRetrievalResult:
        """Retrieve context based on query."""
        start_time = datetime.now()

        try:
            results = []

            # Search mission contexts
            if not context_type or context_type == ContextType.MISSION:
                mission_results = await self._search_mission_contexts(query)
                results.extend(mission_results)

            # Search agent capabilities
            if not context_type or context_type == ContextType.AGENT_CAPABILITY:
                capability_results = await self._search_agent_capabilities(query)
                results.extend(capability_results)

            # Search emergency contexts
            if not context_type or context_type == ContextType.EMERGENCY:
                emergency_results = await self._search_emergency_contexts(query)
                results.extend(emergency_results)

            # Sort by relevance score
            results.sort(key=lambda x: x.relevance_score, reverse=True)

            execution_time = (datetime.now() - start_time).total_seconds()

            return ContextRetrievalResult(
                retrieval_id=f"retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                query=query,
                results=results,
                execution_time=execution_time,
                success=True,
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ContextRetrievalResult(
                retrieval_id=f"retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                query=query,
                results=[],
                execution_time=execution_time,
                success=False,
                error_message=str(e),
            )

    async def _search_mission_contexts(self, query: str) -> list[SearchResult]:
        """Search mission contexts."""
        results = []
        query_lower = query.lower()

        for context in self.base_engine.contexts.values():
            relevance_score = 0.0

            # Check mission name
            if query_lower in context.mission_name.lower():
                relevance_score += 0.8

            # Check description
            if query_lower in context.description.lower():
                relevance_score += 0.6

            # Check capabilities
            for capability in context.capabilities_required:
                if query_lower in capability.lower():
                    relevance_score += 0.4

            # Check objectives
            for objective in context.objectives:
                if query_lower in objective.lower():
                    relevance_score += 0.5

            if relevance_score > 0:
                results.append(
                    SearchResult(
                        result_id=f"mission_{context.context_id}",
                        title=context.mission_name,
                        description=context.description,
                        relevance_score=relevance_score,
                        context_type=ContextType.MISSION,
                        metadata={"context_id": context.context_id},
                    )
                )

        return results

    async def _search_agent_capabilities(self, query: str) -> list[SearchResult]:
        """Search agent capabilities."""
        results = []
        query_lower = query.lower()

        for capability in self.base_engine.capabilities.values():
            relevance_score = 0.0

            # Check capability name
            if query_lower in capability.capability_name.lower():
                relevance_score += 0.8

            # Check description
            if query_lower in capability.description.lower():
                relevance_score += 0.6

            # Check skills
            for skill in capability.skills:
                if query_lower in skill.lower():
                    relevance_score += 0.4

            if relevance_score > 0:
                results.append(
                    SearchResult(
                        result_id=f"capability_{capability.capability_id}",
                        title=capability.capability_name,
                        description=capability.description,
                        relevance_score=relevance_score,
                        context_type=ContextType.AGENT_CAPABILITY,
                        metadata={"capability_id": capability.capability_id},
                    )
                )

        return results

    async def _search_emergency_contexts(self, query: str) -> list[SearchResult]:
        """Search emergency contexts."""
        results = []
        query_lower = query.lower()

        for emergency in self.base_engine.emergencies.values():
            relevance_score = 0.0

            # Check emergency type
            if query_lower in emergency.emergency_type.lower():
                relevance_score += 0.8

            # Check description
            if query_lower in emergency.description.lower():
                relevance_score += 0.6

            # Check affected systems
            for system in emergency.affected_systems:
                if query_lower in system.lower():
                    relevance_score += 0.4

            if relevance_score > 0:
                results.append(
                    SearchResult(
                        result_id=f"emergency_{emergency.emergency_id}",
                        title=emergency.emergency_type,
                        description=emergency.description,
                        relevance_score=relevance_score,
                        context_type=ContextType.EMERGENCY,
                        metadata={"emergency_id": emergency.emergency_id},
                    )
                )

        return results
