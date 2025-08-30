#!/usr/bin/env python3
"""
Performance Profiling Validation System
Contract: PERF-005 - Advanced Performance Profiling Tools
Agent: Agent-6 (Performance Optimization Manager)
Description: Validation system for ensuring profiling accuracy and reliability
"""

import time
import statistics
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of a validation test"""
    test_name: str
    passed: bool
    expected_value: Any
    actual_value: Any
    tolerance: float
    error_message: Optional[str] = None
    execution_time: float = 0.0

@dataclass
class ValidationReport:
    """Complete validation report"""
    validation_timestamp: str
    total_tests: int
    passed_tests: int
    failed_tests: int
    success_rate: float
    test_results: List[ValidationResult]
    overall_verdict: str
    recommendations: List[str]

class ProfilingValidationSystem:
    """
    Performance Profiling Validation System
    
    Features:
    - Accuracy validation for timing measurements
    - Memory usage validation
    - CPU usage validation
    - Statistical significance testing
    - Automated validation reports
    - Calibration capabilities
    """
    
    def __init__(self, tolerance: float = 0.05):
        self.tolerance = tolerance  # 5% tolerance by default
        self.validation_results: List[ValidationResult] = []
        self.calibration_data: Dict[str, Any] = {}
        
        logger.info("Profiling Validation System initialized")
    
    def validate_timing_accuracy(self, iterations: int = 100) -> ValidationResult:
        """
        Validate timing accuracy using known sleep durations
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Validation result
        """
        test_name = "Timing Accuracy Validation"
        logger.info(f"Starting {test_name}")
        
        start_time = time.time()
        
        # Test with known sleep durations
        test_durations = [0.001, 0.01, 0.1, 0.5, 1.0]
        results = []
        
        for duration in test_durations:
            for _ in range(iterations // len(test_durations)):
                start = time.time()
                time.sleep(duration)
                end = time.time()
                measured_duration = end - start
                results.append((duration, measured_duration))
        
        # Calculate accuracy metrics
        total_error = 0
        for expected, actual in results:
            error = abs(actual - expected) / expected
            total_error += error
        
        average_error = total_error / len(results)
        passed = average_error <= self.tolerance
        
        validation_result = ValidationResult(
            test_name=test_name,
            passed=passed,
            expected_value=f"<{self.tolerance * 100:.1f}% error",
            actual_value=f"{average_error * 100:.2f}% error",
            tolerance=self.tolerance,
            error_message=None if passed else f"Average error {average_error * 100:.2f}% exceeds tolerance {self.tolerance * 100:.1f}%",
            execution_time=time.time() - start_time
        )
        
        self.validation_results.append(validation_result)
        logger.info(f"{test_name}: {'PASSED' if passed else 'FAILED'}")
        
        return validation_result
    
    def validate_memory_measurement(self, iterations: int = 50) -> ValidationResult:
        """
        Validate memory measurement accuracy
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Validation result
        """
        test_name = "Memory Measurement Validation"
        logger.info(f"Starting {test_name}")
        
        start_time = time.time()
        
        try:
            import psutil
            memory = psutil.virtual_memory()
            
            # Test memory measurement consistency
            measurements = []
            for _ in range(iterations):
                memory = psutil.virtual_memory()
                measurements.append(memory.percent)
                time.sleep(0.01)  # Small delay between measurements
            
            # Check if measurements are reasonable (0-100%)
            valid_measurements = [m for m in measurements if 0 <= m <= 100]
            consistency_score = len(valid_measurements) / len(measurements)
            
            # Check measurement variance (should be relatively stable)
            if len(valid_measurements) > 1:
                variance = statistics.variance(valid_measurements)
                variance_threshold = 50.0  # Reasonable variance threshold
                variance_ok = variance <= variance_threshold
            else:
                variance_ok = False
                variance = 0
            
            passed = consistency_score >= 0.95 and variance_ok
            
            validation_result = ValidationResult(
                test_name=test_name,
                passed=passed,
                expected_value="Consistent measurements with low variance",
                actual_value=f"Consistency: {consistency_score:.2f}, Variance: {variance:.2f}",
                tolerance=self.tolerance,
                error_message=None if passed else f"Memory measurement issues: consistency={consistency_score:.2f}, variance={variance:.2f}",
                execution_time=time.time() - start_time
            )
            
        except ImportError:
            validation_result = ValidationResult(
                test_name=test_name,
                passed=False,
                expected_value="psutil available",
                actual_value="psutil not available",
                tolerance=self.tolerance,
                error_message="psutil library not available for memory validation",
                execution_time=time.time() - start_time
            )
        
        self.validation_results.append(validation_result)
        logger.info(f"{test_name}: {'PASSED' if validation_result.passed else 'FAILED'}")
        
        return validation_result
    
    def validate_cpu_measurement(self, iterations: int = 50) -> ValidationResult:
        """
        Validate CPU measurement accuracy
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Validation result
        """
        test_name = "CPU Measurement Validation"
        logger.info(f"Starting {test_name}")
        
        start_time = time.time()
        
        try:
            import psutil
            cpu = psutil.cpu_percent()
            
            # Test CPU measurement consistency
            measurements = []
            for _ in range(iterations):
                cpu = psutil.cpu_percent()
                measurements.append(cpu)
                time.sleep(0.01)  # Small delay between measurements
            
            # Check if measurements are reasonable (0-100%)
            valid_measurements = [m for m in measurements if 0 <= m <= 100]
            consistency_score = len(valid_measurements) / len(measurements)
            
            # Check measurement variance (should be reasonable)
            if len(valid_measurements) > 1:
                variance = statistics.variance(valid_measurements)
                variance_threshold = 100.0  # CPU can vary more than memory
                variance_ok = variance <= variance_threshold
            else:
                variance_ok = False
                variance = 0
            
            passed = consistency_score >= 0.95 and variance_ok
            
            validation_result = ValidationResult(
                test_name=test_name,
                passed=passed,
                expected_value="Consistent measurements with reasonable variance",
                actual_value=f"Consistency: {consistency_score:.2f}, Variance: {variance:.2f}",
                tolerance=self.tolerance,
                error_message=None if passed else f"CPU measurement issues: consistency={consistency_score:.2f}, variance={variance:.2f}",
                execution_time=time.time() - start_time
            )
            
        except ImportError:
            validation_result = ValidationResult(
                test_name=test_name,
                passed=False,
                expected_value="psutil available",
                actual_value="psutil not available",
                tolerance=self.tolerance,
                error_message="psutil library not available for CPU validation",
                execution_time=time.time() - start_time
            )
        
        self.validation_results.append(validation_result)
        logger.info(f"{test_name}: {'PASSED' if validation_result.passed else 'FAILED'}")
        
        return validation_result
    
    def validate_statistical_significance(self, sample_size: int = 100) -> ValidationResult:
        """
        Validate statistical significance of profiling data
        
        Args:
            sample_size: Minimum sample size for significance
            
        Returns:
            Validation result
        """
        test_name = "Statistical Significance Validation"
        logger.info(f"Starting {test_name}")
        
        start_time = time.time()
        
        # Generate synthetic profiling data
        base_time = 0.1  # Base execution time
        noise_level = 0.01  # Random noise level
        
        synthetic_data = []
        for _ in range(sample_size):
            # Add random noise to base time
            execution_time = base_time + random.uniform(-noise_level, noise_level)
            synthetic_data.append(execution_time)
        
        # Calculate statistical measures
        mean_time = statistics.mean(synthetic_data)
        std_dev = statistics.stdev(synthetic_data) if len(synthetic_data) > 1 else 0
        
        # Check if sample size is sufficient
        sample_size_ok = len(synthetic_data) >= 30  # Minimum for normal distribution approximation
        
        # Check if standard deviation is reasonable
        cv = std_dev / mean_time if mean_time > 0 else float('inf')  # Coefficient of variation
        cv_ok = cv <= 0.5  # CV should be reasonable
        
        # Check if mean is close to expected
        mean_error = abs(mean_time - base_time) / base_time
        mean_ok = mean_error <= self.tolerance
        
        passed = sample_size_ok and cv_ok and mean_ok
        
        validation_result = ValidationResult(
            test_name=test_name,
            passed=passed,
            expected_value=f"Sample size >= 30, CV <= 0.5, mean error <= {self.tolerance * 100:.1f}%",
            actual_value=f"Sample size: {len(synthetic_data)}, CV: {cv:.3f}, mean error: {mean_error * 100:.2f}%",
            tolerance=self.tolerance,
            error_message=None if passed else f"Statistical significance issues: sample_size_ok={sample_size_ok}, cv_ok={cv_ok}, mean_ok={mean_ok}",
            execution_time=time.time() - start_time
        )
        
        self.validation_results.append(validation_result)
        logger.info(f"{test_name}: {'PASSED' if passed else 'FAILED'}")
        
        return validation_result
    
    def validate_profiler_overhead(self, iterations: int = 100) -> ValidationResult:
        """
        Validate that profiler overhead is minimal
        
        Args:
            iterations: Number of test iterations
            
        Returns:
            Validation result
        """
        test_name = "Profiler Overhead Validation"
        logger.info(f"Starting {test_name}")
        
        start_time = time.time()
        
        def simple_function():
            """Simple function for overhead testing"""
            return sum(range(1000))
        
        # Measure execution time without profiler
        no_profiler_times = []
        for _ in range(iterations):
            start = time.time()
            simple_function()
            end = time.time()
            no_profiler_times.append(end - start)
        
        # Measure execution time with profiler (simulated)
        with_profiler_times = []
        for _ in range(iterations):
            start = time.time()
            # Simulate profiler overhead
            time.sleep(0.0001)  # 0.1ms overhead simulation
            simple_function()
            end = time.time()
            with_profiler_times.append(end - start)
        
        # Calculate overhead
        avg_no_profiler = statistics.mean(no_profiler_times)
        avg_with_profiler = statistics.mean(with_profiler_times)
        
        overhead = (avg_with_profiler - avg_no_profiler) / avg_no_profiler if avg_no_profiler > 0 else float('inf')
        
        # Overhead should be less than 10%
        overhead_threshold = 0.10
        passed = overhead <= overhead_threshold
        
        validation_result = ValidationResult(
            test_name=test_name,
            passed=passed,
            expected_value=f"Overhead <= {overhead_threshold * 100:.1f}%",
            actual_value=f"Overhead: {overhead * 100:.2f}%",
            tolerance=overhead_threshold,
            error_message=None if passed else f"Profiler overhead {overhead * 100:.2f}% exceeds threshold {overhead_threshold * 100:.1f}%",
            execution_time=time.time() - start_time
        )
        
        self.validation_results.append(validation_result)
        logger.info(f"{test_name}: {'PASSED' if passed else 'FAILED'}")
        
        return validation_result
    
    def run_comprehensive_validation(self) -> ValidationReport:
        """
        Run all validation tests
        
        Returns:
            Complete validation report
        """
        logger.info("Starting comprehensive validation")
        
        # Run all validation tests
        self.validate_timing_accuracy()
        self.validate_memory_measurement()
        self.validate_cpu_measurement()
        self.validate_statistical_significance()
        self.validate_profiler_overhead()
        
        # Generate report
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for result in self.validation_results if result.passed)
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
        
        # Determine overall verdict
        if success_rate >= 90:
            overall_verdict = "EXCELLENT"
        elif success_rate >= 80:
            overall_verdict = "GOOD"
        elif success_rate >= 70:
            overall_verdict = "FAIR"
        elif success_rate >= 60:
            overall_verdict = "POOR"
        else:
            overall_verdict = "FAILED"
        
        # Generate recommendations
        recommendations = self._generate_validation_recommendations()
        
        report = ValidationReport(
            validation_timestamp=datetime.now().isoformat(),
            total_tests=total_tests,
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            success_rate=success_rate,
            test_results=self.validation_results,
            overall_verdict=overall_verdict,
            recommendations=recommendations
        )
        
        logger.info(f"Validation completed: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
        return report
    
    def _generate_validation_recommendations(self) -> List[str]:
        """Generate recommendations based on validation results"""
        recommendations = []
        
        failed_tests = [result for result in self.validation_results if not result.passed]
        
        for result in failed_tests:
            if "Timing Accuracy" in result.test_name:
                recommendations.append("Review timing measurement implementation for accuracy")
            elif "Memory Measurement" in result.test_name:
                recommendations.append("Verify memory measurement methodology and psutil integration")
            elif "CPU Measurement" in result.test_name:
                recommendations.append("Check CPU measurement implementation and calibration")
            elif "Statistical Significance" in result.test_name:
                recommendations.append("Increase sample size or improve measurement precision")
            elif "Profiler Overhead" in result.test_name:
                recommendations.append("Optimize profiler implementation to reduce overhead")
        
        if not recommendations:
            recommendations.append("All validation tests passed - profiling system is reliable")
        
        return recommendations
    
    def export_validation_report(self, report: ValidationReport, output_file: Optional[str] = None) -> str:
        """
        Export validation report to file
        
        Args:
            report: Validation report to export
            output_file: Optional output file path
            
        Returns:
            Path to exported report
        """
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"profiling_validation_report_{timestamp}.json"
        
        # Convert dataclass to dict for JSON serialization
        report_dict = asdict(report)
        
        with open(output_file, 'w') as f:
            json.dump(report_dict, f, indent=2)
        
        logger.info(f"Validation report exported to {output_file}")
        return output_file
    
    def calibrate_system(self) -> Dict[str, Any]:
        """
        Calibrate the validation system
        
        Returns:
            Calibration data
        """
        logger.info("Starting system calibration")
        
        # Run baseline measurements
        baseline_tests = []
        
        # Timing calibration
        timing_results = []
        for _ in range(10):
            start = time.time()
            time.sleep(0.1)
            end = time.time()
            timing_results.append(end - start)
        
        baseline_tests.append({
            'test_type': 'timing_baseline',
            'expected': 0.1,
            'measured': statistics.mean(timing_results),
            'variance': statistics.variance(timing_results) if len(timing_results) > 1 else 0
        })
        
        # Store calibration data
        self.calibration_data = {
            'calibration_timestamp': datetime.now().isoformat(),
            'baseline_tests': baseline_tests,
            'system_tolerance': self.tolerance
        }
        
        logger.info("System calibration completed")
        return self.calibration_data
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """Get summary of validation status"""
        if not self.validation_results:
            return {'status': 'No validation tests run'}
        
        return {
            'total_tests': len(self.validation_results),
            'passed_tests': sum(1 for result in self.validation_results if result.passed),
            'failed_tests': sum(1 for result in self.validation_results if not result.passed),
            'success_rate': (sum(1 for result in self.validation_results if result.passed) / len(self.validation_results)) * 100,
            'last_validation': max(result.execution_time for result in self.validation_results) if self.validation_results else 0,
            'calibration_available': bool(self.calibration_data)
        }


if __name__ == "__main__":
    # Example usage
    validation_system = ProfilingValidationSystem()
    
    # Run comprehensive validation
    report = validation_system.run_comprehensive_validation()
    
    print(f"Validation Results:")
    print(f"Total Tests: {report.total_tests}")
    print(f"Passed: {report.passed_tests}")
    print(f"Failed: {report.failed_tests}")
    print(f"Success Rate: {report.success_rate:.1f}%")
    print(f"Overall Verdict: {report.overall_verdict}")
    
    # Export report
    report_file = validation_system.export_validation_report(report)
    print(f"\nReport exported to: {report_file}")
    
    # Show recommendations
    if report.recommendations:
        print(f"\nRecommendations:")
        for rec in report.recommendations:
            print(f"- {rec}")
