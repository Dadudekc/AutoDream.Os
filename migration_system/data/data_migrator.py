#!/usr/bin/env python3
"""
Data Migrator
==============

Handles data migration operations.
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class DataMigrator:
    """Handles data migration operations."""

    def __init__(self, db_path: Path):
        """Initialize data migrator."""
        self.db_path = db_path

    def migrate_data(self) -> Dict[str, Any]:
        """Migrate existing data to new schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                migration_results = {
                    'success': True,
                    'migrated_tables': [],
                    'migrated_records': 0,
                    'errors': []
                }
                
                # Migrate agent workspaces
                workspace_result = self._migrate_agent_workspaces(cursor)
                if workspace_result['success']:
                    migration_results['migrated_tables'].append('agent_workspaces')
                    migration_results['migrated_records'] += workspace_result['record_count']
                else:
                    migration_results['errors'].append(workspace_result['error'])
                
                # Migrate configuration data
                config_result = self._migrate_configuration(cursor)
                if config_result['success']:
                    migration_results['migrated_tables'].append('configuration')
                    migration_results['migrated_records'] += config_result['record_count']
                else:
                    migration_results['errors'].append(config_result['error'])
                
                # Migrate project analysis data
                analysis_result = self._migrate_project_analysis(cursor)
                if analysis_result['success']:
                    migration_results['migrated_tables'].append('project_analysis')
                    migration_results['migrated_records'] += analysis_result['record_count']
                else:
                    migration_results['errors'].append(analysis_result['error'])
                
                conn.commit()
                
                logger.info(f"Data migration completed: {migration_results['migrated_records']} records migrated")
                return migration_results

        except Exception as e:
            logger.error(f"Data migration failed: {e}")
            return {'success': False, 'error': str(e)}

    def _migrate_agent_workspaces(self, cursor) -> Dict[str, Any]:
        """Migrate agent workspace data."""
        try:
            # Check if agent_workspaces directory exists
            workspaces_dir = Path("agent_workspaces")
            if not workspaces_dir.exists():
                return {'success': True, 'record_count': 0, 'message': 'No workspaces to migrate'}
            
            migrated_count = 0
            
            # Migrate each agent workspace
            for agent_dir in workspaces_dir.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    agent_id = agent_dir.name
                    
                    # Check if workspace already exists in database
                    cursor.execute("SELECT id FROM agent_workspaces WHERE agent_id = ?", (agent_id,))
                    if cursor.fetchone():
                        continue  # Already migrated
                    
                    # Insert workspace record
                    cursor.execute("""
                        INSERT INTO agent_workspaces (agent_id, workspace_path, status, integration_status)
                        VALUES (?, ?, 'active', 'pending')
                    """, (agent_id, str(agent_dir)))
                    
                    migrated_count += 1
            
            return {'success': True, 'record_count': migrated_count}

        except Exception as e:
            logger.error(f"Agent workspaces migration failed: {e}")
            return {'success': False, 'error': str(e)}

    def _migrate_configuration(self, cursor) -> Dict[str, Any]:
        """Migrate configuration data."""
        try:
            migrated_count = 0
            
            # Migrate coordinates configuration
            coords_file = Path("config/coordinates.json")
            if coords_file.exists():
                with open(coords_file, 'r') as f:
                    coords_data = json.load(f)
                
                # Store coordinates in core_systems_status
                cursor.execute("""
                    INSERT INTO core_systems_status (system_name, status, details)
                    VALUES ('coordinates_config', 'active', ?)
                """, (json.dumps(coords_data),))
                
                migrated_count += 1
            
            return {'success': True, 'record_count': migrated_count}

        except Exception as e:
            logger.error(f"Configuration migration failed: {e}")
            return {'success': False, 'error': str(e)}

    def _migrate_project_analysis(self, cursor) -> Dict[str, Any]:
        """Migrate project analysis data."""
        try:
            migrated_count = 0
            
            # Migrate project analysis file
            analysis_file = Path("project_analysis.json")
            if analysis_file.exists():
                with open(analysis_file, 'r') as f:
                    analysis_data = json.load(f)
                
                # Store analysis in core_systems_status
                cursor.execute("""
                    INSERT INTO core_systems_status (system_name, status, details)
                    VALUES ('project_analysis', 'active', ?)
                """, (json.dumps(analysis_data),))
                
                migrated_count += 1
            
            return {'success': True, 'record_count': migrated_count}

        except Exception as e:
            logger.error(f"Project analysis migration failed: {e}")
            return {'success': False, 'error': str(e)}


