"""OpenAI API integration for code generation and analysis."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional
import os

from .integration_common import get_env_var, logger

try:
    import openai
except ImportError as exc:  # pragma: no cover - dependency not installed
    raise ImportError(
        "OpenAI package not available. Install with: pip install openai"
    ) from exc


class OpenAIIntegration:
    """Integration wrapper for the OpenAI chat/completions API."""

    def __init__(
        self, api_key: Optional[str] = None, organization: Optional[str] = None
    ):
        self.api_key = api_key or get_env_var("OPENAI_API_KEY")
        self.organization = organization or os.getenv("OPENAI_ORGANIZATION")

        openai.api_key = self.api_key
        if self.organization:
            openai.organization = self.organization

        self.default_model = "gpt-4"
        self.max_tokens = 4096
        self.temperature = 0.7

        logger.info("OpenAI integration initialized")

    def generate_code(
        self,
        prompt: str,
        model: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate code using OpenAI API."""
        try:
            response = openai.ChatCompletion.create(
                model=model or self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python developer. Generate clean, well-documented code.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=max_tokens or self.max_tokens,
                temperature=temperature or self.temperature,
            )

            generated_code = response.choices[0].message.content
            logger.info("Generated code using %s", model or self.default_model)
            return generated_code

        except Exception as err:  # pragma: no cover - network errors
            logger.error("Error generating code with OpenAI: %s", err)
            return ""

    def analyze_code(self, code: str, analysis_type: str = "quality") -> Dict[str, Any]:
        """Analyze code quality and provide feedback."""
        try:
            prompt = f"""
            Analyze the following Python code for {analysis_type}:

            {code}

            Provide a detailed analysis including:
            1. Code quality score (1-10)
            2. Potential improvements
            3. Best practices recommendations
            4. Security considerations
            5. Performance optimizations
            """

            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior Python code reviewer and security expert.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=0.3,
            )

            analysis = response.choices[0].message.content
            logger.info("Code analysis completed for %s", analysis_type)

            return {
                "analysis_type": analysis_type,
                "analysis": analysis,
                "timestamp": datetime.now().isoformat(),
                "model_used": self.default_model,
            }

        except Exception as err:  # pragma: no cover - network errors
            logger.error("Error analyzing code with OpenAI: %s", err)
            return {"error": str(err)}

    def generate_tests(self, code: str, test_framework: str = "pytest") -> str:
        """Generate test cases for given code."""
        try:
            prompt = f"""
            Generate comprehensive {test_framework} test cases for the following Python code:

            {code}

            Include:
            1. Unit tests for all functions/methods
            2. Edge case testing
            3. Error handling tests
            4. Mock/stub examples where appropriate
            5. Test data generation
            """

            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert in {test_framework} testing and Python development.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=0.4,
            )

            tests = response.choices[0].message.content
            logger.info("Generated %s tests", test_framework)

            return tests

        except Exception as err:  # pragma: no cover - network errors
            logger.error("Error generating tests with OpenAI: %s", err)
            return ""

    def refactor_code(self, code: str, refactoring_goal: str) -> str:
        """Refactor code based on a specific goal."""
        try:
            prompt = f"""
            Refactor the following Python code to {refactoring_goal}:

            {code}

            Provide the refactored code with:
            1. Improved readability
            2. Better performance
            3. Cleaner architecture
            4. Proper error handling
            5. Documentation
            """

            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a Python refactoring expert focused on clean code principles.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=self.max_tokens,
                temperature=0.3,
            )

            refactored_code = response.choices[0].message.content
            logger.info("Code refactoring completed for goal: %s", refactoring_goal)

            return refactored_code

        except Exception as err:  # pragma: no cover - network errors
            logger.error("Error refactoring code with OpenAI: %s", err)
            return ""
