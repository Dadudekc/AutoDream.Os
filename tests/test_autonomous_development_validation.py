#!/usr/bin/env python3
"""Validation tests for autonomous development action execution."""

import unittest
from unittest.mock import patch

from src.utils.stability_improvements import safe_import

autonomous_dev_module = safe_import("src.core.autonomous_development")
AutonomousDevelopmentEngine = getattr(
    autonomous_dev_module, "AutonomousDevelopmentEngine", None
)
DevelopmentAction = getattr(autonomous_dev_module, "DevelopmentAction", None)

code_module = safe_import("src.autonomous_development.code.generator")
CodeImprovement = getattr(code_module, "CodeImprovement", None)


@unittest.skipUnless(
    AutonomousDevelopmentEngine and DevelopmentAction and CodeImprovement,
    "Autonomous development validation components not available",
)


class TestDevelopmentActionExecution(unittest.TestCase):
    """Test suite for development action execution flow"""

    def setUp(self):
        """Set up test fixtures"""
        self.pyautogui_patcher = patch("src.core.autonomous_development.pyautogui")
        self.mock_pyautogui = self.pyautogui_patcher.start()

        self.pyperclip_patcher = patch("src.core.autonomous_development.pyperclip")
        self.mock_pyperclip = self.pyperclip_patcher.start()

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
            mock_sleep.assert_called_with(0.5)

    def test_typing_in_cursor(self):
        """Test typing text in Cursor editor"""
        test_text = "This is a test prompt for autonomous development"

        with patch("time.sleep") as mock_sleep:
            self.engine._type_in_cursor(test_text)
            self.mock_pyperclip.copy.assert_called_with(test_text)
            self.mock_pyautogui.hotkey.assert_called_with("ctrl", "v")
            mock_sleep.assert_called_with(0.2)

    def test_intelligent_code_generation_execution(self):
        """Test execution of intelligent code generation actions"""
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

        with patch.object(self.engine, "_navigate_to_cursor") as mock_navigate:
            with patch.object(self.engine, "_type_in_cursor") as mock_type:
                with patch.object(self.engine, "mock_pyautogui") as mock_pg:
                    self.engine._execute_intelligent_code_generation_action(action)
                    mock_navigate.assert_called_once()
                    mock_type.assert_called_once()
                    mock_pg.press.assert_called_with("enter")

    def test_missing_cursor_agent_prompt_handling(self):
        """Test handling of actions without cursor agent prompts"""
        action = DevelopmentAction(
            action_id="invalid_action",
            action_type="code_generation",
            target_element="cursor_editor",
            action_data={},
            priority=1,
        )

        try:
            self.engine._execute_intelligent_code_generation_action(action)
            self.assertTrue(True)
        except Exception as e:  # pragma: no cover - safeguard
            self.fail(f"Should handle missing cursor agent prompt gracefully: {e}")
