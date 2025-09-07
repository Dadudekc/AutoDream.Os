# flake8: noqa
"""Unified Constants Package"""

from .manager import *

__all__ = [
    'DEFAULT_HEALTH_CHECK_INTERVAL',
    'DEFAULT_MAX_STATUS_HISTORY',
    'DEFAULT_AUTO_RESOLVE_TIMEOUT',
    'STATUS_CONFIG_PATH',
    'COMPLETION_SIGNAL',
    'get_completion_signal',
]

