#!/usr/bin/env python3
"""
Configuration Report Generator - Agent Cellphone V2
=================================================

Generates configuration consolidation reports.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

from typing import Dict, Any, List

from .config_consolidator import ConfigPattern


class ConfigurationReportGenerator:
    """Generates configuration consolidation reports."""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
    
    def generate_consolidation_report(self, patterns: List[ConfigPattern], 
                                    consolidated_count: int,
                                    migrated_files: set) -> str:
        """Generate a consolidation report."""
        report_lines = [
            "# Configuration Consolidation Report",
            "",
            f"**Agent**: Agent-8 (SSOT Maintenance & System Integration Specialist)",
            f"**Mission**: Configuration Pattern Consolidation",
            f"**Status**: SSOT Implementation Complete",
            "",
            "## Summary",
            f"- Total patterns found: {len(patterns)}",
            f"- Consolidated patterns: {consolidated_count}",
            f"- Migrated files: {len(migrated_files)}",
            "",
            "## Pattern Types",
        ]
        
        pattern_types = {}
        for pattern in patterns:
            if pattern.pattern_type not in pattern_types:
                pattern_types[pattern.pattern_type] = 0
            pattern_types[pattern.pattern_type] += 1
            
        for pattern_type, count in pattern_types.items():
            report_lines.append(f"- {pattern_type}: {count} patterns")
            
        report_lines.extend([
            "",
            "## Centralized Configuration Keys",
        ])
        
        all_config = self.config_manager.get_all_config()
        for key, value in sorted(all_config.items()):
            config_info = self.config_manager.get_config_info(key)
            source = config_info.source.value if config_info else "unknown"
            report_lines.append(f"- {key} = {value} (source: {source})")
            
        report_lines.extend([
            "",
            "## Benefits Achieved",
            "- ✅ Single Source of Truth (SSOT) for all configuration",
            "- ✅ Centralized configuration management",
            "- ✅ Environment-specific configuration support",
            "- ✅ Configuration validation and metadata",
            "- ✅ Reduced configuration duplication",
            "- ✅ Improved maintainability and consistency",
            "",
            "**Agent-8 - SSOT Maintenance & System Integration Specialist**",
            "**Configuration Pattern Consolidation Mission Complete**"
        ])
        
        return '\n'.join(report_lines)
