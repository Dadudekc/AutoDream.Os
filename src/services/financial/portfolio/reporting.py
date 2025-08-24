"""Reporting utilities for portfolio performance tracking."""

import logging
from datetime import datetime
from typing import Dict, List, Optional

from .data_management import PerformanceDataManager
from .models import PerformanceReport, PerformanceSnapshot

logger = logging.getLogger(__name__)


class PerformanceReporter:
    """Generate reports from performance history."""

    def __init__(self, data_manager: PerformanceDataManager) -> None:
        self.data_manager = data_manager

    # ------------------------------------------------------------------
    def generate_report(
        self,
        history: List[PerformanceSnapshot],
        start_date: datetime,
        end_date: datetime,
    ) -> Optional[PerformanceReport]:
        """Create a :class:`PerformanceReport` from snapshots."""

        try:
            period = [s for s in history if start_date <= s.timestamp <= end_date]
            if len(period) < 2:
                logger.warning("Insufficient data for performance report")
                return None

            period.sort(key=lambda s: s.timestamp)
            start_value = period[0].total_value
            end_value = period[-1].total_value
            total_return = (
                (end_value - start_value) / start_value if start_value else 0.0
            )

            report = PerformanceReport(
                report_id=f"PERF_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}",
                start_date=start_date,
                end_date=end_date,
                portfolio_value_start=start_value,
                portfolio_value_end=end_value,
                total_return=total_return,
            )

            self.data_manager.save_report(report)
            return report
        except Exception as exc:  # pragma: no cover - defensive
            logger.error(f"Error generating performance report: {exc}")
            return None
