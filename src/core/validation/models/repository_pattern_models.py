#!/usr/bin/env python3
"""
Repository Pattern Models - Agent Cellphone V2
=============================================

Data models and enums for repository pattern validation.
Extracted from repository_pattern_validator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional
from datetime import datetime

class RepositoryPatternType(Enum):
    """Types of repository patterns."""
    GENERIC_REPOSITORY = "generic_repository"
    SPECIFIC_REPOSITORY = "specific_repository"
    UNIT_OF_WORK = "unit_of_work"
    SPECIFICATION_PATTERN = "specification_pattern"
    CQRS_PATTERN = "cqrs_pattern"

@dataclass
class RepositoryPatternProfile:
    """Repository pattern validation profile."""
    file_path: str
    pattern_type: RepositoryPatternType
    classes_found: List[str]
    interfaces_found: List[str]
    methods_found: List[str]
    v2_compliant: bool = False
    pattern_score: float = 0.0
    implementation_quality: float = 0.0
    separation_score: float = 0.0

@dataclass
class RepositoryPatternMetrics:
    """Repository pattern validation metrics."""
    total_files_analyzed: int
    v2_compliant_files: int
    pattern_implementations: int
    generic_repositories: int
    specific_repositories: int
    unit_of_work_patterns: int
    specification_patterns: int
    cqrs_patterns: int
    average_pattern_score: float
    average_implementation_quality: float

@dataclass
class RepositoryPatternResult:
    """Repository pattern validation result."""
    file_path: str
    pattern_type: RepositoryPatternType
    is_v2_compliant: bool
    pattern_score: float
    implementation_quality: float
    separation_score: float
    issues: List[str]
    recommendations: List[str]
    classes_implemented: List[str]
    interfaces_implemented: List[str]
    methods_implemented: List[str]
    estimated_effort: int

@dataclass
class RepositoryPatternConfig:
    """Repository pattern validation configuration."""
    max_file_lines: int = 300
    min_pattern_score: float = 70.0
    min_implementation_quality: float = 60.0
    min_separation_score: float = 50.0
    required_interfaces: List[str] = field(default_factory=lambda: ["IRepository", "IUnitOfWork"])
    required_methods: List[str] = field(default_factory=lambda: ["GetById", "GetAll", "Add", "Update", "Delete"])
    pattern_indicators: Dict[str, List[str]] = field(default_factory=lambda: {
        "repository_keywords": ["Repository", "Repo", "DataAccess", "DataStore"],
        "interface_keywords": ["Interface", "I", "Contract", "Abstract"],
        "method_keywords": ["Get", "Find", "Add", "Update", "Delete", "Save", "Remove"]
    })

@dataclass
class RepositoryPatternThresholds:
    """Repository pattern validation thresholds."""
    excellent_score: float = 90.0
    good_score: float = 75.0
    acceptable_score: float = 60.0
    poor_score: float = 40.0
    excellent_quality: float = 85.0
    good_quality: float = 70.0
    acceptable_quality: float = 55.0
    poor_quality: float = 35.0
