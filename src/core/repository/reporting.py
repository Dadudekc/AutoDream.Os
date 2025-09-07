import logging
import time
from datetime import datetime
from typing import Any, Dict, List

from .analysis import AnalysisResult
from .discovery import RepositoryMetadata

logger = logging.getLogger(__name__)


def analyze_repository_performance_patterns(
    repositories: Dict[str, RepositoryMetadata],
    discovery_history: List[Dict[str, Any]],
    analysis_results: List[AnalysisResult],
    max_repositories: int,
    time_range_hours: int = 24,
) -> Dict[str, Any]:
    """Analyze repository system performance patterns."""
    try:
        recent_time = time.time() - (time_range_hours * 3600)
        performance_analysis: Dict[str, Any] = {
            "total_repositories": len(repositories),
            "discovery_performance": {},
            "analysis_performance": {},
            "technology_detection_accuracy": {},
            "optimization_opportunities": [],
        }
        recent_discoveries = [
            d for d in discovery_history if d.get("timestamp", 0) > recent_time
        ]
        if recent_discoveries:
            discovery_times = [d.get("duration", 0) for d in recent_discoveries]
            performance_analysis["discovery_performance"] = {
                "total_discoveries": len(recent_discoveries),
                "average_time": sum(discovery_times) / len(discovery_times),
                "fastest_discovery": min(discovery_times),
                "slowest_discovery": max(discovery_times),
            }
        recent_analyses = [a for a in analysis_results if a.timestamp > recent_time]
        if recent_analyses:
            analysis_times = [a.metadata.get("duration", 0) for a in recent_analyses]
            performance_analysis["analysis_performance"] = {
                "total_analyses": len(recent_analyses),
                "average_time": sum(analysis_times) / len(analysis_times)
                if analysis_times
                else 0,
                "success_rate": len(
                    [a for a in recent_analyses if a.metadata.get("status") == "success"]
                )
                / len(recent_analyses),
            }
        if len(repositories) > max_repositories * 0.8:
            performance_analysis["optimization_opportunities"].append(
                "Repository limit approaching - consider cleanup"
            )
        if (
            recent_discoveries
            and performance_analysis["discovery_performance"].get("average_time", 0) > 30
        ):
            performance_analysis["optimization_opportunities"].append(
                "Slow discovery performance - optimize scanning algorithms"
            )
        logger.info("Repository performance analysis completed")
        return performance_analysis
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to analyze repository performance patterns: {e}")
        return {"error": str(e)}


def generate_repository_report(
    repositories: Dict[str, RepositoryMetadata],
    analysis_results: List[AnalysisResult],
    discovery_history: List[Dict[str, Any]],
    scan_history: List[Dict[str, Any]],
    status: str,
    technology_db_size: int,
    max_repositories: int,
    report_type: str = "comprehensive",
) -> Dict[str, Any]:
    """Generate comprehensive repository system report."""
    try:
        report: Dict[str, Any] = {
            "report_id": f"repository_system_report_{int(time.time())}",
            "generated_at": datetime.now().isoformat(),
            "report_type": report_type,
            "summary": {},
            "detailed_metrics": {},
            "repository_summary": {},
            "recommendations": [],
        }
        total_repos = len(repositories)
        total_analyses = len(analysis_results)
        report["summary"] = {
            "total_repositories": total_repos,
            "total_analyses": total_analyses,
            "total_technologies": technology_db_size,
            "system_status": status,
            "last_discovery": max(
                [d.get("timestamp", 0) for d in discovery_history]
            )
            if discovery_history
            else 0,
        }
        if repositories:
            tech_stack_distribution: Dict[str, int] = {}
            architecture_distribution: Dict[str, int] = {}
            security_score_distribution: Dict[int, int] = {}
            for repo in repositories.values():
                for tech in repo.technology_stack:
                    tech_stack_distribution[tech] = (
                        tech_stack_distribution.get(tech, 0) + 1
                    )
                for arch in repo.architecture_patterns:
                    architecture_distribution[arch] = (
                        architecture_distribution.get(arch, 0) + 1
                    )
                bucket = int(repo.security_score * 10) // 10 * 10
                security_score_distribution[bucket] = (
                    security_score_distribution.get(bucket, 0) + 1
                )
            report["detailed_metrics"] = {
                "technology_distribution": tech_stack_distribution,
                "architecture_distribution": architecture_distribution,
                "security_score_distribution": security_score_distribution,
                "total_discoveries": len(discovery_history),
                "total_scan_operations": len(scan_history),
            }
            recent_repos = sorted(
                repositories.values(),
                key=lambda r: r.discovery_timestamp,
                reverse=True,
            )[:10]
            report["repository_summary"] = {
                "recent_repositories": [
                    {"id": r.repo_id, "name": r.name, "path": r.path}
                    for r in recent_repos
                ],
                "largest_repositories": sorted(
                    repositories.values(),
                    key=lambda r: r.size_bytes,
                    reverse=True,
                )[:5],
                "most_technologies": sorted(
                    repositories.values(),
                    key=lambda r: len(r.technology_stack),
                    reverse=True,
                )[:5],
            }
        performance_analysis = analyze_repository_performance_patterns(
            repositories, discovery_history, analysis_results, max_repositories
        )
        for opportunity in performance_analysis.get("optimization_opportunities", []):
            report["recommendations"].append(opportunity)
        if total_repos > 0:
            if total_repos > max_repositories * 0.8:
                report["recommendations"].append(
                    "Repository limit approaching - consider cleanup"
                )
            if total_analyses / total_repos < 0.5:
                report["recommendations"].append(
                    "Low analysis coverage - consider re-analyzing repositories"
                )
        logger.info(
            f"Repository system report generated: {report['report_id']}"
        )
        return report
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to generate repository system report: {e}")
        return {"error": str(e)}
