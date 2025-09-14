"""
Module Import Patterns
=====================

Patterns for module-level imports and caching.
"""

import re
from typing import Dict, List, Optional, Pattern
from dataclasses import dataclass


@dataclass
class ModuleImportPattern:
    """Pattern for module import matching."""
    name: str
    pattern: Pattern[str]
    priority: int = 1
    cache_ttl: int = 3600  # 1 hour default
    
    def matches(self, module_name: str) -> bool:
        """Check if module name matches this pattern."""
        return bool(self.pattern.match(module_name))


class ModulePatternRegistry:
    """Registry for module import patterns."""
    
    def __init__(self):
        self.patterns: List[ModuleImportPattern] = []
        self._compile_default_patterns()
    
    def _compile_default_patterns(self):
        """Compile default import patterns."""
        default_patterns = [
            ModuleImportPattern(
                name="core_modules",
                pattern=re.compile(r"^src\.core\."),
                priority=1
            ),
            ModuleImportPattern(
                name="service_modules", 
                pattern=re.compile(r"^src\.services\."),
                priority=2
            ),
            ModuleImportPattern(
                name="tool_modules",
                pattern=re.compile(r"^tools\."),
                priority=3
            )
        ]
        self.patterns.extend(default_patterns)
    
    def get_matching_pattern(self, module_name: str) -> Optional[ModuleImportPattern]:
        """Get the highest priority pattern that matches the module name."""
        matching_patterns = [p for p in self.patterns if p.matches(module_name)]
        if not matching_patterns:
            return None
        return min(matching_patterns, key=lambda p: p.priority)
    
    def add_pattern(self, pattern: ModuleImportPattern):
        """Add a new import pattern."""
        self.patterns.append(pattern)
        self.patterns.sort(key=lambda p: p.priority)

