#!/usr/bin/env python3
"""
Integration Tester
===================

Runs integration tests after migration.
"""

import sqlite3
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class IntegrationTester:
    """Runs integration tests after migration."""

    def __init__(self, db_path: Path):
        """Initialize integration tester."""
        self.db_path = db_path

    def run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests."""
        try:
            test_results = {
                'success': True,
                'tests_run': 0,
                'tests_passed': 0,
                'tests_failed': 0,
                'test_details': [],
                'errors': []
            }
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Test 1: Database connectivity
                connectivity_test = self._test_database_connectivity(cursor)
                test_results['tests_run'] += 1
                test_results['test_details'].append(connectivity_test)
                if connectivity_test['passed']:
                    test_results['tests_passed'] += 1
                else:
                    test_results['tests_failed'] += 1
                
                # Test 2: Table structure
                structure_test = self._test_table_structure(cursor)
                test_results['tests_run'] += 1
                test_results['test_details'].append(structure_test)
                if structure_test['passed']:
                    test_results['tests_passed'] += 1
                else:
                    test_results['tests_failed'] += 1
                
                # Test 3: Data integrity
                integrity_test = self._test_data_integrity(cursor)
                test_results['tests_run'] += 1
                test_results['test_details'].append(integrity_test)
                if integrity_test['passed']:
                    test_results['tests_passed'] += 1
                else:
                    test_results['tests_failed'] += 1
                
                # Test 4: Performance
                performance_test = self._test_performance(cursor)
                test_results['tests_run'] += 1
                test_results['test_details'].append(performance_test)
                if performance_test['passed']:
                    test_results['tests_passed'] += 1
                else:
                    test_results['tests_failed'] += 1
                
                # Overall success
                test_results['success'] = test_results['tests_failed'] == 0
                
                logger.info(f"Integration tests completed: {test_results['tests_passed']}/{test_results['tests_run']} passed")
                return test_results

        except Exception as e:
            logger.error(f"Integration tests failed: {e}")
            return {'success': False, 'error': str(e)}

    def _test_database_connectivity(self, cursor) -> Dict[str, Any]:
        """Test database connectivity."""
        try:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            return {
                'test_name': 'database_connectivity',
                'passed': result[0] == 1,
                'message': 'Database connectivity test passed' if result[0] == 1 else 'Database connectivity test failed'
            }
        except Exception as e:
            return {
                'test_name': 'database_connectivity',
                'passed': False,
                'message': f'Database connectivity test failed: {e}'
            }

    def _test_table_structure(self, cursor) -> Dict[str, Any]:
        """Test table structure."""
        try:
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
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            return {
                'test_name': 'table_structure',
                'passed': len(missing_tables) == 0,
                'message': f'All required tables present' if len(missing_tables) == 0 else f'Missing tables: {missing_tables}',
                'details': {
                    'required_tables': required_tables,
                    'existing_tables': existing_tables,
                    'missing_tables': missing_tables
                }
            }
        except Exception as e:
            return {
                'test_name': 'table_structure',
                'passed': False,
                'message': f'Table structure test failed: {e}'
            }

    def _test_data_integrity(self, cursor) -> Dict[str, Any]:
        """Test data integrity."""
        try:
            # Test foreign key constraints
# SECURITY: Key placeholder - replace with environment variable
            fk_violations = cursor.fetchall()
            
            # Test for orphaned records (example)
            cursor.execute("""
                SELECT COUNT(*) FROM agent_messages 
                WHERE from_agent NOT IN (SELECT agent_id FROM agent_workspaces)
            """)
            orphaned_messages = cursor.fetchone()[0]
            
            integrity_issues = []
            if fk_violations:
# SECURITY: Key placeholder - replace with environment variable
            if orphaned_messages > 0:
                integrity_issues.append(f"Orphaned messages: {orphaned_messages}")
            
            return {
                'test_name': 'data_integrity',
                'passed': len(integrity_issues) == 0,
                'message': 'Data integrity test passed' if len(integrity_issues) == 0 else f'Data integrity issues: {integrity_issues}',
                'details': {
# SECURITY: Key placeholder - replace with environment variable
                    'orphaned_messages': orphaned_messages
                }
            }
        except Exception as e:
            return {
                'test_name': 'data_integrity',
                'passed': False,
                'message': f'Data integrity test failed: {e}'
            }

    def _test_performance(self, cursor) -> Dict[str, Any]:
        """Test database performance."""
        try:
            import time
            
            # Test query performance
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM agent_workspaces")
            count = cursor.fetchone()[0]
            query_time = time.time() - start_time
            
            # Performance threshold: queries should complete in < 1 second
            performance_ok = query_time < 1.0
            
            return {
                'test_name': 'performance',
                'passed': performance_ok,
                'message': f'Performance test passed (query time: {query_time:.3f}s)' if performance_ok else f'Performance test failed (query time: {query_time:.3f}s)',
                'details': {
                    'query_time_seconds': query_time,
                    'record_count': count,
                    'performance_threshold': 1.0
                }
            }
        except Exception as e:
            return {
                'test_name': 'performance',
                'passed': False,
                'message': f'Performance test failed: {e}'
            }


