"""Results Processing - V2 Compliance | Agent-5"""
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable


class ResultStatus(Enum):
    """Result processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    ARCHIVED = "archived"


class ResultsProcessor:
    """Handles result processing operations."""
    
    def __init__(self, processors: dict, archived: dict, archive_days: int):
        """Initialize results processor."""
        self.result_processors = processors
        self.archived_results = archived
        self.archive_after_days = archive_days
    
    def process_result_by_type(
        self, context: Any, result_type: str, result_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Process result by type using registered processors."""
        if result_type in self.result_processors:
            try:
                return self.result_processors[result_type](result_data)
            except Exception as e:
                context.logger(f"Processor error for {result_type}: {e}")
                return {"error": str(e), "original_data": result_data}
        else:
            return {"processed": True, "original_data": result_data}
    
    def archive_old_results(self, results: dict) -> None:
        """Archive results older than archive_after_days."""
        try:
            cutoff_date = datetime.now() - timedelta(days=self.archive_after_days)
            to_archive = []
            for result_id, result in results.items():
                created_at = datetime.fromisoformat(result["created_at"])
                if created_at < cutoff_date:
                    to_archive.append(result_id)
            for result_id in to_archive:
                result = results[result_id]
                result["status"] = ResultStatus.ARCHIVED.value
                result["archived_at"] = datetime.now().isoformat()
                self.archived_results[result_id] = result
                del results[result_id]
        except Exception:
            pass

