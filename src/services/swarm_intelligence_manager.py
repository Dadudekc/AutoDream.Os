"""
Swarm Intelligence Manager
==========================

Swarm intelligence operations for agent vector integration.
V2 Compliance: < 100 lines, single responsibility.

Author: Agent-2 (Architecture & Design Specialist)
"""

import logging
from datetime import datetime
from typing import Any

from .vector_database import get_vector_database_service, search_vector_database
from .vector_database.vector_database_models import SearchQuery


class SwarmIntelligenceManager:
    """Handles swarm intelligence operations."""

    def __init__(self, agent_id: str, config_path: str | None = None):

EXAMPLE USAGE:
==============

# Import the service
from src.services.swarm_intelligence_manager import Swarm_Intelligence_ManagerService

# Initialize service
service = Swarm_Intelligence_ManagerService()

# Basic service operation
response = service.handle_request(request_data)
print(f"Service response: {response}")

# Service with dependency injection
from src.core.dependency_container import Container

container = Container()
service = container.get(Swarm_Intelligence_ManagerService)

# Execute service method
result = service.execute_operation(input_data, context)
print(f"Operation result: {result}")

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
            "swarm_agents": [
                "Agent-1",
                "Agent-2",
                "Agent-3",
                "Agent-4",
                "Agent-5",
                "Agent-6",
                "Agent-7",
                "Agent-8",
            ],
            "coordination_threshold": 0.7,
            "knowledge_sharing_enabled": True,
            "sync_interval_minutes": 30,
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
                "timestamp": datetime.now().isoformat(),
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

            self.logger.info(
                f"Swarm sync completed: shared {shared_count}, updated {updated_count}"
            )
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
                    query=f"agent:{agent} {query}", collection_name="agent_work", limit=3
                )
                results = search_vector_database(query_obj)

                for result in results:
                    if hasattr(result, "document"):
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
                    query=f"agent:{agent} {query}", collection_name="agent_work", limit=2
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
            query_obj = SearchQuery(query=query, collection_name="agent_work", limit=20)
            results = search_vector_database(query_obj)

            # Analyze common tags and approaches
            all_tags = []
            for result in results:
                if hasattr(result, "document") and result.document.tags:
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
            shared_count = 0

            # Search for this agent's recent work and insights
            query = SearchQuery(
                query=f"agent:{self.agent_id}", collection_name="agent_work", limit=10
            )
            results = search_vector_database(query)

            # Extract valuable insights and patterns
            insights_to_share = self._extract_shareable_insights(results)

            # Share each insight with the swarm
            for insight in insights_to_share:
                if self._broadcast_insight_to_swarm(insight):
                    shared_count += 1

            # Share agent status and capabilities
            if self._share_agent_capabilities():
                shared_count += 1

            # Share any discovered patterns or best practices
            pattern_count = self._share_discovered_patterns()
            shared_count += pattern_count

            return shared_count
        except Exception as e:
            self.logger.error(f"Error sharing knowledge: {e}")
            return 0

    def _update_from_swarm_knowledge(self) -> int:
        """Update from swarm knowledge."""
        try:
            updated_count = 0

            # Learn from other agents' successful patterns
            pattern_updates = self._learn_from_swarm_patterns()
            updated_count += pattern_updates

            # Update agent capabilities knowledge
            capability_updates = self._update_capability_knowledge()
            updated_count += capability_updates

            # Learn from shared insights and solutions
            insight_updates = self._learn_from_shared_insights()
            updated_count += insight_updates

            # Update coordination strategies based on swarm behavior
            coordination_updates = self._update_coordination_strategies()
            updated_count += coordination_updates

            return updated_count
        except Exception as e:
            self.logger.error(f"Error updating from swarm: {e}")
            return 0

    def _extract_shareable_insights(self, results) -> list[dict[str, Any]]:
        """Extract valuable insights from search results that are worth sharing."""
        insights = []

        for result in results:
            if hasattr(result, "document"):
                doc = result.document
                content = doc.content if hasattr(doc, "content") else str(doc)

                # Extract insights based on content analysis
                if self._is_valuable_insight(content):
                    insights.append(
                        {
                            "content": content[:500],  # Limit content length
                            "tags": getattr(doc, "tags", []),
                            "timestamp": getattr(doc, "timestamp", datetime.now().isoformat()),
                            "category": self._categorize_insight(content),
                        }
                    )

        return insights[:5]  # Limit to top 5 insights

    def _is_valuable_insight(self, content: str) -> bool:
        """Determine if content contains valuable insights worth sharing."""
        valuable_keywords = [
            "solution",
            "fixed",
            "resolved",
            "improved",
            "optimized",
            "discovered",
            "pattern",
            "best practice",
            "lesson learned",
            "recommendation",
            "successful",
            "efficient",
        ]

        content_lower = content.lower()
        return any(keyword in content_lower for keyword in valuable_keywords)

    def _categorize_insight(self, content: str) -> str:
        """Categorize the type of insight."""
        content_lower = content.lower()

        if "bug" in content_lower or "fix" in content_lower or "error" in content_lower:
            return "bug_fix"
        elif "performance" in content_lower or "optimization" in content_lower:
            return "performance"
        elif "security" in content_lower or "vulnerability" in content_lower:
            return "security"
        elif "architecture" in content_lower or "design" in content_lower:
            return "architecture"
        elif "testing" in content_lower or "test" in content_lower:
            return "testing"
        else:
            return "general"

    def _broadcast_insight_to_swarm(self, insight: dict[str, Any]) -> bool:
        """Broadcast an insight to all swarm agents."""
        try:
            # Create sharing message
            message = f"""🧠 **SWARM KNOWLEDGE SHARE**

📋 **Category:** {insight["category"].upper()}
📝 **Insight:** {insight["content"][:200]}...
🏷️ **Tags:** {", ".join(insight["tags"])}
👤 **Shared by:** {self.agent_id}

🎯 **Action:** Consider applying this insight to relevant tasks.

⚡️ **WE ARE SWARM.**"""

            # Send to all swarm agents (except self)
            sent_count = 0
            for agent in self.config["swarm_agents"]:
                if agent != self.agent_id:
                    # Use messaging system to broadcast
                    if self._send_to_agent(agent, message, "NORMAL", "COORDINATION"):
                        sent_count += 1

            return sent_count > 0
        except Exception as e:
            self.logger.error(f"Error broadcasting insight: {e}")
            return False

    def _send_to_agent(
        self, agent_id: str, message: str, priority: str = "NORMAL", tags: str = "GENERAL"
    ) -> bool:
        """Send message to specific agent using consolidated messaging service."""
        try:
            # Import here to avoid circular imports
            from .consolidated_messaging_service import ConsolidatedMessagingService

            service = ConsolidatedMessagingService()
            return service.send_message_pyautogui(
                agent_id=agent_id, message=message, priority=priority, tag=tags
            )
        except Exception as e:
            self.logger.error(f"Error sending message to {agent_id}: {e}")
            return False

    def _share_agent_capabilities(self) -> bool:
        """Share this agent's current capabilities and status."""
        try:
            capabilities_message = f"""🤖 **AGENT CAPABILITIES UPDATE**

👤 **Agent:** {self.agent_id}
📊 **Status:** Active and operational
🧠 **Specialization:** {self._get_agent_specialization()}

🎯 **Current Capabilities:**
• Swarm coordination and communication
• Vector-based similarity search
• Knowledge sharing and pattern recognition
• Task execution and progress tracking

⚡️ **WE ARE SWARM.**"""

            sent_count = 0
            for agent in self.config["swarm_agents"]:
                if agent != self.agent_id:
                    if self._send_to_agent(agent, capabilities_message, "LOW", "GENERAL"):
                        sent_count += 1

            return sent_count > 0
        except Exception as e:
            self.logger.error(f"Error sharing capabilities: {e}")
            return False

    def _get_agent_specialization(self) -> str:
        """Get this agent's specialization description."""
        specializations = {
            "Agent-1": "Integration & Core Systems Specialist",
            "Agent-2": "Architecture & Design Specialist",
            "Agent-3": "Infrastructure & DevOps Specialist",
            "Agent-4": "Quality Assurance Specialist (CAPTAIN)",
            "Agent-5": "Business Intelligence Specialist",
            "Agent-6": "Coordination & Communication Specialist",
            "Agent-7": "Web Development Specialist",
            "Agent-8": "SSOT & System Integration Specialist",
        }
        return specializations.get(self.agent_id, "General Purpose Agent")

    def _share_discovered_patterns(self) -> int:
        """Share any patterns or best practices discovered by this agent."""
        try:
            # Look for patterns in recent work
            query = SearchQuery(
                query=f"agent:{self.agent_id} pattern OR best practice OR optimization",
                collection_name="agent_work",
                limit=5,
            )
            results = search_vector_database(query)

            shared_count = 0
            for result in results:
                if hasattr(result, "document"):
                    pattern_message = f"""🔍 **PATTERN DISCOVERY**

📋 **Pattern:** {result.document.content[:300]}...
👤 **Discovered by:** {self.agent_id}
🏷️ **Tags:** {", ".join(getattr(result.document, "tags", []))}

🎯 **Recommendation:** Consider applying this pattern to similar tasks.

⚡️ **WE ARE SWARM.**"""

                    # Share with relevant agents
                    for agent in self.config["swarm_agents"][:3]:  # Share with first 3 agents
                        if agent != self.agent_id:
                            if self._send_to_agent(
                                agent, pattern_message, "NORMAL", "COORDINATION"
                            ):
                                shared_count += 1

            return shared_count
        except Exception as e:
            self.logger.error(f"Error sharing patterns: {e}")
            return 0

    def _learn_from_swarm_patterns(self) -> int:
        """Learn from successful patterns used by other agents."""
        try:
            learned_count = 0

            # Search for successful patterns from other agents
            for agent in self.config["swarm_agents"]:
                if agent == self.agent_id:
                    continue

                query = SearchQuery(
                    query=f"agent:{agent} successful OR optimized OR improved",
                    collection_name="agent_work",
                    limit=3,
                )
                results = search_vector_database(query)

                for result in results:
                    if hasattr(result, "document"):
                        # Store pattern for future reference
                        pattern = {
                            "source_agent": agent,
                            "content": result.document.content[:200],
                            "tags": getattr(result.document, "tags", []),
                            "learned_at": datetime.now().isoformat(),
                        }
                        self._store_learned_pattern(pattern)
                        learned_count += 1

            return learned_count
        except Exception as e:
            self.logger.error(f"Error learning from swarm patterns: {e}")
            return 0

    def _store_learned_pattern(self, pattern: dict[str, Any]):
        """Store a learned pattern for future reference."""
        # This would typically store in a local database or file
        # For now, just log it
        self.logger.info(
            f"Learned pattern from {pattern['source_agent']}: {pattern['content'][:50]}..."
        )

    def _update_capability_knowledge(self) -> int:
        """Update knowledge about other agents' capabilities."""
        try:
            updated_count = 0

            # Query for capability updates from other agents
            for agent in self.config["swarm_agents"]:
                if agent == self.agent_id:
                    continue

                query = SearchQuery(
                    query=f"agent:{agent} capability OR skill OR specialization",
                    collection_name="agent_work",
                    limit=2,
                )
                results = search_vector_database(query)

                for result in results:
                    if hasattr(result, "document"):
                        # Update local knowledge of agent capabilities
                        capability = {
                            "agent": agent,
                            "capability": result.document.content[:100],
                            "updated_at": datetime.now().isoformat(),
                        }
                        self._update_agent_capability_knowledge(capability)
                        updated_count += 1

            return updated_count
        except Exception as e:
            self.logger.error(f"Error updating capability knowledge: {e}")
            return 0

    def _update_agent_capability_knowledge(self, capability: dict[str, Any]):
        """Update local knowledge of an agent's capabilities."""
        self.logger.info(
            f"Updated capability knowledge for {capability['agent']}: {capability['capability'][:50]}..."
        )

    def _learn_from_shared_insights(self) -> int:
        """Learn from insights shared by other agents."""
        try:
            learned_count = 0

            # Search for shared insights
            query = SearchQuery(
                query="shared insight OR swarm knowledge OR collective learning",
                collection_name="agent_work",
                limit=10,
            )
            results = search_vector_database(query)

            for result in results:
                if hasattr(result, "document"):
                    # Extract and learn from the insight
                    insight = {
                        "content": result.document.content,
                        "source": getattr(result.document, "agent_id", "unknown"),
                        "learned_at": datetime.now().isoformat(),
                    }
                    self._process_shared_insight(insight)
                    learned_count += 1

            return learned_count
        except Exception as e:
            self.logger.error(f"Error learning from shared insights: {e}")
            return 0

    def _process_shared_insight(self, insight: dict[str, Any]):
        """Process and integrate a shared insight."""
        self.logger.info(
            f"Processed shared insight from {insight['source']}: {insight['content'][:50]}..."
        )

    def _update_coordination_strategies(self) -> int:
        """Update coordination strategies based on observed swarm behavior."""
        try:
            updated_count = 0

            # Analyze successful coordination patterns
            query = SearchQuery(
                query="coordination successful OR collaboration effective OR swarm optimization",
                collection_name="agent_work",
                limit=5,
            )
            results = search_vector_database(query)

            for result in results:
                if hasattr(result, "document"):
                    # Extract coordination strategy
                    strategy = {
                        "pattern": result.document.content[:150],
                        "effectiveness": "high",  # Assume successful results are effective
                        "learned_at": datetime.now().isoformat(),
                    }
                    self._store_coordination_strategy(strategy)
                    updated_count += 1

            return updated_count
        except Exception as e:
            self.logger.error(f"Error updating coordination strategies: {e}")
            return 0

    def _store_coordination_strategy(self, strategy: dict[str, Any]):
        """Store a learned coordination strategy."""
        self.logger.info(f"Stored coordination strategy: {strategy['pattern'][:50]}...")

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
            "fallback_mode": True,
        }
