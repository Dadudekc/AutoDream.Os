"""Logging utilities for the unified workspace."""

from __future__ import annotations

import logging
from pathlib import Path


def setup_logger(name: str = "workspace", level: int = logging.INFO) -> logging.Logger:
    """Set up and return a logger with console and file handlers.

    Idempotent: calling multiple times will not duplicate handlers, and will
    ensure a file handler for logs/<name>.log exists.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Ensure console handler exists (stderr/stdout)
    if not any(
        type(h).__name__ == "StreamHandler" and not hasattr(h, "baseFilename")
        for h in logger.handlers
    ):
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    # Ensure file handler exists at logs/<name>.log
    log_dir = Path(__file__).resolve().parents[2] / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    file_path = log_dir / f"{name}.log"
    if not any(
        getattr(h, "baseFilename", None)
        and str(h.baseFilename).lower().endswith(str(file_path).lower())
        for h in logger.handlers
    ):
        file_handler = logging.FileHandler(file_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
