"""Base engine providing common initialization, status, and cleanup.

Child classes should override :meth:`clear_resources` to release engine-
specific resources. The class maintains a single source of truth for engine
state through the ``is_initialized`` flag and ``status`` string.
"""

from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict


class BaseEngine:
    """Provide shared engine lifecycle management."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.is_initialized = False
        self.status = "INACTIVE"

    def initialize(self) -> bool:
        """Initialize engine state.

        Returns:
            True when initialization succeeds, False otherwise.
        """
        try:
            self.is_initialized = True
            self.status = "ACTIVE"
            self.logger.info("%s initialized", self.__class__.__name__)
            return True
        except Exception as exc:  # pragma: no cover - defensive log
            self.logger.error(
                "Failed to initialize %s: %s", self.__class__.__name__, exc
            )
            return False

    def get_status(self) -> Dict[str, Any]:
        """Return basic engine status metadata."""
        return {
            "is_initialized": self.is_initialized,
            "status": self.status,
            "timestamp": datetime.now().isoformat(),
        }

    def clear_resources(self) -> None:
        """Clear engine-specific resources.

        Child classes should override this to remove runtime data or close
        connections. The default implementation does nothing.
        """

    def shutdown(self) -> None:
        """Cleanup resources and reset lifecycle flags."""
        self.clear_resources()
        self.is_initialized = False
        self.status = "INACTIVE"
        self.logger.info("%s shutdown completed", self.__class__.__name__)
