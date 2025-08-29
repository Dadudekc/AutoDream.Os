#!/usr/bin/env python3
"""
Integration Test Interface - Simple Testing Interface
===================================================

Simple interface for running integration tests.
Follows V2 standards: ≤200 LOC, single responsibility.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
from typing import Dict, Any

from .testing.integration_test_coordinator import IntegrationTestCoordinator


class IntegrationTestInterface:
    """
    Simple interface for integration testing.
    
    Single responsibility: Provide simple interface for running tests
    following V2 standards.
    """
    
    def __init__(self):
        """Initialize test interface."""
        self.logger = logging.getLogger(f"{__name__}.IntegrationTestInterface")
        self.coordinator = IntegrationTestCoordinator()
        
        self.logger.info("✅ Integration Test Interface initialized")
    
    def run_tests(self) -> Dict[str, Any]:
        """Run all integration tests."""
        self.logger.info("🚀 Running integration tests...")
        return self.coordinator.execute_full_test_suite()
    
    def run_specific_test(self, test_name: str) -> Dict[str, Any]:
        """Run specific integration test."""
        self.logger.info(f"🧪 Running specific test: {test_name}")
        return self.coordinator.execute_specific_test(test_name)
    
    def get_results(self) -> Dict[str, Any]:
        """Get latest test results."""
        return self.coordinator.generate_test_report()
    
    def get_status(self) -> str:
        """Get testing system status."""
        latest_results = self.coordinator.get_latest_results()
        if not latest_results:
            return "NO_TESTS_EXECUTED"
        
        test_results = latest_results.get("test_results", {})
        total_tests = len(test_results)
        passed_tests = sum(1 for result in test_results.values() 
                          if result.get("status") == "PASSED")
        
        if total_tests == 0:
            return "NO_TESTS_RUN"
        elif passed_tests == total_tests:
            return "ALL_TESTS_PASSED"
        else:
            return f"{passed_tests}/{total_tests} TESTS_PASSED"


def run_integration_tests():
    """Simple function to run integration tests."""
    interface = IntegrationTestInterface()
    results = interface.run_tests()
    
    print("🧪 INTEGRATION TEST RESULTS")
    print("=" * 40)
    
    for test_name, result in results.get("test_results", {}).items():
        status = result.get("status", "UNKNOWN")
        message = result.get("message", "No message")
        
        if status == "PASSED":
            print(f"✅ {test_name}: {message}")
        else:
            print(f"❌ {test_name}: {message}")
    
    print(f"\n📊 Summary: {interface.get_status()}")
    return results


if __name__ == "__main__":
    run_integration_tests()
