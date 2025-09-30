#!/usr/bin/env python3
"""
Database Schema Implementation Tests - Modular Test Suite
=========================================================

Tests for database schema implementation functionality.
Tests table creation, data insertion, and schema validation.

V2 COMPLIANT: Modular architecture with separate models and core logic.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import sqlite3
import tempfile
from pathlib import Path

import pytest

from tests.utils.test_base_classes import DatabaseTestBase
from tests.utils.test_fixtures import TestDataFactory, TestFileManager
from .test_schema_core import SchemaTestCore
from .test_schema_models import (
    TestDatabaseConfig,
    TestPerformanceMetrics,
    TestResult,
    TestSchemaData,
    TestSchemaInfo,
    TestValidationResult,
)


class TestSchemaImplementationCore(DatabaseTestBase):
    """Test schema implementation core functionality."""

    @pytest.fixture
    def temp_database(self):
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix=".db")
        conn = sqlite3.connect(db_path)
        conn.close()
        yield db_path
        TestFileManager.cleanup_file(db_path)

    @pytest.fixture
    def schema_implementation(self, temp_database):
        """Create schema implementation instance."""
        core = SchemaTestCore()
        return core.create_schema_implementation(temp_database)

    @pytest.fixture
    def test_core(self):
        """Create test core instance."""
        return SchemaTestCore()

    @pytest.fixture
    def sample_table_data(self):
        """Create sample table data for testing."""
        return TestSchemaData(
            table_name="test_table",
            columns=["id INTEGER PRIMARY KEY", "name TEXT", "value REAL"],
            data=[
                {"id": 1, "name": "test1", "value": 1.5},
                {"id": 2, "name": "test2", "value": 2.5},
                {"id": 3, "name": "test3", "value": 3.5},
            ],
        )

    @pytest.fixture
    def sample_schema_info(self):
        """Create sample schema info for testing."""
        return TestSchemaInfo(
            schema_name="test_schema",
            version="1.0",
            tables=["test_table"],
            indexes=["idx_test_name"],
            triggers=["trg_test_update"],
        )

    @pytest.mark.unit
    def test_table_creation(self, schema_implementation, test_core, sample_table_data):
        """Test table creation functionality."""
        result = test_core.test_table_creation(schema_implementation, sample_table_data)
        assert result.success, f"Table creation failed: {result.error_message}"
        assert result.data_count > 0, "No tables found after creation"

    @pytest.mark.unit
    def test_data_insertion(self, schema_implementation, test_core, sample_table_data):
        """Test data insertion functionality."""
        # First create the table
        test_core.test_table_creation(schema_implementation, sample_table_data)
        
        # Then test data insertion
        result = test_core.test_data_insertion(schema_implementation, sample_table_data)
        assert result.success, f"Data insertion failed: {result.error_message}"
        assert result.data_count == len(sample_table_data.data), "Data count mismatch"

    @pytest.mark.unit
    def test_schema_validation(self, schema_implementation, test_core, sample_schema_info):
        """Test schema validation functionality."""
        result = test_core.test_schema_validation(schema_implementation, sample_schema_info)
        assert result.passed, f"Schema validation failed: {result.details}"
        assert result.validation_type == "schema_validation"

    @pytest.mark.unit
    def test_performance_metrics(self, schema_implementation, test_core):
        """Test performance metrics."""
        metrics = test_core.test_performance_metrics(schema_implementation)
        assert metrics.query_time >= 0, "Query time should be non-negative"
        assert metrics.memory_usage >= 0, "Memory usage should be non-negative"
        assert metrics.disk_usage >= 0, "Disk usage should be non-negative"
        assert metrics.connection_count >= 0, "Connection count should be non-negative"

    @pytest.mark.unit
    def test_data_integrity(self, schema_implementation, test_core, sample_table_data):
        """Test data integrity constraints."""
        # First create the table and insert data
        test_core.test_table_creation(schema_implementation, sample_table_data)
        test_core.test_data_insertion(schema_implementation, sample_table_data)
        
        # Then test data integrity
        result = test_core.test_data_integrity(schema_implementation, sample_table_data.table_name)
        assert result.passed, f"Data integrity test failed: {result.details}"

    @pytest.mark.unit
    def test_backup_restore(self, schema_implementation, test_core, sample_table_data):
        """Test backup and restore functionality."""
        # First create the table and insert data
        test_core.test_table_creation(schema_implementation, sample_table_data)
        test_core.test_data_insertion(schema_implementation, sample_table_data)
        
        # Then test backup and restore
        backup_path = tempfile.mktemp(suffix=".backup")
        result = test_core.test_backup_restore(schema_implementation, backup_path)
        assert result.success, f"Backup/restore failed: {result.error_message}"

    @pytest.mark.unit
    def test_concurrent_access(self, schema_implementation, test_core):
        """Test concurrent database access."""
        result = test_core.test_concurrent_access(schema_implementation)
        assert result.success, f"Concurrent access test failed: {result.error_message}"
        assert result.data_count == 5, "Expected 5 concurrent operations"

    @pytest.mark.integration
    def test_full_schema_workflow(self, schema_implementation, test_core, sample_table_data, sample_schema_info):
        """Test complete schema workflow."""
        # Test table creation
        creation_result = test_core.test_table_creation(schema_implementation, sample_table_data)
        assert creation_result.success, "Table creation failed in workflow test"
        
        # Test data insertion
        insertion_result = test_core.test_data_insertion(schema_implementation, sample_table_data)
        assert insertion_result.success, "Data insertion failed in workflow test"
        
        # Test schema validation
        validation_result = test_core.test_schema_validation(schema_implementation, sample_schema_info)
        assert validation_result.passed, "Schema validation failed in workflow test"
        
        # Test performance metrics
        metrics = test_core.test_performance_metrics(schema_implementation)
        assert metrics.query_time >= 0, "Performance metrics failed in workflow test"
        
        # Test data integrity
        integrity_result = test_core.test_data_integrity(schema_implementation, sample_table_data.table_name)
        assert integrity_result.passed, "Data integrity failed in workflow test"

    @pytest.mark.performance
    def test_large_dataset_performance(self, schema_implementation, test_core):
        """Test performance with large dataset."""
        # Create large dataset
        large_data = TestSchemaData(
            table_name="large_table",
            columns=["id INTEGER PRIMARY KEY", "data TEXT"],
            data=[{"id": i, "data": f"data_{i}"} for i in range(1000)],
        )
        
        # Test table creation
        creation_result = test_core.test_table_creation(schema_implementation, large_data)
        assert creation_result.success, "Large table creation failed"
        
        # Test data insertion
        insertion_result = test_core.test_data_insertion(schema_implementation, large_data)
        assert insertion_result.success, "Large data insertion failed"
        
        # Test performance metrics
        metrics = test_core.test_performance_metrics(schema_implementation)
        assert metrics.query_time < 1.0, "Query time too slow for large dataset"
        assert metrics.memory_usage < 100, "Memory usage too high for large dataset"

    @pytest.mark.stress
    def test_stress_testing(self, schema_implementation, test_core):
        """Test stress testing scenarios."""
        # Test multiple concurrent operations
        results = []
        for _ in range(10):
            result = test_core.test_concurrent_access(schema_implementation)
            results.append(result.success)
        
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.8, f"Stress test success rate too low: {success_rate}"

    @pytest.mark.error_handling
    def test_error_handling(self, schema_implementation, test_core):
        """Test error handling scenarios."""
        # Test with invalid table data
        invalid_data = TestSchemaData(
            table_name="",  # Empty table name
            columns=[],  # Empty columns
            data=[],  # Empty data
        )
        
        result = test_core.test_table_creation(schema_implementation, invalid_data)
        assert not result.success, "Should fail with invalid table data"
        assert result.error_message is not None, "Should have error message"

    @pytest.mark.cleanup
    def test_cleanup_functionality(self, schema_implementation, test_core, sample_table_data):
        """Test cleanup functionality."""
        # Create table and data
        test_core.test_table_creation(schema_implementation, sample_table_data)
        test_core.test_data_insertion(schema_implementation, sample_table_data)
        
        # Test cleanup
        schema_implementation.cleanup_table(sample_table_data.table_name)
        
        # Verify cleanup
        tables = schema_implementation.get_tables()
        assert sample_table_data.table_name not in tables, "Table not cleaned up properly"