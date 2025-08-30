#!/usr/bin/env python3
"""
Test Suite for Performance Profiler
Contract: PERF-005 - Advanced Performance Profiling Tools
Agent: Agent-6 (Performance Optimization Manager)
Description: Comprehensive testing for performance profiling tools
"""

import unittest
import time
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the modules to test
from performance_profiler import PerformanceProfiler, ProfilingMetrics, quick_profile
from analysis_dashboard import PerformanceAnalysisDashboard
from validation_system import ProfilingValidationSystem, ValidationResult, ValidationReport


class TestPerformanceProfiler(unittest.TestCase):
    """Test cases for PerformanceProfiler class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.profiler = PerformanceProfiler(output_dir=self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_initialization(self):
        """Test profiler initialization"""
        self.assertIsNotNone(self.profiler)
        self.assertEqual(self.profiler.output_dir, Path(self.temp_dir))
        self.assertFalse(self.profiler.monitoring_active)
        self.assertEqual(len(self.profiler.profiling_data), 0)
    
    def test_function_profiling(self):
        """Test basic function profiling"""
        def test_function():
            time.sleep(0.01)
            return "test"
        
        metrics = self.profiler.profile_function(test_function)
        
        self.assertIsInstance(metrics, ProfilingMetrics)
        self.assertEqual(metrics.function_name, "test_function")
        self.assertEqual(metrics.call_count, 1)
        self.assertGreater(metrics.total_time, 0.01)
        self.assertLess(metrics.total_time, 0.1)  # Should be close to sleep time
    
    def test_start_stop_profiling(self):
        """Test start/stop profiling functionality"""
        profiler_id = self.profiler.start_function_profiling("test_function")
        self.assertIn(profiler_id, self.profiler.active_profilers)
        
        # Simulate some work
        time.sleep(0.01)
        
        metrics = self.profiler.stop_function_profiling(profiler_id)
        self.assertIsNotNone(metrics)
        self.assertNotIn(profiler_id, self.profiler.active_profilers)
    
    def test_system_monitoring(self):
        """Test system monitoring functionality"""
        self.profiler.start_system_monitoring(interval=0.1)
        time.sleep(0.3)  # Allow a few monitoring cycles
        
        self.assertTrue(self.profiler.monitoring_active)
        self.assertGreater(len(self.profiler.system_metrics), 0)
        
        self.profiler.stop_system_monitoring()
        self.assertFalse(self.profiler.monitoring_active)
    
    def test_profiling_report_generation(self):
        """Test profiling report generation"""
        # Generate some profiling data
        def test_function():
            time.sleep(0.01)
        
        self.profiler.profile_function(test_function)
        
        # Generate report
        report_file = self.profiler.generate_profiling_report()
        self.assertTrue(os.path.exists(report_file))
        
        # Verify report content
        with open(report_file, 'r') as f:
            report_data = json.load(f)
        
        self.assertIn('function_metrics', report_data)
        self.assertIn('system_metrics', report_data)
        self.assertIn('performance_analysis', report_data)
    
    def test_quick_profile_function(self):
        """Test quick_profile convenience function"""
        def test_function():
            time.sleep(0.01)
            return "quick_test"
        
        metrics = quick_profile(test_function)
        self.assertIsInstance(metrics, ProfilingMetrics)
        self.assertEqual(metrics.function_name, "test_function")
    
    def test_performance_thresholds(self):
        """Test performance threshold functionality"""
        # Test with slow function
        def slow_function():
            time.sleep(1.5)  # Exceeds 1.0s warning threshold
        
        metrics = self.profiler.profile_function(slow_function)
        self.assertGreater(metrics.total_time, self.profiler.performance_thresholds['function_time_warning'])
    
    def test_data_clearing(self):
        """Test data clearing functionality"""
        # Add some data
        def test_function():
            time.sleep(0.01)
        
        self.profiler.profile_function(test_function)
        self.profiler.start_system_monitoring(interval=0.1)
        time.sleep(0.2)
        self.profiler.stop_system_monitoring()
        
        # Verify data exists
        self.assertGreater(len(self.profiler.profiling_data), 0)
        self.assertGreater(len(self.profiler.system_metrics), 0)
        
        # Clear data
        self.profiler.clear_data()
        self.assertEqual(len(self.profiler.profiling_data), 0)
        self.assertEqual(len(self.profiler.system_metrics), 0)
    
    def test_get_summary(self):
        """Test summary generation"""
        summary = self.profiler.get_summary()
        self.assertIsInstance(summary, dict)
        self.assertIn('active_profilers', summary)
        self.assertIn('functions_profiled', summary)
        self.assertIn('system_metrics_collected', summary)


class TestAnalysisDashboard(unittest.TestCase):
    """Test cases for PerformanceAnalysisDashboard class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.dashboard = PerformanceAnalysisDashboard()
        
        # Sample performance data
        self.sample_data = {
            'function_metrics': [
                {
                    'function_name': 'test_function',
                    'total_time': 0.5,
                    'timestamp': '2025-01-27T10:30:00'
                }
            ],
            'system_metrics': [
                {
                    'cpu_percent': 45.0,
                    'memory_percent': 60.0,
                    'timestamp': '2025-01-27T10:30:00'
                }
            ]
        }
    
    def test_initialization(self):
        """Test dashboard initialization"""
        self.assertIsNotNone(self.dashboard)
        self.assertEqual(self.dashboard.performance_thresholds['critical_cpu'], 95.0)
        self.assertEqual(self.dashboard.performance_thresholds['warning_memory'], 75.0)
    
    def test_data_loading(self):
        """Test data loading functionality"""
        # Create temporary file with sample data
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(self.sample_data, f)
            temp_file = f.name
        
        try:
            success = self.dashboard.load_profiler_data(temp_file)
            self.assertTrue(success)
            self.assertEqual(len(self.dashboard.performance_data['function_metrics']), 1)
        finally:
            os.unlink(temp_file)
    
    def test_performance_trend_analysis(self):
        """Test performance trend analysis"""
        self.dashboard.performance_data = self.sample_data
        trends = self.dashboard.analyze_performance_trends()
        
        self.assertIn('cpu_trends', trends)
        self.assertIn('memory_trends', trends)
        self.assertIn('function_performance_trends', trends)
        self.assertIn('system_health_score', trends)
    
    def test_bottleneck_identification(self):
        """Test bottleneck identification"""
        self.dashboard.performance_data = self.sample_data
        bottlenecks = self.dashboard.identify_performance_bottlenecks()
        
        self.assertIn('cpu_bottlenecks', bottlenecks)
        self.assertIn('memory_bottlenecks', bottlenecks)
        self.assertIn('function_bottlenecks', bottlenecks)
    
    def test_performance_summary_generation(self):
        """Test performance summary generation"""
        self.dashboard.performance_data = self.sample_data
        summary = self.dashboard.generate_performance_summary()
        
        self.assertIn('analysis_timestamp', summary)
        self.assertIn('performance_overview', summary)
        self.assertIn('bottleneck_analysis', summary)
        self.assertIn('recommendations', summary)
    
    def test_export_functionality(self):
        """Test report export functionality"""
        self.dashboard.performance_data = self.sample_data
        summary = self.dashboard.generate_performance_summary()
        
        # Test export
        export_file = self.dashboard.export_analysis_report()
        self.assertTrue(os.path.exists(export_file))
        
        # Clean up
        os.unlink(export_file)
    
    def test_dashboard_status(self):
        """Test dashboard status functionality"""
        status = self.dashboard.get_dashboard_status()
        self.assertIn('data_loaded', status)
        self.assertIn('analysis_completed', status)
        self.assertIn('data_points', status)


class TestValidationSystem(unittest.TestCase):
    """Test cases for ProfilingValidationSystem class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.validation_system = ProfilingValidationSystem()
    
    def test_initialization(self):
        """Test validation system initialization"""
        self.assertIsNotNone(self.validation_system)
        self.assertEqual(self.validation_system.tolerance, 0.05)
        self.assertEqual(len(self.validation_system.validation_results), 0)
    
    def test_timing_accuracy_validation(self):
        """Test timing accuracy validation"""
        result = self.validation_system.validate_timing_accuracy(iterations=10)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertIn('Timing Accuracy Validation', result.test_name)
        self.assertIsInstance(result.passed, bool)
        self.assertIsInstance(result.execution_time, float)
    
    def test_memory_measurement_validation(self):
        """Test memory measurement validation"""
        with patch('builtins.__import__', side_effect=ImportError):
            # Test without psutil
            result = self.validation_system.validate_memory_measurement(iterations=5)
            self.assertFalse(result.passed)
            self.assertIn('psutil not available', result.error_message)
    
    def test_cpu_measurement_validation(self):
        """Test CPU measurement validation"""
        with patch('builtins.__import__', side_effect=ImportError):
            # Test without psutil
            result = self.validation_system.validate_cpu_measurement(iterations=5)
            self.assertFalse(result.passed)
            self.assertIn('psutil not available', result.error_message)
    
    def test_statistical_significance_validation(self):
        """Test statistical significance validation"""
        result = self.validation_system.validate_statistical_significance(sample_size=50)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertIn('Statistical Significance Validation', result.test_name)
    
    def test_profiler_overhead_validation(self):
        """Test profiler overhead validation"""
        result = self.validation_system.validate_profiler_overhead(iterations=20)
        
        self.assertIsInstance(result, ValidationResult)
        self.assertIn('Profiler Overhead Validation', result.test_name)
    
    def test_comprehensive_validation(self):
        """Test comprehensive validation execution"""
        report = self.validation_system.run_comprehensive_validation()
        
        self.assertIsInstance(report, ValidationReport)
        self.assertGreater(report.total_tests, 0)
        self.assertIsInstance(report.success_rate, float)
        self.assertIn('overall_verdict', report.__dict__)
    
    def test_validation_report_export(self):
        """Test validation report export"""
        report = self.validation_system.run_comprehensive_validation()
        export_file = self.validation_system.export_validation_report(report)
        
        self.assertTrue(os.path.exists(export_file))
        
        # Clean up
        os.unlink(export_file)
    
    def test_system_calibration(self):
        """Test system calibration"""
        calibration_data = self.validation_system.calibrate_system()
        
        self.assertIsInstance(calibration_data, dict)
        self.assertIn('calibration_timestamp', calibration_data)
        self.assertIn('baseline_tests', calibration_data)
    
    def test_validation_summary(self):
        """Test validation summary generation"""
        # Run some validations first
        self.validation_system.validate_timing_accuracy(iterations=5)
        
        summary = self.validation_system.get_validation_summary()
        self.assertIn('total_tests', summary)
        self.assertIn('passed_tests', summary)
        self.assertIn('success_rate', summary)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.profiler = PerformanceProfiler(output_dir=self.temp_dir)
        self.dashboard = PerformanceAnalysisDashboard()
        self.validation_system = ProfilingValidationSystem()
    
    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        # 1. Profile some functions
        def test_function():
            time.sleep(0.01)
            return "test"
        
        metrics = self.profiler.profile_function(test_function)
        self.assertIsNotNone(metrics)
        
        # 2. Generate profiling report
        report_file = self.profiler.generate_profiling_report()
        self.assertTrue(os.path.exists(report_file))
        
        # 3. Load data into dashboard
        success = self.dashboard.load_profiler_data(report_file)
        self.assertTrue(success)
        
        # 4. Analyze performance
        summary = self.dashboard.generate_performance_summary()
        self.assertIsNotNone(summary)
        
        # 5. Validate system
        validation_report = self.validation_system.run_comprehensive_validation()
        self.assertIsNotNone(validation_report)
        
        # 6. Export analysis
        analysis_export = self.dashboard.export_analysis_report()
        self.assertTrue(os.path.exists(analysis_export))
        
        # Clean up
        os.unlink(analysis_export)
    
    def test_performance_under_load(self):
        """Test system performance under load"""
        # Profile multiple functions rapidly
        def fast_function():
            return sum(range(1000))
        
        start_time = time.time()
        for _ in range(100):
            metrics = self.profiler.profile_function(fast_function)
        
        total_time = time.time() - start_time
        
        # Should complete within reasonable time (less than 10 seconds)
        self.assertLess(total_time, 10.0)
        
        # Verify all profiling data was collected
        self.assertEqual(len(self.profiler.profiling_data), 100)


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)
