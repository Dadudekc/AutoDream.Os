#!/usr/bin/env python3
"""
Migration Executor Module - Agent-3 Database Specialist
======================================================

Migration execution and validation functionality
for V2 compliance and modular architecture.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import logging
from datetime import datetime
from typing import Any

from migration_core import MigrationCore
from migration_scripts import MigrationScripts

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MigrationExecutor:
    """Migration execution and validation functionality."""

    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize the migration executor."""
        self.core = MigrationCore(db_path)
        self.scripts = MigrationScripts()
        self.execution_results = {
            "scripts_executed": 0,
            "scripts_failed": 0,
            "execution_time": 0,
            "validation_passed": False,
        }

    def execute_all_migrations(self) -> dict[str, Any]:
        """Execute all migration scripts."""
        logger.info("🚀 Starting migration execution...")

        start_time = datetime.now()

        try:
            # Create database connection
            if not self.core.create_database_connection():
                return {"success": False, "error": "Failed to create database connection"}

            # Create backup before migration
            backup_path = f"backups/pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            if not self.core.create_backup(backup_path):
                logger.warning("⚠️ Backup creation failed, continuing with migration")

            # Execute table creation scripts
            table_scripts = self.scripts.get_all_migration_scripts()
            for script_name, script_content in table_scripts.items():
                result = self.core.execute_migration_script(script_content)
                if result["success"]:
                    self.execution_results["scripts_executed"] += 1
                    logger.info(f"✅ Executed: {script_name}")
                else:
                    self.execution_results["scripts_failed"] += 1
                    logger.error(f"❌ Failed: {script_name} - {result['error']}")

            # Execute performance indexes script
            indexes_script = self.scripts.create_performance_indexes_script()
            result = self.core.execute_migration_script(indexes_script)
            if result["success"]:
                self.execution_results["scripts_executed"] += 1
                logger.info("✅ Executed: performance indexes")
            else:
                self.execution_results["scripts_failed"] += 1
                logger.error(f"❌ Failed: performance indexes - {result['error']}")

            # Execute views script
            views_script = self.scripts.create_useful_views_script()
            result = self.core.execute_migration_script(views_script)
            if result["success"]:
                self.execution_results["scripts_executed"] += 1
                logger.info("✅ Executed: useful views")
            else:
                self.execution_results["scripts_failed"] += 1
                logger.error(f"❌ Failed: useful views - {result['error']}")

            # Validate database integrity
            validation_result = self.core.validate_database_integrity()
            self.execution_results["validation_passed"] = validation_result["success"]

            # Calculate execution time
            end_time = datetime.now()
            self.execution_results["execution_time"] = (end_time - start_time).total_seconds()

            # Close database connection
            self.core.close_database_connection()

            # Generate execution summary
            execution_summary = self._generate_execution_summary()

            logger.info("✅ Migration execution completed!")
            return {
                "success": True,
                "execution_results": self.execution_results,
                "validation_result": validation_result,
                "execution_summary": execution_summary,
                "migration_results": self.core.get_migration_results(),
            }

        except Exception as e:
            logger.error(f"❌ Migration execution failed: {e}")
            self.core.close_database_connection()
            return {"success": False, "error": str(e)}

    def _generate_execution_summary(self) -> dict[str, Any]:
        """Generate execution summary."""
        total_scripts = (
            self.execution_results["scripts_executed"] + self.execution_results["scripts_failed"]
        )
        success_rate = (self.execution_results["scripts_executed"] / max(1, total_scripts)) * 100

        return {
            "total_scripts": total_scripts,
            "scripts_executed": self.execution_results["scripts_executed"],
            "scripts_failed": self.execution_results["scripts_failed"],
            "success_rate": success_rate,
            "execution_time_seconds": self.execution_results["execution_time"],
            "validation_passed": self.execution_results["validation_passed"],
            "execution_status": "completed" if success_rate >= 90 else "partial_failure",
        }

    def validate_migration_results(self) -> dict[str, Any]:
        """Validate migration results."""
        logger.info("🔍 Validating migration results...")

        try:
            if not self.core.create_database_connection():
                return {"success": False, "error": "Failed to create database connection"}

            # Check if all tables exist
            cursor = self.core.connection.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN (
                    'agent_workspaces', 'agent_messages', 'discord_commands',
                    'v2_compliance_audit', 'integration_tests', 'core_systems_status'
                )
            """
            )
            existing_tables = [row[0] for row in cursor.fetchall()]

            # Check if indexes exist
            cursor = self.core.connection.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='index' AND name LIKE 'idx_%'
            """
            )
            existing_indexes = [row[0] for row in cursor.fetchall()]

            # Check if views exist
            cursor = self.core.connection.execute(
                """
                SELECT name FROM sqlite_master 
                WHERE type='view' AND name IN (
                    'active_agents', 'recent_messages', 'compliance_summary', 'system_health_overview'
                )
            """
            )
            existing_views = [row[0] for row in cursor.fetchall()]

            validation_result = {
                "success": True,
                "tables_created": len(existing_tables),
                "expected_tables": 6,
                "indexes_created": len(existing_indexes),
                "views_created": len(existing_views),
                "expected_views": 4,
                "table_completeness": (len(existing_tables) / 6) * 100,
                "index_completeness": (len(existing_indexes) / 15) * 100,
                "view_completeness": (len(existing_views) / 4) * 100,
            }

            self.core.close_database_connection()

            logger.info("✅ Migration validation completed")
            return validation_result

        except Exception as e:
            logger.error(f"❌ Migration validation failed: {e}")
            self.core.close_database_connection()
            return {"success": False, "error": str(e)}
