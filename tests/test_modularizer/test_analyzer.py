"""
🧪 REGRESSION TESTING SYSTEM - Test Analyzer
Extracted from regression_testing_system.py for modularization

This module handles test analysis, compliance assessment, and reporting.
"""

from typing import Dict, Any, List
from .models import TestStatus


class RegressionTestAnalyzer:
    """Analyzes test results and provides compliance assessment."""
    
    def __init__(self):
        self.compliance_thresholds = {
            "functionality": 95.0,
            "performance": 90.0,
            "integration": 85.0,
            "regression": 100.0
        }
    
    def assess_regression_compliance(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess regression compliance for a test suite.
        
        Args:
            test_results: Test suite execution results
            
        Returns:
            Dictionary containing compliance assessment
        """
        if not test_results or "test_results" not in test_results:
            return {
                "suite_name": test_results.get("suite_name", "unknown"),
                "compliance_status": "UNKNOWN",
                "overall_score": 0.0,
                "requirements_met": 0,
                "requirements_failed": 0,
                "recommendations": ["No test results available for analysis"]
            }
        
        suite_name = test_results.get("suite_name", "unknown")
        category = test_results.get("category", "general")
        total_tests = test_results.get("total_tests", 0)
        tests_passed = test_results.get("tests_passed", 0)
        tests_failed = test_results.get("tests_failed", 0)
        tests_errored = test_results.get("tests_errored", 0)
        tests_timed_out = test_results.get("tests_timed_out", 0)
        
        if total_tests == 0:
            overall_score = 0.0
        else:
            overall_score = (tests_passed / total_tests) * 100.0
        
        # Determine compliance status
        threshold = self.compliance_thresholds.get(category, 80.0)
        
        if overall_score >= threshold:
            compliance_status = "COMPLIANT"
        elif overall_score >= threshold * 0.8:
            compliance_status = "PARTIALLY_COMPLIANT"
        else:
            compliance_status = "NON_COMPLIANT"
        
        # Generate recommendations
        recommendations = []
        
        if tests_failed > 0:
            recommendations.append(f"Fix {tests_failed} failed tests")
        
        if tests_errored > 0:
            recommendations.append(f"Resolve {tests_errored} test errors")
        
        if tests_timed_out > 0:
            recommendations.append(f"Optimize {tests_timed_out} slow tests")
        
        if overall_score < threshold:
            recommendations.append(f"Improve test success rate to meet {threshold}% threshold")
        
        if not recommendations:
            recommendations.append("All tests passing - maintain current quality")
        
        return {
            "suite_name": suite_name,
            "compliance_status": compliance_status,
            "overall_score": overall_score,
            "requirements_met": tests_passed,
            "requirements_failed": total_tests - tests_passed,
            "recommendations": recommendations,
            "category": category,
            "threshold": threshold
        }
    
    def generate_test_summary(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a summary of test execution results.
        
        Args:
            test_results: Test suite execution results
            
        Returns:
            Dictionary containing test summary
        """
        if not test_results:
            return {"error": "No test results provided"}
        
        return {
            "suite_name": test_results.get("suite_name", "unknown"),
            "total_tests": test_results.get("total_tests", 0),
            "tests_passed": test_results.get("tests_passed", 0),
            "tests_failed": test_results.get("tests_failed", 0),
            "tests_errored": test_results.get("tests_errored", 0),
            "tests_timed_out": test_results.get("tests_timed_out", 0),
            "execution_time": test_results.get("execution_time", 0.0),
            "overall_status": test_results.get("overall_status", TestStatus.PENDING),
            "timestamp": test_results.get("timestamp", "unknown")
        }
    
    def analyze_test_trends(self, execution_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze trends in test execution over time.
        
        Args:
            execution_history: List of test execution results
            
        Returns:
            Dictionary containing trend analysis
        """
        if not execution_history:
            return {"error": "No execution history available"}
        
        total_runs = len(execution_history)
        successful_runs = sum(1 for run in execution_history 
                            if run.get("overall_status") == TestStatus.PASSED)
        
        success_rate = (successful_runs / total_runs) * 100.0 if total_runs > 0 else 0.0
        
        # Calculate average execution time
        execution_times = [run.get("execution_time", 0.0) for run in execution_history]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0.0
        
        return {
            "total_runs": total_runs,
            "successful_runs": successful_runs,
            "success_rate": success_rate,
            "average_execution_time": avg_execution_time,
            "trend": "improving" if success_rate > 80.0 else "stable" if success_rate > 60.0 else "declining"
        }
