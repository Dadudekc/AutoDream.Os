import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a module-level logger configured by logging_config."""
    return logging.getLogger(name if name else __name__)
