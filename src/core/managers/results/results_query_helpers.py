"""
Results Query Helpers
=====================

Extract query and archive operations for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""

from datetime import datetime
from typing import Any

from ..contracts import ManagerContext, ManagerResult
from .results_processing import ResultStatus


class ResultsQueryHelper:
    """Handles result querying operations."""

    @staticmethod
    def get_results_filtered(
        results: dict, archived_results: dict, payload: dict[str, Any], context: ManagerContext
    ) -> ManagerResult:
        """Get results with optional filtering."""
        try:
            result_id = payload.get("result_id")
            result_type = payload.get("result_type")
            status = payload.get("status")
            include_archived = payload.get("include_archived", False)

            combined_results = dict(results)
            if include_archived:
                combined_results.update(archived_results)

            if result_id:
                combined_results = {k: v for k, v in combined_results.items() if k == result_id}
            if result_type:
                combined_results = {
                    k: v for k, v in combined_results.items() if v.get("type") == result_type
                }
            if status:
                combined_results = {
                    k: v for k, v in combined_results.items() if v.get("status") == status
                }

            return ManagerResult(
                success=True,
                data={"results": combined_results},
                metrics={"results_found": len(combined_results)},
            )
        except Exception as e:
            context.logger(f"Error getting results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))

    @staticmethod
    def archive_results_batch(
        results: dict, archived_results: dict, payload: dict[str, Any], context: ManagerContext
    ) -> ManagerResult:
        """Archive results."""
        try:
            result_ids = payload.get("result_ids", [])
            archive_all = payload.get("archive_all", False)

            if archive_all:
                result_ids = list(results.keys())

            archived_count = 0
            for result_id in result_ids:
                if result_id in results:
                    result = results[result_id]
                    result["status"] = ResultStatus.ARCHIVED.value
                    result["archived_at"] = datetime.now().isoformat()
                    archived_results[result_id] = result
                    del results[result_id]
                    archived_count += 1

            return ManagerResult(
                success=True,
                data={"archived_count": archived_count},
                metrics={"results_archived": archived_count},
            )
        except Exception as e:
            context.logger(f"Error archiving results: {e}")
            return ManagerResult(success=False, data={}, metrics={}, error=str(e))
