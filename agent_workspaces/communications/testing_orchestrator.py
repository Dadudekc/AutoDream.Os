#!/usr/bin/env python3
"""
Testing Orchestrator Module
===========================

Main orchestrator for interaction system testing.
Follows V2 standards: ≤400 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from .testing_core import TestingCore, TestSuite, TestCategory
from .test_executor import TestExecutor, TestExecutionConfig


class TestingOrchestrator:
    """Main orchestrator for interaction system testing"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.logger = self._setup_logging()
        self.config_file = config_file
        
        # Initialize core components
        self.testing_core = TestingCore()
        self.test_executor = TestExecutor(self.testing_core)
        
        # Testing state
        self.is_running = False
        self.current_test_session = None
        self.session_start_time = None
        
        # Load configuration if provided
        if config_file:
            self._load_configuration()
        
        # Register default test suites
        self._register_default_test_suites()
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the orchestrator"""
        logger = logging.getLogger("TestingOrchestrator")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '[ORCHESTRATOR] %(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            
        return logger
    
    def _load_configuration(self) -> None:
        """Load configuration from file"""
        try:
            if Path(self.config_file).exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Apply configuration to test executor
                if 'execution_config' in config:
                    exec_config = TestExecutionConfig(**config['execution_config'])
                    self.test_executor.config = exec_config
                
                self.logger.info(f"Configuration loaded from {self.config_file}")
            else:
                self.logger.warning(f"Configuration file {self.config_file} not found")
                
        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
    
    def _register_default_test_suites(self) -> None:
        """Register default test suites for common testing scenarios"""
        try:
            # Communication test suite
            comm_suite = TestSuite(
                suite_id="communication_basic",
                name="Basic Communication Tests",
                description="Tests basic agent communication capabilities",
                tests=["comm_test_1", "comm_test_2", "comm_test_3"],
                category=TestCategory.COMMUNICATION,
                timeout_seconds=120
            )
            self.testing_core.register_test_suite(comm_suite)
            
            # Protocol test suite
            protocol_suite = TestSuite(
                suite_id="protocol_validation",
                name="Protocol Validation Tests",
                description="Tests communication protocol compliance",
                tests=["protocol_test_1", "protocol_test_2"],
                category=TestCategory.PROTOCOL,
                timeout_seconds=180
            )
            self.testing_core.register_test_suite(protocol_suite)
            
            # Performance test suite
            perf_suite = TestSuite(
                suite_id="performance_benchmark",
                name="Performance Benchmark Tests",
                description="Tests system performance under various loads",
                tests=["perf_test_1", "perf_test_2", "perf_test_3"],
                category=TestCategory.PERFORMANCE,
                timeout_seconds=300
            )
            self.testing_core.register_test_suite(perf_suite)
            
            self.logger.info("Default test suites registered")
            
        except Exception as e:
            self.logger.error(f"Error registering default test suites: {e}")
    
    def start_testing_session(self, session_name: str = None) -> bool:
        """Start a new testing session"""
        try:
            if self.is_running:
                self.logger.warning("Testing session is already running")
                return True
            
            session_name = session_name or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            self.is_running = True
            self.current_test_session = session_name
            self.session_start_time = datetime.now()
            
            self.logger.info(f"Testing session started: {session_name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error starting testing session: {e}")
            return False
    
    def stop_testing_session(self) -> bool:
        """Stop the current testing session"""
        try:
            if not self.is_running:
                self.logger.warning("No testing session is running")
                return True
            
            # Stop all running tests
            self.test_executor.stop_all_tests()
            
            self.is_running = False
            session_duration = datetime.now() - self.session_start_time if self.session_start_time else timedelta(0)
            
            self.logger.info(f"Testing session stopped: {self.current_test_session} (duration: {session_duration})")
            
            # Reset session state
            self.current_test_session = None
            self.session_start_time = None
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error stopping testing session: {e}")
            return False
    
    def run_comprehensive_test_suite(self) -> Dict[str, Any]:
        """Run a comprehensive test suite covering all categories"""
        try:
            if not self.is_running:
                return {"error": "No testing session is running"}
            
            self.logger.info("Starting comprehensive test suite execution")
            
            comprehensive_results = {
                "session_name": self.current_test_session,
                "start_time": datetime.now().isoformat(),
                "categories_tested": [],
                "total_suites_executed": 0,
                "total_tests_executed": 0,
                "total_tests_passed": 0,
                "total_tests_failed": 0,
                "category_results": {}
            }
            
            # Test each category
            for category in TestCategory:
                self.logger.info(f"Testing category: {category.value}")
                
                category_result = self.test_executor.execute_tests_by_category(category)
                if "error" not in category_result:
                    comprehensive_results["categories_tested"].append(category.value)
                    comprehensive_results["total_suites_executed"] += category_result["suites_executed"]
                    comprehensive_results["total_tests_executed"] += category_result["total_tests_executed"]
                    comprehensive_results["total_tests_passed"] += category_result["total_tests_passed"]
                    comprehensive_results["total_tests_failed"] += category_result["total_tests_failed"]
                    comprehensive_results["category_results"][category.value] = category_result
            
            # Calculate overall success rate
            comprehensive_results["end_time"] = datetime.now().isoformat()
            comprehensive_results["overall_success_rate"] = (
                comprehensive_results["total_tests_passed"] / comprehensive_results["total_tests_executed"]
                if comprehensive_results["total_tests_executed"] > 0 else 0.0
            )
            
            self.logger.info(f"Comprehensive test suite completed: {comprehensive_results['total_tests_passed']}/{comprehensive_results['total_tests_executed']} passed")
            return comprehensive_results
            
        except Exception as e:
            self.logger.error(f"Error running comprehensive test suite: {e}")
            return {"error": str(e)}
    
    def run_focused_testing(self, categories: List[TestCategory], max_tests_per_category: int = 5) -> Dict[str, Any]:
        """Run focused testing on specific categories"""
        try:
            if not self.is_running:
                return {"error": "No testing session is running"}
            
            self.logger.info(f"Starting focused testing on categories: {[c.value for c in categories]}")
            
            focused_results = {
                "session_name": self.current_test_session,
                "start_time": datetime.now().isoformat(),
                "categories_tested": [c.value for c in categories],
                "max_tests_per_category": max_tests_per_category,
                "category_results": {}
            }
            
            for category in categories:
                self.logger.info(f"Testing category: {category.value} (max {max_tests_per_category} tests)")
                
                category_result = self.test_executor.execute_tests_by_category(category, max_tests_per_category)
                if "error" not in category_result:
                    focused_results["category_results"][category.value] = category_result
            
            focused_results["end_time"] = datetime.now().isoformat()
            
            self.logger.info("Focused testing completed")
            return focused_results
            
        except Exception as e:
            self.logger.error(f"Error running focused testing: {e}")
            return {"error": str(e)}
    
    def run_performance_benchmark(self, test_count: int = 20) -> Dict[str, Any]:
        """Run performance benchmarking tests"""
        try:
            if not self.is_running:
                return {"error": "No testing session is running"}
            
            self.logger.info(f"Starting performance benchmark ({test_count} tests)")
            
            performance_results = self.test_executor.run_performance_tests(test_count)
            performance_results["session_name"] = self.current_test_session
            
            self.logger.info("Performance benchmark completed")
            return performance_results
            
        except Exception as e:
            self.logger.error(f"Error running performance benchmark: {e}")
            return {"error": str(e)}
    
    def generate_test_report(self, output_file: str = None) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        try:
            if not output_file:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = f"test_report_{timestamp}.json"
            
            # Get test summary
            test_summary = self.testing_core.get_test_summary()
            
            # Get execution status
            execution_status = self.test_executor.get_execution_status()
            
            # Generate report
            report = {
                "report_timestamp": datetime.now().isoformat(),
                "session_info": {
                    "session_name": self.current_test_session,
                    "session_running": self.is_running,
                    "session_start_time": self.session_start_time.isoformat() if self.session_start_time else None
                },
                "test_summary": test_summary,
                "execution_status": execution_status,
                "test_suites": [asdict(s) for s in self.testing_core.test_suites.values()],
                "recommendations": self._generate_recommendations(test_summary)
            }
            
            # Save report to file
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            self.logger.info(f"Test report generated: {output_file}")
            return report
            
        except Exception as e:
            self.logger.error(f"Error generating test report: {e}")
            return {"error": str(e)}
    
    def _generate_recommendations(self, test_summary: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on test results"""
        try:
            recommendations = []
            
            if "error" in test_summary:
                recommendations.append("Review test execution errors and fix underlying issues")
                return recommendations
            
            success_rate = test_summary.get("success_rate", 0.0)
            
            if success_rate < 0.5:
                recommendations.append("Critical: Test success rate is below 50%. Review and fix failing tests immediately.")
            elif success_rate < 0.8:
                recommendations.append("Warning: Test success rate is below 80%. Investigate failing tests.")
            elif success_rate < 0.95:
                recommendations.append("Good: Test success rate is above 80%. Consider improving remaining failing tests.")
            else:
                recommendations.append("Excellent: Test success rate is above 95%. System is performing well.")
            
            # Performance recommendations
            avg_duration = test_summary.get("average_duration_seconds", 0.0)
            if avg_duration > 10.0:
                recommendations.append("Performance: Consider optimizing slow tests to improve execution time.")
            
            return recommendations
            
        except Exception as e:
            self.logger.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            return {
                "orchestrator_status": {
                    "is_running": self.is_running,
                    "current_session": self.current_test_session,
                    "session_start_time": self.session_start_time.isoformat() if self.session_start_time else None
                },
                "testing_core_status": {
                    "registered_suites": len(self.testing_core.test_suites),
                    "total_results": len(self.testing_core.test_results)
                },
                "executor_status": self.test_executor.get_execution_status(),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
