import json
from pathlib import Path

import pytest

# Skip these tests if psutil isn't available since health metrics rely on it
pytest.importorskip("psutil")

from core.health.reporting import (
    ReportType,
    ReportFormat,
    ReportConfig,
    ReportGenerator,
    ReportFormatter,
    ReportDelivery,
    HealthReportingGenerator,
)


def sample_data():
    health = {
        "agents": {
            "agent_1": {
                "overall_status": "good",
                "health_score": 90.0,
                "metrics": {"cpu": {"value": 50, "unit": "%"}},
            }
        }
    }
    alerts = {"alerts": [{"severity": "warning", "agent_id": "agent_1"}]}
    cfg = ReportConfig(report_type=ReportType.DAILY_SUMMARY, format=ReportFormat.JSON)
    return health, alerts, cfg


def test_report_generator_basic():
    health, alerts, cfg = sample_data()
    gen = ReportGenerator()
    report = gen.generate_report(health, alerts, cfg)
    assert report.summary["total_agents"] == 1
    assert report.alerts_data["total_alerts"] == 1


def test_report_formatter_json():
    health, alerts, cfg = sample_data()
    gen = ReportGenerator()
    report = gen.generate_report(health, alerts, cfg)
    formatter = ReportFormatter()
    output = formatter.format(report, ReportFormat.JSON)
    data = json.loads(output)
    assert data["report_id"] == report.report_id
    assert data["summary"]["total_agents"] == 1


def test_report_delivery_writes_file(tmp_path: Path):
    health, alerts, cfg = sample_data()
    gen = ReportGenerator()
    report = gen.generate_report(health, alerts, cfg)
    delivery = ReportDelivery(reports_dir=tmp_path)
    path = delivery.deliver(report, ReportFormat.JSON)
    assert path is not None and path.exists()


def test_full_generation_flow(tmp_path: Path):
    health, alerts, cfg = sample_data()
    cfg.format = ReportFormat.JSON
    service = HealthReportingGenerator({"reports_dir": tmp_path})
    report = service.generate_report(health, alerts, cfg)
    saved = list(tmp_path.glob("*.json"))
    assert report.report_id in saved[0].stem
