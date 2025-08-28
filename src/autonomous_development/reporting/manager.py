"""Autonomous Development Reporting Manager."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from src.core.base_manager import BaseManager

from . import formatting as fmt
from .generation import generate_performance_report
from .persistence import (
    InMemoryReportStorage,
    ReportStorageBackend,
    load_report_history,
    save_report_history,
)

if TYPE_CHECKING:  # pragma: no cover
    from src.autonomous_development.core import DevelopmentTask
    from src.core.task_manager import DevelopmentTaskManager as TaskManager


class ReportingManager(BaseManager):
    """Manages reporting and status formatting for autonomous development."""

    def __init__(
        self,
        task_manager: "TaskManager",
        storage_backend: Optional[ReportStorageBackend] = None,
    ) -> None:
        super().__init__(
            manager_id="reporting_manager",
            name="Reporting Manager",
            description="Manages reporting and status formatting for autonomous development",
        )
        self.task_manager = task_manager
        self.storage_backend: ReportStorageBackend = (
            storage_backend or InMemoryReportStorage()
        )

        self.reports_generated: int = 0
        self.last_report_time: Optional[datetime] = None
        self.report_history: List[Dict[str, Any]] = []

        self.logger.info("Reporting Manager initialized")

    # ------------------------------------------------------------------
    # BaseManager Abstract Method Implementations
    # ------------------------------------------------------------------
    def _on_start(self) -> bool:
        try:
            self.logger.info("Starting Reporting Manager...")
            self.reports_generated = 0
            self.last_report_time = None
            self.report_history.clear()
            self.logger.info("Reporting Manager started successfully")
            return True
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to start Reporting Manager: {e}")
            return False

    def _on_stop(self) -> None:
        try:
            self.logger.info("Stopping Reporting Manager...")
            self._save_report_history()
            self.report_history.clear()
            self.logger.info("Reporting Manager stopped successfully")
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to stop Reporting Manager: {e}")

    def _on_heartbeat(self) -> None:
        try:
            self._check_reporting_needs()
            self.record_operation("heartbeat", True, 0.0)
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Heartbeat error: {e}")
            self.record_operation("heartbeat", False, 0.0)

    def _on_initialize_resources(self) -> bool:
        try:
            self.reports_generated = 0
            self.last_report_time = None
            self.report_history = []
            return True
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to initialize resources: {e}")
            return False

    def _on_cleanup_resources(self) -> None:
        try:
            self.report_history.clear()
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to cleanup resources: {e}")

    def _on_recovery_attempt(self, error: Exception, context: str) -> bool:
        try:
            self.logger.info(f"Attempting recovery for {context}")
            self.reports_generated = 0
            self.last_report_time = None
            self.report_history.clear()
            self.logger.info("Recovery successful")
            return True
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Recovery failed: {e}")
            return False

    # ------------------------------------------------------------------
    # Formatting Delegates
    # ------------------------------------------------------------------
    def format_task_list_for_agents(self, tasks: List["DevelopmentTask"]) -> str:
        return fmt.format_task_list(tasks)

    def format_progress_summary(self) -> str:
        return fmt.format_progress_summary(self.task_manager)

    def format_cycle_summary(self) -> str:
        return fmt.format_cycle_summary(self.task_manager)

    def format_workflow_start_message(self) -> str:
        return fmt.format_workflow_start_message()

    def format_agent1_message(self) -> str:
        return fmt.format_agent1_message()

    def format_no_tasks_message(self) -> str:
        return fmt.format_no_tasks_message()

    def format_task_claimed_message(self, task: "DevelopmentTask") -> str:
        return fmt.format_task_claimed_message(task)

    def format_progress_update_message(
        self,
        task: "DevelopmentTask",
        new_progress: float,
        blockers: Optional[List[str]] = None,
    ) -> str:
        return fmt.format_progress_update_message(task, new_progress, blockers)

    def format_workflow_complete_message(self) -> str:
        return fmt.format_workflow_complete_message(self.task_manager)

    def format_remaining_tasks_message(self, remaining_count: int) -> str:
        return fmt.format_remaining_tasks_message(remaining_count)

    def format_detailed_task_status(self) -> str:
        return fmt.format_detailed_task_status(self.task_manager)

    def format_workflow_statistics(self) -> str:
        return fmt.format_workflow_statistics(self.task_manager)

    # ------------------------------------------------------------------
    # Report Generation & Persistence
    # ------------------------------------------------------------------
    def generate_performance_report(self) -> Dict[str, Any]:
        try:
            report = generate_performance_report(self.task_manager)
            self.reports_generated += 1
            self.last_report_time = datetime.now()
            self.report_history.append(
                {
                    "timestamp": self.last_report_time.isoformat(),
                    "report_type": "performance",
                    "success": True,
                }
            )
            self.record_operation("generate_performance_report", True, 0.0)
            return report
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to generate performance report: {e}")
            self.report_history.append(
                {
                    "timestamp": datetime.now().isoformat(),
                    "report_type": "performance",
                    "success": False,
                    "error": str(e),
                }
            )
            self.record_operation("generate_performance_report", False, 0.0)
            return {}

    def _save_report_history(self) -> None:
        try:
            save_report_history(
                self.storage_backend,
                self.report_history,
                self.reports_generated,
                self.last_report_time.isoformat() if self.last_report_time else None,
            )
            self.logger.debug("Report history saved")
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to save report history: {e}")

    def get_report_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            return load_report_history(self.storage_backend, limit)
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to retrieve report history: {e}")
            return []

    def get_last_report(self) -> Optional[Dict[str, Any]]:
        history = self.get_report_history(limit=1)
        return history[-1] if history else None

    def _check_reporting_needs(self) -> None:
        try:
            if self.last_report_time:
                time_since_last = (
                    datetime.now() - self.last_report_time
                ).total_seconds()
                if time_since_last > 3600:  # 1 hour
                    self.logger.info("Time for new performance report")
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to check reporting needs: {e}")

    def get_reporting_stats(self) -> Dict[str, Any]:
        try:
            stats = {
                "reports_generated": self.reports_generated,
                "last_report_time": self.last_report_time.isoformat()
                if self.last_report_time
                else None,
                "report_history_size": len(self.report_history),
                "successful_reports": len(
                    [r for r in self.report_history if r.get("success", False)]
                ),
                "failed_reports": len(
                    [r for r in self.report_history if not r.get("success", False)]
                ),
            }
            self.record_operation("get_reporting_stats", True, 0.0)
            return stats
        except Exception as e:  # pragma: no cover - defensive
            self.logger.error(f"Failed to get reporting stats: {e}")
            self.record_operation("get_reporting_stats", False, 0.0)
            return {"error": str(e)}
