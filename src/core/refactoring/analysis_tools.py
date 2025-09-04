
#!/usr/bin/env python3
"""
Architecture Analysis Tools - V2 Compliance Implementation

This module provides V2-compliant architecture analysis tools for the refactoring system.
Implements architecture pattern detection, file analysis, and duplicate identification.

Agent: Agent-2 (Architecture & Design Specialist)
Mission: Architecture & Design V2 Compliance Implementation
Status: V2_COMPLIANT_IMPLEMENTATION
"""



@dataclass
class ArchitecturePattern:
    """Represents an identified architecture pattern."""

    name: str
    pattern_type: str
    files: List[str]
    confidence: float
    description: str


@dataclass
class FileAnalysis:
    """Analysis results for a single file."""

    file_path: str
    line_count: int
    classes: List[str]
    functions: List[str]
    imports: List[str]
    complexity_score: float
    v2_compliance: bool


@dataclass
class DuplicateFile:
    """Represents duplicate file information."""

    original_file: str
    duplicate_files: List[str]
    similarity_score: float
    duplicate_type: str


def analyze_file_for_extraction(file_path: str) -> FileAnalysis:
    """
    Analyze a file for extraction opportunities.

    Args:
        file_path: Path to the file to analyze

    Returns:
        FileAnalysis object with detailed analysis results
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        tree = ast.parse(content)

        classes = [
            node.name for node in ast.walk(tree) if get_unified_validator().validate_type(node, ast.ClassDef)
        ]
        functions = [
            node.name for node in ast.walk(tree) if get_unified_validator().validate_type(node, ast.FunctionDef)
        ]
        imports = [
            node.module for node in ast.walk(tree) if get_unified_validator().validate_type(node, ast.Import)
        ]
        imports.extend(
            [
                f"{node.module}.{node.names[0].name}"
                for node in ast.walk(tree)
                if get_unified_validator().validate_type(node, ast.ImportFrom) and node.module
            ]
        )

        line_count = len(content.splitlines())
        complexity_score = _calculate_complexity(tree)
        v2_compliance = line_count <= 400

        return FileAnalysis(
            file_path=file_path,
            line_count=line_count,
            classes=classes,
            functions=functions,
            imports=imports,
            complexity_score=complexity_score,
            v2_compliance=v2_compliance,
        )
    except Exception as e:
        return FileAnalysis(
            file_path=file_path,
            line_count=0,
            classes=[],
            functions=[],
            imports=[],
            complexity_score=0.0,
            v2_compliance=False,
        )


def find_duplicate_files(
    directory: str, similarity_threshold: float = 0.8
) -> List[DuplicateFile]:
    """
    Find duplicate files in a directory.

    Args:
        directory: Directory to search for duplicates
        similarity_threshold: Minimum similarity score to consider files duplicates

    Returns:
        List of DuplicateFile objects
    """
    duplicates = []
    file_hashes = defaultdict(list)

    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Create hash based on normalized content
                normalized_content = _get_unified_utility().normalize_content(content)
                content_hash = hashlib.md5(normalized_content.encode()).hexdigest()
                file_hashes[content_hash].append(str(file_path))

            except Exception:
                continue

    for content_hash, files in file_hashes.items():
        if len(files) > 1:
            duplicates.append(
                DuplicateFile(
                    original_file=files[0],
                    duplicate_files=files[1:],
                    similarity_score=1.0,
                    duplicate_type="exact",
                )
            )

    return duplicates


def analyze_architecture_patterns(directory: str) -> List[ArchitecturePattern]:
    """
    Analyze architecture patterns in a directory.

    Args:
        directory: Directory to analyze for architecture patterns

    Returns:
        List of identified ArchitecturePattern objects
    """
    patterns = []

    # Pattern detection logic
    patterns.extend(_detect_mvc_patterns(directory))
    patterns.extend(_detect_repository_patterns(directory))
    patterns.extend(_detect_factory_patterns(directory))
    patterns.extend(_detect_observer_patterns(directory))
    patterns.extend(_detect_singleton_patterns(directory))

    return patterns


def _calculate_complexity(tree: ast.AST) -> float:
    """Calculate cyclomatic complexity of an AST."""
    complexity = 1  # Base complexity

    for node in ast.walk(tree):
        if get_unified_validator().validate_type(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif get_unified_validator().validate_type(node, ast.ExceptHandler):
            complexity += 1
        elif get_unified_validator().validate_type(node, ast.BoolOp):
            complexity += len(node.values) - 1

    return complexity


def _get_unified_utility().normalize_content(content: str) -> str:
    """Normalize content for duplicate detection."""
    # Remove comments and docstrings
    lines = content.split("\n")
    normalized_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and not stripped.startswith('"""'):
            normalized_lines.append(stripped)

    return "\n".join(normalized_lines)


def _detect_mvc_patterns(directory: str) -> List[ArchitecturePattern]:
    """Detect MVC architecture patterns."""
    patterns = []
    mvc_files = []

    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()

                if any(
                    keyword in content for keyword in ["model", "view", "controller"]
                ):
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
    """Detect Repository pattern implementations."""
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
    """Detect Factory pattern implementations."""
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
    """Detect Observer pattern implementations."""
    patterns = []
    observer_files = []

    for file_path in get_unified_utility().Path(directory).rglob("*.py"):
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()

                if any(
                    keyword in content
                    for keyword in ["observer", "subscribe", "notify"]
                ):
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
    """Detect Singleton pattern implementations."""
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
