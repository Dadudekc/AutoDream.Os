#!/usr/bin/env python3
"""Core tests for the autonomous development system."""

import unittest

from src.utils.stability_improvements import safe_import

autonomous_dev_module = safe_import("src.core.autonomous_development")
IntelligentPromptGenerator = getattr(
    autonomous_dev_module, "IntelligentPromptGenerator", None
)
CodeImprovement = getattr(autonomous_dev_module, "CodeImprovement", None)
CursorAgentPrompt = getattr(autonomous_dev_module, "CursorAgentPrompt", None)


@unittest.skipUnless(
    IntelligentPromptGenerator and CodeImprovement and CursorAgentPrompt,
    "Autonomous development core components not available",
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
            ("unknown_type", "code_reviewer"),
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

        self.assertIn(
            "Python function definition with low complexity", prompt.intelligent_prompt
        )
        self.assertIn("Add type hints", prompt.intelligent_prompt)
        self.assertIn("Line: 10", prompt.intelligent_prompt)

    def test_confidence_calculation(self):
        """Test that confidence is calculated correctly based on context"""
        context_low = {"complexity": "low"}
        prompt_low = self.generator.generate_intelligent_prompt(
            self.sample_improvement, context_low
        )

        context_high = {"complexity": "high"}
        prompt_high = self.generator.generate_intelligent_prompt(
            self.sample_improvement, context_high
        )

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

        self.assertEqual(prompt.agent_type, "security_expert")
        self.assertIn("security analysis", prompt.intelligent_prompt.lower())
        self.assertIn("vulnerability assessment", prompt.intelligent_prompt.lower())
