"""
Intelligent Context Engine
=========================

Core engine for intelligent context operations.
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


class IntelligentContextEngine:
    """Intelligent context engine."""
    
    def __init__(self):
        """Initialize intelligent context engine."""
        self.contexts: Dict[str, MissionContext] = {}
        self.capabilities: Dict[str, AgentCapability] = {}
        self.emergencies: Dict[str, EmergencyContext] = {}
        self.protocols: Dict[str, InterventionProtocol] = {}
        self.assessments: Dict[str, RiskAssessment] = {}
        self.predictions: Dict[str, SuccessPrediction] = {}
        self.metrics = ContextMetrics()
    
    async def retrieve_context(self, query: str, context_type: ContextType = None) -> ContextRetrievalResult:
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
                success=True
            )
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            return ContextRetrievalResult(
                retrieval_id=f"retrieval_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                query=query,
                results=[],
                execution_time=execution_time,
                success=False,
                error_message=str(e)
            )
    
    async def _search_mission_contexts(self, query: str) -> List[SearchResult]:
        """Search mission contexts."""
        results = []
        query_lower = query.lower()
        
        for context in self.contexts.values():
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
            
            if relevance_score > 0.0:
                results.append(SearchResult(
                    result_id=f"mission_{context.mission_id}",
                    context_type=ContextType.MISSION,
                    relevance_score=relevance_score,
                    content={
                        "mission_id": context.mission_id,
                        "mission_name": context.mission_name,
                        "description": context.description,
                        "priority": context.priority.value,
                        "status": context.status.value,
                        "agent_id": context.agent_id,
                        "capabilities_required": context.capabilities_required
                    },
                    metadata={"context_data": context.context_data}
                ))
        
        return results
    
    async def _search_agent_capabilities(self, query: str) -> List[SearchResult]:
        """Search agent capabilities."""
        results = []
        query_lower = query.lower()
        
        for capability in self.capabilities.values():
            relevance_score = 0.0
            
            # Check capability name
            if query_lower in capability.capability_name.lower():
                relevance_score += 0.9
            
            # Check capability type
            if query_lower in capability.capability_type.lower():
                relevance_score += 0.7
            
            # Check metadata
            for key, value in capability.metadata.items():
                if query_lower in str(value).lower():
                    relevance_score += 0.3
            
            if relevance_score > 0.0:
                results.append(SearchResult(
                    result_id=f"capability_{capability.agent_id}_{capability.capability_name}",
                    context_type=ContextType.AGENT_CAPABILITY,
                    relevance_score=relevance_score,
                    content={
                        "agent_id": capability.agent_id,
                        "capability_name": capability.capability_name,
                        "capability_type": capability.capability_type,
                        "proficiency_level": capability.proficiency_level,
                        "success_rate": capability.success_rate
                    },
                    metadata=capability.metadata
                ))
        
        return results
    
    async def _search_emergency_contexts(self, query: str) -> List[SearchResult]:
        """Search emergency contexts."""
        results = []
        query_lower = query.lower()
        
        for emergency in self.emergencies.values():
            relevance_score = 0.0
            
            # Check emergency type
            if query_lower in emergency.emergency_type.lower():
                relevance_score += 0.8
            
            # Check description
            if query_lower in emergency.description.lower():
                relevance_score += 0.6
            
            # Check affected agents
            for agent in emergency.affected_agents:
                if query_lower in agent.lower():
                    relevance_score += 0.4
            
            if relevance_score > 0.0:
                results.append(SearchResult(
                    result_id=f"emergency_{emergency.emergency_id}",
                    context_type=ContextType.EMERGENCY,
                    relevance_score=relevance_score,
                    content={
                        "emergency_id": emergency.emergency_id,
                        "emergency_type": emergency.emergency_type,
                        "severity": emergency.severity.value,
                        "description": emergency.description,
                        "affected_agents": emergency.affected_agents,
                        "required_actions": emergency.required_actions
                    },
                    metadata={"context_data": emergency.context_data}
                ))
        
        return results
    
    async def add_mission_context(self, context: MissionContext) -> bool:
        """Add mission context."""
        try:
            self.contexts[context.mission_id] = context
            self._update_metrics()
            return True
        except Exception:
            return False
    
    async def add_agent_capability(self, capability: AgentCapability) -> bool:
        """Add agent capability."""
        try:
            key = f"{capability.agent_id}_{capability.capability_name}"
            self.capabilities[key] = capability
            self._update_metrics()
            return True
        except Exception:
            return False
    
    async def add_emergency_context(self, emergency: EmergencyContext) -> bool:
        """Add emergency context."""
        try:
            self.emergencies[emergency.emergency_id] = emergency
            self._update_metrics()
            return True
        except Exception:
            return False
    
    async def get_mission_context(self, mission_id: str) -> Optional[MissionContext]:
        """Get mission context by ID."""
        return self.contexts.get(mission_id)
    
    async def get_agent_capabilities(self, agent_id: str) -> List[AgentCapability]:
        """Get agent capabilities by agent ID."""
        return [cap for cap in self.capabilities.values() if cap.agent_id == agent_id]
    
    async def get_emergency_context(self, emergency_id: str) -> Optional[EmergencyContext]:
        """Get emergency context by ID."""
        return self.emergencies.get(emergency_id)
    
    def get_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        self._update_metrics()
        return self.metrics
    
    def _update_metrics(self):
        """Update context metrics."""
        self.metrics.total_contexts = len(self.contexts)
        self.metrics.active_contexts = sum(1 for c in self.contexts.values() if c.status == Status.ACTIVE)
        self.metrics.last_updated = datetime.now()
    
    def clear_all_contexts(self):
        """Clear all contexts."""
        self.contexts.clear()
        self.capabilities.clear()
        self.emergencies.clear()
        self.protocols.clear()
        self.assessments.clear()
        self.predictions.clear()
        self._update_metrics()
