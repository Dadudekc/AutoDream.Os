#!/usr/bin/env python3
"""
Discovery History
================

Manages discovery history and tracking for repository discovery operations.
Separates history concerns from discovery logic.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging

from src.utils.stability_improvements import stability_manager, safe_import
from typing import List, Set, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class DiscoveryHistory:
    """Manages discovery history and tracking"""
    
    def __init__(self):
        """Initialize the discovery history manager"""
        self.discovered_repositories: Set[str] = set()
        self.discovery_history: List[Dict[str, Any]] = []
        logger.info("Discovery History initialized")

    def add_discovered_repositories(self, repositories: List[str]):
        """Add discovered repositories to the set"""
        try:
            for repo in repositories:
                self.discovered_repositories.add(repo)
            logger.debug(f"Added {len(repositories)} repositories to discovered set")
        except Exception as e:
            logger.error(f"Error adding discovered repositories: {e}")

    def record_discovery_operation(self, root_path: str, recursive: bool, discovered_count: int):
        """Record a discovery operation"""
        try:
            self.discovery_history.append({
                "timestamp": datetime.now().isoformat(),
                "root_path": root_path,
                "recursive": recursive,
                "discovered_count": discovered_count,
                "total_discovered": len(self.discovered_repositories)
            })
            logger.debug(f"Recorded discovery operation: {root_path}")
        except Exception as e:
            logger.error(f"Error recording discovery operation: {e}")

    def get_discovery_summary(self) -> Dict[str, Any]:
        """Get a summary of discovery operations"""
        return {
            "total_discovered": len(self.discovered_repositories),
            "discovery_history": self.discovery_history.copy(),
            "operations_count": len(self.discovery_history)
        }

    def clear_history(self):
        """Clear discovery history and discovered repositories"""
        self.discovered_repositories.clear()
        self.discovery_history.clear()
        logger.info("Discovery history cleared")

    def is_repository_path(self, path: str) -> bool:
        """Check if a path is a known repository"""
        return path in self.discovered_repositories

    def get_repository_paths(self) -> List[str]:
        """Get all discovered repository paths"""
        return list(self.discovered_repositories)

    def get_history_count(self) -> int:
        """Get count of discovery operations"""
        return len(self.discovery_history)

