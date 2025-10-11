"""
Vision Analyzers - Modular Computer Vision Components
====================================================

Focused analyzer modules following SOLID principles and V2 compliance.
Each analyzer provides specific computer vision functionality.

V2 Compliance: All modules ≤200 lines, single responsibility.

Author: Agent-7 - Repository Cloning Specialist (consolidation from vision/analysis.py)
License: MIT
"""

from .change_detector import ChangeDetector
from .color_analyzer import ColorAnalyzer
from .edge_analyzer import EdgeAnalyzer
from .ui_detector import UIDetector

__all__ = [
    "UIDetector",
    "EdgeAnalyzer",
    "ColorAnalyzer",
    "ChangeDetector",
]
