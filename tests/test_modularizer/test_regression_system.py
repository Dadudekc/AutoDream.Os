"""
🧪 REGRESSION TESTING SYSTEM - Test Cases
Extracted from regression_testing_system.py for modularization

This module contains all test cases for the regression testing system.
"""

import pytest
from .models import TestStatus, RegressionTestSuite
from .regression_testing_system import RegressionTestingSystem


class TestRegressionTestingSystem:
    """Test cases for the regression testing system."""
    
    def test_regression_system_initialization(self, regression_system):
        """Test regression testing system initialization."""
        assert regression_system is not None
        assert isinstance(regression_system, RegressionTestingSystem)
        assert regression_system.test_suites == {}
        assert regression_system.test_results == {}
        assert regression_system.execution_history == []
        assert regression_system.timeout_default == 30.0
    
    def test_test_suite_registration(self, regression_system, sample_test_functions):
        """Test test suite registration."""
        # Create a test suite
        test_suite = RegressionTestSuite(
            name="test_suite_1",
            description="Test suite for testing",
            tests=sample_test_functions[:3],
            timeout=30.0,
            category="functionality",
            priority="high"
        )
        
        # Register the suite
        success = regression_system.register_test_suite(test_suite)
        assert success == True
        
        # Verify registration
        assert "test_suite_1" in regression_system.test_suites
        assert regression_system.test_suites["test_suite_1"] == test_suite
        
        # Test duplicate registration
        success = regression_system.register_test_suite(test_suite)
        assert success == False
    
    def test_single_test_execution(self, regression_system, sample_test_functions):
        """Test single test execution."""
        test_func = sample_test_functions[0]  # Simple test function
        
        result = regression_system.run_single_test(test_func)
        
        assert isinstance(result, RegressionTestResult)
        assert result.test_name == "test_function_1"
        assert result.status == TestStatus.PASSED
        assert result.execution_time >= 0.0
        assert result.output == "test_result_1"
        assert result.error_message is None
    
    def test_test_suite_execution(self, regression_system, sample_test_functions):
        """Test test suite execution."""
        # Create and register a test suite
        test_suite = RegressionTestSuite(
            name="test_suite_2",
            description="Test suite for execution testing",
            tests=sample_test_functions[:3],  # Use first 3 tests
            timeout=30.0,
            category="functionality",
            priority="medium"
        )
        
        regression_system.register_test_suite(test_suite)
        
        # Run the test suite
        results = regression_system.run_test_suite("test_suite_2")
        
        assert isinstance(results, dict)
        assert results["suite_name"] == "test_suite_2"
        assert results["total_tests"] == 3
        assert results["tests_passed"] >= 2  # At least 2 should pass
        assert results["overall_status"] in [TestStatus.PASSED, TestStatus.FAILED]
        assert "timestamp" in results
        
        # Verify test results are stored
        assert "test_suite_2" in regression_system.test_results
    
    def test_functionality_test_suite_creation(self, regression_system, sample_test_functions):
        """Test functionality test suite creation."""
        test_suite = regression_system.create_functionality_test_suite(
            "functionality_tests",
            sample_test_functions[:3],
            "Test functionality features"
        )
        
        assert isinstance(test_suite, RegressionTestSuite)
        assert test_suite.name == "functionality_tests"
        assert test_suite.description == "Test functionality features"
        assert test_suite.category == "functionality"
        assert test_suite.priority == "high"
        assert test_suite.timeout == 30.0
        assert len(test_suite.tests) == 3
    
    def test_performance_test_suite_creation(self, regression_system, sample_test_functions):
        """Test performance test suite creation."""
        test_suite = regression_system.create_performance_test_suite(
            "performance_tests",
            sample_test_functions[:2],
            "Test performance characteristics"
        )
        
        assert isinstance(test_suite, RegressionTestSuite)
        assert test_suite.name == "performance_tests"
        assert test_suite.description == "Test performance characteristics"
        assert test_suite.category == "performance"
        assert test_suite.priority == "medium"
        assert test_suite.timeout == 60.0
        assert len(test_suite.tests) == 2
    
    def test_integration_test_suite_creation(self, regression_system, sample_test_functions):
        """Test integration test suite creation."""
        test_suite = regression_system.create_integration_test_suite(
            "integration_tests",
            sample_test_functions[:4],
            "Test integration features"
        )
        
        assert isinstance(test_suite, RegressionTestSuite)
        assert test_suite.name == "integration_tests"
        assert test_suite.description == "Test integration features"
        assert test_suite.category == "integration"
        assert test_suite.priority == "high"
        assert test_suite.timeout == 45.0
        assert len(test_suite.tests) == 4
    
    def test_regression_test_suite_creation(self, regression_system, sample_test_functions):
        """Test regression test suite creation."""
        test_suite = regression_system.create_regression_test_suite(
            "regression_tests",
            sample_test_functions[:3],
            "Test regression scenarios"
        )
        
        assert isinstance(test_suite, RegressionTestSuite)
        assert test_suite.name == "regression_tests"
        assert test_suite.description == "Test regression scenarios"
        assert test_suite.category == "regression"
        assert test_suite.priority == "critical"
        assert test_suite.timeout == 90.0
        assert len(test_suite.tests) == 3
    
    def test_custom_test_suite_creation(self, regression_system, sample_test_functions):
        """Test custom test suite creation."""
        test_suite = regression_system.create_custom_test_suite(
            "custom_tests",
            sample_test_functions[:2],
            "Custom test suite",
            "validation",
            "low",
            120.0
        )
        
        assert isinstance(test_suite, RegressionTestSuite)
        assert test_suite.name == "custom_tests"
        assert test_suite.description == "Custom test suite"
        assert test_suite.category == "validation"
        assert test_suite.priority == "low"
        assert test_suite.timeout == 120.0
        assert len(test_suite.tests) == 2
    
    def test_test_results_retrieval(self, regression_system, sample_test_functions):
        """Test test results retrieval."""
        # Create and run a test suite
        test_suite = RegressionTestSuite(
            name="results_test_suite",
            description="Test suite for results testing",
            tests=sample_test_functions[:2],
            timeout=30.0
        )
        
        regression_system.register_test_suite(test_suite)
        regression_system.run_test_suite("results_test_suite")
        
        # Get specific suite results
        suite_results = regression_system.get_test_results("results_test_suite")
        assert isinstance(suite_results, dict)
        assert suite_results["suite_name"] == "results_test_suite"
        
        # Get all results
        all_results = regression_system.get_test_results()
        assert isinstance(all_results, dict)
        assert "results_test_suite" in all_results
    
    def test_execution_history_retrieval(self, regression_system, sample_test_functions):
        """Test execution history retrieval."""
        # Create and run multiple test suites
        for i in range(3):
            test_suite = RegressionTestSuite(
                name=f"history_test_suite_{i}",
                description=f"Test suite {i} for history testing",
                tests=sample_test_functions[:2],
                timeout=30.0
            )
            
            regression_system.register_test_suite(test_suite)
            regression_system.run_test_suite(f"history_test_suite_{i}")
        
        # Get execution history
        history = regression_system.get_execution_history()
        
        assert isinstance(history, list)
        assert len(history) >= 3
        
        # Test limit parameter
        limited_history = regression_system.get_execution_history(limit=2)
        assert len(limited_history) <= 2
    
    def test_test_results_clearing(self, regression_system, sample_test_functions):
        """Test test results clearing."""
        # Create and run a test suite
        test_suite = RegressionTestSuite(
            name="clear_test_suite",
            description="Test suite for clearing testing",
            tests=sample_test_functions[:2],
            timeout=30.0
        )
        
        regression_system.register_test_suite(test_suite)
        regression_system.run_test_suite("clear_test_suite")
        
        # Verify results exist
        assert "clear_test_suite" in regression_system.test_results
        
        # Clear specific suite
        success = regression_system.clear_test_results("clear_test_suite")
        assert success == True
        assert "clear_test_suite" not in regression_system.test_results
        
        # Clear all results
        regression_system.run_test_suite("clear_test_suite")  # Add some results back
        success = regression_system.clear_test_results()
        assert success == True
        assert len(regression_system.test_results) == 0
        assert len(regression_system.execution_history) == 0
    
    def test_regression_compliance_assessment(self, regression_system, sample_test_functions):
        """Test regression compliance assessment."""
        # Create and run a test suite
        test_suite = RegressionTestSuite(
            name="compliance_test_suite",
            description="Test suite for compliance testing",
            tests=sample_test_functions[:2],  # Use simple tests
            timeout=30.0
        )
        
        regression_system.register_test_suite(test_suite)
        regression_system.run_test_suite("compliance_test_suite")
        
        # Assess compliance
        compliance = regression_system.assess_regression_compliance("compliance_test_suite")
        
        assert isinstance(compliance, dict)
        assert compliance["suite_name"] == "compliance_test_suite"
        assert "compliance_status" in compliance
        assert "overall_score" in compliance
        assert "requirements_met" in compliance
        assert "requirements_failed" in compliance
        assert "recommendations" in compliance
        
        assert compliance["compliance_status"] in ["COMPLIANT", "PARTIALLY_COMPLIANT", "NON_COMPLIANT", "UNKNOWN"]
        assert 0.0 <= compliance["overall_score"] <= 100.0
    
    def test_comparison_mode_execution(self, regression_system, sample_test_functions):
        """Test comparison mode execution."""
        # Create a test suite
        test_suite = RegressionTestSuite(
            name="comparison_test_suite",
            description="Test suite for comparison testing",
            tests=sample_test_functions[:2],
            timeout=30.0
        )
        
        regression_system.register_test_suite(test_suite)
        
        # Run in comparison mode
        results = regression_system.run_test_suite("comparison_test_suite", comparison_mode=True)
        
        assert isinstance(results, dict)
        assert results["suite_name"] == "comparison_test_suite"
        
        # Check that test results have comparison data
        for test_result in results["test_results"]:
            assert hasattr(test_result, "before_output")
            assert hasattr(test_result, "after_output")
            assert test_result.before_output is not None
            assert test_result.after_output is not None
    
    def test_test_summary_generation(self, regression_system, sample_test_functions):
        """Test test summary generation."""
        # Create and run a test suite
        test_suite = RegressionTestSuite(
            name="summary_test_suite",
            description="Test suite for summary testing",
            tests=sample_test_functions[:2],
            timeout=30.0
        )
        
        regression_system.register_test_suite(test_suite)
        regression_system.run_test_suite("summary_test_suite")
        
        # Generate summary
        summary = regression_system.generate_test_summary("summary_test_suite")
        
        assert isinstance(summary, dict)
        assert summary["suite_name"] == "summary_test_suite"
        assert "total_tests" in summary
        assert "tests_passed" in summary
        assert "execution_time" in summary
        assert "overall_status" in summary
    
    def test_test_trends_analysis(self, regression_system, sample_test_functions):
        """Test test trends analysis."""
        # Create and run multiple test suites to build history
        for i in range(3):
            test_suite = RegressionTestSuite(
                name=f"trends_test_suite_{i}",
                description=f"Test suite {i} for trends testing",
                tests=sample_test_functions[:2],
                timeout=30.0
            )
            
            regression_system.register_test_suite(test_suite)
            regression_system.run_test_suite(f"trends_test_suite_{i}")
        
        # Analyze trends
        trends = regression_system.analyze_test_trends()
        
        assert isinstance(trends, dict)
        assert "total_runs" in trends
        assert "successful_runs" in trends
        assert "success_rate" in trends
        assert "average_execution_time" in trends
        assert "trend" in trends
        
        assert trends["total_runs"] >= 3
        assert 0.0 <= trends["success_rate"] <= 100.0
        assert trends["trend"] in ["improving", "stable", "declining"]
