#!/usr/bin/env python3
"""
Schema Manager
==============

Manages database schema creation and updates.
"""

import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class SchemaManager:
    """Manages database schema creation and updates."""

    def __init__(self, db_path: Path):
        """Initialize schema manager."""
        self.db_path = db_path

    def create_database_schema(self) -> Dict[str, Any]:
        """Create the complete database schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create all tables
                self._create_agent_workspaces_table(cursor)
                self._create_agent_messages_table(cursor)
                self._create_discord_commands_table(cursor)
                self._create_core_systems_status_table(cursor)
                self._create_v2_compliance_audit_table(cursor)
                self._create_integration_tests_table(cursor)
                
                # Create indexes
                self._create_performance_indexes(cursor)
                
                # Create views
                self._create_useful_views(cursor)
                
                conn.commit()
                
                logger.info("Database schema created successfully")
                return {'success': True, 'message': 'Schema created successfully'}

        except Exception as e:
            logger.error(f"Schema creation failed: {e}")
            return {'success': False, 'error': str(e)}

    def _create_agent_workspaces_table(self, cursor):
        """Create agent workspaces table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_workspaces (
# SECURITY: Key placeholder - replace with environment variable
                agent_id TEXT NOT NULL UNIQUE,
                workspace_path TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                integration_status TEXT DEFAULT 'pending',
                last_activity TIMESTAMP,
                task_count INTEGER DEFAULT 0,
                completed_tasks INTEGER DEFAULT 0
            )
        """)

    def _create_agent_messages_table(self, cursor):
        """Create agent messages table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agent_messages (
# SECURITY: Key placeholder - replace with environment variable
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                message TEXT NOT NULL,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'sent',
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                delivered_at TIMESTAMP,
                coordinates_x INTEGER,
                coordinates_y INTEGER,
                delivery_method TEXT DEFAULT 'pyautogui'
            )
        """)

    def _create_discord_commands_table(self, cursor):
        """Create Discord commands table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discord_commands (
# SECURITY: Key placeholder - replace with environment variable
                command_name TEXT NOT NULL,
                user_id TEXT NOT NULL,
                channel_id TEXT NOT NULL,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                success BOOLEAN DEFAULT TRUE,
                response_time_ms INTEGER,
                error_message TEXT
            )
        """)

    def _create_core_systems_status_table(self, cursor):
        """Create core systems status table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS core_systems_status (
# SECURITY: Key placeholder - replace with environment variable
                system_name TEXT NOT NULL,
                status TEXT NOT NULL,
                health_score INTEGER DEFAULT 100,
                last_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                details TEXT,
                performance_metrics TEXT
            )
        """)

    def _create_v2_compliance_audit_table(self, cursor):
        """Create V2 compliance audit table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS v2_compliance_audit (
# SECURITY: Key placeholder - replace with environment variable
                file_path TEXT NOT NULL,
                line_count INTEGER NOT NULL,
                compliance_status TEXT NOT NULL,
                audit_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                issues TEXT,
                refactoring_notes TEXT
            )
        """)

    def _create_integration_tests_table(self, cursor):
        """Create integration tests table."""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS integration_tests (
# SECURITY: Key placeholder - replace with environment variable
                test_name TEXT NOT NULL,
                test_type TEXT NOT NULL,
                status TEXT NOT NULL,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                duration_ms INTEGER,
                error_message TEXT,
                test_data TEXT
            )
        """)

    def _create_performance_indexes(self, cursor):
        """Create performance indexes."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_agent_workspaces_agent_id ON agent_workspaces(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_agent_messages_from_agent ON agent_messages(from_agent)",
            "CREATE INDEX IF NOT EXISTS idx_agent_messages_to_agent ON agent_messages(to_agent)",
            "CREATE INDEX IF NOT EXISTS idx_agent_messages_sent_at ON agent_messages(sent_at)",
            "CREATE INDEX IF NOT EXISTS idx_discord_commands_executed_at ON discord_commands(executed_at)",
            "CREATE INDEX IF NOT EXISTS idx_core_systems_status_system_name ON core_systems_status(system_name)",
            "CREATE INDEX IF NOT EXISTS idx_v2_compliance_audit_file_path ON v2_compliance_audit(file_path)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)

    def _create_useful_views(self, cursor):
        """Create useful database views."""
        views = [
            """
            CREATE VIEW IF NOT EXISTS agent_activity_summary AS
            SELECT 
                agent_id,
                status,
                task_count,
                completed_tasks,
                last_activity,
                (completed_tasks * 100.0 / task_count) as completion_rate
            FROM agent_workspaces
            """,
            """
            CREATE VIEW IF NOT EXISTS message_volume_by_agent AS
            SELECT 
                from_agent,
                COUNT(*) as message_count,
                COUNT(CASE WHEN status = 'delivered' THEN 1 END) as delivered_count
            FROM agent_messages
            GROUP BY from_agent
            """
        ]
        
        for view_sql in views:
            cursor.execute(view_sql)


