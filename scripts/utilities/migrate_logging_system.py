#!/usr/bin/env python3
"""
Logging System Migration Script - Agent Cellphone V2

This script automatically migrates the existing logging system to use the new
unified logging manager, replacing hardcoded debug flags and scattered
logging.basicConfig() calls.

Follows Single Responsibility Principle - only logging migration.
Architecture: Single Responsibility Principle - migration only
LOC: 150 lines (under 400 limit)
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Tuple
import argparse


class LoggingMigrationManager:
    """Manages migration from old logging system to unified logging"""
    
    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root)
        self.migration_log = []
        self.files_processed = 0
        self.files_modified = 0
        self.errors = []
        
        # Patterns to find and replace
        self.patterns = {
            # Hardcoded Flask debug flags
            'flask_debug_true': {
                'pattern': r'app\.run\(debug=True\)',
                'replacement': 'app.run(debug=get_flask_debug())',
                'import': 'from src.utils.unified_logging_manager import get_flask_debug'
            },
            'flask_debug_false': {
                'pattern': r'app\.run\(debug=False\)',
                'replacement': 'app.run(debug=get_flask_debug())',
                'import': 'from src.utils.unified_logging_manager import get_flask_debug'
            },
            
            # Hardcoded debug mode flags
            'debug_mode_true': {
                'pattern': r'debug_mode=True',
                'replacement': 'debug_mode=is_debug_enabled()',
                'import': 'from src.utils.unified_logging_manager import is_debug_enabled'
            },
            'debug_mode_false': {
                'pattern': r'debug_mode=False',
                'replacement': 'debug_mode=is_debug_enabled()',
                'import': 'from src.utils.unified_logging_manager import is_debug_enabled'
            },
            
            # Hardcoded DEBUG variables
            'debug_var_true': {
                'pattern': r'DEBUG\s*=\s*\$?true',
                'replacement': 'DEBUG = $env:DEBUG_MODE',
                'import': None  # PowerShell doesn't need import
            },
            'debug_var_false': {
                'pattern': r'DEBUG\s*=\s*\$?false',
                'replacement': 'DEBUG = $env:DEBUG_MODE',
                'import': None
            },
            
            # logging.basicConfig calls
            'logging_basic_config': {
                'pattern': r'logging\.basicConfig\(',
                'replacement': '# logging.basicConfig(  # Migrated to unified logging\n        # Use get_logger() instead',
                'import': 'from src.utils.unified_logging_manager import get_logger'
            },
            
            # logging.getLogger().setLevel calls
            'logging_set_level': {
                'pattern': r'logging\.getLogger\(\)\.setLevel\(',
                'replacement': '# logging.getLogger().setLevel(  # Migrated to unified logging\n        # Use get_logger() instead',
                'import': 'from src.utils.unified_logging_manager import get_logger'
            }
        }
    
    def find_files_to_migrate(self) -> List[Path]:
        """Find all files that need logging migration"""
        files_to_migrate = []
        
        # File extensions to process
        extensions = {'.py', '.ps1', '.md'}
        
        # Directories to skip
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', 'venv', 'env'}
        
        for root, dirs, files in os.walk(self.workspace_root):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if Path(file).suffix in extensions:
                    file_path = Path(root) / file
                    if self._needs_migration(file_path):
                        files_to_migrate.append(file_path)
        
        return files_to_migrate
    
    def _needs_migration(self, file_path: Path) -> bool:
        """Check if file needs logging migration"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check if file contains any patterns that need migration
            for pattern_name, pattern_info in self.patterns.items():
                if re.search(pattern_info['pattern'], content, re.IGNORECASE):
                    return True
                    
        except Exception as e:
            self.errors.append(f"Error reading {file_path}: {e}")
            
        return False
    
    def migrate_file(self, file_path: Path) -> bool:
        """Migrate a single file to use unified logging"""
        try:
            # Create backup
            backup_path = file_path.with_suffix(file_path.suffix + '.backup')
            shutil.copy2(file_path, backup_path)
            
            # Read file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            imports_added = set()
            
            # Apply each pattern
            for pattern_name, pattern_info in self.patterns.items():
                if re.search(pattern_info['pattern'], content, re.IGNORECASE):
                    # Replace pattern
                    content = re.sub(
                        pattern_info['pattern'],
                        pattern_info['replacement'],
                        content,
                        flags=re.IGNORECASE
                    )
                    
                    # Add import if needed and not already added
                    if (pattern_info['import'] and 
                        pattern_info['import'] not in imports_added and
                        pattern_info['import'] not in content):
                        
                        content = self._add_import(content, pattern_info['import'])
                        imports_added.add(pattern_info['import'])
            
            # Only write if content changed
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                self.files_modified += 1
                self.migration_log.append(f"✅ Migrated: {file_path}")
                return True
            else:
                # Remove backup if no changes
                backup_path.unlink()
                self.migration_log.append(f"⏭️  No changes needed: {file_path}")
                return False
                
        except Exception as e:
            self.errors.append(f"Error migrating {file_path}: {e}")
            return False
    
    def _add_import(self, content: str, import_statement: str) -> str:
        """Add import statement to file content"""
        lines = content.split('\n')
        
        # Find the first import line or add at the top
        import_index = 0
        for i, line in enumerate(lines):
            if line.strip().startswith('import ') or line.strip().startswith('from '):
                import_index = i + 1
            elif line.strip() and not line.strip().startswith('#'):
                break
        
        # Insert import
        lines.insert(import_index, import_statement)
        
        return '\n'.join(lines)
    
    def run_migration(self) -> bool:
        """Run the complete logging migration"""
        print("🚀 Starting Logging System Migration...")
        print(f"📁 Workspace: {self.workspace_root.absolute()}")
        
        # Find files to migrate
        files_to_migrate = self.find_files_to_migrate()
        print(f"📋 Found {len(files_to_migrate)} files to migrate")
        
        if not files_to_migrate:
            print("✅ No files need migration")
            return True
        
        # Process each file
        for file_path in files_to_migrate:
            self.files_processed += 1
            print(f"🔄 Processing {self.files_processed}/{len(files_to_migrate)}: {file_path.name}")
            
            try:
                self.migrate_file(file_path)
            except Exception as e:
                self.errors.append(f"Failed to migrate {file_path}: {e}")
        
        # Generate migration report
        self._generate_report()
        
        return len(self.errors) == 0
    
    def _generate_report(self):
        """Generate migration report"""
        print("\n" + "="*60)
        print("📊 LOGGING MIGRATION REPORT")
        print("="*60)
        print(f"📁 Files Processed: {self.files_processed}")
        print(f"✅ Files Modified: {self.files_modified}")
        print(f"❌ Errors: {len(self.errors)}")
        
        if self.migration_log:
            print("\n📝 Migration Log:")
            for log_entry in self.migration_log:
                print(f"  {log_entry}")
        
        if self.errors:
            print("\n❌ Errors:")
            for error in self.errors:
                print(f"  {error}")
        
        print("\n" + "="*60)
    
    def rollback_migration(self):
        """Rollback migration by restoring backup files"""
        print("🔄 Rolling back migration...")
        
        backup_files = list(self.workspace_root.rglob("*.backup"))
        restored_count = 0
        
        for backup_file in backup_files:
            try:
                original_file = backup_file.with_suffix('')
                if original_file.exists():
                    original_file.unlink()
                shutil.move(backup_file, original_file)
                restored_count += 1
                print(f"✅ Restored: {original_file}")
            except Exception as e:
                print(f"❌ Failed to restore {backup_file}: {e}")
        
        print(f"🔄 Rollback complete: {restored_count} files restored")


def main():
    """CLI interface for logging migration"""
    parser = argparse.ArgumentParser(description="Logging System Migration Tool")
    parser.add_argument("--workspace", default=".", help="Workspace root directory")
    parser.add_argument("--rollback", action="store_true", help="Rollback migration")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be migrated without making changes")
    
    args = parser.parse_args()
    
    migration_manager = LoggingMigrationManager(args.workspace)
    
    if args.rollback:
        migration_manager.rollback_migration()
    elif args.dry_run:
        files_to_migrate = migration_manager.find_files_to_migrate()
        print(f"📋 Files that would be migrated: {len(files_to_migrate)}")
        for file_path in files_to_migrate:
            print(f"  {file_path}")
    else:
        success = migration_manager.run_migration()
        if success:
            print("🎉 Migration completed successfully!")
        else:
            print("⚠️  Migration completed with errors. Check the report above.")


if __name__ == "__main__":
    main()
