"""
System Launch and Initialization

This package contains launchers for different system modes:
- Unified Launcher: Enhanced from original, supports multiple modes
- Unified Launcher V2: FSM-integrated launcher with full coordination
- System initialization and startup
- Configuration validation and setup

Design Principles:
- Launch Layer: System startup and initialization
- Validation: Ensure system is ready before launch
- Flexibility: Support multiple launch modes
- FSM Integration: Complete agent coordination via FSM
"""

from .unified_launcher_v2 import UnifiedLauncherV2, LaunchConfig

__all__ = [
    "UnifiedLauncherV2",
    "LaunchConfig"
]
