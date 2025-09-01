#!/usr/bin/env python3
"""
Phase 3 Validation Models - Agent Cellphone V2
=============================================

Data models and enums for Phase 3 validation coordination.
Extracted from phase3_validation_coordinator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime

class Phase3ValidationType(Enum):
    """Types of Phase 3 validation activities."""
    CLI_MODULAR_VALIDATION = "cli_modular_validation"
    JAVASCRIPT_V2_VALIDATION = "javascript_v2_validation"
    REPOSITORY_PATTERN_VALIDATION = "repository_pattern_validation"
    GAMING_PERFORMANCE_VALIDATION = "gaming_performance_validation"
    CROSS_AGENT_COORDINATION = "cross_agent_coordination"
    INTEGRATION_TESTING = "integration_testing"

@dataclass
class Phase3ValidationProfile:
    """Phase 3 validation profile for an agent."""
    agent_id: str
    agent_name: str
    validation_type: Phase3ValidationType
    target_files: List[str]
    validation_status: str = "pending"
    validation_results: Dict[str, Any] = field(default_factory=dict)
    compliance_score: float = 0.0
    achievements: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    last_validated: Optional[datetime] = None

@dataclass
class Phase3ValidationResult:
    """Phase 3 validation execution result."""
    validation_type: Phase3ValidationType
    agent_id: str
    execution_time: float
    validation_results: Dict[str, Any]
    compliance_score: float
    achievements: List[str]
    recommendations: List[str]
    timestamp: datetime

@dataclass
class Phase3ValidationConfig:
    """Phase 3 validation configuration."""
    validation_type: Phase3ValidationType
    priority: str
    target_reduction: int
    max_file_lines: int
    required_patterns: List[str]
    timeout_seconds: int = 300
    retry_attempts: int = 3
    parallel_execution: bool = True

@dataclass
class Phase3ValidationMetrics:
    """Phase 3 validation metrics."""
    total_validations: int
    successful_validations: int
    failed_validations: int
    average_execution_time: float
    total_compliance_score: float
    average_compliance_score: float
    validation_coverage: float
    cross_agent_coordinations: int
    integration_tests: int

@dataclass
class Phase3ValidationStrategy:
    """Phase 3 validation strategy."""
    strategy_name: str
    validation_types: List[Phase3ValidationType]
    execution_order: List[str]
    parallel_groups: List[List[str]]
    dependencies: Dict[str, List[str]]
    timeout_config: Dict[str, int]
    retry_config: Dict[str, int]
