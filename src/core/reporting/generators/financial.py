"""Financial report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class FinancialReportGenerator(ReportGenerator):
    """Generates financial reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a financial report."""
        transactions = data.get("transactions", [])
        total_amount = sum(t.get("amount", 0) for t in transactions)

        content = {
            "financial_summary": {
                "transaction_count": len(transactions),
                "total_amount": total_amount,
            },
            "transactions": transactions,
        }

        summary = f"Financial Report: {len(transactions)} transactions totaling {total_amount:.2f}"

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.FINANCIAL,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_financial_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)
