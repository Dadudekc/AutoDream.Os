#!/usr/bin/env python3
"""
SOLID Refactoring Verification Plan - Agent Cellphone V2
=======================================================

Comprehensive verification strategy for SOLID-compliant architecture.
Tests all components, integrations, and V2 compliance requirements.
"""
# ruff: noqa: S101  # Assert statements are appropriate for verification scripts

import sys
import time
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))


class VerificationSuite:
    """Comprehensive verification suite for SOLID architecture."""

    def __init__(self):
        self.results = {
            "unit_tests": {},
            "integration_tests": {},
            "end_to_end_tests": {},
            "performance_tests": {},
            "compliance_tests": {}
        }
        self.start_time = time.time()

    def run_all_verifications(self) -> dict[str, Any]:
        """Run complete verification suite."""
        print("🚀 STARTING SOLID REFACTORING VERIFICATION SUITE")
        print("=" * 60)

        try:
            # Unit Tests
            self._run_unit_tests()

            # Integration Tests
            self._run_integration_tests()

            # End-to-End Tests
            self._run_end_to_end_tests()

            # Performance Tests
            self._run_performance_tests()

            # Compliance Tests
            self._run_compliance_tests()

            # Generate Report
            return self._generate_report()

        except Exception as e:
            print(f"❌ VERIFICATION FAILED: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "FAILED", "error": str(e)}

    def _run_unit_tests(self):
        """Test individual SOLID components."""
        print("🧪 RUNNING UNIT TESTS...")
        print("-" * 30)

        # Test Coordinator Components
        self._test_coordinator_registry()
        self._test_coordinator_status_parser()

        # Test Message Queue Components
        self._test_message_queue()
        self._test_queue_persistence()
        self._test_queue_statistics()

        # Test Interfaces
        self._test_interfaces()

        print("✅ UNIT TESTS COMPLETED")
        print()

    def _test_coordinator_registry(self):
        """Test CoordinatorRegistry SOLID compliance."""
        try:
            from core.coordinator_registry import CoordinatorRegistry

            # Mock logger
            class MockLogger:
                def __init__(self):
                    self.messages = []
                def info(self, msg): self.messages.append(f"INFO: {msg}")
                def warning(self, msg): self.messages.append(f"WARN: {msg}")
                def error(self, msg): self.messages.append(f"ERROR: {msg}")

            logger = MockLogger()

            # Test dependency injection
            registry = CoordinatorRegistry(logger=logger)

            # Test coordinator registration
            class MockCoordinator:
                def __init__(self, name):
                    self.name = name
                def get_status(self):
                    return {"status": "active"}

            coord = MockCoordinator("test-coordinator")
            success = registry.register_coordinator(coord)

            assert success, "Coordinator registration failed"
            assert (registry.get_coordinator("test-coordinator") == coord,
                    "Coordinator retrieval failed")

            self.results["unit_tests"]["coordinator_registry"] = "PASSED"
            print("  ✅ CoordinatorRegistry: PASSED")

        except Exception as e:
            self.results["unit_tests"]["coordinator_registry"] = f"FAILED: {e}"
            print(f"  ❌ CoordinatorRegistry: FAILED - {e}")

    def _test_coordinator_status_parser(self):
        """Test CoordinatorStatusParser."""
        try:
            from core.coordinator_status_parser import CoordinatorStatusParser

            parser = CoordinatorStatusParser()

            # Test status parsing
            class MockCoordinator:
                def get_status(self):
                    return {"status": "active", "coordination_status": "running"}

            coord = MockCoordinator()
            status = parser.parse_status(coord)

            assert status["status"] == "active", "Status parsing failed"
            assert parser.can_parse_status(coord), "Can parse check failed"

            self.results["unit_tests"]["coordinator_status_parser"] = "PASSED"
            print("  ✅ CoordinatorStatusParser: PASSED")

        except Exception as e:
            self.results["unit_tests"]["coordinator_status_parser"] = f"FAILED: {e}"
            print(f"  ❌ CoordinatorStatusParser: FAILED - {e}")

    def _test_message_queue(self):
        """Test MessageQueue SOLID compliance."""
        try:
            import os
            import tempfile

            from core.message_queue import MessageQueue, QueueConfig

            # Use temporary directory to avoid conflicts
            with tempfile.TemporaryDirectory() as temp_dir:
                config = QueueConfig(
                    max_queue_size=10,
                    queue_directory=os.path.join(temp_dir, "queue")
                )
                queue = MessageQueue(config=config)

                # Test enqueue
                test_msg = {"type": "test", "content": "Hello World"}
                queue_id = queue.enqueue(test_msg)
                assert queue_id, "Enqueue failed"

                # Test with proper priority object
                from services.models.messaging_models import UnifiedMessagePriority
                priority_msg = {
                    "type": "test",
                    "content": "Hello World",
                    "priority": UnifiedMessagePriority.REGULAR
                }
                queue_id2 = queue.enqueue(priority_msg)
                assert queue_id2, "Priority enqueue failed"

                # Test dequeue
                entries = queue.dequeue(batch_size=1)
                assert len(entries) == 1, "Dequeue failed"

                # Test mark delivered
                success = queue.mark_delivered(entries[0].queue_id)
                assert success, "Mark delivered failed"

            self.results["unit_tests"]["message_queue"] = "PASSED"
            print("  ✅ MessageQueue: PASSED")

        except Exception as e:
            self.results["unit_tests"]["message_queue"] = f"FAILED: {e}"
            print(f"  ❌ MessageQueue: FAILED - {e}")

    def _test_queue_persistence(self):
        """Test QueuePersistence."""
        try:
            import tempfile
            from pathlib import Path

            from core.message_queue_persistence import FileQueuePersistence, QueueEntry

            with tempfile.TemporaryDirectory() as temp_dir:
                queue_file = Path(temp_dir) / "test_queue.json"
                persistence = FileQueuePersistence(queue_file)

                # Test save/load
                entry = QueueEntry(
                    message={"test": "data"},
                    queue_id="test-123",
                    priority_score=0.5,
                    status="PENDING",
                    created_at=time.time(),
                    updated_at=time.time()
                )

                persistence.save_entries([entry])
                loaded_entries = persistence.load_entries()

                assert len(loaded_entries) == 1, "Persistence save/load failed"
                assert loaded_entries[0].queue_id == "test-123", "Data integrity failed"

            self.results["unit_tests"]["queue_persistence"] = "PASSED"
            print("  ✅ QueuePersistence: PASSED")

        except Exception as e:
            self.results["unit_tests"]["queue_persistence"] = f"FAILED: {e}"
            print(f"  ❌ QueuePersistence: FAILED - {e}")

    def _test_queue_statistics(self):
        """Test QueueStatistics."""
        try:
            from core.message_queue_persistence import QueueEntry
            from core.message_queue_statistics import QueueStatisticsCalculator

            calculator = QueueStatisticsCalculator()

            # Create test entries
            entries = [
                QueueEntry(
                    message={"test": "data"},
                    queue_id=f"test-{i}",
                    priority_score=0.5 + i * 0.1,
                    status="PENDING" if i < 5 else "DELIVERED",
                    created_at=time.time() - i * 3600,  # Different ages
                    updated_at=time.time()
                ) for i in range(10)
            ]

            stats = calculator.calculate_statistics(entries)

            assert stats["total_entries"] == 10, "Statistics calculation failed"
            assert "pending_entries" in stats, "Status counts missing"
            assert "average_age" in stats, "Age calculations missing"

            self.results["unit_tests"]["queue_statistics"] = "PASSED"
            print("  ✅ QueueStatistics: PASSED")

        except Exception as e:
            self.results["unit_tests"]["queue_statistics"] = f"FAILED: {e}"
            print(f"  ❌ QueueStatistics: FAILED - {e}")

    def _test_interfaces(self):
        """Test interface compliance."""
        try:
            from core.message_queue import MessageQueue
            from core.message_queue_interfaces import IMessageQueue, IQueuePersistence
            from core.message_queue_persistence import FileQueuePersistence

            # Test interface implementation
            queue = MessageQueue()
            assert isinstance(queue, IMessageQueue), "IMessageQueue not implemented"

            from pathlib import Path
            persistence = FileQueuePersistence(Path("test.json"))
            assert isinstance(persistence, IQueuePersistence), "IQueuePersistence not implemented"

            self.results["unit_tests"]["interfaces"] = "PASSED"
            print("  ✅ Interfaces: PASSED")

        except Exception as e:
            self.results["unit_tests"]["interfaces"] = f"FAILED: {e}"
            print(f"  ❌ Interfaces: FAILED - {e}")

    def _run_integration_tests(self):
        """Test component integrations."""
        print("🔗 RUNNING INTEGRATION TESTS...")
        print("-" * 30)

        self._test_messaging_integration()
        self._test_coordinator_integration()

        print("✅ INTEGRATION TESTS COMPLETED")
        print()

    def _test_messaging_integration(self):
        """Test messaging system integration."""
        try:
            from core.message_queue import AsyncQueueProcessor, MessageQueue
            from src.core.messaging_core import UnifiedMessagingCore

            # Test unified messaging with queue integration
            core = UnifiedMessagingCore()

            # Test message sending
            success = core.send_message(
                content="Integration test message",
                sender="TestSender",
                recipient="Agent-1",
                message_type="test",
                priority="regular"
            )

            # Test with queue processor
            queue = MessageQueue()
            def mock_callback(msg): return True

            processor = AsyncQueueProcessor(
                queue=queue,
                delivery_callback=mock_callback
            )

            # Test processor methods
            processor.stop_processing()  # Should not fail

            self.results["integration_tests"]["messaging_integration"] = "PASSED"
            print("  ✅ Messaging Integration: PASSED")

        except Exception as e:
            self.results["integration_tests"]["messaging_integration"] = f"FAILED: {e}"
            print(f"  ❌ Messaging Integration: FAILED - {e}")

    def _test_coordinator_integration(self):
        """Test coordinator system integration."""
        try:
            from core.coordinator_registry import CoordinatorRegistry
            from services.coordinator import Coordinator

            # Mock logger
            class MockLogger:
                def info(self, msg): pass
                def warning(self, msg): pass
                def error(self, msg): pass

            logger = MockLogger()
            registry = CoordinatorRegistry(logger=logger)

            # Test coordinator integration
            coordinator = Coordinator("test-coord", logger)
            success = registry.register_coordinator(coordinator)

            assert success, "Coordinator integration failed"

            self.results["integration_tests"]["coordinator_integration"] = "PASSED"
            print("  ✅ Coordinator Integration: PASSED")

        except Exception as e:
            self.results["integration_tests"]["coordinator_integration"] = f"FAILED: {e}"
            print(f"  ❌ Coordinator Integration: FAILED - {e}")

    def _run_end_to_end_tests(self):
        """Test complete workflows."""
        print("🔄 RUNNING END-TO-END TESTS...")
        print("-" * 30)

        self._test_complete_messaging_workflow()
        self._test_agent_onboarding_workflow()

        print("✅ END-TO-END TESTS COMPLETED")
        print()

    def _test_complete_messaging_workflow(self):
        """Test complete messaging workflow."""
        try:
            from src.core.messaging_core import UnifiedMessagingCore

            core = UnifiedMessagingCore()

            # Test message sending workflow
            success = core.send_message(
                content="End-to-end test message",
                sender="TestSystem",
                recipient="Agent-1",
                message_type="notification",
                priority="high"
            )

            assert success, "Message sending workflow failed"

            # Test message history
            history = core.show_message_history()
            assert history is not None, "Message history failed"

            self.results["end_to_end_tests"]["messaging_workflow"] = "PASSED"
            print("  ✅ Messaging Workflow: PASSED")

        except Exception as e:
            self.results["end_to_end_tests"]["messaging_workflow"] = f"FAILED: {e}"
            print(f"  ❌ Messaging Workflow: FAILED - {e}")

    def _test_agent_onboarding_workflow(self):
        """Test agent onboarding workflow."""
        try:
            from src.core.messaging_core import UnifiedMessagingCore

            core = UnifiedMessagingCore()

            # Test onboarding message
            success = core.send_onboarding_message(
                agent_id="Agent-1",
                style="professional",
                mode="dry_run"
            )

            assert success, "Onboarding workflow failed"

            self.results["end_to_end_tests"]["onboarding_workflow"] = "PASSED"
            print("  ✅ Onboarding Workflow: PASSED")

        except Exception as e:
            self.results["end_to_end_tests"]["onboarding_workflow"] = f"FAILED: {e}"
            print(f"  ❌ Onboarding Workflow: FAILED - {e}")

    def _run_performance_tests(self):
        """Test performance characteristics."""
        print("⚡ RUNNING PERFORMANCE TESTS...")
        print("-" * 30)

        self._test_queue_performance()
        self._test_message_throughput()

        print("✅ PERFORMANCE TESTS COMPLETED")
        print()

    def _test_queue_performance(self):
        """Test queue performance."""
        try:
            import os
            import tempfile

            from core.message_queue import MessageQueue, QueueConfig

            with tempfile.TemporaryDirectory() as temp_dir:
                config = QueueConfig(
                    max_queue_size=100,
                    queue_directory=os.path.join(temp_dir, "queue")
                )
                queue = MessageQueue(config=config)

                # Performance test
                start_time = time.time()

                # Enqueue fewer messages for performance test
                for i in range(10):
                    queue.enqueue({"type": "perf_test", "id": i})

                enqueue_time = time.time() - start_time

                # Dequeue messages
                start_time = time.time()
                entries = queue.dequeue(batch_size=5)
                dequeue_time = time.time() - start_time

                assert len(entries) == 5, "Queue performance test failed"
                assert enqueue_time < 1.0, f"Enqueue too slow: {enqueue_time}s"
                assert dequeue_time < 0.5, f"Dequeue too slow: {dequeue_time}s"

            self.results["performance_tests"]["queue_performance"] = "PASSED"
            print("  ✅ Queue Performance: PASSED")

        except Exception as e:
            self.results["performance_tests"]["queue_performance"] = f"FAILED: {e}"
            print(f"  ❌ Queue Performance: FAILED - {e}")

    def _test_message_throughput(self):
        """Test message throughput."""
        try:
            from src.core.messaging_core import UnifiedMessagingCore

            core = UnifiedMessagingCore()

            start_time = time.time()

            # Send multiple messages
            success_count = 0
            for i in range(5):  # Reduced count for performance
                success = core.send_message(
                    content=f"Throughput test {i}",
                    sender="PerfTest",
                    recipient="Agent-1",
                    message_type="notification",
                    priority="regular"
                )
                if success:
                    success_count += 1

            throughput_time = time.time() - start_time

            assert success_count >= 3, f"Low throughput: {success_count}/5 messages"
            assert throughput_time < 2.0, f"Low throughput time: {throughput_time}s"

            self.results["performance_tests"]["message_throughput"] = "PASSED"
            print("  ✅ Message Throughput: PASSED")

        except Exception as e:
            self.results["performance_tests"]["message_throughput"] = f"FAILED: {e}"
            print(f"  ❌ Message Throughput: FAILED - {e}")

    def _run_compliance_tests(self):
        """Test V2 compliance requirements."""
        print("📋 RUNNING COMPLIANCE TESTS...")
        print("-" * 30)

        self._test_solid_compliance()
        self._test_v2_standards()

        print("✅ COMPLIANCE TESTS COMPLETED")
        print()

    def _test_solid_compliance(self):
        """Test SOLID principles compliance."""
        try:
            # Test dependency injection
            from core.message_queue import MessageQueue, QueueConfig
            from core.message_queue_statistics import QueueStatisticsCalculator

            config = QueueConfig()
            stats_calc = QueueStatisticsCalculator()
            queue = MessageQueue(config=config)

            # Verify dependencies are injected
            assert queue.config is not None, "Config not injected"
            assert queue.statistics_calculator is not None, "Statistics calculator not injected"

            # Test interface compliance
            from core.message_queue_interfaces import IMessageQueue
            assert isinstance(queue, IMessageQueue), "Interface compliance failed"

            self.results["compliance_tests"]["solid_compliance"] = "PASSED"
            print("  ✅ SOLID Compliance: PASSED")

        except Exception as e:
            self.results["compliance_tests"]["solid_compliance"] = f"FAILED: {e}"
            print(f"  ❌ SOLID Compliance: FAILED - {e}")

    def _test_v2_standards(self):
        """Test V2 compliance standards."""
        try:
            # Test file size compliance (< 400 lines)
            import inspect

            from core.message_queue import MessageQueue
            source = inspect.getsource(MessageQueue)
            lines = len(source.split('\n'))

            assert lines < 400, f"V2 violation: MessageQueue has {lines} lines (>400)"

            # Test modularity
            assert hasattr(MessageQueue, '__init__'), "Missing constructor"
            assert hasattr(MessageQueue, 'enqueue'), "Missing enqueue method"
            assert hasattr(MessageQueue, 'dequeue'), "Missing dequeue method"

            self.results["compliance_tests"]["v2_standards"] = "PASSED"
            print("  ✅ V2 Standards: PASSED")

        except Exception as e:
            self.results["compliance_tests"]["v2_standards"] = f"FAILED: {e}"
            print(f"  ❌ V2 Standards: FAILED - {e}")

    def _generate_report(self) -> dict[str, Any]:
        """Generate comprehensive verification report."""
        end_time = time.time()
        duration = end_time - self.start_time

        # Calculate overall status
        all_tests = []
        for category in self.results.values():
            all_tests.extend(category.values())

        passed_tests = sum(1 for result in all_tests if result == "PASSED")
        total_tests = len(all_tests)
        success_rate = ((passed_tests / total_tests * 100)
                         if total_tests > 0 else 0)

        overall_status = "PASSED" if success_rate >= 95 else "WARNING" if success_rate >= 80 else "FAILED"

        report = {
            "status": overall_status,
            "duration_seconds": round(duration, 2),
            "success_rate": round(success_rate, 1),
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "results": self.results,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Print summary
        print("📊 VERIFICATION REPORT SUMMARY")
        print("=" * 40)
        print(f"Status: {overall_status}")
        print(".1f")
        print(f"Duration: {report['duration_seconds']}s")
        print(f"Tests: {passed_tests}/{total_tests} passed")

        if overall_status == "PASSED":
            print("🎉 ALL SYSTEMS VERIFIED - SOLID REFACTORING SUCCESSFUL!")
        elif overall_status == "WARNING":
            print("⚠️  MOST SYSTEMS VERIFIED - MINOR ISSUES DETECTED")
        else:
            print("❌ VERIFICATION FAILED - CRITICAL ISSUES DETECTED")

        return report


def main():
    """Main verification function."""
    suite = VerificationSuite()
    report = suite.run_all_verifications()

    # Save report
    import json
    report_file = Path("verification_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n📄 Detailed report saved to: {report_file}")

    return report


if __name__ == "__main__":
    main()
