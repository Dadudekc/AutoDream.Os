#!/usr/bin/env python3
"""
Configuration File Migrator - Agent Cellphone V2
===============================================

Migrates files to use centralized configuration.

Author: Agent-8 (SSOT Maintenance & System Integration Specialist)
License: MIT
"""

from pathlib import Path
from typing import List

from .config_consolidator import ConfigPattern


class ConfigurationFileMigrator:
    """Migrates files to use centralized configuration."""
    
    def __init__(self):
        self.migrated_files: set[Path] = set()
    
    def migrate_file_to_centralized(self, file_path: Path, patterns: List[ConfigPattern]) -> bool:
        """Migrate a file to use centralized configuration."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Add import if not present
            if 'from src.utils.config_core import get_config' not in content:
                # Find the best place to add the import
                lines = content.split('\n')
                import_section_end = 0
                
                for i, line in enumerate(lines):
                    if line.strip().startswith('import ') or line.strip().startswith('from '):
                        import_section_end = i + 1
                    elif line.strip() and not line.strip().startswith('#'):
                        break
                        
                import_line = "from src.utils.config_core import get_config"
                lines.insert(import_section_end, import_line)
                content = '\n'.join(lines)
                
            # Replace configuration patterns with centralized calls
            for pattern in patterns:
                if pattern.pattern_type in ["hardcoded_values", "config_constants", "settings_patterns"]:
                    # Replace direct assignment with get_config call
                    old_pattern = f"{pattern.key} = {pattern.value}"
                    new_pattern = f"{pattern.key} = get_config('{pattern.key}', {pattern.value})"
                    content = content.replace(old_pattern, new_pattern)
                    
            # Write back the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
                
            self.migrated_files.add(file_path)
            return True
            
        except Exception as e:
            print(f"⚠️  Error migrating {file_path}: {e}")
            return False
    
    def get_migration_summary(self) -> dict[str, any]:
        """Get summary of migration operations."""
        return {
            "total_migrated_files": len(self.migrated_files),
            "migrated_files": list(self.migrated_files)
        }
