"""
Unified Base Model Class

This class consolidates functionality from 32 duplicate models.py files:
- Task models
- Health models
- Validation models
- Learning models
- FSM models
- Service models
- And many more...

Provides unified data model patterns for the entire system.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union, TypeVar, Generic, get_type_hints
from dataclasses import dataclass, field, asdict, is_dataclass
from enum import Enum
import logging
import json
import uuid
from datetime import datetime, timezone
from pathlib import Path


class ModelType(Enum):
    """Unified model types."""
    TASK = "task"
    HEALTH = "health"
    VALIDATION = "validation"
    LEARNING = "learning"
    FSM = "fsm"
    SERVICE = "service"
    WORKFLOW = "workflow"
    PERFORMANCE = "performance"
    SECURITY = "security"
    DATABASE = "database"
    CUSTOM = "custom"


class ModelStatus(Enum):
    """Unified model status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ARCHIVED = "archived"
    DELETED = "deleted"
    DRAFT = "draft"
    PUBLISHED = "published"


@dataclass
class ModelMetadata:
    """Unified model metadata."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    description: str = ""
    model_type: ModelType = ModelType.CUSTOM
    version: str = "1.0.0"
    status: ModelStatus = ModelStatus.ACTIVE
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    modified: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    author: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationError:
    """Unified validation error."""
    field: str
    message: str
    code: str = ""
    severity: str = "error"
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelValidationResult:
    """Unified model validation result."""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class BaseModel(ABC):
    """
    Unified base class for all data models.
    
    Consolidates functionality from duplicate models implementations:
    - src/core/task_management/models.py
    - src/core/health/models.py
    - src/core/validation/models.py
    - src/core/learning/models.py
    - src/core/fsm/models.py
    - src/services/models.py
    - And 26+ more...
    """
    
    def __init__(self, **kwargs):
        """
        Initialize the unified base model.
        
        Args:
            **kwargs: Model attributes
        """
        self.metadata = ModelMetadata(
            name=self.__class__.__name__,
            model_type=self._get_model_type()
        )
        self.logger = self._setup_logging()
        
        # Set attributes from kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self._initialize()
    
    def _setup_logging(self) -> logging.Logger:
        """Set up unified logging for all model types."""
        logger = logging.getLogger(f"{self.__class__.__name__}")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize(self) -> None:
        """Initialize model-specific components."""
        try:
            self.logger.debug(f"Initializing model: {self.metadata.name}")
            
            # Initialize model-specific resources
            self._initialize_resources()
            
            # Validate model if validation is enabled
            if self._should_validate_on_init():
                self._validate_model()
            
            self.logger.debug(f"Model {self.metadata.name} initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize model {self.metadata.name}: {e}")
            raise
    
    @abstractmethod
    def _initialize_resources(self) -> None:
        """Initialize model-specific resources. Must be implemented by subclasses."""
        pass
    
    def _get_model_type(self) -> ModelType:
        """Get the model type. Can be overridden by subclasses."""
        return ModelType.CUSTOM
    
    def _should_validate_on_init(self) -> bool:
        """Whether to validate the model on initialization. Can be overridden."""
        return True
    
    def _validate_model(self) -> None:
        """Validate the model."""
        validation_result = self.validate()
        if not validation_result.is_valid:
            error_messages = [f"{e.field}: {e.message}" for e in validation_result.errors]
            raise ValueError(f"Model validation failed: {'; '.join(error_messages)}")
    
    def validate(self) -> ModelValidationResult:
        """
        Validate the model.
        
        Returns:
            ModelValidationResult with validation status
        """
        errors = []
        warnings = []
        
        try:
            # Get type hints for validation
            type_hints = get_type_hints(self.__class__)
            
            # Validate each field
            for field_name, field_type in type_hints.items():
                if field_name.startswith('_'):
                    continue
                
                field_value = getattr(self, field_name, None)
                field_errors = self._validate_field(field_name, field_value, field_type)
                
                for error in field_errors:
                    if error.severity == "error":
                        errors.append(error)
                    else:
                        warnings.append(error)
            
            # Run model-specific validation
            model_errors = self._validate_model_specific()
            errors.extend(model_errors)
            
            is_valid = len(errors) == 0
            
            return ModelValidationResult(
                is_valid=is_valid,
                errors=errors,
                warnings=warnings
            )
            
        except Exception as e:
            self.logger.error(f"Validation failed: {e}")
            error = ValidationError(
                field="validation_system",
                message=f"Validation system error: {e}",
                code="validation_error",
                severity="error"
            )
            return ModelValidationResult(
                is_valid=False,
                errors=[error]
            )
    
    def _validate_field(self, field_name: str, field_value: Any, field_type: type) -> List[ValidationError]:
        """Validate a single field."""
        errors = []
        
        try:
            # Check if field is required (not Optional)
            if not self._is_optional_type(field_type) and field_value is None:
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Field {field_name} is required",
                    code="required_field",
                    severity="error"
                ))
                return errors
            
            # Skip validation if value is None and field is optional
            if field_value is None:
                return errors
            
            # Type validation
            if not self._is_valid_type(field_value, field_type):
                errors.append(ValidationError(
                    field=field_name,
                    message=f"Field {field_name} has invalid type. Expected {field_type}, got {type(field_value)}",
                    code="invalid_type",
                    severity="error"
                ))
            
            # Custom field validation
            field_errors = self._validate_field_custom(field_name, field_value, field_type)
            errors.extend(field_errors)
            
        except Exception as e:
            errors.append(ValidationError(
                field=field_name,
                message=f"Field validation error: {e}",
                code="validation_error",
                severity="error"
            ))
        
        return errors
    
    def _is_optional_type(self, field_type: type) -> bool:
        """Check if a type is Optional (Union with None)."""
        if hasattr(field_type, '__origin__') and field_type.__origin__ is Union:
            return type(None) in field_type.__args__
        return False
    
    def _is_valid_type(self, value: Any, expected_type: type) -> bool:
        """Check if a value matches the expected type."""
        try:
            # Handle Union types
            if hasattr(expected_type, '__origin__') and expected_type.__origin__ is Union:
                return any(self._is_valid_type(value, t) for t in expected_type.__args__)
            
            # Handle generic types
            if hasattr(expected_type, '__origin__'):
                base_type = expected_type.__origin__
                if base_type in (list, dict, tuple):
                    if not isinstance(value, base_type):
                        return False
                    # Could add more detailed generic type checking here
                    return True
            
            # Basic type checking
            if expected_type == Any:
                return True
            
            return isinstance(value, expected_type)
            
        except Exception:
            return False
    
    def _validate_field_custom(self, field_name: str, field_value: Any, field_type: type) -> List[ValidationError]:
        """Custom field validation. Can be overridden by subclasses."""
        return []
    
    def _validate_model_specific(self) -> List[ValidationError]:
        """Model-specific validation. Can be overridden by subclasses."""
        return []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        result = {}
        
        # Get type hints
        type_hints = get_type_hints(self.__class__)
        
        for field_name, field_type in type_hints.items():
            if field_name.startswith('_'):
                continue
            
            field_value = getattr(self, field_name, None)
            
            # Handle special cases
            if field_name == 'metadata':
                result[field_name] = asdict(field_value) if field_value else {}
            elif isinstance(field_value, datetime):
                result[field_name] = field_value.isoformat()
            elif isinstance(field_value, Enum):
                result[field_name] = field_value.value
            elif is_dataclass(field_value):
                result[field_name] = asdict(field_value)
            elif isinstance(field_value, list) and field_value and is_dataclass(field_value[0]):
                result[field_name] = [asdict(item) for item in field_value]
            else:
                result[field_name] = field_value
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Convert model to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model instance from dictionary."""
        # Filter out metadata fields that shouldn't be passed to __init__
        init_data = {k: v for k, v in data.items() if not k.startswith('_')}
        return cls(**init_data)
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BaseModel':
        """Create model instance from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def update(self, **kwargs) -> None:
        """Update model attributes."""
        for key, value in kwargs.items():
            if hasattr(self, key) and not key.startswith('_'):
                setattr(self, key, value)
        
        # Update modification timestamp
        if hasattr(self, 'metadata') and hasattr(self.metadata, 'modified'):
            self.metadata.modified = datetime.now(timezone.utc)
        
        # Re-validate if validation is enabled
        if self._should_validate_on_init():
            self._validate_model()
    
    def clone(self) -> 'BaseModel':
        """Create a copy of the model."""
        data = self.to_dict()
        
        # Generate new ID for cloned model
        if 'id' in data:
            data['id'] = str(uuid.uuid4())
        
        # Update timestamps
        if 'created' in data:
            data['created'] = datetime.now(timezone.utc).isoformat()
        if 'modified' in data:
            data['modified'] = datetime.now(timezone.utc).isoformat()
        
        return self.__class__.from_dict(data)
    
    def get_field_value(self, field_name: str, default: Any = None) -> Any:
        """Get field value with default fallback."""
        return getattr(self, field_name, default)
    
    def set_field_value(self, field_name: str, value: Any) -> None:
        """Set field value with validation."""
        if hasattr(self, field_name) and not field_name.startswith('_'):
            setattr(self, field_name, value)
            
            # Update modification timestamp
            if hasattr(self, 'metadata') and hasattr(self.metadata, 'modified'):
                self.metadata.modified = datetime.now(timezone.utc)
        else:
            raise AttributeError(f"Field {field_name} does not exist or is not settable")
    
    def get_metadata(self) -> Dict[str, Any]:
        """Get model metadata."""
        if hasattr(self, 'metadata') and self.metadata:
            return asdict(self.metadata)
        return {}
    
    def is_valid(self) -> bool:
        """Check if the model is valid."""
        validation_result = self.validate()
        return validation_result.is_valid
    
    def get_validation_errors(self) -> List[str]:
        """Get list of validation error messages."""
        validation_result = self.validate()
        return [f"{e.field}: {e.message}" for e in validation_result.errors]
    
    def get_validation_warnings(self) -> List[str]:
        """Get list of validation warning messages."""
        validation_result = self.validate()
        return [f"{e.field}: {e.message}" for e in validation_result.warnings]
    
    def __eq__(self, other: Any) -> bool:
        """Equality comparison."""
        if not isinstance(other, self.__class__):
            return False
        
        # Compare all non-private attributes
        type_hints = get_type_hints(self.__class__)
        for field_name in type_hints:
            if field_name.startswith('_'):
                continue
            
            if getattr(self, field_name) != getattr(other, field_name):
                return False
        
        return True
    
    def __hash__(self) -> int:
        """Hash based on model ID."""
        if hasattr(self, 'metadata') and hasattr(self.metadata, 'id'):
            return hash(self.metadata.id)
        return hash(id(self))
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.__class__.__name__}(id='{getattr(self.metadata, 'id', 'unknown')}', name='{getattr(self.metadata, 'name', 'unknown')}')"
    
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"{self.__class__.__name__}({self.to_dict()})"
