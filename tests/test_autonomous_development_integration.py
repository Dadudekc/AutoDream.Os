#!/usr/bin/env python3
"""Integration tests for the autonomous development system."""

import unittest
from unittest.mock import Mock, patch

from src.utils.stability_improvements import safe_import

autonomous_dev_module = safe_import("src.core.autonomous_development")
AutonomousDevelopmentEngine = getattr(
    autonomous_dev_module, "AutonomousDevelopmentEngine", None
)
DevelopmentAction = getattr(autonomous_dev_module, "DevelopmentAction", None)

code_module = safe_import("src.autonomous_development.code.generator")
CodeImprovement = getattr(code_module, "CodeImprovement", None)
CursorAgentPrompt = getattr(code_module, "CursorAgentPrompt", None)


@unittest.skipUnless(
    AutonomousDevelopmentEngine
    and DevelopmentAction
    and CodeImprovement
    and CursorAgentPrompt,
    "Autonomous development integration components not available",
)


class TestAutonomousDevelopmentIntegration(unittest.TestCase):
    """Integration tests covering action creation and execution."""

    def setUp(self):
        self.pyautogui_patcher = patch("src.core.autonomous_development.pyautogui")
        self.mock_pyautogui = self.pyautogui_patcher.start()

        self.pyperclip_patcher = patch("src.core.autonomous_development.pyperclip")
        self.mock_pyperclip = self.pyperclip_patcher.start()

        self.mock_perpetual_motion = Mock()
        self.mock_cursor_capture = Mock()

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
        self.pyautogui_patcher.stop()
        self.pyperclip_patcher.stop()

    def test_intelligent_development_action_creation(self):
        """Ensure actions include cursor agent prompts."""
        improvement = CodeImprovement(
            file_path="test.py",
            line_number=1,
            current_code="test code",
            suggested_improvement="test improvement",
            improvement_type="code_review",
            confidence=0.8,
        )

        test_message = {"content": "test message", "role": "assistant"}
        self.engine._create_intelligent_development_action(improvement, test_message)

        self.assertEqual(len(self.engine.development_actions), 1)
        action = self.engine.development_actions[0]
        self.assertEqual(action.action_type, "code_generation")
        self.assertEqual(action.target_element, "cursor_editor")
        cursor_agent_prompt = action.action_data.get("cursor_agent_prompt")
        self.assertIsNotNone(cursor_agent_prompt)
        self.assertIsInstance(cursor_agent_prompt, CursorAgentPrompt)

    def test_development_action_execution(self):
        """Verify development actions execute correctly."""
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

        self.engine.development_actions.append(action)

        with patch.object(self.engine, "_navigate_to_cursor") as mock_nav:
            with patch.object(self.engine, "_type_in_cursor") as mock_type:
                self.engine._execute_development_actions()
                mock_nav.assert_called_once()
                mock_type.assert_called_once()
                self.assertEqual(len(self.engine.development_actions), 0)
