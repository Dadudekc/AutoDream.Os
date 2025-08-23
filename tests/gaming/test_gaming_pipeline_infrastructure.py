#!/usr/bin/env python3
"""
Test Suite for Gaming Pipeline Infrastructure
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- Pipeline data structures and processing
- Data processors and routing
- Storage and retrieval systems
- Pipeline management and metrics
- Cross-platform data flow
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from pathlib import Path
import numpy as np

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.gaming_pipeline_infrastructure import (
    PipelineStage,
    DataType,
    PipelinePriority,
    PipelineStatus,
    PipelineData,
    PipelineMetrics,
    DataProcessor,
    GameStateProcessor,
    EntertainmentContentProcessor,
    DataRouter,
    DataStorage,
    PipelineManager,
    create_pipeline_manager,
)


class TestPipelineEnums(unittest.TestCase):
    """Test pipeline enumeration classes"""

    def test_pipeline_stages(self):
        """Test all pipeline stages exist"""
        stages = [
            PipelineStage.INPUT,
            PipelineStage.PROCESSING,
            PipelineStage.TRANSFORMATION,
            PipelineStage.ROUTING,
            PipelineStage.OUTPUT,
            PipelineStage.STORAGE,
            PipelineStage.SYNC,
        ]

        for stage in stages:
            self.assertIsInstance(stage.value, str)
            self.assertTrue(len(stage.value) > 0)

    def test_data_types(self):
        """Test all data types exist"""
        data_types = [
            DataType.GAME_STATE,
            DataType.PLAYER_ACTION,
            DataType.AI_DECISION,
            DataType.PERFORMANCE_METRICS,
            DataType.ENTERTAINMENT_CONTENT,
            DataType.USER_ENGAGEMENT,
            DataType.SYSTEM_EVENT,
            DataType.ANALYTICS_DATA,
        ]

        for data_type in data_types:
            self.assertIsInstance(data_type.value, str)
            self.assertTrue(len(data_type.value) > 0)

    def test_pipeline_priorities(self):
        """Test all pipeline priorities exist"""
        priorities = [
            PipelinePriority.CRITICAL,
            PipelinePriority.HIGH,
            PipelinePriority.NORMAL,
            PipelinePriority.LOW,
            PipelinePriority.BACKGROUND,
        ]

        for priority in priorities:
            self.assertIsInstance(priority.value, int)
            self.assertGreaterEqual(priority.value, 0)

    def test_pipeline_status(self):
        """Test all pipeline statuses exist"""
        statuses = [
            PipelineStatus.IDLE,
            PipelineStatus.RUNNING,
            PipelineStatus.PAUSED,
            PipelineStatus.ERROR,
            PipelineStatus.SHUTDOWN,
        ]

        for status in statuses:
            self.assertIsInstance(status.value, str)
            self.assertTrue(len(status.value) > 0)


class TestPipelineData(unittest.TestCase):
    """Test PipelineData dataclass"""

    def test_pipeline_data_creation(self):
        """Test pipeline data creation"""
        data = PipelineData(
            data_id="test_data_123",
            data_type=DataType.GAME_STATE,
            source="game_engine",
            destination="analytics",
            payload={"player_health": 100, "level": 5},
            priority=PipelinePriority.HIGH,
        )

        self.assertEqual(data.data_id, "test_data_123")
        self.assertEqual(data.data_type, DataType.GAME_STATE)
        self.assertEqual(data.source, "game_engine")
        self.assertEqual(data.destination, "analytics")
        self.assertEqual(data.payload["player_health"], 100)
        self.assertEqual(data.priority, PipelinePriority.HIGH)
        self.assertEqual(data.processing_stage, PipelineStage.INPUT)
        self.assertIsNotNone(data.checksum)
        self.assertIsNotNone(data.timestamp)

    def test_pipeline_data_checksum_calculation(self):
        """Test checksum calculation"""
        data1 = PipelineData(
            data_id="test1",
            data_type=DataType.GAME_STATE,
            source="source1",
            destination="dest1",
            payload={"test": "data"},
        )

        data2 = PipelineData(
            data_id="test2",
            data_type=DataType.GAME_STATE,
            source="source1",
            destination="dest1",
            payload={"test": "data"},
        )

        # Different IDs should have different checksums
        self.assertNotEqual(data1.checksum, data2.checksum)

        # Add a small delay to ensure different timestamps
        import time

        time.sleep(0.001)  # 1 millisecond delay

        # Different timestamps should result in different checksums even for same data
        data3 = PipelineData(
            data_id="test1",
            data_type=DataType.GAME_STATE,
            source="source1",
            destination="dest1",
            payload={"test": "data"},
        )
        # Since timestamps are different, checksums should be different
        self.assertNotEqual(data1.checksum, data3.checksum)

        # Test that checksums are consistent for the same object
        self.assertEqual(data1.checksum, data1.checksum)

        # Test that checksums are deterministic (same object, same checksum)
        checksum1 = data1._calculate_checksum()
        checksum2 = data1._calculate_checksum()
        self.assertEqual(checksum1, checksum2)

    def test_pipeline_data_serialization(self):
        """Test pipeline data serialization"""
        data = PipelineData(
            data_id="test_serialization",
            data_type=DataType.ENTERTAINMENT_CONTENT,
            source="content_engine",
            destination="recommendation_engine",
            payload={"title": "Test Content", "category": "gaming"},
            priority=PipelinePriority.NORMAL,
        )

        data_dict = data.to_dict()

        self.assertIsInstance(data_dict, dict)
        self.assertEqual(data_dict["data_id"], "test_serialization")
        self.assertEqual(data_dict["data_type"], "entertainment_content")
        self.assertEqual(data_dict["source"], "content_engine")
        self.assertEqual(data_dict["priority"], 2)  # NORMAL priority value

    def test_pipeline_data_deserialization(self):
        """Test pipeline data deserialization"""
        original_data = PipelineData(
            data_id="test_deserialization",
            data_type=DataType.PERFORMANCE_METRICS,
            source="metrics_collector",
            destination="dashboard",
            payload={"fps": 60, "latency": 16.67},
            priority=PipelinePriority.CRITICAL,
        )

        data_dict = original_data.to_dict()
        reconstructed_data = PipelineData.from_dict(data_dict)

        self.assertEqual(original_data.data_id, reconstructed_data.data_id)
        self.assertEqual(original_data.data_type, reconstructed_data.data_type)
        self.assertEqual(original_data.source, reconstructed_data.source)
        self.assertEqual(original_data.destination, reconstructed_data.destination)
        self.assertEqual(original_data.payload, reconstructed_data.payload)
        self.assertEqual(original_data.priority, reconstructed_data.priority)


class TestPipelineMetrics(unittest.TestCase):
    """Test PipelineMetrics dataclass"""

    def test_pipeline_metrics_initialization(self):
        """Test pipeline metrics initialization"""
        metrics = PipelineMetrics()

        self.assertEqual(metrics.total_processed, 0)
        self.assertEqual(metrics.successful_processed, 0)
        self.assertEqual(metrics.failed_processed, 0)
        self.assertEqual(metrics.average_processing_time, 0.0)
        self.assertEqual(metrics.throughput_per_second, 0.0)
        self.assertEqual(metrics.error_rate, 0.0)
        self.assertIsNone(metrics.last_processed_time)
        self.assertIsInstance(metrics.stage_metrics, dict)

    def test_pipeline_metrics_update_success(self):
        """Test metrics update with successful processing"""
        metrics = PipelineMetrics()

        # First update
        metrics.update_metrics(0.5, True)

        self.assertEqual(metrics.total_processed, 1)
        self.assertEqual(metrics.successful_processed, 1)
        self.assertEqual(metrics.failed_processed, 0)
        self.assertEqual(metrics.average_processing_time, 0.5)
        self.assertEqual(metrics.error_rate, 0.0)
        self.assertIsNotNone(metrics.last_processed_time)

        # Second update
        metrics.update_metrics(1.5, True)

        self.assertEqual(metrics.total_processed, 2)
        self.assertEqual(metrics.successful_processed, 2)
        self.assertEqual(metrics.failed_processed, 0)
        self.assertEqual(metrics.average_processing_time, 1.0)  # (0.5 + 1.5) / 2
        self.assertEqual(metrics.error_rate, 0.0)

    def test_pipeline_metrics_update_failure(self):
        """Test metrics update with failed processing"""
        metrics = PipelineMetrics()

        # Success then failure
        metrics.update_metrics(0.5, True)
        metrics.update_metrics(1.0, False)

        self.assertEqual(metrics.total_processed, 2)
        self.assertEqual(metrics.successful_processed, 1)
        self.assertEqual(metrics.failed_processed, 1)
        self.assertEqual(metrics.average_processing_time, 0.75)  # (0.5 + 1.0) / 2
        self.assertEqual(metrics.error_rate, 0.5)  # 1/2


class TestDataProcessor(unittest.TestCase):
    """Test DataProcessor abstract base class"""

    def test_data_processor_initialization(self):
        """Test data processor initialization"""

        # Create a concrete implementation for testing
        class TestProcessor(DataProcessor):
            async def process(self, data):
                return data

        processor = TestProcessor("TestProcessor", "test_type")

        self.assertEqual(processor.name, "TestProcessor")
        self.assertEqual(processor.processor_type, "test_type")
        self.assertFalse(processor.is_active)
        self.assertIsInstance(processor.processing_stats, dict)
        self.assertEqual(processor.processing_stats["total_processed"], 0)

    def test_data_processor_start_stop(self):
        """Test processor start and stop"""

        class TestProcessor(DataProcessor):
            async def process(self, data):
                return data

        processor = TestProcessor("TestProcessor", "test_type")

        self.assertFalse(processor.is_active)

        processor.start()
        self.assertTrue(processor.is_active)

        processor.stop()
        self.assertFalse(processor.is_active)

    def test_data_processor_stats_update(self):
        """Test processor statistics update"""

        class TestProcessor(DataProcessor):
            async def process(self, data):
                return data

        processor = TestProcessor("TestProcessor", "test_type")

        # Update stats
        processor.update_stats(True)
        self.assertEqual(processor.processing_stats["total_processed"], 1)
        self.assertEqual(processor.processing_stats["successful"], 1)
        self.assertEqual(processor.processing_stats["failed"], 0)

        processor.update_stats(False)
        self.assertEqual(processor.processing_stats["total_processed"], 2)
        self.assertEqual(processor.processing_stats["successful"], 1)
        self.assertEqual(processor.processing_stats["failed"], 1)


class TestGameStateProcessor(unittest.TestCase):
    """Test GameStateProcessor"""

    def test_game_state_processor_initialization(self):
        """Test game state processor initialization"""
        processor = GameStateProcessor()

        self.assertEqual(processor.name, "GameStateProcessor")
        self.assertEqual(processor.processor_type, "game_state")
        self.assertIsInstance(processor.state_cache, dict)
        self.assertIsInstance(processor.change_detectors, dict)

    @patch("asyncio.create_task")
    async def test_game_state_processor_process_success(self, mock_create_task):
        """Test successful game state processing"""
        processor = GameStateProcessor()

        # Create test data
        test_data = PipelineData(
            data_id="test_game_state",
            data_type=DataType.GAME_STATE,
            source="test_game",
            destination="analytics",
            payload={"player_health": 100, "level": 5},
        )

        # Process data
        result = await processor.process(test_data)

        self.assertEqual(result.processing_stage, PipelineStage.PROCESSING)
        self.assertIn("changes_detected", result.metadata)
        self.assertIn("state_hash", result.metadata)
        self.assertEqual(result.metadata["changes_detected"], ["initial_state"])
        self.assertIsNotNone(result.metadata["state_hash"])

    @patch("asyncio.create_task")
    async def test_game_state_processor_process_wrong_type(self, mock_create_task):
        """Test processing wrong data type"""
        processor = GameStateProcessor()

        # Create wrong data type
        wrong_data = PipelineData(
            data_id="test_wrong_type",
            data_type=DataType.ENTERTAINMENT_CONTENT,
            source="test_source",
            destination="test_dest",
            payload={"test": "data"},
        )

        # Process data (should fail)
        result = await processor.process(wrong_data)

        self.assertEqual(result.processing_stage, PipelineStage.ERROR)
        self.assertIn("error", result.metadata)
        self.assertIn("Expected GAME_STATE data", result.metadata["error"])

    def test_game_state_change_detection(self):
        """Test game state change detection"""
        processor = GameStateProcessor()

        # First state - manually update cache to simulate processing
        state1 = {"player_health": 100, "level": 5}
        processor.state_cache["test_game"] = state1

        # Same state (no changes)
        changes1 = processor._detect_changes("test_game", state1)
        self.assertEqual(changes1, [])

        # Different state (changes detected)
        state2 = {"player_health": 80, "level": 6}
        changes2 = processor._detect_changes("test_game", state2)
        self.assertIn("changed_player_health", changes2)
        self.assertIn("changed_level", changes2)

        # Test initial state detection
        processor.state_cache.clear()
        changes3 = processor._detect_changes("new_game", state1)
        self.assertEqual(changes3, ["initial_state"])

    def test_game_state_hashing(self):
        """Test game state hashing"""
        processor = GameStateProcessor()

        state1 = {"player_health": 100, "level": 5}
        hash1 = processor._hash_state(state1)

        # Same state should have same hash
        hash2 = processor._hash_state(state1)
        self.assertEqual(hash1, hash2)

        # Different state should have different hash
        state2 = {"player_health": 80, "level": 5}
        hash3 = processor._hash_state(state2)
        self.assertNotEqual(hash1, hash3)


class TestEntertainmentContentProcessor(unittest.TestCase):
    """Test EntertainmentContentProcessor"""

    def test_entertainment_processor_initialization(self):
        """Test entertainment processor initialization"""
        processor = EntertainmentContentProcessor()

        self.assertEqual(processor.name, "EntertainmentContentProcessor")
        self.assertEqual(processor.processor_type, "entertainment")
        self.assertIsInstance(processor.content_cache, dict)
        self.assertIsInstance(processor.user_preferences, dict)

    @patch("asyncio.create_task")
    async def test_entertainment_processor_process_success(self, mock_create_task):
        """Test successful entertainment content processing"""
        processor = EntertainmentContentProcessor()

        # Create test data
        test_data = PipelineData(
            data_id="test_entertainment",
            data_type=DataType.ENTERTAINMENT_CONTENT,
            source="content_engine",
            destination="recommendation_engine",
            payload={
                "id": "content_123",
                "title": "Gaming Tutorial",
                "tags": ["gaming", "tutorial", "fun"],
            },
        )

        # Process data
        result = await processor.process(test_data)

        self.assertEqual(result.processing_stage, PipelineStage.PROCESSING)
        self.assertIn("processed_content", result.metadata)
        self.assertIn("content_id", result.metadata)

        processed_content = result.metadata["processed_content"]
        self.assertEqual(processed_content["content_type"], "gaming")
        self.assertIn("engagement_score", processed_content)
        self.assertIn("processed_at", processed_content)

    @patch("asyncio.create_task")
    async def test_entertainment_processor_process_wrong_type(self, mock_create_task):
        """Test processing wrong data type"""
        processor = EntertainmentContentProcessor()

        # Create wrong data type
        wrong_data = PipelineData(
            data_id="test_wrong_type",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload={"test": "data"},
        )

        # Process data (should fail)
        result = await processor.process(wrong_data)

        self.assertEqual(result.processing_stage, PipelineStage.ERROR)
        self.assertIn("error", result.metadata)
        self.assertIn("Expected ENTERTAINMENT_CONTENT data", result.metadata["error"])

    def test_content_classification(self):
        """Test content classification"""
        processor = EntertainmentContentProcessor()

        # Test gaming content
        gaming_title = "How to Play Minecraft"
        gaming_type = processor._classify_content(gaming_title)
        self.assertEqual(gaming_type, "gaming")

        # Test video content
        video_title = "Amazing Movie Trailer"
        video_type = processor._classify_content(video_title)
        self.assertEqual(video_type, "video")

        # Test music content
        music_title = "Best Song Ever"
        music_type = processor._classify_content(music_title)
        self.assertEqual(music_type, "audio")

        # Test news content
        news_title = "Breaking News Article"
        news_type = processor._classify_content(news_title)
        self.assertEqual(news_type, "news")

        # Test unknown content
        unknown_title = "Random Text"
        unknown_type = processor._classify_content(unknown_title)
        self.assertEqual(unknown_type, "general")

    def test_engagement_score_calculation(self):
        """Test engagement score calculation"""
        processor = EntertainmentContentProcessor()

        # Test with gaming tags
        gaming_tags = ["gaming", "esports", "streaming"]
        score1 = processor._calculate_engagement_score(gaming_tags)
        self.assertGreater(score1, 0.5)  # Should be higher than base score

        # Test with entertainment tags
        entertainment_tags = ["fun", "entertainment", "comedy"]
        score2 = processor._calculate_engagement_score(entertainment_tags)
        self.assertGreater(score2, 0.5)

        # Test with mixed tags
        mixed_tags = ["gaming", "fun", "action"]
        score3 = processor._calculate_engagement_score(mixed_tags)
        self.assertGreater(score3, 0.5)

        # Test with no special tags
        no_special_tags = ["random", "generic", "content"]
        score4 = processor._calculate_engagement_score(no_special_tags)
        self.assertEqual(score4, 0.5)  # Should be base score

        # Test score cap
        many_tags = ["gaming", "gaming", "gaming", "gaming", "gaming"]
        score5 = processor._calculate_engagement_score(many_tags)
        self.assertEqual(score5, 1.0)  # Should be capped at 1.0


class TestDataRouter(unittest.TestCase):
    """Test DataRouter"""

    def test_data_router_initialization(self):
        """Test data router initialization"""
        router = DataRouter()

        self.assertEqual(router.name, "DataRouter")
        self.assertEqual(router.processor_type, "routing")
        self.assertIsInstance(router.routing_rules, dict)
        self.assertIsInstance(router.destination_processors, dict)
        self.assertTrue(router.load_balancing)

    @patch("asyncio.create_task")
    async def test_data_router_process_success(self, mock_create_task):
        """Test successful data routing"""
        router = DataRouter()

        # Create test data
        test_data = PipelineData(
            data_id="test_routing",
            data_type=DataType.GAME_STATE,
            source="game_engine",
            destination="analytics",
            payload={"test": "data"},
        )

        # Process data
        result = await router.process(test_data)

        self.assertEqual(result.processing_stage, PipelineStage.ROUTING)
        self.assertIn("routed_destinations", result.metadata)

        # Should have default destinations for game state
        destinations = result.metadata["routed_destinations"]
        self.assertIn("analytics", destinations)
        self.assertIn("ai_engine", destinations)
        self.assertIn("storage", destinations)

    def test_routing_rules(self):
        """Test routing rules"""
        router = DataRouter()

        # Add a routing rule
        rule_conditions = [
            {"type": "data_type", "value": "game_state"},
            {"type": "priority", "value": 1},
        ]
        rule_destinations = ["high_priority_processor", "storage"]

        router.add_routing_rule(
            "high_priority_gaming", rule_conditions, rule_destinations
        )

        self.assertIn("high_priority_gaming", router.routing_rules)
        rule = router.routing_rules["high_priority_gaming"]
        self.assertEqual(rule["conditions"], rule_conditions)
        self.assertEqual(rule["destinations"], rule_destinations)

    def test_rule_matching(self):
        """Test routing rule matching"""
        router = DataRouter()

        # Add a simple rule
        router.add_routing_rule(
            "test_rule",
            [{"type": "data_type", "value": "game_state"}],
            ["test_destination"],
        )

        # Create test data
        test_data = PipelineData(
            data_id="test_rule_matching",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload={"test": "data"},
        )

        # Test rule matching
        destinations = router._determine_destinations(test_data)
        self.assertIn("test_destination", destinations)

    def test_default_destinations(self):
        """Test default destination routing"""
        router = DataRouter()

        # Test game state routing
        game_state_destinations = router._get_default_destinations(DataType.GAME_STATE)
        self.assertIn("analytics", game_state_destinations)
        self.assertIn("ai_engine", game_state_destinations)
        self.assertIn("storage", game_state_destinations)

        # Test entertainment content routing
        entertainment_destinations = router._get_default_destinations(
            DataType.ENTERTAINMENT_CONTENT
        )
        self.assertIn("content_engine", entertainment_destinations)
        self.assertIn("recommendation_engine", entertainment_destinations)
        self.assertIn("storage", entertainment_destinations)

        # Test unknown data type
        unknown_destinations = router._get_default_destinations(DataType.SYSTEM_EVENT)
        self.assertEqual(unknown_destinations, ["storage"])

    def test_load_balancing(self):
        """Test load balancing"""
        router = DataRouter()

        destinations = ["dest1", "dest2", "dest3"]

        # Test load balancing
        balanced1 = router._apply_load_balancing(destinations)
        balanced2 = router._apply_load_balancing(destinations)

        # Should have same destinations but potentially different order
        self.assertEqual(set(balanced1), set(destinations))
        self.assertEqual(set(balanced2), set(destinations))
        self.assertEqual(len(balanced1), len(destinations))
        self.assertEqual(len(balanced2), len(destinations))


class TestDataStorage(unittest.TestCase):
    """Test DataStorage"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.storage = DataStorage(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_data_storage_initialization(self):
        """Test data storage initialization"""
        self.assertEqual(self.storage.name, "DataStorage")
        self.assertEqual(self.storage.processor_type, "storage")
        self.assertEqual(self.storage.storage_path, Path(self.temp_dir))
        self.assertIsInstance(self.storage.db_path, Path)

    @patch("asyncio.create_task")
    async def test_data_storage_process_success(self, mock_create_task):
        """Test successful data storage"""
        # Create test data
        test_data = PipelineData(
            data_id="test_storage",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload={"test": "data"},
        )

        # Process data
        result = await self.storage.process(test_data)

        self.assertEqual(result.processing_stage, PipelineStage.STORAGE)
        self.assertIn("stored", result.metadata)
        self.assertTrue(result.metadata["stored"])
        self.assertIn("storage_path", result.metadata)

    def test_file_storage_decision(self):
        """Test file storage decision logic"""
        # Test with numpy array (should store in file)
        numpy_payload = np.zeros((100, 100, 3))
        numpy_data = PipelineData(
            data_id="test_numpy",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload=numpy_payload,
        )
        self.assertTrue(self.storage._should_store_in_file(numpy_data))

        # Test with large string (should store in file)
        large_string = "x" * (1024 * 1024 + 1)  # > 1MB
        large_data = PipelineData(
            data_id="test_large",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload=large_string,
        )
        self.assertTrue(self.storage._should_store_in_file(large_data))

        # Test with small data (should not store in file)
        small_data = PipelineData(
            data_id="test_small",
            data_type=DataType.GAME_STATE,
            source="test_source",
            destination="test_dest",
            payload={"small": "data"},
        )
        self.assertFalse(self.storage._should_store_in_file(small_data))


class TestPipelineManager(unittest.TestCase):
    """Test PipelineManager"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.config = {"storage_path": self.temp_dir}
        self.pipeline = PipelineManager(self.config)

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_pipeline_manager_initialization(self):
        """Test pipeline manager initialization"""
        self.assertEqual(self.pipeline.status, PipelineStatus.IDLE)
        self.assertIsInstance(self.pipeline.processors, dict)
        self.assertFalse(self.pipeline.running)
        self.assertIsInstance(self.pipeline.metrics, PipelineMetrics)

    def test_processors_initialization(self):
        """Test processors initialization"""
        expected_processors = ["game_state", "entertainment", "router", "storage"]

        for processor_name in expected_processors:
            self.assertIn(processor_name, self.pipeline.processors)
            processor = self.pipeline.processors[processor_name]
            self.assertIsInstance(processor, DataProcessor)

    def test_routing_rules_initialization(self):
        """Test routing rules initialization"""
        router = self.pipeline.processors["router"]

        # Check that default rules were added
        self.assertIn("gaming_data", router.routing_rules)
        self.assertIn("entertainment_content", router.routing_rules)
        self.assertIn("high_priority", router.routing_rules)

    @patch("asyncio.create_task")
    async def test_pipeline_start_stop(self, mock_create_task):
        """Test pipeline start and stop"""
        # Mock the create_task to return a mock task
        mock_task = AsyncMock()
        mock_create_task.return_value = mock_task

        # Start pipeline
        await self.pipeline.start()

        self.assertTrue(self.pipeline.running)
        self.assertEqual(self.pipeline.status, PipelineStatus.RUNNING)

        # Check that processors were started
        for processor in self.pipeline.processors.values():
            self.assertTrue(processor.is_active)

        # Stop pipeline
        await self.pipeline.stop()

        self.assertFalse(self.pipeline.running)
        self.assertEqual(self.pipeline.status, PipelineStatus.IDLE)

        # Check that processors were stopped
        for processor in self.pipeline.processors.values():
            self.assertFalse(processor.is_active)

    def test_pipeline_metrics(self):
        """Test pipeline metrics retrieval"""
        metrics = self.pipeline.get_metrics()

        self.assertIsInstance(metrics, dict)
        self.assertIn("status", metrics)
        self.assertIn("running", metrics)
        self.assertIn("total_processed", metrics)
        self.assertIn("successful_processed", metrics)
        self.assertIn("failed_processed", metrics)
        self.assertIn("processor_stats", metrics)

        # Check processor stats
        processor_stats = metrics["processor_stats"]
        for processor_name in ["game_state", "entertainment", "router", "storage"]:
            self.assertIn(processor_name, processor_stats)


class TestCreatePipelineManager(unittest.TestCase):
    """Test factory function"""

    def test_create_pipeline_manager_default(self):
        """Test creating pipeline manager with default config"""
        pipeline = create_pipeline_manager()

        self.assertIsInstance(pipeline, PipelineManager)
        self.assertEqual(pipeline.config, {})

    def test_create_pipeline_manager_custom(self):
        """Test creating pipeline manager with custom config"""
        config = {
            "storage_path": "/custom/path",
            "max_queue_size": 2000,
            "custom_setting": "test",
        }

        pipeline = create_pipeline_manager(config)

        self.assertIsInstance(pipeline, PipelineManager)
        self.assertEqual(pipeline.config, config)


def run_pipeline_infrastructure_tests():
    """Run all gaming pipeline infrastructure tests"""
    print("🔧 Running Gaming Pipeline Infrastructure Tests...")
    print("=" * 70)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestPipelineEnums,
        TestPipelineData,
        TestPipelineMetrics,
        TestDataProcessor,
        TestGameStateProcessor,
        TestEntertainmentContentProcessor,
        TestDataRouter,
        TestDataStorage,
        TestPipelineManager,
        TestCreatePipelineManager,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 GAMING PIPELINE INFRASTRUCTURE TEST RESULTS:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"⚠️ Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if result.wasSuccessful():
        print("\n🎉 ALL GAMING PIPELINE INFRASTRUCTURE TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME GAMING PIPELINE INFRASTRUCTURE TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_pipeline_infrastructure_tests()
    sys.exit(0 if success else 1)
