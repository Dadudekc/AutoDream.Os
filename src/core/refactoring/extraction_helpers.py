"""
Extraction Helper Functions
===========================

Helper functions for code extraction operations.

Author: Agent-6 (VSCode Forking & Quality Gates Specialist)
License: MIT
"""

import ast
from typing import Any

try:
    import astor
except ImportError:
    astor = None


def extract_models(tree: ast.AST) -> str:
    """Extract model classes from AST."""
    if astor is None:
        return "# astor not available"
    
    models = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            source = astor.to_source(node)
            if any(base in source.lower() for base in ["model", "data", "entity"]):
                models.append(source)

    return "\n".join(models) if models else "# No models found"


def extract_utils(tree: ast.AST) -> str:
    """Extract utility functions from AST."""
    if astor is None:
        return "# astor not available"
    
    utils = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            source = astor.to_source(node)
            if not node.name.startswith("_") and "util" in source.lower():
                utils.append(source)

    return "\n".join(utils) if utils else "# No utilities found"


def extract_core(tree: ast.AST) -> str:
    """Extract core logic from AST."""
    if astor is None:
        return "# astor not available"
    
    core_elements = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef)):
            source = astor.to_source(node)
            if not any(base in source.lower() for base in ["model", "util", "data"]):
                core_elements.append(source)

    return "\n".join(core_elements) if core_elements else "# No core logic found"

