from pathlib import Path

from src.core.reporting.backends.file import FileReportBackend
from src.core.reporting.report_data_collector import ReportDataCollector
from src.core.reporting.report_formatter import ReportFormatter
from src.core.reporting.report_models import ReportFormat, ReportType
from src.core.reporting.report_storage import ReportStorage


def test_file_backend_saves_content(tmp_path: Path) -> None:
    backend = FileReportBackend()
    path = tmp_path / "report.txt"
    backend.save(path, "hello")
    assert path.read_text(encoding="utf-8") == "hello"


def test_report_storage_saves_report(tmp_path: Path) -> None:
    Path("reports").mkdir(exist_ok=True)
    collector = ReportDataCollector()
    formatter = ReportFormatter()
    collector.report_generators[ReportType.TESTING].output_dir = tmp_path
    storage = ReportStorage(collector, FileReportBackend())

    report = collector.generate(ReportType.TESTING, {"value": 1})
    formatted = formatter.format(report, ReportFormat.JSON)
    saved_path = storage.save(report, formatted, ReportFormat.JSON)

    saved = Path(saved_path)
    assert saved.is_file()
    assert saved.read_text(encoding="utf-8") == formatted
