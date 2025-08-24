"""High level orchestration for the modular CodeCrafter system.

This module wires together separate components responsible for template
generation, code synthesis, validation and deployment.  The original project
implemented all these responsibilities in a single monolithic file; the
refactored design keeps the public surface area small while enabling focused
unit testing.
"""

from pathlib import Path
from typing import Optional

try:  # pragma: no cover - import flexibility for tests
    from .code_crafter_models import (
        CodeAnalysis,
        CodeGenerationRequest,
        CodeGenerationResult,
    )
    from .template_generation import TemplateGenerator
    from .code_synthesis import CodeSynthesizer
    from .validation import CodeValidator
    from .deployment import CodeDeployer
except ImportError:  # pragma: no cover - fallback when loaded outside package
    from code_crafter_models import (
        CodeAnalysis,
        CodeGenerationRequest,
        CodeGenerationResult,
    )
    from template_generation import TemplateGenerator
    from code_synthesis import CodeSynthesizer
    from validation import CodeValidator
    from deployment import CodeDeployer


class CodeCrafter:
    """Coordinate template generation, synthesis, validation and deployment."""

    def __init__(
        self,
        template_generator: Optional[TemplateGenerator] = None,
        synthesizer: Optional[CodeSynthesizer] = None,
        validator: Optional[CodeValidator] = None,
        deployer: Optional[CodeDeployer] = None,
    ) -> None:
        self.template_generator = template_generator or TemplateGenerator()
        self.synthesizer = synthesizer or CodeSynthesizer()
        self.validator = validator or CodeValidator()
        self.deployer = deployer or CodeDeployer()

    def generate_code(
        self, request: CodeGenerationRequest, destination: Optional[Path] = None
    ) -> CodeGenerationResult:
        """Generate, validate and optionally persist source code."""

        template = self.template_generator.build_template(request)
        code = self.synthesizer.synthesize_code(template)
        self.validator.validate(code)
        path = self.deployer.deploy(code, destination) if destination else None
        return CodeGenerationResult(code=code, path=path)

    # ------------------------------------------------------------------
    # Compatibility helpers
    # ------------------------------------------------------------------
    def generate_tests(self, _code_path: str) -> str:  # pragma: no cover - trivial
        """Return a tiny placeholder test suite."""

        return "def test_placeholder():\n    assert True\n"

    def analyze_code(self, file_path: str) -> CodeAnalysis:
        """Perform extremely light analysis on *file_path*.

        The analysis simply counts the number of lines to provide a numeric
        complexity score.  This keeps the method fast and deterministic while
        satisfying consumers expecting a :class:`CodeAnalysis` instance.
        """

        content = Path(file_path).read_text(encoding="utf-8")
        complexity = float(content.count("\n"))
        return CodeAnalysis(
            file_path=file_path,
            complexity_score=complexity,
            maintainability_index=100.0,
        )


def get_code_crafter() -> CodeCrafter:
    """Return a lazily instantiated :class:`CodeCrafter` singleton."""

    if not hasattr(get_code_crafter, "_instance"):
        get_code_crafter._instance = CodeCrafter()
    return get_code_crafter._instance


__all__ = [
    "CodeCrafter",
    "CodeGenerationRequest",
    "CodeGenerationResult",
    "CodeAnalysis",
    "get_code_crafter",
]

