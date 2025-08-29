"""Unified AI model representation."""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional

from .model_capability import ModelCapability
from .model_metrics import ModelMetrics
from .model_utils import ModelType, Provider


@dataclass
class AIModel:
    """Metadata and configuration for an AI model."""

    model_id: str
    name: str
    model_type: ModelType
    provider: Provider
    version: str
    capabilities: List[ModelCapability]
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    last_used: Optional[datetime] = None
    usage_count: int = 0
    metrics: ModelMetrics = field(default_factory=ModelMetrics)

    # Configuration
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

    # Resource requirements
    memory_requirement: Optional[str] = None
    gpu_requirement: Optional[str] = None
    storage_requirement: Optional[str] = None

    def __post_init__(self) -> None:
        """Normalize enum values after initialization."""
        if isinstance(self.model_type, str):
            self.model_type = ModelType(self.model_type)
        if isinstance(self.provider, str):
            self.provider = Provider(self.provider)

    def to_dict(self) -> Dict[str, Any]:
        """Return a JSON-serialisable representation of the model."""
        return asdict(self)

    def update_metrics(self, success: bool, response_time: float) -> None:
        """Update metrics using the result of a request."""
        self.metrics.total_requests += 1
        if success:
            self.metrics.successful_requests += 1
        else:
            self.metrics.failed_requests += 1

        if self.metrics.total_requests == 1:
            self.metrics.average_response_time = response_time
        else:
            self.metrics.average_response_time = (
                (self.metrics.average_response_time * (self.metrics.total_requests - 1) + response_time)
                / self.metrics.total_requests
            )

        self.metrics.error_rate = self.metrics.failed_requests / self.metrics.total_requests
