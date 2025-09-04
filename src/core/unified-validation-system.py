#!/usr/bin/env python3
"""
Unified Validation System - V2 Compliant
========================================

This module provides a unified validation system that consolidates all validation
patterns across the codebase, eliminating DRY violations.

Author: Agent-7 - Web Development Specialist (DRY Consolidation)
Created: 2025-01-27
Purpose: Consolidate all validation patterns into unified system
"""

import re
from typing import Any, Dict, List, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from .unified-logging-utility import UnifiedLoggingUtility
from .unified-configuration-utility import UnifiedConfigurationUtility
from .unified-error-handling-utility import UnifiedErrorHandlingUtility


class ValidationSeverity(Enum):
    """Validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class ValidationIssue:
    """Represents a validation issue."""
    message: str
    severity: ValidationSeverity
    field: Optional[str] = None
    value: Any = None
    suggestion: Optional[str] = None


class UnifiedValidationSystem:
    """
    Unified validation system that consolidates all validation patterns.
    
    CONSOLIDATES:
    - Coordination validation
    - Coordinate validation
    - Message validation
    - CLI validation
    - Security validation
    - Performance validation
    """
    
    def __init__(self):
        """Initialize unified validation system."""
        self.logger = UnifiedLoggingUtility.get_logger(__name__)
        self.config = UnifiedConfigurationUtility.load_config()
        
        # Validation patterns
        self.validation_patterns = {
            "coordinate": {
                "x_range": (0, 1920),
                "y_range": (0, 1080),
                "required_fields": ["x", "y"]
            },
            "message": {
                "max_length": 1000,
                "required_fields": ["content", "recipient"],
                "allowed_types": ["text", "broadcast", "onboarding", "agent_to_agent", "system_to_agent", "human_to_agent"]
            },
            "coordination": {
                "max_agents": 8,
                "required_fields": ["agent_id", "status"],
                "allowed_statuses": ["ACTIVE", "INACTIVE", "PENDING", "ERROR"]
            },
            "security": {
                "max_attempts": 3,
                "timeout_seconds": 30,
                "required_fields": ["user_id", "permissions"]
            },
            "performance": {
                "max_response_time": 5.0,
                "max_memory_usage": 100,
                "required_fields": ["operation", "start_time"]
            }
        }

    def validate_coordinates(self, coords: Tuple[int, int], recipient: str = None) -> List[ValidationIssue]:
        """
        Validate coordinates for PyAutoGUI operations.
        
        Args:
            coords: Tuple of (x, y) coordinates
            recipient: Optional recipient for context
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            x, y = coords
            
            # Validate x coordinate
            if not isinstance(x, int):
                issues.append(ValidationIssue(
                    message="X coordinate must be an integer",
                    severity=ValidationSeverity.ERROR,
                    field="x",
                    value=x
                ))
            elif not (self.validation_patterns["coordinate"]["x_range"][0] <= x <= self.validation_patterns["coordinate"]["x_range"][1]):
                issues.append(ValidationIssue(
                    message=f"X coordinate {x} is out of range {self.validation_patterns['coordinate']['x_range']}",
                    severity=ValidationSeverity.ERROR,
                    field="x",
                    value=x
                ))
            
            # Validate y coordinate
            if not isinstance(y, int):
                issues.append(ValidationIssue(
                    message="Y coordinate must be an integer",
                    severity=ValidationSeverity.ERROR,
                    field="y",
                    value=y
                ))
            elif not (self.validation_patterns["coordinate"]["y_range"][0] <= y <= self.validation_patterns["coordinate"]["y_range"][1]):
                issues.append(ValidationIssue(
                    message=f"Y coordinate {y} is out of range {self.validation_patterns['coordinate']['y_range']}",
                    severity=ValidationSeverity.ERROR,
                    field="y",
                    value=y
                ))
            
            # Log validation
            if issues:
                self.logger.warning(f"Coordinate validation failed for {coords}: {len(issues)} issues")
            else:
                self.logger.debug(f"Coordinate validation passed for {coords}")
                
        except Exception as e:
            issues.append(ValidationIssue(
                message=f"Coordinate validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="coords",
                value=coords
            ))
        
        return issues

    def validate_message(self, message_data: Dict[str, Any]) -> List[ValidationIssue]:
        """
        Validate message data.
        
        Args:
            message_data: Message data dictionary
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Check required fields
            for field in self.validation_patterns["message"]["required_fields"]:
                if field not in message_data:
                    issues.append(ValidationIssue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate content length
            if "content" in message_data:
                content = message_data["content"]
                if len(content) > self.validation_patterns["message"]["max_length"]:
                    issues.append(ValidationIssue(
                        message=f"Content length {len(content)} exceeds maximum {self.validation_patterns['message']['max_length']}",
                        severity=ValidationSeverity.ERROR,
                        field="content",
                        value=content[:50] + "..." if len(content) > 50 else content
                    ))
            
            # Validate message type
            if "type" in message_data:
                msg_type = message_data["type"]
                if msg_type not in self.validation_patterns["message"]["allowed_types"]:
                    issues.append(ValidationIssue(
                        message=f"Invalid message type '{msg_type}'. Allowed: {self.validation_patterns['message']['allowed_types']}",
                        severity=ValidationSeverity.ERROR,
                        field="type",
                        value=msg_type
                    ))
            
            # Log validation
            if issues:
                self.logger.warning(f"Message validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Message validation passed")
                
        except Exception as e:
            issues.append(ValidationIssue(
                message=f"Message validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="message_data",
                value=message_data
            ))
        
        return issues

    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationIssue]:
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
            for field in self.validation_patterns["coordination"]["required_fields"]:
                if field not in system_data:
                    issues.append(ValidationIssue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate agent count
            if "agents" in system_data:
                agent_count = len(system_data["agents"])
                if agent_count > self.validation_patterns["coordination"]["max_agents"]:
                    issues.append(ValidationIssue(
                        message=f"Agent count {agent_count} exceeds maximum {self.validation_patterns['coordination']['max_agents']}",
                        severity=ValidationSeverity.WARNING,
                        field="agents",
                        value=agent_count
                    ))
            
            # Validate agent statuses
            if "agents" in system_data:
                for agent_id, agent_data in system_data["agents"].items():
                    if "status" in agent_data:
                        status = agent_data["status"]
                        if status not in self.validation_patterns["coordination"]["allowed_statuses"]:
                            issues.append(ValidationIssue(
                                message=f"Invalid status '{status}' for agent {agent_id}",
                                severity=ValidationSeverity.ERROR,
                                field=f"agents.{agent_id}.status",
                                value=status
                            ))
            
            # Log validation
            if issues:
                self.logger.warning(f"Coordination validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Coordination validation passed")
                
        except Exception as e:
            issues.append(ValidationIssue(
                message=f"Coordination validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="system_data",
                value=system_data
            ))
        
        return issues

    def validate_security(self, security_data: Dict[str, Any]) -> List[ValidationIssue]:
        """
        Validate security data.
        
        Args:
            security_data: Security data dictionary
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Check required fields
            for field in self.validation_patterns["security"]["required_fields"]:
                if field not in security_data:
                    issues.append(ValidationIssue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate attempts
            if "attempts" in security_data:
                attempts = security_data["attempts"]
                if attempts > self.validation_patterns["security"]["max_attempts"]:
                    issues.append(ValidationIssue(
                        message=f"Attempt count {attempts} exceeds maximum {self.validation_patterns['security']['max_attempts']}",
                        severity=ValidationSeverity.ERROR,
                        field="attempts",
                        value=attempts
                    ))
            
            # Validate timeout
            if "timeout" in security_data:
                timeout = security_data["timeout"]
                if timeout > self.validation_patterns["security"]["timeout_seconds"]:
                    issues.append(ValidationIssue(
                        message=f"Timeout {timeout}s exceeds maximum {self.validation_patterns['security']['timeout_seconds']}s",
                        severity=ValidationSeverity.WARNING,
                        field="timeout",
                        value=timeout
                    ))
            
            # Log validation
            if issues:
                self.logger.warning(f"Security validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Security validation passed")
                
        except Exception as e:
            issues.append(ValidationIssue(
                message=f"Security validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="security_data",
                value=security_data
            ))
        
        return issues

    def validate_performance(self, performance_data: Dict[str, Any]) -> List[ValidationIssue]:
        """
        Validate performance data.
        
        Args:
            performance_data: Performance data dictionary
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            # Check required fields
            for field in self.validation_patterns["performance"]["required_fields"]:
                if field not in performance_data:
                    issues.append(ValidationIssue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate response time
            if "response_time" in performance_data:
                response_time = performance_data["response_time"]
                if response_time > self.validation_patterns["performance"]["max_response_time"]:
                    issues.append(ValidationIssue(
                        message=f"Response time {response_time}s exceeds maximum {self.validation_patterns['performance']['max_response_time']}s",
                        severity=ValidationSeverity.WARNING,
                        field="response_time",
                        value=response_time
                    ))
            
            # Validate memory usage
            if "memory_usage" in performance_data:
                memory_usage = performance_data["memory_usage"]
                if memory_usage > self.validation_patterns["performance"]["max_memory_usage"]:
                    issues.append(ValidationIssue(
                        message=f"Memory usage {memory_usage}MB exceeds maximum {self.validation_patterns['performance']['max_memory_usage']}MB",
                        severity=ValidationSeverity.WARNING,
                        field="memory_usage",
                        value=memory_usage
                    ))
            
            # Log validation
            if issues:
                self.logger.warning(f"Performance validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Performance validation passed")
                
        except Exception as e:
            issues.append(ValidationIssue(
                message=f"Performance validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="performance_data",
                value=performance_data
            ))
        
        return issues

    def validate_all(self, data: Dict[str, Any], validation_type: str) -> List[ValidationIssue]:
        """
        Validate data based on type.
        
        Args:
            data: Data to validate
            validation_type: Type of validation to perform
            
        Returns:
            List of validation issues
        """
        if validation_type == "coordinate":
            return self.validate_coordinates(data.get("coords"), data.get("recipient"))
        elif validation_type == "message":
            return self.validate_message(data)
        elif validation_type == "coordination":
            return self.validate_coordination_system(data)
        elif validation_type == "security":
            return self.validate_security(data)
        elif validation_type == "performance":
            return self.validate_performance(data)
        else:
            return [ValidationIssue(
                message=f"Unknown validation type: {validation_type}",
                severity=ValidationSeverity.ERROR,
                field="validation_type",
                value=validation_type
            )]

    def get_validation_summary(self, issues: List[ValidationIssue]) -> Dict[str, Any]:
        """
        Get validation summary.
        
        Args:
            issues: List of validation issues
            
        Returns:
            Validation summary dictionary
        """
        summary = {
            "total_issues": len(issues),
            "by_severity": {},
            "by_field": {},
            "has_errors": False,
            "has_warnings": False
        }
        
        for issue in issues:
            # Count by severity
            severity = issue.severity.value
            if severity not in summary["by_severity"]:
                summary["by_severity"][severity] = 0
            summary["by_severity"][severity] += 1
            
            # Count by field
            if issue.field:
                if issue.field not in summary["by_field"]:
                    summary["by_field"][issue.field] = 0
                summary["by_field"][issue.field] += 1
            
            # Check for errors and warnings
            if issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]:
                summary["has_errors"] = True
            elif issue.severity == ValidationSeverity.WARNING:
                summary["has_warnings"] = True
        
        return summary


# Convenience functions for backward compatibility
def validate_coordinates(coords: Tuple[int, int], recipient: str = None) -> List[ValidationIssue]:
    """Validate coordinates for PyAutoGUI operations."""
    validator = UnifiedValidationSystem()
    return validator.validate_coordinates(coords, recipient)

def validate_message(message_data: Dict[str, Any]) -> List[ValidationIssue]:
    """Validate message data."""
    validator = UnifiedValidationSystem()
    return validator.validate_message(message_data)

def validate_coordination_system(system_data: Dict[str, Any]) -> List[ValidationIssue]:
    """Validate coordination system data."""
    validator = UnifiedValidationSystem()
    return validator.validate_coordination_system(system_data)
