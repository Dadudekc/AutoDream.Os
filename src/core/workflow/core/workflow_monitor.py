#!/usr/bin/env python3
"""
Workflow Monitor - Performance Monitoring Engine
==============================================

Performance monitoring and status tracking for unified workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Workflow Unification)
License: MIT
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

from ..types.workflow_models import WorkflowExecution, WorkflowStep
from ..types.workflow_enums import TaskStatus


@dataclass
class PerformanceMetrics:
    """Performance metrics for workflow monitoring."""
    execution_time: float
    step_count: int
    completed_steps: int
    failed_steps: int
    average_step_time: float


@dataclass
class HealthStatus:
    """Health status for workflow monitoring."""
    overall_health: str
    performance_score: float
    error_count: int
    warning_count: int
    recommendations: List[str]


class WorkflowMonitor:
    """Performance monitoring engine for workflow system."""
    
    def __init__(self):
        self.logger = logging.getLogger(f"{__name__}.WorkflowMonitor")
        self.monitoring_history: Dict[str, List[PerformanceMetrics]] = {}
        self.health_history: Dict[str, List[HealthStatus]] = {}
        self.thresholds = {"max_exec_time": 3600.0, "max_step_time": 300.0}
    
    def monitor_workflow(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Monitor workflow execution performance and health."""
        self.logger.info(f"Monitoring workflow: {execution.execution_id}")
        
        # Collect metrics and assess health in one pass
        start_time = self._parse_time(execution.start_time)
        end_time = self._parse_time(execution.end_time or datetime.now())
        execution_time = (end_time - start_time).total_seconds()
        
        steps = execution.steps or []
        step_count = len(steps)
        completed_steps = sum(1 for step in steps if step.status == TaskStatus.COMPLETED)
        failed_steps = sum(1 for step in steps if step.status == TaskStatus.FAILED)
        
        # Calculate average step time
        step_times = []
        for step in steps:
            if step.start_time and step.end_time:
                step_start = self._parse_time(step.start_time)
                step_end = self._parse_time(step.end_time)
                step_times.append((step_end - step_start).total_seconds())
        
        avg_step_time = sum(step_times) / len(step_times) if step_times else 0.0
        
        metrics = PerformanceMetrics(
            execution_time=execution_time,
            step_count=step_count,
            completed_steps=completed_steps,
            failed_steps=failed_steps,
            average_step_time=avg_step_time
        )
        
        # Assess health
        performance_score = self._calculate_score(metrics)
        warnings = self._count_warnings(metrics)
        
        # Determine health level
        if performance_score >= 0.9 and failed_steps == 0:
            health_level = "EXCELLENT"
        elif performance_score >= 0.7 and failed_steps <= 1:
            health_level = "GOOD"
        elif performance_score >= 0.5 and failed_steps <= 2:
            health_level = "FAIR"
        else:
            health_level = "POOR"
        
        # Generate recommendations inline
        recommendations = []
        if failed_steps > 0:
            recommendations.append("Review failed steps and implement error handling")
        if avg_step_time > self.thresholds["max_step_time"]:
            recommendations.append("Optimize step execution time - consider parallelization")
        if execution_time > self.thresholds["max_exec_time"]:
            recommendations.append("Review workflow design for potential bottlenecks")
        if performance_score < 0.7:
            recommendations.append("Implement comprehensive workflow optimization")
        if not recommendations:
            recommendations.append("Workflow performance is optimal - maintain current configuration")
        
        health = HealthStatus(
            overall_health=health_level,
            performance_score=performance_score,
            error_count=failed_steps,
            warning_count=warnings,
            recommendations=recommendations
        )
        
        # Store data and generate report
        self._store_data(execution.execution_id, metrics, health)
        return self._generate_report(execution, metrics, health)
    
    def _parse_time(self, time_value) -> datetime:
        """Parse time value to datetime object."""
        return datetime.fromisoformat(time_value) if isinstance(time_value, str) else time_value
    
    def _calculate_score(self, metrics: PerformanceMetrics) -> float:
        """Calculate performance score based on metrics."""
        if metrics.step_count == 0:
            return 0.0
        
        completion_rate = metrics.completed_steps / metrics.step_count
        time_efficiency = 1.0 if metrics.execution_time <= self.thresholds["max_exec_time"] else 0.5
        error_penalty = max(0, metrics.failed_steps * 0.1)
        
        score = (completion_rate * 0.6 + time_efficiency * 0.4) - error_penalty
        return max(0.0, min(1.0, score))
    
    def _count_warnings(self, metrics: PerformanceMetrics) -> int:
        """Count warnings based on performance thresholds."""
        warnings = 0
        if metrics.execution_time > self.thresholds["max_exec_time"]:
            warnings += 1
        if metrics.average_step_time > self.thresholds["max_step_time"]:
            warnings += 1
        if metrics.failed_steps > 0:
            warnings += 1
        return warnings
    
    def _store_data(self, execution_id: str, metrics: PerformanceMetrics, 
                   health: HealthStatus):
        """Store monitoring data for historical analysis."""
        if execution_id not in self.monitoring_history:
            self.monitoring_history[execution_id] = []
        if execution_id not in self.health_history:
            self.health_history[execution_id] = []
        
        self.monitoring_history[execution_id].append(metrics)
        self.health_history[execution_id].append(health)
    
    def _generate_report(self, execution: WorkflowExecution, 
                        metrics: PerformanceMetrics, 
                        health: HealthStatus) -> Dict[str, Any]:
        """Generate comprehensive monitoring report."""
        return {
            "execution_id": execution.execution_id,
            "workflow_name": execution.workflow_name,
            "monitoring_timestamp": datetime.now().isoformat(),
            "performance_metrics": {
                "execution_time_seconds": metrics.execution_time,
                "step_count": metrics.step_count,
                "completed_steps": metrics.completed_steps,
                "failed_steps": metrics.failed_steps,
                "average_step_time_seconds": metrics.average_step_time
            },
            "health_status": {
                "overall_health": health.overall_health,
                "performance_score": health.performance_score,
                "error_count": health.error_count,
                "warning_count": health.warning_count,
                "recommendations": health.recommendations
            },
            "thresholds": self.thresholds
        }
    
    def get_performance_history(self, execution_id: str) -> List[PerformanceMetrics]:
        """Get performance history for a specific workflow execution."""
        return self.monitoring_history.get(execution_id, [])
    
    def get_health_history(self, execution_id: str) -> List[HealthStatus]:
        """Get health history for a specific workflow execution."""
        return self.health_history.get(execution_id, [])
    
    def clear_history(self, execution_id: Optional[str] = None):
        """Clear monitoring history for specific or all executions."""
        if execution_id:
            self.monitoring_history.pop(execution_id, None)
            self.health_history.pop(execution_id, None)
            self.logger.info(f"Cleared monitoring history for {execution_id}")
        else:
            self.monitoring_history.clear()
            self.health_history.clear()
            self.logger.info("Cleared all monitoring history")
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for workflow monitor."""
        try:
            mock_step = WorkflowStep(
                step_id="test_step",
                name="Test Step",
                step_type="test",
                status=TaskStatus.COMPLETED,
                start_time=datetime.now().isoformat(),
                end_time=datetime.now().isoformat()
            )
            
            mock_execution = WorkflowExecution(
                execution_id="test_execution",
                workflow_id="test_workflow",
                workflow_name="Test Workflow",
                start_time=datetime.now().isoformat(),
                steps=[mock_step]
            )
            
            report = self.monitor_workflow(mock_execution)
            
            if (report and "performance_metrics" in report and 
                "health_status" in report):
                self.logger.info("✅ Workflow monitor smoke test passed.")
                return True
            else:
                self.logger.error("❌ Workflow monitor smoke test failed: Invalid report structure.")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Workflow monitor smoke test failed: {e}")
            return False
