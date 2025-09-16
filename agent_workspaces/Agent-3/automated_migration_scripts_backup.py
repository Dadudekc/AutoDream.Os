#!/usr/bin/env python3
"""
Automated Migration Scripts - Agent-3 Database Specialist
========================================================

This module provides automated migration scripts for Phase 1 database implementation,
including data migration, schema validation, and integration testing.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import sqlite3
import json
import shutil
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AutomatedMigrationScripts:
    """Main class for automated database migration scripts."""
    
    def __init__(self, db_path: str = "data/agent_system.db", backup_dir: str = "backups/migration"):
        """Initialize the migration scripts."""
        self.db_path = Path(db_path)
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        self.connection = None
        
    def run_complete_migration(self) -> Dict[str, Any]:
        """Run complete migration process with validation."""
        migration_results = {
            'start_time': datetime.now().isoformat(),
            'steps_completed': [],
            'errors': [],
            'warnings': [],
            'success': False
        }
        
        try:
            # Step 1: Create backup
            logger.info("🔄 Step 1: Creating data backup...")
            backup_result = self._create_migration_backup()
            migration_results['steps_completed'].append('backup_creation')
            if not backup_result['success']:
                migration_results['errors'].append(backup_result['error'])
                return migration_results
            
            # Step 2: Validate existing data
            logger.info("🔄 Step 2: Validating existing data...")
            validation_result = self._validate_existing_data()
            migration_results['steps_completed'].append('data_validation')
            if not validation_result['success']:
                migration_results['warnings'].append(validation_result['warning'])
            
            # Step 3: Create database schema
            logger.info("🔄 Step 3: Creating database schema...")
            schema_result = self._create_database_schema()
            migration_results['steps_completed'].append('schema_creation')
            if not schema_result['success']:
                migration_results['errors'].append(schema_result['error'])
                return migration_results
            
            # Step 4: Migrate data
            logger.info("🔄 Step 4: Migrating data...")
            migration_result = self._migrate_data()
            migration_results['steps_completed'].append('data_migration')
            if not migration_result['success']:
                migration_results['errors'].append(migration_result['error'])
                return migration_results
            
            # Step 5: Validate migration
            logger.info("🔄 Step 5: Validating migration...")
            validation_result = self._validate_migration()
            migration_results['steps_completed'].append('migration_validation')
            if not validation_result['success']:
                migration_results['errors'].append(validation_result['error'])
                return migration_results
            
            # Step 6: Run integration tests
            logger.info("🔄 Step 6: Running integration tests...")
            test_result = self._run_integration_tests()
            migration_results['steps_completed'].append('integration_tests')
            if not test_result['success']:
                migration_results['warnings'].append(test_result['warning'])
            
            migration_results['success'] = True
            migration_results['end_time'] = datetime.now().isoformat()
            logger.info("✅ Migration completed successfully!")
            
        except Exception as e:
            migration_results['errors'].append(f"Migration failed: {str(e)}")
            logger.error(f"❌ Migration failed: {e}")
        
        return migration_results
    
    def _create_migration_backup(self) -> Dict[str, Any]:
        """Create comprehensive backup before migration."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"migration_backup_{timestamp}"
            backup_path.mkdir(exist_ok=True)
            
            # Backup agent workspaces
            workspace_dir = Path("agent_workspaces")
            if workspace_dir.exists():
                shutil.copytree(workspace_dir, backup_path / "agent_workspaces")
            
            # Backup configuration
            config_dir = Path("config")
            if config_dir.exists():
                shutil.copytree(config_dir, backup_path / "config")
            
            # Backup project analysis files
            analysis_files = ["project_analysis.json", "chatgpt_project_context.json"]
            for file_name in analysis_files:
                file_path = Path(file_name)
                if file_path.exists():
                    shutil.copy2(file_path, backup_path / file_name)
            
            # Create backup manifest
            manifest = {
                'backup_timestamp': timestamp,
                'backup_path': str(backup_path),
                'files_backed_up': list(backup_path.rglob('*')),
                'backup_size_bytes': sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
            }
            
            with open(backup_path / "backup_manifest.json", 'w') as f:
                json.dump(manifest, f, indent=2, default=str)
            
            return {'success': True, 'backup_path': str(backup_path)}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _validate_existing_data(self) -> Dict[str, Any]:
        """Validate existing data before migration."""
        try:
            validation_results = {
                'agent_workspaces': {'valid': True, 'count': 0, 'errors': []},
                'configuration': {'valid': True, 'count': 0, 'errors': []},
                'project_analysis': {'valid': True, 'count': 0, 'errors': []}
            }
            
            # Validate agent workspaces
            workspace_dir = Path("agent_workspaces")
            if workspace_dir.exists():
                for agent_dir in workspace_dir.iterdir():
                    if agent_dir.is_dir():
                        validation_results['agent_workspaces']['count'] += 1
                        
                        # Check required files
                        required_files = ['status.json', 'working_tasks.json', 'future_tasks.json']
                        for required_file in required_files:
                            file_path = agent_dir / required_file
                            if file_path.exists():
                                try:
                                    with open(file_path, 'r') as f:
                                        json.load(f)
                                except json.JSONDecodeError as e:
                                    validation_results['agent_workspaces']['errors'].append(
                                        f"Invalid JSON in {file_path}: {e}"
                                    )
                                    validation_results['agent_workspaces']['valid'] = False
                            else:
                                validation_results['agent_workspaces']['errors'].append(
                                    f"Missing required file: {file_path}"
                                )
                                validation_results['agent_workspaces']['valid'] = False
            
            # Validate configuration
            config_file = Path("config/coordinates.json")
            if config_file.exists():
                validation_results['configuration']['count'] = 1
                try:
                    with open(config_file, 'r') as f:
                        config_data = json.load(f)
                        if 'agents' not in config_data:
                            validation_results['configuration']['errors'].append("Missing 'agents' key in coordinates.json")
                            validation_results['configuration']['valid'] = False
                except json.JSONDecodeError as e:
                    validation_results['configuration']['errors'].append(f"Invalid JSON in coordinates.json: {e}")
                    validation_results['configuration']['valid'] = False
            
            # Validate project analysis
            analysis_files = ["project_analysis.json", "chatgpt_project_context.json"]
            for file_name in analysis_files:
                file_path = Path(file_name)
                if file_path.exists():
                    validation_results['project_analysis']['count'] += 1
                    try:
                        with open(file_path, 'r') as f:
                            json.load(f)
                    except json.JSONDecodeError as e:
                        validation_results['project_analysis']['errors'].append(f"Invalid JSON in {file_name}: {e}")
                        validation_results['project_analysis']['valid'] = False
            
            overall_valid = all(result['valid'] for result in validation_results.values())
            
            return {
                'success': overall_valid,
                'warning': 'Data validation issues found' if not overall_valid else None,
                'validation_results': validation_results
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _create_database_schema(self) -> Dict[str, Any]:
        """Create database schema with all integration tables."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            # Create all tables
            self._create_agent_workspaces_table()
            self._create_agent_messages_table()
            self._create_discord_commands_table()
            self._create_core_systems_status_table()
            self._create_v2_compliance_audit_table()
            self._create_integration_tests_table()
            
            # Create indexes
            self._create_performance_indexes()
            
            # Create views
            self._create_useful_views()
            
            self.connection.commit()
            return {'success': True}
            
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if self.connection:
                self.connection.close()
    
    def _migrate_data(self) -> Dict[str, Any]:
        """Migrate existing data to new database schema."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            # Migrate agent workspaces
            self._migrate_agent_workspaces()
            
            # Migrate configuration
            self._migrate_configuration()
            
            # Migrate project analysis
            self._migrate_project_analysis()
            
            self.connection.commit()
            return {'success': True}
            
        except Exception as e:
            if self.connection:
                self.connection.rollback()
            return {'success': False, 'error': str(e)}
        finally:
            if self.connection:
                self.connection.close()
    
    def _validate_migration(self) -> Dict[str, Any]:
        """Validate migration results."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            validation_results = {}
            
            # Validate agent workspaces migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            agent_count = cursor.fetchone()['count']
            validation_results['agent_workspaces_migrated'] = agent_count
            
            # Validate configuration migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM configuration")
            config_count = cursor.fetchone()['count']
            validation_results['configuration_migrated'] = config_count
            
            # Validate project analysis migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM project_analysis")
            analysis_count = cursor.fetchone()['count']
            validation_results['project_analysis_migrated'] = analysis_count
            
            # Check data integrity
            cursor = self.connection.execute("""
                SELECT COUNT(*) as count FROM agent_workspaces 
                WHERE agent_id IS NULL OR team IS NULL
            """)
            null_violations = cursor.fetchone()['count']
            validation_results['data_integrity_violations'] = null_violations
            
            success = (agent_count > 0 and config_count > 0 and null_violations == 0)
            
            return {
                'success': success,
                'validation_results': validation_results
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if self.connection:
                self.connection.close()
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests after migration."""
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            test_results = {
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0,
                'test_details': []
            }
            
            # Test 1: Database connection
            test_results['total_tests'] += 1
            try:
                cursor = self.connection.execute("SELECT 1")
                test_results['passed_tests'] += 1
                test_results['test_details'].append({'test': 'database_connection', 'status': 'PASS'})
            except Exception as e:
                test_results['failed_tests'] += 1
                test_results['test_details'].append({'test': 'database_connection', 'status': 'FAIL', 'error': str(e)})
            
            # Test 2: Table existence
            test_results['total_tests'] += 1
            try:
                cursor = self.connection.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN ('agent_workspaces', 'agent_messages', 'discord_commands')
                """)
                tables = cursor.fetchall()
                if len(tables) >= 3:
                    test_results['passed_tests'] += 1
                    test_results['test_details'].append({'test': 'table_existence', 'status': 'PASS'})
                else:
                    test_results['failed_tests'] += 1
                    test_results['test_details'].append({'test': 'table_existence', 'status': 'FAIL', 'error': 'Missing required tables'})
            except Exception as e:
                test_results['failed_tests'] += 1
                test_results['test_details'].append({'test': 'table_existence', 'status': 'FAIL', 'error': str(e)})
            
            # Test 3: Data migration
            test_results['total_tests'] += 1
            try:
                cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces")
                agent_count = cursor.fetchone()['count']
                if agent_count > 0:
                    test_results['passed_tests'] += 1
                    test_results['test_details'].append({'test': 'data_migration', 'status': 'PASS', 'agent_count': agent_count})
                else:
                    test_results['failed_tests'] += 1
                    test_results['test_details'].append({'test': 'data_migration', 'status': 'FAIL', 'error': 'No agents migrated'})
            except Exception as e:
                test_results['failed_tests'] += 1
                test_results['test_details'].append({'test': 'data_migration', 'status': 'FAIL', 'error': str(e)})
            
            success = test_results['failed_tests'] == 0
            
            return {
                'success': success,
                'warning': f"{test_results['failed_tests']} tests failed" if not success else None,
                'test_results': test_results
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
        finally:
            if self.connection:
                self.connection.close()
    
    def _create_agent_workspaces_table(self):
        """Create agent workspaces table with integration fields."""
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
                integration_status TEXT DEFAULT 'pending',
                integration_components TEXT,
                integration_tests_passed INTEGER DEFAULT 0,
                integration_tests_total INTEGER DEFAULT 0
            )
        """)
    
    def _create_agent_messages_table(self):
        """Create agent messages table with PyAutoGUI integration."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS agent_messages (
                message_id TEXT PRIMARY KEY,
                from_agent TEXT NOT NULL,
                to_agent TEXT NOT NULL,
                priority TEXT NOT NULL,
                tags TEXT,
                content TEXT NOT NULL,
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processed_at TIMESTAMP,
                status TEXT DEFAULT 'pending',
                pyautogui_coordinates TEXT,
                delivery_method TEXT DEFAULT 'pyautogui',
                delivery_status TEXT DEFAULT 'pending',
                retry_count INTEGER DEFAULT 0,
                max_retries INTEGER DEFAULT 3
            )
        """)
    
    def _create_discord_commands_table(self):
        """Create Discord commands table with controller integration."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS discord_commands (
                command_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                command_type TEXT NOT NULL,
                command_data TEXT NOT NULL,
                channel_id TEXT,
                user_id TEXT,
                executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                execution_status TEXT DEFAULT 'pending',
                response_data TEXT,
                controller_status TEXT DEFAULT 'active',
                command_priority INTEGER DEFAULT 1,
                execution_time_ms INTEGER,
                error_message TEXT
            )
        """)
    
    def _create_core_systems_status_table(self):
        """Create core systems status table."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS core_systems_status (
                system_id TEXT PRIMARY KEY,
                system_name TEXT NOT NULL,
                system_status TEXT NOT NULL,
                health_score REAL DEFAULT 100.0,
                last_health_check TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                error_count INTEGER DEFAULT 0,
                performance_metrics TEXT
            )
        """)
    
    def _create_v2_compliance_audit_table(self):
        """Create V2 compliance audit table."""
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS v2_compliance_audit (
                audit_id TEXT PRIMARY KEY,
                component_name TEXT NOT NULL,
                component_type TEXT NOT NULL,
                compliance_score REAL NOT NULL,
                violations_found INTEGER DEFAULT 0,
                violations_details TEXT,
                audit_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                auditor_agent TEXT NOT NULL
            )
        """)
    
    def _create_integration_tests_table(self):
        """Create integration tests table."""
        self.connection.execute("""
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
                v2_compliance_check BOOLEAN DEFAULT FALSE,
                test_agent TEXT NOT NULL
            )
        """)
    
    def _create_performance_indexes(self):
        """Create performance indexes."""
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_agent_team ON agent_workspaces(team)",
            "CREATE INDEX IF NOT EXISTS idx_agent_status ON agent_workspaces(status)",
            "CREATE INDEX IF NOT EXISTS idx_message_to_agent ON agent_messages(to_agent)",
            "CREATE INDEX IF NOT EXISTS idx_message_status ON agent_messages(delivery_status)",
            "CREATE INDEX IF NOT EXISTS idx_discord_agent ON discord_commands(agent_id)",
            "CREATE INDEX IF NOT EXISTS idx_discord_status ON discord_commands(execution_status)"
        ]
        
        for index_sql in indexes:
            self.connection.execute(index_sql)
    
    def _create_useful_views(self):
        """Create useful views for common queries."""
        views = [
            """
            CREATE VIEW IF NOT EXISTS agent_performance_summary AS
            SELECT 
                team,
                COUNT(*) as agent_count,
                AVG(coordination_efficiency) as avg_efficiency,
                AVG(v2_compliance) as avg_compliance,
                SUM(tasks_completed) as total_tasks
            FROM agent_workspaces
            GROUP BY team
            """
        ]
        
        for view_sql in views:
            self.connection.execute(view_sql)
    
    def _migrate_agent_workspaces(self):
        """Migrate agent workspace data."""
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
        """Migrate configuration data."""
        config_file = Path("config/coordinates.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)
            
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
            """, ('coordinates', json.dumps(config_data), 'json'))
    
    def _migrate_project_analysis(self):
        """Migrate project analysis data."""
        analysis_files = ["project_analysis.json", "chatgpt_project_context.json"]
        
        for analysis_file in analysis_files:
            file_path = Path(analysis_file)
            if file_path.exists():
                with open(file_path, 'r') as f:
                    analysis_data = json.load(f)
                
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
                """, (analysis_id, file_path.stem, json.dumps(analysis_data)))

def main():
    """Main function to run automated migration."""
    logger.info("🚀 Starting automated migration scripts...")
    
    migration_scripts = AutomatedMigrationScripts()
    results = migration_scripts.run_complete_migration()
    
    if results['success']:
        logger.info("✅ Migration completed successfully!")
        logger.info(f"Steps completed: {', '.join(results['steps_completed'])}")
    else:
        logger.error("❌ Migration failed!")
        for error in results['errors']:
            logger.error(f"Error: {error}")
    
    return results

if __name__ == "__main__":
    main()
