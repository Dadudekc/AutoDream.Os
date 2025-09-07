"""Rule definitions for cleanup validation."""
from __future__ import annotations

from typing import List

from .shared import CleanupRequirement, StandardRequirement


def get_cleanup_requirements() -> List[CleanupRequirement]:
    """Return standard cleanup requirements for all contracts."""
    return [
        CleanupRequirement(
            requirement_id="code_cleanup",
            description="Clean up any temporary code, debug statements, or unused imports",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="documentation_cleanup",
            description="Update or create proper documentation (README, docstrings, comments)",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="test_cleanup",
            description="Ensure tests pass and remove any test-specific temporary code",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="file_organization",
            description="Organize files in proper directories and remove any temporary files",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="git_cleanup",
            description="Commit all changes with proper commit messages and push to remote",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="devlog_entry",
            description="Create comprehensive devlog entry documenting all work completed",
            required=True,
            evidence_files=[],
        ),
        CleanupRequirement(
            requirement_id="discord_update",
            description="Post Discord devlog update summarizing completed work",
            required=True,
            evidence_files=[],
        ),
    ]


def get_v2_standards_requirements() -> List[StandardRequirement]:
    """Return V2 architecture standards requirements."""
    return [
        StandardRequirement(
            standard_id="srp_compliance",
            description="Single Responsibility Principle - Each class/module has one clear purpose",
            required=True,
            compliance_score=0.0,
        ),
        StandardRequirement(
            standard_id="loc_compliance",
            description="Line count compliance - No file exceeds 200 LOC",
            required=True,
            compliance_score=0.0,
        ),
        StandardRequirement(
            standard_id="oop_patterns",
            description="Proper OOP patterns and inheritance structure",
            required=True,
            compliance_score=0.0,
        ),
        StandardRequirement(
            standard_id="no_duplication",
            description="No duplicate functionality - use existing unified systems",
            required=True,
            compliance_score=0.0,
        ),
        StandardRequirement(
            standard_id="error_handling",
            description="Comprehensive error handling and logging",
            required=True,
            compliance_score=0.0,
        ),
        StandardRequirement(
            standard_id="integration_compliance",
            description="Proper integration with existing systems",
            required=True,
            compliance_score=0.0,
        ),
    ]


__all__ = ["get_cleanup_requirements", "get_v2_standards_requirements"]
