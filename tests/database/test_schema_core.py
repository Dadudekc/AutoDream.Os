#!/usr/bin/env python3
"""
Database Schema Test Core
========================

Core functionality for database schema implementation tests.

Author: Agent-8 (SSOT & System Integration Specialist)
License: MIT
"""

import sqlite3
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

from tests.utils.test_base_classes import DatabaseTestBase
from tests.utils.test_fixtures import TestDataFactory, TestFileManager
from .test_schema_models import (
    TestDatabaseConfig,
    TestPerformanceMetrics,
    TestResult,
    TestSchemaData,
    TestSchemaInfo,
    TestValidationResult,
)


class SchemaTestCore(DatabaseTestBase):
    """Core schema testing functionality."""

    def __init__(self):
        super().__init__()

    def create_temp_database(self) -> str:
        """Create temporary database for testing."""
        db_path = tempfile.mktemp(suffix=".db")
        conn = sqlite3.connect(db_path)
        conn.close()
        return db_path

    def cleanup_temp_database(self, db_path: str) -> None:
        """Cleanup temporary database."""
        TestFileManager.cleanup_file(db_path)

    def create_schema_implementation(self, db_path: str) -> Any:
        """Create schema implementation instance."""
        import os
        import sys

        sys.path.insert(
            0, os.path.join(os.path.dirname(__file__), "../../agent_workspaces/Agent-3")
        )

        from schema_implementation import SchemaImplementation

        return SchemaImplementation(db_path)

    def test_table_creation(self, schema_impl: Any, table_data: TestSchemaData) -> TestResult:
        """Test table creation functionality."""
        try:
            # Create table
            schema_impl.create_table(table_data.table_name, table_data.columns)
            
            # Verify table exists
            tables = schema_impl.get_tables()
            success = table_data.table_name in tables
            
            return TestResult(
                test_name="table_creation",
                success=success,
                data_count=len(tables),
            )
        except Exception as e:
            return TestResult(
                test_name="table_creation",
                success=False,
                error_message=str(e),
            )

    def test_data_insertion(self, schema_impl: Any, table_data: TestSchemaData) -> TestResult:
        """Test data insertion functionality."""
        try:
            # Insert test data
            for row in table_data.data:
                schema_impl.insert_data(table_data.table_name, row)
            
            # Verify data count
            count = schema_impl.get_row_count(table_data.table_name)
            success = count == len(table_data.data)
            
            return TestResult(
                test_name="data_insertion",
                success=success,
                data_count=count,
            )
        except Exception as e:
            return TestResult(
                test_name="data_insertion",
                success=False,
                error_message=str(e),
            )

    def test_schema_validation(self, schema_impl: Any, expected_schema: TestSchemaInfo) -> TestValidationResult:
        """Test schema validation functionality."""
        try:
            # Get current schema
            current_tables = schema_impl.get_tables()
            current_indexes = schema_impl.get_indexes()
            current_triggers = schema_impl.get_triggers()
            
            # Validate schema
            tables_match = set(current_tables) == set(expected_schema.tables)
            indexes_match = set(current_indexes) == set(expected_schema.indexes)
            triggers_match = set(current_triggers) == set(expected_schema.triggers)
            
            passed = tables_match and indexes_match and triggers_match
            
            details = {
                "tables_match": tables_match,
                "indexes_match": indexes_match,
                "triggers_match": triggers_match,
                "current_tables": current_tables,
                "expected_tables": expected_schema.tables,
            }
            
            recommendations = []
            if not tables_match:
                recommendations.append("Table structure needs adjustment")
            if not indexes_match:
                recommendations.append("Index configuration needs review")
            if not triggers_match:
                recommendations.append("Trigger setup needs verification")
            
            return TestValidationResult(
                validation_type="schema_validation",
                passed=passed,
                details=details,
                recommendations=recommendations,
            )
        except Exception as e:
            return TestValidationResult(
                validation_type="schema_validation",
                passed=False,
                details={"error": str(e)},
                recommendations=["Fix schema validation error"],
            )

    def test_performance_metrics(self, schema_impl: Any) -> TestPerformanceMetrics:
        """Test performance metrics."""
        import time
        import psutil
        import os
        
        start_time = time.time()
        
        # Execute test query
        schema_impl.execute_query("SELECT COUNT(*) FROM sqlite_master")
        
        query_time = time.time() - start_time
        
        # Get memory usage
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        # Get disk usage
        db_path = schema_impl.db_path
        disk_usage = os.path.getsize(db_path) / 1024 / 1024  # MB
        
        # Get connection count
        connection_count = schema_impl.get_connection_count()
        
        return TestPerformanceMetrics(
            query_time=query_time,
            memory_usage=memory_usage,
            disk_usage=disk_usage,
            connection_count=connection_count,
        )

    def test_data_integrity(self, schema_impl: Any, table_name: str) -> TestValidationResult:
        """Test data integrity constraints."""
        try:
            # Test foreign key constraints
            fk_violations = schema_impl.check_foreign_key_violations(table_name)
            
            # Test unique constraints
            unique_violations = schema_impl.check_unique_constraint_violations(table_name)
            
            # Test not null constraints
            null_violations = schema_impl.check_not_null_violations(table_name)
            
            passed = len(fk_violations) == 0 and len(unique_violations) == 0 and len(null_violations) == 0
            
            details = {
                "foreign_key_violations": len(fk_violations),
                "unique_violations": len(unique_violations),
                "null_violations": len(null_violations),
            }
            
            recommendations = []
            if fk_violations:
                recommendations.append("Fix foreign key constraint violations")
            if unique_violations:
                recommendations.append("Resolve unique constraint violations")
            if null_violations:
                recommendations.append("Address not null constraint violations")
            
            return TestValidationResult(
                validation_type="data_integrity",
                passed=passed,
                details=details,
                recommendations=recommendations,
            )
        except Exception as e:
            return TestValidationResult(
                validation_type="data_integrity",
                passed=False,
                details={"error": str(e)},
                recommendations=["Fix data integrity test error"],
            )

    def test_backup_restore(self, schema_impl: Any, backup_path: str) -> TestResult:
        """Test backup and restore functionality."""
        try:
            # Create backup
            schema_impl.create_backup(backup_path)
            
            # Verify backup exists
            backup_exists = Path(backup_path).exists()
            
            if backup_exists:
                # Test restore
                schema_impl.restore_from_backup(backup_path)
                restore_success = True
            else:
                restore_success = False
            
            success = backup_exists and restore_success
            
            return TestResult(
                test_name="backup_restore",
                success=success,
                data_count=1 if success else 0,
            )
        except Exception as e:
            return TestResult(
                test_name="backup_restore",
                success=False,
                error_message=str(e),
            )

    def test_concurrent_access(self, schema_impl: Any) -> TestResult:
        """Test concurrent database access."""
        try:
            import threading
            import time
            
            results = []
            
            def worker():
                try:
                    # Simulate concurrent access
                    schema_impl.execute_query("SELECT COUNT(*) FROM sqlite_master")
                    results.append(True)
                except Exception:
                    results.append(False)
            
            # Create multiple threads
            threads = []
            for _ in range(5):
                thread = threading.Thread(target=worker)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads
            for thread in threads:
                thread.join()
            
            success = all(results) and len(results) == 5
            
            return TestResult(
                test_name="concurrent_access",
                success=success,
                data_count=len(results),
            )
        except Exception as e:
            return TestResult(
                test_name="concurrent_access",
                success=False,
                error_message=str(e),
            )
