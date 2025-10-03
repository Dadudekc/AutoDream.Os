"""
Unified Coordinate Loader Models - V2 Compliant
===============================================

Data models for coordinate loading system.
V2 Compliance: ≤400 lines, ≤5 classes, KISS principle
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional


class CoordinateSource(Enum):
    """Coordinate source enumeration."""
    
    PRIMARY = "primary"
    BACKUP = "backup"
    ENVIRONMENT = "environment"


@dataclass
class AgentCoordinates:
    """Agent coordinates data structure."""
    
    x: int
    y: int
    monitor: str
    description: str


@dataclass
class CoordinateConfig:
    """Coordinate configuration data structure."""
    
    version: str
    last_updated: str
    source: CoordinateSource
    agents: Dict[str, AgentCoordinates]


@dataclass
class LoadResult:
    """Coordinate loading result."""
    
    success: bool
    config: Optional[CoordinateConfig]
    error: Optional[str]
    source: Optional[CoordinateSource]


@dataclass
class ValidationResult:
    """Coordinate validation result."""
    
    valid: bool
    errors: List[str]
    warnings: List[str]