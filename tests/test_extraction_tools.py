"""Tests for AST-based extraction utilities."""

import ast
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from core.refactoring.tools.extraction_tools import (
    ExtractionTools,
    NO_CORE,
    NO_MODELS,
    NO_UTILS,
)


def test_extract_models_utils_core():
    """Models, utilities, and core logic are separated correctly."""

    source = (
        "class UserModel:\n"
        "    pass\n\n"
        "class HelperClass:\n"
        "    pass\n\n"
        "def util_function():\n"
        "    return 1\n\n"
        "def core_logic():\n"
        "    return 2\n"
    )
    tree = ast.parse(source)
    tools = ExtractionTools()

    models = tools._extract_models(tree)
    utils = tools._extract_utils(tree)
    core = tools._extract_core(tree)

    assert "class UserModel" in models
    assert "def util_function" in utils
    assert "class HelperClass" in core
    assert "def core_logic" in core
    assert "class UserModel" not in core
    assert "def util_function" not in core


def test_extract_handles_absence():
    """Missing categories yield placeholder comments."""

    tree = ast.parse("def only_core():\n    pass\n")
    tools = ExtractionTools()

    assert tools._extract_models(tree) == NO_MODELS
    assert tools._extract_utils(tree) == NO_UTILS
    assert "def only_core" in tools._extract_core(tree)


def test_extract_core_absence():
    """Only models and utilities yield core placeholder."""

    source = (
        "class UserModel:\n    pass\n\n"
        "def util_function():\n    return 1\n"
    )
    tree = ast.parse(source)
    tools = ExtractionTools()

    assert "class UserModel" in tools._extract_models(tree)
    assert "def util_function" in tools._extract_utils(tree)
    assert tools._extract_core(tree) == NO_CORE

