#!/usr/bin/env python3
"""Data models for the constants consolidation system."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ConstantDefinition:
    """Represents a constant definition found in a file."""

    name: str
    value: Any
    file_path: str
    line_number: int
    description: str = ""
    category: str = "unknown"
