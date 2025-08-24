"""Validation helpers for V2 standards checker.

This module focuses on analysing individual files. Each function returns a
boolean indicating whether a particular standard is satisfied. A
high-level :func:`validate_file` combines these checks for convenience.
"""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Dict


def _read_file(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def count_loc(file_path: Path) -> int:
    """Count non-empty, non-comment lines of code."""
    text = _read_file(file_path)
    return sum(1 for line in text.splitlines() if line.strip() and not line.strip().startswith("#"))


def check_oop(content: str) -> bool:
    """Ensure classes are present and free functions are minimal."""
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return False

    has_class = any(isinstance(n, ast.ClassDef) for n in ast.walk(tree))
    if not has_class:
        return False

    free_funcs = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            parents = [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef)]
            in_class = any(
                getattr(node, "lineno", 0) >= getattr(cls, "lineno", 0)
                and getattr(node, "end_lineno", 0) <= getattr(cls, "end_lineno", 0)
                for cls in parents
            )
            if not in_class:
                free_funcs += 1
    return free_funcs <= 2


def check_cli(content: str) -> bool:
    """Verify argparse usage when a CLI entry point exists."""
    has_main = "if __name__" in content or "def main(" in content
    if not has_main:
        return True
    return "argparse" in content or "ArgumentParser" in content


def check_srp(content: str) -> bool:
    """Heuristic single responsibility check based on operation counts."""
    operations = {
        "file_ops": content.count("open(") + content.count("Path("),
        "network_ops": content.count("requests.") + content.count("urllib."),
        "db_ops": content.count("sqlite") + content.count("database"),
        "gui_ops": content.count("tkinter") + content.count("PyQt"),
        "cli_ops": content.count("argparse") + content.count("click"),
    }
    return sum(1 for c in operations.values() if c) <= 2


def validate_file(file_path: Path, max_loc: int) -> Dict[str, bool]:
    """Validate a file against all standards."""
    try:
        content = _read_file(file_path)
    except OSError:
        return {
            "loc": False,
            "oop": False,
            "cli": False,
            "srp": False,
        }

    return {
        "loc": count_loc(file_path) <= max_loc,
        "oop": check_oop(content),
        "cli": check_cli(content),
        "srp": check_srp(content),
    }
