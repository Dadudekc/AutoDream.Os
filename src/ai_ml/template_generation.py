"""Template generation component for CodeCrafter.

The generator transforms a :class:`CodeGenerationRequest` into a textual
template that will later be consumed by the synthesis step.  The goal is to
keep this module intentionally lightweight so it can be easily extended in
the future.
"""

try:  # pragma: no cover - allow direct execution
    from .code_crafter_models import CodeGenerationRequest
except ImportError:  # pragma: no cover
    from code_crafter_models import CodeGenerationRequest


class TemplateGenerator:
    """Create textual templates from generation requests."""

    def build_template(self, request: CodeGenerationRequest) -> str:
        """Return a simple template representing the user's request."""

        return (
            f"Generate {request.language} code for: {request.description}"
        )

