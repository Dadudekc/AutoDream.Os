#!/usr/bin/env python3
"""Common base for agent communication engines."""

from __future__ import annotations

import logging


class AgentCommunicationEngineBase:
    """Provides shared utilities for communication engine variants."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self._unified_utility = None

    def _get_unified_utility(self):
        """Lazily load unified utility instance."""
        if self._unified_utility is None:
            from ..core.unified_utility import get_unified_utility

            self._unified_utility = get_unified_utility()
        return self._unified_utility


__all__ = ["AgentCommunicationEngineBase"]
