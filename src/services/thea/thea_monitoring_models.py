#!/usr/bin/env python3
"""
Thea Monitoring Data Models - Core Data Structures
==================================================

Core data models for Thea monitoring system.
Defines performance metrics and system health structures.

V2 Compliance: ≤400 lines, focused data models module
Author: Agent-6 (Quality Assurance Specialist)
"""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass
class PerformanceMetrics:
    """Performance metrics for Thea operations."""

    timestamp: str
    operation: str
    duration: float
    success: bool
    memory_usage: float
    cpu_usage: float
    response_length: int
    error_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class SystemHealth:
    """System health status for Thea operations."""

    timestamp: str
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    network_connected: bool
    browser_running: bool
    cookies_valid: bool
    overall_health: str
    alerts: list[str] | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


__all__ = ["PerformanceMetrics", "SystemHealth"]
