"""Compliance report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class ComplianceReportGenerator(ReportGenerator):
    """Generates compliance reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a compliance report."""
        issues = data.get("issues", [])
        compliance_score = data.get("compliance_score", 0)

        content = {
            "compliance_summary": {
                "total_issues": len(issues),
                "compliance_score": compliance_score,
            },
            "issues": issues,
        }

        summary = (
            f"Compliance Report: {len(issues)} issues found (Score: {compliance_score})"
        )

        recommendations = []
        if compliance_score < 100 and issues:
            recommendations.append(
                "Compliance issues detected - review required policies"
            )

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.COMPLIANCE,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_compliance_system",
        )

        return UnifiedReport(
            metadata=metadata,
            content=content,
            summary=summary,
            recommendations=recommendations,
        )
