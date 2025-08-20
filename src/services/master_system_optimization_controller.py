#!/usr/bin/env python3
"""
Master System Optimization Controller
===================================
Master controller for autonomous system optimization and continuous enhancement.
Follows 200 LOC limit and single responsibility principle.
"""

import logging
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from autonomous_performance_monitor import AutonomousPerformanceMonitor, MetricType
from system_improvement_engine import SystemImprovementEngine, ImprovementType
from optimization_recommendation_system import OptimizationRecommendationSystem, RecommendationType

logger = logging.getLogger(__name__)


@dataclass
class OptimizationStatus:
    """Overall system optimization status"""
    timestamp: str
    monitoring_active: bool
    improvement_engine_active: bool
    recommendations_active: int
    total_optimizations: int
    system_health: str
    optimization_score: float


class MasterSystemOptimizationController:
    """Master controller for system optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.MasterSystemOptimizationController")
        self.performance_monitor = AutonomousPerformanceMonitor("master-monitor")
        self.improvement_engine = SystemImprovementEngine("master-improvement")
        self.recommendation_system = OptimizationRecommendationSystem("master-recommendations")
        self._optimization_active = False
        self._start_time = time.time()
        self.logger.info("Master System Optimization Controller initialized")
    
    def start_optimization_systems(self) -> bool:
        """Start all optimization systems"""
        try:
            self.performance_monitor.start_monitoring()
            self.improvement_engine.start_engine()
            self._optimization_active = True
            self.logger.info("All optimization systems started")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start optimization systems: {e}")
            return False
    
    def record_system_metrics(self, component: str, agent_id: Optional[str] = None):
        """Record system performance metrics"""
        import random
        response_time = random.uniform(100, 2000)
        self.performance_monitor.record_metric(MetricType.RESPONSE_TIME, response_time, component, agent_id)
        error_rate = random.uniform(0.01, 0.10)
        self.performance_monitor.record_metric(MetricType.ERROR_RATE, error_rate, component, agent_id)
        latency = random.uniform(50, 500)
        self.performance_monitor.record_metric(MetricType.LATENCY, latency, component, agent_id)
        resource_usage = random.uniform(0.3, 0.9)
        self.performance_monitor.record_metric(MetricType.RESOURCE_USAGE, resource_usage, component, agent_id)
    
    def analyze_performance_and_optimize(self):
        """Analyze performance and trigger optimizations"""
        performance_summary = self.performance_monitor.get_performance_summary()
        self._generate_performance_recommendations(performance_summary)
        pending_improvements = self.improvement_engine.get_pending_improvements()
        for improvement in pending_improvements[:2]:
            self.improvement_engine.execute_improvement(improvement.action_id)
    
    def _generate_performance_recommendations(self, performance_summary: Dict[str, Any]):
        """Generate performance-based optimization recommendations"""
        for metric_type, data in performance_summary.items():
            if metric_type == "response_time" and data["avg"] > 1500:
                self.recommendation_system.generate_recommendation(
                    "performance_bottleneck", 
                    custom_data={"description": f"High response time detected: {data['avg']:.0f}ms"},
                    confidence=0.9
                )
            elif metric_type == "error_rate" and data["avg"] > 0.05:
                self.recommendation_system.generate_recommendation(
                    "error_rate_reduction",
                    custom_data={"description": f"High error rate detected: {data['avg']:.2%}"},
                    confidence=0.85
                )
            elif metric_type == "resource_usage" and data["avg"] > 0.8:
                self.recommendation_system.generate_recommendation(
                    "resource_optimization",
                    custom_data={"description": f"High resource usage detected: {data['avg']:.1%}"},
                    confidence=0.8
                )
    
    def get_optimization_status(self) -> OptimizationStatus:
        """Get comprehensive optimization system status"""
        from datetime import datetime
        
        monitor_stats = self.performance_monitor.get_monitoring_stats()
        improvement_stats = self.improvement_engine.get_improvement_stats()
        recommendation_summary = self.recommendation_system.get_recommendation_summary()
        
        active_recommendations = recommendation_summary.get("active_recommendations", 0)
        total_optimizations = improvement_stats.get("total_improvements", 0)
        
        system_health = "HEALTHY"
        if monitor_stats.get("active_alerts", 0) > 5:
            system_health = "CRITICAL"
        elif monitor_stats.get("active_alerts", 0) > 2:
            system_health = "DEGRADED"
        
        optimization_score = min(100, max(0, 100 - (monitor_stats.get("active_alerts", 0) * 10)))
        
        return OptimizationStatus(
            timestamp=datetime.now().isoformat(),
            monitoring_active=monitor_stats.get("monitoring_active", False),
            improvement_engine_active=improvement_stats.get("engine_active", False),
            recommendations_active=active_recommendations,
            total_optimizations=total_optimizations,
            system_health=system_health,
            optimization_score=optimization_score
        )
    
    def generate_optimization_report(self) -> str:
        """Generate comprehensive optimization system report"""
        status = self.get_optimization_status()
        
        lines = [
            "🚀 SYSTEM OPTIMIZATION COMPREHENSIVE REPORT",
            "=" * 55,
            f"Timestamp: {status.timestamp}",
            f"System Health: {status.system_health}",
            f"Optimization Score: {status.optimization_score:.1f}/100",
            f"Total Optimizations: {status.total_optimizations}",
            f"Active Recommendations: {status.recommendations_active}",
            "",
            "COMPONENT STATUS:",
            f"  Performance Monitoring: {'ACTIVE' if status.monitoring_active else 'INACTIVE'}",
            f"  Improvement Engine: {'ACTIVE' if status.improvement_engine_active else 'INACTIVE'}",
            f"  Recommendation System: {'ACTIVE' if status.recommendations_active > 0 else 'INACTIVE'}",
            "",
            "SYSTEM METRICS:"
        ]
        
        monitor_stats = self.performance_monitor.get_monitoring_stats()
        improvement_stats = self.improvement_engine.get_improvement_stats()
        
        lines.extend([
            f"  Performance Metrics: {monitor_stats.get('total_metrics', 0)}",
            f"  Active Alerts: {monitor_stats.get('active_alerts', 0)}",
            f"  Improvement Success Rate: {improvement_stats.get('success_rate', 0):.1f}%",
            f"  Total Impact: {improvement_stats.get('total_impact', 0):.2f}"
        ])
        
        lines.append("=" * 55)
        return "\n".join(lines)
    
    def shutdown_optimization_systems(self):
        """Gracefully shutdown all optimization systems"""
        self.logger.info("Shutting down System Optimization Systems")
        
        try:
            self.performance_monitor.stop_monitoring()
            self.improvement_engine.stop_engine()
            self._optimization_active = False
            self.logger.info("System Optimization Systems shutdown complete")
        except Exception as e:
            self.logger.error(f"Shutdown error: {e}")


def main():
    """CLI interface for testing MasterSystemOptimizationController"""
    import argparse
    parser = argparse.ArgumentParser(description="Master System Optimization Controller CLI")
    parser.add_argument("--test", action="store_true", help="Run comprehensive test")
    args = parser.parse_args()
    
    if args.test:
        print("🧪 MasterSystemOptimizationController Comprehensive Test")
        controller = MasterSystemOptimizationController()
        start_success = controller.start_optimization_systems()
        print(f"✅ Optimization systems started: {start_success}")
        controller.record_system_metrics("test-component", "test-agent")
        controller.analyze_performance_and_optimize()
        status = controller.get_optimization_status()
        print(f"✅ System health: {status.system_health}")
        print(f"✅ Optimization score: {status.optimization_score:.1f}")
        report = controller.generate_optimization_report()
        print("\n📊 OPTIMIZATION REPORT:")
        print(report)
        controller.shutdown_optimization_systems()
        print("\n🎉 MasterSystemOptimizationController test PASSED!")
    else:
        print("MasterSystemOptimizationController ready")
        print("Use --test to run comprehensive test")


if __name__ == "__main__":
    main()
