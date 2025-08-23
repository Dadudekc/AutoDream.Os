#!/usr/bin/env python3
"""
Test Suite: Autonomous Development System - Agent Cellphone V2
============================================================

Comprehensive testing of the autonomous development system including:
- IntelligentPromptGenerator class
- AutonomousDevelopmentEngine class
- PyAutoGUI integration safety
- Context-aware prompt generation
- Development action execution flow
- Input targeting validation

Focus: Ensuring the system correctly identifies input targets and generates
intelligent, context-aware development prompts.
"""

import unittest
import time
import json
from unittest.mock import Mock, patch, MagicMock, call
from typing import Dict, List, Any

# Import the classes we want to test
from src.core.autonomous_development import (
    AutonomousDevelopmentEngine,
    IntelligentPromptGenerator,
    DevelopmentAction,
    CodeImprovement,
    CursorAgentPrompt,
)


class TestIntelligentPromptGenerator(unittest.TestCase):
    """Test suite for the IntelligentPromptGenerator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.generator = IntelligentPromptGenerator()

        # Sample improvement for testing
        self.sample_improvement = CodeImprovement(
            file_path="test_function.py",
            line_number=42,
            current_code="def complex_function():",
            suggested_improvement="Add error handling and documentation",
            improvement_type="code_review",
            confidence=0.8,
        )

        # Sample context for testing
        self.sample_context = {
            "file_type": "function definition",
            "language": "python",
            "complexity": "high",
            "current_issues": ["missing error handling", "no documentation"],
            "recent_changes": ["function added", "basic logic implemented"],
        }

    def test_agent_specializations_initialization(self):
        """Test that agent specializations are properly initialized"""
        # Verify all expected agent types are present
        expected_agents = [
            "code_reviewer",
            "documentation_expert",
            "testing_specialist",
            "performance_analyst",
            "security_expert",
        ]

        for agent_type in expected_agents:
            self.assertIn(agent_type, self.generator.agent_specializations)
            self.assertIn("expertise", self.generator.agent_specializations[agent_type])
            self.assertIn(
                "prompt_template", self.generator.agent_specializations[agent_type]
            )
            self.assertIn(
                "focus_areas", self.generator.agent_specializations[agent_type]
            )

    def test_agent_selection_logic(self):
        """Test that the correct agent is selected for each improvement type"""
        test_cases = [
            ("code_review", "code_reviewer"),
            ("documentation", "documentation_expert"),
            ("testing", "testing_specialist"),
            ("optimization", "performance_analyst"),
            ("security", "security_expert"),
            ("bug_fix", "code_reviewer"),
            ("unknown_type", "code_reviewer"),  # Default case
        ]

        for improvement_type, expected_agent in test_cases:
            with self.subTest(improvement_type=improvement_type):
                improvement = CodeImprovement(
                    file_path="test.py",
                    line_number=1,
                    current_code="test code",
                    suggested_improvement="test improvement",
                    improvement_type=improvement_type,
                    confidence=0.8,
                )

                context = {"language": "python", "complexity": "medium"}

                prompt = self.generator.generate_intelligent_prompt(
                    improvement, context
                )
                self.assertEqual(prompt.agent_type, expected_agent)

    def test_context_analysis_accuracy(self):
        """Test that context analysis accurately identifies development context"""
        test_context = {
            "file_type": "API endpoint",
            "language": "javascript",
            "complexity": "high",
            "current_issues": ["security", "performance"],
            "recent_changes": ["refactored", "added tests"],
        }

        analysis = self.generator._analyze_context(test_context)

        self.assertEqual(analysis["file_type"], "API endpoint")
        self.assertEqual(analysis["language"], "javascript")
        self.assertEqual(analysis["complexity"], "high")
        self.assertEqual(len(analysis["current_issues"]), 2)
        self.assertEqual(len(analysis["recent_changes"]), 2)
        self.assertIn("summary", analysis)

    def test_context_summary_generation(self):
        """Test that context summaries are generated correctly"""
        context = {
            "file_type": "function definition",
            "language": "python",
            "complexity": "high",
            "current_issues": ["missing error handling"],
            "recent_changes": ["function added"],
        }

        summary = self.generator._generate_context_summary(context)

        self.assertIn("Python function definition with high complexity", summary)
        self.assertIn("has 1 identified issues", summary)
        self.assertIn("recently modified with 1 changes", summary)

    def test_focus_area_selection(self):
        """Test that focus areas are selected appropriately"""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="optimization",
            confidence=0.8,
        )

        agent_info = self.generator.agent_specializations["performance_analyst"]
        focus_area = self.generator._select_focus_area(improvement, agent_info)

        self.assertEqual(focus_area, "performance")

    def test_intelligent_prompt_generation(self):
        """Test that intelligent prompts are generated with proper context"""
        prompt = self.generator.generate_intelligent_prompt(
            self.sample_improvement, self.sample_context
        )

        # Verify prompt structure
        self.assertIsInstance(prompt, CursorAgentPrompt)
        self.assertEqual(prompt.agent_type, "code_reviewer")
        self.assertIn("Python function definition with high complexity", prompt.context)
        self.assertIn("Add error handling and documentation", prompt.intelligent_prompt)
        self.assertIn("Line: 42", prompt.intelligent_prompt)
        self.assertIn("complex code", prompt.intelligent_prompt)
        self.assertGreater(prompt.confidence, 0.8)

    def test_prompt_template_filling(self):
        """Test that prompt templates are properly filled with context"""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=10,
            current_code="def test_function():",
            suggested_improvement="Add type hints",
            improvement_type="code_review",
            confidence=0.7,
        )

        context = {
            "file_type": "function definition",
            "language": "python",
            "complexity": "low",
            "current_issues": [],
            "recent_changes": [],
        }

        prompt = self.generator.generate_intelligent_prompt(improvement, context)

        # Verify template was filled
        self.assertIn(
            "Python function definition with low complexity", prompt.intelligent_prompt
        )
        self.assertIn("Add type hints", prompt.intelligent_prompt)
        self.assertIn("Line: 10", prompt.intelligent_prompt)

    def test_confidence_calculation(self):
        """Test that confidence is calculated correctly based on context"""
        # Test low complexity (should increase confidence)
        context_low = {"complexity": "low"}
        prompt_low = self.generator.generate_intelligent_prompt(
            self.sample_improvement, context_low
        )

        # Test high complexity (should decrease confidence)
        context_high = {"complexity": "high"}
        prompt_high = self.generator.generate_intelligent_prompt(
            self.sample_improvement, context_high
        )

        # Low complexity should have higher confidence
        self.assertGreater(prompt_low.confidence, prompt_high.confidence)

    def test_expected_outcome_definition(self):
        """Test that expected outcomes are defined correctly for each agent type"""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="documentation",
            confidence=0.8,
        )

        prompt = self.generator.generate_intelligent_prompt(
            improvement, self.sample_context
        )

        # Should be documentation expert
        self.assertEqual(prompt.agent_type, "documentation_expert")
        self.assertIn("Clearer, more comprehensive", prompt.expected_outcome)

    def test_agent_expertise_integration(self):
        """Test that agent expertise is properly integrated into prompts"""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="security",
            confidence=0.8,
        )

        context = {"language": "python", "complexity": "medium"}
        prompt = self.generator.generate_intelligent_prompt(improvement, context)

        # Should include security expertise
        self.assertEqual(prompt.agent_type, "security_expert")
        self.assertIn("security analysis", prompt.intelligent_prompt.lower())
        self.assertIn("vulnerability assessment", prompt.intelligent_prompt.lower())


class TestAutonomousDevelopmentEngine(unittest.TestCase):
    """Test suite for the AutonomousDevelopmentEngine class"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock PyAutoGUI to prevent actual automation
        self.pyautogui_patcher = patch("src.core.autonomous_development.pyautogui")
        self.mock_pyautogui = self.pyautogui_patcher.start()

        # Mock pyperclip
        self.pyperclip_patcher = patch("src.core.autonomous_development.pyperclip")
        self.mock_pyperclip = self.pyperclip_patcher.start()

        # Mock the core systems
        self.mock_perpetual_motion = Mock()
        self.mock_cursor_capture = Mock()

        # Create test engine with mocked dependencies
        with patch("src.core.autonomous_development.PYAUTOGUI_AVAILABLE", True):
            with patch(
                "src.core.autonomous_development.PerpetualMotionEngine",
                return_value=self.mock_perpetual_motion,
            ):
                with patch(
                    "src.core.autonomous_development.CursorResponseCapture",
                    return_value=self.mock_cursor_capture,
                ):
                    self.engine = AutonomousDevelopmentEngine()

    def tearDown(self):
        """Clean up after tests"""
        self.pyautogui_patcher.stop()
        self.pyperclip_patcher.stop()

    def test_engine_initialization(self):
        """Test that the engine initializes correctly"""
        self.assertIsNotNone(self.engine.prompt_generator)
        self.assertIsInstance(self.engine.prompt_generator, IntelligentPromptGenerator)
        self.assertEqual(len(self.engine.development_actions), 0)
        self.assertEqual(self.engine.autonomous_cycle_count, 0)
        self.assertFalse(self.engine.is_autonomous)

    def test_pyautogui_setup(self):
        """Test that PyAutoGUI is configured safely"""
        # Verify PyAutoGUI safety settings
        self.mock_pyautogui.FAILSAFE.assert_called_with(True)
        self.mock_pyautogui.PAUSE.assert_called_with(0.1)

        # Verify screen dimensions are captured
        self.mock_pyautogui.size.assert_called_once()

    def test_autonomous_triggers_setup(self):
        """Test that autonomous development triggers are properly configured"""
        # Verify triggers were added to perpetual motion engine
        self.mock_perpetual_motion.add_trigger.assert_called()

        # Verify agent activations were registered
        self.mock_perpetual_motion.register_agent_activation.assert_called()

        # Should have registered 4 agent types
        expected_calls = [
            call("autonomous_code_review", self.engine.autonomous_code_review),
            call("autonomous_documentation", self.engine.autonomous_documentation),
            call("autonomous_testing", self.engine.autonomous_testing),
            call("autonomous_optimization", self.engine.autonomous_optimization),
        ]

        self.mock_perpetual_motion.register_agent_activation.assert_has_calls(
            expected_calls, any_order=True
        )

    def test_start_autonomous_development(self):
        """Test starting autonomous development mode"""
        # Mock perpetual motion start
        self.mock_perpetual_motion.start_perpetual_motion.return_value = None

        # Start autonomous development
        result = self.engine.start_autonomous_development()

        # Verify success
        self.assertTrue(result)
        self.assertTrue(self.engine.is_autonomous)

        # Verify perpetual motion was started
        self.mock_perpetual_motion.start_perpetual_motion.assert_called_once()

        # Verify autonomous thread was started
        self.assertTrue(hasattr(self.engine, "autonomous_thread"))
        self.assertTrue(self.engine.autonomous_thread.is_alive())

    def test_stop_autonomous_development(self):
        """Test stopping autonomous development mode"""
        # Start autonomous development first
        self.engine.is_autonomous = True
        self.engine.start_autonomous_development()

        # Stop autonomous development
        self.engine.stop_autonomous_development()

        # Verify stopped
        self.assertFalse(self.engine.is_autonomous)

        # Verify perpetual motion was stopped
        self.mock_perpetual_motion.stop_perpetual_motion.assert_called_once()

    def test_message_improvement_analysis(self):
        """Test that messages are analyzed for improvement opportunities"""
        test_message = {
            "content": "This function needs optimization and better documentation",
            "role": "assistant",
            "thread_id": "test_thread_123",
        }

        # Mock cursor capture to return our test message
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        # Execute one cycle to trigger analysis
        self.engine._execute_autonomous_cycle()

        # Verify that improvements were identified
        self.assertGreater(len(self.engine.development_actions), 0)

        # Check that actions have proper target elements
        for action in self.engine.development_actions:
            self.assertEqual(action.target_element, "cursor_editor")
            self.assertEqual(action.action_type, "code_generation")

    def test_context_extraction(self):
        """Test that development context is properly extracted"""
        test_message = {
            "content": "This Python API endpoint function is too complex and needs refactoring",
            "role": "assistant",
            "thread_id": "test_thread_456",
        }

        # Mock cursor capture
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        # Execute cycle
        self.engine._execute_autonomous_cycle()

        # Verify context extraction
        self.assertGreater(len(self.engine.development_actions), 0)

        action = self.engine.development_actions[0]
        context = action.action_data.get("context")

        self.assertIsNotNone(context)
        self.assertEqual(context["language"], "python")
        self.assertEqual(context["file_type"], "API endpoint")
        self.assertEqual(context["complexity"], "high")

    def test_intelligent_development_action_creation(self):
        """Test that intelligent development actions are created with proper prompts"""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="code_review",
            confidence=0.8,
        )

        test_message = {"content": "test message", "role": "assistant"}

        # Create intelligent development action
        self.engine._create_intelligent_development_action(improvement, test_message)

        # Verify action was created
        self.assertEqual(len(self.engine.development_actions), 1)

        action = self.engine.development_actions[0]
        self.assertEqual(action.action_type, "code_generation")
        self.assertEqual(action.target_element, "cursor_editor")

        # Verify cursor agent prompt was generated
        cursor_agent_prompt = action.action_data.get("cursor_agent_prompt")
        self.assertIsNotNone(cursor_agent_prompt)
        self.assertIsInstance(cursor_agent_prompt, CursorAgentPrompt)

    def test_development_action_execution(self):
        """Test that development actions are executed correctly"""
        # Create a test action
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="code_review",
            confidence=0.8,
        )

        context = {"language": "python", "complexity": "medium"}
        cursor_agent_prompt = self.engine.prompt_generator.generate_intelligent_prompt(
            improvement, context
        )

        action = DevelopmentAction(
            action_id="test_action",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={
                "improvement": improvement,
                "cursor_agent_prompt": cursor_agent_prompt,
                "context": context,
            },
            priority=8,
        )

        # Add action
        self.engine.development_actions.append(action)

        # Execute actions
        with patch.object(self.engine, "_navigate_to_cursor") as mock_navigate:
            with patch.object(self.engine, "_type_in_cursor") as mock_type:
                self.engine._execute_development_actions()

                # Verify execution flow
                mock_navigate.assert_called_once()
                mock_type.assert_called_once()

                # Verify action was removed
                self.assertEqual(len(self.engine.development_actions), 0)

    def test_action_priority_ordering(self):
        """Test that actions are executed in priority order"""
        # Create actions with different priorities
        low_priority = DevelopmentAction(
            action_id="low_priority",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},
            priority=1,
        )

        high_priority = DevelopmentAction(
            action_id="high_priority",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},
            priority=10,
        )

        # Add in reverse order
        self.engine.development_actions.append(low_priority)
        self.engine.development_actions.append(high_priority)

        # Execute actions
        with patch.object(
            self.engine, "_execute_intelligent_code_generation_action"
        ) as mock_execute:
            self.engine._execute_development_actions()

            # Verify high priority was executed first
            mock_execute.assert_called_once()
            call_args = mock_execute.call_args[0][0]
            self.assertEqual(call_args.action_id, "high_priority")

    def test_autonomous_agent_activation(self):
        """Test that autonomous agents are activated correctly"""
        test_message = {
            "content": "This code needs security review",
            "role": "assistant",
            "thread_id": "test_thread_789",
        }

        # Mock cursor capture
        self.mock_cursor_capture.get_recent_messages.return_value = [test_message]

        # Execute cycle
        self.engine._execute_autonomous_cycle()

        # Verify that security-related improvement was identified
        self.assertGreater(len(self.engine.development_actions), 0)

        action = self.engine.development_actions[0]
        cursor_agent_prompt = action.action_data.get("cursor_agent_prompt")

        # Should select security expert for security review
        self.assertEqual(cursor_agent_prompt.agent_type, "security_expert")

    def test_conversation_generation(self):
        """Test that new intelligent conversations are generated"""
        # Set up conditions for conversation generation
        self.engine.autonomous_cycle_count = 10  # Multiple of 10
        self.engine.active_conversations = 2  # Below limit

        # Mock the conversation generation
        with patch.object(
            self.engine, "_generate_intelligent_conversation"
        ) as mock_generate:
            self.engine._execute_autonomous_cycle()

            # Verify conversation generation was called
            mock_generate.assert_called_once()

    def test_error_handling(self):
        """Test that errors are handled gracefully"""
        # Test with malformed message
        malformed_message = {"content": "", "role": "assistant"}  # Empty content

        # Mock cursor capture
        self.mock_cursor_capture.get_recent_messages.return_value = [malformed_message]

        # Execute cycle (should not crash)
        try:
            self.engine._execute_autonomous_cycle()
            # Should handle gracefully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Should handle malformed messages gracefully: {e}")

    def test_performance_metrics(self):
        """Test that performance metrics are tracked correctly"""
        # Start autonomous development
        self.engine.start_autonomous_development()

        # Verify performance tracking is active
        self.assertTrue(self.engine.is_autonomous)

        # Check that performance metrics are available
        stats = self.engine.get_autonomous_stats()
        self.assertIn("autonomous_cycle_count", stats)
        self.assertIn("pending_actions", stats)
        self.assertIn("enhanced_prompts", stats)
        self.assertIn("intelligent_agents", stats)

        # Stop autonomous development
        self.engine.stop_autonomous_development()


class TestDevelopmentActionExecution(unittest.TestCase):
    """Test suite for development action execution flow"""

    def setUp(self):
        """Set up test fixtures"""
        # Mock PyAutoGUI
        self.pyautogui_patcher = patch("src.core.autonomous_development.pyautogui")
        self.mock_pyautogui = self.pyautogui_patcher.start()

        # Mock pyperclip
        self.pyperclip_patcher = patch("src.core.autonomous_development.pyperclip")
        self.mock_pyperclip = self.pyperclip_patcher.start()

        # Create test engine
        with patch("src.core.autonomous_development.PYAUTOGUI_AVAILABLE", True):
            with patch("src.core.autonomous_development.PerpetualMotionEngine"):
                with patch("src.core.autonomous_development.CursorResponseCapture"):
                    self.engine = AutonomousDevelopmentEngine()

    def tearDown(self):
        """Clean up after tests"""
        self.pyautogui_patcher.stop()
        self.pyperclip_patcher.stop()

    def test_navigation_to_cursor(self):
        """Test navigation to Cursor window"""
        with patch("time.sleep") as mock_sleep:
            self.engine._navigate_to_cursor()

            # Verify pause for focus
            mock_sleep.assert_called_with(0.5)

    def test_typing_in_cursor(self):
        """Test typing text in Cursor editor"""
        test_text = "This is a test prompt for autonomous development"

        with patch("time.sleep") as mock_sleep:
            self.engine._type_in_cursor(test_text)

            # Verify clipboard copy
            self.mock_pyperclip.copy.assert_called_with(test_text)

            # Verify paste operation
            self.mock_pyautogui.hotkey.assert_called_with("ctrl", "v")

            # Verify typing pause
            mock_sleep.assert_called_with(0.2)

    def test_intelligent_code_generation_execution(self):
        """Test execution of intelligent code generation actions"""
        # Create test action with cursor agent prompt
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="code_review",
            confidence=0.8,
        )

        context = {"language": "python", "complexity": "medium"}
        cursor_agent_prompt = self.engine.prompt_generator.generate_intelligent_prompt(
            improvement, context
        )

        action = DevelopmentAction(
            action_id="test_action",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={
                "improvement": improvement,
                "cursor_agent_prompt": cursor_agent_prompt,
                "context": context,
            },
            priority=8,
        )

        # Mock the execution methods
        with patch.object(self.engine, "_navigate_to_cursor") as mock_navigate:
            with patch.object(self.engine, "_type_in_cursor") as mock_type:
                with patch.object(self.engine, "mock_pyautogui") as mock_pyautogui:
                    # Execute action
                    self.engine._execute_intelligent_code_generation_action(action)

                    # Verify execution flow
                    mock_navigate.assert_called_once()
                    mock_type.assert_called_once()

                    # Verify Enter key was pressed
                    mock_pyautogui.press.assert_called_with("enter")

    def test_missing_cursor_agent_prompt_handling(self):
        """Test handling of actions without cursor agent prompts"""
        # Create action without cursor agent prompt
        action = DevelopmentAction(
            action_id="invalid_action",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},  # Missing cursor_agent_prompt
            priority=1,
        )

        # Execute action (should handle gracefully)
        try:
            self.engine._execute_intelligent_code_generation_action(action)
            # Should handle gracefully
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Should handle missing cursor agent prompt gracefully: {e}")


def run_autonomous_development_tests():
    """Run all autonomous development tests"""
    print("🧪 RUNNING AUTONOMOUS DEVELOPMENT SYSTEM TESTS")
    print("=" * 70)
    print("Focus: Input targeting validation, intelligent prompt generation")
    print("Note: PyAutoGUI automation is mocked - no actual GUI interaction")
    print()

    # Create test suite
    test_suite = unittest.TestSuite()

    # Add test classes
    test_suite.addTest(unittest.makeSuite(TestIntelligentPromptGenerator))
    test_suite.addTest(unittest.makeSuite(TestAutonomousDevelopmentEngine))
    test_suite.addTest(unittest.makeSuite(TestDevelopmentActionExecution))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)

    # Print summary
    print("\n" + "=" * 70)
    print("📊 AUTONOMOUS DEVELOPMENT TEST SUMMARY")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.failures:
        print("\n❌ FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")

    if result.errors:
        print("\n⚠️ ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")

    if not result.failures and not result.errors:
        print("\n✅ ALL TESTS PASSED!")
        print("   Autonomous development system validation successful!")
        print("   Input targeting validation working correctly!")
        print("   Intelligent prompt generation functioning properly!")

    return result.wasSuccessful()


if __name__ == "__main__":
    # Run autonomous development tests
    success = run_autonomous_development_tests()

    # Exit with appropriate code
    exit(0 if success else 1)
