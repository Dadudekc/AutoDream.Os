"""Post-processing and reporting utilities for validation execution."""

from typing import Any, Dict, List

from ..base_validator import ValidationResult
from ..validation_reporting import generate_validation_report


def post_process_results(results: Dict[str, List[ValidationResult]]) -> Dict[str, Any]:
    """Aggregate raw validation results into a summary report."""
    flattened: List[ValidationResult] = []
    for res in results.values():
        flattened.extend(res)
    return generate_validation_report(flattened)
