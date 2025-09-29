"""
Repository Management Interface for Team Beta Mission
Agent-7 Web Development Expert - User-Friendly Interfaces

V2 Compliance: ≤400 lines, type hints, KISS principle
"""

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any


class RepositoryStatus(Enum):
    """Repository status enumeration."""

    READY = "ready"
    CLONING = "cloning"
    CLONED = "cloned"
    ERROR = "error"
    UPDATING = "updating"


class ErrorType(Enum):
    """Error type enumeration for repository operations."""

    CLONE_FAILED = "clone_failed"
    DEPENDENCY_MISSING = "dependency_missing"
    PERMISSION_DENIED = "permission_denied"
    NETWORK_ERROR = "network_error"
    CONFIG_ERROR = "config_error"


@dataclass
class Repository:
    """Repository data structure."""

    name: str
    url: str
    local_path: str
    status: RepositoryStatus
    dependencies: list[str]
    errors: list[str]
    progress: float
    last_updated: str


@dataclass
class CloneOperation:
    """Clone operation tracking."""

    repository: Repository
    start_time: str
    estimated_duration: int
    progress: float
    current_step: str
    error_count: int


@dataclass
class ErrorResolution:
    """Error resolution data structure."""

    error_type: ErrorType
    description: str
    suggested_fix: str
    automated_fix_available: bool
    priority: int


class RepositoryManagerInterface:
    """
    Repository management interface for Team Beta mission.

    Provides user-friendly and agent-friendly repository cloning,
    error resolution, and management tools.
    """

    def __init__(self, base_path: str = "./repositories"):
        """Initialize repository manager interface."""
        self.base_path = Path(base_path)
        self.repositories: list[Repository] = []
        self.active_operations: list[CloneOperation] = []
        self.error_resolutions: list[ErrorResolution] = []
        self._initialize_error_resolutions()

    def _initialize_error_resolutions(self):
        """Initialize common error resolution strategies."""
        self.error_resolutions = [
            ErrorResolution(
                error_type=ErrorType.CLONE_FAILED,
                description="Repository cloning failed",
                suggested_fix="Check repository URL and network connection",
                automated_fix_available=True,
                priority=1,
            ),
            ErrorResolution(
                error_type=ErrorType.DEPENDENCY_MISSING,
                description="Required dependencies not found",
                suggested_fix="Install missing dependencies using package manager",
                automated_fix_available=True,
                priority=2,
            ),
            ErrorResolution(
                error_type=ErrorType.PERMISSION_DENIED,
                description="Permission denied for repository access",
                suggested_fix="Check SSH keys or authentication credentials",
                automated_fix_available=False,
                priority=1,
            ),
            ErrorResolution(
                error_type=ErrorType.NETWORK_ERROR,
                description="Network connection error during clone",
                suggested_fix="Retry operation or check network connectivity",
                automated_fix_available=True,
                priority=3,
            ),
            ErrorResolution(
                error_type=ErrorType.CONFIG_ERROR,
                description="Configuration error in repository",
                suggested_fix="Review and fix configuration files",
                automated_fix_available=False,
                priority=2,
            ),
        ]

    def add_repository(self, name: str, url: str, dependencies: list[str] = None) -> Repository:
        """Add repository to management list."""
        if dependencies is None:
            dependencies = []

        local_path = str(self.base_path / name)
        repository = Repository(
            name=name,
            url=url,
            local_path=local_path,
            status=RepositoryStatus.READY,
            dependencies=dependencies,
            errors=[],
            progress=0.0,
            last_updated="",
        )

        self.repositories.append(repository)
        return repository

    def get_repository_by_name(self, name: str) -> Repository | None:
        """Get repository by name."""
        for repo in self.repositories:
            if repo.name == name:
                return repo
        return None

    def get_repositories_by_status(self, status: RepositoryStatus) -> list[Repository]:
        """Get repositories by status."""
        return [repo for repo in self.repositories if repo.status == status]

    def get_repositories_with_errors(self) -> list[Repository]:
        """Get repositories that have errors."""
        return [repo for repo in self.repositories if repo.errors]

    def start_clone_operation(self, repository: Repository) -> CloneOperation:
        """Start repository cloning operation."""
        operation = CloneOperation(
            repository=repository,
            start_time="",
            estimated_duration=300,  # 5 minutes default
            progress=0.0,
            current_step="Initializing clone operation",
            error_count=0,
        )

        self.active_operations.append(operation)
        repository.status = RepositoryStatus.CLONING

        return operation

    def update_clone_progress(self, operation: CloneOperation, progress: float, step: str):
        """Update clone operation progress."""
        operation.progress = progress
        operation.current_step = step
        operation.repository.progress = progress

        if progress >= 100.0:
            operation.repository.status = RepositoryStatus.CLONED
            operation.repository.last_updated = "now"
            self.active_operations.remove(operation)

    def add_error_to_repository(self, repository: Repository, error: str):
        """Add error to repository."""
        repository.errors.append(error)
        repository.status = RepositoryStatus.ERROR

    def get_error_resolution(self, error_type: ErrorType) -> ErrorResolution | None:
        """Get error resolution strategy by type."""
        for resolution in self.error_resolutions:
            if resolution.error_type == error_type:
                return resolution
        return None

    def get_high_priority_errors(self) -> list[tuple[Repository, ErrorResolution]]:
        """Get high priority errors requiring immediate attention."""
        high_priority = []
        for repo in self.get_repositories_with_errors():
            for error in repo.errors:
                # Simple error type detection
                if "clone" in error.lower() and "failed" in error.lower():
                    resolution = self.get_error_resolution(ErrorType.CLONE_FAILED)
                    if resolution and resolution.priority == 1:
                        high_priority.append((repo, resolution))
        return high_priority

    def create_repository_dashboard_data(self) -> dict[str, Any]:
        """Create dashboard data for repository management interface."""
        return {
            "total_repositories": len(self.repositories),
            "repositories_by_status": {
                status.value: len(self.get_repositories_by_status(status))
                for status in RepositoryStatus
            },
            "repositories_with_errors": len(self.get_repositories_with_errors()),
            "active_operations": len(self.active_operations),
            "high_priority_errors": len(self.get_high_priority_errors()),
            "repositories": [
                {
                    "name": repo.name,
                    "url": repo.url,
                    "status": repo.status.value,
                    "progress": repo.progress,
                    "error_count": len(repo.errors),
                    "dependencies": repo.dependencies,
                }
                for repo in self.repositories
            ],
            "active_clone_operations": [
                {
                    "repository_name": op.repository.name,
                    "progress": op.progress,
                    "current_step": op.current_step,
                    "error_count": op.error_count,
                }
                for op in self.active_operations
            ],
            "error_summary": [
                {
                    "error_type": resolution.error_type.value,
                    "description": resolution.description,
                    "priority": resolution.priority,
                    "automated_fix_available": resolution.automated_fix_available,
                }
                for resolution in self.error_resolutions
            ],
        }

    def export_dashboard_data(self, filepath: str) -> bool:
        """Export dashboard data to JSON file."""
        try:
            data = self.create_repository_dashboard_data()
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting dashboard data: {e}")
            return False

    def validate_repository_setup(self, repository: Repository) -> tuple[bool, list[str]]:
        """Validate repository setup and configuration."""
        errors = []

        # Check if repository URL is valid
        if not repository.url or not repository.url.startswith(("http", "git")):
            errors.append("Invalid repository URL")

        # Check if local path is writable
        try:
            Path(repository.local_path).parent.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            errors.append("Permission denied for local path")

        # Check dependencies
        for dep in repository.dependencies:
            if not dep or len(dep.strip()) == 0:
                errors.append(f"Invalid dependency: {dep}")

        return len(errors) == 0, errors


def create_sample_repository_manager() -> RepositoryManagerInterface:
    """Create sample repository manager with test data."""
    manager = RepositoryManagerInterface()

    # Add sample repositories
    manager.add_repository(
        "vscode-fork", "https://github.com/microsoft/vscode.git", ["nodejs", "npm", "typescript"]
    )

    manager.add_repository(
        "agent-cellphone-v2",
        "https://github.com/example/agent-cellphone-v2.git",
        ["python", "pip", "pytest"],
    )

    manager.add_repository(
        "dream-os", "https://github.com/example/dream-os.git", ["python", "docker", "kubernetes"]
    )

    return manager


if __name__ == "__main__":
    # Example usage
    manager = create_sample_repository_manager()

    # Create dashboard data
    dashboard_data = manager.create_repository_dashboard_data()
    print(
        f"✅ Repository dashboard data created: {dashboard_data['total_repositories']} repositories"
    )

    # Export dashboard data
    success = manager.export_dashboard_data("repository_dashboard.json")
    if success:
        print("✅ Repository dashboard data exported successfully")
    else:
        print("❌ Failed to export dashboard data")

    # Validate repository setup
    for repo in manager.repositories:
        is_valid, errors = manager.validate_repository_setup(repo)
        if is_valid:
            print(f"✅ Repository '{repo.name}' setup is valid")
        else:
            print(f"❌ Repository '{repo.name}' has errors: {errors}")
