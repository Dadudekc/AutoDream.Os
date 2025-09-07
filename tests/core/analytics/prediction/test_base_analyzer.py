"""Tests for BasePredictionAnalyzer."""

import importlib.util
from enum import Enum
from pathlib import Path

module_path = Path(__file__).resolve().parents[4] / "src" / "core" / "analytics" / "prediction" / "base_analyzer.py"
spec = importlib.util.spec_from_file_location("base_analyzer", module_path)
base_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base_module)
BasePredictionAnalyzer = base_module.BasePredictionAnalyzer


class DummyLevel(Enum):
    VERY_HIGH = "very_high"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


def test_normalize_probability_clamps_values():
    assert BasePredictionAnalyzer.normalize_probability(1.2) == 1.0
    assert BasePredictionAnalyzer.normalize_probability(-0.1) == 0.0


def test_confidence_level_returns_label():
    assert BasePredictionAnalyzer.confidence_level(0.72) == "high"


def test_confidence_level_custom_mapping():
    mapping = {
        "very_high": DummyLevel.VERY_HIGH,
        "high": DummyLevel.HIGH,
        "medium": DummyLevel.MEDIUM,
        "low": DummyLevel.LOW,
    }
    assert BasePredictionAnalyzer.confidence_level(0.85, mapping) == DummyLevel.HIGH
