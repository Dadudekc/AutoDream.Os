"""Search History Service.

Manages search history and provides suggestions based on past queries.
"""

logger = logging.getLogger(__name__)


class SearchHistoryService:
    """Service for managing search history and providing query suggestions."""

    def __init__(self, max_history: int = 100):
        self.search_history: List[Dict[str, Any]] = []
        self.max_history = max_history
        self.agent_queries = defaultdict(list)

    def add_search(
        self, agent_id: str, query: str, enhanced_query: str, results_count: int
    ) -> None:
        """Add a search to the history.

        Args:
            agent_id: Agent that performed the search
            query: Original search query
            enhanced_query: Context-enhanced query
            results_count: Number of results returned
        """
        search_entry = {
            "agent_id": agent_id,
            "query": query,
            "enhanced_query": enhanced_query,
            "results_count": results_count,
            "timestamp": datetime.now().isoformat(),
        }

        self.search_history.append(search_entry)
        self.agent_queries[agent_id].append(search_entry)

        # Maintain history limits
        if len(self.search_history) > self.max_history:
            self.search_history = self.search_history[-self.max_history :]

        # Keep only last 50 queries per agent
        if len(self.agent_queries[agent_id]) > 50:
            self.agent_queries[agent_id] = self.agent_queries[agent_id][-50:]

    def get_search_suggestions(
        self, agent_id: str, partial_query: str, agent_context: Dict[str, Any] = None
    ) -> List[str]:
        """Get search suggestions based on history and context.

        Args:
            agent_id: Agent requesting suggestions
            partial_query: Partial query to complete
            agent_context: Agent context for context-aware suggestions

        Returns:
            List of suggested search terms
        """
        suggestions = []

        # Context-based suggestions
        if agent_context:
            role = agent_context.get("role", "")
            domain = agent_context.get("domain", "")

            if role and partial_query.lower() in role.lower():
                suggestions.extend(
                    [
                        f"{role} documentation",
                        f"{role} examples",
                        f"{role} best practices",
                    ]
                )

            if domain and partial_query.lower() in domain.lower():
                suggestions.extend(
                    [
                        f"{domain} architecture",
                        f"{domain} implementation",
                        f"{domain} patterns",
                    ]
                )

        # Common search patterns
        common_patterns = [
            "how to",
            "examples",
            "troubleshooting",
            "configuration",
            "setup",
            "deployment",
        ]

        for pattern in common_patterns:
            if pattern.startswith(partial_query.lower()):
                suggestions.append(pattern)

        # History-based suggestions
        agent_history = self.agent_queries.get(agent_id, [])
        for entry in agent_history[-10:]:  # Last 10 queries
            query = entry["query"]
            if partial_query.lower() in query.lower() and query not in suggestions:
                suggestions.append(query)

        return suggestions[:10]  # Return top 10 suggestions

    def get_agent_search_history(self, agent_id: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Get search history for a specific agent.

        Args:
            agent_id: Agent to get history for
            limit: Maximum number of entries to return

        Returns:
            List of search history entries
        """
        return self.agent_queries.get(agent_id, [])[-limit:]

    def clear_history(self, agent_id: str = None) -> None:
        """Clear search history.

        Args:
            agent_id: If provided, clear history for specific agent only
        """
        if agent_id:
            self.agent_queries[agent_id] = []
            # Remove from main history
            self.search_history = [
                entry for entry in self.search_history if entry["agent_id"] != agent_id
            ]
        else:
            self.search_history = []
            self.agent_queries = defaultdict(list)

        get_logger(__name__).info(f"Cleared search history for {agent_id or 'all agents'}")

    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics.

        Returns:
            Dictionary with search statistics
        """
        total_searches = len(self.search_history)
        unique_agents = len(self.agent_queries)

        agent_stats = {}
        for agent_id, queries in self.agent_queries.items():
            agent_stats[agent_id] = {
                "total_searches": len(queries),
                "last_search": queries[-1]["timestamp"] if queries else None,
            }

        return {
            "total_searches": total_searches,
            "unique_agents": unique_agents,
            "agent_statistics": agent_stats,
        }
