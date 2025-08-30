
# MIGRATED: This file has been migrated to the centralized configuration system

# MIGRATED: This file has been migrated to the centralized configuration system
"""Configuration data structures for ConfigManager modules.

These lightweight dataclasses store configuration metadata and values
without embedding any loading or validation logic. Keeping this module
small and focused maintains the single responsibility principle.
"""

from dataclasses import dataclass, field
from typing import Any, Dict
import time


@dataclass
class ConfigMetadata:
    """Basic metadata about a configuration source."""

    path: str
    loaded_at: float = field(default_factory=time.time)


@dataclass
class ConfigEntry:
    """Represents a named configuration section."""

    name: str
    data: Dict[str, Any]
    metadata: ConfigMetadata | None = None
