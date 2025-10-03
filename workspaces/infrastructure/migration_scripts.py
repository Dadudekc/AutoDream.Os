#!/usr/bin/env python3
"""
Migration Scripts Module - Agent-3 Database Specialist
=====================================================

Migration script definitions and execution functionality
for V2 compliance and modular architecture.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MigrationScripts:
    """Migration script definitions and execution functionality."""
    
    def __init__(self):
        """Initialize the migration scripts."""
        self.scripts = self._define_migration_scripts()
    
    def _define_migration_scripts(self) -> Dict[str, str]:
        """Define migration scripts."""
        return {
            'create_agent_workspaces_table': """
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
                    integration_status TEXT DEFAULT 'pending',
                    integration_components TEXT,
                    integration_tests_passed INTEGER DEFAULT 0,
                    integration_tests_total INTEGER DEFAULT 0
                );
            """,
            'create_agent_messages_table': """
                CREATE TABLE IF NOT EXISTS agent_messages (
                    message_id TEXT PRIMARY KEY,
                    from_agent TEXT NOT NULL,
                    to_agent TEXT NOT NULL,
                    message_content TEXT NOT NULL,
                    priority TEXT DEFAULT 'NORMAL',
                    tags TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    delivery_status TEXT DEFAULT 'pending',
                    delivery_timestamp TIMESTAMP,
                    coordinates_x INTEGER,
                    coordinates_y INTEGER,
                    retry_count INTEGER DEFAULT 0,
                    error_message TEXT
                );
            """,
            'create_discord_commands_table': """
                CREATE TABLE IF NOT EXISTS discord_commands (
                    command_id TEXT PRIMARY KEY,
                    agent_id TEXT NOT NULL,
                    command_type TEXT NOT NULL,
                    command_content TEXT NOT NULL,
                    execution_status TEXT DEFAULT 'pending',
                    execution_timestamp TIMESTAMP,
                    response_content TEXT,
                    error_message TEXT,
                    execution_duration_ms INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """,
            'create_v2_compliance_audit_table': """
                CREATE TABLE IF NOT EXISTS v2_compliance_audit (
                    audit_id TEXT PRIMARY KEY,
                    component_name TEXT NOT NULL,
                    component_type TEXT NOT NULL,
                    compliance_score REAL NOT NULL,
                    violations_found INTEGER DEFAULT 0,
                    violations_details TEXT,
                    audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    auditor_agent TEXT NOT NULL,
                    integration_impact TEXT,
                    refactoring_required BOOLEAN DEFAULT FALSE,
                    refactoring_priority TEXT DEFAULT 'medium',
                    estimated_refactoring_cycles INTEGER DEFAULT 1
                );
            """,
            'create_integration_tests_table': """
                CREATE TABLE IF NOT EXISTS integration_tests (
                    test_id TEXT PRIMARY KEY,
                    test_name TEXT NOT NULL,
                    test_type TEXT NOT NULL,
                    test_status TEXT DEFAULT 'pending',
                    test_data TEXT,
                    expected_result TEXT,
                    actual_result TEXT,
                    test_duration_ms INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    executed_at TIMESTAMP,
                    integration_component TEXT NOT NULL,
                    test_coverage_percentage REAL DEFAULT 0.0,
                    v2_compliance_check BOOLEAN DEFAULT FALSE
                );
            """,
            'create_core_systems_status_table': """
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
                );
            """
        }
    
    def get_migration_script(self, script_name: str) -> Optional[str]:
        """Get specific migration script."""
        return self.scripts.get(script_name)
    
    def get_all_migration_scripts(self) -> Dict[str, str]:
        """Get all migration scripts."""
        return self.scripts.copy()
    
    def create_performance_indexes_script(self) -> str:
        """Create performance indexes script."""
        return """
            -- Performance indexes for agent_workspaces
            CREATE INDEX IF NOT EXISTS idx_agent_workspaces_team ON agent_workspaces(team);
            CREATE INDEX IF NOT EXISTS idx_agent_workspaces_status ON agent_workspaces(status);
            CREATE INDEX IF NOT EXISTS idx_agent_workspaces_last_cycle ON agent_workspaces(last_cycle);
            
            -- Performance indexes for agent_messages
            CREATE INDEX IF NOT EXISTS idx_agent_messages_from_agent ON agent_messages(from_agent);
            CREATE INDEX IF NOT EXISTS idx_agent_messages_to_agent ON agent_messages(to_agent);
            CREATE INDEX IF NOT EXISTS idx_agent_messages_sent_at ON agent_messages(sent_at);
            CREATE INDEX IF NOT EXISTS idx_agent_messages_delivery_status ON agent_messages(delivery_status);
            
            -- Performance indexes for discord_commands
            CREATE INDEX IF NOT EXISTS idx_discord_commands_agent_id ON discord_commands(agent_id);
            CREATE INDEX IF NOT EXISTS idx_discord_commands_command_type ON discord_commands(command_type);
            CREATE INDEX IF NOT EXISTS idx_discord_commands_execution_status ON discord_commands(execution_status);
            
            -- Performance indexes for v2_compliance_audit
            CREATE INDEX IF NOT EXISTS idx_v2_compliance_component_name ON v2_compliance_audit(component_name);
            CREATE INDEX IF NOT EXISTS idx_v2_compliance_compliance_score ON v2_compliance_audit(compliance_score);
            CREATE INDEX IF NOT EXISTS idx_v2_compliance_audit_timestamp ON v2_compliance_audit(audit_timestamp);
            
            -- Performance indexes for integration_tests
            CREATE INDEX IF NOT EXISTS idx_integration_tests_test_type ON integration_tests(test_type);
            CREATE INDEX IF NOT EXISTS idx_integration_tests_test_status ON integration_tests(test_status);
            CREATE INDEX IF NOT EXISTS idx_integration_tests_integration_component ON integration_tests(integration_component);
            
            -- Performance indexes for core_systems_status
            CREATE INDEX IF NOT EXISTS idx_core_systems_system_name ON core_systems_status(system_name);
            CREATE INDEX IF NOT EXISTS idx_core_systems_status ON core_systems_status(status);
            CREATE INDEX IF NOT EXISTS idx_core_systems_health_score ON core_systems_status(health_score);
        """
    
    def create_useful_views_script(self) -> str:
        """Create useful views script."""
        return """
            -- View for active agents
            CREATE VIEW IF NOT EXISTS active_agents AS
            SELECT 
                agent_id,
                team,
                specialization,
                captain,
                current_focus,
                cycle_count,
                tasks_completed,
                coordination_efficiency,
                v2_compliance,
                last_updated
            FROM agent_workspaces
            WHERE status = 'active';
            
            -- View for recent messages
            CREATE VIEW IF NOT EXISTS recent_messages AS
            SELECT 
                message_id,
                from_agent,
                to_agent,
                message_content,
                priority,
                sent_at,
                delivery_status
            FROM agent_messages
            WHERE sent_at >= datetime('now', '-24 hours')
            ORDER BY sent_at DESC;
            
            -- View for compliance summary
            CREATE VIEW IF NOT EXISTS compliance_summary AS
            SELECT 
                component_name,
                component_type,
                AVG(compliance_score) as avg_compliance_score,
                COUNT(*) as audit_count,
                MAX(audit_timestamp) as last_audit
            FROM v2_compliance_audit
            GROUP BY component_name, component_type;
            
            -- View for system health overview
            CREATE VIEW IF NOT EXISTS system_health_overview AS
            SELECT 
                system_name,
                status,
                health_score,
                error_count,
                warning_count,
                last_health_check,
                last_updated
            FROM core_systems_status
            ORDER BY health_score DESC;
        """
    
    def get_migration_script_names(self) -> List[str]:
        """Get list of migration script names."""
        return list(self.scripts.keys())


