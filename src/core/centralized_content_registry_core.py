#!/usr/bin/env python3
"""
Centralized Content Registry Core
===============================
Core logic for centralized content management system
V2 Compliant: ≤400 lines, focused content management logic
"""

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any


class ContentType(Enum):
    """Content type enumeration"""

    CODE = "code"
    DOCUMENTATION = "documentation"
    CONFIGURATION = "configuration"
    TEST = "test"
    SCRIPT = "script"
    TEMPLATE = "template"
    DATA = "data"
    LOG = "log"


class ContentStatus(Enum):
    """Content status enumeration"""

    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"
    PENDING_REVIEW = "pending_review"


@dataclass
class ContentMetadata:
    """Content metadata structure"""

    file_path: str
    content_type: ContentType
    agent_id: str
    created_at: str
    last_modified: str
    last_accessed: str
    file_size: int
    content_hash: str
    description: str
    tags: list[str]
    dependencies: list[str]
    status: ContentStatus
    access_count: int = 0
    quality_score: float = 0.0
    v2_compliant: bool = False

    def __post_init__(self):
        if isinstance(self.content_type, str):
            self.content_type = ContentType(self.content_type)
        if isinstance(self.status, str):
            self.status = ContentStatus(self.status)


class CentralizedContentRegistryCore:
    """Core logic for centralized content management system"""

    def __init__(
        self, registry_file: str = "content_registry.json", archive_dir: str = "content_archive"
    ):
        self.registry_file = Path(registry_file)
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)

        self.content_registry: dict[str, ContentMetadata] = {}
        self.agent_stats: dict[str, dict[str, Any]] = {}

        # Anti-slop settings
        self.max_files_per_agent_per_day = 10
        self.auto_archive_threshold_days = 30
        self.auto_delete_threshold_days = 90
        self.quality_threshold = 0.7

        self.load_registry()

    def manage_registry_operations(self, action: str, **kwargs) -> Any:
        """Consolidated registry operations"""
        if action == "load":
            self.load_registry()
            return True
        elif action == "save":
            self.save_registry()
            return True
        elif action == "register":
            return self.register_content(
                kwargs["file_path"],
                kwargs["content_type"],
                kwargs["agent_id"],
                kwargs.get("description", ""),
                kwargs.get("tags"),
                kwargs.get("dependencies"),
            )
        elif action == "get_by_agent":
            return self.get_content_by_agent(kwargs["agent_id"])
        elif action == "get_by_type":
            return self.get_content_by_type(kwargs["content_type"])
        elif action == "search":
            return self.search_content(kwargs["query"], kwargs.get("tags"))
        elif action == "archive":
            return self.archive_content(kwargs["file_path"])
        elif action == "delete":
            return self.delete_content(kwargs["file_path"], kwargs.get("permanent", False))
        elif action == "cleanup":
            return self.cleanup_old_content(kwargs.get("days_threshold"))
        elif action == "statistics":
            return self.get_registry_statistics()
        return None

    def load_registry(self) -> None:
        """Load content registry from disk"""
        if self.registry_file.exists():
            try:
                with open(self.registry_file) as f:
                    data = json.load(f)

                # Load content registry
                for file_path, metadata in data.get("content", {}).items():
                    self.content_registry[file_path] = ContentMetadata(**metadata)

                # Load agent statistics
                self.agent_stats = data.get("agent_stats", {})

            except Exception as e:
                print(f"Warning: Failed to load content registry: {e}")

    def save_registry(self) -> None:
        """Save content registry to disk"""
        try:
            data = {
                "content": {k: asdict(v) for k, v in self.content_registry.items()},
                "agent_stats": self.agent_stats,
                "last_updated": datetime.now().isoformat(),
            }

            with open(self.registry_file, "w") as f:
                json.dump(data, f, indent=2)

        except Exception as e:
            print(f"Error saving content registry: {e}")

    def register_content(
        self,
        file_path: str,
        content_type: ContentType,
        agent_id: str,
        description: str = "",
        tags: list[str] = None,
        dependencies: list[str] = None,
    ) -> bool:
        """Register new content in the centralized registry"""
        file_path_obj = Path(file_path)

        if not file_path_obj.exists():
            print(f"Warning: File {file_path} does not exist")
            return False

        # Check agent file creation limits
        if not self.check_agent_limits(agent_id):
            print(f"Warning: Agent {agent_id} has exceeded file creation limits")
            return False

        # Calculate content metadata
        stat = file_path_obj.stat()
        content_hash = self.calculate_file_hash(file_path)
        quality_score = self.calculate_quality_score(file_path, content_type)
        v2_compliant = self.check_v2_compliance(file_path)

        now = datetime.now().isoformat()

        metadata = ContentMetadata(
            file_path=file_path,
            content_type=content_type,
            agent_id=agent_id,
            created_at=now,
            last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
            last_accessed=now,
            file_size=stat.st_size,
            content_hash=content_hash,
            description=description,
            tags=tags or [],
            dependencies=dependencies or [],
            status=ContentStatus.ACTIVE,
            quality_score=quality_score,
            v2_compliant=v2_compliant,
        )

        self.content_registry[file_path] = metadata
        self.update_agent_stats(agent_id, "file_created", 1)

        self.save_registry()
        return True

    def calculate_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file content"""
        try:
            with open(file_path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return ""

    def calculate_quality_score(self, file_path: str, content_type: ContentType) -> float:
        """Calculate quality score for content"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            score = 0.0

            # File size score (not too small, not too large)
            file_size = len(content)
            if 100 <= file_size <= 10000:
                score += 0.3
            elif file_size < 100:
                score += 0.1

            # Content complexity score
            lines = content.split("\n")
            non_empty_lines = [line for line in lines if line.strip()]

            if len(non_empty_lines) > 10:
                score += 0.3

            # Code quality indicators
            if content_type == ContentType.CODE:
                if "def " in content or "class " in content:
                    score += 0.2
                if '"""' in content or "'''" in content:  # Has docstrings
                    score += 0.2

            # Documentation quality
            elif content_type == ContentType.DOCUMENTATION:
                if content.count("#") > 3:  # Has structure
                    score += 0.2
                if len(content) > 500:  # Substantial content
                    score += 0.2

            return min(score, 1.0)

        except Exception as e:
            print(f"Error calculating quality score for {file_path}: {e}")
            return 0.0

    def check_v2_compliance(self, file_path: str) -> bool:
        """Check if file is V2 compliant"""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            lines = content.split("\n")

            # Check line count (≤400 lines)
            if len(lines) > 400:
                return False

            # Check for Python-specific V2 compliance
            if file_path.endswith(".py"):
                # Count classes and functions
                class_count = content.count("class ")
                def_count = content.count("def ")

                if class_count > 5 or def_count > 10:
                    return False

            return True

        except Exception as e:
            print(f"Error checking V2 compliance for {file_path}: {e}")
            return False

    def check_agent_limits(self, agent_id: str) -> bool:
        """Check if agent has exceeded file creation limits"""
        today = datetime.now().date()
        today_str = today.isoformat()

        # Count files created today by this agent
        today_files = [
            metadata
            for metadata in self.content_registry.values()
            if metadata.agent_id == agent_id and metadata.created_at.startswith(today_str)
        ]

        return len(today_files) < self.max_files_per_agent_per_day

    def update_agent_stats(self, agent_id: str, action: str, value: Any) -> None:
        """Update agent statistics"""
        if agent_id not in self.agent_stats:
            self.agent_stats[agent_id] = {
                "files_created": 0,
                "files_modified": 0,
                "files_deleted": 0,
                "total_size": 0,
                "quality_score": 0.0,
                "last_activity": datetime.now().isoformat(),
            }

        stats = self.agent_stats[agent_id]

        if action == "file_created":
            stats["files_created"] += value
        elif action == "file_modified":
            stats["files_modified"] += value
        elif action == "file_deleted":
            stats["files_deleted"] += value

        stats["last_activity"] = datetime.now().isoformat()

    def get_content_by_agent(self, agent_id: str) -> list[ContentMetadata]:
        """Get all content created by specific agent"""
        return [
            metadata for metadata in self.content_registry.values() if metadata.agent_id == agent_id
        ]

    def get_content_by_type(self, content_type: ContentType) -> list[ContentMetadata]:
        """Get all content of specific type"""
        return [
            metadata
            for metadata in self.content_registry.values()
            if metadata.content_type == content_type
        ]

    def search_content(self, query: str, tags: list[str] = None) -> list[ContentMetadata]:
        """Search content by query and tags"""
        results = []
        query_lower = query.lower()

        for metadata in self.content_registry.values():
            # Search in description and file path
            if (
                query_lower in metadata.description.lower()
                or query_lower in metadata.file_path.lower()
            ):
                # Filter by tags if provided
                if tags:
                    if any(tag in metadata.tags for tag in tags):
                        results.append(metadata)
                else:
                    results.append(metadata)

        return results

    def archive_content(self, file_path: str) -> bool:
        """Archive content to archive directory"""
        if file_path not in self.content_registry:
            return False

        metadata = self.content_registry[file_path]

        try:
            # Create archive path
            archive_path = self.archive_dir / Path(file_path).name

            # Copy file to archive
            import shutil

            shutil.copy2(file_path, archive_path)

            # Update metadata
            metadata.status = ContentStatus.ARCHIVED
            metadata.last_accessed = datetime.now().isoformat()

            self.save_registry()
            return True

        except Exception as e:
            print(f"Error archiving {file_path}: {e}")
            return False

    def delete_content(self, file_path: str, permanent: bool = False) -> bool:
        """Delete content from registry and optionally from filesystem"""
        if file_path not in self.content_registry:
            return False

        metadata = self.content_registry[file_path]

        try:
            if permanent:
                # Delete file from filesystem
                Path(file_path).unlink(missing_ok=True)

            # Update metadata
            metadata.status = ContentStatus.DELETED
            metadata.last_accessed = datetime.now().isoformat()

            # Update agent stats
            self.update_agent_stats(metadata.agent_id, "file_deleted", 1)

            self.save_registry()
            return True

        except Exception as e:
            print(f"Error deleting {file_path}: {e}")
            return False

    def cleanup_old_content(self, days_threshold: int = None) -> dict[str, Any]:
        """Clean up old content based on age and quality"""
        if days_threshold is None:
            days_threshold = self.auto_archive_threshold_days

        cutoff_date = datetime.now() - timedelta(days=days_threshold)
        cleanup_report = {"archived": 0, "deleted": 0, "processed_files": []}

        for file_path, metadata in self.content_registry.items():
            if metadata.status != ContentStatus.ACTIVE:
                continue

            last_accessed = datetime.fromisoformat(metadata.last_accessed)

            # Archive old, low-quality content
            if last_accessed < cutoff_date and metadata.quality_score < self.quality_threshold:
                if self.archive_content(file_path):
                    cleanup_report["archived"] += 1
                    cleanup_report["processed_files"].append(file_path)

            # Delete very old content
            elif last_accessed < (cutoff_date - timedelta(days=60)):
                if self.delete_content(file_path, permanent=False):
                    cleanup_report["deleted"] += 1
                    cleanup_report["processed_files"].append(file_path)

        return cleanup_report

    def get_registry_statistics(self) -> dict[str, Any]:
        """Get comprehensive registry statistics"""
        total_files = len(self.content_registry)
        total_size = sum(m.file_size for m in self.content_registry.values())

        # Status breakdown
        status_counts = {}
        for status in ContentStatus:
            status_counts[status.value] = len(
                [m for m in self.content_registry.values() if m.status == status]
            )

        # Type breakdown
        type_counts = {}
        for content_type in ContentType:
            type_counts[content_type.value] = len(
                [m for m in self.content_registry.values() if m.content_type == content_type]
            )

        # Agent breakdown
        agent_counts = {}
        for agent_id in set(m.agent_id for m in self.content_registry.values()):
            agent_counts[agent_id] = len(
                [m for m in self.content_registry.values() if m.agent_id == agent_id]
            )

        return {
            "total_files": total_files,
            "total_size": total_size,
            "status_breakdown": status_counts,
            "type_breakdown": type_counts,
            "agent_breakdown": agent_counts,
            "average_quality_score": sum(m.quality_score for m in self.content_registry.values())
            / total_files
            if total_files > 0
            else 0,
            "v2_compliant_count": len(
                [m for m in self.content_registry.values() if m.v2_compliant]
            ),
            "last_updated": datetime.now().isoformat(),
        }
