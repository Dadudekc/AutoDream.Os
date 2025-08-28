"""Validation routines for contract cleanup."""
from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

from .shared import (
    CleanupRequirement,
    CleanupValidation,
    StandardRequirement,
    DEBUG_PATTERNS,
)
from . import rules


def check_code_cleanup(contract_id: str) -> Tuple[bool, List[str]]:
    """Check if code cleanup requirements are met."""
    issues: List[str] = []
    temp_files = list(Path(".").glob("*.tmp")) + list(Path(".").glob("*temp*"))
    if temp_files:
        issues.append(f"Temporary files found: {[f.name for f in temp_files]}")
    for py_file in Path("src").rglob("*.py"):
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for pattern in DEBUG_PATTERNS:
            if pattern in content:
                issues.append(f"{pattern} found in {py_file}")
                break
    return len(issues) == 0, issues


def check_documentation_cleanup(contract_id: str) -> Tuple[bool, List[str]]:
    """Check if documentation cleanup requirements are met."""
    issues: List[str] = []
    devlog_files = list(Path("logs").glob(f"*{contract_id}*"))
    if not devlog_files:
        issues.append("Devlog entry not found")
    readme_files = list(Path(".").glob("README*"))
    if not readme_files:
        issues.append("No README files found")
    return len(issues) == 0, issues


def check_git_cleanup(contract_id: str) -> Tuple[bool, List[str]]:
    """Check if git cleanup requirements are met."""
    issues: List[str] = []
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout.strip():
            issues.append("Uncommitted changes found")
    except Exception:
        issues.append("Could not check git status")
    return len(issues) == 0, issues


def check_v2_standards_compliance(contract_id: str) -> Tuple[bool, List[str]]:
    """Check V2 standards compliance."""
    issues: List[str] = []
    large_files: List[str] = []
    for py_file in Path("src").rglob("*.py"):
        try:
            lines = py_file.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        if len(lines) > 200:
            large_files.append(f"{py_file}: {len(lines)} lines")
    if large_files:
        issues.append(f"Files exceeding 200 LOC: {large_files[:5]}")
    return len(issues) == 0, issues


def validate_cleanup_completion(
    contract_id: str,
    cleanup_requirements: List[CleanupRequirement],
    standards_requirements: List[StandardRequirement],
) -> CleanupValidation:
    """Validate that all cleanup requirements are met."""
    missing_cleanup: List[str] = []
    validation_errors: List[str] = []
    warnings: List[str] = []

    cleanup_completed = sum(req.completed for req in cleanup_requirements)
    total_cleanup = len(cleanup_requirements)
    for req in cleanup_requirements:
        if not req.completed:
            missing_cleanup.append(req.description)

    cleanup_score = cleanup_completed / total_cleanup if total_cleanup > 0 else 0.0

    standards_compliant = sum(std.compliant for std in standards_requirements)
    total_standards = len(standards_requirements)
    standards_score = (
        standards_compliant / total_standards if total_standards > 0 else 0.0
    )

    overall_score = (cleanup_score * 0.6) + (standards_score * 0.4)
    is_valid = overall_score >= 0.9 and cleanup_score >= 0.85 and standards_score >= 0.8

    return CleanupValidation(
        is_valid=is_valid,
        missing_cleanup=missing_cleanup,
        validation_errors=validation_errors,
        warnings=warnings,
        cleanup_score=cleanup_score,
        standards_score=standards_score,
        overall_score=overall_score,
        timestamp=datetime.now().isoformat(),
    )


def auto_validate_contract(contract_id: str) -> CleanupValidation:
    """Automatically validate contract cleanup and standards."""
    cleanup_requirements = rules.get_cleanup_requirements()
    standards_requirements = rules.get_v2_standards_requirements()

    code_cleanup_ok, code_issues = check_code_cleanup(contract_id)
    doc_cleanup_ok, doc_issues = check_documentation_cleanup(contract_id)
    git_cleanup_ok, git_issues = check_git_cleanup(contract_id)
    standards_ok, standards_issues = check_v2_standards_compliance(contract_id)

    for req in cleanup_requirements:
        if req.requirement_id == "code_cleanup":
            req.completed = code_cleanup_ok
            if not code_cleanup_ok:
                req.validation_notes = f"Issues found: {', '.join(code_issues)}"
        elif req.requirement_id == "documentation_cleanup":
            req.completed = doc_cleanup_ok
            if not doc_cleanup_ok:
                req.validation_notes = f"Issues found: {', '.join(doc_issues)}"
        elif req.requirement_id == "git_cleanup":
            req.completed = git_cleanup_ok
            if not git_cleanup_ok:
                req.validation_notes = f"Issues found: {', '.join(git_issues)}"

    for std in standards_requirements:
        if std.standard_id == "loc_compliance":
            std.compliant = standards_ok
            if not standards_ok:
                std.validation_notes = f"Issues found: {', '.join(standards_issues)}"

    return validate_cleanup_completion(
        contract_id, cleanup_requirements, standards_requirements
    )


__all__ = [
    "check_code_cleanup",
    "check_documentation_cleanup",
    "check_git_cleanup",
    "check_v2_standards_compliance",
    "validate_cleanup_completion",
    "auto_validate_contract",
]
