"""
Refactoring Consolidation Tools - V2 Compliance Module
=====================================================

Consolidation functionality for refactoring tools.

V2 Compliance: < 300 lines, single responsibility, consolidation tools.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from dataclasses import dataclass
from typing import Any

from ...unified_import_system import get_unified_import_system


@dataclass
class ConsolidationPlan:
    """Plan for consolidating duplicate code."""

    duplicate_groups: list[list[str]]
    consolidation_targets: list[str]
    consolidation_rules: list[str]
    estimated_savings: int


class ConsolidationTools:
    """Consolidation tools for refactoring."""

    def __init__(self):
        """Initialize consolidation tools."""
        self.unified_imports = get_unified_import_system()

    def create_consolidation_plan(self, directory: str) -> ConsolidationPlan:
        """Create a consolidation plan for duplicate code."""
        try:
            duplicates = self._find_duplicate_files(directory)

            duplicate_groups = []
            consolidation_targets = []
            consolidation_rules = []
            estimated_savings = 0

            for group in duplicates:
                if len(group) > 1:
                    duplicate_groups.append(group)
                    consolidation_targets.append(group[0])  # Keep first file
                    consolidation_rules.append(f"Consolidate {len(group)} duplicate files")
                    estimated_savings += len(group) - 1

            return ConsolidationPlan(
                duplicate_groups=duplicate_groups,
                consolidation_targets=consolidation_targets,
                consolidation_rules=consolidation_rules,
                estimated_savings=estimated_savings,
            )
        except Exception:
            return ConsolidationPlan(
                duplicate_groups=[],
                consolidation_targets=[],
                consolidation_rules=[],
                estimated_savings=0,
            )

    def execute_consolidation(self, plan: ConsolidationPlan) -> bool:
        """Execute consolidation plan."""
        try:
            for group in plan.duplicate_groups:
                if len(group) > 1:
                    # Keep first file, remove others
                    for file_path in group[1:]:
                        path = self.unified_imports.Path(file_path)
                        if path.exists():
                            path.unlink()

            return True
        except Exception:
            return False

    def _find_duplicate_files(self, directory: str) -> list[list[str]]:
        """Find duplicate files in directory."""
        try:
            dir_path = self.unified_imports.Path(directory)
            if not dir_path.exists():
                return []

            file_hashes = {}
            duplicates = []

            for file_path in dir_path.rglob("*.py"):
                if file_path.is_file():
                    try:
                        content = file_path.read_text(encoding="utf-8")
                        file_hash = hash(content)

                        if file_hash in file_hashes:
                            file_hashes[file_hash].append(str(file_path))
                        else:
                            file_hashes[file_hash] = [str(file_path)]
                    except Exception:
                        continue

            # Find groups with more than one file
            for file_group in file_hashes.values():
                if len(file_group) > 1:
                    duplicates.append(file_group)

            return duplicates
        except Exception:
            return []

    def analyze_duplicates(self, directory: str) -> dict[str, Any]:
        """Analyze duplicate files in directory."""
        try:
            duplicates = self._find_duplicate_files(directory)

            total_duplicates = sum(len(group) - 1 for group in duplicates)
            total_groups = len(duplicates)

            return {
                "total_duplicate_files": total_duplicates,
                "duplicate_groups": total_groups,
                "potential_savings": total_duplicates,
                "analysis_timestamp": self.unified_imports.datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "error": str(e),
                "total_duplicate_files": 0,
                "duplicate_groups": 0,
                "potential_savings": 0,
            }
