#!/usr/bin/env python3
"""
Configuration Consolidator Module - V2 Compliant
==============================================

Configuration consolidation functionality extracted from consolidated_config_management.py
for V2 compliance (≤400 lines).

Provides:
- Configuration pattern consolidation
- Unified configuration management
- Configuration analysis and reporting
- Single source of truth for configuration

Author: Agent-3 (Infrastructure & DevOps Specialist)
License: MIT
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .config_scanner import ConfigPattern
from .config_validator import ConfigValidationResult

logger = logging.getLogger(__name__)


@dataclass
class ConfigConsolidationResult:
    """Result of configuration consolidation."""

    patterns_found: int
    files_scanned: int
    consolidation_suggestions: list[str]
    validation_results: ConfigValidationResult
    consolidated_config: dict[str, Any] = field(default_factory=dict)


class ConfigurationConsolidator:
    """Consolidates configuration patterns and provides unified management."""

    def __init__(self):
        self.consolidated_config = {}
        self.pattern_history = []
        self.consolidation_rules = {}

    def consolidate_patterns(self, patterns: list[ConfigPattern]) -> ConfigConsolidationResult:
        """Consolidate configuration patterns into a unified structure."""
        logger.info(f"Consolidating {len(patterns)} configuration patterns")
        
        # Group patterns by type and key
        grouped_patterns = self._group_patterns(patterns)
        
        # Consolidate each group
        consolidated_config = {}
        suggestions = []
        
        for group_key, group_patterns in grouped_patterns.items():
            consolidated_item = self._consolidate_pattern_group(group_key, group_patterns)
            consolidated_config[group_key] = consolidated_item
            
            # Generate suggestions for this group
            group_suggestions = self._generate_consolidation_suggestions(group_key, group_patterns)
            suggestions.extend(group_suggestions)
        
        # Validate consolidated configuration
        from .config_validator import ConfigurationValidator
        validator = ConfigurationValidator()
        validation_results = validator.validate_patterns(patterns)
        
        result = ConfigConsolidationResult(
            patterns_found=len(patterns),
            files_scanned=len(set(p.file_path for p in patterns)),
            consolidation_suggestions=suggestions,
            validation_results=validation_results,
            consolidated_config=consolidated_config
        )
        
        self.consolidated_config = consolidated_config
        self.pattern_history.extend(patterns)
        
        return result

    def _group_patterns(self, patterns: list[ConfigPattern]) -> dict[str, list[ConfigPattern]]:
        """Group patterns by type and key for consolidation."""
        groups = {}
        
        for pattern in patterns:
            # Create a group key based on pattern type and key
            group_key = f"{pattern.pattern_type}:{pattern.key}"
            
            if group_key not in groups:
                groups[group_key] = []
            groups[group_key].append(pattern)
        
        return groups

    def _consolidate_pattern_group(self, group_key: str, patterns: list[ConfigPattern]) -> dict[str, Any]:
        """Consolidate a group of related patterns."""
        if not patterns:
            return {}
        
        # Use the first pattern as the base
        base_pattern = patterns[0]
        
        consolidated = {
            "type": base_pattern.pattern_type,
            "key": base_pattern.key,
            "source": base_pattern.source,
            "files": list(set(p.file_path for p in patterns)),
            "line_numbers": [p.line_number for p in patterns],
            "contexts": [p.context for p in patterns],
            "confidence": sum(p.confidence for p in patterns) / len(patterns),
            "count": len(patterns),
            "metadata": self._merge_metadata([p.metadata for p in patterns])
        }
        
        # Add type-specific consolidation
        if base_pattern.pattern_type in ["getenv", "environ_get", "environ_direct"]:
            consolidated["env_var"] = base_pattern.key
            consolidated["usage_count"] = len(patterns)
        elif base_pattern.pattern_type in ["json_load_file", "yaml_load_file"]:
            consolidated["config_file"] = base_pattern.key
            consolidated["file_type"] = base_pattern.pattern_type.split("_")[0]
        elif base_pattern.pattern_type in ["config_parser", "ini_file_extension"]:
            consolidated["config_type"] = "ini"
            consolidated["file_extension"] = base_pattern.key.split(".")[-1] if "." in base_pattern.key else "unknown"
        
        return consolidated

    def _merge_metadata(self, metadata_list: list[dict[str, Any]]) -> dict[str, Any]:
        """Merge metadata from multiple patterns."""
        merged = {}
        
        for metadata in metadata_list:
            for key, value in metadata.items():
                if key not in merged:
                    merged[key] = []
                if isinstance(value, list):
                    merged[key].extend(value)
                else:
                    merged[key].append(value)
        
        # Deduplicate lists
        for key, value in merged.items():
            if isinstance(value, list):
                merged[key] = list(set(value))
        
        return merged

    def _generate_consolidation_suggestions(self, group_key: str, patterns: list[ConfigPattern]) -> list[str]:
        """Generate consolidation suggestions for a pattern group."""
        suggestions = []
        
        if len(patterns) > 1:
            pattern_type = patterns[0].pattern_type
            key = patterns[0].key
            
            if pattern_type in ["getenv", "environ_get", "environ_direct"]:
                suggestions.append(f"Consider centralizing environment variable '{key}' usage (found in {len(patterns)} places)")
            elif pattern_type in ["json_load_file", "yaml_load_file"]:
                suggestions.append(f"Consider consolidating configuration file '{key}' loading (found in {len(patterns)} places)")
            elif pattern_type in ["config_parser"]:
                suggestions.append(f"Consider using a single configuration parser instance for '{key}' (found in {len(patterns)} places)")
        
        # Check for potential conflicts
        files = set(p.file_path for p in patterns)
        if len(files) > 1:
            suggestions.append(f"Configuration '{group_key}' is used across {len(files)} files - consider centralizing")
        
        return suggestions

    def get_consolidated_config(self) -> dict[str, Any]:
        """Get the current consolidated configuration."""
        return self.consolidated_config

    def get_config_summary(self) -> dict[str, Any]:
        """Get a summary of the consolidated configuration."""
        if not self.consolidated_config:
            return {"message": "No configuration consolidated yet"}
        
        summary = {
            "total_config_items": len(self.consolidated_config),
            "pattern_types": {},
            "files_involved": set(),
            "environment_variables": [],
            "config_files": [],
            "suggestions_count": 0
        }
        
        for item_key, item_data in self.consolidated_config.items():
            pattern_type = item_data.get("type", "unknown")
            summary["pattern_types"][pattern_type] = summary["pattern_types"].get(pattern_type, 0) + 1
            
            if "files" in item_data:
                summary["files_involved"].update(item_data["files"])
            
            if pattern_type in ["getenv", "environ_get", "environ_direct"]:
                summary["environment_variables"].append(item_data.get("key"))
            elif pattern_type in ["json_load_file", "yaml_load_file"]:
                summary["config_files"].append(item_data.get("key"))
        
        summary["files_involved"] = list(summary["files_involved"])
        
        return summary

    def export_consolidated_config(self, output_path: Path) -> bool:
        """Export consolidated configuration to a file."""
        try:
            import json
            
            export_data = {
                "consolidated_config": self.consolidated_config,
                "summary": self.get_config_summary(),
                "pattern_history_count": len(self.pattern_history)
            }
            
            with open(output_path, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            logger.info(f"Consolidated configuration exported to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to export consolidated configuration: {e}")
            return False

    def add_consolidation_rule(self, rule_name: str, rule_function: callable):
        """Add a custom consolidation rule."""
        self.consolidation_rules[rule_name] = rule_function

    def apply_custom_rules(self, patterns: list[ConfigPattern]) -> list[str]:
        """Apply custom consolidation rules to patterns."""
        suggestions = []
        
        for rule_name, rule_function in self.consolidation_rules.items():
            try:
                rule_suggestions = rule_function(patterns)
                if isinstance(rule_suggestions, list):
                    suggestions.extend([f"Rule '{rule_name}': {suggestion}" for suggestion in rule_suggestions])
                else:
                    suggestions.append(f"Rule '{rule_name}': {rule_suggestions}")
            except Exception as e:
                logger.error(f"Custom consolidation rule '{rule_name}' failed: {e}")
        
        return suggestions


if __name__ == "__main__":
    # Example usage
    consolidator = ConfigurationConsolidator()
    
    # Create sample patterns
    sample_patterns = [
        ConfigPattern(
            file_path=Path("app.py"),
            line_number=10,
            pattern_type="getenv",
            key="API_KEY",
            value=None,
            context="api_key = os.getenv('API_KEY')",
            source="environment_variable"
        ),
        ConfigPattern(
            file_path=Path("config.py"),
            line_number=5,
            pattern_type="getenv",
            key="API_KEY",
            value=None,
            context="API_KEY = os.getenv('API_KEY')",
            source="environment_variable"
        ),
        ConfigPattern(
            file_path=Path("settings.py"),
            line_number=15,
            pattern_type="json_load_file",
            key="config.json",
            value=None,
            context="config = json.load(open('config.json'))",
            source="json_configuration"
        )
    ]
    
    # Consolidate patterns
    result = consolidator.consolidate_patterns(sample_patterns)
    
    print(f"Consolidated {result.patterns_found} patterns from {result.files_scanned} files")
    print(f"Generated {len(result.consolidation_suggestions)} suggestions")
    print(f"Validation status: {'✅ VALID' if result.validation_results.is_valid else '❌ INVALID'}")
    
    # Get summary
    summary = consolidator.get_config_summary()
    print(f"\nConfiguration Summary:")
    print(f"  Total items: {summary['total_config_items']}")
    print(f"  Pattern types: {summary['pattern_types']}")
    print(f"  Files involved: {len(summary['files_involved'])}")
    print(f"  Environment variables: {len(summary['environment_variables'])}")
    print(f"  Config files: {len(summary['config_files'])}")
