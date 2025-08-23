#!/usr/bin/env python3
"""
Technology Stack Detector
=========================

Responsible for detecting technology stacks in repositories.
Delegates specific responsibilities to focused components.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, field

from .technology_database import TechnologyDatabase
from .version_detector import VersionDetector

# Configure logging
logger = logging.getLogger(__name__)


@dataclass
class TechnologyStack:
    """Detected technology stack information"""

    language: str = "unknown"
    version: str = "unknown"
    framework: Optional[str] = None
    database: Optional[str] = None
    frontend: Optional[str] = None
    backend: Optional[str] = None
    cloud: Optional[str] = None
    container: Optional[str] = None
    ci_cd: Optional[str] = None
    testing: Optional[str] = None
    documentation: Optional[str] = None
    confidence: float = 0.0


class TechnologyDetector:
    """
    Technology stack detector for repository analysis
    
    Features:
    - Language detection
    - Framework identification
    - Database technology recognition
    - Version detection coordination
    """

    def __init__(self):
        """Initialize the technology detector"""
        self.database = TechnologyDatabase()
        self.version_detector = VersionDetector()
        logger.info("Technology Detector initialized")

    def detect_technology_stack(
        self, repo_path: Path, should_exclude_file_func
    ) -> TechnologyStack:
        """Detect technology stack and versions"""
        try:
            detected_languages = self._detect_languages(repo_path, should_exclude_file_func)
            detected_frameworks = self._detect_frameworks(repo_path, should_exclude_file_func)
            detected_databases = self._detect_databases(repo_path, should_exclude_file_func)

            # Create technology stack
            tech_stack = TechnologyStack()
            
            if detected_languages:
                tech_stack.language = list(detected_languages)[0]
                tech_stack.confidence = 0.8

            if detected_frameworks:
                tech_stack.framework = ", ".join(detected_frameworks)

            if detected_databases:
                tech_stack.database = ", ".join(detected_databases)

            logger.debug(
                f"Technology stack: {detected_languages}, {detected_frameworks}, {detected_databases}"
            )
            
            return tech_stack

        except Exception as e:
            logger.error(f"Failed to detect technology stack: {e}")
            return TechnologyStack()

    def _detect_languages(self, repo_path: Path, should_exclude_file_func) -> Set[str]:
        """Detect programming languages"""
        detected = set()
        for language, config in self.database.get_languages().items():
            # Check for language-specific files
            for file_name in config["files"]:
                if (repo_path / file_name).exists():
                    detected.add(language)
                    break

            # Check for language-specific patterns in code files
            if language in detected:
                continue

            for ext in config["extensions"]:
                for file_path in repo_path.rglob(f"*{ext}"):
                    if should_exclude_file_func(file_path):
                        continue

                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            for pattern in config["patterns"]:
                                if re.search(pattern, content, re.IGNORECASE):
                                    detected.add(language)
                                    break
                            if language in detected:
                                break
                    except (OSError, UnicodeDecodeError):
                        continue
        return detected

    def _detect_frameworks(self, repo_path: Path, should_exclude_file_func) -> Set[str]:
        """Detect frameworks"""
        return self._detect_by_patterns(repo_path, should_exclude_file_func, self.database.get_frameworks())

    def _detect_databases(self, repo_path: Path, should_exclude_file_func) -> Set[str]:
        """Detect databases"""
        return self._detect_by_patterns(repo_path, should_exclude_file_func, self.database.get_databases())

    def _detect_by_patterns(self, repo_path: Path, should_exclude_file_func, patterns_dict: Dict[str, Any]) -> Set[str]:
        """Generic pattern-based detection"""
        detected = set()
        for name, config in patterns_dict.items():
            for file_path in repo_path.rglob("*"):
                if file_path.is_file() and not should_exclude_file_func(file_path):
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            content = f.read()
                            for pattern in config["patterns"]:
                                if re.search(pattern, content, re.IGNORECASE):
                                    detected.add(name)
                                    break
                            if name in detected:
                                break
                    except (OSError, UnicodeDecodeError):
                        continue
        return detected

    def detect_versions(self, repo_path: Path, tech_stack: TechnologyStack) -> Dict[str, str]:
        """Detect versions of detected technologies"""
        return self.version_detector.detect_versions(repo_path, {
            "language": tech_stack.language,
            "framework": tech_stack.framework
        })

    def get_technology_patterns(self) -> Dict[str, Any]:
        """Get all technology detection patterns"""
        return self.database.get_database()

    def add_custom_pattern(self, category: str, name: str, patterns: List[str]):
        """Add custom detection patterns"""
        self.database.add_custom_pattern(category, name, patterns)

    def get_detection_stats(self) -> Dict[str, int]:
        """Get statistics about detection capabilities"""
        return self.database.get_detection_stats()


def main():
    """Main function for standalone testing"""
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Technology Stack Detector")
    parser.add_argument("--detect", type=str, help="Detect technology in repository path")
    parser.add_argument("--patterns", action="store_true", help="Show detection patterns")
    parser.add_argument("--stats", action="store_true", help="Show detection statistics")

    args = parser.parse_args()

    detector = TechnologyDetector()

    try:
        if args.detect:
            repo_path = Path(args.detect)
            if not repo_path.exists():
                print(f"❌ Repository path does not exist: {args.detect}")
                return

            print(f"🔍 Detecting technology stack in: {args.detect}")
            
            # Mock exclude function for testing
            def mock_exclude(file_path):
                return False
            
            tech_stack = detector.detect_technology_stack(repo_path, mock_exclude)
            versions = detector.detect_versions(repo_path, tech_stack)
            
            print(f"✅ Technology Stack Detected:")
            print(f"  Language: {tech_stack.language}")
            print(f"  Framework: {tech_stack.framework or 'None'}")
            print(f"  Database: {tech_stack.database or 'None'}")
            print(f"  Confidence: {tech_stack.confidence}")
            print(f"  Versions: {versions}")

        elif args.patterns:
            patterns = detector.get_technology_patterns()
            print(f"🔍 Technology Detection Patterns:")
            for category, items in patterns.items():
                print(f"  {category.upper()}:")
                for name, config in items.items():
                    print(f"    {name}: {len(config.get('patterns', []))} patterns")

        elif args.stats:
            stats = detector.get_detection_stats()
            print(f"📊 Detection Statistics:")
            for category, count in stats.items():
                print(f"  {category}: {count} items")

        else:
            print("🔍 Technology Stack Detector ready")
            print("Use --detect <path> to detect technology in a repository")
            print("Use --patterns to show detection patterns")
            print("Use --stats to show detection statistics")

    except Exception as e:
        print(f"❌ Operation failed: {e}")
        exit(1)


if __name__ == "__main__":
    main()
