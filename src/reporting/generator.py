"""High-level interface for generating error analytics reports."""

from pathlib import Path
import uuid
from typing import Dict, Any, List

from .config import (
    DEFAULT_FORMAT,
    INCLUDE_METADATA,
    INCLUDE_RECOMMENDATIONS,
    ReportFormat,
)
from .data_loader import ErrorDataLoader
from .models import AnalyticsReport
from .output import ReportOutput
from .report_composer import (
    create_report_summary,
    generate_recommendations,
    create_report_metadata,
)


class ErrorReportGenerator:
    """Coordinate data loading, report composition, and output."""

    def __init__(self, output_dir: Path | None = None):
        self.loader = ErrorDataLoader()
        self.output = ReportOutput(output_dir or Path("reports"))

    def generate(
        self,
        patterns_path: Path,
        trends_path: Path,
        correlations_path: Path,
        format_type: ReportFormat = DEFAULT_FORMAT,
    ) -> Path:
        """Generate a report from the provided data sources."""
        patterns, trends, correlations = self.loader.load(
            patterns_path, trends_path, correlations_path
        )

        summary = create_report_summary(patterns, trends, correlations)
        recommendations: List[str] = []
        if INCLUDE_RECOMMENDATIONS:
            recommendations = generate_recommendations(patterns, trends, correlations)

        metadata: Dict[str, Any] = {}
        if INCLUDE_METADATA:
            metadata = create_report_metadata(patterns, trends, correlations)

        report_id = f"error_analytics_{uuid.uuid4()}"
        report = AnalyticsReport.create(
            report_id=report_id,
            summary=summary,
            patterns=patterns,
            trends=trends,
            correlations=correlations,
            recommendations=recommendations,
            metadata=metadata,
        )

        return self.output.output(report, format_type)
