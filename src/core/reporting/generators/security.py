"""Security report generator."""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any, Dict

from ..report_models import ReportMetadata, ReportType, UnifiedReport
from .base import ReportGenerator


class SecurityReportGenerator(ReportGenerator):
    """Generates security reports."""

    def generate_report(self, data: Dict[str, Any], **kwargs) -> UnifiedReport:
        """Generate a security report."""
        vulnerabilities = data.get("vulnerabilities", [])
        severity_counts: Dict[str, int] = {}
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "unknown")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1

        content = {
            "vulnerability_summary": {
                "total_vulnerabilities": len(vulnerabilities),
                "severity_counts": severity_counts,
            },
            "vulnerabilities": vulnerabilities,
        }

        summary = f"Security Report: {len(vulnerabilities)} vulnerabilities detected"

        metadata = ReportMetadata(
            report_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            report_type=ReportType.SECURITY,
            format=self.config.format,
            priority=self.config.priority,
            source_system="unified_security_system",
        )

        return UnifiedReport(metadata=metadata, content=content, summary=summary)
