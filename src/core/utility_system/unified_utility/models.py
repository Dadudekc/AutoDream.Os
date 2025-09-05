"""
Utility System Models
====================

Data models for utility system operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class UtilityOperationType(Enum):
    """Types of utility operations."""
    CACHE_OPERATION = "cache_operation"
    VALIDATION_OPERATION = "validation_operation"
    TRANSFORMATION_OPERATION = "transformation_operation"
    COORDINATION_OPERATION = "coordination_operation"
    METRICS_OPERATION = "metrics_operation"


class UtilityStatus(Enum):
    """Utility system status."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    MAINTENANCE = "maintenance"


@dataclass
class UtilityConfig:
    """Configuration for utility system."""
    cache_enabled: bool = True
    validation_enabled: bool = True
    transformation_enabled: bool = True
    coordination_enabled: bool = True
    metrics_enabled: bool = True
    max_cache_size: int = 1000
    cache_ttl_seconds: int = 3600
    validation_timeout_seconds: int = 30
    transformation_timeout_seconds: int = 60
    coordination_timeout_seconds: int = 120
    metrics_collection_interval: int = 300


@dataclass
class UtilityMetrics:
    """Utility system metrics."""
    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    validation_successes: int = 0
    validation_failures: int = 0
    transformation_successes: int = 0
    transformation_failures: int = 0
    coordination_successes: int = 0
    coordination_failures: int = 0
    average_response_time: float = 0.0
    last_updated: datetime = None


@dataclass
class UtilityOperation:
    """Individual utility operation."""
    operation_id: str
    operation_type: UtilityOperationType
    input_data: Any
    output_data: Any = None
    status: UtilityStatus = UtilityStatus.ACTIVE
    start_time: datetime = None
    end_time: datetime = None
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class UtilityResult:
    """Result of utility operation."""
    success: bool
    data: Any = None
    error_message: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None


class UtilitySystemModels:
    """Utility system models and validation."""
    
    @staticmethod
    def create_utility_config(
        cache_enabled: bool = True,
        validation_enabled: bool = True,
        transformation_enabled: bool = True,
        coordination_enabled: bool = True,
        metrics_enabled: bool = True,
        max_cache_size: int = 1000,
        cache_ttl_seconds: int = 3600,
        validation_timeout_seconds: int = 30,
        transformation_timeout_seconds: int = 60,
        coordination_timeout_seconds: int = 120,
        metrics_collection_interval: int = 300
    ) -> UtilityConfig:
        """Create utility configuration."""
        return UtilityConfig(
            cache_enabled=cache_enabled,
            validation_enabled=validation_enabled,
            transformation_enabled=transformation_enabled,
            coordination_enabled=coordination_enabled,
            metrics_enabled=metrics_enabled,
            max_cache_size=max_cache_size,
            cache_ttl_seconds=cache_ttl_seconds,
            validation_timeout_seconds=validation_timeout_seconds,
            transformation_timeout_seconds=transformation_timeout_seconds,
            coordination_timeout_seconds=coordination_timeout_seconds,
            metrics_collection_interval=metrics_collection_interval
        )
    
    @staticmethod
    def create_utility_metrics() -> UtilityMetrics:
        """Create utility metrics."""
        return UtilityMetrics(
            total_operations=0,
            successful_operations=0,
            failed_operations=0,
            cache_hits=0,
            cache_misses=0,
            validation_successes=0,
            validation_failures=0,
            transformation_successes=0,
            transformation_failures=0,
            coordination_successes=0,
            coordination_failures=0,
            average_response_time=0.0,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_utility_operation(
        operation_id: str,
        operation_type: UtilityOperationType,
        input_data: Any,
        metadata: Dict[str, Any] = None
    ) -> UtilityOperation:
        """Create utility operation."""
        return UtilityOperation(
            operation_id=operation_id,
            operation_type=operation_type,
            input_data=input_data,
            status=UtilityStatus.ACTIVE,
            start_time=datetime.now(),
            metadata=metadata or {}
        )
    
    @staticmethod
    def create_utility_result(
        success: bool,
        data: Any = None,
        error_message: str = None,
        execution_time: float = 0.0,
        metadata: Dict[str, Any] = None
    ) -> UtilityResult:
        """Create utility result."""
        return UtilityResult(
            success=success,
            data=data,
            error_message=error_message,
            execution_time=execution_time,
            metadata=metadata or {}
        )
    
    @staticmethod
    def update_metrics(
        metrics: UtilityMetrics,
        operation_type: UtilityOperationType,
        success: bool,
        execution_time: float
    ) -> UtilityMetrics:
        """Update utility metrics."""
        metrics.total_operations += 1
        
        if success:
            metrics.successful_operations += 1
            
            if operation_type == UtilityOperationType.CACHE_OPERATION:
                metrics.cache_hits += 1
            elif operation_type == UtilityOperationType.VALIDATION_OPERATION:
                metrics.validation_successes += 1
            elif operation_type == UtilityOperationType.TRANSFORMATION_OPERATION:
                metrics.transformation_successes += 1
            elif operation_type == UtilityOperationType.COORDINATION_OPERATION:
                metrics.coordination_successes += 1
        else:
            metrics.failed_operations += 1
            
            if operation_type == UtilityOperationType.CACHE_OPERATION:
                metrics.cache_misses += 1
            elif operation_type == UtilityOperationType.VALIDATION_OPERATION:
                metrics.validation_failures += 1
            elif operation_type == UtilityOperationType.TRANSFORMATION_OPERATION:
                metrics.transformation_failures += 1
            elif operation_type == UtilityOperationType.COORDINATION_OPERATION:
                metrics.coordination_failures += 1
        
        # Update average response time
        total_time = metrics.average_response_time * (metrics.total_operations - 1) + execution_time
        metrics.average_response_time = total_time / metrics.total_operations
        
        metrics.last_updated = datetime.now()
        return metrics
