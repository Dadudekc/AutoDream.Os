"""
Vision System - V2 Compliant
============================

Screen capture, OCR, and visual analysis capabilities for agent coordination.
Integrates with V2's coordinate system for agent-specific screen regions.

V2 Compliance: All files ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Vision & Automation Specialist
License: MIT
"""

from .analysis import VisualAnalyzer
from .capture import ScreenCapture
from .integration import VisionSystem
from .ocr import TextExtractor

__all__ = [
    "ScreenCapture",
    "TextExtractor",
    "VisualAnalyzer",
    "VisionSystem",
]

__version__ = "2.0.0"
__author__ = "Agent-1 - Vision & Automation Specialist"
