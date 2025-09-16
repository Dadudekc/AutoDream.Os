#!/usr/bin/env python3
"""
SQLite Schema Implementation - Agent-3 Database Specialist
=========================================================

This module implements the comprehensive SQLite database schema for the Agent Cellphone V2 system,
including all integration components, messaging system, Discord commander, and V2 compliance tracking.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseSchemaImplementation:
    """Main class for implementing the SQLite database schema."""
    
    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize the database schema implementation."""
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        
    def create_database(self) -> bool:
        """Create the complete database schema."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            # Create all tables
            self._create_agent_workspaces_table()
            self._create_agent_messages_table()
            self._create_discord_commands_table()
            self._create_integration_tests_table()
            self._create_v2_compliance_audit_table()
            self._create_file_compliance_table()
            self._create_message_archive_table()
            self._create_core_systems_status_table()
            
            # Create indexes for performance
            self._create_indexes()
            
            # Create views for common queries
            self._create_views()
            
            self.connection.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return False
            
    def create_complete_schema(self) -> bool:
        """Alias for create_database method for test compatibility."""
        return self.create_database()
        
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
    
    def _create_agent_workspaces_table(self):
        """Create the agent workspaces table with integration fields."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS agent_workspaces (
                agent_id TEXT PRIMARY KEY,
                team TEXT NOT NULL,
                specialization TEXT NOT NULL,
                captain TEXT NOT NULL,
                status TEXT NOT NULL,
                last_cycle TIMESTAMP,
                current_focus TEXT,
                cycle_count INTEGER DEFAULT 0,
                tasks_completed INTEGER DEFAULT 0,
                coordination_efficiency REAL DEFAULT 0.0,
                v2_compliance REAL DEFAULT 0.0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Integration fields
                integration_status TEXT DEFAULT 'pending',
                integration_components TEXT, -- JSON array
                integration_tests_passed INTEGER DEFAULT 0,
                integration_tests_total INTEGER DEFAULT 0
            )
        """)
    
    def _create_agent_messages_table(self):
        """Create the agent messages table with PyAutoGUI integration."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS agent_messages (
                message_id TEXT PRIMARY KEY,
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                priority TEXT NOT NULL,
                tags TEXT, -- JSON array
                content TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                
                -- Integration fields
                pyautogui_coordinates TEXT, -- JSON object
                delivery_method TEXT DEFAULT 'pyautogui',
                delivery_status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3
            )
        """)
    
    def _create_discord_commands_table(self):
        """Create the Discord commands table with controller integration."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS discord_commands (
                command_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                command_type TEXT NOT NULL,
                command_data TEXT NOT NULL, -- JSON object
                channel_id TEXT,
                user_id TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_status TEXT DEFAULT 'pending',
                response_data TEXT, -- JSON object
                
                -- Integration fields
                controller_status TEXT DEFAULT 'active',
                command_priority INTEGER DEFAULT 1,
                execution_time_ms INTEGER,
                error_message TEXT
            )
        """)
    
    def _create_integration_tests_table(self):
        """Create the integration tests table."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS integration_tests (
                test_id TEXT PRIMARY KEY,
                test_name TEXT NOT NULL,
                test_type TEXT NOT NULL,
                test_status TEXT DEFAULT 'pending',
                test_data TEXT, -- JSON object
                expected_result TEXT, -- JSON object
                actual_result TEXT, -- JSON object
                test_duration_ms INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                executed_at TIMESTAMP,
                
                -- Integration fields
                integration_component TEXT NOT NULL,
                test_coverage_percentage REAL DEFAULT 0.0,
                v2_compliance_check BOOLEAN DEFAULT FALSE
            )
        """)
    
    def _create_v2_compliance_audit_table(self):
        """Create the V2 compliance audit table."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS v2_compliance_audit (
                audit_id TEXT PRIMARY KEY,
                component_name TEXT NOT NULL,
                component_type TEXT NOT NULL,
                compliance_score REAL NOT NULL,
                violations_found INTEGER DEFAULT 0,
                violations_details TEXT, -- JSON array
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                auditor_agent TEXT NOT NULL,
                
                -- Integration fields
                integration_impact TEXT, -- JSON object
                refactoring_required BOOLEAN DEFAULT FALSE,
                refactoring_priority TEXT DEFAULT 'medium',
                estimated_refactoring_cycles INTEGER DEFAULT 1
            )
        """)
    
    def _create_file_compliance_table(self):
        """Create the file compliance tracking table."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS file_compliance (
                file_id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                file_size_bytes INTEGER NOT NULL,
                line_count INTEGER NOT NULL,
                compliance_status TEXT NOT NULL,
                violation_type TEXT,
                last_checked TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                
                -- Integration fields
                integration_dependencies TEXT, -- JSON array
                refactoring_plan TEXT, -- JSON object
                refactoring_status TEXT DEFAULT 'pending'
            )
        """)
    
    def _create_message_archive_table(self):
        """Create the message archive table for performance."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS message_archive (
                message_id TEXT PRIMARY KEY,
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                priority TEXT NOT NULL,
                tags TEXT,
                content TEXT NOT NULL,
                sent_at TIMESTAMP,
                processed_at TIMESTAMP,
                status TEXT,
                pyautogui_coordinates TEXT,
                delivery_method TEXT,
                delivery_status TEXT,
                retry_count INTEGER,
                archived_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def _create_core_systems_status_table(self):
        """Create the core systems status table for health monitoring."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS core_systems_status (
                system_id TEXT PRIMARY KEY,
                system_name TEXT NOT NULL,
                status TEXT NOT NULL,
                health_score REAL,
                last_health_check TIMESTAMP,
                error_count INTEGER DEFAULT 0,
                warning_count INTEGER DEFAULT 0,
                performance_metrics TEXT,
                dependencies TEXT,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def _create_indexes(self):
        """Create performance indexes."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_agent_team ON agent_workspaces(team)",
            "CREATE INDEX IF NOT EXISTS idx_agent_status ON agent_workspaces(status)",
            "CREATE INDEX IF NOT EXISTS idx_agent_last_updated ON agent_workspaces(last_updated)",
            "CREATE INDEX IF NOT EXISTS idx_message_to_agent ON agent_messages(to_agent)",
            "CREATE INDEX IF NOT EXISTS idx_message_status ON agent_messages(delivery_status)",
            "CREATE INDEX IF NOT EXISTS idx_message_sent_at ON agent_messages(sent_at)",
            "CREATE INDEX IF NOT EXISTS idx_discord_agent ON discord_commands(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_discord_status ON discord_commands(execution_status)",
            "CREATE INDEX IF NOT EXISTS idx_discord_executed ON discord_commands(executed_at)",
            "CREATE INDEX IF NOT EXISTS idx_test_type ON integration_tests(test_type)",
            "CREATE INDEX IF NOT EXISTS idx_test_status ON integration_tests(test_status)",
            "CREATE INDEX IF NOT EXISTS idx_audit_component ON v2_compliance_audit(component_name)",
            "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON v2_compliance_audit(audit_timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_file_path ON file_compliance(file_path)",
            "CREATE INDEX IF NOT EXISTS idx_file_status ON file_compliance(compliance_status)"
        ]
        
        for index_sql in indexes:
            self.connection.execute(index_sql)
    
    def _create_views(self):
        """Create useful views for common queries."""
        views = [
            """
            CREATE VIEW IF NOT EXISTS agent_performance_summary AS
            SELECT 
                team,
                COUNT(*) as agent_count,
                AVG(coordination_efficiency) as avg_efficiency,
                AVG(v2_compliance) as avg_compliance,
                SUM(tasks_completed) as total_tasks,
                AVG(integration_tests_passed * 100.0 / NULLIF(integration_tests_total, 0)) as avg_integration_success
            FROM agent_workspaces
            GROUP BY team
            """,
            """
            CREATE VIEW IF NOT EXISTS message_delivery_stats AS
            SELECT 
                DATE(sent_at) as delivery_date,
                COUNT(*) as total_messages,
                COUNT(CASE WHEN delivery_status = 'delivered' THEN 1 END) as delivered,
                COUNT(CASE WHEN delivery_status = 'failed' THEN 1 END) as failed,
                COUNT(CASE WHEN delivery_status = 'pending' THEN 1 END) as pending,
                AVG(CASE WHEN processed_at IS NOT NULL 
                    THEN (julianday(processed_at) - julianday(sent_at)) * 24 * 60 * 60 * 1000 
                    END) as avg_delivery_time_ms
            FROM agent_messages
            GROUP BY DATE(sent_at)
            """,
            """
            CREATE VIEW IF NOT EXISTS v2_compliance_summary AS
            SELECT 
                component_type,
                COUNT(*) as total_components,
                AVG(compliance_score) as avg_compliance_score,
                SUM(violations_found) as total_violations,
                COUNT(CASE WHEN refactoring_required = 1 THEN 1 END) as refactoring_required
            FROM v2_compliance_audit
            GROUP BY component_type
            """
        ]
        
        for view_sql in views:
            self.connection.execute(view_sql)
    
    def migrate_existing_data(self) -> bool:
        """Migrate existing JSON data to the database."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            # Migrate agent workspaces
            self._migrate_agent_workspaces()
            
            # Migrate configuration data
            self._migrate_configuration()
            
            # Migrate project analysis data
            self._migrate_project_analysis()
            
            self.connection.commit()
            logger.info("✅ Data migration completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Data migration failed: {e}")
            if self.connection:
                self.connection.rollback()
            return False
        finally:
            if self.connection:
                self.connection.close()
    
    def _migrate_agent_workspaces(self):
        """Migrate agent workspace JSON files to database."""
        workspace_dir = Path("agent_workspaces")
        if not workspace_dir.exists():
            return
        
        for agent_dir in workspace_dir.iterdir():
            if agent_dir.is_dir():
                agent_id = agent_dir.name
                status_file = agent_dir / "status.json"
                
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        status_data = json.load(f)
                    
                    # Insert or update agent workspace
                    self.connection.execute("""
                        INSERT OR REPLACE INTO agent_workspaces 
                        (agent_id, team, specialization, captain, status, last_cycle, 
                         current_focus, cycle_count, tasks_completed, coordination_efficiency, 
                         v2_compliance, last_updated, integration_status)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        status_data.get('agent_id', agent_id),
                        status_data.get('team', 'Unknown'),
                        status_data.get('specialization', 'Unknown'),
                        status_data.get('captain', 'Unknown'),
                        status_data.get('status', 'unknown'),
                        status_data.get('last_cycle'),
                        status_data.get('current_focus'),
                        status_data.get('cycle_count', 0),
                        status_data.get('tasks_completed', 0),
                        status_data.get('coordination_efficiency', 0.0),
                        status_data.get('v2_compliance', 0.0),
                        status_data.get('last_updated', datetime.now().isoformat()),
                        'pending'
                    ))
    
    def _migrate_configuration(self):
        """Migrate configuration data to database."""
        config_file = Path("config/coordinates.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
            # Store configuration as JSON in a simple table
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS configuration (
                    config_key TEXT PRIMARY KEY,
                    config_value TEXT NOT NULL,
                    config_type TEXT NOT NULL,
                    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            self.connection.execute("""
                INSERT OR REPLACE INTO configuration 
                (config_key, config_value, config_type)
                VALUES (?, ?, ?)
            """, (
                'coordinates',
                json.dumps(config_data),
                'json'
            ))
    
    def _migrate_project_analysis(self):
        """Migrate project analysis data to database."""
        analysis_files = [
            "project_analysis.json",
            "chatgpt_project_context.json"
        ]
        
        for analysis_file in analysis_files:
            file_path = Path(analysis_file)
            if file_path.exists():
                with open(file_path, 'r') as f:
                    analysis_data = json.load(f)
                
                # Store in project analysis table
                self.connection.execute("""
                    CREATE TABLE IF NOT EXISTS project_analysis (
                        analysis_id TEXT PRIMARY KEY,
                        analysis_type TEXT NOT NULL,
                        analysis_data TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                analysis_id = f"analysis_{file_path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.connection.execute("""
                    INSERT INTO project_analysis 
                    (analysis_id, analysis_type, analysis_data)
                    VALUES (?, ?, ?)
                """, (
                    analysis_id,
                    file_path.stem,
                    json.dumps(analysis_data)
                ))

def main():
    """Main function to create and initialize the database."""
    logger.info("🚀 Starting SQLite schema implementation...")
    
    # Create database schema
    db_impl = DatabaseSchemaImplementation()
    
    if db_impl.create_database():
        logger.info("✅ Database schema created successfully")
        
        # Migrate existing data
        if db_impl.migrate_existing_data():
            logger.info("✅ Data migration completed successfully")
            logger.info("🎉 Database implementation complete!")
        else:
            logger.error("❌ Data migration failed")
    else:
        logger.error("❌ Database creation failed")

if __name__ == "__main__":
    main()
