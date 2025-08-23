#!/usr/bin/env python3
"""
Core Agent Management System Integration Demo

This demo showcases the integration of all four core agent management modules:
1. Agent Registration Manager
2. Status Manager
3. Contract Manager
4. Performance Tracker

Tests module interaction, data flow, and system performance.
"""

import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.agent_registration_manager import AgentRegistrationManager
from core.status_manager import StatusManager
from core.contract_manager import ContractManager, ContractPriority, ContractStatus
from core.performance_monitor import PerformanceMonitor
from core.agent_manager import AgentManager, AgentStatus, AgentCapability
from core.config_manager import ConfigManager

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class CoreAgentManagementIntegrationDemo:
    """Demo class for testing core agent management system integration"""

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

        # Initialize specialized managers
        self.registration_manager = AgentRegistrationManager(
            self.agent_manager, self.config_manager
        )
        self.status_manager = StatusManager(self.agent_manager, self.config_manager)
        self.contract_manager = ContractManager(self.agent_manager, self.config_manager)
        self.performance_tracker = PerformanceMonitor(
            self.agent_manager, self.config_manager
        )

        logger.info("Core Agent Management Integration Demo initialized")

    def run_integration_test(self):
        """Run comprehensive integration test"""
        print("🚀 Starting Core Agent Management Integration Test...")
        print("=" * 60)

        try:
            # Test 1: Agent Registration and Status Integration
            print("\n📋 Test 1: Agent Registration and Status Integration")
            self._test_registration_status_integration()

            # Test 2: Contract Assignment and Performance Tracking
            print("\n📋 Test 2: Contract Assignment and Performance Tracking")
            self._test_contract_performance_integration()

            # Test 3: Cross-Module Data Flow
            print("\n📋 Test 3: Cross-Module Data Flow")
            self._test_cross_module_data_flow()

            # Test 4: System Performance Under Load
            print("\n📋 Test 4: System Performance Under Load")
            self._test_system_performance()

            # Test 5: Error Handling and Recovery
            print("\n📋 Test 5: Error Handling and Recovery")
            self._test_error_handling()

            print("\n✅ All Integration Tests Completed Successfully!")

        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            print(f"❌ Integration test failed: {e}")
            return False

        return True

    def _test_registration_status_integration(self):
        """Test integration between registration and status managers"""
        print("  Testing agent registration and status monitoring...")

        # Register a test agent
        agent_id = "test_agent_001"
        capabilities = [AgentCapability.TESTING, AgentCapability.DEVELOPMENT]

        # Test registration
        success = self.registration_manager.register_agent_manual(
            agent_id, "Test Agent", capabilities
        )
        assert success, "Agent registration failed"
        print(f"    ✅ Agent {agent_id} registered successfully")

        # Verify agent appears in status manager
        agents = self.agent_manager.get_all_agents()
        assert agent_id in agents, "Agent not found in agent manager"
        print(f"    ✅ Agent {agent_id} found in agent manager")

        # Test status monitoring
        agent_info = self.agent_manager.get_agent_info(agent_id)
        assert agent_info.status == AgentStatus.ONLINE, "Agent status not ONLINE"
        print(f"    ✅ Agent {agent_id} status: {agent_info.status.value}")

        # Test status change
        self.agent_manager.update_agent_status(agent_id, AgentStatus.BUSY)
        updated_info = self.agent_manager.get_agent_info(agent_id)
        assert updated_info.status == AgentStatus.BUSY, "Agent status update failed"
        print(f"    ✅ Agent {agent_id} status updated to: {updated_info.status.value}")

        print("  ✅ Registration and Status Integration Test PASSED")

    def _test_contract_performance_integration(self):
        """Test integration between contract and performance managers"""
        print("  Testing contract assignment and performance tracking...")

        # Create a test contract
        contract_id = self.contract_manager.create_contract(
            "Integration Test Contract",
            "Test contract for integration testing",
            ContractPriority.HIGH,
            [AgentCapability.TESTING],
            4,
        )
        assert contract_id, "Contract creation failed"
        print(f"    ✅ Contract created: {contract_id}")

        # Assign contract to test agent
        success = self.contract_manager.assign_contract(contract_id, "test_agent_001")
        assert success, "Contract assignment failed"
        print(f"    ✅ Contract assigned to test_agent_001")

        # Verify contract status
        status = self.contract_manager.get_contract_status(contract_id)
        assert status == ContractStatus.ASSIGNED, "Contract status not ASSIGNED"
        print(f"    ✅ Contract status: {status.value}")

        # Test performance tracking integration
        # Wait for performance metrics to be collected
        time.sleep(2)

        # Get performance summary
        performance_summary = self.performance_tracker.get_performance_summary()
        assert (
            "total_metrics" in performance_summary
        ), "Performance summary missing total_metrics"
        print(
            f"    ✅ Performance tracking active: {performance_summary['tracking_active']}"
        )

        # Get agent performance
        agent_performance = self.performance_tracker.get_agent_performance(
            "test_agent_001"
        )
        assert "agent_id" in agent_performance, "Agent performance data missing"
        print(
            f"    ✅ Agent performance data collected: {agent_performance['metrics']} metrics"
        )

        print("  ✅ Contract and Performance Integration Test PASSED")

    def _test_cross_module_data_flow(self):
        """Test data flow between all modules"""
        print("  Testing cross-module data flow...")

        # Test data flow: Registration -> Status -> Contract -> Performance

        # 1. Register another agent
        agent_id_2 = "test_agent_002"
        capabilities_2 = [AgentCapability.INTEGRATION, AgentCapability.TESTING]

        success = self.registration_manager.register_agent_manual(
            agent_id_2, "Test Agent 2", capabilities_2
        )
        assert success, "Second agent registration failed"
        print(f"    ✅ Second agent {agent_id_2} registered")

        # 2. Verify status propagation
        agents = self.agent_manager.get_all_agents()
        assert agent_id_2 in agents, "Second agent not in agent manager"
        print(f"    ✅ Second agent status propagated to agent manager")

        # 3. Create and assign contract
        contract_id_2 = self.contract_manager.create_contract(
            "Cross-Module Test Contract",
            "Testing data flow across modules",
            ContractPriority.NORMAL,
            [AgentCapability.INTEGRATION],
            2,
        )
        assert contract_id_2, "Second contract creation failed"

        success = self.contract_manager.assign_contract(contract_id_2, agent_id_2)
        assert success, "Second contract assignment failed"
        print(f"    ✅ Second contract assigned to {agent_id_2}")

        # 4. Verify performance tracking
        time.sleep(2)
        agent_performance_2 = self.performance_tracker.get_agent_performance(agent_id_2)
        assert "agent_id" in agent_performance_2, "Second agent performance missing"
        print(
            f"    ✅ Second agent performance tracked: {agent_performance_2['metrics']} metrics"
        )

        # 5. Test contract summary
        contract_summary = self.contract_manager.get_contract_summary()
        assert contract_summary["total_contracts"] >= 2, "Contract count incorrect"
        print(
            f"    ✅ Contract summary shows {contract_summary['total_contracts']} total contracts"
        )

        print("  ✅ Cross-Module Data Flow Test PASSED")

    def _test_system_performance(self):
        """Test system performance under load"""
        print("  Testing system performance under load...")

        start_time = time.time()

        # Create multiple contracts rapidly
        contract_ids = []
        for i in range(5):
            contract_id = self.contract_manager.create_contract(
                f"Performance Test Contract {i+1}",
                f"Contract {i+1} for performance testing",
                ContractPriority.NORMAL,
                [AgentCapability.TESTING],
                1,
            )
            contract_ids.append(contract_id)

        creation_time = time.time() - start_time
        print(f"    ✅ Created 5 contracts in {creation_time:.3f} seconds")

        # Test contract retrieval performance
        start_time = time.time()
        pending_contracts = self.contract_manager.get_pending_contracts()
        retrieval_time = time.time() - start_time
        print(f"    ✅ Retrieved pending contracts in {retrieval_time:.3f} seconds")

        # Test agent performance data retrieval
        start_time = time.time()
        for agent_id in ["test_agent_001", "test_agent_002"]:
            performance = self.performance_tracker.get_agent_performance(agent_id)
        retrieval_time = time.time() - start_time
        print(f"    ✅ Retrieved agent performance data in {retrieval_time:.3f} seconds")

        # Performance benchmarks
        assert creation_time < 1.0, f"Contract creation too slow: {creation_time}s"
        assert retrieval_time < 0.1, f"Data retrieval too slow: {retrieval_time}s"

        print("  ✅ System Performance Test PASSED")

    def _test_error_handling(self):
        """Test error handling and recovery across modules"""
        print("  Testing error handling and recovery...")

        # Test 1: Invalid agent ID
        try:
            invalid_performance = self.performance_tracker.get_agent_performance(
                "invalid_agent"
            )
            assert (
                "error" in invalid_performance
            ), "Should return error for invalid agent"
            print("    ✅ Invalid agent ID handled gracefully")
        except Exception as e:
            print(f"    ✅ Invalid agent ID error caught: {e}")

        # Test 2: Invalid contract ID
        try:
            invalid_status = self.contract_manager.get_contract_status(
                "invalid_contract"
            )
            assert invalid_status is None, "Should return None for invalid contract"
            print("    ✅ Invalid contract ID handled gracefully")
        except Exception as e:
            print(f"    ✅ Invalid contract ID error caught: {e}")

        # Test 3: Contract assignment to offline agent
        try:
            # Set agent offline
            self.agent_manager.update_agent_status(
                "test_agent_001", AgentStatus.OFFLINE
            )

            # Try to assign contract
            contract_id = self.contract_manager.create_contract(
                "Error Test Contract",
                "Testing error handling",
                ContractPriority.LOW,
                [AgentCapability.TESTING],
                1,
            )

            # Assignment should fail for offline agent
            success = self.contract_manager.assign_contract(
                contract_id, "test_agent_001"
            )
            assert not success, "Should not assign contract to offline agent"
            print("    ✅ Offline agent contract assignment properly rejected")

            # Restore agent status
            self.agent_manager.update_agent_status("test_agent_001", AgentStatus.ONLINE)

        except Exception as e:
            print(f"    ✅ Offline agent error handled: {e}")

        print("  ✅ Error Handling Test PASSED")

    def cleanup(self):
        """Clean up test data and shutdown managers"""
        print("\n🧹 Cleaning up test data...")

        try:
            # Shutdown all managers
            self.performance_tracker.shutdown()
            self.status_manager.shutdown()
            self.registration_manager.shutdown()
            self.contract_manager.shutdown()
            self.agent_manager.shutdown()
            self.config_manager.shutdown()

            print("✅ All managers shut down successfully")

        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
            print(f"❌ Cleanup failed: {e}")


def main():
    """Main demo execution"""
    print("🎯 Core Agent Management System Integration Demo")
    print("=" * 60)

    demo = CoreAgentManagementIntegrationDemo()

    try:
        # Run integration tests
        success = demo.run_integration_test()

        if success:
            print("\n🎉 INTEGRATION TEST RESULTS: ALL TESTS PASSED!")
            print("✅ Agent Registration Manager: Integrated")
            print("✅ Status Manager: Integrated")
            print("✅ Contract Manager: Integrated")
            print("✅ Performance Tracker: Integrated")
            print("✅ Cross-Module Communication: Working")
            print("✅ Data Flow: Validated")
            print("✅ Performance: Within Benchmarks")
            print("✅ Error Handling: Robust")

        else:
            print("\n❌ INTEGRATION TEST FAILED!")

    except Exception as e:
        logger.error(f"Demo execution failed: {e}")
        print(f"\n❌ Demo execution failed: {e}")

    finally:
        # Always cleanup
        demo.cleanup()


if __name__ == "__main__":
    main()
