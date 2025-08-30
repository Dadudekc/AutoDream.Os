#!/usr/bin/env python3
"""
Modularization Validator - Agent Cellphone V2
============================================

Specialized validator for modularization patterns, V2 compliance checking,
and modularization quality assessment.

Follows V2 coding standards: ≤400 lines per module, OOP design, SRP.
"""

import ast
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass
from enum import Enum

from src.core.validation.base_validator import BaseValidator
from src.core.validation.validation_result import ValidationResult, ValidationStatus, ValidationSeverity


class ModularizationPatternType(Enum):
    """Types of modularization patterns to validate."""
    SINGLE_RESPONSIBILITY = "single_responsibility"
    INTERFACE_SEGREGATION = "interface_segregation"
    DEPENDENCY_INVERSION = "dependency_inversion"
    OPEN_CLOSED = "open_closed"
    LISKOV_SUBSTITUTION = "liskov_substitution"
    COMPOSITION_OVER_INHERITANCE = "composition_over_inheritance"
    MODULE_SIZE = "module_size"
    IMPORT_ORGANIZATION = "import_organization"
    CLASS_STRUCTURE = "class_structure"
    METHOD_DISTRIBUTION = "method_distribution"


@dataclass
class ModularizationPattern:
    """Modularization pattern definition."""
    pattern_id: str
    name: str
    description: str
    pattern_type: ModularizationPatternType
    severity: ValidationSeverity
    weight: float
    validation_func: callable
    parameters: Optional[Dict[str, Any]] = None


class ModularizationValidator(BaseValidator):
    """
    Specialized validator for modularization patterns and V2 compliance.
    
    Validates that code follows proper modularization principles, maintains
    V2 coding standards, and achieves optimal architectural quality.
    """
    
    def __init__(self):
        """Initialize Modularization Validator."""
        super().__init__(
            validator_id="modularization_validator",
            name="Modularization Validator",
            description="Specialized validation for modularization patterns and V2 compliance"
        )
        
        self.logger = logging.getLogger(__name__)
        self.modularization_patterns = self._initialize_modularization_patterns()
        self.v2_standards = self._initialize_v2_standards()
        
    def _initialize_modularization_patterns(self) -> Dict[str, ModularizationPattern]:
        """Initialize all modularization pattern validation rules."""
        patterns = {}
        
        # Single Responsibility Principle
        patterns["srp_compliance"] = ModularizationPattern(
            pattern_id="srp_compliance",
            name="Single Responsibility Principle",
            description="Ensure each class has a single, well-defined responsibility",
            pattern_type=ModularizationPatternType.SINGLE_RESPONSIBILITY,
            severity=ValidationSeverity.HIGH,
            weight=2.0,
            validation_func=self._validate_srp_compliance,
            parameters={"max_responsibilities": 1, "max_methods_per_class": 15}
        )
        
        # Interface Segregation
        patterns["interface_segregation"] = ModularizationPattern(
            pattern_id="interface_segregation",
            name="Interface Segregation Principle",
            description="Ensure interfaces are focused and not bloated",
            pattern_type=ModularizationPatternType.INTERFACE_SEGREGATION,
            severity=ValidationSeverity.MEDIUM,
            weight=1.5,
            validation_func=self._validate_interface_segregation,
            parameters={"max_interface_methods": 10}
        )
        
        # Dependency Inversion
        patterns["dependency_inversion"] = ModularizationPattern(
            pattern_id="dependency_inversion",
            name="Dependency Inversion Principle",
            description="Ensure high-level modules don't depend on low-level modules",
            pattern_type=ModularizationPatternType.DEPENDENCY_INVERSION,
            severity=ValidationSeverity.MEDIUM,
            weight=1.3,
            validation_func=self._validate_dependency_inversion,
            parameters={"max_direct_dependencies": 5}
        )
        
        # Module Size Compliance
        patterns["module_size_compliance"] = ModularizationPattern(
            pattern_id="module_size_compliance",
            name="Module Size Compliance",
            description="Ensure modules follow V2 size standards",
            pattern_type=ModularizationPatternType.MODULE_SIZE,
            severity=ValidationSeverity.HIGH,
            weight=1.8,
            validation_func=self._validate_module_size,
            parameters={"max_lines": 400, "max_classes": 5, "max_functions": 20}
        )
        
        # Import Organization
        patterns["import_organization"] = ModularizationPattern(
            pattern_id="import_organization",
            name="Import Organization",
            description="Ensure imports are properly organized and minimal",
            pattern_type=ModularizationPatternType.IMPORT_ORGANIZATION,
            severity=ValidationSeverity.MEDIUM,
            weight=1.0,
            validation_func=self._validate_import_organization,
            parameters={"max_imports": 15, "max_from_imports": 10}
        )
        
        # Class Structure
        patterns["class_structure"] = ModularizationPattern(
            pattern_id="class_structure",
            name="Class Structure Quality",
            description="Ensure classes have proper structure and organization",
            pattern_type=ModularizationPatternType.CLASS_STRUCTURE,
            severity=ValidationSeverity.MEDIUM,
            weight=1.2,
            validation_func=self._validate_class_structure,
            parameters={"min_methods_per_class": 1, "max_attributes": 20}
        )
        
        # Method Distribution
        patterns["method_distribution"] = ModularizationPattern(
            pattern_id="method_distribution",
            name="Method Distribution",
            description="Ensure methods are evenly distributed across classes",
            pattern_type=ModularizationPatternType.METHOD_DISTRIBUTION,
            severity=ValidationSeverity.LOW,
            weight=0.8,
            validation_func=self._validate_method_distribution,
            parameters={"max_methods_variance": 0.5}
        )
        
        return patterns
    
    def _initialize_v2_standards(self) -> Dict[str, Any]:
        """Initialize V2 coding standards for validation."""
        return {
            "line_count_limits": {
                "standard": 400,
                "gui": 600,
                "core": 400
            },
            "oop_requirements": {
                "all_code_in_classes": True,
                "clear_responsibilities": True,
                "proper_inheritance": True
            },
            "cli_interface": {
                "required": True,
                "argument_parsing": True,
                "help_system": True
            },
            "smoke_tests": {
                "required": True,
                "basic_functionality": True
            }
        }
    
    def validate_modularization(self, target_path: str) -> List[ValidationResult]:
        """
        Validate modularization patterns and V2 compliance.
        
        Args:
            target_path: Path to validate (file or directory)
            
        Returns:
            List of validation results
        """
        self.logger.info(f"Starting modularization validation for: {target_path}")
        
        results = []
        target_path_obj = Path(target_path)
        
        if target_path_obj.is_file():
            # Single file validation
            results.extend(self._validate_single_file(target_path_obj))
        elif target_path_obj.is_dir():
            # Directory validation
            results.extend(self._validate_directory(target_path_obj))
        else:
            results.append(ValidationResult(
                rule_id="modularization_validation",
                rule_name="Modularization Validation",
                status=ValidationStatus.FAILED,
                message=f"Invalid path: {target_path}",
                severity=ValidationSeverity.HIGH,
                details={"error": "Path does not exist or is not accessible"}
            ))
        
        return results
    
    def _validate_single_file(self, file_path: Path) -> List[ValidationResult]:
        """Validate a single file against modularization patterns."""
        results = []
        
        if file_path.suffix != '.py':
            return results
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for analysis
            tree = ast.parse(content)
            
            # Run all applicable pattern validations
            for pattern in self.modularization_patterns.values():
                try:
                    pattern_result = pattern.validation_func(file_path, tree, content, pattern.parameters)
                    if pattern_result:
                        results.append(pattern_result)
                except Exception as e:
                    self.logger.warning(f"Pattern {pattern.pattern_id} failed: {e}")
                    results.append(ValidationResult(
                        rule_id=pattern.pattern_id,
                        rule_name=pattern.name,
                        status=ValidationStatus.FAILED,
                        message=f"Pattern validation failed: {e}",
                        severity=pattern.severity,
                        details={"error": str(e)}
                    ))
            
            # Add V2 standards validation
            results.extend(self._validate_v2_standards(file_path, tree, content))
                    
        except Exception as e:
            self.logger.error(f"Failed to validate file {file_path}: {e}")
            results.append(ValidationResult(
                rule_id="file_parsing",
                rule_name="File Parsing",
                status=ValidationStatus.FAILED,
                message=f"Failed to parse file: {e}",
                severity=ValidationSeverity.HIGH,
                details={"error": str(e)}
            ))
        
        return results
    
    def _validate_directory(self, dir_path: Path) -> List[ValidationResult]:
        """Validate a directory recursively against modularization patterns."""
        results = []
        
        # Find all Python files
        python_files = list(dir_path.rglob("*.py"))
        
        self.logger.info(f"Found {len(python_files)} Python files to validate")
        
        # Validate each file
        for file_path in python_files:
            results.extend(self._validate_single_file(file_path))
        
        # Run directory-level validations
        results.extend(self._validate_directory_modularization(dir_path))
        
        return results
    
    def _validate_directory_modularization(self, dir_path: Path) -> List[ValidationResult]:
        """Validate directory-level modularization patterns."""
        results = []
        
        # Check for proper modularization structure
        python_files = [f for f in dir_path.rglob("*.py") if f.name != "__init__.py"]
        
        if len(python_files) > 0:
            # Analyze modularization distribution
            file_sizes = []
            for file_path in python_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    file_sizes.append(len(content.splitlines()))
                except:
                    continue
            
            if file_sizes:
                avg_size = sum(file_sizes) / len(file_sizes)
                max_size = max(file_sizes)
                
                if max_size > self.v2_standards["line_count_limits"]["standard"]:
                    results.append(ValidationResult(
                        rule_id="directory_modularization",
                        rule_name="Directory Modularization",
                        status=ValidationStatus.WARNING,
                        message=f"Directory contains files exceeding V2 line count limits",
                        severity=ValidationSeverity.MEDIUM,
                        details={
                            "directory": str(dir_path),
                            "max_file_size": max_size,
                            "avg_file_size": round(avg_size, 1),
                            "v2_limit": self.v2_standards["line_count_limits"]["standard"]
                        }
                    ))
        
        return results
    
    def _validate_v2_standards(self, file_path: Path, tree: ast.AST, content: str) -> List[ValidationResult]:
        """Validate V2 coding standards compliance."""
        results = []
        
        # Check line count compliance
        line_count = len(content.splitlines())
        max_lines = self.v2_standards["line_count_limits"]["standard"]
        
        if line_count > max_lines:
            results.append(ValidationResult(
                rule_id="v2_line_count",
                rule_name="V2 Line Count Compliance",
                status=ValidationStatus.FAILED,
                message=f"File exceeds V2 line count limit ({line_count} > {max_lines})",
                severity=ValidationSeverity.HIGH,
                details={
                    "file": str(file_path),
                    "line_count": line_count,
                    "v2_limit": max_lines,
                    "excess": line_count - max_lines
                }
            ))
        
        # Check OOP compliance
        class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        function_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        
        # Check if code is properly organized in classes
        if function_count > 0 and class_count == 0:
            # Functions outside classes - check if this is acceptable
            if not self._is_acceptable_standalone_functions(content):
                results.append(ValidationResult(
                    rule_id="v2_oop_compliance",
                    rule_name="V2 OOP Compliance",
                    status=ValidationStatus.WARNING,
                    message="Code should be organized in classes following V2 standards",
                    severity=ValidationSeverity.MEDIUM,
                    details={
                        "file": str(file_path),
                        "standalone_functions": function_count,
                        "classes": class_count
                    }
                ))
        
        # Check for CLI interface
        if not self._has_cli_interface(content):
            results.append(ValidationResult(
                rule_id="v2_cli_interface",
                rule_name="V2 CLI Interface",
                status=ValidationStatus.WARNING,
                message="File should have CLI interface for testing (V2 standard)",
                severity=ValidationSeverity.MEDIUM,
                details={"file": str(file_path)}
            ))
        
        return results
    
    def _is_acceptable_standalone_functions(self, content: str) -> bool:
        """Check if standalone functions are acceptable (e.g., utilities, scripts)."""
        # Acceptable patterns: main function, utility functions, script entry points
        acceptable_patterns = [
            r'def main\(',
            r'if __name__ == "__main__":',
            r'# utility',
            r'# script',
            r'# standalone'
        ]
        
        for pattern in acceptable_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return True
        
        return False
    
    def _has_cli_interface(self, content: str) -> bool:
        """Check if file has CLI interface."""
        cli_patterns = [
            r'def main\(',
            r'if __name__ == "__main__":',
            r'argparse',
            r'ArgumentParser',
            r'add_argument'
        ]
        
        for pattern in cli_patterns:
            if re.search(pattern, content):
                return True
        
        return False
    
    def _validate_srp_compliance(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate Single Responsibility Principle compliance."""
        max_responsibilities = parameters.get("max_responsibilities", 1)
        max_methods = parameters.get("max_methods_per_class", 15)
        
        # Count classes and their methods
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        if not classes:
            return None  # No classes to validate
        
        srp_violations = []
        for class_node in classes:
            methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
            if len(methods) > max_methods:
                srp_violations.append({
                    "class": class_node.name,
                    "method_count": len(methods),
                    "max_allowed": max_methods
                })
        
        if srp_violations:
            return ValidationResult(
                rule_id="srp_compliance",
                rule_name="Single Responsibility Principle",
                status=ValidationStatus.WARNING,
                message=f"Classes with too many methods detected - consider splitting responsibilities",
                severity=ValidationSeverity.HIGH,
                details={
                    "file": str(file_path),
                    "violations": srp_violations,
                    "max_methods_per_class": max_methods
                }
            )
        
        return ValidationResult(
            rule_id="srp_compliance",
            rule_name="Single Responsibility Principle",
            status=ValidationStatus.PASSED,
            message="Single responsibility principle compliance validated successfully",
            severity=ValidationSeverity.HIGH,
            details={"file": str(file_path)}
        )
    
    def _validate_interface_segregation(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate Interface Segregation Principle."""
        max_interface_methods = parameters.get("max_interface_methods", 10)
        
        # Look for interface-like classes (abstract base classes, protocols)
        interface_classes = []
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check if it's an interface-like class
                if self._is_interface_class(node):
                    methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                    if len(methods) > max_interface_methods:
                        interface_classes.append({
                            "class": node.name,
                            "method_count": len(methods),
                            "max_allowed": max_interface_methods
                        })
        
        if interface_classes:
            return ValidationResult(
                rule_id="interface_segregation",
                rule_name="Interface Segregation Principle",
                status=ValidationStatus.WARNING,
                message=f"Interface classes with too many methods detected - consider splitting interfaces",
                severity=ValidationSeverity.MEDIUM,
                details={
                    "file": str(file_path),
                    "interface_violations": interface_classes
                }
            )
        
        return ValidationResult(
            rule_id="interface_segregation",
            rule_name="Interface Segregation Principle",
            status=ValidationStatus.PASSED,
            message="Interface segregation principle validated successfully",
            severity=ValidationSeverity.MEDIUM,
            details={"file": str(file_path)}
        )
    
    def _is_interface_class(self, class_node: ast.ClassDef) -> bool:
        """Check if a class is interface-like."""
        # Look for interface indicators
        interface_indicators = [
            "abstract",
            "interface",
            "protocol",
            "base",
            "abc"
        ]
        
        class_name_lower = class_node.name.lower()
        for indicator in interface_indicators:
            if indicator in class_name_lower:
                return True
        
        # Check for abstract methods
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef):
                if any(decorator.id == "abstractmethod" for decorator in node.decorator_list if hasattr(decorator, 'id')):
                    return True
        
        return False
    
    def _validate_dependency_inversion(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate Dependency Inversion Principle."""
        max_direct_dependencies = parameters.get("max_direct_dependencies", 5)
        
        # Count direct imports and dependencies
        import_count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                import_count += 1
        
        if import_count > max_direct_dependencies:
            return ValidationResult(
                rule_id="dependency_inversion",
                rule_name="Dependency Inversion Principle",
                status=ValidationStatus.WARNING,
                message=f"Too many direct dependencies detected - consider abstraction layers",
                severity=ValidationSeverity.MEDIUM,
                details={
                    "file": str(file_path),
                    "import_count": import_count,
                    "max_recommended": max_direct_dependencies
                }
            )
        
        return ValidationResult(
            rule_id="dependency_inversion",
            rule_name="Dependency Inversion Principle",
            status=ValidationStatus.PASSED,
            message="Dependency inversion principle validated successfully",
            severity=ValidationSeverity.MEDIUM,
            details={"file": str(file_path)}
        )
    
    def _validate_module_size(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate module size compliance."""
        max_lines = parameters.get("max_lines", 400)
        max_classes = parameters.get("max_classes", 5)
        max_functions = parameters.get("max_functions", 20)
        
        line_count = len(content.splitlines())
        class_count = len([n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)])
        function_count = len([n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)])
        
        violations = []
        
        if line_count > max_lines:
            violations.append(f"Line count ({line_count}) exceeds limit ({max_lines})")
        
        if class_count > max_classes:
            violations.append(f"Class count ({class_count}) exceeds limit ({max_classes})")
        
        if function_count > max_functions:
            violations.append(f"Function count ({function_count}) exceeds limit ({max_functions})")
        
        if violations:
            return ValidationResult(
                rule_id="module_size_compliance",
                rule_name="Module Size Compliance",
                status=ValidationStatus.WARNING,
                message=f"Module size violations detected: {'; '.join(violations)}",
                severity=ValidationSeverity.HIGH,
                details={
                    "file": str(file_path),
                    "line_count": line_count,
                    "class_count": class_count,
                    "function_count": function_count,
                    "limits": {"lines": max_lines, "classes": max_classes, "functions": max_functions}
                }
            )
        
        return ValidationResult(
            rule_id="module_size_compliance",
            rule_name="Module Size Compliance",
            status=ValidationStatus.PASSED,
            message="Module size compliance validated successfully",
            severity=ValidationSeverity.HIGH,
            details={"file": str(file_path)}
        )
    
    def _validate_import_organization(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate import organization and minimality."""
        max_imports = parameters.get("max_imports", 15)
        max_from_imports = parameters.get("max_from_imports", 10)
        
        import_count = 0
        from_import_count = 0
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                import_count += len(node.names)
            elif isinstance(node, ast.ImportFrom):
                from_import_count += 1
        
        violations = []
        
        if import_count > max_imports:
            violations.append(f"Import count ({import_count}) exceeds limit ({max_imports})")
        
        if from_import_count > max_from_imports:
            violations.append(f"From-import count ({from_import_count}) exceeds limit ({max_from_imports})")
        
        if violations:
            return ValidationResult(
                rule_id="import_organization",
                rule_name="Import Organization",
                status=ValidationStatus.WARNING,
                message=f"Import organization violations: {'; '.join(violations)}",
                severity=ValidationSeverity.MEDIUM,
                details={
                    "file": str(file_path),
                    "import_count": import_count,
                    "from_import_count": from_import_count,
                    "limits": {"imports": max_imports, "from_imports": max_from_imports}
                }
            )
        
        return ValidationResult(
            rule_id="import_organization",
            rule_name="Import Organization",
            status=ValidationStatus.PASSED,
            message="Import organization validated successfully",
            severity=ValidationSeverity.MEDIUM,
            details={"file": str(file_path)}
        )
    
    def _validate_class_structure(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate class structure quality."""
        min_methods = parameters.get("min_methods_per_class", 1)
        max_attributes = parameters.get("max_attributes", 20)
        
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        if not classes:
            return None
        
        violations = []
        for class_node in classes:
            methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
            attributes = [n for n in class_node.body if isinstance(n, ast.Assign)]
            
            if len(methods) < min_methods:
                violations.append(f"Class '{class_node.name}' has too few methods ({len(methods)} < {min_methods})")
            
            if len(attributes) > max_attributes:
                violations.append(f"Class '{class_node.name}' has too many attributes ({len(attributes)} > {max_attributes})")
        
        if violations:
            return ValidationResult(
                rule_id="class_structure",
                rule_name="Class Structure Quality",
                status=ValidationStatus.WARNING,
                message=f"Class structure violations: {'; '.join(violations)}",
                severity=ValidationSeverity.MEDIUM,
                details={
                    "file": str(file_path),
                    "violations": violations
                }
            )
        
        return ValidationResult(
            rule_id="class_structure",
            rule_name="Class Structure Quality",
            status=ValidationStatus.PASSED,
            message="Class structure quality validated successfully",
            severity=ValidationSeverity.MEDIUM,
            details={"file": str(file_path)}
        )
    
    def _validate_method_distribution(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate method distribution across classes."""
        max_variance = parameters.get("max_methods_variance", 0.5)
        
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        if len(classes) < 2:
            return None  # Need multiple classes to check distribution
        
        method_counts = []
        for class_node in classes:
            methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
            method_counts.append(len(methods))
        
        if method_counts:
            avg_methods = sum(method_counts) / len(method_counts)
            variance = sum((count - avg_methods) ** 2 for count in method_counts) / len(method_counts)
            std_dev = variance ** 0.5
            
            if std_dev > avg_methods * max_variance:
                return ValidationResult(
                    rule_id="method_distribution",
                    rule_name="Method Distribution",
                    status=ValidationStatus.WARNING,
                    message="Method distribution is uneven across classes",
                    severity=ValidationSeverity.LOW,
                    details={
                        "file": str(file_path),
                        "method_counts": method_counts,
                        "average": round(avg_methods, 1),
                        "standard_deviation": round(std_dev, 1),
                        "max_variance_ratio": max_variance
                    }
                )
        
        return ValidationResult(
            rule_id="method_distribution",
            rule_name="Method Distribution",
            status=ValidationStatus.PASSED,
            message="Method distribution validated successfully",
            severity=ValidationSeverity.LOW,
            details={"file": str(file_path)}
        )
    
    def get_validation_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate a summary of modularization validation results."""
        if not results:
            return {"status": "No validation results"}
        
        total_patterns = len(results)
        passed = len([r for r in results if r.status == ValidationStatus.PASSED])
        failed = len([r for r in results if r.status == ValidationStatus.FAILED])
        warnings = len([r for r in results if r.status == ValidationStatus.WARNING])
        
        # Calculate weighted score
        total_weight = sum(self.modularization_patterns.get(r.rule_id, ModularizationPattern("", "", "", ModularizationPatternType.SINGLE_RESPONSIBILITY, ValidationSeverity.MEDIUM, 1.0, lambda: None)).weight 
                          for r in results if r.status == ValidationStatus.PASSED)
        max_weight = sum(pattern.weight for pattern in self.modularization_patterns.values())
        score_percentage = (total_weight / max_weight * 100) if max_weight > 0 else 0
        
        return {
            "total_patterns": total_patterns,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "score_percentage": round(score_percentage, 2),
            "overall_status": "PASSED" if failed == 0 else "FAILED" if failed > warnings else "WARNING"
        }


# CLI interface for testing
def main():
    """CLI interface for modularization validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Modularization Validator CLI")
    parser.add_argument("--validate", required=True, help="Path to validate (file or directory)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", "-o", help="Output file for results")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run validation
    validator = ModularizationValidator()
    results = validator.validate_modularization(args.validate)
    
    # Generate summary
    summary = validator.get_validation_summary(results)
    
    # Output results
    if args.output:
        import json
        with open(args.output, 'w') as f:
            json.dump({
                "summary": summary,
                "results": [vars(r) for r in results]
            }, f, indent=2, default=str)
        print(f"Results saved to: {args.output}")
    else:
        print(f"\n📊 Modularization Validation Summary:")
        print(f"Total Patterns: {summary['total_patterns']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Warnings: {summary['warnings']} ⚠️")
        print(f"Score: {summary['score_percentage']}%")
        print(f"Status: {summary['overall_status']}")
        
        if results:
            print(f"\n📋 Detailed Results:")
            for result in results:
                status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌" if result.status == ValidationStatus.FAILED else "⚠️"
                print(f"{status_icon} {result.rule_name}: {result.message}")


if __name__ == "__main__":
    main()
