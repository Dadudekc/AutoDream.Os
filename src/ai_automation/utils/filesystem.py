"""
Filesystem Utilities - V2 Compliant
===================================

File system utilities for automation workflows.
Cross-platform file permission handling.

V2 Compliance: Type hints, error handling, documentation.

Original: gpt-automation repository
Ported & Adapted: Agent-7 - Repository Cloning Specialist
License: MIT
"""

import logging
import os
import stat
from pathlib import Path

logger = logging.getLogger(__name__)


def make_executable(path: Path) -> None:
    """
    Make a file executable by adding execute permissions.
    
    Args:
        path: Path to the file to make executable
        
    Raises:
        Exception: On non-Windows systems if chmod fails
        
    Note:
        On Windows, this operation may not have an effect and failures are ignored.
    """
    try:
        # Get current permissions
        mode = path.stat().st_mode
        
        # Add execute permissions for user, group, and others
        new_mode = mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        path.chmod(new_mode)
        
        logger.info(f"Made {path} executable")
        
    except Exception as e:
        # On Windows, execute permissions may not matter - ignore failures
        if os.name != "nt":
            logger.error(f"Failed to make {path} executable: {e}")
            raise
        else:
            logger.debug(f"Ignoring chmod failure on Windows for {path}")

