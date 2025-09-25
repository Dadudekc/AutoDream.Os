#!/usr/bin/env python3
"""
Database Schema Implementation Tests - Modular Test Suite
=========================================================

Tests for database schema implementation functionality.
Tests table creation, data insertion, and schema validation.

Author: Agent-3 (Database Specialist)
License: MIT
"""

import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

from tests.utils.test_base_classes import DatabaseTestBase
from tests.utils.test_fixtures import TestDataFactory, MockFactory, TestFileManager


class TestSchemaImplementationCore(DatabaseTestBase):
    """Test schema implementation core functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        # Add the agent workspace to the path
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        return SchemaImplementation(temp_database)
    
    @pytest.mark.unit
    def test_schema_implementation_initialization(self, schema_implementation, temp_database):
        """Test schema implementation initialization."""
        assert schema_implementation is not None
        assert hasattr(schema_implementation, 'db_path')
        assert schema_implementation.db_path == temp_database
    
    @pytest.mark.unit
    def test_database_connection(self, schema_implementation):
        """Test database connection."""
        conn = schema_implementation.get_connection()
        self.assert_database_connection(conn)
        conn.close()
    
    @pytest.mark.unit
    def test_database_creation(self, schema_implementation):
        """Test database creation."""
        # Database should already exist from fixture
        assert Path(schema_implementation.db_path).exists()
        assert Path(schema_implementation.db_path).is_file()


class TestSchemaTableCreation(DatabaseTestBase):
    """Test schema table creation functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        return SchemaImplementation(temp_database)
    
    @pytest.mark.unit
    def test_agent_status_table_creation(self, schema_implementation):
        """Test agent status table creation."""
        schema_implementation.create_agent_status_table()
        
        conn = schema_implementation.get_connection()
        self.assert_table_exists(conn, 'agent_status')
        
        # Verify table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(agent_status)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['agent_id', 'status', 'team', 'specialization', 'captain']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in agent_status table"
        
        conn.close()
    
    @pytest.mark.unit
    def test_working_tasks_table_creation(self, schema_implementation):
        """Test working tasks table creation."""
        schema_implementation.create_working_tasks_table()
        
        conn = schema_implementation.get_connection()
        self.assert_table_exists(conn, 'working_tasks')
        
        # Verify table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(working_tasks)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['task_id', 'title', 'status', 'priority', 'assigned_to']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in working_tasks table"
        
        conn.close()
    
    @pytest.mark.unit
    def test_future_tasks_table_creation(self, schema_implementation):
        """Test future tasks table creation."""
        schema_implementation.create_future_tasks_table()
        
        conn = schema_implementation.get_connection()
        self.assert_table_exists(conn, 'future_tasks')
        
        # Verify table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(future_tasks)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['task_id', 'title', 'priority', 'estimated_duration']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in future_tasks table"
        
        conn.close()
    
    @pytest.mark.unit
    def test_agent_coordinates_table_creation(self, schema_implementation):
        """Test agent coordinates table creation."""
        schema_implementation.create_agent_coordinates_table()
        
        conn = schema_implementation.get_connection()
        self.assert_table_exists(conn, 'agent_coordinates')
        
        # Verify table structure
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(agent_coordinates)")
        columns = cursor.fetchall()
        
        column_names = [col[1] for col in columns]
        expected_columns = ['agent_id', 'x_coordinate', 'y_coordinate', 'active']
        
        for col in expected_columns:
            assert col in column_names, f"Column {col} not found in agent_coordinates table"
        
        conn.close()
    
    @pytest.mark.unit
    def test_all_tables_creation(self, schema_implementation):
        """Test all tables creation."""
        schema_implementation.create_all_tables()
        
        conn = schema_implementation.get_connection()
        
        # Check all expected tables exist
        expected_tables = [
            'agent_status',
            'working_tasks',
            'future_tasks',
            'agent_coordinates'
        ]
        
        for table in expected_tables:
            self.assert_table_exists(conn, table)
        
        conn.close()


class TestSchemaDataOperations(DatabaseTestBase):
    """Test schema data operations functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        schema = SchemaImplementation(temp_database)
        schema.create_all_tables()
        return schema
    
    @pytest.mark.unit
    def test_agent_status_data_insertion(self, schema_implementation):
        """Test agent status data insertion."""
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        
        schema_implementation.insert_agent_status(agent_data)
        
        conn = schema_implementation.get_connection()
        self.assert_data_insertion(conn, 'agent_status', 1)
        
        # Verify data content
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agent_status WHERE agent_id = ?", ("Agent-1",))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] == "Agent-1"  # agent_id
        assert row[1] == "active"    # status
        
        conn.close()
    
    @pytest.mark.unit
    def test_working_tasks_data_insertion(self, schema_implementation):
        """Test working tasks data insertion."""
        task_data = TestDataFactory.create_working_tasks_data()
        current_task = task_data['current_task']
        
        schema_implementation.insert_working_task(current_task)
        
        conn = schema_implementation.get_connection()
        self.assert_data_insertion(conn, 'working_tasks', 1)
        
        # Verify data content
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM working_tasks WHERE task_id = ?", (current_task['id'],))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] == current_task['id']  # task_id
        assert row[1] == current_task['title']  # title
        
        conn.close()
    
    @pytest.mark.unit
    def test_future_tasks_data_insertion(self, schema_implementation):
        """Test future tasks data insertion."""
        future_tasks_data = TestDataFactory.create_future_tasks_data()
        task = future_tasks_data['available_tasks'][0]
        
        schema_implementation.insert_future_task(task)
        
        conn = schema_implementation.get_connection()
        self.assert_data_insertion(conn, 'future_tasks', 1)
        
        # Verify data content
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM future_tasks WHERE task_id = ?", (task['id'],))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] == task['id']  # task_id
        assert row[1] == task['title']  # title
        
        conn.close()
    
    @pytest.mark.unit
    def test_agent_coordinates_data_insertion(self, schema_implementation):
        """Test agent coordinates data insertion."""
        coordinates_data = TestDataFactory.create_coordinates_data()
        agent_data = coordinates_data['agents']['Agent-1']
        
        schema_implementation.insert_agent_coordinates("Agent-1", agent_data)
        
        conn = schema_implementation.get_connection()
        self.assert_data_insertion(conn, 'agent_coordinates', 1)
        
        # Verify data content
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM agent_coordinates WHERE agent_id = ?", ("Agent-1",))
        row = cursor.fetchone()
        
        assert row is not None
        assert row[0] == "Agent-1"  # agent_id
        assert row[1] == agent_data['chat_input_coordinates'][0]  # x_coordinate
        assert row[2] == agent_data['chat_input_coordinates'][1]  # y_coordinate
        
        conn.close()


class TestSchemaDataRetrieval(DatabaseTestBase):
    """Test schema data retrieval functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance with test data."""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        schema = SchemaImplementation(temp_database)
        schema.create_all_tables()
        
        # Insert test data
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        schema.insert_agent_status(agent_data)
        
        task_data = TestDataFactory.create_working_tasks_data()
        schema.insert_working_task(task_data['current_task'])
        
        future_tasks_data = TestDataFactory.create_future_tasks_data()
        schema.insert_future_task(future_tasks_data['available_tasks'][0])
        
        coordinates_data = TestDataFactory.create_coordinates_data()
        schema.insert_agent_coordinates("Agent-1", coordinates_data['agents']['Agent-1'])
        
        return schema
    
    @pytest.mark.unit
    def test_agent_status_retrieval(self, schema_implementation):
        """Test agent status data retrieval."""
        agent_status = schema_implementation.get_agent_status("Agent-1")
        
        assert agent_status is not None
        assert agent_status['agent_id'] == "Agent-1"
        assert agent_status['status'] == "active"
    
    @pytest.mark.unit
    def test_working_tasks_retrieval(self, schema_implementation):
        """Test working tasks data retrieval."""
        working_tasks = schema_implementation.get_working_tasks()
        
        assert working_tasks is not None
        assert len(working_tasks) > 0
        assert working_tasks[0]['task_id'] == "DB_011"
    
    @pytest.mark.unit
    def test_future_tasks_retrieval(self, schema_implementation):
        """Test future tasks data retrieval."""
        future_tasks = schema_implementation.get_future_tasks()
        
        assert future_tasks is not None
        assert len(future_tasks) > 0
        assert future_tasks[0]['task_id'] == "DB_012"
    
    @pytest.mark.unit
    def test_agent_coordinates_retrieval(self, schema_implementation):
        """Test agent coordinates data retrieval."""
        coordinates = schema_implementation.get_agent_coordinates("Agent-1")
        
        assert coordinates is not None
        assert coordinates['agent_id'] == "Agent-1"
        assert coordinates['x_coordinate'] == -1269
        assert coordinates['y_coordinate'] == 481


class TestSchemaValidation(DatabaseTestBase):
    """Test schema validation functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        return SchemaImplementation(temp_database)
    
    @pytest.mark.unit
    def test_schema_validation_success(self, schema_implementation):
        """Test schema validation success."""
        schema_implementation.create_all_tables()
        
        validation_result = schema_implementation.validate_schema()
        
        assert validation_result is True
    
    @pytest.mark.unit
    def test_schema_validation_failure(self, schema_implementation):
        """Test schema validation failure."""
        # Don't create tables, so validation should fail
        validation_result = schema_implementation.validate_schema()
        
        assert validation_result is False
    
    @pytest.mark.unit
    def test_data_integrity_validation(self, schema_implementation):
        """Test data integrity validation."""
        schema_implementation.create_all_tables()
        
        # Insert valid data
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        schema_implementation.insert_agent_status(agent_data)
        
        integrity_result = schema_implementation.validate_data_integrity()
        
        assert integrity_result is True
    
    @pytest.mark.unit
    def test_foreign_key_validation(self, schema_implementation):
        """Test foreign key validation."""
        schema_implementation.create_all_tables()
        
        # Insert data with valid foreign keys
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        schema_implementation.insert_agent_status(agent_data)
        
        task_data = TestDataFactory.create_working_tasks_data()
        schema_implementation.insert_working_task(task_data['current_task'])
        
        fk_result = schema_implementation.validate_foreign_keys()
        
        assert fk_result is True


class TestSchemaPerformance(DatabaseTestBase):
    """Test schema performance functionality."""
    
    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix='.db')
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)
    
    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        import sys
        import os
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))
        
        from schema_implementation import SchemaImplementation
        
        schema = SchemaImplementation(temp_database)
        schema.create_all_tables()
        return schema
    
    @pytest.mark.performance
    def test_table_creation_performance(self, schema_implementation):
        """Test table creation performance."""
        def create_tables():
            schema_implementation.create_all_tables()
        
        # Should be fast (less than 1 second)
        self.assert_performance_threshold(create_tables, 'database_query', 1)
    
    @pytest.mark.performance
    def test_data_insertion_performance(self, schema_implementation):
        """Test data insertion performance."""
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        
        def insert_data():
            schema_implementation.insert_agent_status(agent_data)
        
        # Should be fast (less than 0.1 seconds)
        self.assert_performance_threshold(insert_data, 'database_query', 1)
    
    @pytest.mark.performance
    def test_data_retrieval_performance(self, schema_implementation):
        """Test data retrieval performance."""
        # Insert test data first
        agent_data = TestDataFactory.create_agent_status_data("Agent-1")
        schema_implementation.insert_agent_status(agent_data)
        
        def retrieve_data():
            return schema_implementation.get_agent_status("Agent-1")
        
        # Should be fast (less than 0.1 seconds)
        self.assert_performance_threshold(retrieve_data, 'database_query', 1)




