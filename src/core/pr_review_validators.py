"""
PR Review Protocol Validators - Validation logic for PR reviews.
"""

from pathlib import Path

from .design_authority import design_authority
from .pr_review_models import PullRequest
from .project_registry import registry_manager
from .vibe_check import VibeCheckReport, vibe_check_strict


class PRValidator:
    """Handles validation logic for PR reviews."""

    def check_duplication(self, pr: PullRequest) -> list[str]:
        """Check for duplication with existing components."""
        violations = []
        registry = registry_manager.load_registry()

        for change in pr.changes:
            if change.change_type == "added":
                file_name = Path(change.file_path).stem

                for existing_component in registry.components.values():
                    if (
                        file_name.lower() in existing_component.path.lower()
                        or existing_component.path.lower() in file_name.lower()
                    ):
                        violations.append(
                            f"Potential duplication: {change.file_path} may duplicate {existing_component.path}"
                        )

        return violations

    def run_vibe_check(self, pr: PullRequest) -> VibeCheckReport:
        """Run vibe check on changed files."""
        changed_files = [
            change.file_path for change in pr.changes if change.change_type in ["added", "modified"]
        ]

        if not changed_files:
            return VibeCheckReport(
                result="pass",
                total_files=0,
                violations=[],
                summary={},
                timestamp="",  # Will be set by vibe_check_strict
                agent_author=pr.author,
            )

        return vibe_check_strict(changed_files, pr.author)

    def check_design_compliance(self, pr: PullRequest) -> list[str]:
        """Check compliance with design principles."""
        violations = []

        for change in pr.changes:
            if change.change_type in ["added", "modified"]:
                review = design_authority.review_component_plan(
                    requester=pr.author,
                    component_name=Path(change.file_path).stem,
                    plan=change.new_content[:200] + "..."
                    if len(change.new_content) > 200
                    else change.new_content,
                    context=f"PR: {pr.title}",
                )

                if not review.approved:
                    violations.append(f"Design authority rejected: {review.feedback}")

        return violations

    def check_error_handling(self, pr: PullRequest) -> list[str]:
        """Check for proper error handling."""
        violations = []

        for change in pr.changes:
            if change.change_type in ["added", "modified"]:
                content = change.new_content.lower()

                if "except:" in content and "except exception:" not in content:
                    violations.append(f"Bare except clause in {change.file_path}")

                if "def " in content and "try:" not in content:
                    violations.append(f"New function in {change.file_path} may need error handling")

        return violations

    def check_documentation(self, pr: PullRequest) -> list[str]:
        """Check if documentation needs updating."""
        violations = []

        for change in pr.changes:
            if change.change_type == "added":
                if "def " in change.new_content and not any(
                    doc in change.new_content for doc in ['"""', "'''", "# TODO"]
                ):
                    violations.append(f"New functions in {change.file_path} should be documented")

        return violations
