#!/usr/bin/env python3
"""
Coordination Validation Engine
==============================

Coordination validation engine for the unified validation system.
Handles coordination system validation.
V2 COMPLIANT: Focused coordination validation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR COORDINATION VALIDATION
@license MIT
"""

import logging
from typing import List, Dict, Any, Optional

from .models.validation_models import (
    ValidationSeverity, ValidationResult, ValidationType
)


class CoordinationValidationEngine:
    """Coordination validation engine for system coordination"""
    
    def __init__(self):
        """Initialize coordination validation engine"""
        self.logger = logging.getLogger(__name__)
        self.pattern = ValidationPatterns.get_pattern("coordination")
    
    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationResult]:
        """
        Validate coordination system data.
        
        Args:
            system_data: Coordination system data
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Check required fields
            for field in self.pattern.required_fields:
                if field not in system_data:
                    issues.append(create_validation_issue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate agent count
            if "agents" in system_data:
                agent_count_issues = self._validate_agent_count(system_data["agents"])
                issues.extend(agent_count_issues)
            
            # Validate agent statuses
            if "agents" in system_data:
                status_issues = self._validate_agent_statuses(system_data["agents"])
                issues.extend(status_issues)
            
            # Validate agent IDs
            if "agents" in system_data:
                id_issues = self._validate_agent_ids(system_data["agents"])
                issues.extend(id_issues)
            
            # Validate coordination state
            if "state" in system_data:
                state_issues = self._validate_coordination_state(system_data["state"])
                issues.extend(state_issues)
            
            # Log validation results
            if issues:
                self.logger.warning(f"Coordination validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Coordination validation passed")
                
        except Exception as e:
            issues.append(create_validation_issue(
                message=f"Coordination validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="system_data",
                value=system_data
            ))
        
        return issues
    
    def _validate_agent_count(self, agents: Dict[str, Any]) -> List[ValidationResult]:
        """Validate agent count."""
        issues = []
        
        if not isinstance(agents, dict):
            issues.append(create_validation_issue(
                message="Agents must be a dictionary",
                severity=ValidationSeverity.ERROR,
                field="agents",
                value=agents
            ))
            return issues
        
        agent_count = len(agents)
        max_agents = self.pattern.constraints["max_agents"]
        
        if agent_count > max_agents:
            issues.append(create_validation_issue(
                message=f"Agent count {agent_count} exceeds maximum {max_agents}",
                severity=ValidationSeverity.WARNING,
                field="agents",
                value=agent_count,
                suggestion=f"Consider reducing to {max_agents} or fewer agents"
            ))
        
        if agent_count == 0:
            issues.append(create_validation_issue(
                message="No agents found in coordination system",
                severity=ValidationSeverity.WARNING,
                field="agents",
                suggestion="Add at least one agent to the coordination system"
            ))
        
        return issues
    
    def _validate_agent_statuses(self, agents: Dict[str, Any]) -> List[ValidationResult]:
        """Validate agent statuses."""
        issues = []
        allowed_statuses = self.pattern.allowed_values["status"]
        
        for agent_id, agent_data in agents.items():
            if not isinstance(agent_data, dict):
                issues.append(create_validation_issue(
                    message=f"Agent data for {agent_id} must be a dictionary",
                    severity=ValidationSeverity.ERROR,
                    field=f"agents.{agent_id}",
                    value=agent_data
                ))
                continue
            
            if "status" in agent_data:
                status = agent_data["status"]
                if status not in allowed_statuses:
                    issues.append(create_validation_issue(
                        message=f"Invalid status '{status}' for agent {agent_id}",
                        severity=ValidationSeverity.ERROR,
                        field=f"agents.{agent_id}.status",
                        value=status,
                        suggestion=f"Use one of: {', '.join(allowed_statuses)}"
                    ))
            else:
                issues.append(create_validation_issue(
                    message=f"Status missing for agent {agent_id}",
                    severity=ValidationSeverity.WARNING,
                    field=f"agents.{agent_id}.status",
                    suggestion="Add status field to agent data"
                ))
        
        return issues
    
    def _validate_agent_ids(self, agents: Dict[str, Any]) -> List[ValidationResult]:
        """Validate agent IDs."""
        issues = []
        
        for agent_id in agents.keys():
            if not self._is_valid_agent_id(agent_id):
                issues.append(create_validation_issue(
                    message=f"Invalid agent ID format: {agent_id}",
                    severity=ValidationSeverity.WARNING,
                    field="agent_id",
                    value=agent_id,
                    suggestion="Use format like 'Agent-1', 'Agent-2', etc."
                ))
        
        return issues
    
    def _validate_coordination_state(self, state: str) -> List[ValidationResult]:
        """Validate coordination state."""
        issues = []
        
        if not state:
            issues.append(create_validation_issue(
                message="Coordination state cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="state"
            ))
            return issues
        
        valid_states = ["ACTIVE", "INACTIVE", "MAINTENANCE", "ERROR", "INITIALIZING"]
        if state not in valid_states:
            issues.append(create_validation_issue(
                message=f"Invalid coordination state: {state}",
                severity=ValidationSeverity.WARNING,
                field="state",
                value=state,
                suggestion=f"Use one of: {', '.join(valid_states)}"
            ))
        
        return issues
    
    def _is_valid_agent_id(self, agent_id: str) -> bool:
        """Check if agent ID format is valid."""
        import re
        return bool(re.match(r'^Agent-\d+$', agent_id))
    
    def validate_agent_data(self, agent_id: str, agent_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate individual agent data."""
        issues = []
        
        # Validate agent ID
        if not self._is_valid_agent_id(agent_id):
            issues.append(create_validation_issue(
                message=f"Invalid agent ID format: {agent_id}",
                severity=ValidationSeverity.ERROR,
                field="agent_id",
                value=agent_id
            ))
        
        # Validate required fields
        required_fields = ["status"]
        for field in required_fields:
            if field not in agent_data:
                issues.append(create_validation_issue(
                    message=f"Required field '{field}' is missing for agent {agent_id}",
                    severity=ValidationSeverity.ERROR,
                    field=f"agent_id.{field}"
                ))
        
        # Validate status
        if "status" in agent_data:
            status = agent_data["status"]
            allowed_statuses = self.pattern.allowed_values["status"]
            if status not in allowed_statuses:
                issues.append(create_validation_issue(
                    message=f"Invalid status '{status}' for agent {agent_id}",
                    severity=ValidationSeverity.ERROR,
                    field=f"agent_id.status",
                    value=status,
                    suggestion=f"Use one of: {', '.join(allowed_statuses)}"
                ))
        
        return issues
    
    def get_coordination_validation_result(self, system_data: Dict[str, Any]) -> ValidationResult:
        """Get comprehensive validation result for coordination system."""
        issues = self.validate_coordination_system(system_data)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return create_validation_result(
            is_valid=is_valid,
            issues=issues,
            validated_data=system_data,
            validation_type="coordination"
        )


# Factory function for dependency injection
def create_coordination_validation_engine() -> CoordinationValidationEngine:
    """Factory function to create coordination validation engine"""
    return CoordinationValidationEngine()


# Export for DI
__all__ = ['CoordinationValidationEngine', 'create_coordination_validation_engine']
