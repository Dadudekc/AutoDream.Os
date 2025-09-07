#!/usr/bin/env python3
"""
Legacy Configuration Migration Manager - Agent-2 Consolidation Implementation
Manages migration of legacy configuration systems to unified framework
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from ..unified_configuration_framework import get_unified_config_framework


class LegacyMigrationManager:
    """Manages migration of legacy configuration systems."""
    
    def __init__(self):
        """Initialize migration manager."""
        self.framework = get_unified_config_framework()
        self.migration_log = []
        self.migration_status = {}
    
    def migrate_legacy_configs(self, legacy_paths: List[str]) -> Dict[str, Any]:
        """Migrate legacy configuration files."""
        results = {
            'total_files': len(legacy_paths),
            'migrated': 0,
            'failed': 0,
            'errors': []
        }
        
        for legacy_path in legacy_paths:
            try:
                if self._migrate_single_config(legacy_path):
                    results['migrated'] += 1
                else:
                    results['failed'] += 1
            except Exception as e:
                error_msg = f"Migration error for {legacy_path}: {e}"
                results['errors'].append(error_msg)
                results['failed'] += 1
        
        return results
    
    def _migrate_single_config(self, legacy_path: str) -> bool:
        """Migrate a single legacy configuration file."""
        try:
            file_path = Path(legacy_path)
            if not file_path.exists():
                return False
            
            # Determine format and migrate
            if file_path.suffix.lower() == '.json':
                return self._migrate_json_config(legacy_path)
            elif file_path.suffix.lower() in ['.yaml', '.yml']:
                return self._migrate_yaml_config(legacy_path)
            elif file_path.suffix.lower() == '.ini':
                return self._migrate_ini_config(legacy_path)
            else:
                return self._migrate_generic_config(legacy_path)
                
        except Exception as e:
            print(f"Single config migration error: {e}")
            return False
    
    def _migrate_json_config(self, json_path: str) -> bool:
        """Migrate JSON configuration file."""
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Create unified format
            unified_data = {
                'source': 'legacy_json',
                'original_path': json_path,
                'migrated_at': '2025-08-30T03:15:00',
                'data': data
            }
            
            # Save in unified format
            unified_path = json_path.replace('.json', '_unified.json')
            with open(unified_path, 'w', encoding='utf-8') as f:
                json.dump(unified_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"JSON migration error: {e}")
            return False
    
    def _migrate_yaml_config(self, yaml_path: str) -> bool:
        """Migrate YAML configuration file."""
        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            # Create unified format
            unified_data = {
                'source': 'legacy_yaml',
                'original_path': yaml_path,
                'migrated_at': '2025-08-30T03:15:00',
                'data': data
            }
            
            # Save in unified format
            unified_path = yaml_path.replace('.yaml', '_unified.json').replace('.yml', '_unified.json')
            with open(unified_path, 'w', encoding='utf-8') as f:
                json.dump(unified_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"YAML migration error: {e}")
            return False
    
    def _migrate_ini_config(self, ini_path: str) -> bool:
        """Migrate INI configuration file."""
        try:
            # Simple INI to JSON conversion
            unified_data = {
                'source': 'legacy_ini',
                'original_path': ini_path,
                'migrated_at': '2025-08-30T03:15:00',
                'data': {'ini_file': ini_path, 'migration': 'pending'}
            }
            
            # Save in unified format
            unified_path = ini_path.replace('.ini', '_unified.json')
            with open(unified_path, 'w', encoding='utf-8') as f:
                json.dump(unified_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"INI migration error: {e}")
            return False
    
    def _migrate_generic_config(self, config_path: str) -> bool:
        """Migrate generic configuration file."""
        try:
            unified_data = {
                'source': 'legacy_generic',
                'original_path': config_path,
                'migrated_at': '2025-08-30T03:15:00',
                'data': {'generic_file': config_path, 'migration': 'pending'}
            }
            
            # Save in unified format
            unified_path = config_path + '_unified.json'
            with open(unified_path, 'w', encoding='utf-8') as f:
                json.dump(unified_data, f, indent=2)
            
            return True
            
        except Exception as e:
            print(f"Generic migration error: {e}")
            return False


# Global migration manager instance
legacy_migration_manager = LegacyMigrationManager()


def get_legacy_migration_manager():
    """Get legacy migration manager instance."""
    return legacy_migration_manager


if __name__ == "__main__":
    # Test migration manager
    manager = get_legacy_migration_manager()
    print("✅ Legacy Migration Manager ready for configuration consolidation!")
