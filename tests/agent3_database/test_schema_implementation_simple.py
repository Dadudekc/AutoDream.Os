"""
Simple test suite for SQLite schema implementation
================================================

Tests for the DatabaseSchemaImplementation class including:
- Database creation
- Table creation
- Data migration
- Basic functionality
"""

import pytest
import sqlite3
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the agent workspace to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../agent_workspaces/Agent-3'))

from sqlite_schema_implementation import DatabaseSchemaImplementation


class TestDatabaseSchemaImplementation:
    """Test cases for DatabaseSchemaImplementation class."""
    
    @pytest.fixture
    def temp_db(self):
        """Create a temporary database for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = os.path.join(temp_dir, "test_schema.db")
        yield db_path
        os.unlink(db_path)
        os.rmdir(temp_dir)
    
    @pytest.fixture
    def schema_implementation(self, temp_db):
        """Create DatabaseSchemaImplementation instance with temp database."""
        return DatabaseSchemaImplementation(temp_db)
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_initialization(self, schema_implementation, temp_db):
        """Test DatabaseSchemaImplementation initialization."""
        assert schema_implementation.db_path == Path(temp_db)
        assert schema_implementation.connection is None
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_create_database(self, schema_implementation):
        """Test database creation."""
        result = schema_implementation.create_database()
        
        assert result is True
        assert schema_implementation.db_path.exists()
        
        # Verify tables were created
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN (
                'agent_workspaces', 'agent_messages', 'discord_commands',
                'integration_tests', 'v2_compliance_audit', 'file_compliance', 'message_archive'
            )
        """)
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        assert len(tables) == 7
        assert 'agent_workspaces' in tables
        assert 'agent_messages' in tables
        assert 'discord_commands' in tables
        assert 'integration_tests' in tables
        assert 'v2_compliance_audit' in tables
        assert 'file_compliance' in tables
        assert 'message_archive' in tables
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_agent_workspaces_table_structure(self, schema_implementation):
        """Test agent workspaces table structure."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("PRAGMA table_info(agent_workspaces)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        
        expected_columns = [
            'agent_id', 'team', 'specialization', 'captain', 'status',
            'last_cycle', 'current_focus', 'cycle_count', 'tasks_completed',
            'coordination_efficiency', 'v2_compliance', 'last_updated',
            'integration_status', 'integration_components', 'integration_tests_passed',
            'integration_tests_total'
        ]
        
        for column in expected_columns:
            assert column in columns
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_agent_messages_table_structure(self, schema_implementation):
        """Test agent messages table structure."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("PRAGMA table_info(agent_messages)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        
        expected_columns = [
            'message_id', 'from_agent', 'to_agent', 'priority', 'tags', 'content',
            'sent_at', 'processed_at', 'status', 'pyautogui_coordinates', 'delivery_method',
            'delivery_status', 'retry_count', 'max_retries'
        ]
        
        for column in expected_columns:
            assert column in columns
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_discord_commands_table_structure(self, schema_implementation):
        """Test Discord commands table structure."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("PRAGMA table_info(discord_commands)")
        columns = [row[1] for row in cursor.fetchall()]
        conn.close()
        
        expected_columns = [
            'command_id', 'agent_id', 'command_type', 'command_data', 'channel_id',
            'user_id', 'executed_at', 'execution_status', 'response_data',
            'controller_status', 'command_priority', 'execution_time_ms', 'error_message'
        ]
        
        for column in expected_columns:
            assert column in columns
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_indexes_creation(self, schema_implementation):
        """Test indexes creation."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='index' AND name LIKE 'idx_%'
        """)
        indexes = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_indexes = [
            'idx_agent_team', 'idx_agent_status', 'idx_agent_last_updated',
            'idx_message_to_agent', 'idx_message_status', 'idx_message_sent_at',
            'idx_discord_agent', 'idx_discord_status', 'idx_discord_executed',
            'idx_test_type', 'idx_test_status', 'idx_audit_component',
            'idx_audit_timestamp', 'idx_file_path', 'idx_file_status'
        ]
        
        for expected_index in expected_indexes:
            assert expected_index in indexes
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_views_creation(self, schema_implementation):
        """Test views creation."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='view'
        """)
        views = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        expected_views = [
            'agent_performance_summary', 'message_delivery_stats', 'v2_compliance_summary'
        ]
        
        for expected_view in expected_views:
            assert expected_view in views
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_data_insertion(self, schema_implementation):
        """Test data insertion."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        
        # Insert test data
        conn.execute("""
            INSERT INTO agent_workspaces 
            (agent_id, team, specialization, captain, status, cycle_count, tasks_completed, coordination_efficiency, v2_compliance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('Agent-1', 'Team Alpha', 'Integration', 'Agent-4', 'active', 5, 3, 95.0, 85.0))
        
        conn.commit()
        
        # Verify data was inserted
        cursor = conn.execute("SELECT * FROM agent_workspaces WHERE agent_id = ?", ('Agent-1',))
        row = cursor.fetchone()
        conn.close()
        
        assert row[0] == 'Agent-1'  # agent_id
        assert row[1] == 'Team Alpha'  # team
        assert row[7] == 5  # cycle_count
        assert row[8] == 3  # tasks_completed
        assert row[9] == 95.0  # coordination_efficiency
        assert row[10] == 85.0  # v2_compliance
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_json_field_handling(self, schema_implementation):
        """Test JSON field handling."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        
        # Test JSON field insertion
        coordinates = json.dumps({"x": 100, "y": 200, "agent": "Agent-1"})
        conn.execute("""
            INSERT INTO agent_messages 
            (message_id, from_agent, to_agent, priority, content, pyautogui_coordinates)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('msg_001', 'Agent-1', 'Agent-2', 'normal', 'Test message', coordinates))
        
        # Test JSON field retrieval
        cursor = conn.execute("""
            SELECT pyautogui_coordinates FROM agent_messages WHERE message_id = ?
        """, ('msg_001',))
        result = cursor.fetchone()[0]
        conn.close()
        
        parsed_coordinates = json.loads(result)
        assert parsed_coordinates['x'] == 100
        assert parsed_coordinates['y'] == 200
        assert parsed_coordinates['agent'] == 'Agent-1'
    
    @pytest.mark.integration
    @pytest.mark.agent3
    def test_migrate_existing_data(self, schema_implementation, temp_db):
        """Test data migration."""
        # Create sample agent workspace
        workspace_dir = Path(temp_db).parent / "agent_workspaces" / "Agent-3"
        workspace_dir.mkdir(parents=True, exist_ok=True)
        
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
        
        # Create database and migrate data
        schema_implementation.create_database()
        
        # Change to the temp directory to simulate the project root
        original_cwd = os.getcwd()
        try:
            os.chdir(Path(temp_db).parent)
            result = schema_implementation.migrate_existing_data()
            
            assert result is True
            
            # Verify data was migrated
            conn = sqlite3.connect(str(schema_implementation.db_path))
            cursor = conn.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            agent_count = cursor.fetchone()[0]
            conn.close()
            
            assert agent_count > 0
            
        finally:
            os.chdir(original_cwd)
    
    @pytest.mark.performance
    @pytest.mark.agent3
    def test_index_performance(self, schema_implementation):
        """Test index performance."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        
        # Insert test data
        for i in range(100):
            conn.execute("""
                INSERT INTO agent_workspaces 
                (agent_id, team, specialization, captain, status, cycle_count)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (f'Agent-{i}', f'Team-{i%4}', f'Specialization-{i}', f'Captain-{i}', 'active', i))
        
        conn.commit()
        
        # Test query performance with index
        import time
        start_time = time.time()
        cursor = conn.execute("SELECT * FROM agent_workspaces WHERE team = ?", ('Team-0',))
        results = cursor.fetchall()
        query_time = time.time() - start_time
        
        conn.close()
        
        assert len(results) == 25  # 100/4 = 25 agents per team
        assert query_time < 0.1  # Should be fast with index
    
    @pytest.mark.unit
    @pytest.mark.agent3
    def test_view_functionality(self, schema_implementation):
        """Test view functionality."""
        schema_implementation.create_database()
        
        conn = sqlite3.connect(str(schema_implementation.db_path))
        
        # Insert test data
        conn.execute("""
            INSERT INTO agent_workspaces 
            (agent_id, team, specialization, captain, status, cycle_count, tasks_completed, coordination_efficiency, v2_compliance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('Agent-1', 'Team Alpha', 'Integration', 'Agent-4', 'active', 5, 3, 95.0, 85.0))
        
        conn.execute("""
            INSERT INTO agent_workspaces 
            (agent_id, team, specialization, captain, status, cycle_count, tasks_completed, coordination_efficiency, v2_compliance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, ('Agent-2', 'Team Alpha', 'Architecture', 'Agent-4', 'active', 4, 2, 90.0, 88.0))
        
        conn.commit()
        
        # Test view query
        cursor = conn.execute("SELECT * FROM agent_performance_summary")
        results = cursor.fetchall()
        conn.close()
        
        assert len(results) == 1  # One team
        team_result = results[0]
        assert team_result[0] == 'Team Alpha'  # team
        assert team_result[1] == 2  # agent_count
        assert team_result[2] == 92.5  # avg_efficiency (95.0 + 90.0) / 2
        assert team_result[3] == 86.5  # avg_compliance (85.0 + 88.0) / 2
        assert team_result[4] == 5  # total_tasks (3 + 2)

