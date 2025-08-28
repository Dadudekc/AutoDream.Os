"""Workflow-level validation checks for refactoring validation."""
from pathlib import Path
import time
from typing import Dict, Set, Any, List

from .validation_types import ValidationResult, ValidationStatus, ValidationSeverity


def run_functionality_validation(before_files: Dict[str, str], after_files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Validate core functionality preservation."""
    if not rule.get("enabled"):
        return

    for file_path, after_content in after_files.items():
        if not file_path.endswith('.py'):
            continue

        start_time = time.time()
        before_content = before_files.get(file_path, "")
        if before_content:
            before_functions = _extract_functions(before_content)
            after_functions = _extract_functions(after_content)
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

        test_results.append(result)


def _extract_functions(content: str) -> Set[str]:
    """Extract function names from content."""
    functions: Set[str] = set()
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith('def '):
            func_name = line[4:].split('(')[0].strip()
            functions.add(func_name)
    return functions


def run_performance_validation(before_files: Dict[str, str], after_files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Validate performance characteristics."""
    if not rule.get("enabled"):
        return

    for file_path, after_content in after_files.items():
        if not file_path.endswith('.py'):
            continue

        start_time = time.time()
        lines = len(after_content.splitlines())
        complexity = _calculate_complexity(after_content)

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

        test_results.append(result)


def _calculate_complexity(content: str) -> int:
    """Calculate simple complexity metric."""
    complexity = 0
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith(('if ', 'for ', 'while ', 'try:', 'except:', 'finally:', 'with ')):
            complexity += 1
    return complexity
