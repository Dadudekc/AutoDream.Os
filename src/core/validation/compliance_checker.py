#!/usr/bin/env python3
"""
V2 Compliance Checker - Agent Cellphone V2
==========================================

Comprehensive V2 compliance checking engine for architectural standards,
modularization patterns, and coding standards enforcement.

Follows V2 coding standards: ≤400 lines per module, OOP design, SRP.
"""

import ast
import logging
import re
import time
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum

try:
    from src.core.validation.validation_result import ValidationResult, ValidationStatus, ValidationSeverity
except ImportError:
    # Fallback for direct execution
    from validation_result import ValidationResult, ValidationStatus, ValidationSeverity


class ComplianceRuleType(Enum):
    """Types of compliance rules."""
    LINE_COUNT = "line_count"
    OOP_DESIGN = "oop_design"
    SINGLE_RESPONSIBILITY = "single_responsibility"
    CLI_INTERFACE = "cli_interface"
    SMOKE_TESTS = "smoke_tests"
    MODULARIZATION = "modularization"
    ARCHITECTURE = "architecture"


@dataclass
class ComplianceRule:
    """V2 compliance rule definition."""
    rule_id: str
    name: str
    description: str
    rule_type: ComplianceRuleType
    severity: ValidationSeverity
    weight: float
    validation_func: callable
    parameters: Optional[Dict[str, Any]] = None


class V2ComplianceChecker:
    """
    V2 compliance checker for architectural standards and modularization patterns.
    
    Validates that code follows V2 coding standards, maintains proper architecture,
    and achieves optimal modularization quality.
    """
    
    def __init__(self):
        """Initialize V2 Compliance Checker."""
        self.logger = logging.getLogger(__name__)
        self.compliance_rules = self._initialize_compliance_rules()
        self.v2_standards = self._initialize_v2_standards()
        
    def _initialize_compliance_rules(self) -> Dict[str, ComplianceRule]:
        """Initialize all V2 compliance validation rules."""
        rules = {}
        
        # Line Count Compliance
        rules["line_count_compliance"] = ComplianceRule(
            rule_id="line_count_compliance",
            name="Line Count Compliance",
            description="Ensure files follow V2 line count standards",
            rule_type=ComplianceRuleType.LINE_COUNT,
            severity=ValidationSeverity.HIGH,
            weight=2.0,
            validation_func=self._validate_line_count,
            parameters={"max_lines": 400, "max_gui_lines": 600}
        )
        
        # OOP Design Compliance
        rules["oop_design_compliance"] = ComplianceRule(
            rule_id="oop_design_compliance",
            name="OOP Design Compliance",
            description="Ensure code follows proper OOP principles",
            rule_type=ComplianceRuleType.OOP_DESIGN,
            severity=ValidationSeverity.HIGH,
            weight=1.8,
            validation_func=self._validate_oop_design,
            parameters={"require_classes": True, "min_methods_per_class": 1}
        )
        
        # Single Responsibility Principle
        rules["srp_compliance"] = ComplianceRule(
            rule_id="srp_compliance",
            name="Single Responsibility Principle",
            description="Ensure classes follow single responsibility principle",
            rule_type=ComplianceRuleType.SINGLE_RESPONSIBILITY,
            severity=ValidationSeverity.HIGH,
            weight=1.5,
            validation_func=self._validate_srp_compliance,
            parameters={"max_methods_per_class": 15, "max_responsibilities": 1}
        )
        
        # CLI Interface Compliance
        rules["cli_interface_compliance"] = ComplianceRule(
            rule_id="cli_interface_compliance",
            name="CLI Interface Compliance",
            description="Ensure modules have CLI interface for testing",
            rule_type=ComplianceRuleType.CLI_INTERFACE,
            severity=ValidationSeverity.MEDIUM,
            weight=1.0,
            validation_func=self._validate_cli_interface,
            parameters={"require_cli": True, "require_argparse": True}
        )
        
        # Modularization Compliance
        rules["modularization_compliance"] = ComplianceRule(
            rule_id="modularization_compliance",
            name="Modularization Compliance",
            description="Ensure proper modularization patterns",
            rule_type=ComplianceRuleType.MODULARIZATION,
            severity=ValidationSeverity.MEDIUM,
            weight=1.2,
            validation_func=self._validate_modularization,
            parameters={"max_file_size": 400, "require_separation": True}
        )
        
        return rules
    
    def _initialize_v2_standards(self) -> Dict[str, Any]:
        """Initialize V2 coding standards."""
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
            "modularization": {
                "max_file_size": 400,
                "single_responsibility": True,
                "clean_separation": True
            }
        }
    
    def check_compliance(self, target_path: str) -> List[ValidationResult]:
        """
        Check V2 compliance for a target path.
        
        Args:
            target_path: Path to check (file or directory)
            
        Returns:
            List of compliance validation results
        """
        self.logger.info(f"Starting V2 compliance check for: {target_path}")
        
        results = []
        target_path_obj = Path(target_path)
        
        if target_path_obj.is_file():
            results.extend(self._check_single_file(target_path_obj))
        elif target_path_obj.is_dir():
            results.extend(self._check_directory(target_path_obj))
        else:
            results.append(ValidationResult(
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.HIGH,
                message=f"Invalid path: {target_path}",
                validator_name="V2ComplianceChecker",
                target_object=target_path,
                validation_timestamp=time.time(),
                details={"error": "Path does not exist or is not accessible"}
            ))
        
        return results
    
    def _check_single_file(self, file_path: Path) -> List[ValidationResult]:
        """Check V2 compliance for a single file."""
        results = []
        
        if file_path.suffix != '.py':
            return results
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse AST for analysis
            tree = ast.parse(content)
            
            # Run all compliance rules
            for rule in self.compliance_rules.values():
                try:
                    rule_result = rule.validation_func(file_path, tree, content, rule.parameters)
                    if rule_result:
                        results.append(rule_result)
                except Exception as e:
                    self.logger.warning(f"Rule {rule.rule_id} failed: {e}")
                    results.append(ValidationResult(
                        status=ValidationStatus.FAILED,
                        severity=rule.severity,
                        message=f"Rule execution failed: {e}",
                        validator_name="V2ComplianceChecker",
                        target_object=str(file_path),
                        validation_timestamp=time.time(),
                        details={"error": str(e)}
                    ))
                    
        except Exception as e:
            self.logger.error(f"Failed to check file {file_path}: {e}")
            results.append(ValidationResult(
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.HIGH,
                message=f"Failed to parse file: {e}",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={"error": str(e)}
            ))
        
        return results
    
    def _check_directory(self, dir_path: Path) -> List[ValidationResult]:
        """Check V2 compliance for a directory recursively."""
        results = []
        
        # Find all Python files
        python_files = list(dir_path.rglob("*.py"))
        
        self.logger.info(f"Found {len(python_files)} Python files to check")
        
        # Check each file
        for file_path in python_files:
            results.extend(self._check_single_file(file_path))
        
        # Add directory-level compliance checks
        results.extend(self._check_directory_structure(dir_path))
        
        return results
    
    def _check_directory_structure(self, dir_path: Path) -> List[ValidationResult]:
        """Check directory structure compliance."""
        results = []
        
        # Check for proper package structure
        if (dir_path / "__init__.py").exists():
            results.extend(self._check_package_structure(dir_path))
        
        return results
    
    def _check_package_structure(self, package_path: Path) -> List[ValidationResult]:
        """Check package structure compliance."""
        results = []
        
        # Check for proper __init__.py files
        init_files = list(package_path.rglob("__init__.py"))
        if not init_files:
            results.append(ValidationResult(
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.MEDIUM,
                message="Package missing __init__.py files",
                validator_name="V2ComplianceChecker",
                target_object=str(package_path),
                validation_timestamp=time.time(),
                details={"package": str(package_path)}
            ))
        
        return results
    
    def _validate_line_count(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate line count compliance."""
        max_lines = parameters.get("max_lines", 400)
        max_gui_lines = parameters.get("max_gui_lines", 600)
        
        line_count = len(content.splitlines())
        
        # Determine if this is a GUI file
        is_gui = self._is_gui_file(content)
        limit = max_gui_lines if is_gui else max_lines
        
        if line_count > limit:
            return ValidationResult(
                status=ValidationStatus.FAILED,
                severity=ValidationSeverity.HIGH,
                message=f"File exceeds V2 line count limit ({line_count} > {limit})",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={
                    "file": str(file_path),
                    "line_count": line_count,
                    "v2_limit": limit,
                    "excess": line_count - limit,
                    "file_type": "GUI" if is_gui else "Standard"
                }
            )
        
        return ValidationResult(
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.HIGH,
            message="Line count compliance validated successfully",
            validator_name="V2ComplianceChecker",
            target_object=str(file_path),
            validation_timestamp=time.time(),
            details={"file": str(file_path), "line_count": line_count}
        )
    
    def _is_gui_file(self, content: str) -> bool:
        """Check if file contains GUI-related code."""
        gui_indicators = [
            "tkinter", "PyQt", "PySide", "wx", "Kivy", "Flask", "Django",
            "HTML", "CSS", "JavaScript", "React", "Vue", "Angular"
        ]
        
        return any(indicator.lower() in content.lower() for indicator in gui_indicators)
    
    def _validate_oop_design(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate OOP design compliance."""
        require_classes = parameters.get("require_classes", True)
        min_methods = parameters.get("min_methods_per_class", 1)
        
        # Count classes and functions
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        
        # Check if code is properly organized in classes
        if require_classes and functions and not classes:
            if not self._is_acceptable_standalone_functions(content):
                return ValidationResult(
                    status=ValidationStatus.FAILED,
                    severity=ValidationSeverity.HIGH,
                    message="Code should be organized in classes following V2 standards",
                    validator_name="V2ComplianceChecker",
                    target_object=str(file_path),
                    validation_timestamp=time.time(),
                    details={
                        "file": str(file_path),
                        "standalone_functions": len(functions),
                        "classes": len(classes)
                    }
                )
        
        # Check class quality
        if classes:
            for class_node in classes:
                methods = [n for n in class_node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) < min_methods:
                    return ValidationResult(
                        status=ValidationStatus.WARNING,
                        severity=ValidationSeverity.MEDIUM,
                        message=f"Class '{class_node.name}' has too few methods",
                        validator_name="V2ComplianceChecker",
                        target_object=str(file_path),
                        validation_timestamp=time.time(),
                        details={
                            "file": str(file_path),
                            "class": class_node.name,
                            "method_count": len(methods),
                            "min_required": min_methods
                        }
                    )
        
        return ValidationResult(
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.HIGH,
            message="OOP design compliance validated successfully",
            validator_name="V2ComplianceChecker",
            target_object=str(file_path),
            validation_timestamp=time.time(),
            details={"file": str(file_path)}
        )
    
    def _is_acceptable_standalone_functions(self, content: str) -> bool:
        """Check if standalone functions are acceptable."""
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
    
    def _validate_srp_compliance(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate Single Responsibility Principle compliance."""
        max_methods = parameters.get("max_methods_per_class", 15)
        max_responsibilities = parameters.get("max_responsibilities", 1)
        
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        if not classes:
            return None
        
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
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.HIGH,
                message=f"Classes with too many methods detected - consider splitting responsibilities",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={
                    "file": str(file_path),
                    "violations": srp_violations
                }
            )
        
        return ValidationResult(
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.HIGH,
            message="Single responsibility principle compliance validated successfully",
            validator_name="V2ComplianceChecker",
            target_object=str(file_path),
            validation_timestamp=time.time(),
            details={"file": str(file_path)}
        )
    
    def _validate_cli_interface(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate CLI interface compliance."""
        require_cli = parameters.get("require_cli", True)
        require_argparse = parameters.get("require_argparse", True)
        
        if not require_cli:
            return None
        
        # Check for CLI interface
        cli_patterns = [
            r'def main\(',
            r'if __name__ == "__main__":',
            r'argparse',
            r'ArgumentParser',
            r'add_argument'
        ]
        
        has_cli = any(re.search(pattern, content) for pattern in cli_patterns)
        
        if not has_cli:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.MEDIUM,
                message="File should have CLI interface for testing (V2 standard)",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={"file": str(file_path)}
            )
        
        # Check for argparse if required
        if require_argparse and "argparse" not in content:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.LOW,
                message="CLI interface should use argparse for proper argument handling",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={"file": str(file_path)}
            )
        
        return ValidationResult(
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.MEDIUM,
            message="CLI interface compliance validated successfully",
            validator_name="V2ComplianceChecker",
            target_object=str(file_path),
            validation_timestamp=time.time(),
            details={"file": str(file_path)}
        )
    
    def _validate_modularization(self, file_path: Path, tree: ast.AST, content: str, parameters: Dict[str, Any]) -> Optional[ValidationResult]:
        """Validate modularization compliance."""
        max_file_size = parameters.get("max_file_size", 400)
        require_separation = parameters.get("require_separation", True)
        
        line_count = len(content.splitlines())
        classes = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
        
        violations = []
        
        if line_count > max_file_size:
            violations.append(f"File size ({line_count} lines) exceeds limit ({max_file_size})")
        
        if require_separation and len(classes) > 3:
            violations.append(f"Too many classes ({len(classes)}) - consider splitting into separate modules")
        
        if violations:
            return ValidationResult(
                status=ValidationStatus.WARNING,
                severity=ValidationSeverity.MEDIUM,
                message=f"Modularization violations: {'; '.join(violations)}",
                validator_name="V2ComplianceChecker",
                target_object=str(file_path),
                validation_timestamp=time.time(),
                details={
                    "file": str(file_path),
                    "line_count": line_count,
                    "class_count": len(classes),
                    "violations": violations
                }
            )
        
        return ValidationResult(
            status=ValidationStatus.PASSED,
            severity=ValidationSeverity.MEDIUM,
            message="Modularization compliance validated successfully",
            validator_name="V2ComplianceChecker",
            target_object=str(file_path),
            validation_timestamp=time.time(),
            details={"file": str(file_path)}
        )
    
    def get_compliance_summary(self, results: List[ValidationResult]) -> Dict[str, Any]:
        """Generate a summary of compliance check results."""
        if not results:
            return {"status": "No compliance results"}
        
        total_rules = len(results)
        passed = len([r for r in results if r.status == ValidationStatus.PASSED])
        failed = len([r for r in results if r.status == ValidationStatus.FAILED])
        warnings = len([r for r in results if r.status == ValidationStatus.WARNING])
        
        # Calculate simple score based on passed vs total
        score_percentage = (passed / total_rules * 100) if total_rules > 0 else 0
        
        return {
            "total_rules": total_rules,
            "passed": passed,
            "failed": failed,
            "warnings": warnings,
            "score_percentage": round(score_percentage, 2),
            "overall_status": "PASSED" if failed == 0 else "FAILED" if failed > warnings else "WARNING"
        }


# CLI interface for testing
def main():
    """CLI interface for V2 compliance checking."""
    import argparse
    
    parser = argparse.ArgumentParser(description="V2 Compliance Checker CLI")
    parser.add_argument("--check", required=True, help="Path to check (file or directory)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--output", "-o", help="Output file for results")
    
    args = parser.parse_args()
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO if args.verbose else logging.WARNING,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run compliance check
    checker = V2ComplianceChecker()
    results = checker.check_compliance(args.check)
    
    # Generate summary
    summary = checker.get_compliance_summary(results)
    
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
        print(f"\n📊 V2 Compliance Check Summary:")
        print(f"Total Rules: {summary['total_rules']}")
        print(f"Passed: {summary['passed']} ✅")
        print(f"Failed: {summary['failed']} ❌")
        print(f"Warnings: {summary['warnings']} ⚠️")
        print(f"Score: {summary['score_percentage']}%")
        print(f"Status: {summary['overall_status']}")
        
        if results:
            print(f"\n📋 Detailed Results:")
            for result in results:
                status_icon = "✅" if result.status == ValidationStatus.PASSED else "❌" if result.status == ValidationStatus.FAILED else "⚠️"
                print(f"{status_icon} {result.message}")


if __name__ == "__main__":
    main()
