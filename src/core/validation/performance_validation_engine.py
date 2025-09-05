#!/usr/bin/env python3
"""
Performance Validation Engine
=============================

Performance validation engine for the unified validation system.
Handles performance validation for system operations.
V2 COMPLIANT: Focused performance validation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR PERFORMANCE VALIDATION
@license MIT
"""

import logging
from typing import List, Dict, Any, Optional

from .models.validation_models import (
    ValidationResult, ValidationSeverity, ValidationIssue
)


class PerformanceValidationEngine:
    """Performance validation engine for system operations"""
    
    def __init__(self):
        """Initialize performance validation engine"""
        self.logger = logging.getLogger(__name__)
        self.pattern = ValidationPatterns.get_pattern("performance")
    
    def validate_performance(self, performance_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate performance data."""
        issues = []
        
        try:
            # Check required fields
            for field in self.pattern.required_fields:
                if field not in performance_data:
                    issues.append(create_validation_issue(
                        message=f"Required field '{field}' is missing",
                        severity=ValidationSeverity.ERROR,
                        field=field
                    ))
            
            # Validate response time
            if "response_time" in performance_data:
                response_issues = self._validate_response_time(performance_data["response_time"])
                issues.extend(response_issues)
            
            # Validate memory usage
            if "memory_usage" in performance_data:
                memory_issues = self._validate_memory_usage(performance_data["memory_usage"])
                issues.extend(memory_issues)
            
            # Validate operation
            if "operation" in performance_data:
                op_issues = self._validate_operation(performance_data["operation"])
                issues.extend(op_issues)
            
            # Log validation results
            if issues:
                self.logger.warning(f"Performance validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Performance validation passed")
                
        except Exception as e:
            issues.append(create_validation_issue(
                message=f"Performance validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="performance_data",
                value=performance_data
            ))
        
        return issues
    
    def _validate_response_time(self, response_time: float) -> List[ValidationResult]:
        """Validate response time."""
        issues = []
        max_response_time = self.pattern.constraints["max_response_time"]
        
        if not isinstance(response_time, (int, float)):
            issues.append(create_validation_issue(
                message="Response time must be a number",
                severity=ValidationSeverity.ERROR,
                field="response_time",
                value=response_time
            ))
            return issues
        
        if response_time < 0:
            issues.append(create_validation_issue(
                message="Response time cannot be negative",
                severity=ValidationSeverity.ERROR,
                field="response_time",
                value=response_time
            ))
        
        if response_time > max_response_time:
            issues.append(create_validation_issue(
                message=f"Response time {response_time}s exceeds maximum {max_response_time}s",
                severity=ValidationSeverity.WARNING,
                field="response_time",
                value=response_time,
                suggestion="Consider optimizing the operation"
            ))
        
        return issues
    
    def _validate_memory_usage(self, memory_usage: float) -> List[ValidationResult]:
        """Validate memory usage."""
        issues = []
        max_memory = self.pattern.constraints["max_memory_usage"]
        
        if not isinstance(memory_usage, (int, float)):
            issues.append(create_validation_issue(
                message="Memory usage must be a number",
                severity=ValidationSeverity.ERROR,
                field="memory_usage",
                value=memory_usage
            ))
            return issues
        
        if memory_usage < 0:
            issues.append(create_validation_issue(
                message="Memory usage cannot be negative",
                severity=ValidationSeverity.ERROR,
                field="memory_usage",
                value=memory_usage
            ))
        
        if memory_usage > max_memory:
            issues.append(create_validation_issue(
                message=f"Memory usage {memory_usage}MB exceeds maximum {max_memory}MB",
                severity=ValidationSeverity.WARNING,
                field="memory_usage",
                value=memory_usage,
                suggestion="Consider optimizing memory usage"
            ))
        
        return issues
    
    def _validate_operation(self, operation: str) -> List[ValidationResult]:
        """Validate operation type."""
        issues = []
        
        if not operation:
            issues.append(create_validation_issue(
                message="Operation cannot be empty",
                severity=ValidationSeverity.ERROR,
                field="operation"
            ))
            return issues
        
        valid_operations = ["read", "write", "update", "delete", "query", "process"]
        if operation not in valid_operations:
            issues.append(create_validation_issue(
                message=f"Invalid operation: {operation}",
                severity=ValidationSeverity.WARNING,
                field="operation",
                value=operation,
                suggestion=f"Use one of: {', '.join(valid_operations)}"
            ))
        
        return issues
    
    def get_performance_validation_result(self, performance_data: Dict[str, Any]) -> ValidationResult:
        """Get comprehensive validation result for performance data."""
        issues = self.validate_performance(performance_data)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return create_validation_result(
            is_valid=is_valid,
            issues=issues,
            validated_data=performance_data,
            validation_type="performance"
        )


# Factory function for dependency injection
def create_performance_validation_engine() -> PerformanceValidationEngine:
    """Factory function to create performance validation engine"""
    return PerformanceValidationEngine()


# Export for DI
__all__ = ['PerformanceValidationEngine', 'create_performance_validation_engine']
