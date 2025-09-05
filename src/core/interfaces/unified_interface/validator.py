"""
Interface Validator - KISS Simplified
=====================================

Simplified interface validation for V2 compliance.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined validation logic.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import inspect
from typing import Any, Dict, List, Optional, Type
from datetime import datetime
import logging
from .models import (
    InterfaceMetadata, InterfaceDefinition, InterfaceValidationResult,
    InterfaceType, InterfaceStatus, BaseInterface
)


class InterfaceValidator:
    """Simplified interface validation strategies."""
    
    def __init__(self):
        """Initialize interface validator."""
        self.logger = logging.getLogger(__name__)
        self.validation_strategies = {
            InterfaceType.SERVICE: self._validate_service_interface,
            InterfaceType.REPOSITORY: self._validate_repository_interface,
            InterfaceType.VALIDATOR: self._validate_validator_interface,
            InterfaceType.ORCHESTRATOR: self._validate_orchestrator_interface,
            InterfaceType.ENGINE: self._validate_engine_interface,
            InterfaceType.HANDLER: self._validate_handler_interface,
            InterfaceType.UTILITY: self._validate_utility_interface,
            InterfaceType.CORE: self._validate_core_interface
        }
    
    def validate_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> InterfaceValidationResult:
        """Validate interface - KISS simplified."""
        # Basic validation only
        errors = []
        warnings = []
        
        if not metadata.name:
            errors.append("Interface name is required")
        if not definition.class_name:
            errors.append("Class name is required")
        
        is_valid = len(errors) == 0
        score = 1.0 if is_valid else 0.0
        
        return self._create_validation_result(metadata.interface_id, is_valid, errors, warnings, score)
    
# KISS Simplified - Complex validation methods removed
    
    def _validate_by_type(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate by interface type - simplified."""
        validator = self.validation_strategies.get(metadata.interface_type)
        if validator:
            return validator(metadata, definition)
        return {'is_valid': True, 'errors': [], 'warnings': []}
    
    def _validate_service_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate service interface - simplified."""
        errors = []
        warnings = []
        
        # Service-specific checks
        required_methods = ['initialize', 'execute', 'cleanup']
        for method in required_methods:
            if method not in definition.methods:
                warnings.append(f"Service interface should have {method} method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_repository_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate repository interface - simplified."""
        errors = []
        warnings = []
        
        # Repository-specific checks
        crud_methods = ['create', 'read', 'update', 'delete']
        for method in crud_methods:
            if method not in definition.methods:
                warnings.append(f"Repository interface should have {method} method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_validator_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate validator interface - simplified."""
        errors = []
        warnings = []
        
        # Validator-specific checks
        if 'validate' not in definition.methods:
            errors.append("Validator interface must have validate method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_orchestrator_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate orchestrator interface - simplified."""
        errors = []
        warnings = []
        
        # Orchestrator-specific checks
        if 'orchestrate' not in definition.methods:
            warnings.append("Orchestrator interface should have orchestrate method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_engine_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate engine interface - simplified."""
        errors = []
        warnings = []
        
        # Engine-specific checks
        if 'process' not in definition.methods:
            warnings.append("Engine interface should have process method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_handler_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate handler interface - simplified."""
        errors = []
        warnings = []
        
        # Handler-specific checks
        if 'handle' not in definition.methods:
            warnings.append("Handler interface should have handle method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_utility_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate utility interface - simplified."""
        errors = []
        warnings = []
        
        # Utility-specific checks
        if len(definition.methods) < 2:
            warnings.append("Utility interface should have multiple utility methods")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _validate_core_interface(self, metadata: InterfaceMetadata, definition: InterfaceDefinition) -> Dict[str, Any]:
        """Validate core interface - simplified."""
        errors = []
        warnings = []
        
        # Core-specific checks
        if 'initialize' not in definition.methods:
            warnings.append("Core interface should have initialize method")
        
        return {'is_valid': len(errors) == 0, 'errors': errors, 'warnings': warnings}
    
    def _calculate_validation_score(self, errors: List[str], warnings: List[str]) -> float:
        """Calculate validation score - simplified."""
        if errors:
            return max(0.0, 1.0 - (len(errors) * 0.2))
        if warnings:
            return max(0.5, 1.0 - (len(warnings) * 0.1))
        return 1.0
    
    def _create_validation_result(self, interface_id: str, is_valid: bool, errors: List[str], warnings: List[str], score: float) -> InterfaceValidationResult:
        """Create validation result - simplified."""
        return InterfaceValidationResult(
            validation_id=f"val_{int(datetime.now().timestamp())}",
            interface_id=interface_id,
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            validation_score=score,
            validated_at=datetime.now()
        )
    
    def validate_interface_implementation(self, interface_class: Type[BaseInterface], metadata: InterfaceMetadata) -> InterfaceValidationResult:
        """Validate interface implementation - simplified."""
        try:
            errors = []
            warnings = []
            
            # Check if class implements required methods
            required_methods = metadata.required_methods or []
            for method_name in required_methods:
                if not hasattr(interface_class, method_name):
                    errors.append(f"Missing required method: {method_name}")
            
            # Check method signatures
            for method_name in required_methods:
                if hasattr(interface_class, method_name):
                    method = getattr(interface_class, method_name)
                    if not callable(method):
                        errors.append(f"Method {method_name} is not callable")
            
            validation_score = self._calculate_validation_score(errors, warnings)
            
            return self._create_validation_result(
                metadata.interface_id,
                len(errors) == 0,
                errors,
                warnings,
                validation_score
            )
            
        except Exception as e:
            self.logger.error(f"Error validating implementation: {e}")
            return self._create_validation_result(metadata.interface_id, False, [f"Implementation error: {str(e)}"], [], 0.0)
    
    def get_validation_summary(self, results: List[InterfaceValidationResult]) -> Dict[str, Any]:
        """Get validation summary - simplified."""
        total = len(results)
        valid = len([r for r in results if r.is_valid])
        invalid = total - valid
        
        return {
            "total_interfaces": total,
            "valid_interfaces": valid,
            "invalid_interfaces": invalid,
            "validation_rate": valid / total if total > 0 else 0.0,
            "average_score": sum(r.validation_score for r in results) / total if total > 0 else 0.0
        }