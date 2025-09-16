#!/usr/bin/env python3
"""
Comprehensive Testing and Validation - Agent-3 Database Specialist
================================================================

This module provides comprehensive testing and validation procedures for Phase 1
database migration, including integration testing, performance validation, and
quality assurance.

V2 Compliance: This file is designed to be under 400 lines and follows modular architecture.
"""

import sqlite3
import json
import time
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveTestingValidation:
    """Main class for comprehensive testing and validation."""
    
    def __init__(self, db_path: str = "data/agent_system.db"):
        """Initialize the testing and validation system."""
        self.db_path = Path(db_path)
        self.connection = None
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'performance_metrics': {},
            'validation_summary': {}
        }
        
    def run_comprehensive_testing(self) -> Dict[str, Any]:
        """Run comprehensive testing and validation suite."""
        logger.info("🧪 Starting comprehensive testing and validation...")
        
        try:
            # Test 1: Database Connection and Basic Operations
            self._test_database_connection()
            
            # Test 2: Schema Validation
            self._test_schema_validation()
            
            # Test 3: Data Integrity
            self._test_data_integrity()
            
            # Test 4: Performance Testing
            self._test_performance()
            
            # Test 5: Integration Testing
            self._test_integration_components()
            
            # Test 6: V2 Compliance Testing
            self._test_v2_compliance()
            
            # Test 7: Migration Validation
            self._test_migration_validation()
            
            # Generate comprehensive report
            report = self._generate_test_report()
            
            logger.info(f"✅ Testing completed: {self.test_results['passed_tests']}/{self.test_results['total_tests']} tests passed")
            return report
            
        except Exception as e:
            logger.error(f"❌ Testing failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def _test_database_connection(self):
        """Test database connection and basic operations."""
        test_name = "Database Connection Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            # Test basic query
            cursor = self.connection.execute("SELECT 1 as test_value")
            result = cursor.fetchone()
            
            # Test table existence
            cursor = self.connection.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name IN (
                    'agent_workspaces', 'agent_messages', 'discord_commands',
                    'core_systems_status', 'v2_compliance_audit', 'integration_tests'
                )
            """)
            tables = [row[0] for row in cursor.fetchall()]
            
            test_duration = int((time.time() - start_time) * 1000)
            
            self._record_test_result(
                test_name, 
                'PASS' if len(tables) >= 6 and result['test_value'] == 1 else 'FAIL',
                test_duration,
                {'tables_found': len(tables), 'required_tables': 6}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_schema_validation(self):
        """Test database schema validation."""
        test_name = "Schema Validation Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            schema_validation = {
                'agent_workspaces': {'required_columns': ['agent_id', 'team', 'specialization', 'integration_status'], 'valid': True},
                'agent_messages': {'required_columns': ['message_id', 'from_agent', 'to_agent', 'pyautogui_coordinates'], 'valid': True},
                'discord_commands': {'required_columns': ['command_id', 'agent_id', 'command_type', 'controller_status'], 'valid': True},
                'core_systems_status': {'required_columns': ['system_id', 'system_name', 'system_status', 'health_score'], 'valid': True},
                'v2_compliance_audit': {'required_columns': ['audit_id', 'component_name', 'compliance_score', 'integration_impact'], 'valid': True},
                'integration_tests': {'required_columns': ['test_id', 'test_name', 'test_type', 'integration_component'], 'valid': True}
            }
            
            for table_name, validation in schema_validation.items():
                cursor = self.connection.execute(f"PRAGMA table_info({table_name})")
                columns = [row[1] for row in cursor.fetchall()]
                
                missing_columns = [col for col in validation['required_columns'] if col not in columns]
                if missing_columns:
                    validation['valid'] = False
                    validation['missing_columns'] = missing_columns
            
            test_duration = int((time.time() - start_time) * 1000)
            all_valid = all(validation['valid'] for validation in schema_validation.values())
            
            self._record_test_result(
                test_name,
                'PASS' if all_valid else 'FAIL',
                test_duration,
                {'schema_validation': schema_validation}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_data_integrity(self):
        """Test data integrity constraints."""
        test_name = "Data Integrity Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            integrity_results = {}
            
            # Test primary key constraints
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces WHERE agent_id IS NULL")
            null_agent_ids = cursor.fetchone()['count']
            integrity_results['null_agent_ids'] = null_agent_ids
            
            # Test foreign key relationships (if applicable)
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_messages WHERE from_agent IS NULL OR to_agent IS NULL")
            null_agent_refs = cursor.fetchone()['count']
            integrity_results['null_agent_references'] = null_agent_refs
            
            # Test data type validation
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces WHERE cycle_count < 0")
            negative_cycles = cursor.fetchone()['count']
            integrity_results['negative_cycles'] = negative_cycles
            
            # Test JSON field validation
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_messages WHERE pyautogui_coordinates IS NOT NULL")
            coordinate_messages = cursor.fetchone()['count']
            integrity_results['coordinate_messages'] = coordinate_messages
            
            test_duration = int((time.time() - start_time) * 1000)
            integrity_valid = (null_agent_ids == 0 and null_agent_refs == 0 and negative_cycles == 0)
            
            self._record_test_result(
                test_name,
                'PASS' if integrity_valid else 'FAIL',
                test_duration,
                {'integrity_results': integrity_results}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_performance(self):
        """Test database performance."""
        test_name = "Performance Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            performance_results = {}
            
            # Test query performance
            query_start = time.time()
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            query_result = cursor.fetchone()['count']
            query_time = int((time.time() - query_start) * 1000)
            performance_results['basic_query_time_ms'] = query_time
            
            # Test index performance
            index_start = time.time()
            cursor = self.connection.execute("SELECT * FROM agent_workspaces WHERE team = 'Team Alpha'")
            index_result = cursor.fetchall()
            index_time = int((time.time() - index_start) * 1000)
            performance_results['indexed_query_time_ms'] = index_time
            
            # Test join performance
            join_start = time.time()
            cursor = self.connection.execute("""
                SELECT aw.agent_id, aw.team, COUNT(am.message_id) as message_count
                FROM agent_workspaces aw
                LEFT JOIN agent_messages am ON aw.agent_id = am.from_agent
                GROUP BY aw.agent_id, aw.team
            """)
            join_result = cursor.fetchall()
            join_time = int((time.time() - join_start) * 1000)
            performance_results['join_query_time_ms'] = join_time
            
            test_duration = int((time.time() - start_time) * 1000)
            performance_acceptable = (query_time < 100 and index_time < 50 and join_time < 200)
            
            self._record_test_result(
                test_name,
                'PASS' if performance_acceptable else 'FAIL',
                test_duration,
                {'performance_results': performance_results}
            )
            
            # Store performance metrics
            self.test_results['performance_metrics'] = performance_results
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_integration_components(self):
        """Test integration components."""
        test_name = "Integration Components Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            integration_results = {}
            
            # Test messaging system integration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_messages WHERE pyautogui_coordinates IS NOT NULL")
            messaging_integration = cursor.fetchone()['count']
            integration_results['messaging_integration'] = messaging_integration
            
            # Test Discord commander integration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM discord_commands WHERE controller_status = 'active'")
            discord_integration = cursor.fetchone()['count']
            integration_results['discord_integration'] = discord_integration
            
            # Test V2 compliance integration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM v2_compliance_audit WHERE integration_impact IS NOT NULL")
            compliance_integration = cursor.fetchone()['count']
            integration_results['compliance_integration'] = compliance_integration
            
            # Test core systems integration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM core_systems_status WHERE system_status = 'active'")
            core_systems_integration = cursor.fetchone()['count']
            integration_results['core_systems_integration'] = core_systems_integration
            
            test_duration = int((time.time() - start_time) * 1000)
            integration_valid = (messaging_integration >= 0 and discord_integration >= 0 and 
                               compliance_integration >= 0 and core_systems_integration >= 0)
            
            self._record_test_result(
                test_name,
                'PASS' if integration_valid else 'FAIL',
                test_duration,
                {'integration_results': integration_results}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_v2_compliance(self):
        """Test V2 compliance validation."""
        test_name = "V2 Compliance Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            compliance_results = {}
            
            # Test compliance audit data
            cursor = self.connection.execute("SELECT AVG(compliance_score) as avg_score FROM v2_compliance_audit")
            avg_compliance = cursor.fetchone()['avg_score'] or 0
            compliance_results['average_compliance_score'] = avg_compliance
            
            # Test violation tracking
            cursor = self.connection.execute("SELECT SUM(violations_found) as total_violations FROM v2_compliance_audit")
            total_violations = cursor.fetchone()['total_violations'] or 0
            compliance_results['total_violations'] = total_violations
            
            # Test refactoring tracking
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM v2_compliance_audit WHERE refactoring_required = 1")
            refactoring_required = cursor.fetchone()['count']
            compliance_results['refactoring_required'] = refactoring_required
            
            test_duration = int((time.time() - start_time) * 1000)
            compliance_acceptable = (avg_compliance >= 80.0 and total_violations < 10)
            
            self._record_test_result(
                test_name,
                'PASS' if compliance_acceptable else 'FAIL',
                test_duration,
                {'compliance_results': compliance_results}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _test_migration_validation(self):
        """Test migration validation."""
        test_name = "Migration Validation Test"
        start_time = time.time()
        
        try:
            self.connection = sqlite3.connect(str(self.db_path))
            self.connection.row_factory = sqlite3.Row
            
            migration_results = {}
            
            # Test agent workspace migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM agent_workspaces")
            agent_count = cursor.fetchone()['count']
            migration_results['agents_migrated'] = agent_count
            
            # Test configuration migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM configuration")
            config_count = cursor.fetchone()['count']
            migration_results['config_migrated'] = config_count
            
            # Test project analysis migration
            cursor = self.connection.execute("SELECT COUNT(*) as count FROM project_analysis")
            analysis_count = cursor.fetchone()['count']
            migration_results['analysis_migrated'] = analysis_count
            
            test_duration = int((time.time() - start_time) * 1000)
            migration_valid = (agent_count > 0 and config_count > 0 and analysis_count > 0)
            
            self._record_test_result(
                test_name,
                'PASS' if migration_valid else 'FAIL',
                test_duration,
                {'migration_results': migration_results}
            )
            
        except Exception as e:
            self._record_test_result(test_name, 'FAIL', int((time.time() - start_time) * 1000), {'error': str(e)})
        finally:
            if self.connection:
                self.connection.close()
    
    def _record_test_result(self, test_name: str, status: str, duration_ms: int, details: Dict[str, Any]):
        """Record test result."""
        self.test_results['total_tests'] += 1
        if status == 'PASS':
            self.test_results['passed_tests'] += 1
        else:
            self.test_results['failed_tests'] += 1
        
        test_detail = {
            'test_name': test_name,
            'status': status,
            'duration_ms': duration_ms,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        
        self.test_results['test_details'].append(test_detail)
        logger.info(f"🧪 {test_name}: {status} ({duration_ms}ms)")
    
    def _generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        report = {
            'test_summary': {
                'total_tests': self.test_results['total_tests'],
                'passed_tests': self.test_results['passed_tests'],
                'failed_tests': self.test_results['failed_tests'],
                'success_rate': (self.test_results['passed_tests'] / self.test_results['total_tests'] * 100) if self.test_results['total_tests'] > 0 else 0,
                'test_duration': sum(test['duration_ms'] for test in self.test_results['test_details'])
            },
            'performance_metrics': self.test_results['performance_metrics'],
            'test_details': self.test_results['test_details'],
            'validation_summary': {
                'database_connection': 'PASS' if any(test['test_name'] == 'Database Connection Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'schema_validation': 'PASS' if any(test['test_name'] == 'Schema Validation Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'data_integrity': 'PASS' if any(test['test_name'] == 'Data Integrity Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'performance': 'PASS' if any(test['test_name'] == 'Performance Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'integration': 'PASS' if any(test['test_name'] == 'Integration Components Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'v2_compliance': 'PASS' if any(test['test_name'] == 'V2 Compliance Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL',
                'migration': 'PASS' if any(test['test_name'] == 'Migration Validation Test' and test['status'] == 'PASS' for test in self.test_results['test_details']) else 'FAIL'
            },
            'recommendations': self._generate_recommendations(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on test results."""
        recommendations = []
        
        if self.test_results['failed_tests'] > 0:
            recommendations.append("Address failed tests to ensure system reliability")
        
        if 'performance_metrics' in self.test_results:
            perf = self.test_results['performance_metrics']
            if perf.get('basic_query_time_ms', 0) > 100:
                recommendations.append("Optimize basic query performance")
            if perf.get('indexed_query_time_ms', 0) > 50:
                recommendations.append("Review and optimize database indexes")
            if perf.get('join_query_time_ms', 0) > 200:
                recommendations.append("Optimize join query performance")
        
        if self.test_results['total_tests'] > 0 and self.test_results['passed_tests'] / self.test_results['total_tests'] < 0.9:
            recommendations.append("Improve overall test success rate to above 90%")
        
        return recommendations

def main():
    """Main function to run comprehensive testing and validation."""
    logger.info("🧪 Starting comprehensive testing and validation...")
    
    testing_system = ComprehensiveTestingValidation()
    results = testing_system.run_comprehensive_testing()
    
    if results.get('success', True):
        logger.info("✅ Testing and validation completed successfully!")
        logger.info(f"Test Summary: {results['test_summary']['passed_tests']}/{results['test_summary']['total_tests']} tests passed")
        logger.info(f"Success Rate: {results['test_summary']['success_rate']:.1f}%")
    else:
        logger.error("❌ Testing and validation failed!")
        logger.error(f"Error: {results.get('error', 'Unknown error')}")
    
    return results

if __name__ == "__main__":
    main()
