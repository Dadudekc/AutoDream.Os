import logging
from pathlib import Path
from typing import Optional


def logger_setup(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    log_format: Optional[str] = None,
) -> logging.Logger:
    """Setup logging configuration."""
    if log_format is None:
        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    formatter = logging.Formatter(log_format)
    logger_instance = logging.getLogger("ai_ml")
    logger_instance.setLevel(getattr(logging, log_level.upper()))
    logger_instance.handlers.clear()
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    logger_instance.addHandler(console_handler)
    if log_file:
        try:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            logger_instance.addHandler(file_handler)
        except Exception:  # pragma: no cover - filesystem path
            logger_instance.warning("Could not setup file logging")
    return logger_instance
