#!/usr/bin/env python3
"""
Technology Database Manager
===========================

Manages technology detection patterns and rules.
Separates database concerns from detection logic.

Author: Agent-1 (Performance & Health Systems)
License: MIT
"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class TechnologyDatabase:
    """Manages technology detection patterns and rules"""
    
    def __init__(self):
        """Initialize the technology database"""
        self.database = self._load_default_database()
        logger.info("Technology Database initialized")

    def _load_default_database(self) -> Dict[str, Any]:
        """Load default technology detection patterns and rules"""
        return {
            "languages": {
                "python": {
                    "extensions": [".py", ".pyw", ".pyx"],
                    "files": [
                        "requirements.txt",
                        "setup.py",
                        "pyproject.toml",
                        "Pipfile",
                    ],
                    "patterns": [
                        r"import\s+\w+",
                        r"from\s+\w+\s+import",
                        r"def\s+\w+\s*\(",
                    ],
                },
                "javascript": {
                    "extensions": [".js", ".jsx", ".ts", ".tsx"],
                    "files": ["package.json", "yarn.lock", "package-lock.json"],
                    "patterns": [r"import\s+.*\s+from", r"require\s*\(", r"export\s+"],
                },
                "java": {
                    "extensions": [".java", ".class", ".jar"],
                    "files": ["pom.xml", "build.gradle", "gradle.properties"],
                    "patterns": [r"import\s+\w+", r"public\s+class", r"@\w+"],
                },
                "go": {
                    "extensions": [".go"],
                    "files": ["go.mod", "go.sum", "Gopkg.toml"],
                    "patterns": [r"package\s+\w+", r"import\s+\(", r"func\s+\w+\s*\("],
                },
                "rust": {
                    "extensions": [".rs"],
                    "files": ["Cargo.toml", "Cargo.lock"],
                    "patterns": [r"use\s+\w+", r"fn\s+\w+\s*\(", r"struct\s+\w+"],
                },
            },
            "frameworks": {
                "django": {
                    "patterns": [r"from\s+django", r"INSTALLED_APPS", r"MIDDLEWARE"]
                },
                "flask": {"patterns": [r"from\s+flask", r"Flask\(", r"@app\.route"]},
                "react": {"patterns": [r"import\s+React", r"useState", r"useEffect"]},
                "angular": {"patterns": [r"@Component", r"@Injectable", r"@NgModule"]},
                "spring": {
                    "patterns": [
                        r"@SpringBootApplication",
                        r"@RestController",
                        r"@Service",
                    ]
                },
            },
            "databases": {
                "postgresql": {"patterns": [r"psycopg2", r"postgresql", r"postgres"]},
                "mysql": {"patterns": [r"mysql-connector", r"mysqldb", r"mysql"]},
                "mongodb": {"patterns": [r"pymongo", r"mongodb", r"mongoose"]},
                "redis": {"patterns": [r"redis", r"redis-py", r"ioredis"]},
            },
        }

    def get_database(self) -> Dict[str, Any]:
        """Get the complete technology database"""
        return self.database

    def get_languages(self) -> Dict[str, Any]:
        """Get language detection patterns"""
        return self.database.get("languages", {})

    def get_frameworks(self) -> Dict[str, Any]:
        """Get framework detection patterns"""
        return self.database.get("frameworks", {})

    def get_databases(self) -> Dict[str, Any]:
        """Get database detection patterns"""
        return self.database.get("databases", {})

    def add_custom_pattern(self, category: str, name: str, patterns: List[str]):
        """Add custom detection patterns"""
        if category not in self.database:
            self.database[category] = {}
        
        self.database[category][name] = {"patterns": patterns}
        logger.info(f"Added custom pattern for {category}:{name}")

    def get_detection_stats(self) -> Dict[str, int]:
        """Get statistics about detection capabilities"""
        stats = {}
        for category, items in self.database.items():
            stats[category] = len(items)
        return stats

    def get_patterns_count(self) -> int:
        """Get total count of detection patterns"""
        total = 0
        for category in self.database.values():
            total += len(category)
        return total

