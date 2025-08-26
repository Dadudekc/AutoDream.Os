import logging
import hashlib
import time
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class DiscoveryStatus(Enum):
    """Repository discovery status enumeration."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class RepositoryMetadata:
    """Repository metadata information."""
    repo_id: str
    name: str
    path: str
    size_bytes: int
    file_count: int
    last_modified: float
    technology_stack: List[str]
    architecture_patterns: List[str]
    security_score: float
    performance_metrics: Dict[str, Any]
    discovery_timestamp: float
    analysis_status: str
    metadata: Dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class DiscoveryConfig:
    """Repository discovery configuration."""
    scan_depth: int = 3
    include_hidden: bool = False
    file_extensions: List[str] | None = None
    exclude_patterns: List[str] | None = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    parallel_workers: int = 4
    timeout_seconds: int = 300

    def __post_init__(self) -> None:
        if self.file_extensions is None:
            self.file_extensions = [
                ".py",
                ".js",
                ".java",
                ".cpp",
                ".h",
                ".cs",
                ".go",
                ".rs",
                ".php",
            ]
        if self.exclude_patterns is None:
            self.exclude_patterns = [
                "node_modules",
                ".git",
                "__pycache__",
                ".pytest_cache",
            ]


def _calculate_repository_size(path: Path) -> int:
    """Calculate total size of repository."""
    try:
        total_size = 0
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    except Exception:
        return 0


def _count_files(path: Path, config: DiscoveryConfig) -> int:
    """Count files in repository based on configuration."""
    try:
        count = 0
        for file_path in path.rglob("*"):
            if file_path.is_file():
                if config.file_extensions and file_path.suffix not in config.file_extensions:
                    continue
                if any(pattern in str(file_path) for pattern in config.exclude_patterns):
                    continue
                if file_path.stat().st_size > config.max_file_size:
                    continue
                count += 1
        return count
    except Exception:
        return 0


def discover_repository(
    path: str,
    repositories: Dict[str, RepositoryMetadata],
    discovery_history: List[Dict[str, Any]],
    config: DiscoveryConfig,
) -> Optional[str]:
    """Discover and register a new repository."""
    try:
        repo_path = Path(path)
        if not repo_path.exists():
            logger.error(f"Repository path does not exist: {path}")
            return None

        repo_id = hashlib.md5(f"{path}_{time.time()}".encode()).hexdigest()[:12]

        metadata = RepositoryMetadata(
            repo_id=repo_id,
            name=repo_path.name,
            path=str(repo_path),
            size_bytes=_calculate_repository_size(repo_path),
            file_count=_count_files(repo_path, config),
            last_modified=repo_path.stat().st_mtime,
            technology_stack=[],
            architecture_patterns=[],
            security_score=0.0,
            performance_metrics={},
            discovery_timestamp=time.time(),
            analysis_status="discovered",
        )

        repositories[repo_id] = metadata

        discovery_history.append(
            {
                "timestamp": time.time(),
                "repo_id": repo_id,
                "path": path,
                "duration": 0,
                "status": "discovered",
            }
        )

        logger.info(f"Discovered repository: {repo_id} at {path}")
        return repo_id
    except Exception as e:  # pragma: no cover - defensive programming
        logger.error(f"Failed to discover repository at {path}: {e}")
        return None


def cleanup_old_repositories(
    repositories: Dict[str, RepositoryMetadata], days: int = 7
) -> None:
    """Clean up old repository entries."""
    try:
        current_time = time.time()
        cutoff_time = current_time - (days * 24 * 3600)
        old_repos = [
            repo_id
            for repo_id, repo in repositories.items()
            if repo.discovery_timestamp < cutoff_time
        ]
        for repo_id in old_repos:
            del repositories[repo_id]
        logger.info(f"Cleaned up {len(old_repos)} old repositories")
    except Exception as e:  # pragma: no cover - defensive
        logger.error(f"Failed to cleanup old repositories: {e}")
