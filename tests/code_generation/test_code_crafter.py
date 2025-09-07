"""Orchestrator for the modular CodeCrafter test suite.

This file re-exports the main test classes so legacy imports of
``tests.code_generation.test_code_crafter`` continue to function. Each test class
is defined in its own module focusing on a single concern:

* ``test_code_crafter_models`` – dataclass validations
* ``test_code_crafter_generation`` – code generation workflow
* ``test_code_crafter_validation`` – analysis and helper methods
* ``test_code_crafter_integration`` – end-to-end scenarios
"""

from .code_crafter_support import (
    CodeAnalysis,
    CodeGenerationRequest,
    CodeGenerationResult,
    CodeCrafter,
)
from .test_code_crafter_models import *  # noqa: F401,F403
from .test_code_crafter_generation import *  # noqa: F401,F403
from .test_code_crafter_validation import *  # noqa: F401,F403
from .test_code_crafter_integration import *  # noqa: F401,F403

__all__ = [
    "CodeAnalysis",
    "CodeGenerationRequest",
    "CodeGenerationResult",
    "CodeCrafter",
]
