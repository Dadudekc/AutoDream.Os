"""Error-rate measurement utilities."""
from typing import Union

Number = Union[int, float]


def calculate_error_rate(errors: Number, total_operations: Number) -> float:
    """Return the error rate as a floating point ratio.

    Returns 0.0 when *total_operations* is zero to avoid division errors.
    """
    if total_operations == 0:
        return 0.0
    return float(errors) / float(total_operations)
