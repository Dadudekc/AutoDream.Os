"""Integration tests for the new data orchestration system."""
from __future__ import annotations

import os
import tempfile

from src.core.data_sources import (
    DataSource,
    DataSourceType,
    DataType,
    DataPriority,
)
from src.core.data_orchestrator import DataOrchestrator
from src.core.data_transform import DataValidationEngine


def test_validation_engine() -> None:
    validator = DataValidationEngine()
    data = {"symbol": "AAPL", "price": 150.0, "timestamp": "2025-01-01"}
    result = validator.validate_data(data, DataType.MARKET)
    assert result["valid"]


def test_data_orchestrator_register_and_list() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = os.path.join(tmp, "sources.db")
        orchestrator = DataOrchestrator(db_path)
        source = DataSource(
            id="test",
            name="Test Source",
            type=DataSourceType.API,
            data_type=DataType.SYSTEM,
            location="test/location",
            priority=DataPriority.HIGH,
        )
        assert orchestrator.register_data_source(source)
        sources = orchestrator.list_data_sources()
        assert len(sources) == 1
        assert sources[0].name == "Test Source"
        status = orchestrator.get_consolidation_status()
        assert status["total_sources"] == 1
