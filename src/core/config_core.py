#!/usr/bin/env python3
"""
DEPRECATED: This file has been replaced by src/core/config/config_manager.py
=============================================================================

This file is DEPRECATED as part of DUP-001 ConfigManager SSOT consolidation.

CONSOLIDATION: Agent-8 (2025-10-16) - DUP-001 SSOT Fix
All functionality has been moved to src/core/config/config_manager.py

Please update your imports to use src/core/config_ssot instead:

OLD:
    from src.core.config_core import get_config, UnifiedConfigManager

NEW:
    from src.core.config_ssot import get_config, UnifiedConfigManager

This file will be removed in a future release.
"""

import warnings

warnings.warn(
    "config_core.py is deprecated. Use src.core.config_ssot instead. "
    "This file will be removed in a future release.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export from SSOT for backward compatibility
from .config_ssot import (
    ConfigEnvironment,
    ConfigSource,
    UnifiedConfigManager,
    get_agent_config,
    get_config,
    get_test_config,
    get_threshold_config,
    get_timeout_config,
)


# Export deprecated functions
def set_config(*args, **kwargs):
    """DEPRECATED: Use _config_manager.set() instead."""
    warnings.warn("set_config is deprecated", DeprecationWarning, stacklevel=2)
    from .config.config_manager import _config_manager

    return _config_manager.set(*args, **kwargs)


def reload_config(*args, **kwargs):
    """DEPRECATED: Use _config_manager.reload_configs() instead."""
    warnings.warn("reload_config is deprecated", DeprecationWarning, stacklevel=2)
    from .config.config_manager import _config_manager

    return _config_manager.reload_configs(*args, **kwargs)


def validate_config(*args, **kwargs):
    """DEPRECATED: Use _config_manager.validate() instead."""
    warnings.warn("validate_config is deprecated", DeprecationWarning, stacklevel=2)
    from .config.config_manager import _config_manager

    return _config_manager.validate(*args, **kwargs)


def get_all_config(*args, **kwargs):
    """DEPRECATED: Use _config_manager.get_all_configs() instead."""
    warnings.warn("get_all_config is deprecated", DeprecationWarning, stacklevel=2)
    from .config.config_manager import _config_manager

    return _config_manager.get_all_configs(*args, **kwargs)


__all__ = [
    "get_config",
    "set_config",
    "reload_config",
    "validate_config",
    "get_all_config",
    "get_agent_config",
    "get_timeout_config",
    "get_threshold_config",
    "get_test_config",
    "UnifiedConfigManager",
    "ConfigEnvironment",
    "ConfigSource",
]
