"""Metric collection utilities for extended AI/ML managers."""

from dataclasses import dataclass


@dataclass
class MetricsCollector:
    """Simple container for operation metrics."""

    total_operations: int = 0
    successful_operations: int = 0
    failed_operations: int = 0

    def record_success(self) -> None:
        """Record a successful operation."""
        self.total_operations += 1
        self.successful_operations += 1

    def record_failure(self) -> None:
        """Record a failed operation."""
        self.total_operations += 1
        self.failed_operations += 1
