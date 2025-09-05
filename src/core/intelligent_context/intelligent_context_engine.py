#!/usr/bin/env python3
"""
Intelligent Context Engine - V2 Compliance Module
================================================

Core business logic for intelligent context retrieval operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
from typing import Any, Dict, List, Optional, Set
from datetime import datetime

from .intelligent_context_models import (
    MissionContext,
    AgentCapability,
    SearchResult,
    ContextRetrievalResult,
    EmergencyContext,
    InterventionProtocol,
    AgentRecommendation,
    RiskAssessment,
    SuccessPrediction,
    ContextMetrics,
    MissionPhase,
    AgentStatus,
    RiskLevel,
)
from .intelligent_context_search import IntelligentContextSearch
from .intelligent_context_emergency import IntelligentContextEmergency
from .intelligent_context_optimization import IntelligentContextOptimization


class IntelligentContextEngine:
    """Core engine for intelligent context retrieval operations."""

    def __init__(self):
        """Initialize intelligent context engine."""
        self.active_missions: Dict[str, MissionContext] = {}
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.metrics = ContextMetrics()
        
        # Initialize operation modules
        self.search = IntelligentContextSearch(self)
        self.emergency = IntelligentContextEmergency(self)
        self.optimization = IntelligentContextOptimization(self)

    # ================================
    # CORE CONTEXT OPERATIONS
    # ================================
    
    def update_mission_context(self, mission_context: MissionContext) -> bool:
        """Update mission context."""
        try:
            self.active_missions[mission_context.mission_id] = mission_context
            return True
        except Exception:
            return False

    def get_mission_context(self, mission_id: str) -> Optional[MissionContext]:
        """Get mission context by ID."""
        return self.active_missions.get(mission_id)

    def update_agent_capability(self, capability: AgentCapability) -> bool:
        """Update agent capability."""
        try:
            self.agent_capabilities[capability.agent_id] = capability
            return True
        except Exception:
            return False

    def get_agent_capabilities(self) -> Dict[str, AgentCapability]:
        """Get all agent capabilities."""
        return self.agent_capabilities.copy()

    def search_context(self, query: str, mission_id: str = None) -> List[SearchResult]:
        """Search for relevant context."""
        return self.search.search_context(query, mission_id)

    # ================================
    # EMERGENCY OPERATIONS
    # ================================
    
    def get_emergency_context(self, mission: MissionContext) -> EmergencyContext:
        """Get emergency context for mission."""
        return self.emergency.get_emergency_context(mission)

    def get_intervention_protocols(self, mission: MissionContext) -> List[InterventionProtocol]:
        """Get intervention protocols for mission."""
        return self.emergency.get_intervention_protocols(mission)

    # ================================
    # OPTIMIZATION OPERATIONS
    # ================================
    
    def optimize_agent_assignment(self, mission: MissionContext) -> Dict[str, Any]:
        """Optimize agent assignment for mission."""
        return self.optimization.optimize_agent_assignment(mission)

    def analyze_success_patterns(self, mission: MissionContext) -> Dict[str, Any]:
        """Analyze success patterns for mission."""
        return self.optimization.analyze_success_patterns(mission)

    def assess_mission_risks(self, mission: MissionContext) -> RiskAssessment:
        """Assess mission risks."""
        return self.optimization.assess_mission_risks(mission)

    def generate_success_predictions(self, mission: MissionContext) -> SuccessPrediction:
        """Generate success predictions for mission."""
        return self.optimization.generate_success_predictions(mission)

    # ================================
    # METRICS AND MONITORING
    # ================================
    
    def get_metrics(self) -> ContextMetrics:
        """Get context retrieval metrics."""
        return self.metrics

    def _update_metrics(self, operation: str, success: bool, execution_time: float) -> None:
        """Update metrics."""
        self.metrics.total_retrievals += 1
        
        if success:
            self.metrics.successful_retrievals += 1
        else:
            self.metrics.failed_retrievals += 1
        
        self.metrics.total_execution_time_ms += execution_time
        self.metrics.average_execution_time_ms = (
            self.metrics.total_execution_time_ms / self.metrics.total_retrievals
        )
        
        if operation == "emergency":
            self.metrics.emergency_interventions += 1
        elif operation == "optimization":
            self.metrics.agent_optimizations += 1
        elif operation == "risk_assessment":
            self.metrics.risk_assessments += 1
        elif operation == "prediction":
            self.metrics.success_predictions += 1
        
        self.metrics.last_updated = datetime.now()
