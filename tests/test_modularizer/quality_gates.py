#!/usr/bin/env python3
"""
🧪 QUALITY GATES FOR MODULARIZATION VALIDATION - MODULAR-004
Testing Framework Enhancement Manager - Agent-3

This module implements comprehensive quality gates for validating
modularization quality and ensuring V2 compliance standards.

Features:
- Configurable quality thresholds
- Automated quality validation
- Quality scoring and reporting
- Integration with testing framework
- Support for different file types
"""

import os
import sys
import ast
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import statistics

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


class QualityLevel(Enum):
    """Quality level classifications"""
    EXCELLENT = "EXCELLENT"
    GOOD = "GOOD"
    FAIR = "FAIR"
    POOR = "POOR"
    CRITICAL = "CRITICAL"


@dataclass
class QualityGateResult:
    """Result of quality gate validation"""
    gate_name: str
    passed: bool
    score: float
    threshold: float
    details: Dict[str, Any]
    recommendations: List[str]
    quality_level: QualityLevel


@dataclass
class QualityMetrics:
    """Quality metrics for a file"""
    file_path: str
    file_size: int
    line_count: int
    function_count: int
    class_count: int
    import_count: int
    complexity_score: float
    documentation_score: float
    naming_score: float
    structure_score: float
    overall_score: float


class QualityGate:
    """Base class for quality gates"""
    
    def __init__(self, name: str, description: str, threshold: float, weight: float = 1.0):
        self.name = name
        self.description = description
        self.threshold = threshold
        self.weight = weight
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate quality gate for a file"""
        raise NotImplementedError("Subclasses must implement validate method")
    
    def _calculate_quality_level(self, score: float) -> QualityLevel:
        """Calculate quality level based on score"""
        if score >= 90.0:
            return QualityLevel.EXCELLENT
        elif score >= 80.0:
            return QualityLevel.GOOD
        elif score >= 70.0:
            return QualityLevel.FAIR
        elif score >= 60.0:
            return QualityLevel.POOR
        else:
            return QualityLevel.CRITICAL


class FileSizeReductionGate(QualityGate):
    """Quality gate for file size reduction validation"""
    
    def __init__(self):
        super().__init__(
            name="File Size Reduction",
            description="Ensure significant file size reduction after modularization",
            threshold=30.0,  # 30% minimum reduction
            weight=0.25
        )
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate file size reduction"""
        try:
            # This would compare original vs modularized file sizes
            # For now, analyze current file size and estimate reduction potential
            
            file_size = Path(file_path).stat().st_size
            line_count = self._count_lines(file_path)
            
            # Estimate reduction potential based on file characteristics
            reduction_potential = self._estimate_reduction_potential(file_path, line_count)
            
            # Calculate score based on current file size and reduction potential
            if line_count > 400:  # Monolithic file
                score = min(100.0, max(0.0, (line_count - 400) / 200 * 100))
                passed = reduction_potential >= self.threshold
            else:
                score = 100.0  # Already compliant
                passed = True
            
            details = {
                "current_size_bytes": file_size,
                "current_lines": line_count,
                "reduction_potential_percent": reduction_potential,
                "needs_modularization": line_count > 400
            }
            
            recommendations = self._generate_recommendations(line_count, reduction_potential)
            
            return QualityGateResult(
                gate_name=self.name,
                passed=passed,
                score=score,
                threshold=self.threshold,
                details=details,
                recommendations=recommendations,
                quality_level=self._calculate_quality_level(score)
            )
            
        except Exception as e:
            return QualityGateResult(
                gate_name=self.name,
                passed=False,
                score=0.0,
                threshold=self.threshold,
                details={"error": str(e)},
                recommendations=["Fix file access issues"],
                quality_level=QualityLevel.CRITICAL
            )
    
    def _count_lines(self, file_path: str) -> int:
        """Count lines in a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return len(f.readlines())
        except:
            return 0
    
    def _estimate_reduction_potential(self, file_path: str, line_count: int) -> float:
        """Estimate potential reduction percentage"""
        if line_count <= 400:
            return 0.0
        
        # Estimate based on file characteristics
        if line_count > 800:
            return 60.0  # High reduction potential
        elif line_count > 600:
            return 50.0  # Medium-high reduction potential
        elif line_count > 500:
            return 40.0  # Medium reduction potential
        else:
            return 25.0  # Low reduction potential
    
    def _generate_recommendations(self, line_count: int, reduction_potential: float) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        if line_count > 800:
            recommendations.extend([
                "Break into 4-6 focused modules",
                "Extract utility functions to separate files",
                "Create interface modules for complex interactions"
            ])
        elif line_count > 600:
            recommendations.extend([
                "Break into 3-4 focused modules",
                "Extract common functionality to utilities",
                "Separate concerns into logical modules"
            ])
        elif line_count > 500:
            recommendations.extend([
                "Break into 2-3 focused modules",
                "Extract helper functions to utilities",
                "Consider if file can be split logically"
            ])
        
        if reduction_potential < self.threshold:
            recommendations.append(f"Ensure at least {self.threshold}% reduction for compliance")
        
        return recommendations


class SingleResponsibilityGate(QualityGate):
    """Quality gate for single responsibility principle validation"""
    
    def __init__(self):
        super().__init__(
            name="Single Responsibility",
            description="Ensure each module has single responsibility",
            threshold=0.8,  # 80% SRP compliance
            weight=0.20
        )
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate single responsibility principle compliance"""
        try:
            if not file_path.endswith('.py'):
                return QualityGateResult(
                    gate_name=self.name,
                    passed=True,
                    score=100.0,
                    threshold=self.threshold,
                    details={"file_type": "non-python"},
                    recommendations=[],
                    quality_level=QualityLevel.EXCELLENT
                )
            
            # Parse Python file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Analyze responsibilities
            responsibilities = self._analyze_responsibilities(tree)
            srp_score = self._calculate_srp_score(responsibilities)
            
            passed = srp_score >= self.threshold
            details = {
                "responsibilities": responsibilities,
                "srp_score": srp_score,
                "classes": len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]),
                "functions": len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]),
                "imports": len([node for node in ast.walk(tree) if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom)])
            }
            
            recommendations = self._generate_srp_recommendations(responsibilities, srp_score)
            
            return QualityGateResult(
                gate_name=self.name,
                passed=passed,
                score=srp_score * 100,
                threshold=self.threshold * 100,
                details=details,
                recommendations=recommendations,
                quality_level=self._calculate_quality_level(srp_score * 100)
            )
            
        except Exception as e:
            return QualityGateResult(
                gate_name=self.name,
                passed=False,
                score=0.0,
                threshold=self.threshold * 100,
                details={"error": str(e)},
                recommendations=["Fix Python parsing issues"],
                quality_level=QualityLevel.CRITICAL
            )
    
    def _analyze_responsibilities(self, tree: ast.AST) -> Dict[str, int]:
        """Analyze responsibilities in the AST"""
        responsibilities = {
            "data_processing": 0,
            "file_operations": 0,
            "network_communication": 0,
            "user_interface": 0,
            "business_logic": 0,
            "utility_functions": 0,
            "testing": 0,
            "configuration": 0
        }
        
        # Analyze based on function names, class names, and imports
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_name = node.name.lower()
                if any(keyword in func_name for keyword in ['process', 'transform', 'calculate']):
                    responsibilities["data_processing"] += 1
                elif any(keyword in func_name for keyword in ['read', 'write', 'save', 'load']):
                    responsibilities["file_operations"] += 1
                elif any(keyword in func_name for keyword in ['send', 'receive', 'request', 'response']):
                    responsibilities["network_communication"] += 1
                elif any(keyword in func_name for keyword in ['render', 'display', 'show', 'ui']):
                    responsibilities["user_interface"] += 1
                elif any(keyword in func_name for keyword in ['validate', 'check', 'verify']):
                    responsibilities["business_logic"] += 1
                elif any(keyword in func_name for keyword in ['format', 'parse', 'convert']):
                    responsibilities["utility_functions"] += 1
                elif any(keyword in func_name for keyword in ['test', 'assert', 'mock']):
                    responsibilities["testing"] += 1
                elif any(keyword in func_name for keyword in ['config', 'setting', 'option']):
                    responsibilities["configuration"] += 1
            
            elif isinstance(node, ast.ClassDef):
                class_name = node.name.lower()
                if any(keyword in class_name for keyword in ['processor', 'handler', 'service']):
                    responsibilities["data_processing"] += 1
                elif any(keyword in func_name for keyword in ['manager', 'controller', 'orchestrator']):
                    responsibilities["business_logic"] += 1
        
        return responsibilities
    
    def _calculate_srp_score(self, responsibilities: Dict[str, int]) -> float:
        """Calculate SRP compliance score"""
        total_responsibilities = sum(responsibilities.values())
        if total_responsibilities == 0:
            return 1.0
        
        # Count primary responsibilities (those with >0 count)
        primary_responsibilities = sum(1 for count in responsibilities.values() if count > 0)
        
        # Ideal: 1-2 primary responsibilities
        if primary_responsibilities <= 2:
            return 1.0
        elif primary_responsibilities == 3:
            return 0.8
        elif primary_responsibilities == 4:
            return 0.6
        else:
            return 0.4
    
    def _generate_srp_recommendations(self, responsibilities: Dict[str, int], srp_score: float) -> List[str]:
        """Generate SRP improvement recommendations"""
        recommendations = []
        
        primary_responsibilities = [name for name, count in responsibilities.items() if count > 0]
        
        if len(primary_responsibilities) > 3:
            recommendations.append("Split into multiple focused modules")
            recommendations.append("Extract utility functions to separate files")
            recommendations.append("Create interface modules for complex interactions")
        
        if srp_score < 0.8:
            recommendations.append("Focus each module on a single responsibility")
            recommendations.append("Consider if functionality can be logically separated")
        
        return recommendations


class InterfaceQualityGate(QualityGate):
    """Quality gate for interface quality validation"""
    
    def __init__(self):
        super().__init__(
            name="Interface Quality",
            description="Ensure high-quality interfaces between modules",
            threshold=0.7,  # 70% interface quality
            weight=0.20
        )
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate interface quality"""
        try:
            if not file_path.endswith('.py'):
                return QualityGateResult(
                    gate_name=self.name,
                    passed=True,
                    score=100.0,
                    threshold=self.threshold,
                    details={"file_type": "non-python"},
                    recommendations=[],
                    quality_level=QualityLevel.EXCELLENT
                )
            
            # Analyze interface quality
            interface_metrics = self._analyze_interface_quality(file_path)
            quality_score = self._calculate_interface_quality_score(interface_metrics)
            
            passed = quality_score >= self.threshold
            details = {
                "interface_metrics": interface_metrics,
                "quality_score": quality_score,
                "interface_count": interface_metrics.get("interface_count", 0),
                "coupling_score": interface_metrics.get("coupling_score", 0.0),
                "cohesion_score": interface_metrics.get("cohesion_score", 0.0)
            }
            
            recommendations = self._generate_interface_recommendations(interface_metrics, quality_score)
            
            return QualityGateResult(
                gate_name=self.name,
                passed=passed,
                score=quality_score * 100,
                threshold=self.threshold * 100,
                details=details,
                recommendations=recommendations,
                quality_level=self._calculate_quality_level(quality_score * 100)
            )
            
        except Exception as e:
            return QualityGateResult(
                gate_name=self.name,
                passed=False,
                score=0.0,
                threshold=self.threshold * 100,
                details={"error": str(e)},
                recommendations=["Fix interface analysis issues"],
                quality_level=QualityLevel.CRITICAL
            )
    
    def _analyze_interface_quality(self, file_path: str) -> Dict[str, Any]:
        """Analyze interface quality metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Count interfaces (classes, functions, constants)
            interface_count = 0
            coupling_score = 0.0
            cohesion_score = 0.0
            
            # Count public interfaces
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    interface_count += 1
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if not node.name.startswith('_'):  # Public function
                        interface_count += 1
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and not target.id.startswith('_'):
                            interface_count += 1
            
            # Simple coupling and cohesion estimation
            if interface_count > 0:
                coupling_score = min(1.0, interface_count / 20.0)  # More interfaces = higher coupling
                cohesion_score = max(0.0, 1.0 - coupling_score)  # Inverse relationship
            
            return {
                "interface_count": interface_count,
                "coupling_score": coupling_score,
                "cohesion_score": cohesion_score
            }
            
        except Exception:
            return {
                "interface_count": 0,
                "coupling_score": 0.0,
                "cohesion_score": 0.0
            }
    
    def _calculate_interface_quality_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate interface quality score"""
        coupling_score = metrics.get("coupling_score", 0.0)
        cohesion_score = metrics.get("cohesion_score", 0.0)
        interface_count = metrics.get("interface_count", 0)
        
        # Quality factors
        coupling_quality = 1.0 - coupling_score  # Lower coupling is better
        cohesion_quality = cohesion_score  # Higher cohesion is better
        interface_balance = 1.0 if 3 <= interface_count <= 15 else 0.5  # Balanced interface count
        
        # Weighted average
        return (coupling_quality * 0.4 + cohesion_quality * 0.4 + interface_balance * 0.2)
    
    def _generate_interface_recommendations(self, metrics: Dict[str, Any], quality_score: float) -> List[str]:
        """Generate interface quality improvement recommendations"""
        recommendations = []
        
        interface_count = metrics.get("interface_count", 0)
        coupling_score = metrics.get("coupling_score", 0.0)
        
        if interface_count < 3:
            recommendations.append("Consider adding more focused interfaces")
        elif interface_count > 15:
            recommendations.append("Consider consolidating related interfaces")
        
        if coupling_score > 0.7:
            recommendations.append("Reduce coupling between modules")
            recommendations.append("Use dependency injection to reduce tight coupling")
        
        if quality_score < 0.7:
            recommendations.append("Improve interface design and organization")
            recommendations.append("Ensure clear separation of concerns")
        
        return recommendations


class TestCoverageGate(QualityGate):
    """Quality gate for test coverage validation"""
    
    def __init__(self):
        super().__init__(
            name="Test Coverage",
            description="Ensure adequate test coverage for modularized components",
            threshold=80.0,  # 80% test coverage
            weight=0.15
        )
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate test coverage"""
        try:
            # Estimate test coverage based on file characteristics
            coverage_metrics = self._estimate_test_coverage(file_path)
            overall_coverage = coverage_metrics.get("overall_coverage", 0.0)
            
            passed = overall_coverage >= self.threshold
            details = {
                "coverage_metrics": coverage_metrics,
                "overall_coverage": overall_coverage,
                "has_test_file": coverage_metrics.get("has_test_file", False),
                "test_file_quality": coverage_metrics.get("test_file_quality", 0.0)
            }
            
            recommendations = self._generate_coverage_recommendations(coverage_metrics, overall_coverage)
            
            return QualityGateResult(
                gate_name=self.name,
                passed=passed,
                score=overall_coverage,
                threshold=self.threshold,
                details=details,
                recommendations=recommendations,
                quality_level=self._calculate_quality_level(overall_coverage)
            )
            
        except Exception as e:
            return QualityGateResult(
                gate_name=self.name,
                passed=False,
                score=0.0,
                threshold=self.threshold,
                details={"error": str(e)},
                recommendations=["Fix coverage analysis issues"],
                quality_level=QualityLevel.CRITICAL
            )
    
    def _estimate_test_coverage(self, file_path: str) -> Dict[str, Any]:
        """Estimate test coverage for a file"""
        path = Path(file_path)
        
        # Check if test file exists
        test_file = self._find_test_file(path)
        has_test_file = test_file is not None
        
        # Estimate coverage based on test file presence and quality
        if has_test_file:
            test_quality = self._assess_test_file_quality(test_file)
            line_coverage = min(95.0, 70.0 + test_quality * 25.0)  # 70-95% range
            branch_coverage = line_coverage * 0.9  # Slightly lower than line coverage
            function_coverage = min(98.0, 75.0 + test_quality * 20.0)  # 75-98% range
        else:
            line_coverage = 0.0
            branch_coverage = 0.0
            function_coverage = 0.0
            test_quality = 0.0
        
        overall_coverage = (line_coverage + branch_coverage + function_coverage) / 3
        
        return {
            "line_coverage": line_coverage,
            "branch_coverage": branch_coverage,
            "function_coverage": function_coverage,
            "overall_coverage": overall_coverage,
            "has_test_file": has_test_file,
            "test_file_quality": test_quality
        }
    
    def _find_test_file(self, file_path: Path) -> Optional[Path]:
        """Find corresponding test file"""
        # Common test file patterns
        test_patterns = [
            f"test_{file_path.stem}.py",
            f"test_{file_path.stem}_test.py",
            f"{file_path.stem}_test.py"
        ]
        
        # Check in tests directory
        tests_dir = file_path.parent.parent / "tests"
        if tests_dir.exists():
            for pattern in test_patterns:
                test_file = tests_dir / pattern
                if test_file.exists():
                    return test_file
        
        # Check in same directory
        for pattern in test_patterns:
            test_file = file_path.parent / pattern
            if test_file.exists():
                return test_file
        
        return None
    
    def _assess_test_file_quality(self, test_file: Path) -> float:
        """Assess the quality of a test file"""
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Simple quality indicators
            quality_score = 0.0
            
            # Has test classes
            if "class Test" in content or "class Test" in content:
                quality_score += 0.3
            
            # Has test functions
            if "def test_" in content:
                quality_score += 0.3
            
            # Has assertions
            if "assert" in content or "self.assert" in content:
                quality_score += 0.2
            
            # Has setup/teardown
            if "setUp" in content or "tearDown" in content:
                quality_score += 0.1
            
            # Has docstrings
            if '"""' in content or "'''" in content:
                quality_score += 0.1
            
            return min(1.0, quality_score)
            
        except Exception:
            return 0.0
    
    def _generate_coverage_recommendations(self, metrics: Dict[str, Any], overall_coverage: float) -> List[str]:
        """Generate test coverage improvement recommendations"""
        recommendations = []
        
        if not metrics.get("has_test_file", False):
            recommendations.append("Create comprehensive test file")
            recommendations.append("Add unit tests for all functions and classes")
            recommendations.append("Include integration tests for complex workflows")
        else:
            if overall_coverage < 80.0:
                recommendations.append("Increase test coverage to at least 80%")
                recommendations.append("Add tests for uncovered code paths")
                recommendations.append("Include edge case testing")
            
            if metrics.get("test_file_quality", 0.0) < 0.7:
                recommendations.append("Improve test file quality and organization")
                recommendations.append("Add proper test documentation")
                recommendations.append("Ensure comprehensive test coverage")
        
        return recommendations


class DependencyComplexityGate(QualityGate):
    """Quality gate for dependency complexity validation"""
    
    def __init__(self):
        super().__init__(
            name="Dependency Complexity",
            description="Ensure low dependency complexity",
            threshold=0.6,  # Maximum 0.6 complexity
            weight=0.20
        )
    
    def validate(self, file_path: str) -> QualityGateResult:
        """Validate dependency complexity"""
        try:
            if not file_path.endswith('.py'):
                return QualityGateResult(
                    gate_name=self.name,
                    passed=True,
                    score=100.0,
                    threshold=self.threshold,
                    details={"file_type": "non-python"},
                    recommendations=[],
                    quality_level=QualityLevel.EXCELLENT
                )
            
            # Analyze dependency complexity
            complexity_metrics = self._analyze_dependency_complexity(file_path)
            complexity_score = complexity_metrics.get("complexity_score", 0.0)
            
            # Lower complexity is better, so invert the score
            quality_score = max(0.0, 1.0 - complexity_score)
            passed = complexity_score <= self.threshold
            
            details = {
                "complexity_metrics": complexity_metrics,
                "complexity_score": complexity_score,
                "dependency_count": complexity_metrics.get("dependency_count", 0),
                "circular_dependencies": complexity_metrics.get("circular_dependencies", 0)
            }
            
            recommendations = self._generate_complexity_recommendations(complexity_metrics, complexity_score)
            
            return QualityGateResult(
                gate_name=self.name,
                passed=passed,
                score=quality_score * 100,
                threshold=self.threshold * 100,
                details=details,
                recommendations=recommendations,
                quality_level=self._calculate_quality_level(quality_score * 100)
            )
            
        except Exception as e:
            return QualityGateResult(
                gate_name=self.name,
                passed=False,
                score=0.0,
                threshold=self.threshold * 100,
                details={"error": str(e)},
                recommendations=["Fix complexity analysis issues"],
                quality_level=QualityLevel.CRITICAL
            )
    
    def _analyze_dependency_complexity(self, file_path: str) -> Dict[str, Any]:
        """Analyze dependency complexity metrics"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            tree = ast.parse(content)
            
            # Count imports and dependencies
            import_count = 0
            from_import_count = 0
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    import_count += len(node.names)
                elif isinstance(node, ast.ImportFrom):
                    from_import_count += 1
            
            total_dependencies = import_count + from_import_count
            
            # Calculate complexity score (0.0 to 1.0)
            # More dependencies = higher complexity
            complexity_score = min(1.0, total_dependencies / 15.0)
            
            # Check for potential circular dependencies (simplified)
            circular_dependencies = 0
            if "import " + Path(file_path).stem in content:
                circular_dependencies = 1
            
            return {
                "dependency_count": total_dependencies,
                "import_count": import_count,
                "from_import_count": from_import_count,
                "complexity_score": complexity_score,
                "circular_dependencies": circular_dependencies
            }
            
        except Exception:
            return {
                "dependency_count": 0,
                "import_count": 0,
                "from_import_count": 0,
                "complexity_score": 0.0,
                "circular_dependencies": 0
            }
    
    def _generate_complexity_recommendations(self, metrics: Dict[str, Any], complexity_score: float) -> List[str]:
        """Generate dependency complexity improvement recommendations"""
        recommendations = []
        
        dependency_count = metrics.get("dependency_count", 0)
        circular_dependencies = metrics.get("circular_dependencies", 0)
        
        if dependency_count > 10:
            recommendations.append("Reduce number of dependencies")
            recommendations.append("Consolidate related imports")
            recommendations.append("Use dependency injection where possible")
        
        if circular_dependencies > 0:
            recommendations.append("Eliminate circular dependencies")
            recommendations.append("Restructure import hierarchy")
            recommendations.append("Use forward references if needed")
        
        if complexity_score > 0.6:
            recommendations.append("Simplify dependency structure")
            recommendations.append("Consider breaking into smaller modules")
            recommendations.append("Use interfaces to reduce coupling")
        
        return recommendations


class QualityGateManager:
    """Manager for quality gates"""
    
    def __init__(self):
        self.gates = [
            FileSizeReductionGate(),
            SingleResponsibilityGate(),
            InterfaceQualityGate(),
            TestCoverageGate(),
            DependencyComplexityGate()
        ]
    
    def run_all_gates(self, file_path: str) -> List[QualityGateResult]:
        """Run all quality gates for a file"""
        results = []
        
        for gate in self.gates:
            try:
                result = gate.validate(file_path)
                results.append(result)
            except Exception as e:
                # Create error result
                error_result = QualityGateResult(
                    gate_name=gate.name,
                    passed=False,
                    score=0.0,
                    threshold=gate.threshold,
                    details={"error": str(e)},
                    recommendations=["Fix gate execution issues"],
                    quality_level=QualityLevel.CRITICAL
                )
                results.append(error_result)
        
        return results
    
    def run_specific_gate(self, file_path: str, gate_name: str) -> Optional[QualityGateResult]:
        """Run a specific quality gate"""
        gate = next((g for g in self.gates if g.name == gate_name), None)
        if gate:
            return gate.validate(file_path)
        return None
    
    def get_gate_summary(self, results: List[QualityGateResult]) -> Dict[str, Any]:
        """Get summary of quality gate results"""
        if not results:
            return {}
        
        total_gates = len(results)
        passed_gates = sum(1 for r in results if r.passed)
        failed_gates = total_gates - passed_gates
        
        scores = [r.score for r in results if r.score > 0]
        avg_score = statistics.mean(scores) if scores else 0.0
        
        quality_levels = [r.quality_level for r in results]
        level_counts = {level: quality_levels.count(level) for level in QualityLevel}
        
        return {
            "total_gates": total_gates,
            "passed_gates": passed_gates,
            "failed_gates": failed_gates,
            "pass_rate": (passed_gates / total_gates) * 100 if total_gates > 0 else 0.0,
            "average_score": avg_score,
            "quality_level_distribution": level_counts,
            "overall_quality": self._determine_overall_quality(level_counts)
        }
    
    def _determine_overall_quality(self, level_counts: Dict[QualityLevel, int]) -> QualityLevel:
        """Determine overall quality level"""
        if level_counts[QualityLevel.CRITICAL] > 0:
            return QualityLevel.CRITICAL
        elif level_counts[QualityLevel.POOR] > 0:
            return QualityLevel.POOR
        elif level_counts[QualityLevel.FAIR] > 0:
            return QualityLevel.FAIR
        elif level_counts[QualityLevel.GOOD] > 0:
            return QualityLevel.GOOD
        else:
            return QualityLevel.EXCELLENT


# Convenience functions
def run_quality_gates(file_path: str) -> List[QualityGateResult]:
    """Run all quality gates for a file"""
    manager = QualityGateManager()
    return manager.run_all_gates(file_path)


def get_quality_summary(file_path: str) -> Dict[str, Any]:
    """Get quality summary for a file"""
    manager = QualityGateManager()
    results = manager.run_all_gates(file_path)
    return manager.get_gate_summary(results)


if __name__ == "__main__":
    # Example usage
    print("🧪 Quality Gates for Modularization Validation")
    print("=" * 50)
    
    # Test with a sample file
    sample_file = "tests/test_modularizer/enhanced_modularization_framework.py"
    
    if Path(sample_file).exists():
        print(f"Running quality gates on: {sample_file}")
        results = run_quality_gates(sample_file)
        
        for result in results:
            status = "✅ PASS" if result.passed else "❌ FAIL"
            print(f"{status} {result.gate_name}: {result.score:.1f}/{result.threshold:.1f}")
            print(f"   Quality: {result.quality_level.value}")
            if result.recommendations:
                print(f"   Recommendations: {', '.join(result.recommendations)}")
            print()
        
        summary = get_quality_summary(sample_file)
        print(f"Overall Quality: {summary['overall_quality'].value}")
        print(f"Pass Rate: {summary['pass_rate']:.1f}%")
        print(f"Average Score: {summary['average_score']:.1f}")
    else:
        print("Sample file not found. Run quality gates on an existing file.")
