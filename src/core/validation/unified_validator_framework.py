#!/usr/bin/env python3
"""
Unified Validator Framework - Agent-2 Consolidation Implementation
Consolidates all validator implementations into unified framework
"""

import json
import re
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Unified validation result structure."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    
    def add_error(self, error: str) -> None:
        """Add validation error."""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str) -> None:
        """Add validation warning."""
        self.warnings.append(warning)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            'is_valid': self.is_valid,
            'errors': self.errors,
            'warnings': self.warnings,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class IValidator(ABC):
    """Unified validator interface."""
    
    @abstractmethod
    def validate(self, data: Any) -> ValidationResult:
        """Validate data and return result."""
        pass
    
    @abstractmethod
    def get_validator_name(self) -> str:
        """Get validator name."""
        pass


class IChecker(ABC):
    """Unified checker interface."""
    
    @abstractmethod
    def check(self, data: Any) -> bool:
        """Check data validity."""
        pass
    
    @abstractmethod
    def get_checker_name(self) -> str:
        """Get checker name."""
        pass


class IValidationRule(ABC):
    """Unified validation rule interface."""
    
    @abstractmethod
    def apply(self, data: Any) -> ValidationResult:
        """Apply validation rule."""
        pass
    
    @abstractmethod
    def get_rule_name(self) -> str:
        """Get rule name."""
        pass


class BaseValidator(IValidator):
    """Base validator implementation."""
    
    def __init__(self, name: str, rules: Optional[List[IValidationRule]] = None):
        """Initialize base validator."""
        self.name = name
        self.rules = rules or []
        self.validation_history: List[ValidationResult] = []
    
    def validate(self, data: Any) -> ValidationResult:
        """Validate data using all rules."""
        result = ValidationResult(is_valid=True)
        result.metadata['validator_name'] = self.name
        result.metadata['rules_applied'] = len(self.rules)
        
        for rule in self.rules:
            rule_result = rule.apply(data)
            if not rule_result.is_valid:
                result.errors.extend(rule_result.errors)
            result.warnings.extend(rule_result.warnings)
        
        result.is_valid = len(result.errors) == 0
        self.validation_history.append(result)
        
        return result
    
    def get_validator_name(self) -> str:
        """Get validator name."""
        return self.name
    
    def add_rule(self, rule: IValidationRule) -> None:
        """Add validation rule."""
        self.rules.append(rule)
    
    def get_validation_history(self) -> List[ValidationResult]:
        """Get validation history."""
        return self.validation_history.copy()


class BaseChecker(IChecker):
    """Base checker implementation."""
    
    def __init__(self, name: str, validation_func: Optional[Callable[[Any], bool]] = None):
        """Initialize base checker."""
        self.name = name
        self.validation_func = validation_func or (lambda x: True)
        self.check_history: List[bool] = []
    
    def check(self, data: Any) -> bool:
        """Check data validity."""
        result = self.validation_func(data)
        self.check_history.append(result)
        return result
    
    def get_checker_name(self) -> str:
        """Get checker name."""
        return self.name
    
    def get_check_history(self) -> List[bool]:
        """Get check history."""
        return self.check_history.copy()


class BaseValidationRule(IValidationRule):
    """Base validation rule implementation."""
    
    def __init__(self, name: str, rule_func: Optional[Callable[[Any], ValidationResult]] = None):
        """Initialize base validation rule."""
        self.name = name
        self.rule_func = rule_func or (lambda x: ValidationResult(is_valid=True))
        self.rule_history: List[ValidationResult] = []
    
    def apply(self, data: Any) -> ValidationResult:
        """Apply validation rule."""
        result = self.rule_func(data)
        result.metadata['rule_name'] = self.name
        self.rule_history.append(result)
        return result
    
    def get_rule_name(self) -> str:
        """Get rule name."""
        return self.name
    
    def get_rule_history(self) -> List[ValidationResult]:
        """Get rule history."""
        return self.rule_history.copy()


class UnifiedValidationFramework:
    """Unified validation framework for all validator implementations."""
    
    def __init__(self):
        """Initialize unified validation framework."""
        self.validators: Dict[str, IValidator] = {}
        self.checkers: Dict[str, IChecker] = {}
        self.rules: Dict[str, IValidationRule] = {}
        self.framework_stats = {
            'total_validators': 0,
            'total_checkers': 0,
            'total_rules': 0,
            'validations_performed': 0,
            'checks_performed': 0,
            'rules_applied': 0
        }
    
    def register_validator(self, validator: IValidator) -> None:
        """Register validator in framework."""
        name = validator.get_validator_name()
        self.validators[name] = validator
        self.framework_stats['total_validators'] += 1
    
    def register_checker(self, checker: IChecker) -> None:
        """Register checker in framework."""
        name = checker.get_checker_name()
        self.checkers[name] = checker
        self.framework_stats['total_checkers'] += 1
    
    def register_rule(self, rule: IValidationRule) -> None:
        """Register validation rule in framework."""
        name = rule.get_rule_name()
        self.rules[name] = rule
        self.framework_stats['total_rules'] += 1
    
    def validate_with(self, validator_name: str, data: Any) -> ValidationResult:
        """Validate data using specific validator."""
        if validator_name not in self.validators:
            result = ValidationResult(is_valid=False)
            result.add_error(f"Validator '{validator_name}' not found")
            return result
        
        validator = self.validators[validator_name]
        result = validator.validate(data)
        self.framework_stats['validations_performed'] += 1
        return result
    
    def check_with(self, checker_name: str, data: Any) -> bool:
        """Check data using specific checker."""
        if checker_name not in self.checkers:
            return False
        
        checker = self.checkers[checker_name]
        result = checker.check(data)
        self.framework_stats['checks_performed'] += 1
        return result
    
    def apply_rule(self, rule_name: str, data: Any) -> ValidationResult:
        """Apply specific validation rule."""
        if rule_name not in self.rules:
            result = ValidationResult(is_valid=False)
            result.add_error(f"Rule '{rule_name}' not found")
            return result
        
        rule = self.rules[rule_name]
        result = rule.apply(data)
        self.framework_stats['rules_applied'] += 1
        return result
    
    def get_framework_stats(self) -> Dict[str, Any]:
        """Get framework statistics."""
        return self.framework_stats.copy()
    
    def list_validators(self) -> List[str]:
        """List all registered validators."""
        return list(self.validators.keys())
    
    def list_checkers(self) -> List[str]:
        """List all registered checkers."""
        return list(self.checkers.keys())
    
    def list_rules(self) -> List[str]:
        """List all registered rules."""
        return list(self.rules.keys())


class ValidatorFactory:
    """Factory for creating validators, checkers, and rules."""
    
    @staticmethod
    def create_validator(name: str, rules: Optional[List[IValidationRule]] = None) -> BaseValidator:
        """Create new validator."""
        return BaseValidator(name, rules)
    
    @staticmethod
    def create_checker(name: str, validation_func: Optional[Callable[[Any], bool]] = None) -> BaseChecker:
        """Create new checker."""
        return BaseChecker(name, validation_func)
    
    @staticmethod
    def create_rule(name: str, rule_func: Optional[Callable[[Any], ValidationResult]] = None) -> BaseValidationRule:
        """Create new validation rule."""
        return BaseValidationRule(name, rule_func)
    
    @staticmethod
    def create_string_validator(name: str, min_length: int = 0, max_length: Optional[int] = None) -> BaseValidator:
        """Create string validator with common rules."""
        rules = []
        
        if min_length > 0:
            rules.append(BaseValidationRule(
                f"{name}_min_length",
                lambda x: ValidationResult(is_valid=len(str(x)) >= min_length) if x else ValidationResult(is_valid=False)
            ))
        
        if max_length:
            rules.append(BaseValidationRule(
                f"{name}_max_length",
                lambda x: ValidationResult(is_valid=len(str(x)) <= max_length) if x else ValidationResult(is_valid=False)
            ))
        
        return BaseValidator(name, rules)
    
    @staticmethod
    def create_numeric_validator(name: str, min_value: Optional[float] = None, max_value: Optional[float] = None) -> BaseValidator:
        """Create numeric validator with common rules."""
        rules = []
        
        if min_value is not None:
            rules.append(BaseValidationRule(
                f"{name}_min_value",
                lambda x: ValidationResult(is_valid=float(x) >= min_value) if x else ValidationResult(is_valid=False)
            ))
        
        if max_value is not None:
            rules.append(BaseValidationRule(
                f"{name}_max_value",
                lambda x: ValidationResult(is_valid=float(x) <= max_value) if x else ValidationResult(is_valid=False)
            ))
        
        return BaseValidator(name, rules)


class ValidationRegistry:
    """Registry for managing validation components."""
    
    def __init__(self):
        """Initialize validation registry."""
        self.registry: Dict[str, Dict[str, Any]] = {}
    
    def register(self, component_type: str, name: str, component: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Register validation component."""
        if component_type not in self.registry:
            self.registry[component_type] = {}
        
        self.registry[component_type][name] = {
            'component': component,
            'metadata': metadata or {},
            'registered_at': datetime.now().isoformat()
        }
    
    def get(self, component_type: str, name: str) -> Optional[Any]:
        """Get validation component."""
        if component_type in self.registry and name in self.registry[component_type]:
            return self.registry[component_type][name]['component']
        return None
    
    def list_components(self, component_type: str) -> List[str]:
        """List components of specific type."""
        if component_type in self.registry:
            return list(self.registry[component_type].keys())
        return []
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        stats = {}
        for component_type, components in self.registry.items():
            stats[component_type] = len(components)
        return stats


# Global framework instance
unified_framework = UnifiedValidationFramework()
validation_registry = ValidationRegistry()


def get_unified_framework() -> UnifiedValidationFramework:
    """Get global unified validation framework."""
    return unified_framework


def get_validation_registry() -> ValidationRegistry:
    """Get global validation registry."""
    return validation_registry


# Example usage and migration helpers
def migrate_existing_validator(old_validator: Any, new_name: str) -> BaseValidator:
    """Migrate existing validator to unified framework."""
    # This is a placeholder for actual migration logic
    # In practice, you would analyze the old validator and create a compatible one
    return BaseValidator(new_name)


def create_consolidated_validator(validator_names: List[str], consolidated_name: str) -> BaseValidator:
    """Create consolidated validator from multiple existing validators."""
    # This is a placeholder for actual consolidation logic
    # In practice, you would merge validation logic from multiple validators
    return BaseValidator(consolidated_name)


if __name__ == "__main__":
    # Example usage
    print("🚀 Unified Validator Framework - Agent-2 Consolidation Implementation")
    print("=" * 80)
    
    # Create example validators
    string_validator = ValidatorFactory.create_string_validator("email", min_length=5, max_length=100)
    numeric_validator = ValidatorFactory.create_numeric_validator("age", min_value=0, max_value=150)
    
    # Register in framework
    unified_framework.register_validator(string_validator)
    unified_framework.register_validator(numeric_validator)
    
    # Test validations
    email_result = unified_framework.validate_with("email", "test@example.com")
    age_result = unified_framework.validate_with("age", 25)
    
    print(f"Email validation: {email_result.is_valid}")
    print(f"Age validation: {age_result.is_valid}")
    print(f"Framework stats: {unified_framework.get_framework_stats()}")
    
    print("✅ Unified Validator Framework ready for consolidation!")
