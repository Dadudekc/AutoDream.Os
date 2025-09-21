#!/usr/bin/env python3
"""
Data Validator
==============

Validates data integrity during migration operations.
"""

import sqlite3
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data integrity during migration operations."""

    def __init__(self, db_path: Path):
        """Initialize data validator."""
        self.db_path = db_path

    def validate_existing_data(self) -> Dict[str, Any]:
        """Validate existing data before migration."""
        try:
            if not self.db_path.exists():
                return {'success': True, 'message': 'No existing database to validate'}

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check for existing tables
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                validation_results = {
                    'success': True,
                    'existing_tables': existing_tables,
                    'table_count': len(existing_tables),
                    'issues': []
                }
                
                # Validate each table
                for table in existing_tables:
                    try:
                        cursor.execute(f"SELECT COUNT(*) FROM {table}")
                        count = cursor.fetchone()[0]
                        validation_results[f'{table}_count'] = count
                        
                        if count > 0:
                            logger.info(f"Table {table} has {count} records")
                        
                    except Exception as e:
                        validation_results['issues'].append(f"Error validating table {table}: {e}")
                
                return validation_results

        except Exception as e:
            logger.error(f"Data validation failed: {e}")
            return {'success': False, 'error': str(e)}

    def validate_migration(self) -> Dict[str, Any]:
        """Validate data after migration."""
        try:
            if not self.db_path.exists():
                return {'success': False, 'error': 'Database not found'}

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check for required tables
                required_tables = [
                    'agent_workspaces',
                    'agent_messages', 
                    'discord_commands',
                    'core_systems_status',
                    'v2_compliance_audit',
                    'integration_tests'
                ]
                
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                existing_tables = [row[0] for row in cursor.fetchall()]
                
                validation_results = {
                    'success': True,
                    'required_tables': required_tables,
                    'existing_tables': existing_tables,
                    'missing_tables': [],
                    'table_counts': {},
                    'issues': []
                }
                
                # Check for missing tables
                for table in required_tables:
                    if table not in existing_tables:
                        validation_results['missing_tables'].append(table)
                        validation_results['issues'].append(f"Required table {table} is missing")
                    else:
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table}")
                            count = cursor.fetchone()[0]
                            validation_results['table_counts'][table] = count
                        except Exception as e:
                            validation_results['issues'].append(f"Error counting records in {table}: {e}")
                
                # Check for data integrity
                if validation_results['missing_tables']:
                    validation_results['success'] = False
                
                return validation_results

        except Exception as e:
            logger.error(f"Migration validation failed: {e}")
            return {'success': False, 'error': str(e)}

    def validate_data_integrity(self) -> Dict[str, Any]:
        """Validate data integrity constraints."""
        try:
            if not self.db_path.exists():
                return {'success': False, 'error': 'Database not found'}

            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                integrity_results = {
                    'success': True,
                    'constraints_checked': [],
                    'violations': []
                }
                
                # Check foreign key constraints
# SECURITY: Key placeholder - replace with environment variable
                fk_violations = cursor.fetchall()
                
                if fk_violations:
                    integrity_results['violations'].extend([
# SECURITY: Key placeholder - replace with environment variable
                    ])
                    integrity_results['success'] = False
                
# SECURITY: Key placeholder - replace with environment variable
                
                # Check for orphaned records
                # This would be specific to your data model
                # Example: Check for agent messages without corresponding workspaces
                
                return integrity_results

        except Exception as e:
            logger.error(f"Data integrity validation failed: {e}")
            return {'success': False, 'error': str(e)}


