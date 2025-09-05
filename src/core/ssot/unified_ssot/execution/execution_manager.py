"""
SSOT Execution Manager - V2 Compliance Module
============================================

Execution management functionality for SSOT operations.

V2 Compliance: < 300 lines, single responsibility, execution management.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from typing import Dict, List, Optional, Any
from datetime import datetime

from ..models import (
    SSOTExecutionTask, SSOTIntegrationResult, SSOTExecutionPhase
)


class ExecutionManager:
    """SSOT execution management functionality."""
    
    def __init__(self):
        """Initialize execution manager."""
        self.execution_history: List[SSOTIntegrationResult] = []
        self.performance_metrics: Dict[str, Any] = {}
    
    def add_execution_result(self, result: SSOTIntegrationResult) -> None:
        """Add execution result to history."""
        self.execution_history.append(result)
    
    def get_execution_history(self, limit: int = 100) -> List[SSOTIntegrationResult]:
        """Get execution history."""
        return self.execution_history[-limit:]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        if not self.execution_history:
            return {
                "total_executions": 0,
                "success_rate": 0.0,
                "average_execution_time": 0.0,
                "total_execution_time": 0.0
            }
        
        total_executions = len(self.execution_history)
        successful_executions = sum(1 for r in self.execution_history if r.status == "completed")
        success_rate = (successful_executions / total_executions) * 100 if total_executions > 0 else 0
        
        execution_times = [r.execution_time for r in self.execution_history if r.execution_time is not None]
        average_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
        total_execution_time = sum(execution_times)
        
        return {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": total_executions - successful_executions,
            "success_rate": success_rate,
            "average_execution_time": average_execution_time,
            "total_execution_time": total_execution_time
        }
    
    def get_execution_summary(self) -> Dict[str, Any]:
        """Get execution summary."""
        metrics = self.get_performance_metrics()
        
        # Group by phase
        phase_counts = {}
        for result in self.execution_history:
            phase = result.phase.value if hasattr(result.phase, 'value') else str(result.phase)
            phase_counts[phase] = phase_counts.get(phase, 0) + 1
        
        # Group by status
        status_counts = {}
        for result in self.execution_history:
            status_counts[result.status] = status_counts.get(result.status, 0) + 1
        
        return {
            "metrics": metrics,
            "phase_distribution": phase_counts,
            "status_distribution": status_counts,
            "last_execution": self.execution_history[-1].created_at.isoformat() if self.execution_history else None
        }
    
    def clear_history(self) -> None:
        """Clear execution history."""
        self.execution_history.clear()
    
    def get_recent_executions(self, hours: int = 24) -> List[SSOTIntegrationResult]:
        """Get recent executions within specified hours."""
        cutoff_time = datetime.now().timestamp() - (hours * 3600)
        return [
            result for result in self.execution_history
            if result.created_at.timestamp() >= cutoff_time
        ]
