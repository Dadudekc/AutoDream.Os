#!/usr/bin/env python3
"""
Automated Migration Scripts V2
===============================

V2 compliant version of automated migration scripts.
Modular architecture with clean separation of concerns.

Usage:
    python automated_migration_scripts_v2.py [--db-path PATH] [--backup-dir DIR]
"""

import argparse
import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from migration_system import (
    MigrationController,
    BackupManager,
    DataValidator,
    SchemaManager,
    DataMigrator,
    IntegrationTester
)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """Main function for automated migration scripts."""
    parser = argparse.ArgumentParser(description="Automated Migration Scripts V2")
    parser.add_argument("--db-path", default="data/agent_system.db", help="Database file path")
    parser.add_argument("--backup-dir", default="backups/migration", help="Backup directory")
    parser.add_argument("--dry-run", action="store_true", help="Run in dry-run mode (no actual changes)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    print("🚀 V2_SWARM Automated Migration Scripts V2")
    print("=" * 50)
    
    try:
        # Initialize migration controller
        controller = MigrationController(
            db_path=args.db_path,
            backup_dir=args.backup_dir
        )
        
        if args.dry_run:
            print("🔍 DRY RUN MODE - No actual changes will be made")
            # Show migration status
            status = controller.get_migration_status()
            print(f"Database path: {status['database_path']}")
            print(f"Backup directory: {status['backup_directory']}")
            print(f"Database exists: {status['database_exists']}")
            print("✅ Dry run completed successfully")
            return 0
        
        # Run complete migration
        print("🔄 Starting complete migration process...")
        results = controller.run_complete_migration()
        
        # Display results
        print("\n📊 Migration Results:")
        print(f"Success: {results['success']}")
        print(f"Steps completed: {len(results['steps_completed'])}")
        print(f"Errors: {len(results['errors'])}")
        print(f"Warnings: {len(results['warnings'])}")
        
        if results['errors']:
            print("\n❌ Errors:")
            for error in results['errors']:
                print(f"  - {error}")
        
        if results['warnings']:
            print("\n⚠️  Warnings:")
            for warning in results['warnings']:
                print(f"  - {warning}")
        
        if results['success']:
            print("\n✅ Migration completed successfully!")
            return 0
        else:
            print("\n❌ Migration failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️  Migration cancelled by user")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


