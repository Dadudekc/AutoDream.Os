#!/usr/bin/env python3
"""
QA Coordination Data Models
==========================

Data models and enums for Agent-6 & Agent-8 Enhanced QA Coordination
V2 Compliant: ≤400 lines, focused data structures
"""

from typing import Dict, List, Any
from dataclasses import dataclass
from enum import Enum


class QAEnhancementArea(Enum):
    """Quality Assurance enhancement areas"""
    VECTOR_DATABASE_INTEGRATION = "vector_database_integration"
    QUALITY_GATES_ENHANCEMENT = "quality_gates_enhancement"
    VALIDATION_PROTOCOLS = "validation_protocols"
    TESTING_FRAMEWORK = "testing_framework"
    PERFORMANCE_VALIDATION = "performance_validation"


class QAStatus(Enum):
    """Quality Assurance status levels"""
    EXCELLENT = "excellent"
    GOOD = "good"
    ACCEPTABLE = "acceptable"
    NEEDS_IMPROVEMENT = "needs_improvement"
    CRITICAL = "critical"


class EnhancementPriority(Enum):
    """Enhancement priority levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class QAEnhancement:
    """Quality Assurance enhancement definition"""
    area: QAEnhancementArea
    enhancement_name: str
    description: str
    priority: EnhancementPriority
    agent_responsible: str
    estimated_effort: int  # hours
    dependencies: List[str]
    success_criteria: Dict[str, Any]


@dataclass
class Phase3ConsolidationStatus:
    """Phase 3 consolidation status"""
    coordinate_loader: QAStatus
    ml_pipeline_core: QAStatus
    quality_assurance: QAStatus
    production_ready: bool
    vector_database_ready: bool


@dataclass
class ValidationResult:
    """Validation result structure"""
    test_name: str
    status: QAStatus
    score: float
    issues: List[str]
    recommendations: List[str]
    execution_time: float


@dataclass
class PerformanceMetrics:
    """Performance metrics structure"""
    metric_name: str
    current_value: float
    target_value: float
    unit: str
    status: QAStatus
    improvement_suggestions: List[str]


@dataclass
class QualityGate:
    """Quality gate definition"""
    gate_name: str
    criteria: Dict[str, Any]
    threshold: float
    status: QAStatus
    blocking: bool