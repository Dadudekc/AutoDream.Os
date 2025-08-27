"""Tests for the refactored modular CodeCrafter engine."""

from pathlib import Path

import pytest

import importlib.util
import sys


# Load modules without triggering heavy package imports
def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module

models = _load("code_crafter_models", Path("src/ai_ml/code_crafter_models.py"))
template_generation = _load("template_generation", Path("src/ai_ml/template_generation.py"))
code_synthesis = _load("code_synthesis", Path("src/ai_ml/code_synthesis.py"))
validation = _load("validation", Path("src/ai_ml/validation.py"))
deployment = _load("deployment", Path("src/ai_ml/deployment.py"))
code_crafter = _load("code_crafter", Path("src/ai_ml/code_crafter.py"))

CodeCrafter = code_crafter.CodeCrafter
CodeGenerationRequest = models.CodeGenerationRequest
CodeSynthesizer = code_synthesis.CodeSynthesizer


def test_end_to_end_generation(tmp_path: Path) -> None:
    """The engine should orchestrate all modules to produce code."""

    request = CodeGenerationRequest(
        description="return the number forty two", language="python"
    )
    destination = tmp_path / "generated.py"

    crafter = CodeCrafter()
    result = crafter.generate_code(request, destination)

    # Code is returned and written to disk
    assert "generated_function" in result.code
    assert destination.exists()
    assert destination.read_text() == result.code


def test_validation_failure(tmp_path: Path) -> None:
    """Custom synthesizers producing invalid code should raise errors."""

    class BadSynthesizer(CodeSynthesizer):
        def synthesize_code(self, template: str) -> str:  # pragma: no cover - test
            return "print('no function here')"  # Missing function definition

    request = CodeGenerationRequest(description="whatever", language="python")
    crafter = CodeCrafter(synthesizer=BadSynthesizer())

    with pytest.raises(ValueError):
        crafter.generate_code(request, tmp_path / "out.py")

