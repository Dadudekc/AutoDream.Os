#!/usr/bin/env python3
"""
Emergency Intervention Engine Core - V2 Compliance Module
========================================================

Core business logic for emergency intervention operations.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import time
import uuid
from typing import Any, Dict, List, Optional
from datetime import datetime

from .emergency_intervention_models import (
    Emergency,
    EmergencySeverity,
    EmergencyType,
    EmergencyStatus,
    InterventionProtocol,
    InterventionResult,
    EmergencyPattern,
    EmergencyMetrics,
    InterventionAction,
    EmergencyContext,
    EmergencyResponse,
    EmergencyHistory,
)


class EmergencyInterventionEngineCore:
    """Core engine for emergency intervention operations."""

    def __init__(self):
        """Initialize emergency intervention engine."""
        self.active_emergencies: Dict[str, Emergency] = {}
        self.emergency_history: List[Emergency] = []
        self.intervention_protocols: Dict[str, InterventionProtocol] = {}
        self.intervention_results: List[InterventionResult] = []
        self.emergency_patterns: Dict[EmergencyType, EmergencyPattern] = {}
        self.emergency_metrics = EmergencyMetrics()

    def report_emergency(self, emergency_type: EmergencyType, severity: EmergencySeverity,
                        description: str, affected_agents: List[str] = None,
                        context: EmergencyContext = None) -> Emergency:
        """Report a new emergency."""
        emergency_id = str(uuid.uuid4())
        emergency = Emergency(
            emergency_id=emergency_id,
            emergency_type=emergency_type,
            severity=severity,
            description=description,
            affected_agents=affected_agents or [],
            context=context or EmergencyContext(),
            status=EmergencyStatus.REPORTED,
            reported_at=datetime.now(),
            created_at=datetime.now()
        )
        
        self.active_emergencies[emergency_id] = emergency
        self.emergency_history.append(emergency)
        self.emergency_metrics.total_emergencies += 1
        
        return emergency

    def assess_emergency(self, emergency_id: str) -> EmergencyResponse:
        """Assess emergency severity and determine response."""
        if emergency_id not in self.active_emergencies:
            return EmergencyResponse(
                emergency_id=emergency_id,
                response_type="error",
                message="Emergency not found",
                success=False
            )
        
        emergency = self.active_emergencies[emergency_id]
        
        # Assess severity based on type and context
        assessed_severity = self._assess_severity(emergency)
        emergency.severity = assessed_severity
        
        # Determine intervention protocol
        protocol = self._get_intervention_protocol(emergency.emergency_type, assessed_severity)
        
        response = EmergencyResponse(
            emergency_id=emergency_id,
            response_type="assessment",
            message=f"Emergency assessed as {assessed_severity.value}",
            success=True,
            recommended_actions=protocol.actions if protocol else []
        )
        
        return response

    def execute_intervention(self, emergency_id: str, action: InterventionAction) -> InterventionResult:
        """Execute intervention action."""
        if emergency_id not in self.active_emergencies:
            return InterventionResult(
                intervention_id=str(uuid.uuid4()),
                emergency_id=emergency_id,
                action=action,
                success=False,
                message="Emergency not found",
                executed_at=datetime.now()
            )
        
        emergency = self.active_emergencies[emergency_id]
        intervention_id = str(uuid.uuid4())
        
        try:
            # Execute intervention based on action type
            result = self._execute_action(emergency, action)
            
            intervention_result = InterventionResult(
                intervention_id=intervention_id,
                emergency_id=emergency_id,
                action=action,
                success=result["success"],
                message=result["message"],
                executed_at=datetime.now(),
                duration=result.get("duration", 0.0)
            )
            
            self.intervention_results.append(intervention_result)
            self.emergency_metrics.total_interventions += 1
            
            if result["success"]:
                self.emergency_metrics.successful_interventions += 1
            else:
                self.emergency_metrics.failed_interventions += 1
            
            return intervention_result
            
        except Exception as e:
            intervention_result = InterventionResult(
                intervention_id=intervention_id,
                emergency_id=emergency_id,
                action=action,
                success=False,
                message=f"Intervention failed: {str(e)}",
                executed_at=datetime.now()
            )
            
            self.intervention_results.append(intervention_result)
            self.emergency_metrics.failed_interventions += 1
            
            return intervention_result

    def resolve_emergency(self, emergency_id: str, resolution_notes: str = "") -> EmergencyResponse:
        """Resolve emergency."""
        if emergency_id not in self.active_emergencies:
            return EmergencyResponse(
                emergency_id=emergency_id,
                response_type="error",
                message="Emergency not found",
                success=False
            )
        
        emergency = self.active_emergencies[emergency_id]
        emergency.status = EmergencyStatus.RESOLVED
        emergency.resolved_at = datetime.now()
        emergency.resolution_notes = resolution_notes
        
        # Move to history
        self.emergency_history.append(emergency)
        del self.active_emergencies[emergency_id]
        
        self.emergency_metrics.resolved_emergencies += 1
        
        return EmergencyResponse(
            emergency_id=emergency_id,
            response_type="resolution",
            message="Emergency resolved successfully",
            success=True
        )

    def get_emergency_status(self, emergency_id: str) -> Optional[Emergency]:
        """Get emergency status."""
        return self.active_emergencies.get(emergency_id)

    def get_active_emergencies(self) -> List[Emergency]:
        """Get all active emergencies."""
        return list(self.active_emergencies.values())

    def get_emergency_metrics(self) -> EmergencyMetrics:
        """Get emergency metrics."""
        return self.emergency_metrics

    # ================================
    # PRIVATE HELPER METHODS
    # ================================
    
    def _assess_severity(self, emergency: Emergency) -> EmergencySeverity:
        """Assess emergency severity."""
        # Simple severity assessment based on type and context
        if emergency.emergency_type == EmergencyType.SYSTEM_FAILURE:
            return EmergencySeverity.CRITICAL
        elif emergency.emergency_type == EmergencyType.AGENT_FAILURE:
            return EmergencySeverity.HIGH
        elif emergency.emergency_type == EmergencyType.PERFORMANCE_DEGRADATION:
            return EmergencySeverity.MEDIUM
        else:
            return EmergencySeverity.LOW

    def _get_intervention_protocol(self, emergency_type: EmergencyType, severity: EmergencySeverity) -> Optional[InterventionProtocol]:
        """Get intervention protocol for emergency type and severity."""
        protocol_key = f"{emergency_type.value}_{severity.value}"
        return self.intervention_protocols.get(protocol_key)

    def _execute_action(self, emergency: Emergency, action: InterventionAction) -> Dict[str, Any]:
        """Execute intervention action."""
        start_time = time.time()
        
        try:
            # Simulate action execution
            time.sleep(0.1)  # Simulate processing time
            
            duration = time.time() - start_time
            
            return {
                "success": True,
                "message": f"Action {action.action_type} executed successfully",
                "duration": duration
            }
            
        except Exception as e:
            duration = time.time() - start_time
            return {
                "success": False,
                "message": f"Action execution failed: {str(e)}",
                "duration": duration
            }
