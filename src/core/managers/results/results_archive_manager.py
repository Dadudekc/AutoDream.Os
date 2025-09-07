"""
Results Archive Manager - Phase-2 V2 Compliance Refactoring
============================================================

Handles results archiving and cleanup operations.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from __future__ import annotations
from typing import Dict, Any
from datetime import datetime, timedelta
from .base_results_manager import BaseResultsManager, ResultStatus


class ResultsArchiveManager(BaseResultsManager):
    """Manages results archiving and cleanup."""

    def __init__(self):
        """Initialize archive manager."""
        super().__init__()
        self.archive_retention_days = 90
        self.compression_enabled = True

    def execute(
        self, context, operation: str, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Execute archive operation."""
        try:
            if operation == "archive_old_results":
                return self._archive_old_results_operation(context, payload)
            elif operation == "cleanup_archives":
                return self._cleanup_archives_operation(context, payload)
            elif operation == "compress_archives":
                return self._compress_archives_operation(context, payload)
            else:
                return super().execute(context, operation, payload)
        except Exception as e:
            context.logger(f"Error executing archive operation {operation}: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _archive_old_results_operation(
        self, context, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Archive old results operation."""
        try:
            days_threshold = payload.get("days_threshold", self.archive_after_days)
            force_archive = payload.get("force_archive", False)
            
            cutoff_date = datetime.now() - timedelta(days=days_threshold)
            to_archive = []
            
            for result_id, result in self.results.items():
                created_at = datetime.fromisoformat(result["created_at"])
                if created_at < cutoff_date or force_archive:
                    to_archive.append(result_id)
            
            archived_count = 0
            for result_id in to_archive:
                if self._archive_single_result(result_id):
                    archived_count += 1
            
            return ManagerResult(
                success=True,
                data={"archived_count": archived_count, "threshold_days": days_threshold},
                metrics={"results_archived": archived_count},
            )
            
        except Exception as e:
            context.logger(f"Error archiving old results: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _cleanup_archives_operation(
        self, context, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Cleanup old archives operation."""
        try:
            retention_days = payload.get("retention_days", self.archive_retention_days)
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            
            to_remove = []
            for result_id, result in self.archived_results.items():
                archived_at = datetime.fromisoformat(result.get("archived_at", result["created_at"]))
                if archived_at < cutoff_date:
                    to_remove.append(result_id)
            
            for result_id in to_remove:
                del self.archived_results[result_id]
            
            return ManagerResult(
                success=True,
                data={"removed_count": len(to_remove), "retention_days": retention_days},
                metrics={"archives_cleaned": len(to_remove)},
            )
            
        except Exception as e:
            context.logger(f"Error cleaning up archives: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _compress_archives_operation(
        self, context, payload: Dict[str, Any]
    ) -> ManagerResult:
        """Compress archives operation."""
        try:
            if not self.compression_enabled:
                return ManagerResult(
                    success=True,
                    data={"compression_enabled": False},
                    metrics={"archives_compressed": 0},
                )
            
            compressed_count = 0
            for result_id, result in self.archived_results.items():
                if self._compress_single_archive(result_id, result):
                    compressed_count += 1
            
            return ManagerResult(
                success=True,
                data={"compressed_count": compressed_count},
                metrics={"archives_compressed": compressed_count},
            )
            
        except Exception as e:
            context.logger(f"Error compressing archives: {e}")
            return ManagerResult(
                success=False, data={}, metrics={}, error=str(e)
            )

    def _archive_single_result(self, result_id: str) -> bool:
        """Archive a single result."""
        try:
            if result_id not in self.results:
                return False
            
            result = self.results[result_id]
            result["status"] = ResultStatus.ARCHIVED.value
            result["archived_at"] = datetime.now().isoformat()
            
            self.archived_results[result_id] = result
            del self.results[result_id]
            
            return True
            
        except Exception:
            return False

    def _compress_single_archive(self, result_id: str, result: Dict[str, Any]) -> bool:
        """Compress a single archive."""
        try:
            # Simple compression simulation
            if "compressed" not in result:
                result["compressed"] = True
                result["compressed_at"] = datetime.now().isoformat()
                result["compression_ratio"] = 0.7  # Simulated compression ratio
                return True
            
            return False
            
        except Exception:
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get archive manager status."""
        base_status = super().get_status()
        base_status.update({
            "archive_retention_days": self.archive_retention_days,
            "compression_enabled": self.compression_enabled,
            "compressed_archives": sum(
                1 for r in self.archived_results.values() 
                if r.get("compressed", False)
            ),
        })
        return base_status
