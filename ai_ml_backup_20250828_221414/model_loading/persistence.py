"""Persistence and health utilities for ModelManager."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


class PersistenceMixin:
    """Mixin handling persistence and health checks."""

    models: dict
    model_operations: list
    storage_operations: list
    api_key_operations: list
    manager_id: str
    logger: any

    def _save_model_management_data(self) -> None:
        """Save model management data to persistent storage."""
        try:
            persistence_dir = Path("data/persistent/ai_ml_models")
            persistence_dir.mkdir(parents=True, exist_ok=True)
            model_data = {
                "models": {k: v.__dict__ for k, v in self.models.items()},
                "model_operations": self.model_operations,
                "storage_operations": self.storage_operations,
                "api_key_operations": self.api_key_operations,
                "timestamp": datetime.now().isoformat(),
                "manager_id": self.manager_id,
                "version": "2.0.0",
            }
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"ai_ml_models_data_{timestamp}.json"
            filepath = persistence_dir / filename
            with open(filepath, "w") as f:
                json.dump(model_data, f, indent=2, default=str)
            self._cleanup_old_backups(persistence_dir, "ai_ml_models_data_*.json", 5)
            self.logger.info(f"Model management data saved to {filepath}")
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to save model management data: {e}")
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

    def _check_model_management_health(self) -> None:
        """Check model management health status."""
        try:
            if len(self.model_operations) > 1000:
                self.logger.warning(
                    f"High number of model operations: {len(self.model_operations)}"
                )
            if len(self.storage_operations) > 500:
                self.logger.info(
                    f"Large storage operations history: {len(self.storage_operations)} records"
                )
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to check model management health: {e}")

    def get_model_management_stats(self) -> Dict[str, Any]:
        """Get model management statistics."""
        try:
            stats = {
                "total_models": len(self.models),
                "model_operations_count": len(self.model_operations),
                "storage_operations_count": len(self.storage_operations),
                "api_key_operations_count": len(self.api_key_operations),
                "manager_status": self.status.value,  # type: ignore[attr-defined]
                "manager_uptime": self.metrics.uptime_seconds,  # type: ignore[attr-defined]
            }
            self.record_operation("get_model_management_stats", True, 0.0)
            return stats
        except Exception as e:  # pragma: no cover - defensive programming
            self.logger.error(f"Failed to get model management stats: {e}")
            self.record_operation("get_model_management_stats", False, 0.0)
            return {"error": str(e)}
