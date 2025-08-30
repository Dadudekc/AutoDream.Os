"""
Quality gate registry for managing gate configurations.
"""

from typing import Dict, List, Optional
from .models import QualityGateConfig, GateSeverity
from src.utils.logger import get_logger

logger = get_logger(__name__)


class QualityGateRegistry:
    """Registry for managing quality gates."""
    
    def __init__(self):
        self.gates: Dict[str, QualityGateConfig] = {}
        self._register_default_gates()
    
    def _register_default_gates(self):
        """Register the default set of quality gates."""
        default_gates = [
            QualityGateConfig(
                gate_name="Line Count",
                severity=GateSeverity.CRITICAL,
                enabled=True,
                threshold=300.0,
                weight=1.0,
                description="Check if file meets line count requirements",
                failure_message="File exceeds maximum line count threshold",
                success_message="File meets line count requirements"
            ),
            QualityGateConfig(
                gate_name="Cyclomatic Complexity",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=20.0,
                weight=0.9,
                description="Check cyclomatic complexity of the file",
                failure_message="File has excessive cyclomatic complexity",
                success_message="File has acceptable complexity"
            ),
            QualityGateConfig(
                gate_name="Dependency Count",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=15.0,
                weight=0.8,
                description="Check number of external dependencies",
                failure_message="File has too many external dependencies",
                success_message="File has acceptable dependency count"
            ),
            QualityGateConfig(
                gate_name="Test Coverage",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=80.0,
                weight=0.7,
                description="Check test coverage percentage",
                failure_message="File has insufficient test coverage",
                success_message="File has adequate test coverage"
            ),
            QualityGateConfig(
                gate_name="Naming Conventions",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=90.0,
                weight=0.6,
                description="Check naming convention compliance",
                failure_message="File violates naming conventions",
                success_message="File follows naming conventions"
            ),
            QualityGateConfig(
                gate_name="Documentation Coverage",
                severity=GateSeverity.LOW,
                enabled=True,
                threshold=70.0,
                weight=0.5,
                description="Check documentation coverage",
                failure_message="File has insufficient documentation",
                success_message="File has adequate documentation"
            ),
            QualityGateConfig(
                gate_name="Code Duplication",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=10.0,
                weight=0.7,
                description="Check for code duplication percentage",
                failure_message="File has excessive code duplication",
                success_message="File has acceptable duplication levels"
            ),
            QualityGateConfig(
                gate_name="Function Length",
                severity=GateSeverity.HIGH,
                enabled=True,
                threshold=50.0,
                weight=0.8,
                description="Check maximum function length",
                failure_message="File contains overly long functions",
                success_message="File has appropriately sized functions"
            ),
            QualityGateConfig(
                gate_name="Class Complexity",
                severity=GateSeverity.MEDIUM,
                enabled=True,
                threshold=15.0,
                weight=0.6,
                description="Check class complexity metrics",
                failure_message="File contains overly complex classes",
                success_message="File has appropriately complex classes"
            ),
            QualityGateConfig(
                gate_name="Import Organization",
                severity=GateSeverity.LOW,
                enabled=True,
                threshold=85.0,
                weight=0.4,
                description="Check import statement organization",
                failure_message="File has poorly organized imports",
                success_message="File has well-organized imports"
            )
        ]
        
        for gate in default_gates:
            self.register_gate(gate)
    
    def register_gate(self, gate: QualityGateConfig):
        """Register a new quality gate."""
        self.gates[gate.gate_name] = gate
        logger.info(f"Registered quality gate: {gate.gate_name}")
    
    def get_gate(self, gate_name: str) -> Optional[QualityGateConfig]:
        """Get a quality gate by name."""
        return self.gates.get(gate_name)
    
    def get_enabled_gates(self) -> List[QualityGateConfig]:
        """Get all enabled quality gates."""
        return [gate for gate in self.gates.values() if gate.enabled]
    
    def update_gate_config(self, gate_name: str, **kwargs) -> bool:
        """Update a gate's configuration."""
        if gate_name not in self.gates:
            return False
        
        gate = self.gates[gate_name]
        for key, value in kwargs.items():
            if hasattr(gate, key):
                setattr(gate, key, value)
        
        logger.info(f"Updated gate configuration: {gate_name}")
        return True
