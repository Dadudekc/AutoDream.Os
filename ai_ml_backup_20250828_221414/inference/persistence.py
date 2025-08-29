"""Persistence and health utilities for AIManager."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class PersistenceMixin:
    """Mixin handling persistence and health checks."""

    models: dict
    active_workflows: dict
    model_registrations: list
    workflow_executions: list
    api_key_requests: list
    manager_id: str
    logger: any

    def _save_ai_management_data(self) -> None:
        """Save AI management data to persistent storage."""
        try:
            persistence_dir = Path("data/persistent/ai_ml_core")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            ai_data = {
                "models": {k: v.__dict__ for k, v in self.models.items()},
                "active_workflows": self.active_workflows,
                "model_registrations": self.model_registrations,
                "workflow_executions": self.workflow_executions,
                "api_key_requests": self.api_key_requests,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0",
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_ml_core_data_{timestamp}.json"
            filepath = persistence_dir / filename
            with open(filepath, "w") as f:
                json.dump(ai_data, f, indent=2, default=str)
            self._cleanup_old_backups(persistence_dir, "ai_ml_core_data_*.json", 5)
            self.logger.info(f"AI management data saved to {filepath}")
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to save AI management data: {e}")
            self.logger.warning("Persistence failed, data only logged in memory")

    def _cleanup_old_backups(self, directory: Path, pattern: str, keep_count: int) -> None:
        """Clean up old backup files, keeping only the specified number."""
        try:
            files = list(directory.glob(pattern))
            if len(files) > keep_count:
                files.sort(key=lambda x: x.stat().st_mtime)
                for old_file in files[:-keep_count]:
                    old_file.unlink()
                    self.logger.debug(f"Removed old backup: {old_file}")
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.warning(f"Failed to cleanup old backups: {e}")

    def _check_ai_management_health(self) -> None:
        """Check AI management health status."""
        try:
            if len(self.api_key_requests) > 100:
                self.logger.warning(
                    f"High number of API key requests: {len(self.api_key_requests)}"
                )
            if len(self.workflow_executions) > 500:
                self.logger.info(
                    f"Large workflow execution history: {len(self.workflow_executions)} records"
                )
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to check AI management health: {e}")

    def get_ai_management_stats(self) -> Dict[str, Any]:
        """Get AI management statistics."""
        try:
            stats = {
                "total_models": len(self.models),
                "total_workflows": len(self.active_workflows),
                "model_registrations_count": len(self.model_registrations),
                "workflow_executions_count": len(self.workflow_executions),
                "api_key_requests_count": len(self.api_key_requests),
                "manager_status": self.status.value,  # type: ignore[attr-defined]
                "manager_uptime": self.metrics.uptime_seconds,  # type: ignore[attr-defined]
            }
            self.record_operation("get_ai_management_stats", True, 0.0)
            return stats
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to get AI management stats: {e}")
            self.record_operation("get_ai_management_stats", False, 0.0)
            return {"error": str(e)}
