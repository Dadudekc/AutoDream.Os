"""
Pattern Analysis Enums - V2 Compliance Micro-refactoring
========================================================

Extracted enums for V2 compliance micro-refactoring.
KISS PRINCIPLE: Keep It Simple, Stupid - focused enum definitions.

Author: Agent-8 (SSOT & System Integration Specialist) - V2 Compliance Micro-refactoring
Original: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

from enum import Enum


class PatternType(Enum):
    """Pattern type."""
    PERFORMANCE = "performance"
    COORDINATION = "coordination"
    EFFICIENCY = "efficiency"
    RESOURCE = "resource"
    TIMING = "timing"
    SEQUENCE = "sequence"


class RecommendationType(Enum):
    """Recommendation type."""
    OPTIMIZATION = "optimization"
    COORDINATION = "coordination"
    RESOURCE_ALLOCATION = "resource_allocation"
    TIMING_ADJUSTMENT = "timing_adjustment"
    PROCESS_IMPROVEMENT = "process_improvement"


class ImpactLevel(Enum):
    """Impact level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AnalysisStatus(Enum):
    """Analysis status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class PatternCategory(Enum):
    """Pattern category."""
    SYSTEM = "system"
    AGENT = "agent"
    COORDINATION = "coordination"
    PERFORMANCE = "performance"
    RESOURCE = "resource"


class ConfidenceLevel(Enum):
    """Confidence level."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"
