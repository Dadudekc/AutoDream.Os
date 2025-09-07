import ast
from dataclasses import dataclass
from typing import List

from src.core.validation.unified_validation_orchestrator import (
    get_unified_validator,
)


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


def analyze_file_for_extraction(file_path: str) -> FileAnalysis:
    """Analyze a file for extraction opportunities."""
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
    except Exception:
        return FileAnalysis(
            file_path=file_path,
            line_count=0,
            classes=[],
            functions=[],
            imports=[],
            complexity_score=0.0,
            v2_compliance=False,
        )


def _calculate_complexity(tree: ast.AST) -> float:
    """Calculate cyclomatic complexity of an AST."""
    complexity = 1
    for node in ast.walk(tree):
        if get_unified_validator().validate_type(node, (ast.If, ast.While, ast.For, ast.AsyncFor)):
            complexity += 1
        elif get_unified_validator().validate_type(node, ast.ExceptHandler):
            complexity += 1
        elif get_unified_validator().validate_type(node, ast.BoolOp):
            complexity += len(node.values) - 1
    return complexity
