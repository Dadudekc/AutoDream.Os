import logging
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Any, Optional

from .discovery import RepositoryMetadata

logger = logging.getLogger(__name__)


class TechnologyType(Enum):
    """Technology type enumeration."""
    PROGRAMMING_LANGUAGE = "programming_language"
    FRAMEWORK = "framework"
    DATABASE = "database"
    TOOL = "tool"
    SERVICE = "service"


@dataclass
class TechnologyStack:
    """Technology stack information."""
    name: str
    version: str
    type: TechnologyType
    confidence: float
    detection_method: str
    metadata: Dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class AnalysisResult:
    """Repository analysis result."""
    repo_id: str
    analysis_id: str
    timestamp: float
    technology_stack: List[TechnologyStack]
    architecture_patterns: List[str]
    security_assessment: Dict[str, Any]
    performance_metrics: Dict[str, Any]
    recommendations: List[str]
    metadata: Dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


def detect_technologies(path: str) -> List[TechnologyStack]:
    """Detect technologies in repository."""
    try:
        technologies: List[TechnologyStack] = []
        repo_path = Path(path)
        tech_patterns: Dict[str, List[str]] = {
            "Python": [".py", "requirements.txt", "setup.py", "Pipfile"],
            "JavaScript": [".js", ".ts", "package.json", "yarn.lock"],
            "Java": [".java", "pom.xml", "build.gradle"],
            "C++": [".cpp", ".h", "CMakeLists.txt"],
        }
        for name, patterns in tech_patterns.items():
            for pattern in patterns:
                if pattern.startswith('.'):
                    if any(repo_path.rglob(f"*{pattern}")):
                        technologies.append(
                            TechnologyStack(
                                name=name,
                                version="unknown",
                                type=TechnologyType.PROGRAMMING_LANGUAGE,
                                confidence=0.8,
                                detection_method="pattern_match",
                            )
                        )
                        break
                elif (repo_path / pattern).exists():
                    technologies.append(
                        TechnologyStack(
                            name=name,
                            version="unknown",
                            type=TechnologyType.PROGRAMMING_LANGUAGE,
                            confidence=0.9,
                            detection_method="file_presence",
                        )
                    )
                    break
        return technologies
    except Exception:  # pragma: no cover - defensive
        return []


def detect_architecture_patterns(path: str) -> List[str]:
    """Detect basic architecture patterns."""
    try:
        patterns: List[str] = []
        repo_path = Path(path)
        if (repo_path / "src").exists() and (repo_path / "tests").exists():
            patterns.append("src_tests_separation")
        if (repo_path / "config").exists():
            patterns.append("config_directory")
        return patterns
    except Exception:  # pragma: no cover - defensive
        return []


def calculate_security_score(path: str, technologies: List[TechnologyStack]) -> float:
    """Calculate basic security score."""
    try:
        repo_path = Path(path)
        score = 0.5
        if (repo_path / "SECURITY.md").exists():
            score += 0.2
        if (repo_path / ".git").exists():
            score += 0.2
        if any(t.name == "Python" for t in technologies):
            score += 0.1
        return min(1.0, score)
    except Exception:  # pragma: no cover
        return 0.5


def generate_performance_metrics(path: str) -> Dict[str, Any]:
    """Generate basic performance metrics for repository."""
    try:
        repo_path = Path(path)
        return {
            "file_count": len(list(repo_path.rglob("*"))),
            "total_size_mb": sum(
                f.stat().st_size for f in repo_path.rglob("*") if f.is_file()
            )
            / (1024 * 1024),
            "complexity_score": 0.5,
        }
    except Exception:  # pragma: no cover
        return {}


def generate_recommendations(
    technologies: List[TechnologyStack], patterns: List[str]
) -> List[str]:
    """Generate recommendations based on analysis."""
    recommendations: List[str] = []
    if len(technologies) > 5:
        recommendations.append("Consider reducing technology stack complexity")
    if not patterns:
        recommendations.append("Consider implementing clear architecture patterns")
    return recommendations


def analyze_repository(
    repo_id: str,
    repositories: Dict[str, RepositoryMetadata],
    analysis_results: List[AnalysisResult],
    discovery_history: List[Dict[str, Any]],
) -> Optional[str]:
    """Analyze a discovered repository."""
    try:
        if repo_id not in repositories:
            logger.error(f"Repository not found: {repo_id}")
            return None
        repo = repositories[repo_id]
        start_time = time.time()
        technology_stack = detect_technologies(repo.path)
        repo.technology_stack = [tech.name for tech in technology_stack]
        architecture_patterns = detect_architecture_patterns(repo.path)
        repo.architecture_patterns = architecture_patterns
        security_score = calculate_security_score(repo.path, technology_stack)
        repo.security_score = security_score
        performance_metrics = generate_performance_metrics(repo.path)
        repo.performance_metrics = performance_metrics
        repo.analysis_status = "analyzed"
        analysis_result = AnalysisResult(
            repo_id=repo_id,
            analysis_id=f"analysis_{int(time.time())}",
            timestamp=time.time(),
            technology_stack=technology_stack,
            architecture_patterns=architecture_patterns,
            security_assessment={"score": security_score, "details": {}},
            performance_metrics=performance_metrics,
            recommendations=generate_recommendations(technology_stack, architecture_patterns),
            metadata={"duration": time.time() - start_time, "status": "success"},
        )
        analysis_results.append(analysis_result)
        for record in discovery_history:
            if record.get("repo_id") == repo_id:
                record["duration"] = time.time() - start_time
                record["status"] = "analyzed"
                break
        logger.info(f"Repository analysis completed: {repo_id}")
        return analysis_result.analysis_id
    except Exception as e:  # pragma: no cover
        logger.error(f"Failed to analyze repository {repo_id}: {e}")
        return None
