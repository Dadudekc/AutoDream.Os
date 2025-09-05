#!/usr/bin/env python3
"""
Deployment Metrics Engine
=========================

Tracks and analyzes deployment metrics and performance.
Extracted from deployment_coordinator.py for V2 compliance.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta

from ..deployment_models import (
    MassDeploymentTarget, DeploymentMetrics, DeploymentStatus,
    create_deployment_metrics
)


class DeploymentMetricsEngine:
    """Tracks and analyzes deployment metrics."""
    
    def __init__(self):
        """Initialize deployment metrics engine."""
        self.logger = logging.getLogger(__name__)
        self.metrics_history: List[DeploymentMetrics] = []
        self.current_metrics: Optional[DeploymentMetrics] = None
        
    def start_deployment_tracking(self, total_targets: int) -> DeploymentMetrics:
        """Start tracking a new deployment session."""
        self.current_metrics = create_deployment_metrics(
            total_targets=total_targets,
            start_time=datetime.now()
        )
        
        self.logger.info(f"Started tracking deployment with {total_targets} targets")
        return self.current_metrics
    
    def update_target_completion(self, target: MassDeploymentTarget) -> None:
        """Update metrics when a target completes."""
        if not self.current_metrics:
            return
            
        try:
            if target.status == DeploymentStatus.COMPLETED:
                self.current_metrics.completed_targets += 1
                self.current_metrics.success_count += 1
            elif target.status == DeploymentStatus.FAILED:
                self.current_metrics.completed_targets += 1
                self.current_metrics.failure_count += 1
            elif target.status == DeploymentStatus.CANCELLED:
                self.current_metrics.completed_targets += 1
                
            # Update execution time tracking
            if target.execution_time:
                if self.current_metrics.total_execution_time is None:
                    self.current_metrics.total_execution_time = 0
                self.current_metrics.total_execution_time += target.execution_time
                
                # Update average
                completed = self.current_metrics.completed_targets
                if completed > 0:
                    self.current_metrics.average_execution_time = (
                        self.current_metrics.total_execution_time / completed
                    )
            
            # Update success rate
            if self.current_metrics.completed_targets > 0:
                self.current_metrics.success_rate = (
                    self.current_metrics.success_count / self.current_metrics.completed_targets
                )
            
            self.logger.debug(f"Updated metrics: {self.current_metrics.completed_targets}/{self.current_metrics.total_targets} completed")
            
        except Exception as e:
            self.logger.error(f"Failed to update metrics for target {target.target_id}: {e}")
    
    def finish_deployment_tracking(self) -> Optional[DeploymentMetrics]:
        """Finish tracking and finalize metrics."""
        if not self.current_metrics:
            return None
            
        try:
            self.current_metrics.end_time = datetime.now()
            self.current_metrics.total_duration = (
                self.current_metrics.end_time - self.current_metrics.start_time
            ).total_seconds()
            
            # Calculate throughput (targets per second)
            if self.current_metrics.total_duration > 0:
                self.current_metrics.throughput = (
                    self.current_metrics.completed_targets / self.current_metrics.total_duration
                )
            
            # Add to history
            self.metrics_history.append(self.current_metrics)
            
            # Keep only last 100 entries
            if len(self.metrics_history) > 100:
                self.metrics_history = self.metrics_history[-100:]
            
            final_metrics = self.current_metrics
            self.current_metrics = None
            
            self.logger.info(f"Deployment tracking completed: {final_metrics.success_rate:.2%} success rate")
            return final_metrics
            
        except Exception as e:
            self.logger.error(f"Failed to finalize metrics: {e}")
            return self.current_metrics
    
    def get_current_metrics(self) -> Optional[DeploymentMetrics]:
        """Get current deployment metrics."""
        return self.current_metrics
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get a summary of deployment metrics."""
        if not self.current_metrics:
            return {"status": "No active deployment"}
            
        try:
            progress_percentage = 0
            if self.current_metrics.total_targets > 0:
                progress_percentage = (
                    self.current_metrics.completed_targets / self.current_metrics.total_targets * 100
                )
            
            return {
                "status": "active",
                "progress_percentage": round(progress_percentage, 2),
                "completed_targets": self.current_metrics.completed_targets,
                "total_targets": self.current_metrics.total_targets,
                "success_count": self.current_metrics.success_count,
                "failure_count": self.current_metrics.failure_count,
                "success_rate": round(self.current_metrics.success_rate * 100, 2) if self.current_metrics.success_rate else 0,
                "average_execution_time": round(self.current_metrics.average_execution_time, 3) if self.current_metrics.average_execution_time else 0,
                "throughput": round(self.current_metrics.throughput, 3) if self.current_metrics.throughput else 0,
                "elapsed_time": (datetime.now() - self.current_metrics.start_time).total_seconds()
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate metrics summary: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_historical_metrics(self, limit: int = 10) -> List[DeploymentMetrics]:
        """Get historical deployment metrics."""
        return self.metrics_history[-limit:] if self.metrics_history else []
    
    def analyze_performance_trends(self) -> Dict[str, Any]:
        """Analyze performance trends from historical data."""
        if len(self.metrics_history) < 2:
            return {"status": "insufficient_data"}
            
        try:
            recent_metrics = self.metrics_history[-10:]  # Last 10 deployments
            
            # Calculate averages
            avg_success_rate = sum(m.success_rate for m in recent_metrics if m.success_rate) / len(recent_metrics)
            avg_throughput = sum(m.throughput for m in recent_metrics if m.throughput) / len(recent_metrics)
            avg_execution_time = sum(m.average_execution_time for m in recent_metrics if m.average_execution_time) / len(recent_metrics)
            
            return {
                "status": "analysis_complete",
                "deployments_analyzed": len(recent_metrics),
                "average_success_rate": round(avg_success_rate * 100, 2),
                "average_throughput": round(avg_throughput, 3),
                "average_execution_time": round(avg_execution_time, 3),
                "total_deployments": len(self.metrics_history)
            }
            
        except Exception as e:
            self.logger.error(f"Performance trend analysis failed: {e}")
            return {"status": "analysis_error", "message": str(e)}
