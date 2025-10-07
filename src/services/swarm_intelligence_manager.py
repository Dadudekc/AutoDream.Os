"""
Swarm Intelligence Manager
==========================

Swarm intelligence operations for agent vector integration.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
"""

import logging
from typing import Any
from datetime import datetime

from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery


class SwarmIntelligenceManager:
    """Handles swarm intelligence operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):
        """Initialize swarm intelligence manager."""
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
        """Load swarm intelligence configuration."""
        return {
            "swarm_agents": ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"],
            "coordination_threshold": 0.7,
            "knowledge_sharing_enabled": True,
            "sync_interval_minutes": 30
        }

    def get_swarm_intelligence(self, query: str) -> dict[str, Any]:
        """Get swarm intelligence insights from collective knowledge."""
        try:
            if self.vector_integration["status"] != "connected":
                return self._get_fallback_intelligence(query)

            # Search for collective knowledge
            collective_insights = self._search_collective_knowledge(query)
            coordination_opportunities = self._find_coordination_opportunities(query)
            swarm_patterns = self._analyze_swarm_patterns(query)

            return {
                "query": query,
                "insights": collective_insights,
                "coordination_opportunities": coordination_opportunities,
                "swarm_patterns": swarm_patterns,
                "confidence": self._calculate_confidence(collective_insights),
                "source_agents": self._get_contributing_agents(collective_insights),
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            self.logger.error(f"Error getting swarm intelligence: {e}")
            return {"error": str(e), "query": query}

    def sync_with_swarm(self) -> bool:
        """Sync with swarm by sharing knowledge and updates."""
        try:
            if self.vector_integration["status"] != "connected":
                self.logger.warning("Vector DB not connected, skipping swarm sync")
                return False

            # Share agent's knowledge with swarm
            shared_count = self._share_knowledge_with_swarm()

            # Update from swarm knowledge
            updated_count = self._update_from_swarm_knowledge()

            self.logger.info(f"Swarm sync completed: shared {shared_count}, updated {updated_count}")
            return True

        except Exception as e:
            self.logger.error(f"Error syncing with swarm: {e}")
            return False

    def _search_collective_knowledge(self, query: str) -> list[str]:
        """Search for collective knowledge across all agents."""
        try:
            insights = []

            # Search across all agents' work
            for agent in self.config["swarm_agents"]:
                if agent == self.agent_id:
                    continue

                query_obj = SearchQuery(
                    query=f"agent:{agent} {query}",
                    collection_name="agent_work",
                    limit=3
                )
                results = search_vector_database(query_obj)

                for result in results:
                    if hasattr(result, 'document'):
                        insights.append(f"From {agent}: {result.document.content[:100]}...")

            return insights[:5]  # Limit to top 5 insights
        except Exception as e:
            self.logger.error(f"Error searching collective knowledge: {e}")
            return []

    def _find_coordination_opportunities(self, query: str) -> list[str]:
        """Find opportunities for coordination with other agents."""
        try:
            opportunities = []

            # Look for similar work by other agents
            for agent in self.config["swarm_agents"]:
                if agent == self.agent_id:
                    continue

                query_obj = SearchQuery(
                    query=f"agent:{agent} {query}",
                    collection_name="agent_work",
                    limit=2
                )
                results = search_vector_database(query_obj)

                if results:
                    opportunities.append(f"Coordinate with {agent} on similar work")

            return opportunities[:3]  # Limit to top 3 opportunities
        except Exception as e:
            self.logger.error(f"Error finding coordination opportunities: {e}")
            return []

    def _analyze_swarm_patterns(self, query: str) -> list[str]:
        """Analyze patterns across the swarm."""
        try:
            patterns = []

            # Look for common patterns in swarm work
            query_obj = SearchQuery(
                query=query,
                collection_name="agent_work",
                limit=20
            )
            results = search_vector_database(query_obj)

            # Analyze common tags and approaches
            all_tags = []
            for result in results:
                if hasattr(result, 'document') and result.document.tags:
                    all_tags.extend(result.document.tags)

            if all_tags:
                from collections import Counter
                common_tags = Counter(all_tags).most_common(3)
                for tag, count in common_tags:
                    patterns.append(f"Common approach: {tag} (used by {count} agents)")

            return patterns
        except Exception as e:
            self.logger.error(f"Error analyzing swarm patterns: {e}")
            return []

    def _calculate_confidence(self, insights: list[str]) -> float:
        """Calculate confidence based on number of insights."""
        if not insights:
            return 0.3
        return min(0.9, 0.5 + (len(insights) * 0.1))

    def _get_contributing_agents(self, insights: list[str]) -> list[str]:
        """Get list of agents contributing to insights."""
        agents = set()
        for insight in insights:
            if "From " in insight:
                agent = insight.split("From ")[1].split(":")[0]
                agents.add(agent)
        return list(agents)[:5]  # Limit to top 5

    def _share_knowledge_with_swarm(self) -> int:
        """Share this agent's knowledge with the swarm."""
        try:
            # Search for this agent's recent work
            query = SearchQuery(
                query=f"agent:{self.agent_id}",
                collection_name="agent_work",
                limit=10
            )
            results = search_vector_database(query)

            # Share knowledge by tagging with swarm identifiers
            shared_count = 0
            for result in results:
                if hasattr(result, 'document'):
                    # Add swarm-shared tag to make knowledge discoverable
                    if result.document.tags:
                        if "swarm-shared" not in result.document.tags:
                            result.document.tags.append("swarm-shared")
                            result.document.tags.append(f"from:{self.agent_id}")
                            shared_count += 1
                    else:
                        result.document.tags = ["swarm-shared", f"from:{self.agent_id}"]
                        shared_count += 1

            self.logger.info(f"Shared {shared_count} knowledge items with swarm")
            return shared_count
        except Exception as e:
            self.logger.error(f"Error sharing knowledge: {e}")
            return 0

    def _update_from_swarm_knowledge(self) -> int:
        """Update from swarm knowledge."""
        try:
            # Search for knowledge shared by other agents
            query = SearchQuery(
                query="swarm-shared",
                collection_name="agent_work",
                limit=50
            )
            swarm_knowledge = search_vector_database(query)

            # Filter out this agent's own contributions
            updated_count = 0
            for result in swarm_knowledge:
                if hasattr(result, 'document'):
                    # Skip own knowledge
                    if result.document.tags and f"from:{self.agent_id}" in result.document.tags:
                        continue

                    # Process relevant knowledge
                    if self._is_relevant_to_agent(result.document):
                        # Mark as integrated
                        if "integrated" not in result.document.tags:
                            result.document.tags.append(f"integrated-by:{self.agent_id}")
                            updated_count += 1

            self.logger.info(f"Integrated {updated_count} knowledge items from swarm")
            return updated_count
        except Exception as e:
            self.logger.error(f"Error updating from swarm: {e}")
            return 0

    def _is_relevant_to_agent(self, document: Any) -> bool:
        """Check if document is relevant to this agent."""
        try:
            # Check if document tags match agent's areas of interest
            if not document.tags:
                return False

            # Simple relevance check based on tags
            relevant_tags = ["coordination", "architecture", "testing", "deployment"]
            return any(tag in document.tags for tag in relevant_tags)
        except Exception:
            return False

    def _get_fallback_intelligence(self, query: str) -> dict[str, Any]:
        """Get fallback intelligence when vector DB is unavailable."""
        return {
            "query": query,
            "insights": [
                "Leverage collective knowledge",
                "Coordinate with other agents",
                "Apply swarm optimization techniques",
            ],
            "coordination_opportunities": [],
            "swarm_patterns": [],
            "confidence": 0.6,
            "source_agents": [],
            "timestamp": datetime.now().isoformat(),
            "fallback_mode": True
        }
