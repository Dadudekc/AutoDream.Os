"""
migrate_logging_system_part_5.py
Module: migrate_logging_system_part_5.py
Purpose: Automated documentation compliance
Created: 2025-08-31 00:36:47
"""

# Part 5 of migrate_logging_system.py
# Original file: .\scripts\utilities\migrate_logging_system.py

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

