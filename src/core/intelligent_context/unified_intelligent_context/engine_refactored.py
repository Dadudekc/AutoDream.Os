"""
Intelligent Context Engine Refactored
====================================

Refactored core engine for intelligent context operations.
V2 Compliance: < 300 lines, single responsibility, engine logic.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
from .models import (
    MissionContext, AgentCapability, SearchResult, ContextRetrievalResult,
    EmergencyContext, InterventionProtocol, RiskAssessment, SuccessPrediction,
    ContextMetrics, ContextType, Priority, Status
)
from .engine_base import IntelligentContextEngineBase
from .engine_search import IntelligentContextEngineSearch


class IntelligentContextEngine(IntelligentContextEngineBase):
    """Refactored intelligent context engine."""
    
    def __init__(self):
        """Initialize intelligent context engine."""
        super().__init__()
        
        # Initialize modular components
        self.search = IntelligentContextEngineSearch(self, None)
    
    async def retrieve_context(self, query: str, context_type: ContextType = None) -> ContextRetrievalResult:
        """Retrieve context based on query."""
        return await self.search.retrieve_context(query, context_type)
    
    async def _search_mission_contexts(self, query: str) -> List[SearchResult]:
        """Search mission contexts."""
        return await self.search._search_mission_contexts(query)
    
    async def _search_agent_capabilities(self, query: str) -> List[SearchResult]:
        """Search agent capabilities."""
        return await self.search._search_agent_capabilities(query)
    
    async def _search_emergency_contexts(self, query: str) -> List[SearchResult]:
        """Search emergency contexts."""
        return await self.search._search_emergency_contexts(query)
