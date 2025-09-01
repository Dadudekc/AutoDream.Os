#!/usr/bin/env python3
"""
Configuration Consolidator - Agent Cellphone V2
=============================================

Utility for consolidating scattered configuration patterns into the centralized
SSOT system.

Agent: Agent-8 (SSOT Maintenance & System Integration Specialist)
Mission: Configuration Pattern Consolidation
Status: SSOT Migration - Configuration Consolidation
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import dataclass

from .config_core import ConfigurationManager, ConfigSource, get_config_manager
from .config_pattern_scanner import ConfigurationPatternScanner
from .config_file_migrator import ConfigurationFileMigrator
from .config_report_generator import ConfigurationReportGenerator


@dataclass
class ConfigPattern:
    """Configuration pattern found in code."""
    file_path: Path
    line_number: int
    pattern_type: str
    key: str
    value: Any
    context: str
    source: str


class ConfigurationConsolidator:
    """Consolidates configuration patterns into centralized SSOT system."""
    
    def __init__(self):
        self.config_manager = get_config_manager()
        self.scanner = ConfigurationPatternScanner()
        self.migrator = ConfigurationFileMigrator()
        self.report_generator = ConfigurationReportGenerator(self.config_manager)
        self.patterns: List[ConfigPattern] = []
        self.consolidated_count = 0
        
    def scan_configuration_patterns(self, root_dir: Path) -> Dict[str, List[ConfigPattern]]:
        """Scan for configuration patterns in the codebase."""
        print("🔍 Scanning for configuration patterns...")
        
        patterns_by_type = {
            "environment_variables": [],
            "hardcoded_values": [],
            "config_constants": [],
            "settings_patterns": []
        }
        
        # Scan Python files for configuration patterns
        for py_file in root_dir.rglob("*.py"):
            if self._should_skip_file(py_file):
                continue
                
            file_patterns = self.scanner.scan_file_for_patterns(py_file)
            for pattern in file_patterns:
                patterns_by_type[pattern.pattern_type].append(pattern)
                self.patterns.append(pattern)
                
        print(f"✅ Found {len(self.patterns)} configuration patterns")
        for pattern_type, patterns in patterns_by_type.items():
            if patterns:
                print(f"   - {pattern_type}: {len(patterns)} patterns")
                
        return patterns_by_type
        
    def _should_skip_file(self, file_path: Path) -> bool:
        """Check if file should be skipped during scanning."""
        skip_patterns = [
            "__pycache__",
            ".git",
            "venv",
            "env",
            "node_modules",
            "*.pyc",
            "config_core.py",  # Skip the core system itself
            "config_consolidator.py"  # Skip this consolidator
        ]
        
        for pattern in skip_patterns:
            if pattern in str(file_path):
                return True
        return False
        
    def consolidate_patterns(self) -> Dict[str, Any]:
        """Consolidate found patterns into the centralized system."""
        print("🔧 Consolidating configuration patterns...")
        
        consolidation_results = {
            "consolidated_patterns": 0,
            "migrated_files": 0,
            "new_config_keys": 0,
            "errors": []
        }
        
        # Group patterns by file for migration
        patterns_by_file = {}
        for pattern in self.patterns:
            if pattern.file_path not in patterns_by_file:
                patterns_by_file[pattern.file_path] = []
            patterns_by_file[pattern.file_path].append(pattern)
            
        # Consolidate patterns into centralized system
        for pattern in self.patterns:
            try:
                if not self.config_manager.has_config(pattern.key):
                    self.config_manager.set_config(
                        pattern.key,
                        pattern.value,
                        ConfigSource.FILE,
                        f"Consolidated from {pattern.file_path.name}:{pattern.line_number}"
                    )
                    consolidation_results["new_config_keys"] += 1
                    
                consolidation_results["consolidated_patterns"] += 1
                
            except Exception as e:
                consolidation_results["errors"].append(f"Error consolidating {pattern.key}: {e}")
                
        # Migrate files to use centralized configuration
        for file_path, patterns in patterns_by_file.items():
            try:
                if self.migrator.migrate_file_to_centralized(file_path, patterns):
                    consolidation_results["migrated_files"] += 1
            except Exception as e:
                consolidation_results["errors"].append(f"Error migrating {file_path}: {e}")
                
        print(f"✅ Consolidated {consolidation_results['consolidated_patterns']} patterns")
        print(f"✅ Migrated {consolidation_results['migrated_files']} files")
        print(f"✅ Added {consolidation_results['new_config_keys']} new config keys")
        
        if consolidation_results["errors"]:
            print(f"⚠️  {len(consolidation_results['errors'])} errors encountered")
            
        return consolidation_results


def run_configuration_consolidation(root_dir: Path = None) -> Dict[str, Any]:
    """Run the complete configuration consolidation process."""
    if root_dir is None:
        root_dir = Path(__file__).resolve().parents[2]
        
    consolidator = ConfigurationConsolidator()
    
    # Scan for patterns
    patterns = consolidator.scan_configuration_patterns(root_dir)
    
    # Consolidate patterns
    results = consolidator.consolidate_patterns()
    
    # Generate report
    report = consolidator.report_generator.generate_consolidation_report(
        consolidator.patterns,
        results["consolidated_patterns"],
        consolidator.migrator.migrated_files
    )
    
    # Save report
    report_path = root_dir / "configuration_consolidation_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
        
    results["report_path"] = str(report_path)
    results["report_content"] = report
    
    return results


if __name__ == "__main__":
    results = run_configuration_consolidation()
    print(f"\n📊 Configuration consolidation complete!")
    print(f"📄 Report saved to: {results['report_path']}")

