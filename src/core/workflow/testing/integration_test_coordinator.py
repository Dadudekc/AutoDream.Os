#!/usr/bin/env python3
"""
Integration Test Coordinator - Test Execution Management
======================================================

Coordinates and manages integration test execution for workflow system.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from .integration_test_core import IntegrationTestCore


class IntegrationTestCoordinator:
    """
    Coordinates integration test execution and reporting.
    
    Single responsibility: Manage test execution flow and reporting
    following V2 standards.
    """
    
    def __init__(self):
        """Initialize test coordinator."""
        self.logger = logging.getLogger(f"{__name__}.IntegrationTestCoordinator")
        self.test_core = IntegrationTestCore()
        self.execution_history: List[Dict[str, Any]] = []
        
        self.logger.info("✅ Integration Test Coordinator initialized")
    
    def execute_full_test_suite(self) -> Dict[str, Any]:
        """Execute complete integration test suite."""
        self.logger.info("🚀 Starting full integration test suite...")
        
        execution_id = f"test_suite_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Load contract data
        contract_data = self.test_core.load_contract_data()
        
        # Execute tests
        test_results = self.test_core.run_basic_integration_tests()
        
        # Generate execution report
        execution_report = {
            "execution_id": execution_id,
            "timestamp": datetime.now().isoformat(),
            "contract_data_loaded": bool(contract_data),
            "test_results": test_results,
            "summary": self.test_core.get_test_summary()
        }
        
        # Store execution history
        self.execution_history.append(execution_report)
        
        self.logger.info(f"✅ Test suite completed: {execution_id}")
        return execution_report
    
    def execute_specific_test(self, test_name: str) -> Dict[str, Any]:
        """Execute specific integration test."""
        self.logger.info(f"🧪 Executing specific test: {test_name}")
        
        if test_name == "workflow_engine":
            result = self.test_core._test_workflow_engine()
        elif test_name == "business_process":
            result = self.test_core._test_business_process()
        elif test_name == "learning_integration":
            result = self.test_core._test_learning_integration()
        else:
            result = {
                "status": "FAILED",
                "error": f"Unknown test: {test_name}",
                "message": "Test not found"
            }
        
        return result
    
    def get_execution_history(self) -> List[Dict[str, Any]]:
        """Get test execution history."""
        return self.execution_history
    
    def get_latest_results(self) -> Optional[Dict[str, Any]]:
        """Get latest test execution results."""
        if self.execution_history:
            return self.execution_history[-1]
        return None
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report."""
        latest_results = self.get_latest_results()
        
        if not latest_results:
            return {"status": "NO_TESTS_EXECUTED"}
        
        # Calculate success rate
        test_results = latest_results.get("test_results", {})
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() 
                          if result.get("status") == "PASSED")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        return {
            "execution_id": latest_results.get("execution_id"),
            "timestamp": latest_results.get("timestamp"),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "success_rate": f"{success_rate:.1f}%",
            "test_details": test_results,
            "contract_data_loaded": latest_results.get("contract_data_loaded", False)
        }
