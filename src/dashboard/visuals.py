"""Visualization helpers for health metrics."""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt

from ..constants import HEALTH_CHARTS_DIR


def plot_status_distribution(
    counts: Dict[str, int], *, directory: Path | None = None
) -> Path:
    """Create a bar chart for agent status distribution.

    Args:
        counts: Mapping of status labels to occurrence counts.
        directory: Optional override for output directory.

    Returns:
        Path to the saved chart image.
    """
    output_dir = directory or HEALTH_CHARTS_DIR
    output_dir.mkdir(exist_ok=True)

    labels = list(counts.keys())
    values = list(counts.values())

    plt.figure()
    plt.bar(labels, values)
    plt.title("Agent Status Distribution")
    plt.xlabel("Status")
    plt.ylabel("Count")

    output_path = output_dir / "status_distribution.png"
    plt.savefig(output_path)
    plt.close()
    return output_path
