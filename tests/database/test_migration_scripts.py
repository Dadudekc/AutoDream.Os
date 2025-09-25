#!/usr/bin/env python3
"""
Database Migration Scripts Tests - Modular Test Suite
======================================================

Tests for automated migration scripts functionality.
Tests backup creation, data migration, and schema validation.

Author: Agent-3 (Database Specialist)
License: MIT
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

from tests.utils.test_base_classes import DatabaseTestBase
from tests.utils.test_fixtures import TestDataFactory, MockFactory, TestFileManager


class TestMigrationScriptsInitialization(DatabaseTestBase):
    """Test migration scripts initialization."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        # Add the agent workspace to the path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.mark.unit
    def test_migration_scripts_initialization(self, migration_scripts):
        """Test migration scripts initialization."""
        assert migration_scripts is not None
        assert hasattr(migration_scripts, 'db_path')
        assert hasattr(migration_scripts, 'backup_dir')
        assert migration_scripts.db_path.endswith("test.db")
        assert migration_scripts.backup_dir.endswith("backups")
    
    @pytest.mark.unit
    def test_migration_scripts_database_creation(self, migration_scripts):
        """Test migration scripts database creation."""
        # Test database file creation
        migration_scripts.create_database()
        
        assert os.path.exists(migration_scripts.db_path)
        assert os.path.isfile(migration_scripts.db_path)
        
        # Test database connection
        conn = sqlite3.connect(migration_scripts.db_path)
        self.assert_database_connection(conn)
        conn.close()


class TestMigrationScriptsBackup(DatabaseTestBase):
    """Test migration scripts backup functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.mark.unit
    def test_backup_directory_creation(self, migration_scripts):
        """Test backup directory creation."""
        # Create backup directory
        migration_scripts.create_backup_directory()
        
        assert os.path.exists(migration_scripts.backup_dir)
        assert os.path.isdir(migration_scripts.backup_dir)
    
    @pytest.mark.unit
    def test_database_backup_creation(self, migration_scripts):
        """Test database backup creation."""
        # Create initial database
        migration_scripts.create_database()
        
        # Create backup
        backup_path = migration_scripts.create_backup()
        
        self.assert_backup_creation(backup_path)
        assert backup_path.startswith(migration_scripts.backup_dir)
        assert backup_path.endswith('.db')
    
    @pytest.mark.unit
    def test_backup_validation(self, migration_scripts):
        """Test backup validation."""
        # Create initial database with some data
        migration_scripts.create_database()
        
        # Add some test data
        conn = sqlite3.connect(migration_scripts.db_path)
        conn.execute("CREATE TABLE test_table (id INTEGER, name TEXT)")
        conn.execute("INSERT INTO test_table VALUES (1, 'test')")
        conn.commit()
        conn.close()
        
        # Create backup
        backup_path = migration_scripts.create_backup()
        
        # Validate backup
        assert migration_scripts.validate_backup(backup_path) == True
        
        # Test backup contains data
        backup_conn = sqlite3.connect(backup_path)
        cursor = backup_conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM test_table")
        count = cursor.fetchone()[0]
        assert count == 1
        backup_conn.close()


class TestMigrationScriptsDataMigration(DatabaseTestBase):
    """Test migration scripts data migration functionality."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.fixture
    def sample_agent_workspace(self, temp_dir):
        """Create sample agent workspace structure."""
        return TestFileManager.create_test_workspace_structure(temp_dir, "Agent-3")
    
    @pytest.mark.integration
    def test_agent_workspace_migration(self, migration_scripts, sample_agent_workspace):
        """Test agent workspace data migration."""
        # Create database
        migration_scripts.create_database()
        
        # Migrate agent workspace data
        migration_scripts.migrate_agent_workspace_data(str(sample_agent_workspace))
        
        # Verify data migration
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Check if tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'agent_status' in tables
        assert 'working_tasks' in tables
        assert 'future_tasks' in tables
        
        conn.close()
    
    @pytest.mark.integration
    def test_configuration_migration(self, migration_scripts, temp_dir):
        """Test configuration data migration."""
        # Create sample configuration
        config_dir = Path(temp_dir) / "config"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        coordinates_data = TestDataFactory.create_coordinates_data()
        with open(config_dir / "coordinates.json", 'w') as f:
            json.dump(coordinates_data, f)
        
        # Create database
        migration_scripts.create_database()
        
        # Migrate configuration data
        migration_scripts.migrate_configuration_data(str(config_dir))
        
        # Verify configuration migration
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Check if configuration tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert 'agent_coordinates' in tables
        
        conn.close()
    
    @pytest.mark.integration
    def test_data_integrity_validation(self, migration_scripts, sample_agent_workspace):
        """Test data integrity validation after migration."""
        # Create database and migrate data
        migration_scripts.create_database()
        migration_scripts.migrate_agent_workspace_data(str(sample_agent_workspace))
        
        # Validate data integrity
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Check agent status data
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM agent_status")
        status_count = cursor.fetchone()[0]
        assert status_count > 0
        
        # Check working tasks data
        cursor.execute("SELECT COUNT(*) FROM working_tasks")
        tasks_count = cursor.fetchone()[0]
        assert tasks_count > 0
        
        conn.close()


class TestMigrationScriptsSchemaValidation(DatabaseTestBase):
    """Test migration scripts schema validation."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.mark.unit
    def test_schema_creation(self, migration_scripts):
        """Test database schema creation."""
        # Create database with schema
        migration_scripts.create_database()
        migration_scripts.create_schema()
        
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Verify schema creation
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Check for expected tables
        expected_tables = [
            'agent_status',
            'working_tasks', 
            'future_tasks',
            'agent_coordinates',
            'migration_log'
        ]
        
        for table in expected_tables:
            assert table in tables, f"Table {table} not found in schema"
        
        conn.close()
    
    @pytest.mark.unit
    def test_table_structure_validation(self, migration_scripts):
        """Test table structure validation."""
        # Create database with schema
        migration_scripts.create_database()
        migration_scripts.create_schema()
        
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Validate agent_status table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(agent_status)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['agent_id', 'status', 'team', 'specialization']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in agent_status table"
        
        conn.close()
    
    @pytest.mark.unit
    def test_index_creation(self, migration_scripts):
        """Test index creation."""
        # Create database with schema
        migration_scripts.create_database()
        migration_scripts.create_schema()
        
        conn = sqlite3.connect(migration_scripts.db_path)
        
        # Check for indexes
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cursor.fetchall()]
        
        # Should have indexes for performance
        assert len(indexes) > 0, "No indexes found in database"
        
        conn.close()


class TestMigrationScriptsErrorHandling(DatabaseTestBase):
    """Test migration scripts error handling."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.mark.unit
    def test_database_connection_error_handling(self, migration_scripts):
        """Test database connection error handling."""
        # Test with invalid database path
        invalid_db_path = "/invalid/path/test.db"
        migration_scripts.db_path = invalid_db_path
        
        # Should handle error gracefully
        try:
            migration_scripts.create_database()
            # If we get here, it should have handled the error
            assert True
        except Exception as e:
            # Should be a specific database error
            assert "database" in str(e).lower() or "sqlite" in str(e).lower()
    
    @pytest.mark.unit
    def test_backup_error_handling(self, migration_scripts):
        """Test backup error handling."""
        # Test with invalid backup directory
        invalid_backup_dir = "/invalid/path/backups"
        migration_scripts.backup_dir = invalid_backup_dir
        
        # Should handle error gracefully
        try:
            migration_scripts.create_backup_directory()
            # If we get here, it should have handled the error
            assert True
        except Exception as e:
            # Should be a file system error
            assert "permission" in str(e).lower() or "directory" in str(e).lower()
    
    @pytest.mark.unit
    def test_migration_error_handling(self, migration_scripts):
        """Test migration error handling."""
        # Create database
        migration_scripts.create_database()
        
        # Test migration with invalid workspace path
        invalid_workspace = "/invalid/path/workspace"
        
        # Should handle error gracefully
        try:
            migration_scripts.migrate_agent_workspace_data(invalid_workspace)
            # If we get here, it should have handled the error
            assert True
        except Exception as e:
            # Should be a file system error
            assert "file" in str(e).lower() or "directory" in str(e).lower()


class TestMigrationScriptsPerformance(DatabaseTestBase):
    """Test migration scripts performance."""
    
    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for testing."""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def migration_scripts(self, temp_dir):
        """Create AutomatedMigrationScripts instance with temp directory."""
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from automated_migration_scripts import AutomatedMigrationScripts
        
        db_path = os.path.join(temp_dir, "test.db")
        backup_dir = os.path.join(temp_dir, "backups")
        return AutomatedMigrationScripts(db_path, backup_dir)
    
    @pytest.mark.performance
    def test_database_creation_performance(self, migration_scripts):
        """Test database creation performance."""
        def create_db():
            migration_scripts.create_database()
            migration_scripts.create_schema()
        
        # Should be fast (less than 1 second)
        self.assert_performance_threshold(create_db, 'database_query', 1)
    
    @pytest.mark.performance
    def test_backup_creation_performance(self, migration_scripts):
        """Test backup creation performance."""
        # Create initial database
        migration_scripts.create_database()
        
        def create_backup():
            return migration_scripts.create_backup()
        
        # Should be fast (less than 2 seconds)
        self.assert_performance_threshold(create_backup, 'database_query', 1)
    
    @pytest.mark.performance
    def test_data_migration_performance(self, migration_scripts, sample_agent_workspace):
        """Test data migration performance."""
        # Create database
        migration_scripts.create_database()
        
        def migrate_data():
            migration_scripts.migrate_agent_workspace_data(str(sample_agent_workspace))
        
        # Should be fast (less than 5 seconds)
        self.assert_performance_threshold(migrate_data, 'database_query', 1)




