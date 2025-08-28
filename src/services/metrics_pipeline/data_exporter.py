"""Export metrics to external storage formats."""

from __future__ import annotations

import json
from typing import Dict, List

from .metrics_config import DEFAULT_EXPORT_PATH, MetricRecord


class MetricsExporter:
    """Handles exporting collected metrics to JSON files."""

    def export(
        self,
        metrics: Dict[str, List[MetricRecord]],
        filename: str = DEFAULT_EXPORT_PATH,
    ) -> bool:
        """Export ``metrics`` to ``filename``.

        Returns ``True`` if the export succeeds, otherwise ``False``.
        """

        try:
            serializable = {
                name: [record.__dict__ for record in values]
                for name, values in metrics.items()
            }
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(serializable, f, indent=2)
            return True
        except OSError:
            return False


__all__ = ["MetricsExporter"]
