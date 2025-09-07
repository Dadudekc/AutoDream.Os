#!/usr/bin/env python3
"""
Async Coordination Metrics - Agent Cellphone V2
==============================================

Performance metrics and monitoring for the asynchronous coordination system.
V2 Compliance: Metrics calculation and monitoring only.

Author: Agent-1 (PERPETUAL MOTION LEADER - COORDINATION ENHANCEMENT MANAGER)
License: MIT
"""

import time
import threading
from typing import Dict, List, Any
from .async_coordination_models import (
    CoordinationTask, TaskResult, PerformanceMetrics, TaskStatus
)


class MetricsManager:
    """
    Performance metrics manager for async coordination system.
    
    Single Responsibility: Track and calculate performance metrics.
    Follows V2 standards: ≤400 LOC, OOP design, SRP compliance.
    """
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.task_metrics: Dict[str, Dict[str, Any]] = {}
        self.lock = threading.Lock()
        self.last_throughput_update = time.time()
        self.throughput_samples: List[float] = []
    
    def update_task_metrics(self, task: CoordinationTask, execution_time: float, success: bool):
        """Update metrics for a completed task."""
        with self.lock:
            # Update basic metrics
            self.metrics.total_tasks += 1
            if success:
                self.metrics.completed_tasks += 1
            else:
                self.metrics.failed_tasks += 1
            
            # Calculate success rate
            if self.metrics.total_tasks > 0:
                self.metrics.success_rate = (
                    self.metrics.completed_tasks / self.metrics.total_tasks
                ) * 100
            
            # Update execution time metrics
            self.metrics.total_execution_time += execution_time
            if self.metrics.completed_tasks > 0:
                self.metrics.avg_execution_time = (
                    self.metrics.total_execution_time / self.metrics.completed_tasks
                )
            
            # Update coordination latency
            if task.started_at and task.created_at:
                latency = task.started_at - task.created_at
                if self.metrics.completed_tasks > 0:
                    current_avg = self.metrics.avg_coordination_latency
                    self.metrics.avg_coordination_latency = (
                        (current_avg * (self.metrics.completed_tasks - 1) + latency) / 
                        self.metrics.completed_tasks
                    )
                else:
                    self.metrics.avg_coordination_latency = latency
            
            # Update throughput metrics
            self._update_throughput_metrics()
            
            # Store task-specific metrics
            self.task_metrics[task.task_id] = {
                "execution_time": execution_time,
                "success": success,
                "task_type": task.task_type.value,
                "priority": task.priority.value,
                "mode": task.mode.value,
                "timestamp": time.time()
            }
            
            self.metrics.last_update = time.time()
    
    def _update_throughput_metrics(self):
        """Update throughput metrics based on recent activity."""
        current_time = time.time()
        time_diff = current_time - self.last_throughput_update
        
        if time_diff >= 0.1:  # Update every 100ms for responsiveness
            # Calculate current throughput
            if time_diff > 0:
                current_throughput = self.metrics.completed_tasks / time_diff
                self.throughput_samples.append(current_throughput)
                
                # Keep only recent samples (last 10 seconds)
                if len(self.throughput_samples) > 100:  # 10s / 0.1s = 100 samples
                    self.throughput_samples.pop(0)
                
                # Calculate average throughput
                if self.throughput_samples:
                    self.metrics.avg_throughput = sum(self.throughput_samples) / len(self.throughput_samples)
            
            self.last_throughput_update = current_time
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        with self.lock:
            return {
                "total_tasks": self.metrics.total_tasks,
                "completed_tasks": self.metrics.completed_tasks,
                "failed_tasks": self.metrics.failed_tasks,
                "success_rate": self.metrics.success_rate,
                "avg_execution_time": self.metrics.avg_execution_time,
                "avg_coordination_latency": self.metrics.avg_coordination_latency,
                "avg_throughput": self.metrics.avg_throughput,
                "total_execution_time": self.metrics.total_execution_time,
                "last_update": self.metrics.last_update
            }
    
    def get_task_metrics(self, task_id: str) -> Dict[str, Any]:
        """Get metrics for a specific task."""
        with self.lock:
            return self.task_metrics.get(task_id, {})
    
    def get_task_type_metrics(self, task_type: str) -> Dict[str, Any]:
        """Get aggregated metrics for a specific task type."""
        with self.lock:
            type_metrics = {
                "total_tasks": 0,
                "completed_tasks": 0,
                "failed_tasks": 0,
                "avg_execution_time": 0.0,
                "success_rate": 0.0
            }
            
            type_tasks = [m for m in self.task_metrics.values() if m.get("task_type") == task_type]
            
            if type_tasks:
                type_metrics["total_tasks"] = len(type_tasks)
                type_metrics["completed_tasks"] = sum(1 for m in type_tasks if m["success"])
                type_metrics["failed_tasks"] = type_metrics["total_tasks"] - type_metrics["completed_tasks"]
                
                if type_metrics["total_tasks"] > 0:
                    type_metrics["success_rate"] = (
                        type_metrics["completed_tasks"] / type_metrics["total_tasks"]
                    ) * 100
                    
                    execution_times = [m["execution_time"] for m in type_tasks if m["success"]]
                    if execution_times:
                        type_metrics["avg_execution_time"] = sum(execution_times) / len(execution_times)
            
            return type_metrics
    
    def reset_metrics(self):
        """Reset all metrics to initial state."""
        with self.lock:
            self.metrics = PerformanceMetrics()
            self.task_metrics.clear()
            self.throughput_samples.clear()
            self.last_throughput_update = time.time()
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export all metrics for external analysis."""
        with self.lock:
            return {
                "system_metrics": self.get_performance_metrics(),
                "task_metrics": self.task_metrics.copy(),
                "throughput_samples": self.throughput_samples.copy(),
                "export_timestamp": time.time()
            }
    
    def get_performance_summary(self) -> str:
        """Get a human-readable performance summary."""
        metrics = self.get_performance_metrics()
        
        summary = f"""📊 Async Coordination Performance Summary

🎯 Task Processing:
   • Total Tasks: {metrics['total_tasks']}
   • Completed: {metrics['completed_tasks']}
   • Failed: {metrics['failed_tasks']}
   • Success Rate: {metrics['success_rate']:.1f}%

⚡ Performance Metrics:
   • Average Execution Time: {metrics['avg_execution_time']:.3f}s
   • Average Coordination Latency: {metrics['avg_coordination_latency']:.3f}s
   • Average Throughput: {metrics['avg_throughput']:.1f} tasks/sec
   • Total Execution Time: {metrics['total_execution_time']:.3f}s

🕒 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(metrics['last_update']))}
"""
        return summary
