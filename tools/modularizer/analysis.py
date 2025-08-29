"""File analysis for identifying monolithic modules."""
from __future__ import annotations

from typing import List, Callable

from . import unified_learning_engine, fsm_compliance_integration, validation_manager, base_manager


def get_targets() -> List[Callable[[], None]]:
    """Return modularization callables for known monolithic files."""
    return [
        unified_learning_engine.modularize,
        fsm_compliance_integration.modularize,
        validation_manager.modularize,
        base_manager.modularize,
    ]
