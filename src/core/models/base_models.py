#!/usr/bin/env python3
"""
Base Models Module - Agent Cellphone V2

Provides base model classes with common functionality for all
unified models in the consolidated framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime
import uuid
import json

try:
    from src.core.models.unified_enums import UnifiedStatus, UnifiedType, UnifiedFormat
except ImportError:
    from unified_enums import UnifiedStatus, UnifiedType, UnifiedFormat

logger = logging.getLogger(__name__)

# ============================================================================
# BASE MODEL CLASSES - Foundation for all unified models
# ============================================================================

@dataclass
class BaseModel:
    """Base model with common functionality for all models"""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: str = "1.0.0"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Post-initialization setup"""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now()
        if not self.updated_at:
            self.updated_at = datetime.now()
    
    def update_timestamp(self) -> None:
        """Update the timestamp to current time"""
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        data = asdict(self)
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        return data
    
    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.to_dict(), indent=2, default=str)
    
    def update_metadata(self, key: str, value: Any) -> None:
        """Update metadata with new key-value pair"""
        self.metadata[key] = value
        self.update_timestamp()
    
    def get_metadata(self, key: str, default: Any = None) -> Any:
        """Get metadata value by key"""
        return self.metadata.get(key, default)
    
    def validate(self) -> bool:
        """Basic validation for the model"""
        try:
            if not self.id:
                return False
            if not isinstance(self.created_at, datetime):
                return False
            if not isinstance(self.updated_at, datetime):
                return False
            return True
        except Exception:
            return False


@dataclass
class StatusModel(BaseModel):
    """Base model with status tracking capabilities"""
    
    status: UnifiedStatus = UnifiedStatus.PENDING
    status_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def update_status(self, new_status: UnifiedStatus, reason: str = None) -> None:
        """Update status and record in history"""
        old_status = self.status
        self.status = new_status
        self.update_timestamp()
        
        # Record status change
        status_record = {
            "timestamp": datetime.now().isoformat(),
            "old_status": old_status.value,
            "new_status": new_status.value,
            "reason": reason
        }
        self.status_history.append(status_record)
    
    def is_active(self) -> bool:
        """Check if model is in active state"""
        return self.status in [UnifiedStatus.ACTIVE, UnifiedStatus.RUNNING, UnifiedStatus.IN_PROGRESS]
    
    def is_completed(self) -> bool:
        """Check if model is in completed state"""
        return self.status in [UnifiedStatus.COMPLETED, UnifiedStatus.SUCCESS, UnifiedStatus.RESOLVED]
    
    def is_failed(self) -> bool:
        """Check if model is in failed state"""
        return self.status in [UnifiedStatus.FAILED, UnifiedStatus.ERROR, UnifiedStatus.CRITICAL]
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get status summary information"""
        return {
            "current_status": self.status.value,
            "is_active": self.is_active(),
            "is_completed": self.is_completed(),
            "is_failed": self.is_failed(),
            "status_changes": len(self.status_history),
            "last_change": self.status_history[-1] if self.status_history else None
        }


@dataclass
class TypedModel(BaseModel):
    """Base model with type classification capabilities"""
    
    model_type: UnifiedType = UnifiedType.DATA
    category: str = "general"
    tags: List[str] = field(default_factory=list)
    
    def add_tag(self, tag: str) -> None:
        """Add a tag to the model"""
        if tag not in self.tags:
            self.tags.append(tag)
            self.update_timestamp()
    
    def remove_tag(self, tag: str) -> bool:
        """Remove a tag from the model"""
        if tag in self.tags:
            self.tags.remove(tag)
            self.update_timestamp()
            return True
        return False
    
    def has_tag(self, tag: str) -> bool:
        """Check if model has a specific tag"""
        return tag in self.tags
    
    def get_type_info(self) -> Dict[str, Any]:
        """Get type classification information"""
        return {
            "model_type": self.model_type.value,
            "category": self.category,
            "tags": self.tags.copy(),
            "tag_count": len(self.tags)
        }


@dataclass
class ConfigurableModel(BaseModel):
    """Base model with configuration capabilities"""
    
    config: Dict[str, Any] = field(default_factory=dict)
    config_schema: Dict[str, Any] = field(default_factory=dict)
    
    def set_config(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
        self.update_timestamp()
    
    def get_config(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def remove_config(self, key: str) -> bool:
        """Remove configuration key"""
        if key in self.config:
            del self.config[key]
            self.update_timestamp()
            return True
        return False
    
    def validate_config(self) -> bool:
        """Validate configuration against schema"""
        try:
            if not self.config_schema:
                return True  # No schema means all configs are valid
            
            for key, value in self.config.items():
                if key in self.config_schema:
                    expected_type = self.config_schema[key].get('type')
                    if expected_type and not isinstance(value, expected_type):
                        return False
            return True
        except Exception:
            return False
    
    def get_config_summary(self) -> Dict[str, Any]:
        """Get configuration summary"""
        return {
            "config_keys": list(self.config.keys()),
            "config_count": len(self.config),
            "has_schema": bool(self.config_schema),
            "is_valid": self.validate_config()
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_base_model(**kwargs) -> BaseModel:
    """Create a base model with specified parameters"""
    return BaseModel(**kwargs)


def create_status_model(**kwargs) -> StatusModel:
    """Create a status model with specified parameters"""
    return StatusModel(**kwargs)


def create_typed_model(**kwargs) -> TypedModel:
    """Create a typed model with specified parameters"""
    return TypedModel(**kwargs)


def create_configurable_model(**kwargs) -> ConfigurableModel:
    """Create a configurable model with specified parameters"""
    return ConfigurableModel(**kwargs)


def validate_model_data(model: BaseModel) -> bool:
    """Validate model data integrity"""
    try:
        return model.validate()
    except Exception:
        return False


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for base models module"""
    print("🚀 BASE MODELS MODULE - TASK 3J V2 Refactoring")
    print("=" * 50)
    
    # Create example models
    base_model = create_base_model()
    status_model = create_status_model()
    typed_model = create_typed_model()
    config_model = create_configurable_model()
    
    print(f"✅ Base Model Created: {base_model.id}")
    print(f"✅ Status Model Created: {status_model.id}")
    print(f"✅ Typed Model Created: {typed_model.id}")
    print(f"✅ Config Model Created: {config_model.id}")
    
    # Test functionality
    status_model.update_status(UnifiedStatus.ACTIVE, "Model activated")
    typed_model.add_tag("example")
    config_model.set_config("timeout", 30)
    
    print(f"\n✅ Status Model Status: {status_model.status.value}")
    print(f"✅ Typed Model Tags: {typed_model.tags}")
    print(f"✅ Config Model Config: {config_model.config}")
    
    print("\n🎯 Base Models Module Ready!")
    return 0


if __name__ == "__main__":
    exit(main())
