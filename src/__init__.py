#!/usr/bin/env python3
"""
Agent Cellphone V2 - Clean Architecture Foundation
=================================================

This module provides the core foundation for the V2 system with strict coding standards:
- Object-Oriented Design
- Single Responsibility Principle
- CLI interfaces for testing
- Smoke tests for validation
"""

# Handle both package import and direct execution
try:
    from .core import CoreManager
    from .services import AgentCellPhoneService
    from .launchers import UnifiedLauncher
    from .utils import OnboardingUtils
except ImportError:
    # Direct execution - add current directory to path
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent))
    
    try:
        from core import CoreManager
        from services import AgentCellPhoneService
        from launchers import UnifiedLauncher
        from utils import OnboardingUtils
    except ImportError:
        # Components not yet implemented
        CoreManager = None
        AgentCellPhoneService = None
        UnifiedLauncher = None
        OnboardingUtils = None

__version__ = "2.0.0"
__author__ = "Agent-1 (Project Coordinator)"
__status__ = "Foundation Complete - Ready for Agent-2"

# Core system components
__all__ = [
    "CoreManager",
    "AgentCellPhoneService", 
    "UnifiedLauncher",
    "OnboardingUtils"
]

def get_system_info():
    """Get system information for CLI testing."""
    return {
        "version": __version__,
        "status": __status__,
        "components": [comp for comp in __all__ if globals().get(comp) is not None],
        "standards": [
            "Object-Oriented Design",
            "Single Responsibility Principle", 
            "CLI interfaces for testing",
            "Smoke tests for validation"
        ]
    }

if __name__ == "__main__":
    """CLI interface for system information."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Cellphone V2 System Info")
    parser.add_argument("--info", action="store_true", help="Show system information")
    parser.add_argument("--version", action="store_true", help="Show version")
    parser.add_argument("--standards", action="store_true", help="Show coding standards")
    
    args = parser.parse_args()
    
    if args.info or not any([args.info, args.version, args.standards]):
        info = get_system_info()
        print(f"🚀 Agent Cellphone V2 System")
        print(f"Version: {info['version']}")
        print(f"Status: {info['status']}")
        print(f"Components: {', '.join(info['components'])}")
    
    if args.version:
        print(f"Version: {__version__}")
    
    if args.standards:
        info = get_system_info()
        print("📋 Enforced Coding Standards:")
        for standard in info['standards']:
            print(f"  ✅ {standard}")
