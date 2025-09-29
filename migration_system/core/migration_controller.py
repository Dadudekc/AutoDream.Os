#!/usr/bin/env python3
"""
Migration Controller
====================

Main controller for automated database migration.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any

from ..backup.backup_manager import BackupManager
from ..data.data_migrator import DataMigrator
from ..schema.schema_manager import SchemaManager
from ..testing.integration_tester import IntegrationTester
from ..validation.data_validator import DataValidator

logger = logging.getLogger(__name__)


class MigrationController:
    """Main controller for automated database migration."""

    def __init__(
        self, db_path: str = "data/agent_system.db", backup_dir: str = "backups/migration"
    ):
        """Initialize the migration controller."""
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)

        # Initialize components
        self.backup_manager = BackupManager(self.db_path, self.backup_dir)
        self.data_validator = DataValidator(self.db_path)
        self.schema_manager = SchemaManager(self.db_path)
        self.data_migrator = DataMigrator(self.db_path)
        self.integration_tester = IntegrationTester(self.db_path)

    def run_complete_migration(self) -> dict[str, Any]:
        """Run complete migration process with validation."""
        migration_results = {
            "start_time": datetime.now().isoformat(),
            "steps_completed": [],
            "errors": [],
            "warnings": [],
            "success": False,
        }

        try:
            # Step 1: Create backup
            logger.info("🔄 Step 1: Creating data backup...")
            backup_result = self.backup_manager.create_migration_backup()
            migration_results["steps_completed"].append("backup_creation")
            if not backup_result["success"]:
                migration_results["errors"].append(f"Backup failed: {backup_result['error']}")
                return migration_results

            # Step 2: Validate existing data
            logger.info("🔍 Step 2: Validating existing data...")
            validation_result = self.data_validator.validate_existing_data()
            migration_results["steps_completed"].append("data_validation")
            if not validation_result["success"]:
                migration_results["warnings"].append(
                    f"Data validation issues: {validation_result['issues']}"
                )

            # Step 3: Create database schema
            logger.info("🏗️ Step 3: Creating database schema...")
            schema_result = self.schema_manager.create_database_schema()
            migration_results["steps_completed"].append("schema_creation")
            if not schema_result["success"]:
                migration_results["errors"].append(
                    f"Schema creation failed: {schema_result['error']}"
                )
                return migration_results

            # Step 4: Migrate data
            logger.info("📦 Step 4: Migrating data...")
            migration_result = self.data_migrator.migrate_data()
            migration_results["steps_completed"].append("data_migration")
            if not migration_result["success"]:
                migration_results["errors"].append(
                    f"Data migration failed: {migration_result['error']}"
                )
                return migration_results

            # Step 5: Validate migration
            logger.info("✅ Step 5: Validating migration...")
            validation_result = self.data_validator.validate_migration()
            migration_results["steps_completed"].append("migration_validation")
            if not validation_result["success"]:
                migration_results["errors"].append(
                    f"Migration validation failed: {validation_result['error']}"
                )
                return migration_results

            # Step 6: Run integration tests
            logger.info("🧪 Step 6: Running integration tests...")
            test_result = self.integration_tester.run_integration_tests()
            migration_results["steps_completed"].append("integration_tests")
            if not test_result["success"]:
                migration_results["warnings"].append(
                    f"Integration tests failed: {test_result['error']}"
                )

            # Migration completed successfully
            migration_results["success"] = True
            migration_results["end_time"] = datetime.now().isoformat()
            logger.info("🎉 Migration completed successfully!")

        except Exception as e:
            logger.error(f"Migration failed with exception: {e}")
            migration_results["errors"].append(f"Unexpected error: {str(e)}")
            migration_results["end_time"] = datetime.now().isoformat()

        return migration_results

    def get_migration_status(self) -> dict[str, Any]:
        """Get current migration status."""
        return {
            "database_path": str(self.db_path),
            "backup_directory": str(self.backup_dir),
            "database_exists": self.db_path.exists(),
            "backup_directory_exists": self.backup_dir.exists(),
            "components_initialized": {
                "backup_manager": self.backup_manager is not None,
                "data_validator": self.data_validator is not None,
                "schema_manager": self.schema_manager is not None,
                "data_migrator": self.data_migrator is not None,
                "integration_tester": self.integration_tester is not None,
            },
        }
