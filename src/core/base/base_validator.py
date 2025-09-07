"""
Unified Base Validator Class

This class consolidates functionality from 2 duplicate base_validator.py files:
- src/core/validation/base_validator.py
- src/core/validation/validators/base_validator.py

Provides unified validation patterns for:
- Contract validation
- Performance validation
- Workflow validation
- Security validation
- Storage validation
- Task validation
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import time
from pathlib import Path


class ValidationSeverity(Enum):
    """Unified validation severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Unified validation status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


class ValidationType(Enum):
    """Unified validation types."""
    CONTRACT = "contract"
    PERFORMANCE = "performance"
    WORKFLOW = "workflow"
    SECURITY = "security"
    STORAGE = "storage"
    TASK = "task"
    CUSTOM = "custom"


@dataclass
class ValidationRule:
    """Unified validation rule definition."""
    name: str
    description: str
    validation_type: ValidationType
    severity: ValidationSeverity
    enabled: bool = True
    timeout: float = 30.0
    retry_attempts: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Unified validation result."""
    rule_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    execution_time: float = 0.0
    timestamp: float = field(default_factory=time.time)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


@dataclass
class ValidationConfig:
    """Unified validation configuration."""
    name: str
    validation_type: ValidationType
    enabled: bool = True
    max_workers: int = 4
    timeout: float = 60.0
    retry_attempts: int = 2
    log_level: str = "INFO"
    rules: List[ValidationRule] = field(default_factory=list)
    config_path: Optional[Path] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseValidator(ABC):
    """
    Unified base class for all validators.
    
    Consolidates functionality from duplicate base_validator implementations:
    - src/core/validation/base_validator.py
    - src/core/validation/validators/base_validator.py
    """
    
    def __init__(self, config: ValidationConfig):
        """
        Initialize the unified base validator.
        
        Args:
            config: Validation configuration object
        """
        self.config = config
        self.logger = self._setup_logging()
        self.results: List[ValidationResult] = []
        self._initialize()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up unified logging for all validator types."""
        logger = logging.getLogger(f"{self.__class__.__name__}.{self.config.name}")
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize(self) -> None:
        """Initialize validator-specific components."""
        try:
            self.logger.info(f"Initializing {self.config.validation_type.value} validator: {self.config.name}")
            
            # Load configuration if path provided
            if self.config.config_path and self.config.config_path.exists():
                self._load_config()
            
            # Initialize validator-specific resources
            self._initialize_resources()
            
            # Validate configuration
            self._validate_config()
            
            # Load validation rules
            self._load_validation_rules()
            
            self.logger.info(f"Validator {self.config.name} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize validator {self.config.name}: {e}")
            raise
    
    @abstractmethod
    def _initialize_resources(self) -> None:
        """Initialize validator-specific resources. Must be implemented by subclasses."""
        pass
    
    def _load_config(self) -> None:
        """Load configuration from file if specified."""
        try:
            self.logger.debug(f"Loading configuration from {self.config.config_path}")
            # Implementation depends on config format (JSON, YAML, etc.)
        except Exception as e:
            self.logger.warning(f"Failed to load config from {self.config.config_path}: {e}")
    
    def _validate_config(self) -> None:
        """Validate validator configuration."""
        if not self.config.name:
            raise ValueError("Validator name is required")
        
        if self.config.max_workers < 1:
            raise ValueError("max_workers must be at least 1")
        
        if self.config.timeout <= 0:
            raise ValueError("timeout must be positive")
        
        if self.config.retry_attempts < 0:
            raise ValueError("retry_attempts must be non-negative")
    
    def _load_validation_rules(self) -> None:
        """Load validation rules from configuration."""
        if not self.config.rules:
            self.logger.warning("No validation rules configured")
            return
        
        self.logger.info(f"Loaded {len(self.config.rules)} validation rules")
        for rule in self.config.rules:
            self.logger.debug(f"Rule: {rule.name} - {rule.description}")
    
    def validate(self, data: Any, context: Optional[Dict[str, Any]] = None) -> List[ValidationResult]:
        """
        Perform validation on the given data.
        
        Args:
            data: Data to validate
            context: Additional context for validation
            
        Returns:
            List of validation results
        """
        start_time = time.time()
        self.logger.info(f"Starting validation for {self.config.name}")
        
        try:
            # Clear previous results
            self.results.clear()
            
            # Perform validation using configured rules
            for rule in self.config.rules:
                if not rule.enabled:
                    continue
                
                result = self._execute_validation_rule(rule, data, context)
                self.results.append(result)
                
                # Log result
                if result.status == ValidationStatus.PASSED:
                    self.logger.debug(f"Rule {rule.name} passed")
                elif result.status == ValidationStatus.FAILED:
                    self.logger.warning(f"Rule {rule.name} failed: {result.message}")
                else:
                    self.logger.info(f"Rule {rule.name} status: {result.status.value}")
            
            execution_time = time.time() - start_time
            self.logger.info(f"Validation completed in {execution_time:.2f}s. Results: {len(self.results)}")
            
            return self.results
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            # Create error result
            error_result = ValidationResult(
                rule_name="validation_error",
                status=ValidationStatus.ERROR,
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation failed: {e}",
                execution_time=time.time() - start_time
            )
            self.results.append(error_result)
            return self.results
    
    def _execute_validation_rule(self, rule: ValidationRule, data: Any, context: Optional[Dict[str, Any]]) -> ValidationResult:
        """Execute a single validation rule."""
        start_time = time.time()
        
        try:
            # Execute the specific validation logic
            validation_result = self._validate_with_rule(rule, data, context)
            
            execution_time = time.time() - start_time
            
            return ValidationResult(
                rule_name=rule.name,
                status=validation_result['status'],
                severity=rule.severity,
                message=validation_result['message'],
                details=validation_result.get('details', {}),
                execution_time=execution_time,
                errors=validation_result.get('errors', []),
                warnings=validation_result.get('warnings', [])
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            self.logger.error(f"Rule {rule.name} execution failed: {e}")
            
            return ValidationResult(
                rule_name=rule.name,
                status=ValidationStatus.ERROR,
                severity=rule.severity,
                message=f"Rule execution failed: {e}",
                execution_time=execution_time,
                errors=[str(e)]
            )
    
    @abstractmethod
    def _validate_with_rule(self, rule: ValidationRule, data: Any, context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate data using a specific rule. Must be implemented by subclasses.
        
        Returns:
            Dict with keys: status, message, details, errors, warnings
        """
        pass
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation results."""
        if not self.results:
            return {
                'total_rules': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'errors': 0,
                'success_rate': 0.0,
                'total_execution_time': 0.0
            }
        
        total_rules = len(self.results)
        passed = sum(1 for r in self.results if r.status == ValidationStatus.PASSED)
        failed = sum(1 for r in self.results if r.status == ValidationStatus.FAILED)
        skipped = sum(1 for r in self.results if r.status == ValidationStatus.SKIPPED)
        errors = sum(1 for r in self.results if r.status == ValidationStatus.ERROR)
        
        success_rate = (passed / total_rules) * 100 if total_rules > 0 else 0.0
        total_execution_time = sum(r.execution_time for r in self.results)
        
        return {
            'total_rules': total_rules,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'errors': errors,
            'success_rate': success_rate,
            'total_execution_time': total_execution_time
        }
    
    def get_failed_validations(self) -> List[ValidationResult]:
        """Get list of failed validations."""
        return [r for r in self.results if r.status == ValidationStatus.FAILED]
    
    def get_critical_validations(self) -> List[ValidationResult]:
        """Get list of critical validation failures."""
        return [
            r for r in self.results 
            if r.status == ValidationStatus.FAILED and r.severity == ValidationSeverity.CRITICAL
        ]
    
    def add_validation_rule(self, rule: ValidationRule) -> None:
        """Add a new validation rule."""
        self.config.rules.append(rule)
        self.logger.info(f"Added validation rule: {rule.name}")
    
    def remove_validation_rule(self, rule_name: str) -> bool:
        """Remove a validation rule by name."""
        for i, rule in enumerate(self.config.rules):
            if rule.name == rule_name:
                del self.config.rules[i]
                self.logger.info(f"Removed validation rule: {rule_name}")
                return True
        return False
    
    def __repr__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(name='{self.config.name}', type='{self.config.validation_type.value}')"
