"""Configuration for V2 standards checking.

This module defines line count limits and component categories used by
standards checker modules. Keeping configuration in a dedicated module
allows tests and utilities to share the same values without importing the
larger orchestrator.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class StandardsConfig:
    """Line count limits for various component types."""

    MAX_LOC_STANDARD: int = 400
    MAX_LOC_GUI: int = 600
    MAX_LOC_CORE: int = 400

    COMPONENTS: Dict[str, str] = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "COMPONENTS",
            {
                "core": "Core system components",
                "services": "Service layer components",
                "launchers": "Launcher components",
                "utils": "Utility components",
                "web": "Web interface components",
            },
        )


def get_category_limit(category: str, config: StandardsConfig) -> int:
    """Return LOC limit for the given category."""

    mapping = {
        "web": config.MAX_LOC_GUI,
        "core": config.MAX_LOC_CORE,
        "services": config.MAX_LOC_CORE,
        "launchers": config.MAX_LOC_CORE,
        "utils": config.MAX_LOC_CORE,
    }
    return mapping.get(category, config.MAX_LOC_STANDARD)
