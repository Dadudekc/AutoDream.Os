#!/usr/bin/env python3
"""
Unified Validation Orchestrator
===============================

Main orchestrator for the unified validation system.
Coordinates all validation engines and provides unified interface.
V2 COMPLIANT: Focused orchestration under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR ORCHESTRATOR
@license MIT
"""

import logging
from typing import Dict, List, Any, Optional, Tuple

from .models.validation_models import ValidationSeverity, ValidationResult, ValidationType
from .coordinate_validation_engine import CoordinateValidationEngine, create_coordinate_validation_engine
from .message_validation_engine import MessageValidationEngine, create_message_validation_engine
from .coordination_validation_engine import CoordinationValidationEngine, create_coordination_validation_engine
from .security_validation_engine import SecurityValidationEngine, create_security_validation_engine
from .performance_validation_engine import PerformanceValidationEngine, create_performance_validation_engine


class UnifiedValidationOrchestrator:
    """Main orchestrator for the unified validation system"""
    
    def __init__(self):
        """Initialize unified validation orchestrator"""
        self.logger = logging.getLogger(__name__)
        
        # Initialize all validation engines
        self.coordinate_engine = create_coordinate_validation_engine()
        self.message_engine = create_message_validation_engine()
        self.coordination_engine = create_coordination_validation_engine()
        self.security_engine = create_security_validation_engine()
        self.performance_engine = create_performance_validation_engine()
        
        self.logger.info("Unified Validation Orchestrator initialized")
    
    def validate(self, data: Any, validation_type: str) -> List[ValidationResult]:
        """
        Validate data using the appropriate validation engine.
        
        Args:
            data: Data to validate
            validation_type: Type of validation to perform
            
        Returns:
            List of validation issues
        """
        if validation_type == "coordinate":
            return self.coordinate_engine.validate_coordinates(data.get("coords"), data.get("recipient"))
        elif validation_type == "message":
            return self.message_engine.validate_message(data)
        elif validation_type == "coordination":
            return self.coordination_engine.validate_coordination_system(data)
        elif validation_type == "security":
            return self.security_engine.validate_security(data)
        elif validation_type == "performance":
            return self.performance_engine.validate_performance(data)
        else:
            return [ValidationResult(
                message=f"Unknown validation type: {validation_type}",
                severity=ValidationSeverity.ERROR,
                field="validation_type",
                value=validation_type
            )]
    
    def validate_coordinates(self, coords: Tuple[int, int], recipient: str = None) -> List[ValidationResult]:
        """Validate coordinates for PyAutoGUI operations."""
        return self.coordinate_engine.validate_coordinates(coords, recipient)
    
    def validate_message(self, message_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate message data."""
        return self.message_engine.validate_message(message_data)
    
    def validate_coordination_system(self, system_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate coordination system data."""
        return self.coordination_engine.validate_coordination_system(system_data)
    
    def validate_security(self, security_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate security data."""
        return self.security_engine.validate_security(security_data)
    
    def validate_performance(self, performance_data: Dict[str, Any]) -> List[ValidationResult]:
        """Validate performance data."""
        return self.performance_engine.validate_performance(performance_data)
    
    def get_validation_summary(self, issues: List[ValidationResult]) -> Dict[str, Any]:
        """Get validation summary."""
        return ValidationSummary.create_summary(issues)
    
    def get_validation_result(self, data: Any, validation_type: str) -> ValidationResult:
        """Get comprehensive validation result."""
        issues = self.validate(data, validation_type)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return ValidationResult(
            is_valid=is_valid,
            issues=issues,
            validated_data=data,
            validation_type=validation_type
        )


# Factory function for dependency injection
def create_unified_validation_orchestrator() -> UnifiedValidationOrchestrator:
    """Factory function to create unified validation orchestrator"""
    return UnifiedValidationOrchestrator()


# Global instance for backward compatibility
_unified_validator = None


def get_unified_validator() -> UnifiedValidationOrchestrator:
    """Get the global unified validator instance."""
    global _unified_validator
    if _unified_validator is None:
        _unified_validator = UnifiedValidationOrchestrator()
    return _unified_validator


# Export for DI
__all__ = ['UnifiedValidationOrchestrator', 'create_unified_validation_orchestrator', 'get_unified_validator']
