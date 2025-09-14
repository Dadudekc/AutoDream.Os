"""Documentation Search Service.

Handles semantic search functionality for the documentation system.
"""

logger = logging.getLogger(__name__)


class DocumentationSearchService:
    """Service for searching documentation with semantic similarity."""

    def __init__(self, vector_db):
        self.vector_db = vector_db

    def search(
        self,
        query: str,
        agent_id: str = None,
        n_results: int = 5,
        context_boost: bool = True,
        agent_context: Dict[str, Any] = None,
    ) -> List[Dict[str, Any]]:
        """Search documentation with optional context enhancement.

        Args:
            query: Search query
            agent_id: Optional agent identifier for context
            n_results: Number of results to return
            context_boost: Whether to enhance query with context
            agent_context: Agent context information

        Returns:
            List of search results
        """
        enhanced_query = query

        if context_boost and agent_context:
            role = agent_context.get("role", "")
            domain = agent_context.get("domain", "")
            current_task = agent_context.get("current_task", "")

            context_parts = [part for part in [role, domain, current_task] if part]
            if context_parts:
                enhanced_query = f"{query} {' '.join(context_parts)}"

        results = self.vector_db.search_documents(enhanced_query, n_results)

        # Add search metadata
        for result in results:
            result["agent_id"] = agent_id
            result["search_timestamp"] = datetime.now().isoformat()
            result["original_query"] = query
            result["enhanced_query"] = enhanced_query

        get_logger(__name__).info(f"Search completed: '{query}' -> {len(results)} results")
        return results

    def get_relevant_docs(
        self, agent_context: Dict[str, Any], doc_types: List[str] = None
    ) -> List[Dict[str, Any]]:
        """Get documentation relevant to agent context.

        Args:
            agent_context: Agent context information
            doc_types: Optional document type filters

        Returns:
            List of relevant documents
        """
        role = agent_context.get("role", "")
        domain = agent_context.get("domain", "")

        search_terms = []
        if role:
            search_terms.append(role)
        if domain:
            search_terms.append(domain)

        if not get_unified_validator().validate_required(search_terms):
            return []

        query = " ".join(search_terms)
        results = self.vector_db.search_documents(query, n_results=10)

        # Filter by document types if specified
        if doc_types:
            filtered_results = []
            for result in results:
                file_type = result["metadata"].get("file_type", "")
                if any(doc_type in file_type for doc_type in doc_types):
                    filtered_results.append(result)
            results = filtered_results

        return results
