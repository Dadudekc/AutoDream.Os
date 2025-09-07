import json
import time
from pathlib import Path
from typing import Any, Dict, List, Optional


class AutomationMonitorMixin:
    """Provides monitoring utilities for automation orchestrator."""

    def _save_pipeline_artifacts(self, pipeline_id: str, results: Dict[str, Any]):
        """Save pipeline artifacts for later analysis."""
        try:
            artifacts_file = self.artifacts_dir / f"{pipeline_id}_results.json"
            serializable_results = self._make_serializable(results)
            with open(artifacts_file, "w", encoding="utf-8") as f:
                json.dump(serializable_results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Pipeline artifacts saved to {artifacts_file}")
        except Exception as e:
            self.logger.warning(f"Failed to save pipeline artifacts: {e}")

    def _make_serializable(self, obj: Any) -> Any:
        """Convert object to JSON serializable format."""
        if isinstance(obj, dict):
            return {k: self._make_serializable(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        if isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        return str(obj)

    def get_pipeline_status(self, pipeline_id: str) -> Optional[Dict[str, Any]]:
        """Get the status of a specific pipeline."""
        if pipeline_id in self.active_automations:
            return self.active_automations[pipeline_id]
        artifacts_file = self.artifacts_dir / f"{pipeline_id}_results.json"
        if artifacts_file.exists():
            try:
                with open(artifacts_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                self.logger.warning(f"Failed to load pipeline artifacts: {e}")
        return None

    def list_pipelines(self) -> List[Dict[str, Any]]:
        """List all pipelines (active and completed)."""
        pipelines = []
        for pipeline_id, status in self.active_automations.items():
            pipelines.append(
                {
                    "pipeline_id": pipeline_id,
                    "status": "active",
                    "current_step": status.get("current_step", "unknown"),
                }
            )
        for artifacts_file in Path(self.artifacts_dir).glob("*_results.json"):
            try:
                pipeline_id = artifacts_file.stem.replace("_results", "")
                with open(artifacts_file, "r", encoding="utf-8") as f:
                    results = json.load(f)
                pipelines.append(
                    {
                        "pipeline_id": pipeline_id,
                        "status": results.get("status", "unknown"),
                        "duration": results.get("duration", 0),
                        "completed_at": results.get("end_time", 0),
                    }
                )
            except Exception as e:
                self.logger.warning(f"Failed to load pipeline {artifacts_file}: {e}")
        return sorted(pipelines, key=lambda x: x.get("completed_at", 0), reverse=True)

    def cleanup_artifacts(self, older_than_days: int = 7):
        """Clean up old pipeline artifacts."""
        try:
            cutoff_time = time.time() - (older_than_days * 24 * 60 * 60)
            for artifacts_file in Path(self.artifacts_dir).glob("*_results.json"):
                if artifacts_file.stat().st_mtime < cutoff_time:
                    artifacts_file.unlink()
                    self.logger.info(f"Cleaned up old artifact: {artifacts_file}")
        except Exception as e:
            self.logger.warning(f"Failed to cleanup artifacts: {e}")
