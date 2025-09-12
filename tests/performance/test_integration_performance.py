#!/usr/bin/env python3
"""
PERFORMANCE TESTS - Integration Service Performance Validation
============================================================

CRITICAL PERFORMANCE TESTING for Agent-1 Final Pytest Assignment:
- Load testing for consolidated services
- Performance benchmarks and scalability testing
- Memory usage and resource consumption analysis

Target: Performance validation for 92%+ integration coverage
Execution: IMMEDIATE - FINAL PYTEST ASSIGNMENT

Author: Agent-1 (Integration & Core Systems Specialist)
Mission: FINAL PYTEST COVERAGE - PERFORMANCE VALIDATION
"""

import os
import statistics
import sys
import time
from pathlib import Path
from unittest.mock import Mock, patch

import psutil
import pytest

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

try:
    from services.consolidated_coordination_service import ConsolidatedCoordinationService
    from services.consolidated_messaging_service import ConsolidatedMessagingService
    from services.consolidated_vector_service import ConsolidatedVectorService
    from services.models.messaging_models import (
        UnifiedMessage,
        UnifiedMessagePriority,
        UnifiedMessageType,
    )
    from services.models.vector_models import EmbeddingModel, VectorDocument

    SERVICES_AVAILABLE = True
except ImportError:
    SERVICES_AVAILABLE = False


@pytest.mark.performance
class TestIntegrationPerformance:
    """Performance tests for integration services."""

    @pytest.fixture(autouse=True)
    def setup_method(self):
        """Setup performance test fixtures."""
        self.messaging_service = ConsolidatedMessagingService(dry_run=True)
        self.vector_service = ConsolidatedVectorService(agent_id="perf-test-agent")
        self.coordination_service = ConsolidatedCoordinationService("perf-coordinator")
        self.process = psutil.Process(os.getpid())

    @pytest.mark.performance
    def test_messaging_service_throughput_performance(self):
        """PERFORMANCE TEST: Messaging service throughput under load."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Measure baseline memory
        baseline_memory = self.process.memory_info().rss / 1024 / 1024  # MB

        # Test high-volume messaging
        start_time = time.time()
        message_count = 1000

        for i in range(message_count):
            self.messaging_service.send_message_pyautogui(
                f"Agent-{i % 8 + 1}", f"Throughput test message {i}"
            )

        end_time = time.time()
        total_time = end_time - start_time

        # Calculate throughput metrics
        messages_per_second = message_count / total_time
        avg_time_per_message = total_time / message_count * 1000  # ms

        # Performance assertions
        assert messages_per_second > 100  # At least 100 messages/second
        assert avg_time_per_message < 10  # Less than 10ms per message

        # Memory usage check
        final_memory = self.process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - baseline_memory
        assert memory_increase < 50  # Less than 50MB increase

        print(".2f")
        print(".2f")
        print(".2f")

    @pytest.mark.performance
    def test_coordination_service_bulk_processing_performance(self):
        """PERFORMANCE TEST: Coordination service bulk processing."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Create large batch of messages
        batch_sizes = [100, 500, 1000]

        for batch_size in batch_sizes:
            # Measure baseline
            baseline_memory = self.process.memory_info().rss / 1024 / 1024
            start_time = time.time()

            # Create batch
            messages = []
            for i in range(batch_size):
                messages.append(
                    UnifiedMessage(
                        content=f"Bulk performance test {i}",
                        sender="Agent-1",
                        recipient="Agent-2",
                        message_type=UnifiedMessageType.AGENT_TO_AGENT,
                        priority=UnifiedMessagePriority.NORMAL,
                    )
                )

            # Process batch
            results = self.coordination_service.process_bulk_messages(messages)
            end_time = time.time()

            # Calculate metrics
            processing_time = end_time - start_time
            messages_per_second = batch_size / processing_time
            final_memory = self.process.memory_info().rss / 1024 / 1024
            memory_increase = final_memory - baseline_memory

            # Performance assertions
            assert len(results) == batch_size
            assert all(result["status"] == "processed" for result in results)
            assert messages_per_second > 50  # At least 50 messages/second
            assert memory_increase < 100  # Less than 100MB increase

            print(
                f"Batch Size {batch_size}: {messages_per_second:.2f} msg/sec, {memory_increase:.2f}MB memory"
            )

    @pytest.mark.performance
    def test_vector_service_embedding_performance(self):
        """PERFORMANCE TEST: Vector service embedding generation performance."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test different batch sizes
        test_batches = [
            ["Short text for embedding"],
            ["This is a medium length text for testing embedding performance and throughput"] * 5,
            [
                "Performance test document with substantial content for benchmarking embedding generation speed and memory usage"
            ]
            * 10,
        ]

        for batch in test_batches:
            baseline_memory = self.process.memory_info().rss / 1024 / 1024
            start_time = time.time()

            with patch(
                "services.consolidated_vector_service.SentenceTransformer"
            ) as mock_transformer:
                mock_encoder = Mock()
                # Create embeddings array matching batch size
                mock_encoder.encode.return_value = [[0.1, 0.2, 0.3] for _ in batch]
                mock_transformer.return_value = mock_encoder

                embeddings = self.vector_service.generate_embeddings(batch)
                end_time = time.time()

            processing_time = end_time - start_time
            final_memory = self.process.memory_info().rss / 1024 / 1024
            memory_increase = final_memory - baseline_memory

            # Performance assertions
            assert len(embeddings) == len(batch)
            assert processing_time < 5.0  # Less than 5 seconds
            assert memory_increase < 200  # Less than 200MB increase

            texts_per_second = len(batch) / processing_time
            print(
                f"Batch Size {len(batch)}: {texts_per_second:.2f} texts/sec, {processing_time:.3f}s, {memory_increase:.2f}MB"
            )

    @pytest.mark.performance
    def test_cross_service_performance_integration(self):
        """PERFORMANCE TEST: Cross-service performance integration."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Measure complete workflow performance
        workflow_iterations = 50

        baseline_memory = self.process.memory_info().rss / 1024 / 1024
        start_time = time.time()

        for i in range(workflow_iterations):
            # Step 1: Messaging
            with patch("services.consolidated_messaging_service.PYAUTOGUI_AVAILABLE", False):
                self.messaging_service.send_message_pyautogui("Agent-2", f"Workflow test {i}")

            # Step 2: Coordination
            coord_message = UnifiedMessage(
                content=f"Coordination workflow {i}",
                sender="Agent-1",
                recipient="coordinator",
                message_type=UnifiedMessageType.COORDINATION,
                priority=UnifiedMessagePriority.NORMAL,
            )
            self.coordination_service.process_message(coord_message)

            # Step 3: Vector storage
            doc = VectorDocument(
                id=f"workflow-doc-{i}",
                content=f"Workflow content {i}",
                metadata={"iteration": i, "workflow": "performance_test"},
            )

            with patch.object(self.vector_service, "_engine", Mock()) as mock_engine:
                mock_engine.store.return_value = Mock(success=True)
                self.vector_service.store_document(doc)

        end_time = time.time()
        total_time = end_time - start_time
        final_memory = self.process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - baseline_memory

        # Performance metrics
        workflows_per_second = workflow_iterations / total_time
        avg_time_per_workflow = total_time / workflow_iterations * 1000  # ms

        # Assertions
        assert workflows_per_second > 10  # At least 10 complete workflows/second
        assert avg_time_per_workflow < 100  # Less than 100ms per workflow
        assert memory_increase < 150  # Less than 150MB total increase

        print(".2f")
        print(".2f")
        print(".2f")

    @pytest.mark.performance
    def test_service_scalability_under_load(self):
        """PERFORMANCE TEST: Service scalability under increasing load."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        load_levels = [10, 50, 100, 200]
        performance_results = []

        for load_level in load_levels:
            # Measure coordination service scalability
            start_time = time.time()

            messages = []
            for i in range(load_level):
                messages.append(
                    UnifiedMessage(
                        content=f"Scalability test {i}",
                        sender="Agent-1",
                        recipient="Agent-2",
                        message_type=UnifiedMessageType.AGENT_TO_AGENT,
                        priority=UnifiedMessagePriority.NORMAL,
                    )
                )

            results = self.coordination_service.process_bulk_messages(messages)
            processing_time = time.time() - start_time

            messages_per_second = load_level / processing_time
            performance_results.append(
                {
                    "load_level": load_level,
                    "processing_time": processing_time,
                    "messages_per_second": messages_per_second,
                    "all_successful": all(r["status"] == "processed" for r in results),
                }
            )

        # Analyze scalability
        for result in performance_results:
            print(
                f"Load {result['load_level']}: {result['messages_per_second']:.2f} msg/sec, {result['processing_time']:.3f}s"
            )

            # Performance should not degrade significantly
            assert result["messages_per_second"] > 10  # Minimum 10 msg/sec
            assert result["all_successful"] is True

        # Check for performance degradation (should be minimal)
        if len(performance_results) >= 2:
            first_throughput = performance_results[0]["messages_per_second"]
            last_throughput = performance_results[-1]["messages_per_second"]
            degradation_percent = (first_throughput - last_throughput) / first_throughput * 100

            # Allow up to 50% degradation under extreme load
            assert degradation_percent < 50

    @pytest.mark.performance
    def test_memory_leak_detection(self):
        """PERFORMANCE TEST: Memory leak detection during extended operation."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Run extended operation to detect memory leaks
        initial_memory = self.process.memory_info().rss / 1024 / 1024
        memory_samples = []

        # Run operations for several minutes (simulated)
        for cycle in range(20):  # 20 cycles of operations
            # Perform various operations
            for i in range(25):
                message = UnifiedMessage(
                    content=f"Memory leak test {cycle}-{i}",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=UnifiedMessageType.AGENT_TO_AGENT,
                    priority=UnifiedMessagePriority.NORMAL,
                )
                self.coordination_service.process_message(message)

            # Sample memory usage
            current_memory = self.process.memory_info().rss / 1024 / 1024
            memory_samples.append(current_memory)

            # Small delay to allow for garbage collection
            time.sleep(0.01)

        final_memory = memory_samples[-1]
        memory_increase = final_memory - initial_memory

        # Calculate memory trend
        memory_trend = statistics.linear_regression(range(len(memory_samples)), memory_samples)
        slope = memory_trend.slope  # Rate of memory increase per cycle

        # Assertions for memory leak detection
        assert memory_increase < 100  # Less than 100MB total increase
        assert slope < 0.1  # Less than 0.1MB increase per cycle (very gradual)

        print(".2f")
        print(".2f")
        print(".6f")

    @pytest.mark.performance
    def test_concurrent_service_operations(self):
        """PERFORMANCE TEST: Concurrent operations across services."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        import threading

        results = {"messaging": [], "coordination": [], "vector": []}
        errors = []

        def messaging_worker():
            """Worker for messaging operations."""
            try:
                for i in range(100):
                    result = self.messaging_service.send_message_pyautogui(
                        "Agent-2", f"Concurrent msg {i}"
                    )
                    results["messaging"].append(result)
            except Exception as e:
                errors.append(f"Messaging error: {e}")

        def coordination_worker():
            """Worker for coordination operations."""
            try:
                for i in range(100):
                    message = UnifiedMessage(
                        content=f"Concurrent coord {i}",
                        sender="Agent-1",
                        recipient="Agent-2",
                        message_type=UnifiedMessageType.AGENT_TO_AGENT,
                        priority=UnifiedMessagePriority.NORMAL,
                    )
                    result = self.coordination_service.process_message(message)
                    results["coordination"].append(result["status"])
            except Exception as e:
                errors.append(f"Coordination error: {e}")

        def vector_worker():
            """Worker for vector operations."""
            try:
                for i in range(50):  # Fewer vector operations as they're more expensive
                    doc = VectorDocument(
                        id=f"concurrent-doc-{i}", content=f"Concurrent content {i}"
                    )
                    with patch.object(self.vector_service, "_engine", Mock()) as mock_engine:
                        mock_engine.store.return_value = Mock(success=True)
                        result = self.vector_service.store_document(doc)
                        results["vector"].append(result.success)
            except Exception as e:
                errors.append(f"Vector error: {e}")

        # Start concurrent operations
        threads = [
            threading.Thread(target=messaging_worker),
            threading.Thread(target=coordination_worker),
            threading.Thread(target=vector_worker),
        ]

        start_time = time.time()
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        end_time = time.time()

        total_time = end_time - start_time

        # Analyze results
        messaging_success_rate = sum(results["messaging"]) / len(results["messaging"]) * 100
        coordination_success_rate = (
            results["coordination"].count("processed") / len(results["coordination"]) * 100
        )
        vector_success_rate = sum(results["vector"]) / len(results["vector"]) * 100

        # Performance assertions
        assert len(errors) == 0  # No errors should occur
        assert messaging_success_rate > 95  # 95%+ success rate
        assert coordination_success_rate > 95
        assert vector_success_rate > 95
        assert total_time < 10  # Should complete within 10 seconds

        print(".2f")
        print(".2f")
        print(".2f")
        print(".2f")

    @pytest.mark.performance
    def test_service_recovery_performance(self):
        """PERFORMANCE TEST: Service recovery performance after failures."""
        if not SERVICES_AVAILABLE:
            pytest.skip("Services not available")

        # Test coordination service recovery
        coordination = ConsolidatedCoordinationService("recovery-perf-test")

        # Normal operation baseline
        normal_times = []
        for i in range(10):
            start = time.time()
            message = UnifiedMessage(
                content=f"Normal operation {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
            )
            coordination.process_message(message)
            normal_times.append(time.time() - start)

        normal_avg = statistics.mean(normal_times)

        # Introduce failures
        with patch.object(
            coordination,
            "determine_coordination_strategy",
            side_effect=Exception("Simulated failure"),
        ):
            failure_times = []
            for i in range(10):
                start = time.time()
                message = UnifiedMessage(
                    content=f"Failure simulation {i}",
                    sender="Agent-1",
                    recipient="Agent-2",
                    message_type=UnifiedMessageType.AGENT_TO_AGENT,
                    priority=UnifiedMessagePriority.NORMAL,
                )
                coordination.process_message(message)
                failure_times.append(time.time() - start)

        # Recovery operation
        recovery_times = []
        for i in range(10):
            start = time.time()
            message = UnifiedMessage(
                content=f"Recovery operation {i}",
                sender="Agent-1",
                recipient="Agent-2",
                message_type=UnifiedMessageType.AGENT_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL,
            )
            coordination.process_message(message)
            recovery_times.append(time.time() - start)

        recovery_avg = statistics.mean(recovery_times)

        # Recovery should not be significantly slower than normal operation
        recovery_overhead = (recovery_avg - normal_avg) / normal_avg * 100
        assert recovery_overhead < 50  # Less than 50% performance degradation

        print(".6f")
        print(".6f")
        print(".2f")


if __name__ == "__main__":
    pytest.main(
        [
            __file__,
            "-v",
            "--cov=src/services",
            "--cov-report=html",
            "--cov-report=term-missing",
            "--tb=short",
            "--durations=10",
            "-k",
            "performance",
        ]
    )
