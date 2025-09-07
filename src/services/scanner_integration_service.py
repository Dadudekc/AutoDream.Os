#!/usr/bin/env python3
"""Scanner Integration Service
================================

Combines scanner data with coordinate calibration.

This module consolidates functionality that previously lived in both
``8_agent_coordinate_calibrator.py`` and
``scanner_integration_service.py``.  The shared logic is now provided by
``ScannerIntegrationService``.
"""

from __future__ import annotations

import logging
from typing import Dict, Tuple

from src.utils.stability_improvements import safe_import

logger = logging.getLogger(__name__)


class ScannerIntegrationService:
    """Provide basic coordinate calibration for scanner results."""

    def __init__(self, x_offset: int = 0, y_offset: int = 0) -> None:
        self.x_offset = x_offset
        self.y_offset = y_offset

    def calibrate(self, x: int, y: int) -> Tuple[int, int]:
        """Apply offsets to raw coordinates."""
        calibrated = (x + self.x_offset, y + self.y_offset)
        logger.debug("Calibrated (%s, %s) -> %s", x, y, calibrated)
        return calibrated

    def process_scan(self, scan: Dict[str, int]) -> Dict[str, int]:
        """Normalize scanner output and apply calibration.

        Parameters
        ----------
        scan:
            Dictionary containing at least ``x`` and ``y`` keys.
        """

        x = scan.get("x", 0)
        y = scan.get("y", 0)
        cx, cy = self.calibrate(x, y)
        return {"x": cx, "y": cy}


__all__ = ["ScannerIntegrationService"]

