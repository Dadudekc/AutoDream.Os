"""
Integration Models
=================

Data models for integration coordination.
V2 Compliance: < 300 lines, single responsibility, data modeling.

Author: Agent-3 - Infrastructure & DevOps Specialist
Mission: V2 Compliance Refactoring
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union
from datetime import datetime
from enum import Enum


class IntegrationType(Enum):
    """Types of system integrations."""
    MESSAGING = "messaging"
    VECTOR_DATABASE = "vector_database"
    VALIDATION = "validation"
    LOGGING = "logging"
    CACHING = "caching"
    MONITORING = "monitoring"


class OptimizationLevel(Enum):
    """Optimization levels."""
    NONE = "none"
    BASIC = "basic"
    ADVANCED = "advanced"
    MAXIMUM = "maximum"


class IntegrationStatus(Enum):
    """Integration status states."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    OPTIMIZING = "optimizing"
    MAINTENANCE = "maintenance"


@dataclass
class IntegrationMetrics:
    """Integration performance metrics."""
    integration_type: IntegrationType
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    max_response_time: float = 0.0
    min_response_time: float = 0.0
    throughput: float = 0.0
    error_rate: float = 0.0
    last_updated: datetime = None


@dataclass
class OptimizationConfig:
    """Configuration for integration optimization."""
    integration_type: IntegrationType
    optimization_level: OptimizationLevel
    target_response_time: float = 1.0
    max_concurrent_requests: int = 100
    cache_enabled: bool = True
    monitoring_enabled: bool = True
    auto_optimize: bool = False


@dataclass
class PerformanceReport:
    """Performance report for integration."""
    integration_type: IntegrationType
    metrics: IntegrationMetrics
    optimization_potential: float
    recommendations: List[str]
    generated_at: datetime


@dataclass
class OptimizationRecommendation:
    """Recommendation for integration optimization."""
    integration_type: IntegrationType
    recommendation_type: str
    description: str
    expected_improvement: float
    priority: int
    implementation_cost: str


@dataclass
class IntegrationConfig:
    """Configuration for integration coordinator."""
    max_concurrent_integrations: int = 10
    optimization_interval: int = 300  # 5 minutes
    monitoring_interval: int = 60  # 1 minute
    auto_optimize: bool = True
    performance_threshold: float = 0.8
    error_threshold: float = 0.1


@dataclass
class IntegrationTask:
    """Task for integration coordination."""
    task_id: str
    integration_type: IntegrationType
    operation: str
    data: Any
    priority: int = 1
    timeout: int = 30
    created_at: datetime = None
    status: IntegrationStatus = IntegrationStatus.ACTIVE


class IntegrationModels:
    """Integration models and validation."""
    
    @staticmethod
    def create_integration_metrics(integration_type: IntegrationType) -> IntegrationMetrics:
        """Create integration metrics."""
        return IntegrationMetrics(
            integration_type=integration_type,
            total_requests=0,
            successful_requests=0,
            failed_requests=0,
            average_response_time=0.0,
            max_response_time=0.0,
            min_response_time=0.0,
            throughput=0.0,
            error_rate=0.0,
            last_updated=datetime.now()
        )
    
    @staticmethod
    def create_optimization_config(
        integration_type: IntegrationType,
        optimization_level: OptimizationLevel = OptimizationLevel.BASIC,
        target_response_time: float = 1.0,
        max_concurrent_requests: int = 100,
        cache_enabled: bool = True,
        monitoring_enabled: bool = True,
        auto_optimize: bool = False
    ) -> OptimizationConfig:
        """Create optimization configuration."""
        return OptimizationConfig(
            integration_type=integration_type,
            optimization_level=optimization_level,
            target_response_time=target_response_time,
            max_concurrent_requests=max_concurrent_requests,
            cache_enabled=cache_enabled,
            monitoring_enabled=monitoring_enabled,
            auto_optimize=auto_optimize
        )
    
    @staticmethod
    def create_performance_report(
        integration_type: IntegrationType,
        metrics: IntegrationMetrics,
        optimization_potential: float,
        recommendations: List[str]
    ) -> PerformanceReport:
        """Create performance report."""
        return PerformanceReport(
            integration_type=integration_type,
            metrics=metrics,
            optimization_potential=optimization_potential,
            recommendations=recommendations,
            generated_at=datetime.now()
        )
    
    @staticmethod
    def create_optimization_recommendation(
        integration_type: IntegrationType,
        recommendation_type: str,
        description: str,
        expected_improvement: float,
        priority: int = 1,
        implementation_cost: str = "low"
    ) -> OptimizationRecommendation:
        """Create optimization recommendation."""
        return OptimizationRecommendation(
            integration_type=integration_type,
            recommendation_type=recommendation_type,
            description=description,
            expected_improvement=expected_improvement,
            priority=priority,
            implementation_cost=implementation_cost
        )
    
    @staticmethod
    def create_integration_config(
        max_concurrent_integrations: int = 10,
        optimization_interval: int = 300,
        monitoring_interval: int = 60,
        auto_optimize: bool = True,
        performance_threshold: float = 0.8,
        error_threshold: float = 0.1
    ) -> IntegrationConfig:
        """Create integration configuration."""
        return IntegrationConfig(
            max_concurrent_integrations=max_concurrent_integrations,
            optimization_interval=optimization_interval,
            monitoring_interval=monitoring_interval,
            auto_optimize=auto_optimize,
            performance_threshold=performance_threshold,
            error_threshold=error_threshold
        )
    
    @staticmethod
    def create_integration_task(
        task_id: str,
        integration_type: IntegrationType,
        operation: str,
        data: Any,
        priority: int = 1,
        timeout: int = 30
    ) -> IntegrationTask:
        """Create integration task."""
        return IntegrationTask(
            task_id=task_id,
            integration_type=integration_type,
            operation=operation,
            data=data,
            priority=priority,
            timeout=timeout,
            created_at=datetime.now(),
            status=IntegrationStatus.ACTIVE
        )
    
    @staticmethod
    def update_metrics(
        metrics: IntegrationMetrics,
        response_time: float,
        success: bool
    ) -> IntegrationMetrics:
        """Update integration metrics."""
        metrics.total_requests += 1
        
        if success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1
        
        # Update response time statistics
        if metrics.total_requests == 1:
            metrics.average_response_time = response_time
            metrics.max_response_time = response_time
            metrics.min_response_time = response_time
        else:
            # Update average
            total_time = metrics.average_response_time * (metrics.total_requests - 1)
            metrics.average_response_time = (total_time + response_time) / metrics.total_requests
            
            # Update min/max
            metrics.max_response_time = max(metrics.max_response_time, response_time)
            metrics.min_response_time = min(metrics.min_response_time, response_time)
        
        # Update error rate
        metrics.error_rate = metrics.failed_requests / metrics.total_requests
        
        # Update throughput (requests per second)
        if metrics.average_response_time > 0:
            metrics.throughput = 1.0 / metrics.average_response_time
        
        metrics.last_updated = datetime.now()
        return metrics
    
    @staticmethod
    def calculate_optimization_potential(metrics: IntegrationMetrics) -> float:
        """Calculate optimization potential score."""
        if metrics.total_requests == 0:
            return 0.0
        
        # Base score from error rate
        error_score = 1.0 - metrics.error_rate
        
        # Response time score (lower is better)
        response_time_score = max(0.0, 1.0 - (metrics.average_response_time / 5.0))
        
        # Throughput score (higher is better)
        throughput_score = min(1.0, metrics.throughput / 10.0)
        
        # Weighted average
        optimization_potential = (
            error_score * 0.4 +
            response_time_score * 0.4 +
            throughput_score * 0.2
        )
        
        return min(1.0, max(0.0, optimization_potential))
    
    @staticmethod
    def generate_recommendations(metrics: IntegrationMetrics) -> List[str]:
        """Generate optimization recommendations."""
        recommendations = []
        
        if metrics.error_rate > 0.1:  # 10%
            recommendations.append("High error rate detected. Review error handling and retry logic.")
        
        if metrics.average_response_time > 2.0:  # 2 seconds
            recommendations.append("Slow response time. Consider caching or performance optimization.")
        
        if metrics.throughput < 1.0:  # Less than 1 request per second
            recommendations.append("Low throughput. Consider parallel processing or resource scaling.")
        
        if metrics.max_response_time > 10.0:  # 10 seconds
            recommendations.append("Very slow requests detected. Investigate timeout issues.")
        
        if not recommendations:
            recommendations.append("Performance metrics look good. Continue monitoring.")
        
        return recommendations
