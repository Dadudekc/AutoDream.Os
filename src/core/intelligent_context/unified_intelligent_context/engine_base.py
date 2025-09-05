"""
Intelligent Context Engine Base
==============================

Base functionality for intelligent context operations.
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


class IntelligentContextEngineBase:
    """Base intelligent context engine."""
    
    def __init__(self):
        """Initialize intelligent context engine."""
        self.contexts: Dict[str, MissionContext] = {}
        self.capabilities: Dict[str, AgentCapability] = {}
        self.emergencies: Dict[str, EmergencyContext] = {}
        self.protocols: Dict[str, InterventionProtocol] = {}
        self.assessments: Dict[str, RiskAssessment] = {}
        self.predictions: Dict[str, SuccessPrediction] = {}
        self.metrics = ContextMetrics()
    
    def get_metrics(self) -> ContextMetrics:
        """Get context metrics."""
        return self.metrics
    
    def _update_metrics(self):
        """Update context metrics."""
        self.metrics.total_contexts = len(self.contexts)
        self.metrics.total_capabilities = len(self.capabilities)
        self.metrics.total_emergencies = len(self.emergencies)
        self.metrics.total_protocols = len(self.protocols)
        self.metrics.total_assessments = len(self.assessments)
        self.metrics.total_predictions = len(self.predictions)
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
    
    def add_mission_context(self, context: MissionContext):
        """Add mission context."""
        self.contexts[context.context_id] = context
        self._update_metrics()
    
    def add_agent_capability(self, capability: AgentCapability):
        """Add agent capability."""
        self.capabilities[capability.capability_id] = capability
        self._update_metrics()
    
    def add_emergency_context(self, emergency: EmergencyContext):
        """Add emergency context."""
        self.emergencies[emergency.emergency_id] = emergency
        self._update_metrics()
    
    def add_intervention_protocol(self, protocol: InterventionProtocol):
        """Add intervention protocol."""
        self.protocols[protocol.protocol_id] = protocol
        self._update_metrics()
    
    def add_risk_assessment(self, assessment: RiskAssessment):
        """Add risk assessment."""
        self.assessments[assessment.assessment_id] = assessment
        self._update_metrics()
    
    def add_success_prediction(self, prediction: SuccessPrediction):
        """Add success prediction."""
        self.predictions[prediction.prediction_id] = prediction
        self._update_metrics()
