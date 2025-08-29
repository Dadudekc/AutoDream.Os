#!/usr/bin/env python3
"""
Configuration Migration Script
Updates existing configuration imports to use the new unified configuration system.
Eliminates SSOT violations by consolidating scattered configuration imports.

Author: Agent-8 (Integration Enhancement Manager)
Contract: SSOT-003: Configuration Management Consolidation (350 pts)
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple, Any
import logging

class ConfigurationMigrator:
    """Migrate existing configuration imports to unified system"""
    
    def __init__(self, repo_root: str = "."):
        self.repo_root = Path(repo_root)
        self.migration_log = []
        self.files_updated = 0
        self.imports_updated = 0
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def scan_for_config_imports(self) -> List[Tuple[Path, List[str]]]:
        """Scan repository for configuration imports"""
        config_imports = []
        
        # Common configuration import patterns
        import_patterns = [
            r'from\s+(\w+\.)*config\s+import',
            r'from\s+(\w+\.)*constants\s+import',
            r'from\s+(\w+\.)*settings\s+import',
            r'from\s+(\w+\.)*agent_config\s+import',
            r'from\s+(\w+\.)*logging_config\s+import',
            r'import\s+(\w+\.)*config',
            r'import\s+(\w+\.)*constants',
            r'import\s+(\w+\.)*settings',
        ]
        
        # Scan Python files
        for py_file in self.repo_root.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                imports = []
                for pattern in import_patterns:
                    matches = re.findall(pattern, content)
                    if matches:
                        imports.extend(matches)
                
                if imports:
                    config_imports.append((py_file, imports))
                    
            except Exception as e:
                self.logger.warning(f"Error reading {py_file}: {e}")
        
        return config_imports
    
    def create_backup(self, file_path: Path) -> bool:
        """Create backup of original file"""
        try:
            backup_path = file_path.with_suffix(f"{file_path.suffix}.backup")
            shutil.copy2(file_path, backup_path)
            self.logger.info(f"Backup created: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating backup for {file_path}: {e}")
            return False
    
    def migrate_config_imports(self, file_path: Path) -> bool:
        """Migrate configuration imports in a single file"""
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            updated = False
            
            # Migration patterns
            migrations = [
                # Old imports to new unified imports
                (r'from\s+(\w+\.)*config\s+import\s+(\w+)', 
                 r'from config.unified_config import \2'),
                (r'from\s+(\w+\.)*constants\s+import\s+(\w+)', 
                 r'from config.unified_config import get_config'),
                (r'from\s+(\w+\.)*settings\s+import\s+(\w+)', 
                 r'from config.unified_config import get_config'),
                (r'from\s+(\w+\.)*agent_config\s+import\s+(\w+)', 
                 r'from config.unified_config import get_config'),
                (r'from\s+(\w+\.)*logging_config\s+import\s+(\w+)', 
                 r'from config.unified_config import get_config'),
                
                # Direct imports
                (r'import\s+(\w+\.)*config', 
                 r'from config.unified_config import config_manager'),
                (r'import\s+(\w+\.)*constants', 
                 r'from config.unified_config import get_config'),
                (r'import\s+(\w+\.)*settings', 
                 r'from config.unified_config import get_config'),
            ]
            
            # Apply migrations
            for old_pattern, new_pattern in migrations:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    updated = True
            
            # Update configuration access patterns
            # Replace direct attribute access with get_config calls
            config_access_patterns = [
                (r'(\w+)\.(\w+)', r'get_config("\1.\2")'),
                (r'(\w+)\.(\w+)\.(\w+)', r'get_config("\1.\2.\3")'),
            ]
            
            for old_pattern, new_pattern in config_access_patterns:
                if re.search(old_pattern, content):
                    content = re.sub(old_pattern, new_pattern, content)
                    updated = True
            
            # Write updated content if changes were made
            if updated and content != original_content:
                # Create backup first
                if self.create_backup(file_path):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    self.files_updated += 1
                    self.imports_updated += 1
                    self.logger.info(f"Updated {file_path}")
                    
                    # Log migration details
                    self.migration_log.append({
                        'file': str(file_path),
                        'status': 'updated',
                        'changes': 'configuration imports migrated'
                    })
                    return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error migrating {file_path}: {e}")
            self.migration_log.append({
                'file': str(file_path),
                'status': 'error',
                'error': str(e)
            })
            return False
    
    def migrate_all_files(self) -> Dict[str, Any]:
        """Migrate configuration imports in all files"""
        self.logger.info("Starting configuration migration...")
        
        # Scan for configuration imports
        config_imports = self.scan_for_config_imports()
        self.logger.info(f"Found {len(config_imports)} files with configuration imports")
        
        # Migrate each file
        for file_path, imports in config_imports:
            self.logger.info(f"Processing {file_path} with imports: {imports}")
            self.migrate_config_imports(file_path)
        
        # Generate migration report
        report = {
            'total_files_scanned': len(config_imports),
            'files_updated': self.files_updated,
            'imports_updated': self.imports_updated,
            'migration_log': self.migration_log,
            'status': 'completed'
        }
        
        self.logger.info(f"Migration completed. Updated {self.files_updated} files.")
        return report
    
    def generate_migration_report(self, report: Dict[str, Any]) -> str:
        """Generate human-readable migration report"""
        report_text = f"""
# Configuration Migration Report

## Summary
- **Total Files Scanned**: {report['total_files_scanned']}
- **Files Updated**: {report['files_updated']}
- **Imports Updated**: {report['imports_updated']}
- **Status**: {report['status']}

## Migration Details
"""
        
        for log_entry in report['migration_log']:
            report_text += f"- **{log_entry['file']}**: {log_entry['status']}"
            if 'changes' in log_entry:
                report_text += f" - {log_entry['changes']}"
            if 'error' in log_entry:
                report_text += f" - ERROR: {log_entry['error']}"
            report_text += "\n"
        
        return report_text
    
    def rollback_migration(self) -> bool:
        """Rollback migration by restoring backup files"""
        try:
            backup_files = list(self.repo_root.rglob("*.backup"))
            restored_count = 0
            
            for backup_file in backup_files:
                original_file = backup_file.with_suffix('')
                if backup_file.exists():
                    shutil.copy2(backup_file, original_file)
                    backup_file.unlink()  # Remove backup
                    restored_count += 1
            
            self.logger.info(f"Rollback completed. Restored {restored_count} files.")
            return True
            
        except Exception as e:
            self.logger.error(f"Error during rollback: {e}")
            return False

def main():
    """Main migration function"""
    print("=== Configuration Migration Script ===")
    print("This script will migrate existing configuration imports to the unified system.")
    print("A backup will be created for each file before making changes.")
    
    # Confirm migration
    response = input("\nDo you want to proceed with the migration? (y/N): ")
    if response.lower() != 'y':
        print("Migration cancelled.")
        return
    
    # Initialize migrator
    migrator = ConfigurationMigrator()
    
    try:
        # Perform migration
        report = migrator.migrate_all_files()
        
        # Generate and save report
        report_text = migrator.generate_migration_report(report)
        report_file = Path("configuration_migration_report.md")
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_text)
        
        print(f"\nMigration completed successfully!")
        print(f"Report saved to: {report_file}")
        print(f"Updated {report['files_updated']} files")
        
        # Offer rollback option
        if report['files_updated'] > 0:
            response = input("\nDo you want to rollback the migration? (y/N): ")
            if response.lower() == 'y':
                if migrator.rollback_migration():
                    print("Rollback completed successfully.")
                else:
                    print("Rollback failed. Check logs for details.")
        
    except Exception as e:
        print(f"Migration failed: {e}")
        logging.error(f"Migration error: {e}")

if __name__ == "__main__":
    main()
