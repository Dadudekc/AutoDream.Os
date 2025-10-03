#!/usr/bin/env python3
"""
Aletheia Prompt Models - Core Data Structures
=============================================

Core data models for Aletheia prompt management system.
Defines prompt structures, metadata, and optimization data.

V2 Compliance: ≤400 lines, focused data models module
Author: Agent-6 (Quality Assurance Specialist)
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class PromptStatus(Enum):
    """Prompt status enumeration."""

    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DEPRECATED = "deprecated"


class PromptType(Enum):
    """Prompt type enumeration."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TEMPLATE = "template"


@dataclass
class PromptMetadata:
    """Prompt metadata structure."""

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    version: str = "1.0.0"
    author: str = "unknown"
    tags: list[str] = field(default_factory=list)
    description: str = ""
    usage_count: int = 0
    performance_score: float = 0.0


@dataclass
class PromptOptimization:
    """Prompt optimization data structure."""

    original_length: int
    optimized_length: int
    improvement_percentage: float
    optimization_techniques: list[str]
    performance_metrics: dict[str, Any]


__all__ = ["PromptStatus", "PromptType", "PromptMetadata", "PromptOptimization"]
