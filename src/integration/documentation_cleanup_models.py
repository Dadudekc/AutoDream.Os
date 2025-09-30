#!/usr/bin/env python3
"""
Documentation Cleanup Models - Data models for Aggressive Documentation Cleanup System
================================================================================

Data models extracted from aggressive_documentation_cleanup_system.py for V2 compliance (≤400 lines).

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any


class CleanupStrategy(Enum):
    """Aggressive cleanup strategies"""

    NUCLEAR = "nuclear"  # Delete everything except critical
    AGGRESSIVE = "aggressive"  # Keep only essential + recent
    MODERATE = "moderate"  # Keep essential + important
    CONSERVATIVE = "conservative"  # Keep most files


class FileCategory(Enum):
    """File categories for aggressive cleanup"""

    KEEP_CRITICAL = "keep_critical"  # Must keep
    KEEP_RECENT = "keep_recent"  # Keep if recent
    CONSOLIDATE = "consolidate"  # Consolidate into single file
    DELETE_AGGRESSIVE = "delete_aggressive"  # Delete aggressively
    DELETE_NUCLEAR = "delete_nuclear"  # Delete in nuclear mode


class CleanupStatus(Enum):
    """Cleanup operation status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class CleanupFile:
    """File analysis for aggressive cleanup"""

    path: str
    size: int
    category: FileCategory
    priority_score: int
    content_hash: str
    is_duplicate: bool
    is_empty: bool
    is_old: bool
    is_devlog: bool
    is_duplicate_name: bool
    last_modified: datetime
    content_preview: str
    dependencies: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "size": self.size,
            "category": self.category.value,
            "priority_score": self.priority_score,
            "content_hash": self.content_hash,
            "is_duplicate": self.is_duplicate,
            "is_empty": self.is_empty,
            "is_old": self.is_old,
            "is_devlog": self.is_devlog,
            "is_duplicate_name": self.is_duplicate_name,
            "last_modified": self.last_modified.isoformat(),
            "content_preview": self.content_preview,
            "dependencies": self.dependencies,
        }

    def should_keep(self, strategy: CleanupStrategy) -> bool:
        """Determine if file should be kept based on strategy."""
        if strategy == CleanupStrategy.NUCLEAR:
            return self.category == FileCategory.KEEP_CRITICAL
        elif strategy == CleanupStrategy.AGGRESSIVE:
            return self.category in [FileCategory.KEEP_CRITICAL, FileCategory.KEEP_RECENT]
        elif strategy == CleanupStrategy.MODERATE:
            return self.category in [
                FileCategory.KEEP_CRITICAL,
                FileCategory.KEEP_RECENT,
                FileCategory.CONSOLIDATE,
            ]
        else:  # CONSERVATIVE
            return self.category != FileCategory.DELETE_NUCLEAR

    def get_cleanup_action(self, strategy: CleanupStrategy) -> str:
        """Get recommended cleanup action."""
        if self.should_keep(strategy):
            return "keep"
        elif self.category == FileCategory.CONSOLIDATE:
            return "consolidate"
        else:
            return "delete"


@dataclass
class CleanupOperation:
    """Cleanup operation tracking"""

    operation_id: str
    strategy: CleanupStrategy
    status: CleanupStatus
    start_time: datetime
    end_time: datetime | None
    files_processed: int
    files_deleted: int
    files_kept: int
    files_consolidated: int
    space_freed: int
    errors: list[str]
    warnings: list[str]

    def get_duration(self) -> float | None:
        """Get operation duration in seconds."""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    def get_success_rate(self) -> float:
        """Get operation success rate."""
        if self.files_processed == 0:
            return 0.0
        return (self.files_processed - len(self.errors)) / self.files_processed * 100

    def is_completed(self) -> bool:
        """Check if operation is completed."""
        return self.status == CleanupStatus.COMPLETED

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "operation_id": self.operation_id,
            "strategy": self.strategy.value,
            "status": self.status.value,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "files_processed": self.files_processed,
            "files_deleted": self.files_deleted,
            "files_kept": self.files_kept,
            "files_consolidated": self.files_consolidated,
            "space_freed": self.space_freed,
            "errors": self.errors,
            "warnings": self.warnings,
            "duration_seconds": self.get_duration(),
            "success_rate": self.get_success_rate(),
        }


@dataclass
class CleanupConfiguration:
    """Cleanup configuration settings"""

    strategy: CleanupStrategy
    target_directory: str
    file_extensions: list[str]
    max_file_age_days: int
    min_file_size_bytes: int
    preserve_critical_files: list[str]
    preserve_recent_files: bool
    backup_enabled: bool
    dry_run: bool
    verbose_logging: bool

    def is_valid(self) -> bool:
        """Validate configuration."""
        return (
            self.target_directory
            and len(self.file_extensions) > 0
            and self.max_file_age_days >= 0
            and self.min_file_size_bytes >= 0
        )

    def get_strategy_aggressiveness(self) -> float:
        """Get strategy aggressiveness score (0-1)."""
        if self.strategy == CleanupStrategy.NUCLEAR:
            return 1.0
        elif self.strategy == CleanupStrategy.AGGRESSIVE:
            return 0.75
        elif self.strategy == CleanupStrategy.MODERATE:
            return 0.5
        else:  # CONSERVATIVE
            return 0.25


@dataclass
class CleanupReport:
    """Cleanup operation report"""

    report_id: str
    operation: CleanupOperation
    configuration: CleanupConfiguration
    analysis_summary: dict[str, Any]
    recommendations: list[str]
    generated_at: datetime

    def get_efficiency_score(self) -> float:
        """Get cleanup efficiency score."""
        if self.operation.files_processed == 0:
            return 0.0

        # Calculate efficiency based on space freed vs files processed
        space_efficiency = self.operation.space_freed / max(self.operation.files_processed, 1)
        success_efficiency = self.operation.get_success_rate() / 100

        return (space_efficiency * 0.6 + success_efficiency * 0.4) * 100

    def get_impact_assessment(self) -> str:
        """Get impact assessment."""
        deleted_ratio = self.operation.files_deleted / max(self.operation.files_processed, 1)

        if deleted_ratio >= 0.8:
            return "high_impact"
        elif deleted_ratio >= 0.5:
            return "medium_impact"
        elif deleted_ratio >= 0.2:
            return "low_impact"
        else:
            return "minimal_impact"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "report_id": self.report_id,
            "operation": self.operation.to_dict(),
            "configuration": {
                "strategy": self.configuration.strategy.value,
                "target_directory": self.configuration.target_directory,
                "aggressiveness": self.configuration.get_strategy_aggressiveness(),
            },
            "analysis_summary": self.analysis_summary,
            "recommendations": self.recommendations,
            "generated_at": self.generated_at.isoformat(),
            "efficiency_score": self.get_efficiency_score(),
            "impact_assessment": self.get_impact_assessment(),
        }


@dataclass
class FileAnalysisResult:
    """File analysis result"""

    total_files: int
    total_size: int
    critical_files: int
    recent_files: int
    duplicate_files: int
    empty_files: int
    old_files: int
    devlog_files: int
    potential_savings: int
    analysis_timestamp: datetime

    def get_cleanup_potential(self) -> dict[str, Any]:
        """Get cleanup potential analysis."""
        return {
            "files_can_delete": self.duplicate_files + self.empty_files + self.old_files,
            "files_can_consolidate": self.devlog_files,
            "space_can_free": self.potential_savings,
            "cleanup_percentage": (self.potential_savings / self.total_size * 100)
            if self.total_size > 0
            else 0,
            "files_to_keep": self.critical_files + self.recent_files,
        }
