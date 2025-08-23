#!/usr/bin/env python3
"""
Repository Discovery Engine
===========================

Responsible for discovering repositories in file systems.
Delegates specific responsibilities to focused components.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging
from pathlib import Path
from typing import List

from .discovery_config import DiscoveryConfig
from .file_filter import FileFilter
from .discovery_history import DiscoveryHistory

# Configure logging
logger = logging.getLogger(__name__)


class RepositoryDiscoveryEngine:
    """
    Repository discovery engine for automatic repository detection
    
    Features:
    - Automatic repository discovery
    - Pattern-based detection
    - Recursive and non-recursive scanning
    - Repository indicator recognition
    """

    def __init__(self, config: DiscoveryConfig = None):
        """Initialize the repository discovery engine"""
        self.config = config or DiscoveryConfig()
        self.file_filter = FileFilter(self.config.excluded_patterns)
        self.history = DiscoveryHistory()
        
        logger.info("Repository Discovery Engine initialized")

    def discover_repositories(self, root_path: str, recursive: bool = True) -> List[str]:
        """Discover repositories in the given path"""
        try:
            discovered = []
            root = Path(root_path)

            if not root.exists():
                logger.error(f"Root path does not exist: {root_path}")
                return discovered

            # Look for common repository indicators
            repository_indicators = [
                ".git",
                ".svn",
                ".hg",
                "package.json",
                "requirements.txt",
                "pom.xml",
                "build.gradle",
                "Cargo.toml",
                "go.mod",
                "*.sln",
            ]

            if recursive:
                # Recursive discovery
                for indicator in repository_indicators:
                    if "*" in indicator:
                        # Pattern matching
                        for path in root.rglob(indicator.replace("*", "*")):
                            repo_path = path.parent if path.is_file() else path
                            if str(repo_path) not in discovered:
                                discovered.append(str(repo_path))
                                logger.info(f"Discovered repository: {repo_path}")
                    else:
                        # Exact file/directory matching
                        for path in root.rglob(indicator):
                            repo_path = path.parent if path.is_file() else path
                            if str(repo_path) not in discovered:
                                discovered.append(str(repo_path))
                                logger.info(f"Discovered repository: {repo_path}")
            else:
                # Non-recursive discovery (only immediate subdirectories)
                for item in root.iterdir():
                    if item.is_dir():
                        for indicator in repository_indicators:
                            indicator_path = item / indicator
                            if indicator_path.exists():
                                if str(item) not in discovered:
                                    discovered.append(str(item))
                                    logger.info(f"Discovered repository: {item}")
                                break

            # Update discovered repositories and history
            self.history.add_discovered_repositories(discovered)
            self.history.record_discovery_operation(root_path, recursive, len(discovered))

            logger.info(f"Discovered {len(discovered)} repositories in {root_path}")
            return discovered

        except Exception as e:
            logger.error(f"Failed to discover repositories: {e}")
            return []

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis"""
        return self.file_filter.should_exclude_file(file_path)

    def get_discovery_summary(self) -> dict:
        """Get a summary of discovery operations"""
        summary = self.history.get_discovery_summary()
        summary["config"] = {
            "scan_depth": self.config.scan_depth,
            "max_file_size_mb": self.config.max_file_size_mb,
            "excluded_patterns_count": self.config.get_excluded_patterns_count(),
            "included_extensions_count": self.config.get_included_extensions_count()
        }
        return summary

    def clear_discovery_cache(self):
        """Clear discovered repositories cache"""
        self.history.clear_history()
        logger.info("Discovery cache cleared")

    def is_repository_path(self, path: str) -> bool:
        """Check if a path is a known repository"""
        return self.history.is_repository_path(path)

    def get_repository_paths(self) -> List[str]:
        """Get all discovered repository paths"""
        return self.history.get_repository_paths()


def main():
    """Main function for standalone testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Repository Discovery Engine")
    parser.add_argument("--discover", type=str, help="Discover repositories in path")
    parser.add_argument("--summary", action="store_true", help="Show discovery summary")
    parser.add_argument("--clear", action="store_true", help="Clear discovery cache")

    args = parser.parse_args()

    engine = RepositoryDiscoveryEngine()

    try:
        if args.discover:
            print(f"🔍 Discovering repositories in: {args.discover}")
            repositories = engine.discover_repositories(args.discover)
            print(f"✅ Discovered {len(repositories)} repositories:")
            for repo in repositories[:10]:  # Show first 10
                print(f"  - {repo}")
            if len(repositories) > 10:
                print(f"  ... and {len(repositories) - 10} more")

        elif args.summary:
            summary = engine.get_discovery_summary()
            print(f"📊 Discovery Summary:")
            print(f"  Total Discovered: {summary['total_discovered']}")
            print(f"  Discovery Operations: {summary['operations_count']}")
            print(f"  Config - Scan Depth: {summary['config']['scan_depth']}")
            print(f"  Config - Max File Size: {summary['config']['max_file_size_mb']} MB")

        elif args.clear:
            engine.clear_discovery_cache()
            print("🗑️ Discovery cache cleared")

        else:
            print("🔍 Repository Discovery Engine ready")
            print("Use --discover <path> to discover repositories")
            print("Use --summary to show discovery summary")
            print("Use --clear to clear discovery cache")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
