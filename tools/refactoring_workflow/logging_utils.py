from datetime import datetime, timezone
from typing import Any, Dict

from .models import WorkflowExecution


class WorkflowPerformanceMonitor:
    """Monitor workflow performance and reliability"""

    def __init__(self) -> None:
        self.performance_metrics: Dict[str, Any] = {}

    def get_execution_metrics(self, execution: WorkflowExecution) -> Dict[str, Any]:
        """Get performance metrics for a workflow execution"""
        if execution.end_time and execution.start_time:
            start_time = datetime.fromisoformat(
                execution.start_time.replace("Z", "+00:00")
            )
            end_time = datetime.fromisoformat(execution.end_time.replace("Z", "+00:00"))
            duration = (end_time - start_time).total_seconds()
        else:
            duration = 0

        return {
            "duration_seconds": duration,
            "steps_completed": len(execution.steps_completed),
            "success_rate": 1.0 if execution.state.value == "completed" else 0.0,
            "error_count": len(execution.error_log),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
