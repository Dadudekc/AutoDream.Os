"""
Vector Database SSOT Indexer for Strategic Oversight & Emergency Intervention

This module provides comprehensive SSOT (Single Source of Truth) indexing capabilities
for intelligent swarm coordination, pattern analysis, and strategic decision making.

Key Features:
- SSOT document indexing with semantic search
- Intelligent context retrieval for mission coordination
- Pattern analysis for strategic decisions
- Emergency intervention based on historical success patterns
- Agent capability matching and task assignment optimization

Author: Agent-3 (Strategic Vector Database Integration)
"""

from ..core.unified_data_processing_system import get_unified_data_processing



@dataclass
class SSOTDocument:
    """SSOT Document structure for vector indexing."""

    title: str
    content: str
    document_type: DocumentType
    source_file: str
    agent_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_vector_document(self) -> VectorDocument:
        """Convert to vector document for indexing."""
        return VectorDocument(
            content=f"{self.title}\n\n{self.content}",
            document_type=self.document_type,
            source_file=self.source_file,
            agent_id=self.agent_id,
            metadata={
                **self.metadata,
                "tags": self.tags,
                "created_at": self.created_at.isoformat(),
                "updated_at": self.updated_at.isoformat()
            }
        )


class VectorDatabaseSSOTIndexer:
    """
    Vector Database SSOT Indexer for Strategic Oversight.

    This class provides comprehensive SSOT indexing and intelligent retrieval
    capabilities for enhanced swarm coordination and mission success.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize the SSOT indexer."""
        self.config = config or {}
        self.vector_db = VectorDatabaseService(self.config.get("vector_db_config"))
        self.embedding_service = EmbeddingService(self.config.get("embedding_config"))

        # SSOT collections
        self.ssot_collections = {
            "captain_handbook": "captain_agent_4_operational_handbook",
            "captain_logs": "captain_agent_4_operational_logs",
            "agent_status": "agent_status_matrix",
            "v2_compliance": "v2_compliance_standards",
            "mission_progress": "mission_progress_tracking",
            "strategic_patterns": "strategic_decision_patterns",
            "emergency_responses": "emergency_intervention_patterns"
        }

        # Initialize collections
        self._initialize_collections()

    def _initialize_collections(self):
        """Initialize vector database collections for SSOT indexing."""
        for collection_name in self.ssot_collections.values():
            try:
                self.vector_db.create_collection(collection_name)
            except Exception as e:
                get_logger(__name__).info(f"Warning: Could not create collection {collection_name}: {e}")

    def index_captain_handbook(self, handbook_content: str, source_file: str):
        """Index Captain Agent-4 Operational Handbook."""
        document = SSOTDocument(
            title="Captain Agent-4 Operational Handbook",
            content=handbook_content,
            document_type=DocumentType.CAPTAIN_HANDBOOK,
            source_file=source_file,
            agent_id="captain_agent_4",
            tags=["strategic_oversight", "operational_protocols", "emergency_intervention"],
            metadata={"priority": "critical", "access_level": "captain_only"}
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["captain_handbook"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_captain_logs(self, logs_content: str, source_file: str, mission_status: str):
        """Index Captain Agent-4 Operational Logs."""
        document = SSOTDocument(
            title=f"Captain Agent-4 Operational Logs - {mission_status}",
            content=logs_content,
            document_type=DocumentType.CAPTAIN_LOGS,
            source_file=source_file,
            agent_id="captain_agent_4",
            tags=["mission_status", "operational_logs", "cycle_tracking"],
            metadata={"current_mission": mission_status, "log_type": "operational"}
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["captain_logs"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_agent_status_matrix(self, agent_data: Dict[str, Any], source_file: str):
        """Index Agent Status Matrix for capability matching."""
        content = json.dumps(agent_data, indent=2)

        document = SSOTDocument(
            title="Agent Status Matrix - Current Capabilities",
            content=content,
            document_type=DocumentType.AGENT_STATUS,
            source_file=source_file,
            tags=["agent_capabilities", "status_matrix", "task_assignment"],
            metadata={"agent_count": len(agent_data), "matrix_type": "capability_overview"}
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["agent_status"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_v2_compliance_standards(self, standards_content: str, source_file: str):
        """Index V2 Compliance Standards and Architecture Patterns."""
        document = SSOTDocument(
            title="V2 Compliance Standards & Architecture Patterns",
            content=standards_content,
            document_type=DocumentType.V2_COMPLIANCE,
            source_file=source_file,
            tags=["v2_compliance", "architecture_patterns", "development_standards"],
            metadata={"compliance_level": "v2", "standard_type": "architectural"}
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["v2_compliance"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_mission_progress(self, mission_data: Dict[str, Any], source_file: str):
        """Index Mission Progress and Task Completion Status."""
        content = json.dumps(mission_data, indent=2)

        document = SSOTDocument(
            title=f"Mission Progress - {mission_data.get('current_phase', 'Unknown')}",
            content=content,
            document_type=DocumentType.MISSION_PROGRESS,
            source_file=source_file,
            tags=["mission_progress", "task_completion", "phase_tracking"],
            metadata={
                "current_phase": mission_data.get("current_phase"),
                "completed_tasks": len(mission_data.get("completed_tasks", [])),
                "pending_tasks": len(mission_data.get("pending_tasks", []))
            }
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["mission_progress"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_strategic_pattern(self, pattern_data: Dict[str, Any], pattern_type: str):
        """Index Strategic Decision Patterns for Future Reference."""
        content = json.dumps(pattern_data, indent=2)

        document = SSOTDocument(
            title=f"Strategic Pattern - {pattern_type}",
            content=content,
            document_type=DocumentType.STRATEGIC_PATTERN,
            source_file="strategic_pattern_analysis",
            tags=["strategic_patterns", pattern_type, "decision_making"],
            metadata={
                "pattern_type": pattern_type,
                "success_rate": pattern_data.get("success_rate", 0),
                "usage_count": pattern_data.get("usage_count", 0)
            }
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["strategic_patterns"]
        self.vector_db.add_document(collection_name, vector_doc)

    def index_emergency_response(self, response_data: Dict[str, Any], emergency_type: str):
        """Index Emergency Intervention Patterns."""
        content = json.dumps(response_data, indent=2)

        document = SSOTDocument(
            title=f"Emergency Response Pattern - {emergency_type}",
            content=response_data.get("description", ""),
            document_type=DocumentType.EMERGENCY_RESPONSE,
            source_file="emergency_intervention_log",
            tags=["emergency_response", emergency_type, "intervention_pattern"],
            metadata={
                "emergency_type": emergency_type,
                "response_time": response_data.get("response_time_seconds", 0),
                "success_rate": response_data.get("success_rate", 0),
                "intervention_steps": response_data.get("steps", [])
            }
        )

        vector_doc = document.to_vector_document()
        collection_name = self.ssot_collections["emergency_responses"]
        self.vector_db.add_document(collection_name, vector_doc)

    def search_intelligent_context(self, query: str, context_type: str = "general",
                                  agent_id: Optional[str] = None, limit: int = 5) -> List[SearchResult]:
        """
        Perform intelligent context search for strategic oversight.

        Args:
            query: Search query for context retrieval
            context_type: Type of context (general, strategic, emergency, mission)
            agent_id: Specific agent context (optional)
            limit: Maximum number of results to return

        Returns:
            List of relevant search results with context
        """
        # Determine which collections to search based on context type
        collections_to_search = []
        if context_type == "strategic" or context_type == "general":
            collections_to_search.extend([
                self.ssot_collections["captain_handbook"],
                self.ssot_collections["strategic_patterns"]
            ])
        if context_type == "emergency" or context_type == "general":
            collections_to_search.append(self.ssot_collections["emergency_responses"])
        if context_type == "mission" or context_type == "general":
            collections_to_search.extend([
                self.ssot_collections["captain_logs"],
                self.ssot_collections["mission_progress"]
            ])
        if context_type == "general":
            collections_to_search.extend([
                self.ssot_collections["agent_status"],
                self.ssot_collections["v2_compliance"]
            ])

        # Perform search across relevant collections
        all_results = []
        for collection_name in collections_to_search:
            try:
                search_query = SearchQuery(
                    query=query,
                    agent_id=agent_id,
                    document_type=None,  # Search all document types
                    limit=limit
                )
                results = self.vector_db.search(collection_name, search_query)
                all_results.extend(results)
            except Exception as e:
                get_logger(__name__).info(f"Warning: Search failed in collection {collection_name}: {e}")

        # Sort by relevance and return top results
        all_results.sort(key=lambda x: x.score, reverse=True)
        return all_results[:limit]

    def get_strategic_insights(self, mission_context: str, agent_capabilities: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate strategic insights for mission coordination.

        Args:
            mission_context: Description of current mission
            agent_capabilities: Available agent capabilities

        Returns:
            Strategic insights and recommendations
        """
        # Search for relevant strategic patterns
        pattern_results = self.search_intelligent_context(
            f"strategic patterns for {mission_context}",
            context_type="strategic",
            limit=3
        )

        # Search for similar mission scenarios
        mission_results = self.search_intelligent_context(
            f"mission coordination for {mission_context}",
            context_type="mission",
            limit=3
        )

        # Analyze agent capabilities against requirements
        capability_analysis = self._analyze_agent_capabilities(agent_capabilities, mission_context)

        return {
            "strategic_patterns": [result.content[:500] + "..." for result in pattern_results],
            "mission_insights": [result.content[:500] + "..." for result in mission_results],
            "capability_analysis": capability_analysis,
            "recommendations": self._generate_recommendations(pattern_results, mission_results, capability_analysis)
        }

    def _analyze_agent_capabilities(self, agent_capabilities: Dict[str, Any], mission_context: str) -> Dict[str, Any]:
        """Analyze agent capabilities against mission requirements."""
        # This would be more sophisticated in a real implementation
        available_agents = len(agent_capabilities)
        mission_complexity = len(mission_context.split()) / 100  # Simple complexity metric

        return {
            "available_agents": available_agents,
            "estimated_complexity": mission_complexity,
            "capability_match": "high" if available_agents >= mission_complexity else "medium"
        }

    def _generate_recommendations(self, patterns: List[SearchResult],
                                 missions: List[SearchResult],
                                 capabilities: Dict[str, Any]) -> List[str]:
        """Generate strategic recommendations based on analysis."""
        recommendations = []

        if capabilities["capability_match"] == "high":
            recommendations.append("High capability match - proceed with standard coordination protocols")
        else:
            recommendations.append("Consider additional agent allocation for optimal mission success")

        if patterns:
            recommendations.append("Leverage proven strategic patterns from historical data")

        if missions:
            recommendations.append("Reference similar mission coordination strategies")

        return recommendations

    def get_emergency_intervention(self, emergency_type: str, current_status: Dict[str, Any]) -> Dict[str, Any]:
        """
        Retrieve emergency intervention patterns based on emergency type and current status.

        Args:
            emergency_type: Type of emergency (e.g., "agent_failure", "mission_blocked")
            current_status: Current system status

        Returns:
            Emergency intervention recommendations and historical success patterns
        """
        # Search for relevant emergency responses
        emergency_results = self.search_intelligent_context(
            f"emergency intervention for {emergency_type}",
            context_type="emergency",
            limit=5
        )

        # Get captain handbook guidance
        handbook_results = self.search_intelligent_context(
            f"emergency protocols for {emergency_type}",
            context_type="strategic",
            limit=2
        )

        return {
            "emergency_type": emergency_type,
            "intervention_patterns": [
                {
                    "pattern": result.content[:300] + "...",
                    "relevance_score": result.score,
                    "source": result.metadata.get("source_file", "unknown")
                }
                for result in emergency_results
            ],
            "captain_guidance": [
                result.content[:500] + "..." for result in handbook_results
            ],
            "recommended_actions": self._extract_emergency_actions(emergency_results),
            "estimated_response_time": self._calculate_response_time(emergency_results)
        }

    def _extract_emergency_actions(self, emergency_results: List[SearchResult]) -> List[str]:
        """Extract actionable emergency response steps."""
        actions = []
        for result in emergency_results:
            metadata = result.metadata
            if "intervention_steps" in metadata:
                actions.extend(metadata["intervention_steps"][:3])  # Limit to top 3 steps

        return list(set(actions))  # Remove duplicates

    def _calculate_response_time(self, emergency_results: List[SearchResult]) -> float:
        """Calculate estimated response time based on historical patterns."""
        if not get_unified_validator().validate_required(emergency_results):
            return 300.0  # Default 5 minutes

        response_times = []
        for result in emergency_results:
            metadata = result.metadata
            if "response_time" in metadata:
                response_times.append(metadata["response_time"])

        return sum(response_times) / len(response_times) if response_times else 300.0

    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive statistics about the vector database SSOT collections."""
        stats = {}
        total_documents = 0
        total_collections = 0

        for collection_key, collection_name in self.ssot_collections.items():
            try:
                collection_stats = self.vector_db.get_collection_stats(collection_name)
                stats[collection_key] = {
                    "documents": collection_stats.get("document_count", 0),
                    "last_updated": collection_stats.get("last_updated"),
                    "collection_name": collection_name
                }
                total_documents += collection_stats.get("document_count", 0)
                total_collections += 1
            except Exception as e:
                stats[collection_key] = {"error": str(e)}

        stats["summary"] = {
            "total_collections": total_collections,
            "total_documents": total_documents,
            "last_indexed": datetime.now().isoformat()
        }

        return stats
