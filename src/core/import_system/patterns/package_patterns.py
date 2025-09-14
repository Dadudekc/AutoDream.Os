"""
Package Import Patterns
=======================

Patterns for package-level imports and dependency management.
"""

import re
from typing import Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class PackageImportPattern:
    """Pattern for package import matching."""
    name: str
    package_pattern: str
    dependencies: List[str]
    version_constraint: Optional[str] = None
    
    def matches(self, package_name: str) -> bool:
        """Check if package name matches this pattern."""
        return package_name.startswith(self.package_pattern)


class PackagePatternRegistry:
    """Registry for package import patterns."""
    
    def __init__(self):
        self.patterns: List[PackageImportPattern] = []
        self._compile_default_patterns()
    
    def _compile_default_patterns(self):
        """Compile default package patterns."""
        default_patterns = [
            PackageImportPattern(
                name="standard_library",
                package_pattern="",
                dependencies=[]
            ),
            PackageImportPattern(
                name="project_packages",
                package_pattern="src.",
                dependencies=["typing", "dataclasses", "pathlib"]
            )
        ]
        self.patterns.extend(default_patterns)
    
    def get_matching_pattern(self, package_name: str) -> Optional[PackageImportPattern]:
        """Get pattern that matches the package name."""
        for pattern in self.patterns:
            if pattern.matches(package_name):
                return pattern
        return None
    
    def get_dependencies(self, package_name: str) -> List[str]:
        """Get dependencies for a package."""
        pattern = self.get_matching_pattern(package_name)
        return pattern.dependencies if pattern else []

