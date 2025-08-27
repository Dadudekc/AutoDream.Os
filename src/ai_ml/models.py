"""Data models for AI/ML components."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class AIModel:
    """AI model configuration and metadata."""

    name: str
    provider: str
    model_id: str
    version: str
    capabilities: List[str] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert model configuration to a serializable dictionary."""
        return {
            "name": self.name,
            "provider": self.provider,
            "model_id": self.model_id,
            "version": self.version,
            "capabilities": self.capabilities,
            "parameters": self.parameters,
            "created_at": self.created_at.isoformat(),
        }


__all__ = ["AIModel"]
