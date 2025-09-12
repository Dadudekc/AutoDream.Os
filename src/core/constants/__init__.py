# AUTO-GENERATED __init__.py
# DO NOT EDIT MANUALLY - changes may be overwritten

# Import FSM constants - try direct import first
import importlib.util
import os
import sys

from . import decision, fsm_constants, fsm_enums, fsm_models, fsm_utilities, manager, paths

# Load FSM constants module directly
fsm_constants_path = os.path.join(os.path.dirname(__file__), "fsm.py")
if os.path.exists(fsm_constants_path):
    spec = importlib.util.spec_from_file_location("fsm_constants", fsm_constants_path)
    if spec and spec.loader:
        fsm_module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(fsm_module)
            # Import the constants
            CORE_FSM_START_STATE = getattr(fsm_module, "CORE_FSM_START_STATE", None)
            CORE_FSM_PROCESS_STATE = getattr(fsm_module, "CORE_FSM_PROCESS_STATE", None)
            CORE_FSM_END_STATE = getattr(fsm_module, "CORE_FSM_END_STATE", None)
            CORE_FSM_DEFAULT_STATES = getattr(fsm_module, "CORE_FSM_DEFAULT_STATES", [])
            CORE_FSM_TRANSITION_START_PROCESS = getattr(
                fsm_module, "CORE_FSM_TRANSITION_START_PROCESS", None
            )
            CORE_FSM_TRANSITION_PROCESS_END = getattr(
                fsm_module, "CORE_FSM_TRANSITION_PROCESS_END", None
            )
        except Exception:
            # Fallback to None values
            CORE_FSM_START_STATE = None
            CORE_FSM_PROCESS_STATE = None
            CORE_FSM_END_STATE = None
            CORE_FSM_DEFAULT_STATES = []
            CORE_FSM_TRANSITION_START_PROCESS = None
            CORE_FSM_TRANSITION_PROCESS_END = None
    else:
        # Fallback to None values
        CORE_FSM_START_STATE = None
        CORE_FSM_PROCESS_STATE = None
        CORE_FSM_END_STATE = None
        CORE_FSM_DEFAULT_STATES = []
        CORE_FSM_TRANSITION_START_PROCESS = None
        CORE_FSM_TRANSITION_PROCESS_END = None
else:
    # Fallback to None values if file doesn't exist
    CORE_FSM_START_STATE = None
    CORE_FSM_PROCESS_STATE = None
    CORE_FSM_END_STATE = None
    CORE_FSM_DEFAULT_STATES = []
    CORE_FSM_TRANSITION_START_PROCESS = None
    CORE_FSM_TRANSITION_PROCESS_END = None

__all__ = [
    "decision",
    "fsm_constants",
    "fsm_enums",
    "fsm_models",
    "fsm_utilities",
    "manager",
    "paths",
    "CORE_FSM_START_STATE",
    "CORE_FSM_PROCESS_STATE",
    "CORE_FSM_END_STATE",
    "CORE_FSM_DEFAULT_STATES",
    "CORE_FSM_TRANSITION_START_PROCESS",
    "CORE_FSM_TRANSITION_PROCESS_END",
]
