"""
Performance Optimization Framework - V2 Compliant (Simplified)
=============================================================

Core performance optimization with essential functionality only.
Eliminates overcomplexity while maintaining core features.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Integration Specialist)
License: MIT
"""
import logging
import threading
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class OptimizationLevel(Enum):
    """Optimization level enumeration."""

    BASIC = "basic"
    ENHANCED = "enhanced"
    ADVANCED = "advanced"


@dataclass
class OptimizationMetric:
    """Optimization metric structure."""

    name: str
    value: float
    target_value: float
    level: OptimizationLevel
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class OptimizationResult:
    """Optimization result structure."""

    success: bool
    metric_name: str
    old_value: float
    new_value: float
    improvement: float
    message: str
    timestamp: datetime = field(default_factory=datetime.now)


class PerformanceOptimizer:
    """Core performance optimizer."""

    def __init__(self):
        self._metrics: dict[str, OptimizationMetric] = {}
        self._results: list[OptimizationResult] = []
        self._lock = threading.Lock()

    def add_metric(self, name: str, value: float, target: float, level: OptimizationLevel) -> None:
        """Add an optimization metric."""
        with self._lock:
            self._metrics[name] = OptimizationMetric(
                name=name, value=value, target_value=target, level=level
            )
            logger.debug(f"Metric added: {name}")

    def update_metric(self, name: str, value: float) -> None:
        """Update a metric value."""
        with self._lock:
            if name in self._metrics:
                self._metrics[name].value = value
                self._metrics[name].timestamp = datetime.now()
                logger.debug(f"Metric updated: {name} = {value}")

    def get_metric(self, name: str) -> OptimizationMetric | None:
        """Get a metric."""
        return self._metrics.get(name)

    def get_all_metrics(self) -> dict[str, OptimizationMetric]:
        """Get all metrics."""
        return self._metrics.copy()

    def optimize_metric(self, name: str, new_value: float) -> OptimizationResult:
        """Optimize a metric."""
        with self._lock:
            if name not in self._metrics:
                result = OptimizationResult(
                    success=False,
                    metric_name=name,
                    old_value=0.0,
                    new_value=new_value,
                    improvement=0.0,
                    message=f"Metric {name} not found",
                )
                self._results.append(result)
                return result

            metric = self._metrics[name]
            old_value = metric.value
            improvement = new_value - old_value

            metric.value = new_value
            metric.timestamp = datetime.now()

            result = OptimizationResult(
                success=True,
                metric_name=name,
                old_value=old_value,
                new_value=new_value,
                improvement=improvement,
                message=f"Metric {name} optimized from {old_value} to {new_value}",
            )

            self._results.append(result)
            logger.info(f"Metric optimized: {name} ({old_value} → {new_value})")
            return result

    def get_optimization_results(self) -> list[OptimizationResult]:
        """Get all optimization results."""
        return self._results.copy()

    def get_metrics_needing_optimization(self) -> list[str]:
        """Get metrics that need optimization."""
        return [
            name for name, metric in self._metrics.items() if metric.value < metric.target_value
        ]


class ResourceOptimizer:
    """Resource optimization manager."""

    def __init__(self):
        self._resource_usage: dict[str, float] = {}
        self._limits: dict[str, float] = {}
        self._lock = threading.Lock()

    def set_resource_limit(self, resource: str, limit: float) -> None:
        """Set a resource limit."""
        with self._lock:
            self._limits[resource] = limit
            logger.debug(f"Resource limit set: {resource} = {limit}")

    def update_resource_usage(self, resource: str, usage: float) -> None:
        """Update resource usage."""
        with self._lock:
            self._resource_usage[resource] = usage
            logger.debug(f"Resource usage updated: {resource} = {usage}")

    def get_resource_usage(self, resource: str) -> float:
        """Get resource usage."""
        return self._resource_usage.get(resource, 0.0)

    def get_resource_limit(self, resource: str) -> float:
        """Get resource limit."""
        return self._limits.get(resource, 0.0)

    def is_resource_over_limit(self, resource: str) -> bool:
        """Check if resource is over limit."""
        usage = self.get_resource_usage(resource)
        limit = self.get_resource_limit(resource)
        return usage > limit if limit > 0 else False

    def get_over_limit_resources(self) -> list[str]:
        """Get resources that are over limit."""
        return [
            resource
            for resource in self._resource_usage.keys()
            if self.is_resource_over_limit(resource)
        ]

    def optimize_resource_usage(self, resource: str, target_usage: float) -> bool:
        """Optimize resource usage."""
        with self._lock:
            if resource in self._resource_usage:
                old_usage = self._resource_usage[resource]
                self._resource_usage[resource] = target_usage
                logger.info(f"Resource optimized: {resource} ({old_usage} → {target_usage})")
                return True
            return False


class BottleneckAnalyzer:
    """Bottleneck analysis system."""

    def __init__(self):
        self._bottlenecks: dict[str, dict[str, Any]] = {}
        self._lock = threading.Lock()

    def identify_bottleneck(
        self, component: str, metric: str, value: float, threshold: float
    ) -> None:
        """Identify a bottleneck."""
        with self._lock:
            if component not in self._bottlenecks:
                self._bottlenecks[component] = {}

            self._bottlenecks[component][metric] = {
                "value": value,
                "threshold": threshold,
                "severity": "high"
                if value > threshold * 1.5
                else "medium"
                if value > threshold
                else "low",
                "timestamp": datetime.now(),
            }
            logger.warning(
                f"Bottleneck identified: {component}.{metric} = {value} (threshold: {threshold})"
            )

    def get_bottlenecks(self, component: str | None = None) -> dict[str, dict[str, Any]]:
        """Get bottlenecks."""
        if component:
            return {component: self._bottlenecks.get(component, {})}
        return self._bottlenecks.copy()

    def clear_bottlenecks(self, component: str | None = None) -> None:
        """Clear bottlenecks."""
        with self._lock:
            if component:
                if component in self._bottlenecks:
                    del self._bottlenecks[component]
                    logger.info(f"Bottlenecks cleared for component: {component}")
            else:
                self._bottlenecks.clear()
                logger.info("All bottlenecks cleared")

    def get_high_severity_bottlenecks(self) -> dict[str, dict[str, Any]]:
        """Get high severity bottlenecks."""
        high_severity = {}
        for component, metrics in self._bottlenecks.items():
            high_metrics = {
                metric: data for metric, data in metrics.items() if data.get("severity") == "high"
            }
            if high_metrics:
                high_severity[component] = high_metrics
        return high_severity


class OptimizationEngine:
    """Main optimization engine."""

    def __init__(self):
        self._performance_optimizer = PerformanceOptimizer()
        self._resource_optimizer = ResourceOptimizer()
        self._bottleneck_analyzer = BottleneckAnalyzer()
        self._enabled = True

    def enable(self) -> None:
        """Enable optimization engine."""
        self._enabled = True
        logger.info("Optimization engine enabled")

    def disable(self) -> None:
        """Disable optimization engine."""
        self._enabled = False
        logger.info("Optimization engine disabled")

    def is_enabled(self) -> bool:
        """Check if optimization engine is enabled."""
        return self._enabled

    def get_performance_optimizer(self) -> PerformanceOptimizer:
        """Get performance optimizer."""
        return self._performance_optimizer

    def get_resource_optimizer(self) -> ResourceOptimizer:
        """Get resource optimizer."""
        return self._resource_optimizer

    def get_bottleneck_analyzer(self) -> BottleneckAnalyzer:
        """Get bottleneck analyzer."""
        return self._bottleneck_analyzer

    def run_optimization_cycle(self) -> dict[str, Any]:
        """Run a complete optimization cycle."""
        if not self._enabled:
            return {"success": False, "message": "Optimization engine disabled"}

        results = {
            "success": True,
            "timestamp": datetime.now(),
            "performance_optimizations": [],
            "resource_optimizations": [],
            "bottlenecks_identified": 0,
        }

        # Performance optimizations
        metrics_needing_optimization = (
            self._performance_optimizer.get_metrics_needing_optimization()
        )
        for metric_name in metrics_needing_optimization:
            metric = self._performance_optimizer.get_metric(metric_name)
            if metric:
                # Simple optimization: move towards target
                new_value = min(metric.value * 1.1, metric.target_value)
                result = self._performance_optimizer.optimize_metric(metric_name, new_value)
                results["performance_optimizations"].append(result)

        # Resource optimizations
        over_limit_resources = self._resource_optimizer.get_over_limit_resources()
        for resource in over_limit_resources:
            current_usage = self._resource_optimizer.get_resource_usage(resource)
            target_usage = current_usage * 0.9  # Reduce by 10%
            success = self._resource_optimizer.optimize_resource_usage(resource, target_usage)
            results["resource_optimizations"].append(
                {
                    "resource": resource,
                    "success": success,
                    "old_usage": current_usage,
                    "new_usage": target_usage,
                }
            )

        # Bottleneck analysis
        bottlenecks = self._bottleneck_analyzer.get_bottlenecks()
        results["bottlenecks_identified"] = sum(len(metrics) for metrics in bottlenecks.values())

        logger.info(
            f"Optimization cycle completed: {len(results['performance_optimizations'])} performance, {len(results['resource_optimizations'])} resource optimizations"
        )
        return results


# Global optimization engine
optimization_engine = OptimizationEngine()


def get_optimization_engine() -> OptimizationEngine:
    """Get the global optimization engine."""
    return optimization_engine


def run_optimization() -> dict[str, Any]:
    """Run optimization cycle."""
    return optimization_engine.run_optimization_cycle()
