#!/usr/bin/env python3
"""
Configuration Models - V2 Compliance Module
============================================

Data models for configuration pattern detection.
Extracted from config_scanners.py for V2 compliance.

Author: Agent-4 (Captain) - V2 Refactoring & Autonomy Enhancement
License: MIT
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ConfigPattern:
    """Configuration pattern found in code."""

    file_path: Path
    line_number: int
    pattern_type: str
    key: str
    value: Any
    context: str
    source: str
