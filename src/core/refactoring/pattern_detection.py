from dataclasses import dataclass
from typing import List

from src.services.unified_messaging_imports import get_unified_utility


@dataclass
class ArchitecturePattern:
    """Represents an identified architecture pattern."""

    name: str
    pattern_type: str
    files: List[str]
    confidence: float
    description: str


def analyze_architecture_patterns(directory: str) -> List[ArchitecturePattern]:
    """Analyze architecture patterns in a directory."""
    patterns = []
    patterns.extend(_detect_mvc_patterns(directory))
    patterns.extend(_detect_repository_patterns(directory))
    patterns.extend(_detect_factory_patterns(directory))
    patterns.extend(_detect_observer_patterns(directory))
    patterns.extend(_detect_singleton_patterns(directory))
    return patterns


def _detect_mvc_patterns(directory: str) -> List[ArchitecturePattern]:
    patterns = []
    mvc_files = []
    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                if any(keyword in content for keyword in ["model", "view", "controller"]):
                    mvc_files.append(str(file_path))
            except Exception:
                continue
    if mvc_files:
        patterns.append(
            ArchitecturePattern(
                name="MVC Pattern",
                pattern_type="architectural",
                files=mvc_files,
                confidence=0.7,
                description="Model-View-Controller architecture pattern detected",
            )
        )
    return patterns


def _detect_repository_patterns(directory: str) -> List[ArchitecturePattern]:
    patterns = []
    repo_files = []
    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                if "repository" in content and "class" in content:
                    repo_files.append(str(file_path))
            except Exception:
                continue
    if repo_files:
        patterns.append(
            ArchitecturePattern(
                name="Repository Pattern",
                pattern_type="design",
                files=repo_files,
                confidence=0.8,
                description="Repository pattern implementation detected",
            )
        )
    return patterns


def _detect_factory_patterns(directory: str) -> List[ArchitecturePattern]:
    patterns = []
    factory_files = []
    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                if "factory" in content and "create" in content:
                    factory_files.append(str(file_path))
            except Exception:
                continue
    if factory_files:
        patterns.append(
            ArchitecturePattern(
                name="Factory Pattern",
                pattern_type="creational",
                files=factory_files,
                confidence=0.6,
                description="Factory pattern implementation detected",
            )
        )
    return patterns


def _detect_observer_patterns(directory: str) -> List[ArchitecturePattern]:
    patterns = []
    observer_files = []
    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                if any(keyword in content for keyword in ["observer", "subscribe", "notify"]):
                    observer_files.append(str(file_path))
            except Exception:
                continue
    if observer_files:
        patterns.append(
            ArchitecturePattern(
                name="Observer Pattern",
                pattern_type="behavioral",
                files=observer_files,
                confidence=0.7,
                description="Observer pattern implementation detected",
            )
        )
    return patterns


def _detect_singleton_patterns(directory: str) -> List[ArchitecturePattern]:
    patterns = []
    singleton_files = []
    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()
                if "instance" in content and "get_instance" in content:
                    singleton_files.append(str(file_path))
            except Exception:
                continue
    if singleton_files:
        patterns.append(
            ArchitecturePattern(
                name="Singleton Pattern",
                pattern_type="creational",
                files=singleton_files,
                confidence=0.8,
                description="Singleton pattern implementation detected",
            )
        )
    return patterns
