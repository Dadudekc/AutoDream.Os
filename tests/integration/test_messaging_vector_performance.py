#!/usr/bin/env python3
"""
Messaging-Vector Database Performance Integration Tests - Agent Cellphone V2
===========================================================================

Performance and load testing for messaging system and vector database integration.
Tests scalability, response times, and resource usage under various conditions.

V2 Compliance: Performance testing with proper benchmarking and metrics.

Author: Agent-3 - Infrastructure & DevOps Specialist
License: MIT
"""

import time
from concurrent.futures import ThreadPoolExecutor

# Import components


@pytest.mark.performance
class TestMessagingVectorPerformance:
    """Performance tests for messaging-vector integration."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = Mock()
        self.mock_config.persist_directory = self.temp_dir
        self.mock_config.default_collection = "perf_test"

    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_bulk_message_indexing_performance(self, mock_config_class, mock_vector_db_class):
        """Test performance of bulk message indexing."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Generate bulk messages
        message_count = 100
        messages = []
        for i in range(message_count):
            message = UnifiedMessage(
                content=f"Performance test message {i} with some content to index",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.REGULAR
            )
            messages.append(message)

        # Measure indexing performance
        start_time = time.time()

        for message in messages:
            integration.index_message(message)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance assertions
        assert total_time < 5.0, f"Bulk indexing took {total_time:.2f}s, should be < 5.0s"
        assert mock_vector_db.add_document.call_count == message_count

        # Calculate throughput
        throughput = message_count / total_time
        assert throughput > 15, f"Indexing throughput {throughput:.1f} msg/s too low, should be > 15 msg/s"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_concurrent_message_processing_performance(self, mock_config_class, mock_vector_db_class):
        """Test performance under concurrent message processing."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Generate concurrent messages
        message_count = 50
        messages = []
        for i in range(message_count):
            message = UnifiedMessage(
                content=f"Concurrent message {i}",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}"
            )
            messages.append(message)

        # Test concurrent processing
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = []
            for message in messages:
                future = executor.submit(integration.index_message, message)
                futures.append(future)

            # Wait for all to complete
            results = [future.result() for future in futures]

        end_time = time.time()
        total_time = end_time - start_time

        # Verify all messages were processed
        assert all(results), "Some messages failed to index"
        assert mock_vector_db.add_document.call_count == message_count

        # Performance assertions for concurrent processing
        assert total_time < 3.0, f"Concurrent processing took {total_time:.2f}s, should be < 3.0s"
        throughput = message_count / total_time
        assert throughput > 20, f"Concurrent throughput {throughput:.1f} msg/s too low"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_search_performance_under_load(self, mock_config_class, mock_vector_db_class):
        """Test search performance with large dataset."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db

        # Mock search results
        mock_results = []
        for i in range(25):
            mock_result = Mock()
            mock_result.document.content = f"Search result {i} matching query"
            mock_result.score = 0.9 - (i * 0.02)
            mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test search performance with multiple queries
        search_queries = [
            "architecture discussion",
            "vector database implementation",
            "testing framework integration",
            "performance optimization",
            "agent communication protocol"
        ]

        start_time = time.time()

        for query in search_queries:
            results = integration.search_messages(query, limit=25)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance assertions
        assert total_time < 2.0, f"Multi-query search took {total_time:.2f}s, should be < 2.0s"
        assert mock_vector_db.search.call_count == len(search_queries)

        # Verify search results quality
        for query in search_queries:
            results = integration.search_messages(query, limit=10)
            assert len(results) <= 10, f"Too many results returned for query: {query}"
            assert all(result.score > 0.5 for result in results), "Search results have low relevance scores"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_memory_usage_during_bulk_operations(self, mock_config_class, mock_vector_db_class):
        """Test memory usage patterns during bulk operations."""

        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Get initial memory usage
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Perform bulk operation
        bulk_size = 200
        messages = []
        for i in range(bulk_size):
            message = UnifiedMessage(
                content=f"Bulk memory test message {i} with substantial content " * 5,
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}"
            )
            messages.append(message)

        start_time = time.time()

        for message in messages:
            integration.index_message(message)

        end_time = time.time()

        # Get final memory usage
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Performance assertions
        processing_time = end_time - start_time
        assert processing_time < 10.0, f"Bulk processing took {processing_time:.2f}s, should be < 10.0s"

        # Memory usage should not grow excessively
        assert memory_increase < 50, f"Memory usage increased by {memory_increase:.1f}MB, should be < 50MB"

        throughput = bulk_size / processing_time
        assert throughput > 10, f"Bulk throughput {throughput:.1f} msg/s too low"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_response_time_distribution(self, mock_config_class, mock_vector_db_class):
        """Test response time distribution for various operations."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test indexing response times
        response_times = []
        test_messages = []

        for i in range(50):
            message = UnifiedMessage(
                content=f"Response time test message {i}",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}"
            )
            test_messages.append(message)

        for message in test_messages:
            start = time.time()
            integration.index_message(message)
            end = time.time()
            response_times.append(end - start)

        # Analyze response time distribution
        avg_response_time = sum(response_times) / len(response_times)
        max_response_time = max(response_times)
        min_response_time = min(response_times)

        # Performance assertions
        assert avg_response_time < 0.1, f"Average response time {avg_response_time:.3f}s too high"
        assert max_response_time < 0.5, f"Max response time {max_response_time:.3f}s too high"
        assert min_response_time < 0.05, f"Min response time {min_response_time:.3f}s too low"

        # Check response time consistency (95th percentile should be reasonable)
        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95)
        p95_response_time = sorted_times[p95_index]
        assert p95_response_time < 0.2, f"95th percentile response time {p95_response_time:.3f}s too high"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_scalability_with_increasing_dataset(self, mock_config_class, mock_vector_db_class):
        """Test system scalability as dataset grows."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test with increasing dataset sizes
        dataset_sizes = [10, 50, 100, 200]
        scalability_results = {}

        for size in dataset_sizes:
            # Generate messages for this dataset size
            messages = []
            for i in range(size):
                message = UnifiedMessage(
                    content=f"Scalability test message {i} in dataset of {size}",
                    sender=f"Agent-{i % 8 + 1}",
                    recipient=f"Agent-{(i + 1) % 8 + 1}"
                )
                messages.append(message)

            # Measure indexing time
            start_time = time.time()

            for message in messages:
                integration.index_message(message)

            end_time = time.time()
            total_time = end_time - start_time

            # Calculate metrics
            throughput = size / total_time
            scalability_results[size] = {
                'total_time': total_time,
                'throughput': throughput,
                'efficiency_ratio': throughput / size if size > 0 else 0
            }

        # Analyze scalability
        # Throughput should remain relatively stable or grow as dataset increases
        base_throughput = scalability_results[10]['throughput']

        for size in dataset_sizes[1:]:
            current_throughput = scalability_results[size]['throughput']
            degradation_ratio = current_throughput / base_throughput

            # Allow some degradation but not more than 50%
            assert degradation_ratio > 0.5, f"Throughput degraded too much at size {size}: {degradation_ratio:.2f}"

        # Overall performance should be acceptable
        final_throughput = scalability_results[200]['throughput']
        assert final_throughput > 5, f"Final throughput {final_throughput:.1f} msg/s too low"


@pytest.mark.load
class TestMessagingVectorLoadTesting:
    """Load testing for messaging-vector integration under stress conditions."""

    def setup_method(self):
        """Setup test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.mock_config = Mock()
        self.mock_config.persist_directory = self.temp_dir
        self.mock_config.default_collection = "load_test"

    def teardown_method(self):
        """Cleanup test fixtures."""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_high_frequency_message_burst(self, mock_config_class, mock_vector_db_class):
        """Test system under high-frequency message burst."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Simulate message burst
        burst_size = 1000
        burst_duration = 5  # seconds

        messages = []
        for i in range(burst_size):
            message = UnifiedMessage(
                content=f"Burst message {i}",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}",
                message_type=UnifiedMessageType.TEXT,
                priority=UnifiedMessagePriority.URGENT if i % 10 == 0 else UnifiedMessagePriority.REGULAR
            )
            messages.append(message)

        # Execute burst
        start_time = time.time()

        for message in messages:
            integration.index_message(message)

        end_time = time.time()
        actual_duration = end_time - start_time

        # Load testing assertions
        assert actual_duration < burst_duration * 2, f"Burst processing took {actual_duration:.2f}s, too slow"
        assert mock_vector_db.add_document.call_count == burst_size

        # Calculate burst metrics
        messages_per_second = burst_size / actual_duration
        assert messages_per_second > 50, f"Burst rate {messages_per_second:.1f} msg/s too low"

        # Verify urgent messages were prioritized (mock verification)
        urgent_count = sum(1 for m in messages if m.priority == UnifiedMessagePriority.URGENT)
        assert urgent_count == burst_size // 10  # Every 10th message is urgent

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_mixed_workload_performance(self, mock_config_class, mock_vector_db_class):
        """Test performance under mixed workload (indexing + searching)."""
        # Setup mocks
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Mock search results
        mock_results = []
        for i in range(10):
            mock_result = Mock()
            mock_result.document.content = f"Mixed workload result {i}"
            mock_result.score = 0.8
            mock_results.append(mock_result)

        mock_vector_db.search.return_value = mock_results

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Mixed workload simulation
        operations = []
        message_count = 200
        search_count = 50

        # Add indexing operations
        for i in range(message_count):
            message = UnifiedMessage(
                content=f"Mixed workload message {i}",
                sender=f"Agent-{i % 8 + 1}",
                recipient=f"Agent-{(i + 1) % 8 + 1}"
            )
            operations.append(("index", message))

        # Add search operations
        for i in range(search_count):
            operations.append(("search", f"mixed query {i}"))

        # Execute mixed workload
        start_time = time.time()

        for op_type, op_data in operations:
            if op_type == "index":
                integration.index_message(op_data)
            elif op_type == "search":
                integration.search_messages(op_data, limit=10)

        end_time = time.time()
        total_time = end_time - start_time

        # Performance assertions for mixed workload
        assert total_time < 15.0, f"Mixed workload took {total_time:.2f}s, should be < 15.0s"

        # Verify operation counts
        assert mock_vector_db.add_document.call_count == message_count
        assert mock_vector_db.search.call_count == search_count

        # Calculate combined throughput
        total_operations = message_count + search_count
        combined_throughput = total_operations / total_time
        assert combined_throughput > 15, f"Combined throughput {combined_throughput:.1f} ops/s too low"

    @patch('src.services.vector_messaging_integration.VectorDatabaseService')
    @patch('src.services.vector_messaging_integration.VectorDatabaseConfig')
    def test_resource_contention_simulation(self, mock_config_class, mock_vector_db_class):
        """Test system behavior under resource contention."""
        # Setup mocks with simulated delays
        mock_config_class.return_value = self.mock_config

        mock_vector_db = Mock()
        mock_vector_db_class.return_value = mock_vector_db
        mock_vector_db.add_document.return_value = True

        # Add simulated delay to operations
        original_add = mock_vector_db.add_document

        def delayed_add(*args, **kwargs):
            time.sleep(0.001)  # 1ms delay to simulate I/O
            return original_add(*args, **kwargs)

        mock_vector_db.add_document = delayed_add

        # Create integration service
        integration = VectorMessagingIntegration(self.mock_config)

        # Test under simulated resource contention
        concurrent_operations = 20
        messages_per_operation = 25

        def worker_operation(worker_id):
            """Worker function simulating concurrent operations."""
            worker_messages = []
            for i in range(messages_per_operation):
                message = UnifiedMessage(
                    content=f"Worker {worker_id} message {i}",
                    sender=f"Agent-{worker_id % 8 + 1}",
                    recipient=f"Agent-{(worker_id + 1) % 8 + 1}"
                )
                worker_messages.append(message)

            start_time = time.time()
            for message in worker_messages:
                integration.index_message(message)
            end_time = time.time()

            return {
                'worker_id': worker_id,
                'messages_processed': len(worker_messages),
                'processing_time': end_time - start_time,
                'throughput': len(worker_messages) / (end_time - start_time)
            }

        # Execute concurrent operations
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_operations) as executor:
            futures = []
            for worker_id in range(concurrent_operations):
                future = executor.submit(worker_operation, worker_id)
                futures.append(future)

            # Collect results
            results = [future.result() for future in futures]

        end_time = time.time()
        total_time = end_time - start_time

        # Analyze contention results
        total_messages = sum(r['messages_processed'] for r in results)
        avg_throughput = sum(r['throughput'] for r in results) / len(results)
        max_processing_time = max(r['processing_time'] for r in results)

        # Performance assertions under contention
        assert total_time < 10.0, f"Contention test took {total_time:.2f}s, should be < 10.0s"
        assert max_processing_time < 2.0, f"Max worker time {max_processing_time:.2f}s too high"
        assert avg_throughput > 10, f"Average worker throughput {avg_throughput:.1f} msg/s too low"

        # Verify all messages were processed
        assert mock_vector_db.add_document.call_count == total_messages


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-m", "performance or load"])

