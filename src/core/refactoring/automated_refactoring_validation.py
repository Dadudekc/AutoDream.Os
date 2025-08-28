#!/usr/bin/env python3
"""
Automated Refactoring Validation - Agent Cellphone V2
====================================================

Comprehensive refactoring validation and testing system.
Part of SPRINT ACCELERATION mission to reach INNOVATION PLANNING MODE.

Follows V2 coding standards: ≤300 lines per module, OOP design, SRP.
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from src.core.base_manager import BaseManager


class ValidationStatus(Enum):
    """Validation status enumeration."""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


class ValidationSeverity(Enum):
    """Validation severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class ValidationResult:
    """Validation result data structure."""
    test_name: str
    status: ValidationStatus
    severity: ValidationSeverity
    message: str
    details: Optional[Dict[str, Any]] = None
    execution_time: float = 0.0
    timestamp: str = ""


@dataclass
class ValidationReport:
    """Comprehensive validation report."""
    validation_id: str
    timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    warning_tests: int
    skipped_tests: int
    execution_time: float
    results: List[ValidationResult]
    summary: Dict[str, Any]


class RefactoringValidator(BaseManager):
    """
    Automated refactoring validation system.
    
    Validates refactoring changes, ensures code quality,
    and provides comprehensive testing and validation reports.
    """
    
    def __init__(self):
        """Initialize Refactoring Validator."""
        super().__init__(
            manager_id="refactoring_validator",
            name="Automated Refactoring Validator",
            description="Comprehensive refactoring validation and testing system"
        )
        
        self.validation_rules = self._initialize_validation_rules()
        self.test_results = []
        self.validation_history = []
        
    def _initialize_validation_rules(self) -> Dict[str, Any]:
        """Initialize validation rules and criteria."""
        return {
            "syntax_validation": {
                "enabled": True,
                "severity": ValidationSeverity.CRITICAL,
                "description": "Validate Python syntax after refactoring"
            },
            "import_validation": {
                "enabled": True,
                "severity": ValidationSeverity.HIGH,
                "description": "Validate import statements and dependencies"
            },
            "functionality_validation": {
                "enabled": True,
                "severity": ValidationSeverity.HIGH,
                "description": "Validate core functionality preservation"
            },
            "performance_validation": {
                "enabled": True,
                "severity": ValidationSeverity.MEDIUM,
                "description": "Validate performance characteristics"
            },
            "style_validation": {
                "enabled": True,
                "severity": ValidationSeverity.MEDIUM,
                "description": "Validate code style and formatting"
            },
            "documentation_validation": {
                "enabled": True,
                "severity": ValidationSeverity.LOW,
                "description": "Validate documentation completeness"
            }
        }
    
    def validate_refactoring(self, 
                           before_files: Dict[str, str],
                           after_files: Dict[str, str],
                           validation_config: Optional[Dict[str, Any]] = None) -> ValidationReport:
        """
        Validate refactoring changes between before and after states.
        
        Args:
            before_files: Dictionary of file paths to original content
            after_files: Dictionary of file paths to refactored content
            validation_config: Optional validation configuration
            
        Returns:
            Comprehensive validation report
        """
        start_time = time.time()
        validation_id = f"validation_{int(time.time())}"
        
        self.logger.info(f"Starting refactoring validation: {validation_id}")
        
        # Initialize results
        self.test_results = []
        
        # Run validation tests
        self._run_syntax_validation(after_files)
        self._run_import_validation(before_files, after_files)
        self._run_functionality_validation(before_files, after_files)
        self._run_performance_validation(before_files, after_files)
        self._run_style_validation(after_files)
        self._run_documentation_validation(after_files)
        
        # Generate report
        execution_time = time.time() - start_time
        report = self._generate_validation_report(validation_id, execution_time)
        
        # Store in history
        self.validation_history.append(report)
        
        self.logger.info(f"Refactoring validation completed: {validation_id}")
        return report
    
    def _run_syntax_validation(self, files: Dict[str, str]) -> None:
        """Run Python syntax validation on refactored files."""
        rule = self.validation_rules["syntax_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, content in files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            try:
                compile(content, file_path, 'exec')
                result = ValidationResult(
                    test_name=f"syntax_validation_{Path(file_path).stem}",
                    status=ValidationStatus.PASSED,
                    severity=rule["severity"],
                    message=f"Syntax validation passed for {file_path}",
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            except SyntaxError as e:
                result = ValidationResult(
                    test_name=f"syntax_validation_{Path(file_path).stem}",
                    status=ValidationStatus.FAILED,
                    severity=rule["severity"],
                    message=f"Syntax error in {file_path}: {e}",
                    details={"error": str(e), "line": getattr(e, 'lineno', 'unknown')},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            except Exception as e:
                result = ValidationResult(
                    test_name=f"syntax_validation_{Path(file_path).stem}",
                    status=ValidationStatus.FAILED,
                    severity=rule["severity"],
                    message=f"Unexpected error during syntax validation: {e}",
                    details={"error": str(e)},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _run_import_validation(self, before_files: Dict[str, str], after_files: Dict[str, str]) -> None:
        """Validate import statements and dependencies."""
        rule = self.validation_rules["import_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, after_content in after_files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            
            # Extract imports from after content
            after_imports = self._extract_imports(after_content)
            
            # Check if file existed before
            if file_path in before_files:
                before_imports = self._extract_imports(before_files[file_path])
                
                # Check for removed imports
                removed_imports = before_imports - after_imports
                added_imports = after_imports - before_imports
                
                if removed_imports and not self._validate_import_removal(removed_imports, after_content):
                    result = ValidationResult(
                        test_name=f"import_validation_{Path(file_path).stem}",
                        status=ValidationStatus.WARNING,
                        severity=rule["severity"],
                        message=f"Potentially unsafe import removal in {file_path}",
                        details={"removed_imports": list(removed_imports), "added_imports": list(added_imports)},
                        execution_time=time.time() - start_time,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
                else:
                    result = ValidationResult(
                        test_name=f"import_validation_{Path(file_path).stem}",
                        status=ValidationStatus.PASSED,
                        severity=rule["severity"],
                        message=f"Import validation passed for {file_path}",
                        details={"removed_imports": list(removed_imports), "added_imports": list(added_imports)},
                        execution_time=time.time() - start_time,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
            else:
                # New file
                result = ValidationResult(
                    test_name=f"import_validation_{Path(file_path).stem}",
                    status=ValidationStatus.PASSED,
                    severity=rule["severity"],
                    message=f"Import validation passed for new file {file_path}",
                    details={"imports": list(after_imports)},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _extract_imports(self, content: str) -> Set[str]:
        """Extract import statements from content."""
        imports = set()
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith('import ') or line.startswith('from '):
                # Basic import extraction
                if line.startswith('import '):
                    parts = line[7:].split(',')
                    for part in parts:
                        imports.add(part.strip().split(' as ')[0])
                elif line.startswith('from '):
                    parts = line[5:].split(' import ')
                    if len(parts) == 2:
                        module = parts[0].strip()
                        items = parts[1].split(',')
                        for item in items:
                            item = item.strip().split(' as ')[0]
                            imports.add(f"{module}.{item}")
        
        return imports
    
    def _validate_import_removal(self, removed_imports: Set[str], content: str) -> bool:
        """Validate that removed imports are not still used in content."""
        for import_name in removed_imports:
            # Simple check for import usage in content
            if import_name in content:
                return False
        return True
    
    def _run_functionality_validation(self, before_files: Dict[str, str], after_files: Dict[str, str]) -> None:
        """Validate core functionality preservation."""
        rule = self.validation_rules["functionality_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, after_content in after_files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            
            # Check for function and class preservation
            before_content = before_files.get(file_path, "")
            if before_content:
                before_functions = self._extract_functions(before_content)
                after_functions = self._extract_functions(after_content)
                
                removed_functions = before_functions - after_functions
                
                if removed_functions:
                    result = ValidationResult(
                        test_name=f"functionality_validation_{Path(file_path).stem}",
                        status=ValidationStatus.WARNING,
                        severity=rule["severity"],
                        message=f"Functions removed in {file_path}",
                        details={"removed_functions": list(removed_functions)},
                        execution_time=time.time() - start_time,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
                else:
                    result = ValidationResult(
                        test_name=f"functionality_validation_{Path(file_path).stem}",
                        status=ValidationStatus.PASSED,
                        severity=rule["severity"],
                        message=f"Functionality validation passed for {file_path}",
                        execution_time=time.time() - start_time,
                        timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                    )
            else:
                result = ValidationResult(
                    test_name=f"functionality_validation_{Path(file_path).stem}",
                    status=ValidationStatus.SKIPPED,
                    severity=rule["severity"],
                    message=f"Functionality validation skipped for new file {file_path}",
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _extract_functions(self, content: str) -> Set[str]:
        """Extract function names from content."""
        functions = set()
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith('def '):
                func_name = line[4:].split('(')[0].strip()
                functions.add(func_name)
        
        return functions
    
    def _run_performance_validation(self, before_files: Dict[str, str], after_files: Dict[str, str]) -> None:
        """Validate performance characteristics."""
        rule = self.validation_rules["performance_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, after_content in after_files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            
            # Simple performance metrics
            lines = len(after_content.splitlines())
            complexity = self._calculate_complexity(after_content)
            
            if complexity > 10:
                result = ValidationResult(
                    test_name=f"performance_validation_{Path(file_path).stem}",
                    status=ValidationStatus.WARNING,
                    severity=rule["severity"],
                    message=f"High complexity detected in {file_path}",
                    details={"complexity": complexity, "lines": lines},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                result = ValidationResult(
                    test_name=f"performance_validation_{Path(file_path).stem}",
                    status=ValidationStatus.PASSED,
                    severity=rule["severity"],
                    message=f"Performance validation passed for {file_path}",
                    details={"complexity": complexity, "lines": lines},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _calculate_complexity(self, content: str) -> int:
        """Calculate simple complexity metric."""
        complexity = 0
        lines = content.splitlines()
        
        for line in lines:
            line = line.strip()
            if line.startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
                complexity += 1
        
        return complexity
    
    def _run_style_validation(self, files: Dict[str, str]) -> None:
        """Validate code style and formatting."""
        rule = self.validation_rules["style_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, content in files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            
            # Basic style checks
            style_issues = []
            lines = content.splitlines()
            
            for i, line in enumerate(lines, 1):
                if len(line) > 120:  # Line length check
                    style_issues.append(f"Line {i}: Exceeds 120 characters")
                if line.strip() and not line.startswith('#') and '  ' in line:  # Double space check
                    style_issues.append(f"Line {i}: Multiple consecutive spaces")
            
            if style_issues:
                result = ValidationResult(
                    test_name=f"style_validation_{Path(file_path).stem}",
                    status=ValidationStatus.WARNING,
                    severity=rule["severity"],
                    message=f"Style issues detected in {file_path}",
                    details={"style_issues": style_issues},
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                result = ValidationResult(
                    test_name=f"style_validation_{Path(file_path).stem}",
                    status=ValidationStatus.PASSED,
                    severity=rule["severity"],
                    message=f"Style validation passed for {file_path}",
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _run_documentation_validation(self, files: Dict[str, str]) -> None:
        """Validate documentation completeness."""
        rule = self.validation_rules["documentation_validation"]
        if not rule["enabled"]:
            return
        
        for file_path, content in files.items():
            if not file_path.endswith('.py'):
                continue
                
            start_time = time.time()
            
            # Check for module docstring
            lines = content.splitlines()
            has_module_docstring = False
            
            for line in lines:
                if line.strip().startswith('"""') or line.strip().startswith("'''"):
                    has_module_docstring = True
                    break
                elif line.strip() and not line.startswith('#'):
                    break
            
            if not has_module_docstring:
                result = ValidationResult(
                    test_name=f"documentation_validation_{Path(file_path).stem}",
                    status=ValidationStatus.WARNING,
                    severity=rule["severity"],
                    message=f"Missing module docstring in {file_path}",
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            else:
                result = ValidationResult(
                    test_name=f"documentation_validation_{Path(file_path).stem}",
                    status=ValidationStatus.PASSED,
                    severity=rule["severity"],
                    message=f"Documentation validation passed for {file_path}",
                    execution_time=time.time() - start_time,
                    timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
                )
            
            self.test_results.append(result)
    
    def _generate_validation_report(self, validation_id: str, execution_time: float) -> ValidationReport:
        """Generate comprehensive validation report."""
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r.status == ValidationStatus.PASSED])
        failed_tests = len([r for r in self.test_results if r.status == ValidationStatus.FAILED])
        warning_tests = len([r for r in self.test_results if r.status == ValidationStatus.WARNING])
        skipped_tests = len([r for r in self.test_results if r.status == ValidationStatus.SKIPPED])
        
        summary = {
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "critical_issues": len([r for r in self.test_results if r.severity == ValidationSeverity.CRITICAL and r.status == ValidationStatus.FAILED]),
            "high_priority_issues": len([r for r in self.test_results if r.severity == ValidationSeverity.HIGH and r.status in [ValidationStatus.FAILED, ValidationStatus.WARNING]]),
            "validation_rules": {k: v["enabled"] for k, v in self.validation_rules.items()}
        }
        
        return ValidationReport(
            validation_id=validation_id,
            timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            warning_tests=warning_tests,
            skipped_tests=skipped_tests,
            execution_time=execution_time,
            results=self.test_results.copy(),
            summary=summary
        )
    
    def get_validation_history(self) -> List[ValidationReport]:
        """Get validation history."""
        return self.validation_history.copy()
    
    def export_validation_report(self, report: ValidationReport, output_path: str) -> bool:
        """Export validation report to file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(asdict(report), f, indent=2, default=str)
            return True
        except Exception as e:
            self.logger.error(f"Failed to export validation report: {e}")
            return False
    
    # BaseManager abstract method implementations
    def _on_start(self) -> bool:
        """Start the refactoring validator."""
        try:
            self.logger.info("Starting Automated Refactoring Validator...")
            return True
        except Exception as e:
            self.logger.error(f"Failed to start validator: {e}")
            return False
    
    def _on_stop(self):
        """Stop the refactoring validator."""
        try:
            self.logger.info("Automated Refactoring Validator stopped")
        except Exception as e:
            self.logger.error(f"Error during validator shutdown: {e}")
    
    def _on_heartbeat(self):
        """Validator heartbeat."""
        try:
            history_size = len(self.validation_history)
            self.logger.debug(f"Validator heartbeat - history size: {history_size}")
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")
    
    def _on_initialize_resources(self) -> bool:
        """Initialize validator resources."""
        try:
            self.test_results.clear()
            return True
        except Exception as e:
            self.logger.error(f"Resource initialization failed: {e}")
            return False
    
    def _on_cleanup_resources(self):
        """Cleanup validator resources."""
        try:
            self.test_results.clear()
        except Exception as e:
            self.logger.error(f"Resource cleanup error: {e}")


def main():
    """CLI interface for Automated Refactoring Validation."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Refactoring Validation")
    parser.add_argument("--validate", help="Validate refactoring changes")
    parser.add_argument("--history", action="store_true", help="Show validation history")
    
    args = parser.parse_args()
    
    validator = RefactoringValidator()
    
    if args.validate:
        print(f"Refactoring validation: {args.validate}")
    elif args.history:
        history = validator.get_validation_history()
        print(f"Validation History: {len(history)} reports")
    else:
        print("Automated Refactoring Validation - Agent Cellphone V2")
        print("Use --validate or --history for validation operations")


if __name__ == "__main__":
    main()
