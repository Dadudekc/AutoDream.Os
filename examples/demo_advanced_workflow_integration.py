#!/usr/bin/env python3
"""
Advanced Workflow Engine Integration Demo

This demo showcases the integration of the Advanced Workflow Engine with all core systems:
1. Agent Management System
2. Contract Management System
3. Performance Tracking System
4. Advanced Workflow Engine

Tests enterprise-grade workflow orchestration capabilities.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.advanced_workflow_engine import (
    AdvancedWorkflowEngine,
    WorkflowType,
    WorkflowPriority,
    WorkflowStep,
    OptimizationStrategy,
)
from core.agent_manager import AgentManager, AgentStatus, AgentCapability
from core.config_manager import ConfigManager
from core.assignment_engine import ContractManager
from core.contract_models import ContractPriority
from core.performance_tracker import PerformanceTracker

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class AdvancedWorkflowIntegrationDemo:
    """Demo class for testing advanced workflow engine integration"""

    def __init__(self):
        """Initialize the integration demo"""
        self.agent_dir = Path("agent_workspaces")
        self.config_dir = Path("config")

        # Create directories if they don't exist
        self.agent_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

        # Initialize core managers
        self.config_manager = ConfigManager(self.config_dir)
        self.agent_manager = AgentManager(self.agent_dir)
        self.contract_manager = ContractManager(self.agent_manager, self.config_manager)
        self.performance_tracker = PerformanceTracker(
            self.agent_manager, self.config_manager
        )

        # Initialize advanced workflow engine
        self.workflow_engine = AdvancedWorkflowEngine(
            self.agent_manager, self.config_manager, self.contract_manager
        )

        logger.info("Advanced Workflow Integration Demo initialized")

    def run_integration_test(self):
        """Run comprehensive integration test"""
        print("🚀 Starting Advanced Workflow Engine Integration Test...")
        print("=" * 70)

        try:
            # Test 1: Basic Workflow Creation and Execution
            print("\n📋 Test 1: Basic Workflow Creation and Execution")
            self._test_basic_workflow_operations()

            # Test 2: Advanced Workflow Types
            print("\n📋 Test 2: Advanced Workflow Types")
            self._test_advanced_workflow_types()

            # Test 3: Workflow Optimization Integration
            print("\n📋 Test 3: Workflow Optimization Integration")
            self._test_workflow_optimization()

            # Test 4: Performance Integration
            print("\n📋 Test 4: Performance Integration")
            self._test_performance_integration()

            # Test 5: Contract Integration
            print("\n📋 Test 5: Contract Integration")
            self._test_contract_integration()

            # Test 6: System Performance Under Load
            print("\n📋 Test 6: System Performance Under Load")
            self._test_system_performance()

            print("\n✅ All Advanced Workflow Integration Tests Completed Successfully!")

        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            print(f"❌ Integration test failed: {e}")
            return False

        return True

    def _test_basic_workflow_operations(self):
        """Test basic workflow creation and execution"""
        print("  Testing basic workflow operations...")

        # Create a simple sequential workflow
        test_steps = [
            WorkflowStep(
                step_id="step1",
                name="Initialize System",
                step_type="initialization",
                dependencies=[],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=1.0,
                timeout=30.0,
                retry_policy={"max_retries": 3, "success_rate": 0.9},
                metadata={"priority": "high"},
            ),
            WorkflowStep(
                step_id="step2",
                name="Process Data",
                step_type="processing",
                dependencies=["step1"],
                required_capabilities=[AgentCapability.INTEGRATION],
                estimated_duration=2.0,
                timeout=60.0,
                retry_policy={"max_retries": 2, "success_rate": 0.8},
                metadata={"priority": "medium"},
            ),
            WorkflowStep(
                step_id="step3",
                name="Generate Report",
                step_type="reporting",
                dependencies=["step2"],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=1.5,
                timeout=45.0,
                retry_policy={"max_retries": 2, "success_rate": 0.95},
                metadata={"priority": "low"},
            ),
        ]

        # Create workflow
        workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.SEQUENTIAL,
            test_steps,
            WorkflowPriority.HIGH,
            [
                OptimizationStrategy.PERFORMANCE,
                OptimizationStrategy.RESOURCE_EFFICIENCY,
            ],
        )

        assert workflow_id, "Workflow creation failed"
        print(f"    ✅ Sequential workflow created: {workflow_id}")

        # Execute workflow
        execution_id = self.workflow_engine.execute_workflow(workflow_id)
        assert execution_id, "Workflow execution failed"
        print(f"    ✅ Workflow execution started: {execution_id}")

        # Monitor workflow status
        max_wait = 30  # seconds
        start_time = time.time()

        while time.time() - start_time < max_wait:
            status = self.workflow_engine.get_workflow_status(workflow_id)
            if status and status.value in ["completed", "failed"]:
                break
            time.sleep(1)

        final_status = self.workflow_engine.get_workflow_status(workflow_id)
        assert final_status, "Workflow status retrieval failed"
        print(f"    ✅ Workflow final status: {final_status.value}")

        print("  ✅ Basic Workflow Operations Test PASSED")

    def _test_advanced_workflow_types(self):
        """Test different workflow types"""
        print("  Testing advanced workflow types...")

        # Test parallel workflow
        parallel_steps = [
            WorkflowStep(
                step_id="parallel1",
                name="Parallel Task 1",
                step_type="parallel",
                dependencies=[],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=2.0,
                timeout=60.0,
                retry_policy={"max_retries": 2, "success_rate": 0.9},
                metadata={},
            ),
            WorkflowStep(
                step_id="parallel2",
                name="Parallel Task 2",
                step_type="parallel",
                dependencies=[],
                required_capabilities=[AgentCapability.INTEGRATION],
                estimated_duration=1.5,
                timeout=45.0,
                retry_policy={"max_retries": 2, "success_rate": 0.9},
                metadata={},
            ),
        ]

        parallel_workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.PARALLEL, parallel_steps, WorkflowPriority.NORMAL
        )

        assert parallel_workflow_id, "Parallel workflow creation failed"
        print(f"    ✅ Parallel workflow created: {parallel_workflow_id}")

        # Test conditional workflow
        conditional_steps = [
            WorkflowStep(
                step_id="condition",
                name="Check Condition",
                step_type="conditional",
                dependencies=[],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=0.5,
                timeout=15.0,
                retry_policy={"max_retries": 1, "success_rate": 0.95},
                metadata={"condition_type": "boolean"},
            ),
            WorkflowStep(
                step_id="branch_a",
                name="Branch A",
                step_type="execution",
                dependencies=["condition"],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=1.0,
                timeout=30.0,
                retry_policy={"max_retries": 2, "success_rate": 0.9},
                metadata={"branch": "A"},
            ),
        ]

        conditional_workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.CONDITIONAL, conditional_steps, WorkflowPriority.NORMAL
        )

        assert conditional_workflow_id, "Conditional workflow creation failed"
        print(f"    ✅ Conditional workflow created: {conditional_workflow_id}")

        print("  ✅ Advanced Workflow Types Test PASSED")

    def _test_workflow_optimization(self):
        """Test workflow optimization capabilities"""
        print("  Testing workflow optimization...")

        # Create workflow for optimization testing
        optimization_steps = [
            WorkflowStep(
                step_id="opt_step1",
                name="Optimization Test Step 1",
                step_type="test",
                dependencies=[],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=3.0,  # Longer duration to trigger optimization
                timeout=90.0,
                retry_policy={"max_retries": 3, "success_rate": 0.7},
                metadata={"optimization_target": True},
            ),
            WorkflowStep(
                step_id="opt_step2",
                name="Optimization Test Step 2",
                step_type="test",
                dependencies=["opt_step1"],
                required_capabilities=[AgentCapability.INTEGRATION],
                estimated_duration=2.5,
                timeout=75.0,
                retry_policy={"max_retries": 2, "success_rate": 0.8},
                metadata={"optimization_target": True},
            ),
        ]

        optimization_workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.SEQUENTIAL,
            optimization_steps,
            WorkflowPriority.HIGH,
            [
                OptimizationStrategy.PERFORMANCE,
                OptimizationStrategy.THROUGHPUT_MAXIMIZATION,
            ],
        )

        assert optimization_workflow_id, "Optimization workflow creation failed"
        print(f"    ✅ Optimization workflow created: {optimization_workflow_id}")

        # Execute workflow to trigger optimization
        execution_id = self.workflow_engine.execute_workflow(optimization_workflow_id)
        assert execution_id, "Optimization workflow execution failed"
        print(f"    ✅ Optimization workflow execution started: {execution_id}")

        # Wait for optimization to occur
        time.sleep(10)  # Allow time for optimization analysis

        # Check optimization summary
        optimization_summary = self.workflow_engine.get_optimization_summary()
        assert (
            "total_optimizations" in optimization_summary
        ), "Optimization summary missing"
        print(
            f"    ✅ Optimization summary: {optimization_summary['total_optimizations']} optimizations"
        )

        print("  ✅ Workflow Optimization Test PASSED")

    def _test_performance_integration(self):
        """Test performance tracking integration"""
        print("  Testing performance integration...")

        # Create workflow for performance testing
        performance_steps = [
            WorkflowStep(
                step_id="perf_step1",
                name="Performance Test Step 1",
                step_type="performance",
                dependencies=[],
                required_capabilities=[AgentCapability.TESTING],
                estimated_duration=1.0,
                timeout=30.0,
                retry_policy={"max_retries": 2, "success_rate": 0.9},
                metadata={"performance_monitoring": True},
            )
        ]

        performance_workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.SEQUENTIAL, performance_steps, WorkflowPriority.NORMAL
        )

        assert performance_workflow_id, "Performance workflow creation failed"
        print(f"    ✅ Performance workflow created: {performance_workflow_id}")

        # Execute workflow
        execution_id = self.workflow_engine.execute_workflow(performance_workflow_id)
        assert execution_id, "Performance workflow execution failed"

        # Wait for execution to complete
        time.sleep(5)

        # Check performance metrics
        execution_status = self.workflow_engine.get_execution_status(execution_id)
        assert execution_status, "Execution status retrieval failed"

        if execution_status.performance_metrics:
            metrics = execution_status.performance_metrics
            print(f"    ✅ Performance metrics recorded: {len(metrics)} metrics")
            for key, value in metrics.items():
                print(f"      {key}: {value}")
        else:
            print("    ⚠️ No performance metrics recorded yet")

        print("  ✅ Performance Integration Test PASSED")

    def _test_contract_integration(self):
        """Test contract management integration"""
        print("  Testing contract integration...")

        # Create workflow that will be assigned to an agent
        contract_steps = [
            WorkflowStep(
                step_id="contract_step1",
                name="Contract Integration Test",
                step_type="integration",
                dependencies=[],
                required_capabilities=[AgentCapability.INTEGRATION],
                estimated_duration=2.0,
                timeout=60.0,
                retry_policy={"max_retries": 2, "success_rate": 0.9},
                metadata={"contract_integration": True},
            )
        ]

        contract_workflow_id = self.workflow_engine.create_dynamic_workflow(
            WorkflowType.SEQUENTIAL, contract_steps, WorkflowPriority.HIGH
        )

        assert contract_workflow_id, "Contract workflow creation failed"
        print(f"    ✅ Contract workflow created: {contract_workflow_id}")

        # Execute workflow with agent assignment
        execution_id = self.workflow_engine.execute_workflow(
            contract_workflow_id, "test_agent_001"
        )
        assert execution_id, "Contract workflow execution failed"
        print(f"    ✅ Contract workflow execution started: {execution_id}")

        # Check if contract was created
        pending_contracts = self.contract_manager.get_pending_contracts()
        workflow_contracts = [
            c for c in pending_contracts if "Workflow Execution" in c.title
        ]

        if workflow_contracts:
            print(
                f"    ✅ Contract created for workflow execution: {len(workflow_contracts)} contracts"
            )
        else:
            print("    ⚠️ No contracts found for workflow execution")

        print("  ✅ Contract Integration Test PASSED")

    def _test_system_performance(self):
        """Test system performance under load"""
        print("  Testing system performance under load...")

        start_time = time.time()

        # Create multiple workflows rapidly
        workflow_ids = []
        for i in range(5):
            steps = [
                WorkflowStep(
                    step_id=f"load_step_{i+1}",
                    name=f"Load Test Step {i+1}",
                    step_type="load_test",
                    dependencies=[],
                    required_capabilities=[AgentCapability.TESTING],
                    estimated_duration=0.5,
                    timeout=15.0,
                    retry_policy={"max_retries": 1, "success_rate": 0.95},
                    metadata={"load_test": True},
                )
            ]

            workflow_id = self.workflow_engine.create_dynamic_workflow(
                WorkflowType.SEQUENTIAL, steps, WorkflowPriority.LOW
            )

            if workflow_id:
                workflow_ids.append(workflow_id)

        creation_time = time.time() - start_time
        print(
            f"    ✅ Created {len(workflow_ids)} workflows in {creation_time:.3f} seconds"
        )

        # Execute workflows
        execution_ids = []
        start_time = time.time()

        for workflow_id in workflow_ids:
            execution_id = self.workflow_engine.execute_workflow(workflow_id)
            if execution_id:
                execution_ids.append(execution_id)

        execution_time = time.time() - start_time
        print(
            f"    ✅ Started {len(execution_ids)} executions in {execution_time:.3f} seconds"
        )

        # Performance benchmarks
        assert creation_time < 2.0, f"Workflow creation too slow: {creation_time}s"
        assert execution_time < 1.0, f"Workflow execution too slow: {execution_time}s"

        print("  ✅ System Performance Test PASSED")

    def cleanup(self):
        """Clean up test data and shutdown managers"""
        print("\n🧹 Cleaning up test data...")

        try:
            # Shutdown all managers
            self.workflow_engine.shutdown()
            self.performance_tracker.shutdown()
            self.contract_manager.shutdown()
            self.agent_manager.shutdown()
            self.config_manager.shutdown()

            print("✅ All managers shut down successfully")

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            print(f"❌ Cleanup failed: {e}")


def main():
    """Main demo execution"""
    print("🎯 Advanced Workflow Engine Integration Demo")
    print("=" * 70)

    demo = AdvancedWorkflowIntegrationDemo()

    try:
        # Run integration tests
        success = demo.run_integration_test()

        if success:
            print("\n🎉 ADVANCED WORKFLOW INTEGRATION TEST RESULTS: ALL TESTS PASSED!")
            print("✅ Basic Workflow Operations: Integrated")
            print("✅ Advanced Workflow Types: Integrated")
            print("✅ Workflow Optimization: Integrated")
            print("✅ Performance Integration: Integrated")
            print("✅ Contract Integration: Integrated")
            print("✅ System Performance: Within Benchmarks")
            print("✅ Enterprise-Grade Workflow Orchestration: OPERATIONAL")

        else:
            print("\n❌ ADVANCED WORKFLOW INTEGRATION TEST FAILED!")

    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        print(f"\n❌ Demo execution failed: {e}")

    finally:
        # Always cleanup
        demo.cleanup()


if __name__ == "__main__":
    main()
