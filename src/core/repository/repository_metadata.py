#!/usr/bin/env python3
"""
Repository Metadata Manager
===========================

Manages repository metadata structures and operations.
Separates metadata concerns from report generation logic.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class RepositoryMetadata:
    """Repository metadata and analysis results"""

    repository_id: str
    name: str
    path: str
    size_bytes: int = 0
    file_count: int = 0
    language_count: int = 0
    last_modified: datetime = None
    technology_stack: Dict[str, Any] = None
    health_score: float = 0.0
    market_readiness: float = 0.0
    dependencies: List[str] = None
    architecture_patterns: List[str] = None
    performance_metrics: Dict[str, Any] = None
    security_analysis: Dict[str, Any] = None
    recommendations: List[str] = None

    def __post_init__(self):
        if self.last_modified is None:
            self.last_modified = datetime.now()
        if self.technology_stack is None:
            self.technology_stack = {}
        if self.dependencies is None:
            self.dependencies = []
        if self.architecture_patterns is None:
            self.architecture_patterns = []
        if self.performance_metrics is None:
            self.performance_metrics = {}
        if self.security_analysis is None:
            self.security_analysis = {}
        if self.recommendations is None:
            self.recommendations = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary"""
        return asdict(self)

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of the metadata"""
        return {
            "repository_id": self.repository_id,
            "name": self.name,
            "path": self.path,
            "size_mb": self.size_bytes / (1024 * 1024),
            "file_count": self.file_count,
            "language_count": self.language_count,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "technology_stack": self.technology_stack,
            "scores": {
                "health_score": self.health_score,
                "market_readiness": self.market_readiness,
            },
            "architecture_patterns": self.architecture_patterns,
            "dependencies_count": len(self.dependencies),
            "recommendations_count": len(self.recommendations),
        }

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get performance metrics summary"""
        return {
            "code_files": self.performance_metrics.get("code_files", 0),
            "complexity_score": self.performance_metrics.get("complexity_score", 0),
            "total_files": self.performance_metrics.get("total_files", 0),
            "average_file_size": self.performance_metrics.get("average_file_size", 0),
        }

    def get_security_summary(self) -> Dict[str, Any]:
        """Get security analysis summary"""
        return {
            "security_score": self.security_analysis.get("security_score", 100),
            "security_issues": len(self.security_analysis.get("security_issues", [])),
            "has_secrets": self.security_analysis.get("has_secrets", False),
        }


class RepositoryMetadataManager:
    """Manages repository metadata operations"""
    
    def __init__(self):
        """Initialize the metadata manager"""
        self.repositories: Dict[str, RepositoryMetadata] = {}
        logger.info("Repository Metadata Manager initialized")

    def add_repository(self, metadata: RepositoryMetadata):
        """Add a repository to the manager"""
        self.repositories[metadata.repository_id] = metadata
        logger.debug(f"Added repository: {metadata.name}")

    def get_repository(self, repository_id: str) -> Optional[RepositoryMetadata]:
        """Get a repository by ID"""
        return self.repositories.get(repository_id)

    def get_all_repositories(self) -> Dict[str, RepositoryMetadata]:
        """Get all repositories"""
        return self.repositories.copy()

    def get_repository_count(self) -> int:
        """Get total number of repositories"""
        return len(self.repositories)

    def clear_repositories(self):
        """Clear all repositories"""
        self.repositories.clear()
        logger.info("All repositories cleared")

    def get_repository_ids(self) -> List[str]:
        """Get list of repository IDs"""
        return list(self.repositories.keys())

    def has_repository(self, repository_id: str) -> bool:
        """Check if repository exists"""
        return repository_id in self.repositories

    def get_repositories_by_language(self, language: str) -> List[RepositoryMetadata]:
        """Get repositories by programming language"""
        return [
            repo for repo in self.repositories.values()
            if repo.technology_stack.get("language") == language
        ]

    def get_repositories_by_score_range(self, min_score: float, max_score: float) -> List[RepositoryMetadata]:
        """Get repositories within a health score range"""
        return [
            repo for repo in self.repositories.values()
            if min_score <= repo.health_score <= max_score
        ]

