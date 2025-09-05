#!/usr/bin/env python3
"""
DRY Eliminator Models - V2 Compliance Module
============================================

Data models and configuration classes for advanced DRY violation elimination.
Extracted from monolithic advanced_dry_eliminator.py for V2 compliance.

Responsibilities:
- DRY violation detection and analysis models
- Elimination strategy configuration
- Result tracking and metrics structures
- File analysis and pattern identification
- Factory functions for model creation

V2 Compliance: < 300 lines, single responsibility, modular design.

Author: Captain Agent-4 - Strategic Oversight & Emergency Intervention Manager
Original: Agent-5 (Business Intelligence Specialist)
License: MIT
"""

from typing import Any, Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

# Import enums from dedicated module for V2 compliance micro-refactoring
from .dry_eliminator_enums import (
    DRYViolationType,
    EliminationStrategy,
    ViolationSeverity,
    DRYScanMode
)


@dataclass
class DRYViolation:
    """DRY violation data structure."""
    violation_id: str
    violation_type: DRYViolationType
    severity: ViolationSeverity
    file_path: str
    line_number: int
    code_snippet: str
    duplicate_locations: List[str] = field(default_factory=list)
    suggested_strategy: EliminationStrategy = EliminationStrategy.CONSOLIDATE
    estimated_effort: str = "medium"
    potential_savings: int = 0  # Lines of code
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate violation after initialization."""
        if not self.violation_id or not self.file_path:
            raise ValueError("Violation ID and file path are required")
        if self.line_number < 0:
            raise ValueError("Line number cannot be negative")
        if self.potential_savings < 0:
            raise ValueError("Potential savings cannot be negative")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'violation_id': self.violation_id,
            'violation_type': self.violation_type.value,
            'severity': self.severity.value,
            'file_path': self.file_path,
            'line_number': self.line_number,
            'code_snippet': self.code_snippet,
            'duplicate_locations': self.duplicate_locations,
            'suggested_strategy': self.suggested_strategy.value,
            'estimated_effort': self.estimated_effort,
            'potential_savings': self.potential_savings,
            'metadata': self.metadata
        }


@dataclass
class EliminationResult:
    """Result of DRY elimination operation."""
    operation_id: str
    violation_id: str
    strategy_applied: EliminationStrategy
    success: bool
    files_modified: List[str] = field(default_factory=list)
    lines_removed: int = 0
    lines_added: int = 0
    error_message: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def calculate_net_reduction(self) -> int:
        """Calculate net lines of code reduction."""
        return self.lines_removed - self.lines_added
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'operation_id': self.operation_id,
            'violation_id': self.violation_id,
            'strategy_applied': self.strategy_applied.value,
            'success': self.success,
            'files_modified': self.files_modified,
            'lines_removed': self.lines_removed,
            'lines_added': self.lines_added,
            'net_reduction': self.calculate_net_reduction(),
            'error_message': self.error_message,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata
        }


@dataclass
class DRYEliminatorConfig:
    """Configuration for DRY elimination system."""
    
    # Analysis settings
    enable_import_analysis: bool = True
    enable_method_analysis: bool = True
    enable_class_analysis: bool = True
    enable_constant_analysis: bool = True
    enable_documentation_analysis: bool = True
    enable_error_handling_analysis: bool = True
    enable_algorithm_analysis: bool = True
    enable_interface_analysis: bool = True
    enable_test_analysis: bool = True
    enable_data_structure_analysis: bool = True
    
    # Detection thresholds
    min_duplicate_lines: int = 3
    min_similarity_threshold: float = 0.8
    min_potential_savings: int = 5
    
    # Processing settings
    max_concurrent_operations: int = 5
    backup_before_modification: bool = True
    dry_run_mode: bool = False
    
    # File patterns
    include_patterns: List[str] = field(default_factory=lambda: [
        "**/*.py"
    ])
    
    exclude_patterns: List[str] = field(default_factory=lambda: [
        "**/test_*.py",
        "**/*_test.py",
        "**/tests/**",
        "**/__pycache__/**",
        "**/.git/**",
        "**/venv/**",
        "**/env/**"
    ])
    
    # Safety settings
    max_files_per_operation: int = 100
    require_confirmation: bool = False
    create_backup_directory: bool = True
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if self.min_duplicate_lines < 1:
            raise ValueError("Min duplicate lines must be at least 1")
        if not 0.0 <= self.min_similarity_threshold <= 1.0:
            raise ValueError("Similarity threshold must be between 0.0 and 1.0")
        if self.min_potential_savings < 0:
            raise ValueError("Min potential savings cannot be negative")
        if self.max_concurrent_operations < 1:
            raise ValueError("Max concurrent operations must be at least 1")
        if self.max_files_per_operation < 1:
            raise ValueError("Max files per operation must be at least 1")
        return True


@dataclass
class EliminationMetrics:
    """Metrics for DRY elimination operations."""
    total_files_analyzed: int = 0
    total_violations_found: int = 0
    total_violations_eliminated: int = 0
    total_lines_removed: int = 0
    total_lines_added: int = 0
    total_files_modified: int = 0
    successful_operations: int = 0
    failed_operations: int = 0
    analysis_time_seconds: float = 0.0
    elimination_time_seconds: float = 0.0
    
    # Violation type breakdown
    imports_consolidated: int = 0
    methods_consolidated: int = 0
    classes_consolidated: int = 0
    constants_consolidated: int = 0
    documentation_consolidated: int = 0
    error_handling_consolidated: int = 0
    algorithms_consolidated: int = 0
    interfaces_consolidated: int = 0
    tests_consolidated: int = 0
    data_structures_consolidated: int = 0
    unused_imports_removed: int = 0
    
    def calculate_success_rate(self) -> float:
        """Calculate success rate of elimination operations."""
        total_operations = self.successful_operations + self.failed_operations
        if total_operations == 0:
            return 1.0
        return self.successful_operations / total_operations
    
    def calculate_net_reduction(self) -> int:
        """Calculate net lines of code reduction."""
        return self.total_lines_removed - self.total_lines_added
    
    def calculate_elimination_rate(self) -> float:
        """Calculate rate of violations eliminated."""
        if self.total_violations_found == 0:
            return 1.0
        return self.total_violations_eliminated / self.total_violations_found
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'total_files_analyzed': self.total_files_analyzed,
            'total_violations_found': self.total_violations_found,
            'total_violations_eliminated': self.total_violations_eliminated,
            'elimination_rate': self.calculate_elimination_rate(),
            'total_lines_removed': self.total_lines_removed,
            'total_lines_added': self.total_lines_added,
            'net_reduction': self.calculate_net_reduction(),
            'total_files_modified': self.total_files_modified,
            'successful_operations': self.successful_operations,
            'failed_operations': self.failed_operations,
            'success_rate': self.calculate_success_rate(),
            'analysis_time_seconds': self.analysis_time_seconds,
            'elimination_time_seconds': self.elimination_time_seconds,
            'violation_breakdown': {
                'imports_consolidated': self.imports_consolidated,
                'methods_consolidated': self.methods_consolidated,
                'classes_consolidated': self.classes_consolidated,
                'constants_consolidated': self.constants_consolidated,
                'documentation_consolidated': self.documentation_consolidated,
                'error_handling_consolidated': self.error_handling_consolidated,
                'algorithms_consolidated': self.algorithms_consolidated,
                'interfaces_consolidated': self.interfaces_consolidated,
                'tests_consolidated': self.tests_consolidated,
                'data_structures_consolidated': self.data_structures_consolidated,
                'unused_imports_removed': self.unused_imports_removed
            }
        }


# Constants
DEFAULT_VIOLATION_TYPES = [
    DRYViolationType.DUPLICATE_IMPORTS,
    DRYViolationType.DUPLICATE_METHODS,
    DRYViolationType.DUPLICATE_CONSTANTS,
    DRYViolationType.UNUSED_IMPORTS
]

ELIMINATION_EFFORT_LEVELS = ["low", "medium", "high", "critical"]

VIOLATION_SEVERITY_SCORES = {
    ViolationSeverity.LOW: 1,
    ViolationSeverity.MEDIUM: 3,
    ViolationSeverity.HIGH: 7,
    ViolationSeverity.CRITICAL: 15
}

# Factory functions
def create_default_config() -> DRYEliminatorConfig:
    """Create default DRY eliminator configuration."""
    return DRYEliminatorConfig()

def create_dry_violation(violation_id: str, violation_type: DRYViolationType,
                        severity: ViolationSeverity, file_path: str,
                        line_number: int, code_snippet: str) -> DRYViolation:
    """Create DRY violation with validation."""
    violation = DRYViolation(
        violation_id=violation_id,
        violation_type=violation_type,
        severity=severity,
        file_path=file_path,
        line_number=line_number,
        code_snippet=code_snippet
    )
    # Validation happens in __post_init__
    return violation

def create_elimination_result(operation_id: str, violation_id: str,
                            strategy: EliminationStrategy, success: bool) -> EliminationResult:
    """Create elimination result with validation."""
    return EliminationResult(
        operation_id=operation_id,
        violation_id=violation_id,
        strategy_applied=strategy,
        success=success
    )

def create_elimination_metrics() -> EliminationMetrics:
    """Create elimination metrics tracker."""
    return EliminationMetrics()

# Validation functions
def validate_dry_violation(violation: DRYViolation) -> bool:
    """Validate DRY violation."""
    try:
        violation.__post_init__()
        return True
    except ValueError:
        return False

def validate_eliminator_config(config: DRYEliminatorConfig) -> bool:
    """Validate DRY eliminator configuration."""
    return config.validate()
