"""Facade for baseline measurement operations."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from core.managers.base_manager import BaseManager

from .calculations import compare_against_baseline
from .data_handler import (
    BaselineDataHandler,
    BaselineMetric,
    BaselineType,
    BaselineComparison,
    PerformanceBaseline,
)
from .reporting import export_baseline_data, get_system_status


class RefactoringBaselineMeasurements(BaseManager):
    """High-level interface for baseline data, calculations and reporting."""

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(config or {})
        self.data_handler = BaselineDataHandler(config)

    # Data handling proxies
    def create_baseline(
        self,
        name: str,
        description: str,
        baseline_type: BaselineType,
        metrics: Dict[str, BaselineMetric],
        version: str = "1.0.0",
        context: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
    ) -> str:
        return self.data_handler.create_baseline(
            name, description, baseline_type, metrics, version, context, tags
        )

    def update_baseline(
        self,
        baseline_id: str,
        updates: Dict[str, Any],
    ) -> bool:
        return self.data_handler.update_baseline(baseline_id, updates)

    def deprecate_baseline(self, baseline_id: str) -> bool:
        return self.data_handler.deprecate_baseline(baseline_id)

    def get_baseline(self, baseline_id: str) -> Optional[PerformanceBaseline]:
        return self.data_handler.get_baseline(baseline_id)

    def get_active_baselines(self) -> List[PerformanceBaseline]:
        return self.data_handler.get_active_baselines()

    # Calculation proxy
    def compare_against_baseline(
        self, baseline_id: str, current_metrics: Dict[str, float]
    ) -> Optional[BaselineComparison]:
        baseline = self.get_baseline(baseline_id)
        if not baseline:
            return None
        return compare_against_baseline(baseline, current_metrics)

    # Reporting proxies
    def export_baseline_data(
        self,
        output_path: str,
        format: str = "json",
    ) -> bool:
        return export_baseline_data(
            self.data_handler.baselines,
            self.data_handler.baseline_config,
            output_path,
            format,
        )

    def get_system_status(self) -> Dict[str, Any]:
        return get_system_status(
            self.data_handler.baselines, self.data_handler.baseline_config
        )


__all__ = ["RefactoringBaselineMeasurements"]
