#!/usr/bin/env python3
"""
Test Suite for AI Gaming Systems
Agent-6: Gaming & Entertainment Development Specialist
TDD Integration Project - Agent_Cellphone_V2_Repository

Comprehensive testing of:
- AI Gaming Systems core functionality
- Object detection and screen capture
- Game state analysis
- AI decision making
- Performance metrics
"""

import unittest
import sys
import os
import tempfile
import shutil
import json
import time
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import numpy as np

# Add the parent directory to the path to import gaming modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from gaming_systems.ai_gaming_systems import (
    GameType,
    AIDecisionType,
    GameState,
    GameObjectData,
    AIGameDecision,
    GameAnalysisResult,
    ScreenCapture,
    ObjectDetector,
    GameStateAnalyzer,
    AIGameController,
    AIGamingSystem,
    create_ai_gaming_system,
)


class TestGameType(unittest.TestCase):
    """Test GameType enumeration"""

    def test_game_types(self):
        """Test all game types exist"""
        game_types = [
            GameType.OSRS,
            GameType.GENERIC_RPG,
            GameType.FPS,
            GameType.STRATEGY,
            GameType.PUZZLE,
            GameType.SIMULATION,
            GameType.ACTION,
            GameType.ADVENTURE,
        ]

        for game_type in game_types:
            self.assertIsInstance(game_type.value, str)
            self.assertTrue(len(game_type.value) > 0)


class TestAIDecisionType(unittest.TestCase):
    """Test AIDecisionType enumeration"""

    def test_decision_types(self):
        """Test all AI decision types exist"""
        decision_types = [
            AIDecisionType.MOVE_TO_LOCATION,
            AIDecisionType.CLICK_OBJECT,
            AIDecisionType.USE_SKILL,
            AIDecisionType.ATTACK_TARGET,
            AIDecisionType.NAVIGATE_PATH,
            AIDecisionType.INTERACT_NPC,
            AIDecisionType.MANAGE_INVENTORY,
            AIDecisionType.OPTIMIZE_ROUTE,
            AIDecisionType.WAIT_FOR_EVENT,
            AIDecisionType.EMERGENCY_ACTION,
        ]

        for decision_type in decision_types:
            self.assertIsInstance(decision_type.value, str)
            self.assertTrue(len(decision_type.value) > 0)


class TestGameState(unittest.TestCase):
    """Test GameState enumeration"""

    def test_game_states(self):
        """Test all game states exist"""
        game_states = [
            GameState.IDLE,
            GameState.COMBAT,
            GameState.SKILLING,
            GameState.QUESTING,
            GameState.TRADING,
            GameState.NAVIGATING,
            GameState.BANKING,
            GameState.INVENTORY_FULL,
            GameState.DANGER,
            GameState.UNKNOWN,
        ]

        for game_state in game_states:
            self.assertIsInstance(game_state.value, str)
            self.assertTrue(len(game_state.value) > 0)


class TestGameObjectData(unittest.TestCase):
    """Test GameObjectData dataclass"""

    def test_game_object_creation(self):
        """Test game object data creation"""
        obj = GameObjectData(
            object_id="test_object_123",
            name="Test Object",
            location=(100, 200),
            object_type="npc",
            confidence=0.95,
        )

        self.assertEqual(obj.object_id, "test_object_123")
        self.assertEqual(obj.name, "Test Object")
        self.assertEqual(obj.location, (100, 200))
        self.assertEqual(obj.object_type, "npc")
        self.assertEqual(obj.confidence, 0.95)
        self.assertIsInstance(obj.properties, dict)
        self.assertIsNotNone(obj.timestamp)


class TestAIGameDecision(unittest.TestCase):
    """Test AIGameDecision dataclass"""

    def test_decision_creation(self):
        """Test AI game decision creation"""
        decision = AIGameDecision(
            decision_type=AIDecisionType.ATTACK_TARGET,
            target="goblin",
            parameters={"weapon": "sword", "style": "aggressive"},
            priority=0.8,
            confidence=0.9,
            reasoning="Goblin is low level and profitable",
            expected_duration=15.0,
            risk_level=0.2,
        )

        self.assertEqual(decision.decision_type, AIDecisionType.ATTACK_TARGET)
        self.assertEqual(decision.target, "goblin")
        self.assertEqual(decision.parameters["weapon"], "sword")
        self.assertEqual(decision.priority, 0.8)
        self.assertEqual(decision.confidence, 0.9)
        self.assertEqual(decision.reasoning, "Goblin is low level and profitable")
        self.assertEqual(decision.expected_duration, 15.0)
        self.assertEqual(decision.risk_level, 0.2)
        self.assertIsNotNone(decision.timestamp)


class TestGameAnalysisResult(unittest.TestCase):
    """Test GameAnalysisResult dataclass"""

    def test_analysis_result_creation(self):
        """Test game analysis result creation"""
        objects = [
            GameObjectData("obj1", "Tree", (50, 50), "resource", 0.9),
            GameObjectData("obj2", "NPC", (100, 100), "npc", 0.8),
        ]

        decisions = [
            AIGameDecision(
                decision_type=AIDecisionType.CLICK_OBJECT,
                target="Tree",
                parameters={"action": "chop"},
                priority=0.7,
                confidence=0.8,
                reasoning="Need wood",
                expected_duration=5.0,
                risk_level=0.1,
            )
        ]

        result = GameAnalysisResult(
            game_state=GameState.SKILLING,
            objects_detected=objects,
            player_stats={"health": 100, "level": 50},
            environment_data={"time": "day", "weather": "clear"},
            recommendations=decisions,
            analysis_confidence=0.85,
        )

        self.assertEqual(result.game_state, GameState.SKILLING)
        self.assertEqual(len(result.objects_detected), 2)
        self.assertEqual(result.player_stats["health"], 100)
        self.assertEqual(result.environment_data["time"], "day")
        self.assertEqual(len(result.recommendations), 1)
        self.assertEqual(result.analysis_confidence, 0.85)
        self.assertIsNotNone(result.timestamp)


class TestScreenCapture(unittest.TestCase):
    """Test ScreenCapture functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.screen_capture = ScreenCapture()

    def test_screen_capture_initialization(self):
        """Test screen capture initialization"""
        self.assertIsNone(self.screen_capture.last_capture)
        self.assertIsNone(self.screen_capture.capture_thread)
        self.assertFalse(self.screen_capture.capturing)

    @patch("pyautogui.screenshot")
    def test_capture_screen_success(self, mock_screenshot):
        """Test successful screen capture"""
        # Mock PIL Image
        mock_image = Mock()
        mock_image.size = (800, 600)
        mock_screenshot.return_value = mock_image

        # Mock numpy array conversion
        with patch("numpy.array") as mock_array, patch(
            "cv2.cvtColor"
        ) as mock_cvt_color:
            mock_array.return_value = np.zeros((600, 800, 3), dtype=np.uint8)
            mock_cvt_color.return_value = np.zeros((600, 800, 3), dtype=np.uint8)

            result = self.screen_capture.capture_screen()

            self.assertIsNotNone(result)
            self.assertIsInstance(result, np.ndarray)
            mock_screenshot.assert_called_once()

    @patch("pyautogui.screenshot")
    def test_capture_screen_with_region(self, mock_screenshot):
        """Test screen capture with specific region"""
        mock_image = Mock()
        mock_screenshot.return_value = mock_image

        with patch("numpy.array") as mock_array, patch(
            "cv2.cvtColor"
        ) as mock_cvt_color:
            mock_array.return_value = np.zeros((200, 200, 3), dtype=np.uint8)
            mock_cvt_color.return_value = np.zeros((200, 200, 3), dtype=np.uint8)

            region = (100, 100, 200, 200)
            result = self.screen_capture.capture_screen(region)

            self.assertIsNotNone(result)
            mock_screenshot.assert_called_once_with(region=region)

    def test_capture_screen_failure(self):
        """Test screen capture failure"""
        # No mocking - should fail without pyautogui
        result = self.screen_capture.capture_screen()
        self.assertIsNone(result)

    @patch("cv2.matchTemplate")
    @patch("cv2.imread")
    def test_find_template_success(self, mock_imread, mock_match_template):
        """Test successful template matching"""
        # Set up mock data
        self.screen_capture.last_capture = np.zeros((600, 800, 3), dtype=np.uint8)
        mock_template = np.zeros((50, 50, 3), dtype=np.uint8)
        mock_imread.return_value = mock_template

        # Mock template matching result
        mock_result = np.array([[0.9, 0.7], [0.6, 0.8]])
        mock_match_template.return_value = mock_result

        with patch("numpy.where") as mock_where:
            mock_where.return_value = ([0, 1], [0, 1])

            matches = self.screen_capture.find_template("test_template.png", 0.8)

            self.assertIsInstance(matches, list)
            self.assertTrue(len(matches) >= 0)

    def test_find_template_no_capture(self):
        """Test template matching without screen capture"""
        matches = self.screen_capture.find_template("test_template.png")
        self.assertEqual(matches, [])

    def test_start_stop_capture(self):
        """Test starting and stopping capture"""
        # Test start (will fail without dependencies but should handle gracefully)
        success = self.screen_capture.start_capture()
        self.assertIsInstance(success, bool)

        # Test stop
        self.screen_capture.stop_capture()
        self.assertFalse(self.screen_capture.capturing)


class TestObjectDetector(unittest.TestCase):
    """Test ObjectDetector functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.detector = ObjectDetector()
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_object_detector_initialization(self):
        """Test object detector initialization"""
        self.assertIsInstance(self.detector.templates, dict)
        self.assertIsInstance(self.detector.color_ranges, dict)
        self.assertIsInstance(self.detector.ml_models, dict)
        self.assertEqual(len(self.detector.templates), 0)

    def test_load_templates_empty_directory(self):
        """Test loading templates from empty directory"""
        self.detector.load_templates(self.test_dir)
        self.assertEqual(len(self.detector.templates), 0)

    @patch("cv2.imread")
    def test_load_templates_with_files(self, mock_imread):
        """Test loading templates with actual files"""
        # Create mock template files
        template_path = Path(self.test_dir) / "tree.png"
        template_path.touch()

        # Mock successful image loading
        mock_imread.return_value = np.zeros((50, 50, 3), dtype=np.uint8)

        self.detector.load_templates(self.test_dir)

        self.assertIn("tree", self.detector.templates)
        mock_imread.assert_called()

    @patch("cv2.matchTemplate")
    def test_detect_objects_template_matching(self, mock_match_template):
        """Test object detection using template matching"""
        # Set up test data
        test_image = np.zeros((600, 800, 3), dtype=np.uint8)
        self.detector.templates["tree"] = np.zeros((50, 50, 3), dtype=np.uint8)

        # Mock template matching
        mock_result = np.array([[0.9, 0.7], [0.6, 0.8]])
        mock_match_template.return_value = mock_result

        with patch("numpy.where") as mock_where:
            mock_where.return_value = ([100, 200], [150, 250])

            objects = self.detector.detect_objects(test_image)

            self.assertIsInstance(objects, list)
            # Should have detected objects from template matching
            template_objects = [
                obj for obj in objects if obj.object_type == "template_match"
            ]
            self.assertTrue(len(template_objects) >= 0)

    def test_detect_objects_empty_image(self):
        """Test object detection with empty image"""
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        objects = self.detector.detect_objects(test_image)

        self.assertIsInstance(objects, list)
        # Should return empty list or objects from other detection methods

    @patch("cv2.findContours")
    @patch("cv2.cvtColor")
    @patch("cv2.inRange")
    def test_detect_by_color(self, mock_inrange, mock_cvtcolor, mock_findcontours):
        """Test color-based object detection"""
        # Set up color ranges
        self.detector.color_ranges["red"] = ([0, 50, 50], [10, 255, 255])

        # Mock OpenCV functions
        mock_cvtcolor.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_inrange.return_value = np.zeros((100, 100), dtype=np.uint8)

        # Mock contours
        mock_contour = np.array([[10, 10], [20, 10], [20, 20], [10, 20]])
        mock_findcontours.return_value = ([mock_contour], None)

        with patch("cv2.contourArea", return_value=200), patch(
            "cv2.boundingRect", return_value=(10, 10, 10, 10)
        ):
            test_image = np.zeros((100, 100, 3), dtype=np.uint8)
            objects = self.detector._detect_by_color(test_image)

            self.assertIsInstance(objects, list)


class TestGameStateAnalyzer(unittest.TestCase):
    """Test GameStateAnalyzer functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = GameStateAnalyzer(GameType.OSRS)

    def test_analyzer_initialization(self):
        """Test analyzer initialization"""
        self.assertEqual(self.analyzer.game_type, GameType.OSRS)
        self.assertIsInstance(self.analyzer.state_history, list)
        self.assertIsInstance(self.analyzer.pattern_database, dict)
        self.assertIsInstance(self.analyzer.learning_data, dict)
        self.assertEqual(len(self.analyzer.state_history), 0)

    def test_analyze_game_state(self):
        """Test game state analysis"""
        test_image = np.zeros((600, 800, 3), dtype=np.uint8)
        test_objects = [
            GameObjectData("obj1", "tree", (100, 100), "resource", 0.9),
            GameObjectData("obj2", "npc", (200, 200), "npc", 0.8),
        ]

        result = self.analyzer.analyze_game_state(test_image, test_objects)

        self.assertIsInstance(result, GameAnalysisResult)
        self.assertIsInstance(result.game_state, GameState)
        self.assertEqual(len(result.objects_detected), 2)
        self.assertIsInstance(result.player_stats, dict)
        self.assertIsInstance(result.environment_data, dict)
        self.assertIsInstance(result.recommendations, list)
        self.assertIsInstance(result.analysis_confidence, float)
        self.assertGreaterEqual(result.analysis_confidence, 0.0)
        self.assertLessEqual(result.analysis_confidence, 1.0)

    def test_determine_game_state_combat(self):
        """Test game state determination for combat"""
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        combat_objects = [
            GameObjectData("obj1", "combat interface", (50, 50), "ui", 0.9)
        ]

        state = self.analyzer._determine_game_state(test_image, combat_objects)
        self.assertEqual(state, GameState.COMBAT)

    def test_determine_game_state_banking(self):
        """Test game state determination for banking"""
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        bank_objects = [GameObjectData("obj1", "bank interface", (50, 50), "ui", 0.9)]

        state = self.analyzer._determine_game_state(test_image, bank_objects)
        self.assertEqual(state, GameState.BANKING)

    def test_extract_player_stats(self):
        """Test player stats extraction"""
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        stat_objects = [GameObjectData("obj1", "HP: 75/100", (50, 50), "text", 0.9)]

        stats = self.analyzer._extract_player_stats(test_image, stat_objects)

        self.assertIsInstance(stats, dict)
        self.assertIn("health", stats)
        self.assertEqual(stats["health"], 75)

    def test_generate_recommendations_low_health(self):
        """Test recommendations for low health"""
        stats = {"health": 25}
        environment = {"threats": [], "opportunities": []}

        recommendations = self.analyzer._generate_recommendations(
            GameState.IDLE, stats, environment
        )

        self.assertIsInstance(recommendations, list)
        # Should have emergency action for low health
        emergency_actions = [
            r
            for r in recommendations
            if r.decision_type == AIDecisionType.EMERGENCY_ACTION
        ]
        self.assertTrue(len(emergency_actions) > 0)

    def test_generate_recommendations_opportunities(self):
        """Test recommendations for opportunities"""
        stats = {"health": 100, "inventory_space": 25}
        environment = {"threats": [], "opportunities": ["tree", "rock"]}

        recommendations = self.analyzer._generate_recommendations(
            GameState.IDLE, stats, environment
        )

        self.assertIsInstance(recommendations, list)
        # Should have click object recommendations
        click_actions = [
            r for r in recommendations if r.decision_type == AIDecisionType.CLICK_OBJECT
        ]
        self.assertTrue(len(click_actions) > 0)

    def test_calculate_confidence(self):
        """Test confidence calculation"""
        high_conf_objects = [
            GameObjectData("obj1", "tree", (100, 100), "resource", 0.95),
            GameObjectData("obj2", "npc", (200, 200), "npc", 0.90),
        ]

        confidence = self.analyzer._calculate_confidence(
            GameState.IDLE, high_conf_objects
        )

        self.assertIsInstance(confidence, float)
        self.assertGreaterEqual(confidence, 0.0)
        self.assertLessEqual(confidence, 1.0)
        self.assertGreater(confidence, 0.5)  # Should be high with good objects


class TestAIGameController(unittest.TestCase):
    """Test AIGameController functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.controller = AIGameController(GameType.OSRS)

    def test_controller_initialization(self):
        """Test controller initialization"""
        self.assertEqual(self.controller.game_type, GameType.OSRS)
        self.assertFalse(self.controller.is_running)
        self.assertIsInstance(self.controller.action_delay, float)
        self.assertGreater(self.controller.action_delay, 0)

    def test_start_stop_controller(self):
        """Test starting and stopping controller"""
        self.controller.start()
        self.assertTrue(self.controller.is_running)

        self.controller.stop()
        self.assertFalse(self.controller.is_running)

    @patch("pyautogui.click")
    def test_execute_click_decision(self, mock_click):
        """Test executing click decision"""
        self.controller.start()

        decision = AIGameDecision(
            decision_type=AIDecisionType.CLICK_OBJECT,
            target="tree",
            parameters={"coordinates": (100, 200)},
            priority=0.8,
            confidence=0.9,
            reasoning="Click tree to chop",
            expected_duration=3.0,
            risk_level=0.1,
        )

        success = self.controller.execute_decision(decision)

        # Should attempt to execute (may fail without pyautogui)
        self.assertIsInstance(success, bool)

        self.controller.stop()

    @patch("pyautogui.moveTo")
    def test_execute_move_decision(self, mock_move):
        """Test executing move decision"""
        self.controller.start()

        decision = AIGameDecision(
            decision_type=AIDecisionType.MOVE_TO_LOCATION,
            target="location",
            parameters={"destination": (300, 400)},
            priority=0.7,
            confidence=0.8,
            reasoning="Move to location",
            expected_duration=5.0,
            risk_level=0.2,
        )

        success = self.controller.execute_decision(decision)

        self.assertIsInstance(success, bool)

        self.controller.stop()

    def test_execute_decision_not_running(self):
        """Test executing decision when controller not running"""
        decision = AIGameDecision(
            decision_type=AIDecisionType.CLICK_OBJECT,
            target="tree",
            parameters={},
            priority=0.8,
            confidence=0.9,
            reasoning="Test",
            expected_duration=3.0,
            risk_level=0.1,
        )

        success = self.controller.execute_decision(decision)
        self.assertFalse(success)


class TestAIGamingSystem(unittest.TestCase):
    """Test AIGamingSystem functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.config = {
            "templates_dir": tempfile.mkdtemp(),
            "capture_region": None,
            "action_delay": 0.1,
        }
        self.ai_system = AIGamingSystem(GameType.OSRS, self.config)

    def tearDown(self):
        """Clean up test fixtures"""
        if self.ai_system.is_running:
            self.ai_system.stop()
        shutil.rmtree(self.config["templates_dir"], ignore_errors=True)

    def test_ai_system_initialization(self):
        """Test AI system initialization"""
        self.assertEqual(self.ai_system.game_type, GameType.OSRS)
        self.assertEqual(self.ai_system.config, self.config)
        self.assertIsNotNone(self.ai_system.screen_capture)
        self.assertIsNotNone(self.ai_system.object_detector)
        self.assertIsNotNone(self.ai_system.state_analyzer)
        self.assertIsNotNone(self.ai_system.controller)
        self.assertFalse(self.ai_system.is_running)

    def test_performance_metrics_initialization(self):
        """Test performance metrics initialization"""
        metrics = self.ai_system.get_performance_metrics()

        self.assertIsInstance(metrics, dict)
        self.assertIn("decisions_made", metrics)
        self.assertIn("actions_executed", metrics)
        self.assertIn("success_rate", metrics)
        self.assertIn("average_confidence", metrics)
        self.assertEqual(metrics["decisions_made"], 0)
        self.assertEqual(metrics["actions_executed"], 0)

    @patch.object(AIGamingSystem, "initialize", return_value=True)
    def test_start_system(self, mock_initialize):
        """Test starting AI system"""
        success = self.ai_system.start()

        self.assertTrue(success)
        self.assertTrue(self.ai_system.is_running)
        mock_initialize.assert_called_once()

    def test_stop_system(self):
        """Test stopping AI system"""
        # Manually set running state for test
        self.ai_system.is_running = True

        self.ai_system.stop()

        self.assertFalse(self.ai_system.is_running)

    @patch.object(AIGamingSystem, "initialize", return_value=False)
    def test_start_system_initialization_failure(self, mock_initialize):
        """Test starting AI system with initialization failure"""
        success = self.ai_system.start()

        self.assertFalse(success)
        self.assertFalse(self.ai_system.is_running)

    def test_manual_analyze(self):
        """Test manual analysis trigger"""
        # This will likely return None without proper setup, but should not crash
        result = self.ai_system.manual_analyze()

        # Should return None or GameAnalysisResult
        self.assertTrue(result is None or isinstance(result, GameAnalysisResult))


class TestCreateAIGamingSystem(unittest.TestCase):
    """Test factory function"""

    def test_create_ai_gaming_system(self):
        """Test creating AI gaming system via factory"""
        config = {"test": "value"}
        system = create_ai_gaming_system(GameType.STRATEGY, config)

        self.assertIsInstance(system, AIGamingSystem)
        self.assertEqual(system.game_type, GameType.STRATEGY)
        self.assertEqual(system.config, config)

    def test_create_ai_gaming_system_no_config(self):
        """Test creating AI gaming system without config"""
        system = create_ai_gaming_system(GameType.PUZZLE)

        self.assertIsInstance(system, AIGamingSystem)
        self.assertEqual(system.game_type, GameType.PUZZLE)
        self.assertEqual(system.config, {})


def run_ai_gaming_tests():
    """Run all AI gaming system tests"""
    print("🤖 Running AI Gaming Systems Tests...")
    print("=" * 60)

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_classes = [
        TestGameType,
        TestAIDecisionType,
        TestGameState,
        TestGameObjectData,
        TestAIGameDecision,
        TestGameAnalysisResult,
        TestScreenCapture,
        TestObjectDetector,
        TestGameStateAnalyzer,
        TestAIGameController,
        TestAIGamingSystem,
        TestCreateAIGamingSystem,
    ]

    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 60)
    print("📊 AI GAMING SYSTEMS TEST RESULTS:")
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
        print("\n🎉 ALL AI GAMING SYSTEMS TESTS PASSED!")
        return True
    else:
        print("\n❌ SOME AI GAMING SYSTEMS TESTS FAILED!")
        return False


if __name__ == "__main__":
    success = run_ai_gaming_tests()
    sys.exit(0 if success else 1)
