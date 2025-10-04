#!/usr/bin/env python3
"""
Knowledge Base Models - Core Data Structures
============================================

Core data models for knowledge base system.
Defines principles, patterns, and anti-patterns structures.

V2 Compliance: ≤400 lines, focused data models module
Author: Agent-6 (Quality Assurance Specialist)
"""

from dataclasses import dataclass
from enum import Enum


class PrincipleCategory(Enum):
    """Categories of design principles."""

    SIMPLICITY = "simplicity"
    MAINTAINABILITY = "maintainability"
    PERFORMANCE = "performance"
    SECURITY = "security"
    TESTING = "testing"
    DOCUMENTATION = "documentation"


@dataclass
class DesignPrinciple:
    """Represents a design principle with examples and guidelines."""

    name: str
    category: PrincipleCategory
    description: str
    rationale: str
    examples: list[str]
    anti_examples: list[str]
    enforcement_level: str  # required, recommended, optional
    related_principles: list[str] = None

    def __post_init__(self):
        if self.related_principles is None:
            self.related_principles = []


@dataclass
class CodePattern:
    """Represents a preferred code pattern."""

    name: str
    pattern_type: str  # structural, behavioral, creational
    description: str
    code_example: str
    when_to_use: list[str]
    when_not_to_use: list[str]
    complexity_score: int  # 1-10, where 1 is simplest


@dataclass
class AntiPattern:
    """Represents an anti-pattern to avoid."""

    name: str
    description: str
    why_bad: str
    examples: list[str]
    how_to_fix: list[str]
    severity: str  # critical, high, medium, low


__all__ = ["PrincipleCategory", "DesignPrinciple", "CodePattern", "AntiPattern"]

