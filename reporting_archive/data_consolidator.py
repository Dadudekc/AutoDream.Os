"""Data consolidation helpers for report generation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Language and complexity statistics


def calculate_language_statistics(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate language distribution statistics for analyzed files."""
    language_counts: Dict[str, int] = {}
    language_lines: Dict[str, int] = {}

    for file_data in files:
        lang = file_data.get("language", "unknown")
        lines = file_data.get("line_count", 0)
        language_counts[lang] = language_counts.get(lang, 0) + 1
        language_lines[lang] = language_lines.get(lang, 0) + lines

    return {
        "file_counts": language_counts,
        "line_counts": language_lines,
        "primary_language": max(language_counts.items(), key=lambda x: x[1])[0]
        if language_counts
        else "unknown",
    }


def calculate_complexity_statistics(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate complexity distribution for analyzed files."""
    complexities = [
        f.get("complexity", 0) for f in files if f.get("complexity") is not None
    ]
    if not complexities:
        return {"average": 0.0, "max": 0, "min": 0, "distribution": {}}

    avg_complexity = sum(complexities) / len(complexities)
    max_complexity = max(complexities)
    min_complexity = min(complexities)

    distribution = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for comp in complexities:
        if comp <= 5:
            distribution["low"] += 1
        elif comp <= 10:
            distribution["medium"] += 1
        elif comp <= 20:
            distribution["high"] += 1
        else:
            distribution["critical"] += 1

    return {
        "average": round(avg_complexity, 2),
        "max": max_complexity,
        "min": min_complexity,
        "distribution": distribution,
    }

# ---------------------------------------------------------------------------
# File analysis helpers


def analyze_files(files: List[Dict[str, Any]], include_details: bool) -> Dict[str, Any]:
    """Analyze individual files for insights such as size and complexity."""
    analysis = {
        "largest_files": [],
        "most_complex_files": [],
        "language_specific_insights": {},
    }
    if not files:
        return analysis

    sorted_by_size = sorted(files, key=lambda x: x.get("line_count", 0), reverse=True)
    sorted_by_complexity = sorted(
        files, key=lambda x: x.get("complexity", 0), reverse=True
    )

    analysis["largest_files"] = [
        {"name": f.get("name", "Unknown"), "lines": f.get("line_count", 0)}
        for f in sorted_by_size[:5]
    ]
    analysis["most_complex_files"] = [
        {"name": f.get("name", "Unknown"), "complexity": f.get("complexity", 0)}
        for f in sorted_by_complexity[:5]
    ]

    if include_details:
        analysis["language_specific_insights"] = generate_language_insights(files)

    return analysis


def generate_language_insights(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate language-specific insights from file metrics."""
    insights: Dict[str, Dict[str, Any]] = {}
    for file_data in files:
        lang = file_data.get("language", "unknown")
        if lang not in insights:
            insights[lang] = {
                "file_count": 0,
                "total_lines": 0,
                "average_complexity": 0.0,
                "complexity_sum": 0.0,
            }
        insights[lang]["file_count"] += 1
        insights[lang]["total_lines"] += file_data.get("line_count", 0)
        insights[lang]["complexity_sum"] += file_data.get("complexity", 0)

    for lang_data in insights.values():
        if lang_data["file_count"] > 0:
            lang_data["average_complexity"] = round(
                lang_data["complexity_sum"] / lang_data["file_count"], 2
            )
    return insights

# ---------------------------------------------------------------------------
# Detailed analysis helpers


def generate_detailed_analysis(project_data: Dict[str, Any]) -> Dict[str, Any]:
    """Generate detailed project analysis including dependencies and metrics."""
    files = project_data.get("files", [])
    return {
        "file_patterns": analyze_file_patterns(files),
        "dependency_analysis": analyze_dependencies(files),
        "code_metrics": calculate_code_metrics(files),
        "recommendations": generate_project_recommendations(files),
    }


def analyze_file_patterns(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze file naming and organization patterns."""
    patterns = {
        "naming_conventions": {},
        "directory_structure": {},
        "file_extensions": {},
    }
    for file_data in files:
        name = file_data.get("name", "")
        if not name:
            continue
        if "_" in name:
            patterns["naming_conventions"]["snake_case"] = (
                patterns["naming_conventions"].get("snake_case", 0) + 1
            )
        elif "-" in name:
            patterns["naming_conventions"]["kebab_case"] = (
                patterns["naming_conventions"].get("kebab_case", 0) + 1
            )
        else:
            patterns["naming_conventions"]["other"] = (
                patterns["naming_conventions"].get("other", 0) + 1
            )
        ext = Path(name).suffix.lower()
        patterns["file_extensions"][ext] = (
            patterns["file_extensions"].get(ext, 0) + 1
        )
    return patterns


def analyze_dependencies(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze dependencies extracted from files."""
    dependencies = {
        "import_counts": {},
        "external_dependencies": set(),
        "internal_dependencies": set(),
    }
    for file_data in files:
        for imp in file_data.get("imports", []):
            if imp.startswith("."):
                dependencies["internal_dependencies"].add(imp)
            else:
                dependencies["external_dependencies"].add(imp)
            dependencies["import_counts"][imp] = (
                dependencies["import_counts"].get(imp, 0) + 1
            )
    dependencies["external_dependencies"] = list(dependencies["external_dependencies"])
    dependencies["internal_dependencies"] = list(dependencies["internal_dependencies"])
    return dependencies


def calculate_code_metrics(files: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate additional code metrics for analyzed files."""
    metrics = {
        "total_functions": 0,
        "total_classes": 0,
        "average_function_length": 0.0,
        "average_class_length": 0.0,
    }
    function_lengths: List[int] = []
    class_lengths: List[int] = []
    for file_data in files:
        if file_data.get("language") == "python":
            metrics["total_functions"] += 1
            metrics["total_classes"] += 1
            function_lengths.append(10)  # Placeholder values
            class_lengths.append(20)
    if function_lengths:
        metrics["average_function_length"] = sum(function_lengths) / len(function_lengths)
    if class_lengths:
        metrics["average_class_length"] = sum(class_lengths) / len(class_lengths)
    return metrics


def generate_project_recommendations(files: List[Dict[str, Any]]) -> List[str]:
    """Generate project-level recommendations based on file metrics."""
    recommendations: List[str] = []
    oversized_files = [f for f in files if f.get("line_count", 0) > 200]
    if oversized_files:
        recommendations.append(
            f"Refactor {len(oversized_files)} oversized files to meet 200 LOC limit"
        )
    files_with_tests = [f for f in files if f.get("has_tests", False)]
    test_coverage = len(files_with_tests) / len(files) * 100 if files else 0
    if test_coverage < 80:
        recommendations.append(
            f"Increase test coverage from {test_coverage:.1f}% to at least 80%"
        )
    high_complexity_files = [f for f in files if f.get("complexity", 0) > 15]
    if high_complexity_files:
        recommendations.append(
            f"Reduce complexity in {len(high_complexity_files)} high-complexity files"
        )
    if not recommendations:
        recommendations.append(
            "Project code quality is excellent - maintain current standards"
        )
    return recommendations

# ---------------------------------------------------------------------------
# Quality metrics and recommendations


def calculate_quality_metrics(analysis_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate overall code quality metrics from analysis data."""
    files = analysis_data.get("files", [])
    if not files:
        return {"overall_score": 0.0}

    total_files = len(files)
    files_with_tests = len([f for f in files if f.get("has_tests", False)])
    files_under_limit = len([f for f in files if f.get("line_count", 0) <= 200])
    low_complexity_files = len([f for f in files if f.get("complexity", 0) <= 10])

    test_coverage_score = (files_with_tests / total_files) * 100 if total_files else 0
    size_compliance_score = (files_under_limit / total_files) * 100 if total_files else 0
    complexity_score = (low_complexity_files / total_files) * 100 if total_files else 0

    overall_score = (
        test_coverage_score * 0.4
        + size_compliance_score * 0.4
        + complexity_score * 0.2
    )

    return {
        "overall_score": round(overall_score, 2),
        "test_coverage_score": round(test_coverage_score, 2),
        "size_compliance_score": round(size_compliance_score, 2),
        "complexity_score": round(complexity_score, 2),
        "metrics": {
            "total_files": total_files,
            "files_with_tests": files_with_tests,
            "files_under_limit": files_under_limit,
            "low_complexity_files": low_complexity_files,
        },
    }


def generate_recommendations(quality_metrics: Dict[str, Any]) -> List[str]:
    """Generate actionable recommendations from quality metrics."""
    recommendations: List[str] = []
    if quality_metrics.get("test_coverage_score", 0) < 80:
        recommendations.append("Increase test coverage to at least 80%")
    if quality_metrics.get("size_compliance_score", 0) < 100:
        recommendations.append("Refactor oversized files to meet 200 LOC limit")
    if quality_metrics.get("complexity_score", 0) < 80:
        recommendations.append("Reduce code complexity in high-complexity files")
    if not recommendations:
        recommendations.append("Code quality is excellent - maintain current standards")
    return recommendations


def identify_priority_actions(quality_metrics: Dict[str, Any]) -> List[str]:
    """Identify high-priority actions for immediate improvement."""
    actions: List[str] = []
    if quality_metrics.get("size_compliance_score", 0) < 90:
        actions.append("URGENT: Refactor oversized files to meet V2 standards")
    if quality_metrics.get("test_coverage_score", 0) < 70:
        actions.append("HIGH: Implement comprehensive test coverage")
    if quality_metrics.get("complexity_score", 0) < 70:
        actions.append("MEDIUM: Reduce code complexity in critical files")
    return actions
