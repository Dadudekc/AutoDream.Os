"""Handoff detection subsystem."""

from typing import Any


class HandoffDetector:
    """Determine if a handoff should occur."""

    def should_handoff(self, context: Any) -> bool:
        """Return True when a handoff should be executed.

        Args:
            context: Handoff context information.

        Returns:
            True if a handoff is required.
        """
        return True
