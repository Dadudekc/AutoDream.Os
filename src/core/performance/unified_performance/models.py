"""
Performance Models
=================

Data models for performance optimization operations.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from enum import Enum
import uuid


class OptimizationType(Enum):
    """Optimization types."""
    MEMORY = "memory"
    CPU = "cpu"
    I_O = "i_o"
    NETWORK = "network"
    CACHE = "cache"
    DATABASE = "database"


class OptimizationStatus(Enum):
    """Optimization status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OptimizationPriority(Enum):
    """Optimization priority."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class OptimizationRule:
    """Performance optimization rule."""
    rule_id: str
    name: str
    description: str
    optimization_type: OptimizationType
    condition: Callable[[Dict[str, Any]], bool]
    action: Callable[[Dict[str, Any]], bool]
    priority: OptimizationPriority
    enabled: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class OptimizationResult:
    """Optimization result."""
    result_id: str
    rule_id: str
    status: OptimizationStatus
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None
    success: bool = False
    error_message: Optional[str] = None
    metrics_before: Dict[str, Any] = None
    metrics_after: Dict[str, Any] = None
    improvement_percentage: Optional[float] = None
    
    def __post_init__(self):
        if self.end_time and self.start_time:
            self.duration = (self.end_time - self.start_time).total_seconds()
            if self.metrics_before and self.metrics_after:
                self.calculate_improvement()


@dataclass
class PerformanceMetrics:
    """Performance metrics."""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_usage: float
    response_time: float
    throughput: float
    error_rate: float
    active_connections: int
    queue_size: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'cpu_usage': self.cpu_usage,
            'memory_usage': self.memory_usage,
            'disk_usage': self.disk_usage,
            'network_usage': self.network_usage,
            'response_time': self.response_time,
            'throughput': self.throughput,
            'error_rate': self.error_rate,
            'active_connections': self.active_connections,
            'queue_size': self.queue_size
        }


@dataclass
class OptimizationConfig:
    """Optimization configuration."""
    config_id: str
    name: str
    description: str
    enabled: bool = True
    max_concurrent_optimizations: int = 3
    optimization_timeout: int = 300  # seconds
    metrics_collection_interval: int = 60  # seconds
    auto_optimization_enabled: bool = True
    notification_enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()


class PerformanceModels:
    """Performance models and validation."""
    
    @staticmethod
    def create_optimization_rule(
        name: str,
        description: str,
        optimization_type: OptimizationType,
        condition: Callable[[Dict[str, Any]], bool],
        action: Callable[[Dict[str, Any]], bool],
        priority: OptimizationPriority = OptimizationPriority.MEDIUM
    ) -> OptimizationRule:
        """Create optimization rule."""
        return OptimizationRule(
            rule_id=str(uuid.uuid4()),
            name=name,
            description=description,
            optimization_type=optimization_type,
            condition=condition,
            action=action,
            priority=priority
        )
    
    @staticmethod
    def create_optimization_result(
        rule_id: str,
        status: OptimizationStatus,
        start_time: datetime,
        metrics_before: Dict[str, Any] = None
    ) -> OptimizationResult:
        """Create optimization result."""
        return OptimizationResult(
            result_id=str(uuid.uuid4()),
            rule_id=rule_id,
            status=status,
            start_time=start_time,
            metrics_before=metrics_before or {}
        )
    
    @staticmethod
    def create_performance_metrics(
        cpu_usage: float,
        memory_usage: float,
        disk_usage: float,
        network_usage: float,
        response_time: float,
        throughput: float,
        error_rate: float,
        active_connections: int,
        queue_size: int
    ) -> PerformanceMetrics:
        """Create performance metrics."""
        return PerformanceMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_usage,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            network_usage=network_usage,
            response_time=response_time,
            throughput=throughput,
            error_rate=error_rate,
            active_connections=active_connections,
            queue_size=queue_size
        )
    
    @staticmethod
    def create_optimization_config(
        name: str,
        description: str,
        enabled: bool = True,
        max_concurrent_optimizations: int = 3,
        optimization_timeout: int = 300,
        metrics_collection_interval: int = 60,
        auto_optimization_enabled: bool = True,
        notification_enabled: bool = True
    ) -> OptimizationConfig:
        """Create optimization config."""
        return OptimizationConfig(
            config_id=str(uuid.uuid4()),
            name=name,
            description=description,
            enabled=enabled,
            max_concurrent_optimizations=max_concurrent_optimizations,
            optimization_timeout=optimization_timeout,
            metrics_collection_interval=metrics_collection_interval,
            auto_optimization_enabled=auto_optimization_enabled,
            notification_enabled=notification_enabled
        )
    
    @staticmethod
    def validate_optimization_rule(rule: OptimizationRule) -> Dict[str, Any]:
        """Validate optimization rule."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check required fields
        if not rule.name:
            validation['errors'].append("Rule name is required")
            validation['is_valid'] = False
        
        if not rule.description:
            validation['warnings'].append("Rule description is recommended")
        
        if not callable(rule.condition):
            validation['errors'].append("Rule condition must be callable")
            validation['is_valid'] = False
        
        if not callable(rule.action):
            validation['errors'].append("Rule action must be callable")
            validation['is_valid'] = False
        
        return validation
    
    @staticmethod
    def validate_performance_metrics(metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Validate performance metrics."""
        validation = {
            'is_valid': True,
            'warnings': [],
            'errors': []
        }
        
        # Check value ranges
        if not 0.0 <= metrics.cpu_usage <= 100.0:
            validation['warnings'].append("CPU usage should be between 0-100%")
        
        if not 0.0 <= metrics.memory_usage <= 100.0:
            validation['warnings'].append("Memory usage should be between 0-100%")
        
        if not 0.0 <= metrics.disk_usage <= 100.0:
            validation['warnings'].append("Disk usage should be between 0-100%")
        
        if metrics.response_time < 0:
            validation['errors'].append("Response time cannot be negative")
            validation['is_valid'] = False
        
        if metrics.throughput < 0:
            validation['errors'].append("Throughput cannot be negative")
            validation['is_valid'] = False
        
        if not 0.0 <= metrics.error_rate <= 100.0:
            validation['warnings'].append("Error rate should be between 0-100%")
        
        return validation
