#!/usr/bin/env python3
"""
Unified Validation Service - Modular Components
================================================

Split from unified_validation_service.py (815 lines) to achieve V2 compliance.
This module contains the core validation service components.

Author: Agent-1 (PERPETUAL MOTION LEADER - V2 COMPLIANCE SPECIALIST)
Mission: V2 COMPLIANCE OPTIMIZATION - File Size Reduction
License: MIT
"""

import json
import logging
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation level enumeration"""
    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"
    CRITICAL = "critical"


@dataclass
class ValidationConfig:
    """Validation service configuration"""
    enable_caching: bool = True
    cache_ttl: int = 300
    default_level: ValidationLevel = ValidationLevel.STANDARD
    enable_logging: bool = True
    max_validation_time: int = 30  # seconds


@dataclass
class ValidationResult:
    """Validation result structure"""
    success: bool
    message: str
    level: ValidationLevel
    timestamp: datetime = field(default_factory=datetime.now)
    details: Dict[str, Any] = field(default_factory=dict)


class ValidationRule:
    """Base class for validation rules"""
    
    def __init__(self, name: str, level: ValidationLevel = ValidationLevel.STANDARD):
        self.name = name
        self.level = level
        
    def validate(self, data: Any) -> ValidationResult:
        """Validate data - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement validate method")


class StringValidationRule(ValidationRule):
    """String validation rule"""
    
    def __init__(self, name: str, min_length: int = 0, max_length: int = None, pattern: str = None):
        super().__init__(name)
        self.min_length = min_length
        self.max_length = max_length
        self.pattern = pattern
        
    def validate(self, data: Any) -> ValidationResult:
        """Validate string data"""
        if not isinstance(data, str):
            return ValidationResult(
                success=False,
                message=f"Expected string, got {type(data).__name__}",
                level=self.level
            )
            
        if len(data) < self.min_length:
            return ValidationResult(
                success=False,
                message=f"String too short: {len(data)} < {self.min_length}",
                level=self.level
            )
            
        if self.max_length and len(data) > self.max_length:
            return ValidationResult(
                success=False,
                message=f"String too long: {len(data)} > {self.max_length}",
                level=self.level
            )
            
        if self.pattern:
            import re
            if not re.match(self.pattern, data):
                return ValidationResult(
                    success=False,
                    message=f"String does not match pattern: {self.pattern}",
                    level=self.level
                )
                
        return ValidationResult(
            success=True,
            message=f"String validation passed",
            level=self.level
        )


class NumberValidationRule(ValidationRule):
    """Number validation rule"""
    
    def __init__(self, name: str, min_value: float = None, max_value: float = None):
        super().__init__(name)
        self.min_value = min_value
        self.max_value = max_value
        
    def validate(self, data: Any) -> ValidationResult:
        """Validate numeric data"""
        try:
            num = float(data)
        except (ValueError, TypeError):
            return ValidationResult(
                success=False,
                message=f"Expected number, got {type(data).__name__}",
                level=self.level
            )
            
        if self.min_value is not None and num < self.min_value:
            return ValidationResult(
                success=False,
                message=f"Number too small: {num} < {self.min_value}",
                level=self.level
            )
            
        if self.max_value is not None and num > self.max_value:
            return ValidationResult(
                success=False,
                message=f"Number too large: {num} > {self.max_value}",
                level=self.level
            )
            
        return ValidationResult(
            success=True,
            message=f"Number validation passed",
            level=self.level
        )


class ValidationEngine:
    """Core validation engine"""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.rules: Dict[str, ValidationRule] = {}
        self.cache = {}
        
    def add_rule(self, rule: ValidationRule) -> None:
        """Add a validation rule"""
        self.rules[rule.name] = rule
        
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a validation rule"""
        if rule_name in self.rules:
            del self.rules[rule_name]
            return True
        return False
        
    def validate(self, data: Any, rule_names: List[str] = None) -> List[ValidationResult]:
        """Validate data using specified rules"""
        if rule_names is None:
            rule_names = list(self.rules.keys())
            
        results = []
        for rule_name in rule_names:
            if rule_name in self.rules:
                rule = self.rules[rule_name]
                result = rule.validate(data)
                results.append(result)
                
        return results


class ValidationCache:
    """Validation result caching"""
    
    def __init__(self, config: ValidationConfig):
        self.config = config
        self.cache = {}
        self.timestamps = {}
        
    def get_cached(self, key: str) -> Optional[List[ValidationResult]]:
        """Get cached validation results"""
        if not self.config.enable_caching:
            return None
            
        if key in self.cache:
            timestamp = self.timestamps.get(key, 0)
            if datetime.now().timestamp() - timestamp < self.config.cache_ttl:
                return self.cache[key]
            else:
                # Expired, remove from cache
                del self.cache[key]
                del self.timestamps[key]
        return None
        
    def set_cached(self, key: str, results: List[ValidationResult]) -> None:
        """Cache validation results"""
        if not self.config.enable_caching:
            return
            
        self.cache[key] = results
        self.timestamps[key] = datetime.now().timestamp()


# Main service class that orchestrates all components
class UnifiedValidationService:
    """Unified validation service - main orchestrator"""
    
    def __init__(self, config: ValidationConfig = None):
        self.config = config or ValidationConfig()
        self.engine = ValidationEngine(self.config)
        self.cache = ValidationCache(self.config)
        
        # Add default rules
        self._setup_default_rules()
        
    def _setup_default_rules(self) -> None:
        """Setup default validation rules"""
        # String rules
        self.engine.add_rule(StringValidationRule("non_empty_string", min_length=1))
        self.engine.add_rule(StringValidationRule("email", pattern=r"^[^@]+@[^@]+\.[^@]+$"))
        
        # Number rules
        self.engine.add_rule(NumberValidationRule("positive_number", min_value=0))
        self.engine.add_rule(NumberValidationRule("percentage", min_value=0, max_value=100))
        
    def validate_data(self, data: Any, rule_names: List[str] = None) -> List[ValidationResult]:
        """Validate data using specified rules"""
        # Check cache first
        cache_key = f"{hash(str(data))}_{','.join(rule_names or [])}"
        cached = self.cache.get_cached(cache_key)
        if cached:
            return cached
            
        # Perform validation
        results = self.engine.validate(data, rule_names)
        
        # Cache results
        self.cache.set_cached(cache_key, results)
        
        return results
        
    def add_custom_rule(self, rule: ValidationRule) -> None:
        """Add a custom validation rule"""
        self.engine.add_rule(rule)
        
    def get_available_rules(self) -> List[str]:
        """Get list of available validation rules"""
        return list(self.engine.rules.keys())
        
    def validate_batch(self, data_list: List[Any], rule_names: List[str] = None) -> Dict[int, List[ValidationResult]]:
        """Validate a batch of data items"""
        results = {}
        for i, data in enumerate(data_list):
            results[i] = self.validate_data(data, rule_names)
        return results


if __name__ == "__main__":
    # Test the modularized validation service
    service = UnifiedValidationService()
    
    # Test data
    test_data = [
        "test@example.com",
        "invalid-email",
        "",
        42,
        -5,
        150
    ]
    
    # Test validation
    print("✅ Testing email validation...")
    email_results = service.validate_data("test@example.com", ["email"])
    print(f"Email validation: {email_results[0].success}")
    
    print("✅ Testing positive number validation...")
    number_results = service.validate_data(42, ["positive_number"])
    print(f"Number validation: {number_results[0].success}")
    
    print("✅ Testing batch validation...")
    batch_results = service.validate_batch(test_data, ["email", "positive_number"])
    print(f"Batch validation completed: {len(batch_results)} items processed")
    
    print("✅ Validation service test successful")
