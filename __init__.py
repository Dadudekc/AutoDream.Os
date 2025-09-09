# AUTO-GENERATED __init__.py
# Safe for test collection. Heavy imports disabled by default.

from __future__ import annotations

import os

__all__ = [
    'core_functionality_test',
    'debug_imports',
    'fix_manager_results',
    'run_smoke_tests',
    'run_unified',
    'simple_overnight_monitor',
    'simple_test_runner',
    'test_coordinate_display',
    'test_coordinates',
    'test_ctrl_t_onboarding_navigation',
    'test_pyautogui_mode',
    'test_runner',
    'test_solid_refactor',
    'verification_plan',
]

# Opt-in import of heavy modules to avoid circular imports and side-effects
# during pytest collection. Set ACV2_IMPORT_ALL=1 to enable.
if os.getenv('ACV2_IMPORT_ALL') == '1':
    from . import core_functionality_test  # noqa: F401
    from . import debug_imports  # noqa: F401
    from . import fix_manager_results  # noqa: F401
    from . import run_smoke_tests  # noqa: F401
    from . import run_unified  # noqa: F401
    from . import simple_overnight_monitor  # noqa: F401
    from . import simple_test_runner  # noqa: F401
    from . import test_coordinate_display  # noqa: F401
    from . import test_coordinates  # noqa: F401
    from . import test_ctrl_t_onboarding_navigation  # noqa: F401
    from . import test_pyautogui_mode  # noqa: F401
    from . import test_runner  # noqa: F401
    from . import test_solid_refactor  # noqa: F401
    from . import verification_plan  # noqa: F401
