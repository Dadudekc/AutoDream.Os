"""Reporting utilities for the Intelligent Reviewer."""

from typing import Any, Dict, List

from .intelligent_review_core import CodeReview, ReviewIssue


def generate_recommendations(issues: List[ReviewIssue], metrics: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations."""
    recommendations: List[str] = []

    security_issues = [i for i in issues if i.category == "security"]
    if security_issues:
        recommendations.append(
            "Address security vulnerabilities immediately, especially high-severity ones"
        )

    if metrics.get("complexity_score", 0) > 10:
        recommendations.append(
            "Reduce cyclomatic complexity by breaking down complex functions"
        )

    if metrics.get("comment_ratio", 0) < 0.1:
        recommendations.append(
            "Add more documentation and comments to improve code readability"
        )

    severity_counts: Dict[str, int] = {}
    for issue in issues:
        severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1

    if severity_counts.get("critical", 0) > 0:
        recommendations.append("Fix critical issues first as they pose immediate risks")

    if severity_counts.get("high", 0) > 5:
        recommendations.append("High number of high-severity issues - consider code refactoring")

    if not recommendations:
        recommendations.append("Code quality is good! Keep up the good practices.")

    return recommendations


def calculate_overall_score(issues: List[ReviewIssue], metrics: Dict[str, Any]) -> float:
    """Calculate overall code quality score."""
    base_score = 100.0
    severity_penalties = {
        "critical": 20,
        "high": 10,
        "medium": 5,
        "low": 2,
        "info": 1,
    }

    for issue in issues:
        base_score -= severity_penalties.get(issue.severity, 0)

    complexity = metrics.get("complexity_score", 0)
    if complexity > 20:
        base_score -= 20
    elif complexity > 10:
        base_score -= 10
    elif complexity > 5:
        base_score -= 5

    comment_ratio = metrics.get("comment_ratio", 0)
    if comment_ratio < 0.05:
        base_score -= 10
    elif comment_ratio < 0.1:
        base_score -= 5

    return max(0.0, base_score)


def generate_review_report(review: CodeReview) -> str:
    """Generate a comprehensive review report."""
    report = f"# Code Review Report\n\n"
    report += f"**File:** {review.file_path}\n"
    report += f"**Date:** {review.review_date.strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Overall Score:** {review.overall_score:.1f}/100\n\n"

    report += "## 📊 Summary\n\n"
    report += f"- **Total Issues:** {len(review.issues)}\n"
    report += f"- **Security Issues:** {len([i for i in review.issues if i.category == 'security'])}\n"
    report += f"- **Quality Issues:** {len([i for i in review.issues if i.category in ['maintainability', 'style']])}\n"
    report += f"- **Documentation Issues:** {len([i for i in review.issues if i.category == 'documentation'])}\n\n"

    critical_issues = [i for i in review.issues if i.severity == "critical"]
    if critical_issues:
        report += "## 🚨 Critical Issues\n\n"
        for issue in critical_issues:
            report += f"### {issue.title}\n"
            report += f"**Description:** {issue.description}\n"
            if issue.line_number:
                report += f"**Line:** {issue.line_number}\n"
            if issue.suggestion:
                report += f"**Suggestion:** {issue.suggestion}\n"
            report += "\n"

    high_issues = [i for i in review.issues if i.severity == "high"]
    if high_issues:
        report += "## ⚠️ High Priority Issues\n\n"
        for issue in high_issues:
            report += f"### {issue.title}\n"
            report += f"**Description:** {issue.description}\n"
            if issue.line_number:
                report += f"**Line:** {issue.line_number}\n"
            if issue.suggestion:
                report += f"**Suggestion:** {issue.suggestion}\n"
            report += "\n"

    if review.ai_insights:
        report += "## 🤖 AI Insights\n\n"
        for insight in review.ai_insights:
            report += f"- {insight}\n"
        report += "\n"

    if review.recommendations:
        report += "## 💡 Recommendations\n\n"
        for rec in review.recommendations:
            report += f"- {rec}\n"
        report += "\n"

    report += "## 📈 Metrics\n\n"
    for key, value in review.metrics.items():
        if isinstance(value, float):
            report += f"- **{key.replace('_', ' ').title()}:** {value:.2f}\n"
        else:
            report += f"- **{key.replace('_', ' ').title()}:** {value}\n"

    return report


__all__ = [
    "generate_recommendations",
    "calculate_overall_score",
    "generate_review_report",
]
