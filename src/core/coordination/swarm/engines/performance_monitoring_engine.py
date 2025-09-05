#!/usr/bin/env python3
"""
Performance Monitoring Engine - V2 Compliance Module
===================================================

Handles performance monitoring and metrics collection for swarm operations.
Extracted from swarm_coordination_orchestrator.py for V2 compliance.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque
import logging

from ..coordination_models import (
    CoordinationMetrics, CoordinationResult, create_coordination_metrics
)


class PerformanceMonitoringEngine:
    """Engine for performance monitoring and metrics collection."""

    def __init__(self, config):
        """Initialize performance monitoring engine."""
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.metrics = create_coordination_metrics()
        self.efficiency_history: deque = deque(maxlen=100)
        self.performance_history: deque = deque(maxlen=1000)

    def update_metrics(self, result: CoordinationResult) -> None:
        """Update metrics based on task result."""
        try:
            # Update basic metrics
            self.metrics.total_tasks += 1
            
            if result.success:
                self.metrics.successful_tasks += 1
            else:
                self.metrics.failed_tasks += 1
            
            # Update execution time metrics
            if result.execution_time_seconds:
                self.metrics.total_execution_time += result.execution_time_seconds
                self.metrics.average_execution_time = (
                    self.metrics.total_execution_time / self.metrics.total_tasks
                )
            
            # Update efficiency
            efficiency = self._calculate_efficiency(result)
            self.efficiency_history.append(efficiency)
            self.metrics.average_efficiency = sum(self.efficiency_history) / len(self.efficiency_history)
            
            # Store performance data
            self.performance_history.append({
                "task_id": result.task_id,
                "success": result.success,
                "execution_time": result.execution_time_seconds,
                "efficiency": efficiency,
                "timestamp": datetime.now()
            })
            
        except Exception as e:
            self.logger.error(f"Failed to update metrics: {e}")

    def _calculate_efficiency(self, result: CoordinationResult) -> float:
        """Calculate efficiency score for task result."""
        try:
            if not result.success:
                return 0.0
            
            # Base efficiency from success
            base_efficiency = 1.0
            
            # Time-based efficiency (faster is better)
            if result.execution_time_seconds:
                time_efficiency = max(0.0, 1.0 - (result.execution_time_seconds / 10.0))  # Normalize to 10s max
            else:
                time_efficiency = 0.5
            
            # Combine factors
            efficiency = (base_efficiency * 0.7) + (time_efficiency * 0.3)
            return min(efficiency, 1.0)
            
        except Exception as e:
            self.logger.error(f"Failed to calculate efficiency: {e}")
            return 0.0

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary."""
        try:
            total_tasks = self.metrics.total_tasks
            success_rate = (
                self.metrics.successful_tasks / total_tasks * 100
                if total_tasks > 0 else 0
            )
            
            return {
                "metrics": {
                    "total_tasks": total_tasks,
                    "successful_tasks": self.metrics.successful_tasks,
                    "failed_tasks": self.metrics.failed_tasks,
                    "success_rate": success_rate,
                    "average_execution_time": self.metrics.average_execution_time,
                    "total_execution_time": self.metrics.total_execution_time,
                    "average_efficiency": self.metrics.average_efficiency
                },
                "efficiency_trend": list(self.efficiency_history),
                "recent_performance": list(self.performance_history)[-10:] if self.performance_history else [],
                "performance_indicators": {
                    "high_efficiency_tasks": sum(1 for p in self.performance_history if p.get("efficiency", 0) > 0.8),
                    "low_efficiency_tasks": sum(1 for p in self.performance_history if p.get("efficiency", 0) < 0.5),
                    "average_task_duration": self.metrics.average_execution_time
                }
            }
            
        except Exception as e:
            self.logger.error(f"Failed to get performance summary: {e}")
            return {"error": str(e)}

    def get_efficiency_trend(self, window_size: int = 10) -> List[float]:
        """Get efficiency trend over specified window."""
        try:
            if len(self.efficiency_history) < window_size:
                return list(self.efficiency_history)
            
            return list(self.efficiency_history)[-window_size:]
            
        except Exception as e:
            self.logger.error(f"Failed to get efficiency trend: {e}")
            return []

    def reset_metrics(self) -> None:
        """Reset all performance metrics."""
        try:
            self.metrics = create_coordination_metrics()
            self.efficiency_history.clear()
            self.performance_history.clear()
            self.logger.info("Performance metrics reset")
            
        except Exception as e:
            self.logger.error(f"Failed to reset metrics: {e}")

    def get_metrics_export(self) -> Dict[str, Any]:
        """Get metrics for export or reporting."""
        try:
            return {
                "coordination_metrics": self.metrics.to_dict(),
                "efficiency_history": list(self.efficiency_history),
                "performance_history": list(self.performance_history),
                "export_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to export metrics: {e}")
            return {"error": str(e)}
