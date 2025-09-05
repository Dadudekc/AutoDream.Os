from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Agent Documentation CLI

Command-line interface for AI agents to interact with the vectorized documentation system.
"""

import logging

# Add src to path
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent.parent / "src"))


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AgentDocumentationCLI:
    """CLI for agent documentation access."""
    
    def __init__(self):
        self.vector_db = None
        self.doc_service = None
        self.current_agent = None
    
    def initialize(self, db_path: str = "vector_db"):
        """Initialize the documentation service."""
        try:
            self.vector_db = create_vector_database(db_path)
            self.doc_service = create_agent_documentation_service(self.vector_db)
            get_logger(__name__).info("✅ Documentation service initialized")
            return True
        except Exception as e:
            get_logger(__name__).error(f"❌ Failed to initialize: {e}")
            return False
    
    def set_agent(self, agent_id: str, role: str = "", domain: str = "", task: str = ""):
        """Set the current agent context."""
        context = {}
        if role:
            context["role"] = role
        if domain:
            context["domain"] = domain
        if task:
            context["current_task"] = task
        
        self.doc_service.set_agent_context(agent_id, context)
        self.current_agent = agent_id
        get_logger(__name__).info(f"✅ Set agent context for {agent_id}")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search documentation."""
        if not self.current_agent:
            get_logger(__name__).error("❌ No agent set. Use --set-agent first.")
            return []
        
        results = self.doc_service.search_documentation(
            self.current_agent, query, n_results
        )
        
        return results
    
    def get_relevant_docs(self, doc_types: List[str] = None) -> List[Dict[str, Any]]:
        """Get relevant documentation for current agent."""
        if not self.current_agent:
            get_logger(__name__).error("❌ No agent set. Use --set-agent first.")
            return []
        
        return self.doc_service.get_agent_relevant_docs(self.current_agent, doc_types)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get documentation summary for current agent."""
        if not self.current_agent:
            get_logger(__name__).error("❌ No agent set. Use --set-agent first.")
            return {}
        
        return self.doc_service.get_documentation_summary(self.current_agent)
    
    def get_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions."""
        if not self.current_agent:
            get_logger(__name__).error("❌ No agent set. Use --set-agent first.")
            return []
        
        return self.doc_service.get_search_suggestions(self.current_agent, partial_query)
    
    def export_knowledge(self, output_path: str) -> bool:
        """Export agent knowledge."""
        if not self.current_agent:
            get_logger(__name__).error("❌ No agent set. Use --set-agent first.")
            return False
        
        return self.doc_service.export_agent_knowledge(self.current_agent, output_path)

def format_search_results(results: List[Dict[str, Any]]) -> str:
    """Format search results for display."""
    if not get_unified_validator().validate_required(results):
        return "No results found."
    
    output = []
    for i, result in enumerate(results, 1):
        metadata = result.get('metadata', {})
        file_path = metadata.get('file_path', 'Unknown')
        distance = result.get('distance', 0)
        
        # Truncate content for display
        content = result.get('content', '')
        if len(content) > 200:
            content = content[:200] + "..."
        
        output.append(f"""
{i}. 📄 {file_path}
   📊 Relevance: {1-distance:.3f}
   📝 Content: {content}
""")
    
    return "\n".join(output)


if __name__ == "__main__":
    main()

