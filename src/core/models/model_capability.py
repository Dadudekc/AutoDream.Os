"""Model capability metadata."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class ModelCapability:
    """Describes a single capability of an AI model."""

    name: str
    description: str
    version: str
    is_supported: bool = True
    parameters: Dict[str, Any] = field(default_factory=dict)
