#!/usr/bin/env python3
"""
Test Suite for Advanced Parallel Testing Implementation
=====================================================

Comprehensive test suite for the advanced parallel testing engine
implemented in contract TEST-002.

Author: Agent-3 (TESTING FRAMEWORK ENHANCEMENT MANAGER)
Contract: TEST-002: Parallel Testing Implementation
Extra Credit: 200 points
"""

import unittest
import tempfile
import os
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock
import subprocess

# Add the tests directory to the path for imports
sys.path.insert(0, str(Path(__file__).parent))

from advanced_parallel_testing import (
    AdvancedParallelTestingEngine,
    TestExecutionMetrics
)

class TestTestExecutionMetrics(unittest.TestCase):
    """Test the TestExecutionMetrics dataclass."""
    
    def test_metrics_creation(self):
        """Test creating TestExecutionMetrics instance."""
        metrics = TestExecutionMetrics(
            test_count=10,
            execution_time=5.5,
            parallel_workers=4,
            cpu_utilization=75.0,
            memory_usage=128.5,
            throughput=2.0,
            efficiency_gain=60.0
        )
        
        self.assertEqual(metrics.test_count, 10)
        self.assertEqual(metrics.execution_time, 5.5)
        self.assertEqual(metrics.parallel_workers, 4)
        self.assertEqual(metrics.cpu_utilization, 75.0)
        self.assertEqual(metrics.memory_usage, 128.5)
        self.assertEqual(metrics.throughput, 2.0)
        self.assertEqual(metrics.efficiency_gain, 60.0)

class TestAdvancedParallelTestingEngine(unittest.TestCase):
    """Test the AdvancedParallelTestingEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = AdvancedParallelTestingEngine(max_workers=2)
        self.test_dir = Path(__file__).parent
        
    def tearDown(self):
        """Clean up test fixtures."""
        pass
    
    def test_engine_initialization(self):
        """Test engine initialization with custom worker count."""
        engine = AdvancedParallelTestingEngine(max_workers=4)
        self.assertEqual(engine.max_workers, 4)
        self.assertEqual(len(engine.worker_pool), 0)
        self.assertIsNotNone(engine.test_queue)
        self.assertIsNotNone(engine.results_queue)
        
    def test_engine_default_initialization(self):
        """Test engine initialization with default worker count."""
        engine = AdvancedParallelTestingEngine()
        self.assertGreater(engine.max_workers, 0)
        self.assertLessEqual(engine.max_workers, 8)
    
    def test_calculate_complexity_score(self):
        """Test complexity score calculation."""
        # Simple test content
        simple_content = "def test_simple(): pass"
        simple_score = self.engine._calculate_complexity_score(simple_content)
        self.assertEqual(simple_score, 1.0)
        
        # Complex test content
        complex_content = """
        import unittest
        class TestComplex(unittest.TestCase):
            def setUp(self):
                self.db = Database()
            def test_database_operation(self):
                result = self.db.query("SELECT * FROM users")
                self.assertIsNotNone(result)
        """
        complex_score = self.engine._calculate_complexity_score(complex_content)
        self.assertGreater(complex_score, 1.0)
        self.assertLessEqual(complex_score, 3.0)
        
        # Content with multiple complexity factors
        multi_factor_content = """
        import requests
        class TestNetwork(unittest.TestCase):
            def setUp(self):
                self.mock_service = Mock()
            def test_http_request(self):
                response = requests.get("http://api.example.com")
                self.assertEqual(response.status_code, 200)
        """
        multi_score = self.engine._calculate_complexity_score(multi_factor_content)
        self.assertGreater(multi_score, 2.0)
    
    def test_create_parallelization_groups(self):
        """Test parallelization group creation."""
        analysis = {
            "estimated_execution_times": {
                "test_file1.py": 2.0,
                "test_file2.py": 1.5,
                "test_file3.py": 3.0,
                "test_file4.py": 0.5
            }
        }
        
        groups = self.engine._create_parallelization_groups(analysis)
        
        # Should create groups based on worker count
        self.assertLessEqual(len(groups), self.engine.max_workers)
        
        # Each group should have files assigned
        for group in groups:
            self.assertIn("files", group)
            self.assertIn("worker_assignment", group)
            self.assertIn("total_estimated_time", group)
            self.assertGreater(len(group["files"]), 0)
    
    def test_compile_execution_summary(self):
        """Test execution summary compilation."""
        # Mock performance metrics
        mock_metrics = [
            TestExecutionMetrics(
                test_count=1,
                execution_time=2.0,
                parallel_workers=2,
                cpu_utilization=50.0,
                memory_usage=64.0,
                throughput=0.5,
                efficiency_gain=0.0
            ),
            TestExecutionMetrics(
                test_count=1,
                execution_time=3.0,
                parallel_workers=2,
                cpu_utilization=75.0,
                memory_usage=128.0,
                throughput=0.33,
                efficiency_gain=0.0
            )
        ]
        
        self.engine.performance_metrics = mock_metrics
        self.engine.execution_start_time = time.time() - 5.0
        self.engine.execution_end_time = time.time()
        
        summary = self.engine._compile_execution_summary()
        
        self.assertIn("execution_summary", summary)
        self.assertIn("performance_metrics", summary)
        self.assertIn("worker_performance", summary)
        
        exec_summary = summary["execution_summary"]
        self.assertIn("total_execution_time", exec_summary)
        self.assertIn("parallel_workers_used", exec_summary)
        self.assertIn("total_tests_executed", exec_summary)
        self.assertIn("efficiency_gain_percentage", exec_summary)
        self.assertIn("throughput_tests_per_second", exec_summary)
    
    def test_generate_performance_report(self):
        """Test performance report generation."""
        execution_summary = {
            "execution_summary": {
                "total_execution_time": 10.5,
                "parallel_workers_used": 4,
                "total_tests_executed": 20,
                "efficiency_gain_percentage": 65.5,
                "throughput_tests_per_second": 1.9
            },
            "worker_performance": {
                "worker_count": 4,
                "average_worker_utilization": 80.0,
                "memory_efficiency": 64.5
            }
        }
        
        report = self.engine.generate_performance_report(execution_summary)
        
        # Check that report contains expected sections
        self.assertIn("# Advanced Parallel Testing Performance Report", report)
        self.assertIn("## 🎯 Executive Summary", report)
        self.assertIn("## 📊 Performance Analysis", report)
        self.assertIn("## 🚀 Optimization Recommendations", report)
        
        # Check that values are included
        self.assertIn("10.50 seconds", report)
        self.assertIn("4", report)
        self.assertIn("20", report)
        self.assertIn("65.50%", report)
        self.assertIn("1.90 tests/second", report)
    
    @patch('subprocess.run')
    def test_execute_test_file_success(self, mock_run):
        """Test successful test file execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "test passed"
        mock_result.stderr = ""
        mock_run.return_value = mock_result
        
        result = self.engine._execute_test_file("test_file.py")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["return_code"], 0)
        self.assertEqual(result["stdout"], "test passed")
        self.assertEqual(result["stderr"], "")
    
    @patch('subprocess.run')
    def test_execute_test_file_failure(self, mock_run):
        """Test failed test file execution."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "test failed"
        mock_run.return_value = mock_result
        
        result = self.engine._execute_test_file("test_file.py")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["return_code"], 1)
        self.assertEqual(result["stderr"], "test failed")
    
    @patch('subprocess.run')
    def test_execute_test_file_timeout(self, mock_run):
        """Test test file execution timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("pytest", 300)
        
        result = self.engine._execute_test_file("test_file.py")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["return_code"], -1)
        self.assertEqual(result["stderr"], "Test execution timed out")
    
    def test_get_cpu_utilization(self):
        """Test CPU utilization calculation."""
        utilization = self.engine._get_cpu_utilization()
        self.assertGreaterEqual(utilization, 0.0)
    
    def test_get_memory_usage(self):
        """Test memory usage calculation."""
        # Test with psutil available
        try:
            import psutil
            memory = self.engine._get_memory_usage()
            self.assertGreaterEqual(memory, 0.0)
        except ImportError:
            # Test fallback when psutil not available
            memory = self.engine._get_memory_usage()
            self.assertEqual(memory, 0.0)

class TestAdvancedParallelTestingIntegration(unittest.TestCase):
    """Integration tests for the advanced parallel testing system."""
    
    def setUp(self):
        """Set up integration test fixtures."""
        self.engine = AdvancedParallelTestingEngine(max_workers=2)
        self.temp_dir = tempfile.mkdtemp()
        
        # Create test files for integration testing
        self._create_test_files()
    
    def tearDown(self):
        """Clean up integration test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def _create_test_files(self):
        """Create temporary test files for integration testing."""
        test_files = [
            ("test_simple.py", "def test_simple(): assert True"),
            ("test_medium.py", """
            import time
            def test_medium():
                time.sleep(0.1)
                assert True
            """),
            ("test_complex.py", """
            import time
            class TestComplex:
                def setup_method(self):
                    self.data = [1, 2, 3]
                def test_complex(self):
                    time.sleep(0.2)
                    assert len(self.data) == 3
            """)
        ]
        
        for filename, content in test_files:
            filepath = os.path.join(self.temp_dir, filename)
            with open(filepath, 'w') as f:
                f.write(content)
    
    def test_test_suite_analysis_integration(self):
        """Test complete test suite analysis workflow."""
        analysis = self.engine.analyze_test_suite(self.temp_dir)
        
        self.assertIn("total_tests", analysis)
        self.assertIn("test_files", analysis)
        self.assertIn("parallelization_groups", analysis)
        
        # Should find our test files
        self.assertGreater(analysis["total_tests"], 0)
        self.assertGreater(len(analysis["test_files"]), 0)
        
        # Should create parallelization groups
        self.assertGreater(len(analysis["parallelization_groups"]), 0)
    
    def test_parallelization_group_creation_integration(self):
        """Test parallelization group creation with real test files."""
        analysis = self.engine.analyze_test_suite(self.temp_dir)
        groups = analysis["parallelization_groups"]
        
        # Verify group structure
        for group in groups:
            self.assertIn("group_id", group)
            self.assertIn("files", group)
            self.assertIn("worker_assignment", group)
            self.assertIn("total_estimated_time", group)
            
            # Each group should have files
            self.assertGreater(len(group["files"]), 0)
            
            # Worker assignment should be valid
            self.assertGreaterEqual(group["worker_assignment"], 0)
            self.assertLess(group["worker_assignment"], self.engine.max_workers)

class TestAdvancedParallelTestingPerformance(unittest.TestCase):
    """Performance tests for the advanced parallel testing system."""
    
    def setUp(self):
        """Set up performance test fixtures."""
        self.engine = AdvancedParallelTestingEngine(max_workers=2)
    
    def test_engine_initialization_performance(self):
        """Test engine initialization performance."""
        start_time = time.time()
        
        for _ in range(100):
            engine = AdvancedParallelTestingEngine(max_workers=2)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should be able to create 100 engines in under 1 second
        self.assertLess(total_time, 1.0)
    
    def test_complexity_score_calculation_performance(self):
        """Test complexity score calculation performance."""
        test_content = """
        import unittest
        import time
        import requests
        from unittest.mock import Mock, patch
        
        class TestPerformance(unittest.TestCase):
            def setUp(self):
                self.mock_service = Mock()
                self.db_connection = Mock()
                
            def test_database_operation(self):
                result = self.db_connection.query("SELECT * FROM users")
                self.assertIsNotNone(result)
                
            def test_network_request(self):
                response = requests.get("http://api.example.com")
                self.assertEqual(response.status_code, 200)
                
            def test_complex_logic(self):
                data = [i for i in range(1000)]
                processed = [x * 2 for x in data if x % 2 == 0]
                self.assertEqual(len(processed), 500)
        """
        
        start_time = time.time()
        
        for _ in range(1000):
            score = self.engine._calculate_complexity_score(test_content)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Should be able to calculate 1000 complexity scores in under 0.1 seconds
        self.assertLess(total_time, 0.1)
        
        # Verify score is reasonable
        self.assertGreater(score, 1.0)
        self.assertLessEqual(score, 3.0)

if __name__ == '__main__':
    # Run the test suite
    unittest.main(verbosity=2)
