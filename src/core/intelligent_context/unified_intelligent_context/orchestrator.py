"""
Intelligent Context Orchestrator
================================

Main orchestrator for intelligent context operations.
V2 Compliance: < 300 lines, single responsibility, orchestration logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from .models import (
    MissionContext, AgentCapability, SearchResult, ContextRetrievalResult,
    EmergencyContext, InterventionProtocol, RiskAssessment, SuccessPrediction,
    ContextMetrics, ContextType, Priority, Status
)
from .engine import IntelligentContextEngine
from .search import IntelligentContextSearch


class IntelligentContextRetrieval:
    """Main orchestrator for intelligent context retrieval operations."""
    
    def __init__(self):
        """Initialize intelligent context orchestrator."""
        self.engine = IntelligentContextEngine()
        self.search = IntelligentContextSearch()
        self.logger = logging.getLogger(__name__)
        self.is_initialized = False
    
    async def initialize(self) -> bool:
        """Initialize the orchestrator."""
        try:
            self.logger.info("Initializing Intelligent Context Orchestrator")
            
            # Initialize search patterns
            self._initialize_search_patterns()
            
            # Load initial contexts
            await self._load_initial_contexts()
            
            self.is_initialized = True
            self.logger.info("Intelligent Context Orchestrator initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize Intelligent Context Orchestrator: {e}")
            return False
    
    def _initialize_search_patterns(self):
        """Initialize search patterns."""
        self.search.add_search_pattern("mission", r"mission|task|objective")
        self.search.add_search_pattern("capability", r"capability|skill|ability")
        self.search.add_search_pattern("emergency", r"emergency|urgent|critical")
        self.search.add_search_pattern("context", r"context|situation|scenario")
    
    async def _load_initial_contexts(self):
        """Load initial contexts."""
        # Load default mission contexts
        default_mission = MissionContext(
            mission_id="default_mission",
            mission_name="Default Mission",
            description="Default mission context",
            priority=Priority.MEDIUM,
            status=Status.ACTIVE,
            agent_id="Agent-3",
            capabilities_required=["infrastructure", "devops"],
            context_data={"type": "default"}
        )
        await self.engine.add_mission_context(default_mission)
        
        # Load default agent capabilities
        default_capability = AgentCapability(
            agent_id="Agent-3",
            capability_name="Infrastructure Management",
            capability_type="infrastructure",
            proficiency_level=0.9,
            success_rate=0.85,
            metadata={"specialization": "devops"}
        )
        await self.engine.add_agent_capability(default_capability)
    
    async def retrieve_context(self, query: str, context_type: ContextType = None) -> ContextRetrievalResult:
        """Retrieve context based on query."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        try:
            # Use search engine for context retrieval
            search_results = self.search.search_contexts(query, context_type)
            
            # Convert search results to context retrieval result
            return ContextRetrievalResult(
                retrieval_id=f"retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                query=query,
                results=search_results,
                execution_time=0.1,  # Mock execution time
                success=True
            )
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve context: {e}")
            return ContextRetrievalResult(
                retrieval_id=f"retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                query=query,
                results=[],
                execution_time=0.0,
                success=False,
                error_message=str(e)
            )
    
    async def add_mission_context(self, context: MissionContext) -> bool:
        """Add mission context."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_mission_context(context)
    
    async def add_agent_capability(self, capability: AgentCapability) -> bool:
        """Add agent capability."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_agent_capability(capability)
    
    async def add_emergency_context(self, emergency: EmergencyContext) -> bool:
        """Add emergency context."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.add_emergency_context(emergency)
    
    async def get_mission_context(self, mission_id: str) -> Optional[MissionContext]:
        """Get mission context by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.get_mission_context(mission_id)
    
    async def get_agent_capabilities(self, agent_id: str) -> List[AgentCapability]:
        """Get agent capabilities by agent ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.get_agent_capabilities(agent_id)
    
    async def get_emergency_context(self, emergency_id: str) -> Optional[EmergencyContext]:
        """Get emergency context by ID."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return await self.engine.get_emergency_context(emergency_id)
    
    def get_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.engine.get_metrics()
    
    def get_search_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.search.get_search_statistics()
    
    def get_search_history(self) -> List[Dict[str, Any]]:
        """Get search history."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        return self.search.get_search_history()
    
    def clear_all_data(self):
        """Clear all data."""
        if not self.is_initialized:
            raise RuntimeError("Orchestrator not initialized")
        
        self.engine.clear_all_contexts()
        self.search.clear_search_history()
        self.logger.info("All data cleared")
    
    def shutdown(self):
        """Shutdown orchestrator."""
        self.logger.info("Shutting down Intelligent Context Orchestrator")
        self.is_initialized = False
