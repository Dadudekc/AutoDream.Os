from pathlib import Path

from src.core.reporting.unified_reporting_framework import (
    UnifiedReportingFramework,
    ReportType,
    ReportFormat,
    ReportConfig,
    UnifiedReport,
)


class DummyFramework(UnifiedReportingFramework):
    """Concrete subclass for testing"""

    def _on_start(self) -> None:  # pragma: no cover - test stub
        pass

    def _on_stop(self) -> None:  # pragma: no cover - test stub
        pass

    def _on_initialize_resources(self) -> None:  # pragma: no cover - test stub
        pass

    def _on_cleanup_resources(self) -> None:  # pragma: no cover - test stub
        pass

    def _on_heartbeat(self) -> None:  # pragma: no cover - test stub
        pass

    def _on_recovery_attempt(self) -> None:  # pragma: no cover - test stub
        pass


def test_generate_report_for_each_type():
    Path("reports").mkdir(exist_ok=True)
    framework = DummyFramework("test_manager")
    test_cases = [
        (ReportType.SECURITY, {"vulnerabilities": []}),
        (ReportType.COMPLIANCE, {"issues": []}),
        (ReportType.QUALITY, {"quality_metrics": {}, "issues": []}),
        (ReportType.ANALYTICS, {"metrics": {}, "insights": []}),
        (ReportType.FINANCIAL, {"transactions": []}),
        (ReportType.CUSTOM, {"content": {}}),
    ]

    for report_type, data in test_cases:
        report = framework.generate_report(report_type, data)
        assert isinstance(report, UnifiedReport)
        assert report.metadata.report_type == report_type


def test_html_output_via_configuration(tmp_path: Path):
    Path("reports").mkdir(exist_ok=True)
    framework = DummyFramework("test_manager")
    config = ReportConfig(
        report_type=ReportType.SECURITY,
        format=ReportFormat.HTML,
        output_directory=str(tmp_path),
    )

    report = framework.generate_report(
        ReportType.SECURITY, {"vulnerabilities": []}, config=config
    )

    file_path = framework.save_report(report)
    assert file_path.endswith(".html")
    content = Path(file_path).read_text(encoding="utf-8")
    assert "<html>" in content.lower()
