#!/usr/bin/env python3
"""
Health & Performance Models Module - Agent Cellphone V2

Provides health monitoring and performance tracking models
for the unified framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

try:
    from src.core.models.base_models import StatusModel, TypedModel
    from src.core.models.unified_enums import UnifiedStatus, UnifiedType
except ImportError:
    from base_models import StatusModel, TypedModel
    from unified_enums import UnifiedStatus, UnifiedType

logger = logging.getLogger(__name__)

# ============================================================================
# HEALTH & PERFORMANCE MODELS - Domain-specific implementations
# ============================================================================

@dataclass
class HealthModel(StatusModel, TypedModel):
    """Health monitoring model with score, metrics, and threshold checking"""
    
    health_score: float = 100.0
    metrics: Dict[str, float] = field(default_factory=dict)
    thresholds: Dict[str, Dict[str, float]] = field(default_factory=dict)
    last_check: datetime = field(default_factory=datetime.now)
    check_interval: int = 300  # seconds
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.SYSTEM
        self.category = "health"
        
        # Set default thresholds
        if not self.thresholds:
            self.thresholds = {
                "cpu_usage": {"warning": 80.0, "critical": 95.0},
                "memory_usage": {"warning": 85.0, "critical": 95.0},
                "disk_usage": {"warning": 90.0, "critical": 95.0}
            }
    
    def update_health_score(self, new_score: float) -> None:
        """Update health score and status"""
        old_score = self.health_score
        self.health_score = max(0.0, min(100.0, new_score))
        self.last_check = datetime.now()
        self.update_timestamp()
        
        # Update status based on health score
        if self.health_score >= 90.0:
            self.update_status(UnifiedStatus.HEALTHY, f"Health score: {self.health_score}")
        elif self.health_score >= 70.0:
            self.update_status(UnifiedStatus.WARNING, f"Health score: {self.health_score}")
        else:
            self.update_status(UnifiedStatus.CRITICAL, f"Health score: {self.health_score}")
        
        logger.info(f"Health score updated: {old_score} → {self.health_score}")
    
    def add_metric(self, name: str, value: float) -> None:
        """Add or update a health metric"""
        self.metrics[name] = value
        self.update_timestamp()
    
    def check_thresholds(self) -> Dict[str, str]:
        """Check all metrics against thresholds"""
        violations = {}
        
        for metric_name, metric_value in self.metrics.items():
            if metric_name in self.thresholds:
                thresholds = self.thresholds[metric_name]
                
                if metric_value >= thresholds.get("critical", float('inf')):
                    violations[metric_name] = "CRITICAL"
                elif metric_value >= thresholds.get("warning", float('inf')):
                    violations[metric_name] = "WARNING"
        
        return violations
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        threshold_violations = self.check_thresholds()
        
        return {
            "health_score": self.health_score,
            "status": self.status.value,
            "metrics_count": len(self.metrics),
            "threshold_violations": threshold_violations,
            "last_check": self.last_check.isoformat(),
            "check_interval": self.check_interval
        }


@dataclass
class PerformanceModel(StatusModel, TypedModel):
    """Performance tracking model with benchmarks and optimization targets"""
    
    performance_score: float = 0.0
    benchmarks: Dict[str, float] = field(default_factory=dict)
    targets: Dict[str, float] = field(default_factory=dict)
    optimization_history: List[Dict[str, Any]] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.SYSTEM
        self.category = "performance"
    
    def add_benchmark(self, name: str, value: float) -> None:
        """Add or update a performance benchmark"""
        self.benchmarks[name] = value
        self.update_timestamp()
        
        # Recalculate performance score
        self._calculate_performance_score()
    
    def set_target(self, name: str, target_value: float) -> None:
        """Set performance target for a benchmark"""
        self.targets[name] = target_value
        self.update_timestamp()
    
    def _calculate_performance_score(self) -> None:
        """Calculate overall performance score based on benchmarks vs targets"""
        if not self.benchmarks or not self.targets:
            return
        
        total_score = 0.0
        valid_metrics = 0
        
        for benchmark_name, benchmark_value in self.benchmarks.items():
            if benchmark_name in self.targets:
                target_value = self.targets[benchmark_name]
                if target_value > 0:
                    # Calculate percentage of target achieved
                    percentage = min(100.0, (benchmark_value / target_value) * 100)
                    total_score += percentage
                    valid_metrics += 1
        
        if valid_metrics > 0:
            self.performance_score = total_score / valid_metrics
            self.update_timestamp()
    
    def record_optimization(self, benchmark_name: str, old_value: float, new_value: float, 
                          improvement: float, method: str) -> None:
        """Record an optimization attempt"""
        optimization_record = {
            "timestamp": datetime.now().isoformat(),
            "benchmark": benchmark_name,
            "old_value": old_value,
            "new_value": new_value,
            "improvement": improvement,
            "method": method
        }
        
        self.optimization_history.append(optimization_record)
        self.update_timestamp()
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        return {
            "performance_score": self.performance_score,
            "benchmarks_count": len(self.benchmarks),
            "targets_count": len(self.targets),
            "optimizations_count": len(self.optimization_history),
            "recent_optimizations": self.optimization_history[-5:] if self.optimization_history else []
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_health_model(**kwargs) -> HealthModel:
    """Create a health model with specified parameters"""
    return HealthModel(**kwargs)


def create_performance_model(**kwargs) -> PerformanceModel:
    """Create a performance model with specified parameters"""
    return PerformanceModel(**kwargs)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for health & performance models module"""
    print("🚀 HEALTH & PERFORMANCE MODELS MODULE - TASK 3J V2 Refactoring")
    print("=" * 60)
    
    # Create example models
    health_model = create_health_model(health_score=95.0)
    performance_model = create_performance_model()
    
    print(f"✅ Health Model Created: {health_model.id}")
    print(f"✅ Performance Model Created: {performance_model.id}")
    
    # Test functionality
    health_model.update_health_score(85.0)
    performance_model.add_benchmark("response_time", 150.0)
    
    print(f"\n✅ Health Score: {health_model.health_score}")
    print(f"✅ Performance Benchmarks: {len(performance_model.benchmarks)}")
    
    print("\n🎯 Health & Performance Models Module Ready!")
    return 0


if __name__ == "__main__":
    exit(main())
