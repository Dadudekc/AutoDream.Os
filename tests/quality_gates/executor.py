"""
Quality gate executor that orchestrates all gate checks.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List
from .models import QualityGateResult, QualityGateSummary, GateStatus
from .registry import QualityGateRegistry
from .gates import (
    LineCountGate, ComplexityGate, DependencyGate, TestCoverageGate,
    NamingGate, DocumentationGate, DuplicationGate, FunctionLengthGate,
    ClassComplexityGate, ImportOrganizationGate
)
from src.utils.logger import get_logger

logger = get_logger(__name__)


class QualityGateExecutor:
    """Executes quality gate checks."""
    
    def __init__(self, registry: QualityGateRegistry):
        self.registry = registry
        self.execution_history: List[QualityGateResult] = []
        self._initialize_gates()
    
    def _initialize_gates(self):
        """Initialize all quality gate instances."""
        self.gates = {
            "Line Count": LineCountGate,
            "Cyclomatic Complexity": ComplexityGate,
            "Dependency Count": DependencyGate,
            "Test Coverage": TestCoverageGate,
            "Naming Conventions": NamingGate,
            "Documentation Coverage": DocumentationGate,
            "Code Duplication": DuplicationGate,
            "Function Length": FunctionLengthGate,
            "Class Complexity": ClassComplexityGate,
            "Import Organization": ImportOrganizationGate
        }
    
    def execute_all_gates(self, file_path: Path, file_metrics: Dict[str, Any]) -> List[QualityGateResult]:
        """Execute all enabled quality gates for a file."""
        enabled_gates = self.registry.get_enabled_gates()
        results = []
        
        for gate_config in enabled_gates:
            try:
                start_time = datetime.now()
                result = self._execute_single_gate(gate_config, file_path, file_metrics)
                execution_time = (datetime.now() - start_time).total_seconds() * 1000
                result.execution_time_ms = execution_time
                
                results.append(result)
                self.execution_history.append(result)
                
            except Exception as e:
                logger.error(f"Error executing gate {gate_config.gate_name}: {e}")
                error_result = QualityGateResult(
                    gate_name=gate_config.gate_name,
                    status=GateStatus.ERROR,
                    score=0.0,
                    threshold=gate_config.threshold,
                    weight=gate_config.weight,
                    severity=gate_config.severity,
                    details=f"Gate execution failed: {e}",
                    recommendations=["Fix gate implementation", "Check file format"],
                    timestamp=datetime.now().isoformat(),
                    execution_time_ms=0.0
                )
                results.append(error_result)
        
        return results
    
    def _execute_single_gate(self, gate_config: QualityGateConfig, file_path: Path, 
                           file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute a single quality gate."""
        gate_class = self.gates.get(gate_config.gate_name)
        if gate_class:
            gate = gate_class(gate_config)
            return gate.execute(file_path, file_metrics)
        else:
            return self._execute_generic_gate(gate_config, file_path, file_metrics)
    
    def _execute_generic_gate(self, gate_config: QualityGateConfig, file_path: Path, 
                            file_metrics: Dict[str, Any]) -> QualityGateResult:
        """Execute a generic quality gate for unknown gate types."""
        return QualityGateResult(
            gate_name=gate_config.gate_name,
            status=GateStatus.ERROR,
            score=0.0,
            threshold=gate_config.threshold,
            weight=gate_config.weight,
            severity=gate_config.severity,
            details=f"Unknown gate type: {gate_config.gate_name}",
            recommendations=["Implement specific gate executor", "Check gate configuration"],
            timestamp=datetime.now().isoformat(),
            execution_time_ms=0.0
        )
    
    def generate_summary(self, results: List[QualityGateResult]) -> QualityGateSummary:
        """Generate a summary of quality gate results."""
        total_gates = len(results)
        passed_gates = len([r for r in results if r.status == GateStatus.PASSED])
        failed_gates = len([r for r in results if r.status == GateStatus.FAILED])
        warning_gates = len([r for r in results if r.status == GateStatus.WARNING])
        error_gates = len([r for r in results if r.status == GateStatus.ERROR])
        
        # Calculate overall scores
        overall_score = sum(r.score for r in results) / total_gates if total_gates > 0 else 0
        
        # Calculate weighted score
        total_weight = sum(r.weight for r in results)
        weighted_score = sum(r.score * r.weight for r in results) / total_weight if total_weight > 0 else 0
        
        # Count failures by severity
        critical_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == "CRITICAL"])
        high_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == "HIGH"])
        medium_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == "MEDIUM"])
        low_failures = len([r for r in results if r.status == GateStatus.FAILED and r.severity == "LOW"])
        
        return QualityGateSummary(
            total_gates=total_gates,
            passed_gates=passed_gates,
            failed_gates=failed_gates,
            warning_gates=warning_gates,
            error_gates=error_gates,
            overall_score=overall_score,
            weighted_score=weighted_score,
            critical_failures=critical_failures,
            high_failures=high_failures,
            medium_failures=medium_failures,
            low_failures=low_failures,
            timestamp=datetime.now().isoformat()
        )
    
    def save_results(self, results: List[QualityGateResult], output_path: Path):
        """Save quality gate results to a JSON file."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert results to serializable format
        serializable_results = []
        for result in results:
            serializable_result = {
                'gate_name': result.gate_name,
                'status': result.status.value,
                'score': result.score,
                'threshold': result.threshold,
                'weight': result.weight,
                'severity': result.severity.value,
                'details': result.details,
                'recommendations': result.recommendations,
                'timestamp': result.timestamp,
                'execution_time_ms': result.execution_time_ms
            }
            serializable_results.append(serializable_result)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, default=str)
        
        logger.info(f"Quality gate results saved to {output_path}")
