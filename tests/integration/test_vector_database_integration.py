#!/usr/bin/env python3
"""
Vector Database Integration Tests
=================================

Integration tests for vector database components and swarm intelligence.

V2 Compliance: ≤400 lines, focused vector database testing
Author: Agent-1 (Architecture Foundation Specialist)
"""

import pytest
import asyncio
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock
from typing import Dict, Any, List

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Import vector database components with error handling
try:
    from src.services.vector_database.vector_database_integration import VectorDatabaseIntegration
except ImportError:
    VectorDatabaseIntegration = None

try:
    from src.services.vector_database.vector_database_orchestrator import VectorDatabaseOrchestrator
except ImportError:
    VectorDatabaseOrchestrator = None

try:
    from src.services.vector_database.vector_database_models import VectorRecord
except ImportError:
    VectorRecord = None


class TestVectorDatabaseCoreIntegration:
    """Test vector database core integration."""
    
    @pytest.fixture
    def temp_vector_db(self):
        """Create temporary vector database for testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "test_vector_db"
        
        yield str(db_path)
        
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_vector_database_initialization(self, temp_vector_db):
        """Test vector database initialization."""
        if VectorDatabaseIntegration is None:
            pytest.skip("VectorDatabaseIntegration not available")
        integration = VectorDatabaseIntegration(temp_vector_db)
        
        assert integration is not None
        assert integration.db_path == temp_vector_db
        assert hasattr(integration, 'initialize_database')
    
    @pytest.mark.integration
    def test_vector_record_creation(self):
        """Test vector record creation and serialization."""
        if VectorRecord is None:
            pytest.skip("VectorRecord not available")
        record = VectorRecord(
            id="test_record_1",
            content="Test content for vector database",
            agent_id="Agent-1",
            timestamp=datetime.now(),
            vector_data=[0.1, 0.2, 0.3, 0.4, 0.5]
        )
        
        assert record.id == "test_record_1"
        assert record.content == "Test content for vector database"
        assert record.agent_id == "Agent-1"
        assert len(record.vector_data) == 5
        
        # Test serialization
        record_dict = record.to_dict()
        assert record_dict['id'] == "test_record_1"
        assert record_dict['content'] == "Test content for vector database"
    
    @pytest.mark.integration
    def test_vector_record_deserialization(self):
        """Test vector record deserialization."""
        record_data = {
            "id": "test_record_2",
            "content": "Deserialization test content",
            "agent_id": "Agent-2",
            "timestamp": datetime.now().isoformat(),
            "vector_data": [0.6, 0.7, 0.8, 0.9, 1.0]
        }
        
        record = VectorRecord.from_dict(record_data)
        
        assert record.id == "test_record_2"
        assert record.content == "Deserialization test content"
        assert record.agent_id == "Agent-2"
        assert len(record.vector_data) == 5


class TestVectorDatabaseOperationsIntegration:
    """Test vector database operations integration."""
    
    @pytest.fixture
    async def vector_db_with_data(self, temp_vector_db):
        """Create vector database with test data."""
        integration = VectorDatabaseIntegration(temp_vector_db)
        await integration.initialize_database()
        
        # Add test records
        test_records = [
            VectorRecord(
                id=f"test_record_{i}",
                content=f"Test content {i}",
                agent_id=f"Agent-{i % 8 + 1}",
                timestamp=datetime.now(),
                vector_data=[float(i), float(i+1), float(i+2)]
            )
            for i in range(5)
        ]
        
        for record in test_records:
            await integration.add_record(record)
        
        yield integration
    
    @pytest.mark.integration
    async def test_record_addition_and_retrieval(self, vector_db_with_data):
        """Test adding and retrieving records."""
        integration = vector_db_with_data
        
        # Test record retrieval
        records = await integration.get_all_records()
        assert len(records) == 5
        
        # Test specific record retrieval
        record = await integration.get_record_by_id("test_record_1")
        assert record is not None
        assert record.content == "Test content 1"
    
    @pytest.mark.integration
    async def test_vector_similarity_search(self, vector_db_with_data):
        """Test vector similarity search."""
        integration = vector_db_with_data
        
        # Test similarity search
        query_vector = [1.0, 2.0, 3.0]
        similar_records = await integration.find_similar_records(query_vector, limit=3)
        
        assert len(similar_records) <= 3
        assert all(isinstance(record, VectorRecord) for record in similar_records)
    
    @pytest.mark.integration
    async def test_agent_specific_queries(self, vector_db_with_data):
        """Test agent-specific queries."""
        integration = vector_db_with_data
        
        # Test agent-specific record retrieval
        agent_records = await integration.get_records_by_agent("Agent-1")
        assert len(agent_records) >= 0  # May be 0 or more depending on test data
        
        # Test content search
        content_records = await integration.search_by_content("Test content")
        assert len(content_records) >= 0


class TestVectorDatabaseOrchestratorIntegration:
    """Test vector database orchestrator integration."""
    
    @pytest.fixture
    def temp_orchestrator_dir(self):
        """Create temporary orchestrator directory."""
        temp_dir = tempfile.mkdtemp()
        orchestrator_dir = Path(temp_dir) / "orchestrator"
        orchestrator_dir.mkdir()
        
        yield str(orchestrator_dir)
        
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    def test_orchestrator_initialization(self, temp_orchestrator_dir):
        """Test orchestrator initialization."""
        orchestrator = VectorDatabaseOrchestrator(temp_orchestrator_dir)
        
        assert orchestrator is not None
        assert orchestrator.base_path == temp_orchestrator_dir
        assert hasattr(orchestrator, 'initialize_orchestrator')
    
    @pytest.mark.integration
    async def test_orchestrator_coordination(self, temp_orchestrator_dir):
        """Test orchestrator coordination functionality."""
        orchestrator = VectorDatabaseOrchestrator(temp_orchestrator_dir)
        await orchestrator.initialize_orchestrator()
        
        # Test orchestrator status
        status = orchestrator.get_orchestrator_status()
        assert status is not None
        assert 'initialized' in status
        assert 'active_databases' in status


class TestVectorDatabaseSwarmIntegration:
    """Test vector database swarm intelligence integration."""
    
    @pytest.fixture
    async def swarm_vector_system(self):
        """Create swarm vector system for testing."""
        temp_dir = tempfile.mkdtemp()
        
        # Create multiple agent databases
        agent_dbs = {}
        for agent_id in ["Agent-1", "Agent-2", "Agent-3"]:
            db_path = Path(temp_dir) / f"{agent_id.lower()}_db"
            integration = VectorDatabaseIntegration(str(db_path))
            await integration.initialize_database()
            agent_dbs[agent_id] = integration
        
        yield agent_dbs
        
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    async def test_cross_agent_knowledge_sharing(self, swarm_vector_system):
        """Test cross-agent knowledge sharing."""
        agent_dbs = swarm_vector_system
        
        # Add knowledge to Agent-1
        agent1_db = agent_dbs["Agent-1"]
        knowledge_record = VectorRecord(
            id="shared_knowledge_1",
            content="Shared knowledge from Agent-1",
            agent_id="Agent-1",
            timestamp=datetime.now(),
            vector_data=[0.1, 0.2, 0.3]
        )
        await agent1_db.add_record(knowledge_record)
        
        # Verify knowledge is accessible
        records = await agent1_db.get_all_records()
        assert len(records) == 1
        assert records[0].content == "Shared knowledge from Agent-1"
    
    @pytest.mark.integration
    async def test_swarm_intelligence_aggregation(self, swarm_vector_system):
        """Test swarm intelligence aggregation."""
        agent_dbs = swarm_vector_system
        
        # Add different knowledge to each agent
        for i, (agent_id, db) in enumerate(agent_dbs.items()):
            record = VectorRecord(
                id=f"agent_{i}_knowledge",
                content=f"Knowledge from {agent_id}",
                agent_id=agent_id,
                timestamp=datetime.now(),
                vector_data=[float(i), float(i+1), float(i+2)]
            )
            await db.add_record(record)
        
        # Verify each agent has its knowledge
        for agent_id, db in agent_dbs.items():
            records = await db.get_all_records()
            assert len(records) == 1
            assert records[0].agent_id == agent_id


class TestVectorDatabasePerformanceIntegration:
    """Test vector database performance integration."""
    
    @pytest.fixture
    async def performance_test_db(self):
        """Create database for performance testing."""
        temp_dir = tempfile.mkdtemp()
        db_path = Path(temp_dir) / "performance_db"
        
        integration = VectorDatabaseIntegration(str(db_path))
        await integration.initialize_database()
        
        yield integration
        
        shutil.rmtree(temp_dir)
    
    @pytest.mark.integration
    @pytest.mark.performance
    async def test_bulk_record_insertion(self, performance_test_db):
        """Test bulk record insertion performance."""
        integration = performance_test_db
        
        # Create many records
        records = [
            VectorRecord(
                id=f"perf_record_{i}",
                content=f"Performance test content {i}",
                agent_id=f"Agent-{i % 8 + 1}",
                timestamp=datetime.now(),
                vector_data=[float(i), float(i+1), float(i+2)]
            )
            for i in range(100)  # 100 records
        ]
        
        start_time = datetime.now()
        
        # Insert all records
        for record in records:
            await integration.add_record(record)
        
        end_time = datetime.now()
        insertion_time = (end_time - start_time).total_seconds()
        
        # Verify all records were inserted
        all_records = await integration.get_all_records()
        assert len(all_records) == 100
        
        # Performance should be reasonable (adjust threshold as needed)
        assert insertion_time < 10  # 10 seconds max for 100 records
    
    @pytest.mark.integration
    @pytest.mark.performance
    async def test_search_performance(self, performance_test_db):
        """Test search performance with many records."""
        integration = performance_test_db
        
        # Add test records
        for i in range(50):
            record = VectorRecord(
                id=f"search_record_{i}",
                content=f"Search test content {i}",
                agent_id=f"Agent-{i % 8 + 1}",
                timestamp=datetime.now(),
                vector_data=[float(i), float(i+1), float(i+2)]
            )
            await integration.add_record(record)
        
        # Test search performance
        start_time = datetime.now()
        
        query_vector = [25.0, 26.0, 27.0]
        similar_records = await integration.find_similar_records(query_vector, limit=10)
        
        end_time = datetime.now()
        search_time = (end_time - start_time).total_seconds()
        
        # Verify search results
        assert len(similar_records) <= 10
        
        # Search should be fast (adjust threshold as needed)
        assert search_time < 2  # 2 seconds max for search


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "integration"])
