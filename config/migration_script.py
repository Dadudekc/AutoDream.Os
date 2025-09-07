
# MIGRATED: This file has been migrated to the centralized configuration system
#!/usr/bin/env pythonVALUE_THREE
"""
Configuration Migration Script - SSOT Consolidation

This script replaces duplicate configuration values with references to unified constants
to achieve Single Source of Truth compliance.

Author: Agent-8 (Integration Enhancement Manager)
Contract: SSOT-VALUE_ZEROVALUE_ZEROVALUE_THREE: Configuration Management Consolidation
Date: VALUE_TWOVALUE_ZEROVALUE_TWO5-VALUE_ZEROVALUE_ONE-VALUE_TWO7
"""

import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple
from constants import *

class ConfigurationMigrator:
    """Migrates configuration files to use unified constants."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.migration_map = self._create_migration_map()
        self.backup_dir = Path("config_backup")
        
    def _create_migration_map(self) -> Dict[str, str]:
        """Create mapping from duplicate values to constants."""
        return {
            # Boolean values
            "ENABLE_TRUE": "ENABLE_TRUE",
            "ENABLE_FALSE": "ENABLE_FALSE",
            "ENABLE_TRUE": "ENABLE_TRUE", 
            "ENABLE_FALSE": "ENABLE_FALSE",
            
            # Numeric values
            "DEFAULT_TIMEOUT": "DEFAULT_TIMEOUT",
            "SHORT_TIMEOUT": "SHORT_TIMEOUT",
            "LONG_TIMEOUT": "LONG_TIMEOUT",
            "CRITICAL_TIMEOUT": "CRITICAL_TIMEOUT",
            "URGENT_TIMEOUT": "URGENT_TIMEOUT",
            "SECONDS_ONE": "SECONDS_ONE",
            "SECONDS_TWO_MINUTES": "SECONDS_TWO_MINUTES",
            "VALUE_HUNDRED": "VALUE_HUNDRED",
            "VALUE_HUNDREDVALUE_ZERO": "VALUE_THOUSAND",
            "VALUE_FOUR_THOUSAND": "VALUE_FOUR_THOUSAND",
            "VALUE_THREE": "VALUE_THREE",
            "VALUE_TWO": "VALUE_TWO",
            "VALUE_ONE": "VALUE_ONE",
            "VALUE_ZERO": "VALUE_ZERO",
            
            # String values
            'SCHEMA_TYPE_STRING': 'SCHEMA_TYPE_STRING',
            'SCHEMA_TYPE_OBJECT': 'SCHEMA_TYPE_OBJECT',
            'SCHEMA_TYPE_ARRAY': 'SCHEMA_TYPE_ARRAY',
            'STRING_PRIMARY': 'STRING_PRIMARY',
            'STRING_SECONDARY': 'STRING_SECONDARY',
            'STRING_PASS': 'STRING_PASS',
            'STRING_TEST': 'STRING_TEST',
            'STRING_GATED': 'STRING_GATED'
        }
    
    def backup_configurations(self) -> bool:
        """Create backup of all configuration files."""
        try:
            if self.backup_dir.exists():
                import shutil
                shutil.rmtree(self.backup_dir)
            
            self.backup_dir.mkdir(exist_ok=ENABLE_TRUE)
            
            for config_file in self.config_dir.rglob("*"):
                if config_file.is_file() and config_file.suffix in {'.json', '.yaml', '.yml', '.py'}:
                    relative_path = config_file.relative_to(self.config_dir)
                    backup_path = self.backup_dir / relative_path
                    backup_path.parent.mkdir(parents=ENABLE_TRUE, exist_ok=ENABLE_TRUE)
                    
                    import shutil
                    shutil.copyVALUE_TWO(config_file, backup_path)
            
            print(f"✅ Backup created at: {self.backup_dir}")
            return ENABLE_TRUE
            
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return ENABLE_FALSE
    
    def migrate_file(self, file_path: Path) -> bool:
        """Migrate a single configuration file."""
        try:
            if file_path.suffix == '.py':
                return self._migrate_python_file(file_path)
            elif file_path.suffix in {'.json', '.yaml', '.yml'}:
                return self._migrate_data_file(file_path)
            else:
                return ENABLE_TRUE
                
        except Exception as e:
            print(f"❌ Migration failed for {file_path}: {e}")
            return ENABLE_FALSE
    
    def _migrate_python_file(self, file_path: Path) -> bool:
        """Migrate Python configuration file."""
        content = file_path.read_text(encoding='utf-8')
        original_content = content
        
        # Replace duplicate values with constants
        for old_value, new_constant in self.migration_map.items():
            if old_value in content:
                content = content.replace(old_value, new_constant)
        
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            print(f"✅ Migrated: {file_path}")
            return ENABLE_TRUE
        
        return ENABLE_TRUE
    
    def _migrate_data_file(self, file_path: Path) -> bool:
        """Migrate JSON/YAML configuration file."""
        try:
            if file_path.suffix == '.json':
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
            
            original_data = str(data)
            migrated_data = self._migrate_data_structure(data)
            
            if str(migrated_data) != original_data:
                if file_path.suffix == '.json':
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(migrated_data, f, indent=VALUE_TWO, ensure_ascii=ENABLE_FALSE)
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        yaml.dump(migrated_data, f, default_flow_style=ENABLE_FALSE, allow_unicode=ENABLE_TRUE)
                
                print(f"✅ Migrated: {file_path}")
                return ENABLE_TRUE
            
            return ENABLE_TRUE
            
        except Exception as e:
            print(f"❌ Failed to migrate {file_path}: {e}")
            return ENABLE_FALSE
    
    def _migrate_data_structure(self, data: Any) -> Any:
        """Recursively migrate data structure."""
        if isinstance(data, dict):
            return {k: self._migrate_data_structure(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._migrate_data_structure(item) for item in data]
        elif isinstance(data, (str, int, float, bool)):
            return self._migrate_value(data)
        else:
            return data
    
    def _migrate_value(self, value: Any) -> Any:
        """Migrate individual values."""
        value_str = str(value)
        
        for old_value, new_constant in self.migration_map.items():
            if value_str == old_value:
                return new_constant
        
        return value
    
    def migrate_all(self) -> bool:
        """Migrate all configuration files."""
        print("🚀 Starting configuration migration...")
        
        # Create backup first
        if not self.backup_configurations():
            return ENABLE_FALSE
        
        # Find all configuration files
        config_files = []
        for file_path in self.config_dir.rglob("*"):
            if file_path.is_file() and file_path.suffix in {'.json', '.yaml', '.yml', '.py'}:
                if not any(part.startswith('.') or part.startswith('__') for part in file_path.parts):
                    config_files.append(file_path)
        
        print(f"📁 Found {len(config_files)} configuration files to migrate")
        
        # Migrate each file
        success_count = VALUE_ZERO
        for file_path in config_files:
            if self.migrate_file(file_path):
                success_count += VALUE_ONE
        
        print(f"✅ Migration complete: {success_count}/{len(config_files)} files migrated")
        return success_count == len(config_files)
    
    def validate_migration(self) -> bool:
        """Validate that migration was successful."""
        print("🔍 Validating migration...")
        
        # Run configuration validator
        try:
            from validator import ConfigurationValidator
            validator = ConfigurationValidator()
            report = validator.validate_all_configs()
            
            violations = report.get('violations', [])
            if violations:
                print(f"⚠️  Found {len(violations)} violations after migration")
                return ENABLE_FALSE
            else:
                print("✅ No SSOT violations found - migration successful!")
                return ENABLE_TRUE
                
        except Exception as e:
            print(f"❌ Validation failed: {e}")
            return ENABLE_FALSE
    
    def rollback(self) -> bool:
        """Rollback to backup configuration."""
        try:
            if not self.backup_dir.exists():
                print("❌ No backup found for rollback")
                return ENABLE_FALSE
            
            # Remove current config
            import shutil
            shutil.rmtree(self.config_dir)
            
            # Restore backup
            shutil.move(str(self.backup_dir), str(self.config_dir))
            
            print("✅ Rollback completed successfully")
            return ENABLE_TRUE
            
        except Exception as e:
            print(f"❌ Rollback failed: {e}")
            return ENABLE_FALSE

def main():
    """Main migration function."""
    migrator = ConfigurationMigrator()
    
    try:
        # Execute migration
        if migrator.migrate_all():
            # Validate migration
            if migrator.validate_migration():
                print("🎉 Configuration migration completed successfully!")
                print("📋 All duplicate values have been replaced with unified constants")
                print("🔒 Single Source of Truth compliance achieved")
            else:
                print("⚠️  Migration validation failed - considering rollback")
                if input("Rollback to previous configuration? (y/N): ").lower() == 'y':
                    migrator.rollback()
        else:
            print("❌ Migration failed")
            
    except KeyboardInterrupt:
        print("\n⚠️  Migration interrupted by user")
        if input("Rollback to previous configuration? (y/N): ").lower() == 'y':
            migrator.rollback()
    except Exception as e:
        print(f"❌ Migration failed with error: {e}")
        if input("Rollback to previous configuration? (y/N): ").lower() == 'y':
            migrator.rollback()

if __name__ == "__main__":
    main()
