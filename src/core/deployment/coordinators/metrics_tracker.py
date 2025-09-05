"""
Deployment Metrics Tracker - V2 Compliant Module
===============================================

Handles tracking and reporting of deployment metrics.
Extracted from deployment_coordinator.py for V2 compliance.

V2 Compliance: < 300 lines, single responsibility.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

from typing import Dict, Any, List
import logging

from ..deployment_models import (
    MassDeploymentTarget, MaximumEfficiencyDeploymentStatus, 
    DeploymentMetrics, create_deployment_metrics
)


class DeploymentMetricsTracker:
    """
    Tracker for deployment metrics and status reporting.
    
    Manages metrics collection, status tracking, and reporting.
    """
    
    def __init__(self, config):
        """Initialize metrics tracker."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Metrics state
        self.deployment_metrics = create_deployment_metrics()
        self.agent_statuses: Dict[str, MaximumEfficiencyDeploymentStatus] = {}
    
    def update_deployment_metrics(self, results: List[Dict[str, Any]]):
        """Update deployment metrics based on results."""
        for result in results:
            if result.get("success", False):
                self.deployment_metrics.successful_deployments += 1
            else:
                self.deployment_metrics.failed_deployments += 1
            
            # Update total deployment time
            if "deployment_time" in result:
                self.deployment_metrics.total_deployment_time += result["deployment_time"]
        
        # Update success rate
        total_deployments = self.deployment_metrics.successful_deployments + self.deployment_metrics.failed_deployments
        if total_deployments > 0:
            self.deployment_metrics.success_rate = (
                self.deployment_metrics.successful_deployments / total_deployments
            ) * 100
    
    def update_agent_status(self, agent_id: str, status: MaximumEfficiencyDeploymentStatus):
        """Update agent deployment status."""
        self.agent_statuses[agent_id] = status
        self.logger.debug(f"Updated status for {agent_id}")
    
    def get_agent_status(self, agent_id: str) -> MaximumEfficiencyDeploymentStatus:
        """Get agent deployment status."""
        return self.agent_statuses.get(agent_id)
    
    def get_deployment_metrics(self) -> DeploymentMetrics:
        """Get current deployment metrics."""
        return self.deployment_metrics
    
    def get_metrics_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary."""
        return {
            "deployment_metrics": self.deployment_metrics.to_dict(),
            "agent_count": len(self.agent_statuses),
            "agent_statuses": {k: v.to_dict() for k, v in self.agent_statuses.items()},
            "efficiency_score": self._calculate_efficiency_score()
        }
    
    def _calculate_efficiency_score(self) -> float:
        """Calculate overall deployment efficiency score."""
        if self.deployment_metrics.successful_deployments == 0:
            return 0.0
        
        # Base score from success rate
        success_score = self.deployment_metrics.success_rate
        
        # Time efficiency bonus
        if self.deployment_metrics.total_deployment_time > 0:
            avg_time_per_deployment = (
                self.deployment_metrics.total_deployment_time / 
                (self.deployment_metrics.successful_deployments + self.deployment_metrics.failed_deployments)
            )
            time_efficiency = max(0, 100 - (avg_time_per_deployment * 10))  # Penalty for slow deployments
        else:
            time_efficiency = 100
        
        # Combine scores
        efficiency_score = (success_score * 0.7) + (time_efficiency * 0.3)
        return min(100.0, max(0.0, efficiency_score))
    
    def get_target_analysis(self, targets: List[MassDeploymentTarget]) -> Dict[str, Any]:
        """Analyze deployment targets."""
        if not targets:
            return {"total": 0, "by_type": {}, "by_priority": {}, "by_status": {}}
        
        # Count by pattern type
        by_type = {}
        for target in targets:
            by_type[target.pattern_type] = by_type.get(target.pattern_type, 0) + 1
        
        # Count by priority
        by_priority = {}
        for target in targets:
            by_priority[target.priority] = by_priority.get(target.priority, 0) + 1
        
        # Count by status
        by_status = {}
        for target in targets:
            by_status[target.deployment_status] = by_status.get(target.deployment_status, 0) + 1
        
        return {
            "total": len(targets),
            "by_type": by_type,
            "by_priority": by_priority,
            "by_status": by_status
        }
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report."""
        total_deployments = (
            self.deployment_metrics.successful_deployments + 
            self.deployment_metrics.failed_deployments
        )
        
        if total_deployments == 0:
            return {
                "status": "No deployments completed",
                "efficiency_score": 0.0,
                "recommendations": ["Start deployment process"]
            }
        
        efficiency_score = self._calculate_efficiency_score()
        
        # Generate recommendations
        recommendations = []
        
        if self.deployment_metrics.success_rate < 80:
            recommendations.append("Improve deployment success rate - investigate failures")
        
        if self.deployment_metrics.total_deployment_time > 300:  # 5 minutes
            recommendations.append("Optimize deployment time - consider parallel processing")
        
        if efficiency_score < 70:
            recommendations.append("Overall efficiency needs improvement")
        
        if not recommendations:
            recommendations.append("Deployment performance is optimal")
        
        return {
            "status": "Deployment analysis complete",
            "efficiency_score": efficiency_score,
            "success_rate": self.deployment_metrics.success_rate,
            "total_deployments": total_deployments,
            "average_time": (
                self.deployment_metrics.total_deployment_time / total_deployments
                if total_deployments > 0 else 0
            ),
            "recommendations": recommendations
        }
    
    def reset_metrics(self):
        """Reset all metrics to initial state."""
        self.deployment_metrics = create_deployment_metrics()
        self.agent_statuses.clear()
        self.logger.info("Deployment metrics reset")
    
    def export_metrics(self) -> Dict[str, Any]:
        """Export metrics data for external use."""
        return {
            "metrics": self.deployment_metrics.to_dict(),
            "agent_statuses": {k: v.to_dict() for k, v in self.agent_statuses.items()},
            "efficiency_score": self._calculate_efficiency_score(),
            "exported_at": self.logger.info("Metrics exported")
        }
