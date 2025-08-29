"""Coordinate the validation execution workflow."""

from typing import Any, Dict

from .validation_manager import ValidationManager
from .execution import (
    prepare_validation_data,
    run_validations,
    post_process_results,
)


class ValidationExecutor:
    """High-level interface for running the validation pipeline."""

    def __init__(self) -> None:
        self.manager = ValidationManager()

    def run(self, raw_data: Any) -> Dict[str, Any]:
        """Execute the validation workflow for ``raw_data``.

        The process consists of three stages:
        1. preparation of input
        2. execution of all registered validators
        3. post-processing/reporting of results
        """
        prepared = prepare_validation_data(raw_data)
        results = run_validations(self.manager, prepared)
        report = post_process_results(results)
        return {"results": results, "report": report}


__all__ = ["ValidationExecutor"]
