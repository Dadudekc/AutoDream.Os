"""
Agent Documentation Integration

Simple integration module for AI agents to access vectorized documentation.
"""


# Add current directory to path for imports
current_dir = get_unified_utility().Path(__file__).parent
sys.path.insert(0, str(current_dir))

try:
except ImportError as e:
    get_logger(__name__).info(f"Warning: Could not import vector database modules: {e}")
    get_logger(__name__).info("Make sure to install requirements: pip install -r requirements-vector.txt")


class AgentDocs:
    """
    Simple interface for AI agents to access project documentation.
    """

    def __init__(self, agent_id: str, db_path: str = "vector_db"):
        """
        Initialize agent documentation access.

        Args:
            agent_id: Unique identifier for the agent
            db_path: Path to the vector database
        """
        self.agent_id = agent_id
        self.db_path = db_path
        self.doc_service = None
        self._initialize()

    def _initialize(self):
        """Initialize the documentation service."""
        try:
            vector_db = create_vector_database(self.db_path)
            self.doc_service = create_agent_documentation_service(vector_db)
        except Exception as e:
            get_logger(__name__).info(f"Warning: Could not initialize documentation service: {e}")
            self.doc_service = None

    def set_context(self, role: str = "", domain: str = "", task: str = ""):
        """
        Set agent context for better search relevance.

        Args:
            role: Agent's role (e.g., "Web Development Specialist")
            domain: Agent's domain (e.g., "JavaScript, TypeScript, Frontend")
            task: Current task description
        """
        if not self.doc_service:
            get_logger(__name__).info("Documentation service not available")
            return

        context = {}
        if role:
            context["role"] = role
        if domain:
            context["domain"] = domain
        if task:
            context["current_task"] = task

        self.doc_service.set_agent_context(self.agent_id, context)
        get_logger(__name__).info(f"✅ Context set for {self.agent_id}")

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search project documentation.

        Args:
            query: Search query
            max_results: Maximum number of results to return

        Returns:
            List of search results with content and metadata
        """
        if not self.doc_service:
            get_logger(__name__).info("Documentation service not available")
            return []

        results = self.doc_service.search_documentation(
            self.agent_id, query, max_results
        )

        get_logger(__name__).info(f"🔍 Found {len(results)} results for '{query}'")
        return results

    def get_relevant_docs(self, doc_types: List[str] = None) -> List[Dict[str, Any]]:
        """
        Get documentation relevant to the agent's role and domain.

        Args:
            doc_types: Optional list of document types to filter by

        Returns:
            List of relevant documents
        """
        if not self.doc_service:
            get_logger(__name__).info("Documentation service not available")
            return []

        results = self.doc_service.get_agent_relevant_docs(self.agent_id, doc_types)
        get_logger(__name__).info(f"📚 Found {len(results)} relevant documents")
        return results

    def get_summary(self) -> Dict[str, Any]:
        """
        Get a summary of available documentation for this agent.

        Returns:
            Dictionary with documentation summary
        """
        if not self.doc_service:
            get_logger(__name__).info("Documentation service not available")
            return {}

        return self.doc_service.get_documentation_summary(self.agent_id)

    def get_suggestions(self, partial_query: str) -> List[str]:
        """
        Get search suggestions based on agent context.

        Args:
            partial_query: Partial search query

        Returns:
            List of suggested search terms
        """
        if not self.doc_service:
            get_logger(__name__).info("Documentation service not available")
            return []

        return self.doc_service.get_search_suggestions(self.agent_id, partial_query)

    def is_available(self) -> bool:
        """
        Check if the documentation service is available.

        Returns:
            True if service is available, False otherwise
        """
        return self.doc_service is not None


# Convenience function for quick agent setup
def get_agent_docs(
    agent_id: str, role: str = "", domain: str = "", task: str = ""
) -> AgentDocs:
    """
    Quick setup function for agent documentation access.

    Args:
        agent_id: Unique identifier for the agent
        role: Agent's role
        domain: Agent's domain
        task: Current task description

    Returns:
        Initialized AgentDocs instance
    """
    docs = AgentDocs(agent_id)
    if role or domain or task:
        docs.set_context(role, domain, task)
    return docs


# Example usage for agents
if __name__ == "__main__":
    # Example: Agent-7 (Web Development Specialist) accessing documentation
    agent_docs = get_agent_docs(
        agent_id="Agent-7",
        role="Web Development Specialist",
        domain="JavaScript, TypeScript, Frontend Development",
        task="Implementing V2 compliance patterns",
    )

    if agent_docs.is_available():
        # Search for specific information
        results = agent_docs.search("JavaScript V2 compliance patterns", max_results=3)

        # Get relevant documentation
        relevant = agent_docs.get_relevant_docs([".md", ".js", ".ts"])

        # Get summary
        summary = agent_docs.get_summary()
        get_logger(__name__).info(f"📊 Documentation summary: {summary}")

        # Get search suggestions
        suggestions = agent_docs.get_suggestions("V2")
        get_logger(__name__).info(f"💡 Search suggestions: {suggestions}")
    else:
        get_logger(__name__).info(
            "❌ Documentation service not available. Run setup_vector_database.py first."
        )

