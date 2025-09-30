#!/usr/bin/env python3
"""
Migration Core Module - Agent-3 Database Specialist
==================================================

Core migration functionality extracted from the main system
for V2 compliance and modular architecture.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import logging
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MigrationCore:
    """Core migration functionality."""

    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize the migration core."""
        self.db_path = Path(db_path)
        self.connection = None
        self.migration_results = {
            "migrations_completed": 0,
            "backups_created": 0,
            "validations_passed": 0,
            "errors_encountered": 0,
        }

    def create_database_connection(self) -> bool:
        """Create database connection."""
        try:
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self.with sqlite3.connect(str(self.db_path) as connection:)
            self.connection.row_factory = sqlite3.Row
            logger.info("✅ Database connection established")
            return True
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            return False

    def close_database_connection(self) -> None:
        """Close database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info("✅ Database connection closed")

    def create_backup(self, backup_path: str) -> bool:
        """Create database backup."""
        try:
            if not self.connection:
                logger.error("❌ No database connection available")
                return False

            backup_path = Path(backup_path)
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Create backup using SQLite backup API
            with sqlite3.connect(str(backup_path) as backup_conn:)
            self.connection.backup(backup_conn)
            backup_conn.close()

            self.migration_results["backups_created"] += 1
            logger.info(f"✅ Backup created: {backup_path}")
            return True

        except Exception as e:
            logger.error(f"❌ Backup creation failed: {e}")
            return False

    def validate_database_integrity(self) -> dict[str, Any]:
        """Validate database integrity."""
        try:
            if not self.connection:
                return {"success": False, "error": "No database connection"}

            # Run integrity check
            cursor = self.connection.execute("PRAGMA integrity_check")
            integrity_result = cursor.fetchone()

            # Check foreign key constraints
            cursor = self.connection.execute("PRAGMA foreign_key_check")
            fk_errors = cursor.fetchall()

            validation_result = {
                "success": integrity_result[0] == "ok",
                "integrity_check": integrity_result[0],
                "foreign_key_errors": len(fk_errors),
                "validation_timestamp": datetime.now().isoformat(),
            }

            if validation_result["success"]:
                self.migration_results["validations_passed"] += 1
                logger.info("✅ Database integrity validation passed")
            else:
                logger.warning("⚠️ Database integrity validation failed")

            return validation_result

        except Exception as e:
            logger.error(f"❌ Database validation failed: {e}")
            return {"success": False, "error": str(e)}

    def execute_migration_script(self, script_content: str) -> dict[str, Any]:
        """Execute migration script."""
        try:
            if not self.connection:
                return {"success": False, "error": "No database connection"}

            # Execute the migration script
            self.connection.executescript(script_content)
            self.connection.commit()

            self.migration_results["migrations_completed"] += 1
            logger.info("✅ Migration script executed successfully")

            return {
                "success": True,
                "execution_time": datetime.now().isoformat(),
                "rows_affected": self.connection.total_changes,
            }

        except Exception as e:
            logger.error(f"❌ Migration script execution failed: {e}")
            self.migration_results["errors_encountered"] += 1
            return {"success": False, "error": str(e)}

    def get_migration_results(self) -> dict[str, Any]:
        """Get migration results summary."""
        return {
            "migrations_completed": self.migration_results["migrations_completed"],
            "backups_created": self.migration_results["backups_created"],
            "validations_passed": self.migration_results["validations_passed"],
            "errors_encountered": self.migration_results["errors_encountered"],
            "success_rate": (
                self.migration_results["migrations_completed"]
                / max(
                    1,
                    self.migration_results["migrations_completed"]
                    + self.migration_results["errors_encountered"],
                )
            )
            * 100,
        }
