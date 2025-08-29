"""Data-level validation checks for refactoring validation."""
from pathlib import Path
import time
from typing import Dict, Set, Any, List

from .validation_types import ValidationResult, ValidationStatus, ValidationSeverity


def run_syntax_validation(files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Run Python syntax validation on refactored files."""
    if not rule.get("enabled"):
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

        test_results.append(result)


def run_import_validation(before_files: Dict[str, str], after_files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Validate import statements and dependencies."""
    if not rule.get("enabled"):
        return

    for file_path, after_content in after_files.items():
        if not file_path.endswith('.py'):
            continue

        start_time = time.time()
        after_imports = _extract_imports(after_content)

        if file_path in before_files:
            before_imports = _extract_imports(before_files[file_path])
            removed_imports = before_imports - after_imports
            added_imports = after_imports - before_imports

            if removed_imports and not _validate_import_removal(removed_imports, after_content):
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
            result = ValidationResult(
                test_name=f"import_validation_{Path(file_path).stem}",
                status=ValidationStatus.PASSED,
                severity=rule["severity"],
                message=f"Import validation passed for new file {file_path}",
                details={"imports": list(after_imports)},
                execution_time=time.time() - start_time,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )

        test_results.append(result)


def _extract_imports(content: str) -> Set[str]:
    """Extract import statements from content."""
    imports: Set[str] = set()
    lines = content.splitlines()

    for line in lines:
        line = line.strip()
        if line.startswith('import ') or line.startswith('from '):
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


def _validate_import_removal(removed_imports: Set[str], content: str) -> bool:
    """Validate that removed imports are not still used in content."""
    for import_name in removed_imports:
        if import_name in content:
            return False
    return True


def run_style_validation(files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Validate code style and formatting."""
    if not rule.get("enabled"):
        return

    for file_path, content in files.items():
        if not file_path.endswith('.py'):
            continue

        start_time = time.time()
        style_issues: List[str] = []
        lines = content.splitlines()

        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                style_issues.append(f"Line {i}: Exceeds 120 characters")
            if line.strip() and not line.startswith('#') and '  ' in line:
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

        test_results.append(result)


def run_documentation_validation(files: Dict[str, str], rule: Dict[str, Any], test_results: List[ValidationResult]) -> None:
    """Validate documentation completeness."""
    if not rule.get("enabled"):
        return

    for file_path, content in files.items():
        if not file_path.endswith('.py'):
            continue

        start_time = time.time()
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

        test_results.append(result)
