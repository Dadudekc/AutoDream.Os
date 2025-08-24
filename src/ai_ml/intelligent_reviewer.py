#!/usr/bin/env python3
"""Orchestrator for the Intelligent Reviewer system."""

import logging
from datetime import datetime
from pathlib import Path
from typing import Union

from .api_key_manager import get_openai_api_key, get_anthropic_api_key
from .utils import performance_monitor, get_config_manager
from .intelligent_review_core import (
    ReviewIssue,
    CodeReview,
    SecurityVulnerability,
    ReviewCore,
)
from .intelligent_review_ai_analysis import AIAnalyzer
from .intelligent_review_reporting import (
    generate_recommendations,
    calculate_overall_score,
    generate_review_report,
)

logger = logging.getLogger(__name__)


class IntelligentReviewer:
    """High level orchestrator coordinating analysis, AI insights and reporting."""

    def __init__(self) -> None:
        self.config = get_config_manager()
        self.core = ReviewCore()
        self.ai_analyzer = AIAnalyzer(
            openai_key=get_openai_api_key(),
            anthropic_key=get_anthropic_api_key(),
        )

    @performance_monitor("code_review")
    def review_code(self, file_path: Union[str, Path]) -> CodeReview:
        """Perform a comprehensive code review for the given file."""
        file_path = Path(file_path)
        logger.info(f"Reviewing code: {file_path}")
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        review = CodeReview(
            file_path=str(file_path),
            review_date=datetime.now(),
            overall_score=100.0,
        )

        review.issues.extend(self.core.security_analysis(content, file_path))
        review.issues.extend(self.core.quality_analysis(content, file_path))
        review.issues.extend(self.core.style_analysis(content, file_path))
        review.issues.extend(self.core.maintainability_analysis(content, file_path))
        review.issues.extend(self.core.documentation_analysis(content, file_path))

        review.metrics = self.core.calculate_metrics(content, review.issues)
        review.ai_insights = self.ai_analyzer.get_ai_insights(content, review.issues)
        review.recommendations = generate_recommendations(review.issues, review.metrics)
        review.overall_score = calculate_overall_score(review.issues, review.metrics)
        return review

    def generate_review_report(self, review: CodeReview) -> str:
        """Generate a formatted review report."""
        return generate_review_report(review)

    def is_configured(self) -> bool:
        """Check if any AI provider is configured."""
        return self.ai_analyzer.is_configured()


def get_intelligent_reviewer() -> "IntelligentReviewer":
    """Return a global IntelligentReviewer instance."""
    if not hasattr(get_intelligent_reviewer, "_instance"):
        get_intelligent_reviewer._instance = IntelligentReviewer()
    return get_intelligent_reviewer._instance


__all__ = [
    "IntelligentReviewer",
    "ReviewIssue",
    "CodeReview",
    "SecurityVulnerability",
    "get_intelligent_reviewer",
]


if __name__ == "__main__":  # pragma: no cover
    reviewer = get_intelligent_reviewer()
    if reviewer.is_configured():
        print("✅ Intelligent Reviewer is configured and ready!")
    else:
        print("❌ Intelligent Reviewer not configured. Please set up API keys.")
