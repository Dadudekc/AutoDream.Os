"""Cleanup helpers for validation finalization."""
import logging
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)


def cleanup(paths: Iterable[Path]) -> None:
    """Remove temporary files produced during finalization."""
    for path in paths:
        try:
            if path.exists():
                path.unlink()
                logger.debug("Removed %s", path)
        except OSError as exc:  # pragma: no cover - best effort
            logger.warning("Failed to remove %s: %s", path, exc)
