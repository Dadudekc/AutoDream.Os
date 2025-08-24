"""AI-powered analysis helpers for the Intelligent Reviewer."""

from typing import List
import json
import logging

from .intelligent_review_core import ReviewIssue

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Wrapper around third-party AI providers for insights."""

    def __init__(self, openai_key: str | None = None, anthropic_key: str | None = None) -> None:
        self.openai_key = openai_key
        self.anthropic_key = anthropic_key

    def get_ai_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get AI-powered insights about the code."""
        try:
            if self.openai_key:
                return self._get_openai_insights(content, issues)
            if self.anthropic_key:
                return self._get_anthropic_insights(content, issues)
        except Exception as exc:  # pragma: no cover - defensive
            logger.warning(f"Failed to get AI insights: {exc}")
        return []

    # ------------------------------------------------------------------
    def _get_openai_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get insights using OpenAI."""
        try:
            import openai

            openai.api_key = self.openai_key
            issue_summary = "\n".join([f"- {i.severity.upper()}: {i.title}" for i in issues[:10]])
            prompt = f"""Analyze this code and provide 3-5 high-level insights:

Code (first 1000 chars):
{content[:1000]}...

Issues found:
{issue_summary}

Provide insights about:
1. Overall code quality
2. Potential improvements
3. Best practices to follow
4. Architecture considerations

Format as a JSON list of strings."""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a senior software architect and code reviewer."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )
            content = response.choices[0].message.content
            try:
                insights = json.loads(content)
                return insights if isinstance(insights, list) else []
            except json.JSONDecodeError:
                return []
        except Exception as exc:  # pragma: no cover - network/keys
            logger.warning(f"OpenAI insights failed: {exc}")
            return []

    # ------------------------------------------------------------------
    def _get_anthropic_insights(self, content: str, issues: List[ReviewIssue]) -> List[str]:
        """Get insights using Anthropic Claude."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.anthropic_key)
            issue_summary = "\n".join([f"- {i.severity.upper()}: {i.title}" for i in issues[:10]])
            prompt = f"""Analyze this code and provide 3-5 high-level insights:

Code (first 1000 chars):
{content[:1000]}...

Issues found:
{issue_summary}

Provide insights about:
1. Overall code quality
2. Potential improvements
3. Best practices to follow
4. Architecture considerations

Format as a JSON list of strings."""

            response = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}],
            )
            content = response.content[0].text
            try:
                insights = json.loads(content)
                return insights if isinstance(insights, list) else []
            except json.JSONDecodeError:
                return []
        except Exception as exc:  # pragma: no cover
            logger.warning(f"Anthropic insights failed: {exc}")
            return []

    def is_configured(self) -> bool:
        """Return True if any AI provider is configured."""
        return bool(self.openai_key or self.anthropic_key)


__all__ = ["AIAnalyzer"]
