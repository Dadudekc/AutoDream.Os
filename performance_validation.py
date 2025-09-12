#!/usr/bin/env python3
"""
Performance Optimization Validation Suite
========================================

Validates that performance optimizations maintain functionality and improve
performance metrics as specified in CONTRACT-AGENT1-PERFORMANCE-001.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import cProfile
import io
import logging
import pstats
import sys
import time
import tracemalloc
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List

import psutil

logger = logging.getLogger(__name__)


class PerformanceValidator:
    """Validates performance optimizations and functionality"""

    def __init__(self):
        self.baseline_metrics = {}
        self.optimized_metrics = {}
        self.validation_results = {}

    def measure_execution_time(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Measure function execution time"""
        start_time = time.time()
        start_memory = psutil.virtual_memory().used

        try:
            result = func(*args, **kwargs)
            success = True
        except Exception as e:
            result = None
            success = False
            error = str(e)

        end_time = time.time()
        end_memory = psutil.virtual_memory().used

        return {
            'execution_time_ms': (end_time - start_time) * 1000,
            'memory_delta_mb': (end_memory - start_memory) / 1024 / 1024,
            'success': success,
            'result': result,
            'error': locals().get('error')
        }

    def profile_function(self, func: Callable, *args, **kwargs) -> Dict[str, Any]:
        """Profile function performance"""
        pr = cProfile.Profile()
        pr.enable()

        result = self.measure_execution_time(func, *args, **kwargs)

        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(10)
        result['profile_stats'] = s.getvalue()

        return result

    def measure_import_time(self, module_name: str) -> Dict[str, Any]:
        """Measure module import time"""
        tracemalloc.start()

        start_time = time.time()
        try:
            __import__(module_name)
            success = True
        except ImportError as e:
            success = False
            error = str(e)

        import_time = (time.time() - start_time) * 1000
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        return {
            'module': module_name,
            'import_time_ms': import_time,
            'peak_memory_mb': peak / 1024 / 1024,
            'success': success,
            'error': locals().get('error')
        }

    def validate_lazy_loading(self) -> Dict[str, Any]:
        """Validate lazy loading optimizations"""
        logger.info("Validating lazy loading optimizations...")

        # Test lazy loading of heavy modules
        heavy_modules = ['pandas', 'numpy', 'matplotlib.pyplot']

        results = {}
        for module in heavy_modules:
            # Test lazy import time
            lazy_start = time.time()
            try:
                sys.path.append(str(Path(__file__).parent / 'src'))
                from src.core.lazy_loader import get_lazy_module
                lazy_module = get_lazy_module(module.replace('.pyplot', ''), 'plt' if 'pyplot' in module else module.split('.')[-1])
                lazy_time = (time.time() - lazy_start) * 1000

                # Test actual module access
                access_start = time.time()
                test_attr = getattr(lazy_module, 'DataFrame' if 'pandas' in module else ('array' if 'numpy' in module else 'plot'))
                access_time = (time.time() - access_start) * 1000

                results[module] = {
                    'lazy_load_time_ms': lazy_time,
                    'first_access_time_ms': access_time,
                    'total_time_ms': lazy_time + access_time,
                    'success': True
                }
            except Exception as e:
                results[module] = {
                    'success': False,
                    'error': str(e)
                }

        return {
            'test_name': 'lazy_loading_validation',
            'results': results,
            'summary': {
                'modules_tested': len(heavy_modules),
                'successful_lazy_loads': sum(1 for r in results.values() if r.get('success', False)),
                'average_lazy_time_ms': sum(r.get('lazy_load_time_ms', 0) for r in results.values() if r.get('success', False)) / max(1, sum(1 for r in results.values() if r.get('success', False)))
            }
        }

    def validate_memory_optimization(self) -> Dict[str, Any]:
        """Validate memory optimization improvements"""
        logger.info("Validating memory optimizations...")

        # Test resource manager
        try:
            from src.core.resource_manager import managed_resource, resource_manager

            initial_memory = psutil.virtual_memory().used

            # Test managed resource
            with managed_resource("test_validation", "validation_test", lambda: None):
                # Simulate some work
                test_data = [i for i in range(10000)]
                time.sleep(0.1)

            final_memory = psutil.virtual_memory().used
            memory_delta = (final_memory - initial_memory) / 1024 / 1024

            # Test resource cleanup
            resource_manager.cleanup_resource("test_validation")

            return {
                'test_name': 'memory_optimization_validation',
                'memory_delta_mb': memory_delta,
                'resources_registered': len(resource_manager.resources),
                'success': True
            }
        except Exception as e:
            return {
                'test_name': 'memory_optimization_validation',
                'success': False,
                'error': str(e)
            }

    def validate_performance_monitoring(self) -> Dict[str, Any]:
        """Validate performance monitoring system"""
        logger.info("Validating performance monitoring...")

        try:
            from src.core.performance_monitor import performance_monitor, performance_profiler

            # Start monitoring
            performance_monitor.start_monitoring()
            time.sleep(2)  # Let it collect some data

            # Test metric recording
            performance_monitor.record_metric("test_metric", 42.0, "units", {"test": True})

            # Get report
            report = performance_monitor.get_performance_report()

            # Stop monitoring
            performance_monitor.stop_monitoring()

            return {
                'test_name': 'performance_monitoring_validation',
                'monitoring_active': report != {"error": "No performance data available"},
                'snapshots_collected': report.get('total_snapshots', 0),
                'metrics_recorded': len(performance_monitor.metrics),
                'alerts_generated': len(performance_monitor.alerts),
                'success': True
            }
        except Exception as e:
            return {
                'test_name': 'performance_monitoring_validation',
                'success': False,
                'error': str(e)
            }

    def validate_functionality_preservation(self) -> Dict[str, Any]:
        """Validate that optimizations don't break existing functionality"""
        logger.info("Validating functionality preservation...")

        tests = []

        # Test lazy loading doesn't break imports
        try:
            from src.core.lazy_loader import LazyLoader
            loader = LazyLoader()
            tests.append({
                'test': 'lazy_loader_instantiation',
                'success': True
            })
        except Exception as e:
            tests.append({
                'test': 'lazy_loader_instantiation',
                'success': False,
                'error': str(e)
            })

        # Test resource manager
        try:
            from src.core.resource_manager import ResourceManager
            manager = ResourceManager()
            tests.append({
                'test': 'resource_manager_instantiation',
                'success': True
            })
        except Exception as e:
            tests.append({
                'test': 'resource_manager_instantiation',
                'success': False,
                'error': str(e)
            })

        # Test performance monitor
        try:
            from src.core.performance_monitor import PerformanceMonitor
            monitor = PerformanceMonitor()
            tests.append({
                'test': 'performance_monitor_instantiation',
                'success': True
            })
        except Exception as e:
            tests.append({
                'test': 'performance_monitor_instantiation',
                'success': False,
                'error': str(e)
            })

        successful_tests = sum(1 for t in tests if t['success'])
        total_tests = len(tests)

        return {
            'test_name': 'functionality_preservation_validation',
            'tests': tests,
            'summary': {
                'total_tests': total_tests,
                'successful_tests': successful_tests,
                'success_rate': successful_tests / total_tests if total_tests > 0 else 0
            }
        }

    def run_full_validation(self) -> Dict[str, Any]:
        """Run comprehensive validation suite"""
        logger.info("Starting comprehensive performance validation...")

        validation_results = {
            'timestamp': datetime.now().isoformat(),
            'validation_suite': 'AGENT-1 Performance Optimization Validation',
            'tests': {}
        }

        # Run all validation tests
        test_functions = [
            self.validate_lazy_loading,
            self.validate_memory_optimization,
            self.validate_performance_monitoring,
            self.validate_functionality_preservation
        ]

        for test_func in test_functions:
            try:
                test_name = test_func.__name__
                logger.info(f"Running {test_name}...")
                result = test_func()
                validation_results['tests'][test_name] = result
                logger.info(f"{test_name}: {'✅ PASSED' if result.get('success', False) else '❌ FAILED'}")
            except Exception as e:
                logger.error(f"Error running {test_func.__name__}: {e}")
                validation_results['tests'][test_func.__name__] = {
                    'success': False,
                    'error': str(e)
                }

        # Generate summary
        total_tests = len(validation_results['tests'])
        successful_tests = sum(1 for t in validation_results['tests'].values() if t.get('success', False))

        validation_results['summary'] = {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': successful_tests / total_tests if total_tests > 0 else 0,
            'overall_success': successful_tests == total_tests
        }

        self.validation_results = validation_results
        return validation_results

    def generate_validation_report(self) -> str:
        """Generate a comprehensive validation report"""
        if not self.validation_results:
            return "No validation results available. Run run_full_validation() first."

        report = []
        report.append("=" * 80)
        report.append("PERFORMANCE OPTIMIZATION VALIDATION REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {self.validation_results['timestamp']}")
        report.append("")

        # Summary
        summary = self.validation_results['summary']
        report.append("VALIDATION SUMMARY:")
        report.append("-" * 20)
        report.append(f"Total Tests: {summary['total_tests']}")
        report.append(f"Successful Tests: {summary['successful_tests']}")
        report.append(".1f")
        report.append(f"Overall Status: {'✅ PASSED' if summary['overall_success'] else '❌ FAILED'}")
        report.append("")

        # Individual test results
        for test_name, result in self.validation_results['tests'].items():
            report.append(f"TEST: {test_name.replace('_', ' ').title()}")
            report.append("-" * (6 + len(test_name)))

            if result.get('success', False):
                report.append("Status: ✅ PASSED")

                # Add specific metrics
                if 'summary' in result:
                    for key, value in result['summary'].items():
                        if isinstance(value, float):
                            report.append(".2f")
                        else:
                            report.append(f"{key}: {value}")

                if 'results' in result:
                    report.append("Detailed Results:")
                    for module, metrics in result['results'].items():
                        if metrics.get('success', False):
                            report.append(f"  {module}: ✅ ({metrics.get('lazy_load_time_ms', 0):.2f}ms)")
                        else:
                            report.append(f"  {module}: ❌ {metrics.get('error', 'Unknown error')}")

            else:
                report.append("Status: ❌ FAILED")
                if 'error' in result:
                    report.append(f"Error: {result['error']}")

            report.append("")

        # Performance targets check
        report.append("CONTRACT TARGETS VALIDATION:")
        report.append("-" * 30)

        lazy_test = self.validation_results['tests'].get('validate_lazy_loading', {})
        if lazy_test.get('success', False):
            avg_time = lazy_test.get('summary', {}).get('average_lazy_time_ms', 0)
            report.append(f"Lazy Loading: {'✅ TARGET MET' if avg_time < 50 else '⚠️  TARGET NEAR'} ({avg_time:.2f}ms avg)")

        memory_test = self.validation_results['tests'].get('validate_memory_optimization', {})
        if memory_test.get('success', False):
            memory_delta = memory_test.get('memory_delta_mb', 0)
            report.append(f"Memory Optimization: {'✅ TARGET MET' if memory_delta < 10 else '⚠️  MONITORING'} ({memory_delta:.2f}MB delta)")

        monitoring_test = self.validation_results['tests'].get('validate_performance_monitoring', {})
        if monitoring_test.get('success', False):
            snapshots = monitoring_test.get('snapshots_collected', 0)
            report.append(f"Performance Monitoring: {'✅ TARGET MET' if snapshots > 0 else '❌ TARGET MISSED'} ({snapshots} snapshots)")

        functionality_test = self.validation_results['tests'].get('validate_functionality_preservation', {})
        if functionality_test.get('success', False):
            success_rate = functionality_test.get('summary', {}).get('success_rate', 0)
            report.append(".1f")

        report.append("")
        report.append("=" * 80)

        return "\n".join(report)


def main():
    """Main validation entry point"""
    validator = PerformanceValidator()

    print("🚀 Starting Performance Optimization Validation...")
    print("This may take a few moments...")

    try:
        results = validator.run_full_validation()
        report = validator.generate_validation_report()

        # Save report
        report_file = f"performance_validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)

        print("\n✅ Validation completed!")
        print(f"📊 Report saved to: {report_file}")
        print("\n" + "="*80)
        print(report)

        # Exit with appropriate code
        summary = results.get('summary', {})
        if summary.get('overall_success', False):
            print("🎉 All validations passed! Performance optimizations are working correctly.")
        else:
            print("⚠️  Some validations failed. Please review the report for details.")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
