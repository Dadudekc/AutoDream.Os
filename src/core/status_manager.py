#!/usr/bin/env python3
"""Status Manager orchestrator importing modular components."""

from .status_manager_core import StatusManager, run_smoke_test, main
from .status_manager_config import (
    StatusTransition,
    HealthCheck,
    Alert,
    StatusEvent,
)

__all__ = [
    "StatusManager",
    "run_smoke_test",
    "main",
    "StatusTransition",
    "HealthCheck",
    "Alert",
    "StatusEvent",
]

if __name__ == "__main__":
    main()
