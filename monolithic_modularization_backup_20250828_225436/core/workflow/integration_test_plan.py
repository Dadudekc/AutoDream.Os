#!/usr/bin/env python3
"""
Workflow System Integration Test Plan
====================================

Comprehensive testing plan for integrating the unified workflow system
with existing contracts and learning systems following established architecture.

Author: Agent-3 (Integration & Testing)
License: MIT
"""

import logging
import sys
from typing import Any, Dict
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from .base_workflow_engine import BaseWorkflowEngine
from .specialized.business_process_workflow import BusinessProcessWorkflow
from .consolidation_migration import WorkflowConsolidationMigrator
from .learning_integration import LearningWorkflowIntegration
from .testing.integration_test_plan_structures import (
    ContractIntegrationResult,
    LearningIntegrationResult,
    BusinessProcessIntegrationResult,
    PerformanceTestResult,
    DataModelCompatibilityResult,
)
from .testing.helpers import (
    load_contract_data,
    test_contract_workflow_integration,
    test_learning_workflow_integration,
    test_business_process_workflow_integration,
    test_performance_and_scalability,
    test_data_model_compatibility,
)


class WorkflowIntegrationTestPlan:
    """Comprehensive integration testing for unified workflow system."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{__name__}.WorkflowIntegrationTestPlan")
        self.base_engine = BaseWorkflowEngine()
        self.business_process_workflow = BusinessProcessWorkflow()
        self.consolidation_migrator = WorkflowConsolidationMigrator()
        self.learning_integration = LearningWorkflowIntegration()
        self.contract_data: Dict[str, Any] = {}
        self.contract_workflows: Dict[str, str] = {}
        self.logger.info(
            "🚀 Workflow Integration Test Plan initialized using existing unified systems"
        )

    def run_comprehensive_integration_test(self) -> Dict[str, Any]:
        """Run comprehensive integration testing suite."""
        self.logger.info("🚀 Starting comprehensive integration testing...")
        start_time = datetime.now()

        self.contract_data = load_contract_data(self.logger)
        contract_results = test_contract_workflow_integration(
            self.base_engine, self.contract_data, self.logger, self.contract_workflows
        )
        learning_results = test_learning_workflow_integration(
            self.learning_integration, self.logger
        )
        business_results = test_business_process_workflow_integration(
            self.business_process_workflow, self.logger
        )
        performance_results = test_performance_and_scalability(
            self.base_engine, self.logger
        )
        compatibility_results = test_data_model_compatibility(
            self.base_engine, self.business_process_workflow, self.logger
        )

        test_suites = {
            "contract_integration": asdict(contract_results),
            "learning_integration": asdict(learning_results),
            "business_process_integration": asdict(business_results),
            "performance_testing": asdict(performance_results),
            "data_model_compatibility": asdict(compatibility_results),
        }

        total_tests = (
            contract_results.integration_success + contract_results.integration_failures
            + learning_results.integration_success + learning_results.integration_failures
            + business_results.integration_success + business_results.integration_failures
            + compatibility_results.compatibility_success + compatibility_results.compatibility_failures
        )
        total_successes = (
            contract_results.integration_success
            + learning_results.integration_success
            + business_results.integration_success
            + compatibility_results.compatibility_success
        )
        total_failures = (
            contract_results.integration_failures
            + learning_results.integration_failures
            + business_results.integration_failures
            + compatibility_results.compatibility_failures
        )

        end_time = datetime.now()
        test_duration = (end_time - start_time).total_seconds()

        comprehensive_results = {
            "test_execution_time": test_duration,
            "total_tests": total_tests,
            "total_successes": total_successes,
            "total_failures": total_failures,
            "success_rate": (total_successes / total_tests * 100) if total_tests > 0 else 0,
            "test_suites": test_suites,
            "overall_status": "PASSED"
            if total_failures == 0
            else "PARTIAL" if total_successes > 0 else "FAILED",
            "timestamp": datetime.now().isoformat(),
        }

        self.logger.info("🎉 Comprehensive integration testing complete!")
        self.logger.info(
            f"📊 Results: {total_successes}/{total_tests} tests passed ({comprehensive_results['success_rate']:.1f}%)"
        )
        self.logger.info(f"⏱️ Duration: {test_duration:.2f} seconds")
        self.logger.info(
            f"📈 Overall Status: {comprehensive_results['overall_status']}"
        )

        return comprehensive_results

    def generate_integration_report(self) -> str:
        """Generate comprehensive integration test report."""
        try:
            results = self.run_comprehensive_integration_test()
            report = f"""
🎯 WORKFLOW SYSTEM INTEGRATION TEST REPORT
=========================================

📅 Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
⏱️ Test Duration: {results['test_execution_time']:.2f} seconds
📊 Overall Status: {results['overall_status']}

📈 TEST SUMMARY
---------------
Total Tests: {results['total_tests']}
Successful: {results['total_successes']}
Failed: {results['total_failures']}
Success Rate: {results['success_rate']:.1f}%

🔍 DETAILED RESULTS
-------------------

1. CONTRACT INTEGRATION TESTING
   - Status: {'✅ PASSED' if 'error' not in results['test_suites']['contract_integration'] else '❌ FAILED'}
   - Workflows Created: {results['test_suites']['contract_integration'].get('workflows_created', 0)}
   - Integration Success: {results['test_suites']['contract_integration'].get('integration_success', 0)}

2. LEARNING WORKFLOW INTEGRATION TESTING
   - Status: {'✅ PASSED' if 'error' not in results['test_suites']['learning_integration'] else '❌ FAILED'}
   - Learning Workflows: {results['test_suites']['learning_integration'].get('learning_workflows_created', 0)}
   - Decision Workflows: {results['test_suites']['learning_integration'].get('decision_workflows_created', 0)}

3. BUSINESS PROCESS INTEGRATION TESTING
   - Status: {'✅ PASSED' if 'error' not in results['test_suites']['business_process_integration'] else '❌ FAILED'}
   - Business Processes: {results['test_suites']['business_process_integration'].get('business_processes_created', 0)}
   - Approval Workflows: {results['test_suites']['business_process_integration'].get('approval_workflows', 0)}

4. PERFORMANCE TESTING
   - Status: {'✅ PASSED' if 'error' not in results['test_suites']['performance_testing'] else '❌ FAILED'}
   - Performance Score: {results['test_suites']['performance_testing'].get('performance_score', 0):.1f}/100
   - Concurrent Workflows: {results['test_suites']['performance_testing'].get('concurrent_workflows', 0)}

5. DATA MODEL COMPATIBILITY TESTING
   - Status: {'✅ PASSED' if 'error' not in results['test_suites']['data_model_compatibility'] else '❌ FAILED'}
   - Models Tested: {results['test_suites']['data_model_compatibility'].get('models_tested', 0)}
   - Compatibility Success: {results['test_suites']['data_model_compatibility'].get('compatibility_success', 0)}

🎯 RECOMMENDATIONS
------------------
"""
            if results['overall_status'] == 'PASSED':
                report += "✅ All integration tests passed successfully. Workflow system is ready for production use."
            elif results['overall_status'] == 'PARTIAL':
                report += (
                    "⚠️ Some integration tests failed. Review failed tests and address issues before production deployment."
                )
            else:
                report += (
                    "❌ Multiple integration tests failed. System requires significant fixes before production use."
                )
            report += f"""

📋 NEXT STEPS
-------------
1. Review detailed test results for any failures
2. Address identified issues and re-run tests
3. Validate system performance under load
4. Deploy to staging environment for further testing
5. Prepare production deployment plan

🔗 INTEGRATION STATUS
---------------------
Contract Integration: {'✅ READY' if results['test_suites']['contract_integration'].get('integration_success', 0) > 0 else '❌ NOT READY'}
Learning Integration: {'✅ READY' if results['test_suites']['learning_integration'].get('integration_success', 0) > 0 else '❌ NOT READY'}
Business Process Integration: {'✅ READY' if results['test_suites']['business_process_integration'].get('integration_success', 0) > 0 else '❌ NOT READY'}
Performance: {'✅ READY' if results['test_suites']['performance_testing'].get('performance_score', 0) >= 80 else '⚠️ NEEDS IMPROVEMENT'}
Data Model Compatibility: {'✅ READY' if results['test_suites']['data_model_compatibility'].get('compatibility_success', 0) > 0 else '❌ NOT READY'}

---
Report Generated: {datetime.now().isoformat()}
Agent: Agent-3 (Integration & Testing)
"""
            return report
        except Exception as e:
            self.logger.error(f"❌ Failed to generate integration report: {e}")
            return f"❌ Error generating report: {str(e)}"


if __name__ == "__main__":
    test_plan = WorkflowIntegrationTestPlan()
    report = test_plan.generate_integration_report()
    print(report)
    with open("workflow_integration_test_report.md", "w") as f:
        f.write(report)
    print("\n📄 Report saved to: workflow_integration_test_report.md")
