"""Tests for validation pipeline assembly."""
from src.services.validation_pipeline import ValidationPipeline


def test_pipeline_runs_and_reports():
    pipeline = ValidationPipeline()
    contract = {
        "contract_id": "c1",
        "deadline": "2024-01-01",
        "delivery_date": "2024-02-01",
    }
    report = pipeline.run(contract)
    assert "results" in report and "summary" in report
    assert report["summary"]["failed"] >= 1
