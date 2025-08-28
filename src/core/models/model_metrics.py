"""Performance metrics for AI models."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ModelMetrics:
    """Runtime statistics collected for model usage."""

    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    average_response_time: float = 0.0
    last_request: Optional[datetime] = None
    error_rate: float = 0.0
    throughput: float = 0.0  # requests per second
