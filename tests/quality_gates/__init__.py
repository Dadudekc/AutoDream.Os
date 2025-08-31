"""
Quality Gates for Monolithic File Modularization

This module provides a modularized quality gate system that must be passed
before a file is considered successfully modularized.
"""

from .models import (
    GateSeverity,
    GateStatus,
    QualityGateConfig,
    QualityGateResult,
    QualityGateSummary
)
from .registry import QualityGateRegistry
from .executor import QualityGateExecutor

__all__ = [
    'GateSeverity',
    'GateStatus', 
    'QualityGateConfig',
    'QualityGateResult',
    'QualityGateSummary',
    'QualityGateRegistry',
    'QualityGateExecutor',
    'create_quality_gate_system',
    'run_quality_gates'
]


def create_quality_gate_system() -> tuple[QualityGateRegistry, QualityGateExecutor]:
    """Create a quality gate system with default configuration."""
    registry = QualityGateRegistry()
    executor = QualityGateExecutor(registry)
    return registry, executor


def run_quality_gates(file_path, file_metrics) -> tuple[list[QualityGateResult], QualityGateSummary]:
    """Run quality gates for a single file."""
    registry, executor = create_quality_gate_system()
    
    # Execute all gates
    results = executor.execute_all_gates(file_path, file_metrics)
    
    # Generate summary
    summary = executor.generate_summary(results)
    
    return results, summary
