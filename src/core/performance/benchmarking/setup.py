"""Benchmark setup utilities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .benchmark_types import BenchmarkConfig
from .benchmark_runner import BenchmarkRunner


@dataclass
class BenchmarkSetup:
    """Prepare benchmark execution environment."""

    config: BenchmarkConfig

    def create_runner(self) -> BenchmarkRunner:
        """Instantiate a benchmark runner for the configured benchmark."""
        return BenchmarkRunner()

    def parameters(self) -> Dict[str, Any]:
        """Return benchmark parameters from configuration."""
        return self.config.metadata.get("parameters", {})

__all__ = ["BenchmarkSetup"]
