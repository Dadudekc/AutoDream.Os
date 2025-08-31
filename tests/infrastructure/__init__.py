"""Core infrastructure for testing pipeline."""

from .setup import prepare_tests
from .executor import run_tests
from .teardown import perform_teardown

__all__ = ["prepare_tests", "run_tests", "perform_teardown"]
