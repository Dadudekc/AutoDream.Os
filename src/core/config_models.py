#!/usr/bin/env python3
"""
Unified Configuration Models - Consolidated Configuration Data Structures

This module provides unified configuration models to eliminate duplication.
Follows Single Responsibility Principle - only configuration data structures.
Architecture: Single Responsibility Principle - configuration models only
LOC: Target 150 lines (under 200 limit)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pathlib import Path


class ConfigType(Enum):
    """Configuration file types"""

    JSON = "json"
    YAML = "yaml"
    INI = "ini"
    ENV = "env"


class ConfigValidationLevel(Enum):
    """Configuration validation levels"""

    BASIC = "basic"
    STANDARD = "standard"
    STRICT = "strict"


@dataclass
class ConfigSection:
    """Unified configuration section definition"""

    name: str
    data: Dict[str, Any]
    required: bool = False
    default_value: Any = None
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    description: str = ""
    source_file: Optional[str] = None
    last_modified: Optional[float] = None


@dataclass
class ConfigValidationResult:
    """Configuration validation result"""

    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    validation_level: ConfigValidationLevel = ConfigValidationLevel.STANDARD


@dataclass
class ConfigChangeEvent:
    """Configuration change event"""

    section_name: str
    change_type: str  # "added", "modified", "deleted"
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    timestamp: float = field(default_factory=lambda: __import__("time").time())
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConfigMetadata:
    """Configuration metadata"""

    version: str = "1.0.0"
    created_at: float = field(default_factory=lambda: __import__("time").time())
    last_modified: float = field(default_factory=lambda: __import__("time").time())
    author: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
