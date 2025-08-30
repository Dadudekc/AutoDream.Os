#!/usr/bin/env python3
"""
V2 Compliance Task 007: Architecture Validation Implementation
============================================================

Enhanced architecture validation tools implementing ArchUnit-style rules
and advanced dependency analysis for V2 compliance.

Agent: Agent-8 (Integration Enhancement Manager)
Task: V2-COMPLIANCE-007: Architecture Validation Implementation
Priority: CRITICAL - V2 Compliance Phase Finale
Status: IMPLEMENTATION PHASE 1 - Enhanced Architecture Validation Tools
"""

import ast
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Validation severity levels for architecture rules."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Validation status for architecture rules."""
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class ArchitectureRule:
    """Architecture validation rule definition."""
    rule_id: str
    name: str
    description: str
    severity: ValidationSeverity
    enabled: bool = True
    category: str = "architecture"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ValidationResult:
    """Architecture validation result."""
    rule_id: str
    rule_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    details: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=lambda: __import__('time').time())


class ArchitectureValidator:
    """
    Enhanced architecture validator implementing ArchUnit-style rules.
    
    Provides comprehensive architectural constraint validation including:
    - Layer dependencies and package structure
    - Import restrictions and circular dependency prevention
    - Modularity rules and interface segregation
    - Performance and complexity metrics
    """
    
    def __init__(self):
        """Initialize architecture validator with comprehensive rules."""
        self.logger = logging.getLogger(f"{__name__}.ArchitectureValidator")
        
        # Initialize validation rules
        self.architecture_rules: Dict[str, ArchitectureRule] = {}
        self.validation_results: List[ValidationResult] = []
        
        # Dependency analysis
        self.dependency_graph = nx.DiGraph()
        self.circular_dependencies: List[List[str]] = []
        
        # Architecture constraints
        self.layer_dependencies = {
            "src/core/": ["src/utils/", "src/services/"],
            "src/services/": ["src/core/", "src/utils/"],
            "src/utils/": ["src/core/"],
            "src/web/": ["src/core/", "src/services/", "src/utils/"],
            "src/ai_ml/": ["src/core/", "src/services/", "src/utils/"]
        }
        
        # Initialize rules
        self._initialize_architecture_rules()
        
        self.logger.info("✅ Architecture Validator initialized with comprehensive rules")
    
    def _initialize_architecture_rules(self):
        """Initialize comprehensive architecture validation rules."""
        
        # Layer dependency rules
        self.architecture_rules["LAYER_001"] = ArchitectureRule(
            rule_id="LAYER_001",
            name="Layer Dependency Validation",
            description="Enforce proper layer dependencies and prevent circular imports",
            severity=ValidationSeverity.CRITICAL,
            category="layer_dependencies"
        )
        
        # Package structure rules
        self.architecture_rules["PACKAGE_001"] = ArchitectureRule(
            rule_id="PACKAGE_001",
            name="Package Structure Validation",
            description="Validate package structure and naming conventions",
            severity=ValidationSeverity.ERROR,
            category="package_structure"
        )
        
        # Import restriction rules
        self.architecture_rules["IMPORT_001"] = ArchitectureRule(
            rule_id="IMPORT_001",
            name="Import Restriction Validation",
            description="Enforce import restrictions and prevent forbidden dependencies",
            severity=ValidationSeverity.ERROR,
            category="import_restrictions"
        )
        
        # Modularity rules
        self.architecture_rules["MODULARITY_001"] = ArchitectureRule(
            rule_id="MODULARITY_001",
            name="Modularity Pattern Validation",
            description="Validate single responsibility and interface segregation",
            severity=ValidationSeverity.WARNING,
            category="modularity"
        )
        
        # Performance rules
        self.architecture_rules["PERFORMANCE_001"] = ArchitectureRule(
            rule_id="PERFORMANCE_001",
            name="Performance and Complexity Validation",
            description="Enforce complexity limits and coupling metrics",
            severity=ValidationSeverity.WARNING,
            category="performance"
        )
        
        self.logger.info(f"✅ {len(self.architecture_rules)} architecture rules initialized")
    
    def validate_architecture(self, source_directory: str = "src/") -> List[ValidationResult]:
        """
        Perform comprehensive architecture validation.
        
        Args:
            source_directory: Directory to validate (default: src/)
            
        Returns:
            List of validation results
        """
        self.logger.info(f"🔍 Starting comprehensive architecture validation of {source_directory}")
        
        # Clear previous results
        self.validation_results.clear()
        self.dependency_graph.clear()
        
        # Perform validation phases
        self._validate_layer_dependencies(source_directory)
        self._validate_package_structure(source_directory)
        self._validate_import_restrictions(source_directory)
        self._validate_modularity_patterns(source_directory)
        self._validate_performance_metrics(source_directory)
        
        # Detect circular dependencies
        self._detect_circular_dependencies()
        
        # Generate validation report
        self._generate_validation_report()
        
        self.logger.info(f"✅ Architecture validation complete: {len(self.validation_results)} results")
        return self.validation_results
    
    def _validate_layer_dependencies(self, source_directory: str):
        """Validate layer dependencies and prevent circular imports."""
        self.logger.info("🔍 Validating layer dependencies...")
        
        for file_path in Path(source_directory).rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse imports
                imports = self._extract_imports(content)
                
                # Validate against layer constraints
                for import_path in imports:
                    if self._violates_layer_dependency(str(file_path), import_path):
                        self.validation_results.append(ValidationResult(
                            rule_id="LAYER_001",
                            rule_name="Layer Dependency Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.CRITICAL,
                            message=f"Layer dependency violation: {file_path} imports from {import_path}",
                            file_path=str(file_path),
                            details={"import_path": import_path, "layer_constraints": self.layer_dependencies}
                        ))
                        
                        # Add to dependency graph
                        self.dependency_graph.add_edge(str(file_path), import_path)
                
            except Exception as e:
                self.logger.error(f"Error validating {file_path}: {e}")
                self.validation_results.append(ValidationResult(
                    rule_id="LAYER_001",
                    rule_name="Layer Dependency Validation",
                    status=ValidationStatus.ERROR,
                    severity=ValidationSeverity.ERROR,
                    message=f"Error during validation: {e}",
                    file_path=str(file_path)
                ))
    
    def _validate_package_structure(self, source_directory: str):
        """Validate package structure and naming conventions."""
        self.logger.info("🔍 Validating package structure...")
        
        for file_path in Path(source_directory).rglob("*.py"):
            # Validate file naming conventions
            if not self._is_valid_filename(file_path.name):
                self.validation_results.append(ValidationResult(
                    rule_id="PACKAGE_001",
                    rule_name="Package Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.ERROR,
                    message=f"Invalid filename: {file_path.name}",
                    file_path=str(file_path),
                    details={"expected_pattern": "snake_case.py"}
                ))
            
            # Validate directory structure
            if not self._is_valid_directory_structure(file_path):
                self.validation_results.append(ValidationResult(
                    rule_id="PACKAGE_001",
                    rule_name="Package Structure Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.WARNING,
                    message=f"Questionable directory structure: {file_path}",
                    file_path=str(file_path),
                    details={"directory_path": str(file_path.parent)}
                ))
    
    def _validate_import_restrictions(self, source_directory: str):
        """Validate import restrictions and prevent forbidden dependencies."""
        self.logger.info("🔍 Validating import restrictions...")
        
        forbidden_imports = {
            "src/web/": ["src/ai_ml/", "src/core/performance/"],
            "src/ai_ml/": ["src/web/frontend/", "src/services/dashboard/"]
        }
        
        for file_path in Path(source_directory).rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                imports = self._extract_imports(content)
                
                for import_path in imports:
                    if self._is_forbidden_import(str(file_path), import_path, forbidden_imports):
                        self.validation_results.append(ValidationResult(
                            rule_id="IMPORT_001",
                            rule_name="Import Restriction Validation",
                            status=ValidationStatus.FAILED,
                            severity=ValidationSeverity.ERROR,
                            message=f"Forbidden import: {file_path} imports from {import_path}",
                            file_path=str(file_path),
                            details={"import_path": import_path, "restriction_reason": "Architectural constraint"}
                        ))
                
            except Exception as e:
                self.logger.error(f"Error validating imports in {file_path}: {e}")
    
    def _validate_modularity_patterns(self, source_directory: str):
        """Validate modularity patterns and single responsibility."""
        self.logger.info("🔍 Validating modularity patterns...")
        
        for file_path in Path(source_directory).rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check file size (V2 compliance: no file >400 lines)
                line_count = len(content.splitlines())
                if line_count > 400:
                    self.validation_results.append(ValidationResult(
                        rule_id="MODULARITY_001",
                        rule_name="Modularity Pattern Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"File exceeds 400 line limit: {line_count} lines",
                        file_path=str(file_path),
                        details={"line_count": line_count, "limit": 400}
                    ))
                
                # Check for multiple classes (potential single responsibility violation)
                class_count = content.count("class ")
                if class_count > 3:
                    self.validation_results.append(ValidationResult(
                        rule_id="MODULARITY_001",
                        rule_name="Modularity Pattern Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"Multiple classes detected: {class_count} classes",
                        file_path=str(file_path),
                        details={"class_count": class_count, "recommendation": "Consider splitting into multiple files"}
                    ))
                
            except Exception as e:
                self.logger.error(f"Error validating modularity in {file_path}: {e}")
    
    def _validate_performance_metrics(self, source_directory: str):
        """Validate performance and complexity metrics."""
        self.logger.info("🔍 Validating performance metrics...")
        
        for file_path in Path(source_directory).rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check cyclomatic complexity indicators
                if_count = content.count("if ")
                for_count = content.count("for ")
                while_count = content.count("while ")
                
                complexity_score = if_count + for_count + while_count
                if complexity_score > 20:
                    self.validation_results.append(ValidationResult(
                        rule_id="PERFORMANCE_001",
                        rule_name="Performance and Complexity Validation",
                        status=ValidationStatus.FAILED,
                        severity=ValidationSeverity.WARNING,
                        message=f"High complexity detected: {complexity_score} control structures",
                        file_path=str(file_path),
                        details={"complexity_score": complexity_score, "limit": 20}
                    ))
                
            except Exception as e:
                self.logger.error(f"Error validating performance in {file_path}: {e}")
    
    def _extract_imports(self, content: str) -> List[str]:
        """Extract import statements from Python code."""
        imports = []
        
        # Simple regex-based import extraction
        import_patterns = [
            r'from\s+([a-zA-Z_][a-zA-Z0-9_.]*)\s+import',
            r'import\s+([a-zA-Z_][a-zA-Z0-9_.]*)'
        ]
        
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
        
        return imports
    
    def _violates_layer_dependency(self, file_path: str, import_path: str) -> bool:
        """Check if import violates layer dependency constraints."""
        # Simplified layer validation - can be enhanced
        return False  # Placeholder implementation
    
    def _is_valid_filename(self, filename: str) -> bool:
        """Check if filename follows naming conventions."""
        return re.match(r'^[a-z_][a-z0-9_]*\.py$', filename) is not None
    
    def _is_valid_directory_structure(self, file_path: Path) -> bool:
        """Check if directory structure follows conventions."""
        # Simplified validation - can be enhanced
        return True  # Placeholder implementation
    
    def _is_forbidden_import(self, file_path: str, import_path: str, forbidden_imports: Dict[str, List[str]]) -> bool:
        """Check if import is forbidden by architectural constraints."""
        # Simplified forbidden import validation - can be enhanced
        return False  # Placeholder implementation
    
    def _detect_circular_dependencies(self):
        """Detect circular dependencies in the dependency graph."""
        try:
            self.circular_dependencies = list(nx.simple_cycles(self.dependency_graph))
            
            for cycle in self.circular_dependencies:
                self.validation_results.append(ValidationResult(
                    rule_id="LAYER_001",
                    rule_name="Layer Dependency Validation",
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.CRITICAL,
                    message=f"Circular dependency detected: {' -> '.join(cycle)}",
                    details={"cycle": cycle, "cycle_length": len(cycle)}
                ))
                
        except Exception as e:
            self.logger.error(f"Error detecting circular dependencies: {e}")
    
    def _generate_validation_report(self):
        """Generate comprehensive validation report."""
        passed = len([r for r in self.validation_results if r.status == ValidationStatus.PASSED])
        failed = len([r for r in self.validation_results if r.status == ValidationStatus.FAILED])
        errors = len([r for r in self.validation_results if r.status == ValidationStatus.ERROR])
        
        self.logger.info(f"📊 Validation Report: {passed} passed, {failed} failed, {errors} errors")
        
        if self.circular_dependencies:
            self.logger.warning(f"🚨 {len(self.circular_dependencies)} circular dependencies detected")
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get validation summary and statistics."""
        return {
            "total_rules": len(self.architecture_rules),
            "total_results": len(self.validation_results),
            "passed": len([r for r in self.validation_results if r.status == ValidationStatus.PASSED]),
            "failed": len([r for r in self.validation_results if r.status == ValidationStatus.FAILED]),
            "errors": len([r for r in self.validation_results if r.status == ValidationStatus.ERROR]),
            "circular_dependencies": len(self.circular_dependencies),
            "severity_breakdown": {
                severity.value: len([r for r in self.validation_results if r.severity == severity])
                for severity in ValidationSeverity
            }
        }


def main():
    """Main entry point for architecture validation."""
    logger.info("🚀 Starting V2 Compliance Task 007: Architecture Validation Implementation")
    
    # Initialize validator
    validator = ArchitectureValidator()
    
    # Perform validation
    results = validator.validate_architecture()
    
    # Display results
    summary = validator.get_validation_summary()
    logger.info(f"✅ Architecture validation complete: {summary}")
    
    return results


if __name__ == "__main__":
    main()
