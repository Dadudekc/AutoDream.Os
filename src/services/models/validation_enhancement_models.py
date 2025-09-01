"""
Validation Enhancement Models

Data models and enums for CLI validation enhancement system.

Author: Agent-3 - Infrastructure & DevOps Specialist
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional

from ..validation_models import ValidationError, ValidationResult, ValidationExitCodes


class ValidationStrategy(Enum):
    """Validation strategy types."""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    PIPELINE = "pipeline"
    CACHED = "cached"


class ValidationPriority(Enum):
    """Validation priority levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationMetrics:
    """Validation performance metrics."""
    validation_time_ms: float
    memory_usage_mb: float
    cache_hit_rate: float
    error_count: int
    success_count: int
    timestamp: datetime


@dataclass
class ValidationContext:
    """Context for validation operations."""
    request_id: str
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    priority: ValidationPriority = ValidationPriority.MEDIUM
    strategy: ValidationStrategy = ValidationStrategy.SEQUENTIAL
    timeout_seconds: float = 30.0
    metadata: Dict[str, Any] = field(default_factory=dict)
