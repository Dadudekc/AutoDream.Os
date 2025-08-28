"""Throughput measurement utilities."""

from typing import Union

Number = Union[int, float]


def calculate_throughput(total_work: Number, duration_seconds: Number) -> float:  # noqa: E501
    """Calculate throughput as work per second.

    Returns 0.0 when *duration_seconds* is zero to avoid division errors.
    """
    if duration_seconds == 0:
        return 0.0
    return float(total_work) / float(duration_seconds)
