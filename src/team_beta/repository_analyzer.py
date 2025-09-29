"""
Repository Analyzer for Team Beta Mission
Agent-7 Repository Cloning Specialist - Clone Automation & Error Resolution

V2 Compliance: ≤400 lines, type hints, KISS principle
"""

import json
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class RepositoryType(Enum):
    """Repository type classification."""

    MAIN_PROJECT = "main_project"
    VSCODE_FORK = "vscode_fork"
    DEPENDENCY = "dependency"
    DOCUMENTATION = "documentation"
    TESTING = "testing"


class CloneStatus(Enum):
    """Repository clone status."""

    NOT_CLONED = "not_cloned"
    CLONING = "cloning"
    CLONED = "cloned"
    ERROR = "error"
    UPDATED = "updated"


@dataclass
class RepositoryInfo:
    """Repository information structure."""

    name: str
    url: str
    type: RepositoryType
    local_path: str
    status: CloneStatus
    dependencies: list[str]
    errors: list[str]
    size_mb: float
    last_commit: str
    branch: str


@dataclass
class CloneResult:
    """Clone operation result."""

    repository: RepositoryInfo
    success: bool
    duration_seconds: float
    errors: list[str]
    warnings: list[str]
    files_cloned: int


class RepositoryAnalyzer:
    """
    Repository analyzer for Team Beta mission.

    Analyzes repositories for cloning, dependency management,
    and error resolution automation.
    """

    def __init__(self, base_path: str = "./repositories"):
        """Initialize repository analyzer."""
        self.base_path = Path(base_path)
        self.repositories: list[RepositoryInfo] = []
        self.clone_results: list[CloneResult] = []
        self._initialize_target_repositories()

    def _initialize_target_repositories(self):
        """Initialize target repositories for Team Beta mission."""
        self.repositories = [
            RepositoryInfo(
                name="vscode",
                url="https://github.com/microsoft/vscode.git",
                type=RepositoryType.VSCODE_FORK,
                local_path=str(self.base_path / "vscode"),
                status=CloneStatus.NOT_CLONED,
                dependencies=["nodejs", "npm", "typescript"],
                errors=[],
                size_mb=0.0,
                last_commit="",
                branch="main",
            ),
            RepositoryInfo(
                name="autodream-os",
                url="https://github.com/Dadudekc/AutoDream.Os.git",
                type=RepositoryType.MAIN_PROJECT,
                local_path=str(self.base_path / "autodream-os"),
                status=CloneStatus.NOT_CLONED,
                dependencies=["python", "pip", "pytest"],
                errors=[],
                size_mb=0.0,
                last_commit="",
                branch="main",
            ),
            RepositoryInfo(
                name="agent-cellphone-v2",
                url="https://github.com/Dadudekc/Agent_Cellphone_V2_Repository.git",
                type=RepositoryType.MAIN_PROJECT,
                local_path=str(self.base_path / "agent-cellphone-v2"),
                status=CloneStatus.NOT_CLONED,
                dependencies=["python", "pip", "pytest"],
                errors=[],
                size_mb=0.0,
                last_commit="",
                branch="main",
            ),
            RepositoryInfo(
                name="team-beta-docs",
                url="https://github.com/example/team-beta-docs.git",
                type=RepositoryType.DOCUMENTATION,
                local_path=str(self.base_path / "team-beta-docs"),
                status=CloneStatus.NOT_CLONED,
                dependencies=[],
                errors=[],
                size_mb=0.0,
                last_commit="",
                branch="main",
            ),
            RepositoryInfo(
                name="vscode-extensions",
                url="https://github.com/microsoft/vscode-extensions.git",
                type=RepositoryType.DEPENDENCY,
                local_path=str(self.base_path / "vscode-extensions"),
                status=CloneStatus.NOT_CLONED,
                dependencies=["nodejs", "npm"],
                errors=[],
                size_mb=0.0,
                last_commit="",
                branch="main",
            ),
        ]

    def analyze_repository_dependencies(self, repo: RepositoryInfo) -> dict[str, Any]:
        """Analyze repository dependencies and requirements."""
        analysis = {
            "repository": repo.name,
            "dependencies": repo.dependencies,
            "dependency_status": {},
            "missing_dependencies": [],
            "version_requirements": {},
            "installation_commands": [],
        }

        # Check each dependency
        for dep in repo.dependencies:
            if dep == "nodejs":
                analysis["dependency_status"][dep] = self._check_nodejs()
                if not analysis["dependency_status"][dep]:
                    analysis["missing_dependencies"].append(dep)
                    analysis["installation_commands"].append(
                        "Install Node.js from https://nodejs.org/"
                    )

            elif dep == "python":
                analysis["dependency_status"][dep] = self._check_python()
                if not analysis["dependency_status"][dep]:
                    analysis["missing_dependencies"].append(dep)
                    analysis["installation_commands"].append(
                        "Install Python from https://python.org/"
                    )

            elif dep == "npm":
                analysis["dependency_status"][dep] = self._check_npm()
                if not analysis["dependency_status"][dep]:
                    analysis["missing_dependencies"].append(dep)
                    analysis["installation_commands"].append("npm install -g npm@latest")

            elif dep == "pip":
                analysis["dependency_status"][dep] = self._check_pip()
                if not analysis["dependency_status"][dep]:
                    analysis["missing_dependencies"].append(dep)
                    analysis["installation_commands"].append("python -m ensurepip --upgrade")

        return analysis

    def _check_nodejs(self) -> bool:
        """Check if Node.js is installed."""
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _check_python(self) -> bool:
        """Check if Python is installed."""
        try:
            result = subprocess.run(["python", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _check_npm(self) -> bool:
        """Check if npm is installed."""
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def _check_pip(self) -> bool:
        """Check if pip is installed."""
        try:
            result = subprocess.run(["pip", "--version"], capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def clone_repository(self, repo: RepositoryInfo) -> CloneResult:
        """Clone repository with error handling and progress tracking."""
        start_time = time.time()
        errors = []
        warnings = []
        files_cloned = 0

        try:
            # Update status
            repo.status = CloneStatus.CLONING

            # Ensure base path exists
            self.base_path.mkdir(parents=True, exist_ok=True)

            # Clone repository
            clone_cmd = ["git", "clone", repo.url, repo.local_path]
            result = subprocess.run(clone_cmd, capture_output=True, text=True)

            if result.returncode == 0:
                repo.status = CloneStatus.CLONED
                files_cloned = self._count_cloned_files(repo.local_path)
                warnings.append("Repository cloned successfully")
            else:
                repo.status = CloneStatus.ERROR
                errors.append(f"Clone failed: {result.stderr}")

        except Exception as e:
            repo.status = CloneStatus.ERROR
            errors.append(f"Clone exception: {str(e)}")

        duration = time.time() - start_time

        clone_result = CloneResult(
            repository=repo,
            success=repo.status == CloneStatus.CLONED,
            duration_seconds=duration,
            errors=errors,
            warnings=warnings,
            files_cloned=files_cloned,
        )

        self.clone_results.append(clone_result)
        return clone_result

    def _count_cloned_files(self, path: str) -> int:
        """Count files in cloned repository."""
        try:
            return sum(1 for _ in Path(path).rglob("*") if _.is_file())
        except Exception:
            return 0

    def get_repositories_by_type(self, repo_type: RepositoryType) -> list[RepositoryInfo]:
        """Get repositories by type."""
        return [repo for repo in self.repositories if repo.type == repo_type]

    def get_repositories_by_status(self, status: CloneStatus) -> list[RepositoryInfo]:
        """Get repositories by clone status."""
        return [repo for repo in self.repositories if repo.status == status]

    def get_failed_clones(self) -> list[CloneResult]:
        """Get failed clone operations."""
        return [result for result in self.clone_results if not result.success]

    def create_analysis_report(self) -> dict[str, Any]:
        """Create comprehensive repository analysis report."""
        return {
            "analysis_timestamp": "2025-01-18T19:00:00Z",
            "total_repositories": len(self.repositories),
            "repositories_by_type": {
                repo_type.value: len(self.get_repositories_by_type(repo_type))
                for repo_type in RepositoryType
            },
            "repositories_by_status": {
                status.value: len(self.get_repositories_by_status(status)) for status in CloneStatus
            },
            "clone_results": {
                "total_attempts": len(self.clone_results),
                "successful": len([r for r in self.clone_results if r.success]),
                "failed": len(self.get_failed_clones()),
                "average_duration": sum(r.duration_seconds for r in self.clone_results)
                / max(len(self.clone_results), 1),
            },
            "dependency_analysis": {
                repo.name: self.analyze_repository_dependencies(repo) for repo in self.repositories
            },
            "recommendations": self._generate_recommendations(),
        }

    def _generate_recommendations(self) -> list[str]:
        """Generate recommendations for repository cloning."""
        recommendations = []

        # Check for failed clones
        failed_clones = self.get_failed_clones()
        if failed_clones:
            recommendations.append(f"Address {len(failed_clones)} failed clone operations")

        # Check for missing dependencies
        for repo in self.repositories:
            analysis = self.analyze_repository_dependencies(repo)
            if analysis["missing_dependencies"]:
                recommendations.append(
                    f"Install missing dependencies for {repo.name}: {', '.join(analysis['missing_dependencies'])}"
                )

        # Check for VSCode fork priority
        vscode_repos = self.get_repositories_by_type(RepositoryType.VSCODE_FORK)
        if vscode_repos:
            recommendations.append("Prioritize VSCode fork cloning for Team Beta mission")

        return recommendations


def create_repository_analyzer() -> RepositoryAnalyzer:
    """Create repository analyzer instance."""
    return RepositoryAnalyzer()


if __name__ == "__main__":
    import time

    # Example usage
    analyzer = create_repository_analyzer()

    # Create analysis report
    report = analyzer.create_analysis_report()
    print(f"✅ Repository analysis complete: {report['total_repositories']} repositories analyzed")

    # Export analysis report
    with open("repository_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print("✅ Analysis report exported to repository_analysis_report.json")

    # Show recommendations
    if report["recommendations"]:
        print("📋 Recommendations:")
        for rec in report["recommendations"]:
            print(f"  - {rec}")
