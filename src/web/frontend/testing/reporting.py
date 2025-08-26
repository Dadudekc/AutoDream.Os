import logging
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover - for type hints only
    from ..frontend_testing import TestResult

logger = logging.getLogger(__name__)


class TestReportGenerator:
    """Generate aggregated test reports."""

    def __init__(self, output_dir: str = "test_reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    def aggregate_results(self, results: List["TestResult"]) -> Dict[str, Any]:
        """Aggregate basic statistics from test results."""
        total = len(results)
        passed = sum(1 for r in results if r.status == "passed")
        failed = sum(1 for r in results if r.status == "failed")
        skipped = sum(1 for r in results if r.status == "skipped")
        duration = sum(r.duration for r in results)
        return {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": duration,
            "timestamp": datetime.now().isoformat(),
            "results": [asdict(r) for r in results],
        }

    # ------------------------------------------------------------------
    def generate_report(
        self,
        results: List["TestResult"],
        fmt: str = "markdown",
        template: Optional[str] = None,
    ) -> str:
        """Generate a formatted report and return the file path."""
        data = self.aggregate_results(results)
        if fmt.lower() == "html":
            content = self._render_html(data, template)
            filename = (
                f"frontend_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
            )
        else:
            content = self._render_markdown(data, template)
            filename = (
                f"frontend_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            )

        path = self.output_dir / filename
        path.write_text(content, encoding="utf-8")
        logger.info("Saved test report: %s", path)
        return str(path)

    # ------------------------------------------------------------------
    def _render_markdown(self, data: Dict[str, Any], template: Optional[str]) -> str:
        """Render report using Markdown template."""
        template = template or (
            "# Frontend Test Report\n\n"
            "- Generated: {timestamp}\n"
            "- Total Tests: {total}\n"
            "- Passed: {passed}\n"
            "- Failed: {failed}\n"
            "- Skipped: {skipped}\n"
            "- Total Duration: {duration:.2f}s\n"
        )
        return template.format(**data)

    # ------------------------------------------------------------------
    def _render_html(self, data: Dict[str, Any], template: Optional[str]) -> str:
        """Render report using HTML template."""
        template = template or (
            "<html><body><h1>Frontend Test Report</h1>"
            "<ul>"
            "<li>Generated: {timestamp}</li>"
            "<li>Total Tests: {total}</li>"
            "<li>Passed: {passed}</li>"
            "<li>Failed: {failed}</li>"
            "<li>Skipped: {skipped}</li>"
            "<li>Total Duration: {duration:.2f}s</li>"
            "</ul></body></html>"
        )
        return template.format(**data)
