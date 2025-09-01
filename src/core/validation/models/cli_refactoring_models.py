#!/usr/bin/env python3
"""
CLI Refactoring Models - Agent Cellphone V2
==========================================

Data models and enums for CLI modular refactoring validation.
Extracted from cli_modular_refactoring_validator.py for V2 compliance.

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Any, Optional

class CLIRefactoringPattern(Enum):
    """Types of CLI refactoring patterns."""
    COMPONENT_EXTRACTION = "component_extraction"
    FACTORY_PATTERN = "factory_pattern"
    SERVICE_LAYER = "service_layer"
    DEPENDENCY_INJECTION = "dependency_injection"
    MODULAR_REFACTORING = "modular_refactoring"

@dataclass
class CLIModuleProfile:
    """CLI module refactoring profile."""
    module_name: str
    file_path: str
    original_lines: int
    target_lines: int
    reduction_percent: float
    refactoring_patterns: List[CLIRefactoringPattern] = field(default_factory=list)
    extracted_components: List[str] = field(default_factory=list)
    factory_implementations: List[str] = field(default_factory=list)
    service_layers: List[str] = field(default_factory=list)
    dependency_injections: List[str] = field(default_factory=list)
    modular_structures: List[str] = field(default_factory=list)
    v2_compliant: bool = False
    refactoring_score: float = 0.0

@dataclass
class CLIRefactoringMetrics:
    """CLI refactoring metrics."""
    total_files_analyzed: int
    v2_compliant_files: int
    refactoring_opportunities: int
    total_reduction_potential: int
    average_reduction_percent: float
    component_extractions: int
    factory_implementations: int
    service_layers: int
    dependency_injections: int
    modular_structures: int

@dataclass
class CLIRefactoringThresholds:
    """CLI refactoring validation thresholds."""
    max_file_lines: int = 200
    min_reduction_percent: float = 30.0
    min_component_separation: int = 3
    min_factory_implementations: int = 1
    min_service_layers: int = 1
    min_dependency_injections: int = 2
    min_modular_structures: int = 2

@dataclass
class CLIPatternIndicators:
    """CLI pattern detection indicators."""
    component_keywords: List[str] = field(default_factory=lambda: ["Component", "Module", "Handler", "Processor", "Manager"])
    factory_keywords: List[str] = field(default_factory=lambda: ["Factory", "Builder", "Creator", "Provider", "Generator"])
    service_keywords: List[str] = field(default_factory=lambda: ["Service", "Business", "Logic", "Operation", "Action"])
    dependency_keywords: List[str] = field(default_factory=lambda: ["Dependency", "Inject", "DI", "Container", "Resolver"])
    modular_keywords: List[str] = field(default_factory=lambda: ["Modular", "Separated", "Isolated", "Independent", "Decoupled"])

@dataclass
class CLIRefactoringResult:
    """CLI refactoring validation result."""
    file_path: str
    is_v2_compliant: bool
    refactoring_score: float
    issues: List[str]
    recommendations: List[str]
    extracted_components: List[str]
    refactoring_patterns: List[CLIRefactoringPattern]
    reduction_potential: int
    estimated_effort: int
