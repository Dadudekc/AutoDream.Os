"""
Test suite for automated migration scripts
=========================================

Tests for the AutomatedMigrationScripts class including:
- Backup creation and validation
- Data migration processes
- Schema creation and validation
- Integration testing
"""

import pytest
import tempfile
import shutil
import json
import sqlite3
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
import os

# Add the agent workspace to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))

from automated_migration_scripts import AutomatedMigrationScripts


class TestAutomatedMigrationScripts:
    """Test cases for AutomatedMigrationScripts class."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.fixture
    def sample_agent_workspace(self, temp_dir):
        """Create sample agent workspace structure."""
        workspace_dir = Path(temp_dir) / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        # Create sample status.json
        status_data = {
            "agent_id": "Agent-3",
            "team": "Team Alpha",
            "specialization": "Database Specialist",
            "captain": "Agent-4",
            "status": "active",
            "cycle_count": 5,
            "tasks_completed": 7,
            "coordination_efficiency": 98.0,
            "v2_compliance": 90.0
        }
        
        with open(workspace_dir / "status.json", 'w') as f:
            json.dump(status_data, f)
        
        # Create sample working_tasks.json
        working_tasks_data = {
            "current_task": {
                "id": "DB_011",
                "title": "Query Optimization",
                "status": "in_progress"
            },
            "task_history": []
        }
        
        with open(workspace_dir / "working_tasks.json", 'w') as f:
            json.dump(working_tasks_data, f)
        
        # Create sample future_tasks.json
        future_tasks_data = {
            "available_tasks": []
        }
        
        with open(workspace_dir / "future_tasks.json", 'w') as f:
            json.dump(future_tasks_data, f)
        
        return workspace_dir
    
    @pytest.fixture
    def sample_config(self, temp_dir):
        """Create sample configuration files."""
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        coordinates_data = {
            "agents": {
                "Agent-1": {"x": -1269, "y": 481},
                "Agent-2": {"x": -308, "y": 480},
                "Agent-3": {"x": -1269, "y": 1001}
            }
        }
        
        with open(config_dir / "coordinates.json", 'w') as f:
            json.dump(coordinates_data, f)
        
        return config_dir
    
    @pytest.fixture
    def sample_analysis_files(self, temp_dir):
        """Create sample project analysis files."""
        analysis_data = {
            "project_name": "Agent Cellphone V2",
            "v2_compliance": 90.0,
            "total_files": 150,
            "analysis_timestamp": "2025-01-16T13:00:00Z"
        }
        
        with open(Path(temp_dir) / "project_analysis.json", 'w') as f:
            json.dump(analysis_data, f)
        
        context_data = {
            "project_context": "Agent Cellphone V2 Repository",
            "architecture": "Multi-agent system with database integration"
        }
        
        with open(Path(temp_dir) / "chatgpt_project_context.json", 'w') as f:
            json.dump(context_data, f)
        
        return temp_dir
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_migration_scripts_initialization(self, migration_scripts):
        """Test AutomatedMigrationScripts initialization."""
        assert migration_scripts.db_path.exists() is False  # Database not created yet
        assert migration_scripts.backup_dir.exists() is True
        assert migration_scripts.connection is None
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_create_migration_backup(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test migration backup creation."""
        # Change to the temp directory to simulate the project root
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            
            result = migration_scripts._create_migration_backup()
            
            assert result['success'] is True
            assert 'backup_path' in result
            
            backup_path = Path(result['backup_path'])
            assert backup_path.exists()
            assert (backup_path / "agent_workspaces").exists()
            assert (backup_path / "config").exists()
            assert (backup_path / "project_analysis.json").exists()
            assert (backup_path / "backup_manifest.json").exists()
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_validate_existing_data(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test existing data validation."""
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            
            result = migration_scripts._validate_existing_data()
            
            assert result['success'] is True
            assert 'validation_results' in result
            
            validation_results = result['validation_results']
            assert 'agent_workspaces' in validation_results
            assert 'configuration' in validation_results
            assert 'project_analysis' in validation_results
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.integration
    @pytest.mark.agent3
    def test_create_database_schema(self, migration_scripts):
        """Test database schema creation."""
        result = migration_scripts._create_database_schema()
        
        assert result['success'] is True
        assert migration_scripts.db_path.exists()
        
        # Verify tables were created
        conn = sqlite3.connect(str(migration_scripts.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN (
                'agent_workspaces', 'agent_messages', 'discord_commands',
                'core_systems_status', 'v2_compliance_audit', 'integration_tests'
            )
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert len(tables) == 6
        assert 'agent_workspaces' in tables
        assert 'agent_messages' in tables
        assert 'discord_commands' in tables
        assert 'core_systems_status' in tables
        assert 'v2_compliance_audit' in tables
        assert 'integration_tests' in tables
    
    @pytest.mark.integration
    @pytest.mark.agent3
    def test_migrate_data(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test data migration."""
        # First create the schema
        migration_scripts._create_database_schema()
        
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            
            result = migration_scripts._migrate_data()
            
            assert result['success'] is True
            
            # Verify data was migrated
            conn = sqlite3.connect(str(migration_scripts.db_path))
            cursor = conn.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            agent_count = cursor.fetchone()[0]
            conn.close()
            
            assert agent_count > 0
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.integration
    @pytest.mark.agent3
    def test_validate_migration(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test migration validation."""
        # First create schema and migrate data
        migration_scripts._create_database_schema()
        
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            migration_scripts._migrate_data()
            
            result = migration_scripts._validate_migration()
            
            assert result['success'] is True
            assert 'validation_results' in result
            
            validation_results = result['validation_results']
            assert 'agent_workspaces_migrated' in validation_results
            assert 'configuration_migrated' in validation_results
            assert 'project_analysis_migrated' in validation_results
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.integration
    @pytest.mark.agent3
    def test_run_integration_tests(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test integration test execution."""
        # First create schema and migrate data
        migration_scripts._create_database_schema()
        
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            migration_scripts._migrate_data()
            
            result = migration_scripts._run_integration_tests()
            
            assert result['success'] is True
            assert 'test_results' in result
            
            test_results = result['test_results']
            assert 'total_tests' in test_results
            assert 'passed_tests' in test_results
            assert 'failed_tests' in test_results
            assert test_results['total_tests'] > 0
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.system
    @pytest.mark.agent3
    @pytest.mark.slow
    def test_run_complete_migration(self, migration_scripts, sample_agent_workspace, sample_config, sample_analysis_files):
        """Test complete migration process."""
        original_cwd = os.getcwd()
        try:
            os.chdir(sample_analysis_files)
            
            result = migration_scripts.run_complete_migration()
            
            assert result['success'] is True
            assert 'steps_completed' in result
            assert 'errors' in result
            assert 'warnings' in result
            
            # Verify all steps were completed
            expected_steps = [
                'backup_creation',
                'data_validation',
                'schema_creation',
                'data_migration',
                'migration_validation',
                'integration_tests'
            ]
            
            for step in expected_steps:
                assert step in result['steps_completed']
            
            # Verify database was created and has data
            assert migration_scripts.db_path.exists()
            
            conn = sqlite3.connect(str(migration_scripts.db_path))
            cursor = conn.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            agent_count = cursor.fetchone()[0]
            conn.close()
            
            assert agent_count > 0
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_error_handling_invalid_json(self, migration_scripts, temp_dir):
        """Test error handling with invalid JSON files."""
        # Create invalid JSON file
        workspace_dir = Path(temp_dir) / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
        with open(workspace_dir / "status.json", 'w') as f:
            f.write("invalid json content")
        
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            result = migration_scripts._validate_existing_data()
            
            assert result['success'] is False
            assert 'validation_results' in result
            
            validation_results = result['validation_results']
            assert validation_results['agent_workspaces']['valid'] is False
            assert len(validation_results['agent_workspaces']['errors']) > 0
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_performance_indexes_creation(self, migration_scripts):
        """Test performance indexes creation."""
        migration_scripts._create_database_schema()
        
        conn = sqlite3.connect(str(migration_scripts.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        indexes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_indexes = [
            'idx_agent_team',
            'idx_agent_status',
            'idx_message_to_agent',
            'idx_message_status',
            'idx_discord_agent',
            'idx_discord_status'
        ]
        
        for expected_index in expected_indexes:
            assert expected_index in indexes
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_useful_views_creation(self, migration_scripts):
        """Test useful views creation."""
        migration_scripts._create_database_schema()
        
        conn = sqlite3.connect(str(migration_scripts.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='view' AND name = 'agent_performance_summary'
        """)
        views = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert 'agent_performance_summary' in views

