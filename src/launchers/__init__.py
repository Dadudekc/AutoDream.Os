"""
🚀 Launchers Package - Agent_Cellphone_V2

This package contains the entry point launchers for the Agent_Cellphone_V2 system:
- System startup launchers
- Service launchers
- Test launchers
- Demo launchers

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Launcher & Integration Team"
__status__ = "ACTIVE"

import argparse
import sys

# Launcher component imports
try:
    from .unified_launcher_v2 import UnifiedLauncherV2
    from .launcher_core import LauncherCore
    from .launcher_modes import LauncherModes
    from .workspace_management_launcher import WorkspaceManagementLauncher
    from .contract_management_launcher import ContractManagementLauncher
    from .onboarding_system_launcher import OnboardingSystemLauncher
    from .sprint_management_launcher import SprintManagementLauncher

    __all__ = [
        "UnifiedLauncherV2",
        "LauncherCore",
        "LauncherModes",
        "WorkspaceManagementLauncher",
        "ContractManagementLauncher",
        "OnboardingSystemLauncher",
        "SprintManagementLauncher",
    ]

except ImportError as e:
    print(f"⚠️ Warning: Some launcher components not available: {e}")
    __all__ = []


def main():
    """CLI interface for launchers module"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 Launchers Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.launchers --test                    # Run launcher tests
    python -m src.launchers --status                 # Show launcher status
    python -m src.launchers --demo                   # Run launcher demo
    python -m src.launchers --launch unified         # Launch unified system
        """,
    )

    parser.add_argument("--test", action="store_true", help="Run launcher module tests")
    parser.add_argument(
        "--status", action="store_true", help="Show launcher module status"
    )
    parser.add_argument("--demo", action="store_true", help="Run launcher module demo")
    parser.add_argument(
        "--list", action="store_true", help="List available launcher components"
    )
    parser.add_argument(
        "--launch",
        choices=["unified", "core", "workspace", "contract", "onboarding", "sprint"],
        help="Launch specific system component",
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running launcher module tests...")
        # Run tests for each component
        test_results = {}
        for component in __all__:
            try:
                component_class = globals()[component]
                if hasattr(component_class, "run_smoke_test"):
                    print(f"  Testing {component}...")
                    success = component_class().run_smoke_test()
                    test_results[component] = success
                    print(f"    {'✅ PASS' if success else '❌ FAIL'}")
                else:
                    print(f"  ⚠️ {component} has no smoke test")
                    test_results[component] = False
            except Exception as e:
                print(f"  ❌ {component} test failed: {e}")
                test_results[component] = False

        passed = sum(test_results.values())
        total = len(test_results)
        print(f"\n📊 Test Results: {passed}/{total} passed")
        return 0 if passed == total else 1

    elif args.status:
        print("📊 Launchers Module Status")
        print("=" * 30)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Components: {len(__all__)}")
        print("\n🚀 Available Launchers:")
        for component in __all__:
            print(f"  ✅ {component}")
        return 0

    elif args.demo:
        print("🚀 Starting launcher module demo...")
        try:
            # Create instances and demonstrate functionality
            if "UnifiedLauncherV2" in __all__:
                launcher = UnifiedLauncherV2()
                print("✅ UnifiedLauncherV2 created")

            if "LauncherCore" in __all__:
                core = LauncherCore()
                print("✅ LauncherCore created")

            print("🎯 Launcher module demo completed")
            return 0
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return 1

    elif args.launch:
        print(f"🚀 Launching {args.launch} system...")
        try:
            if args.launch == "unified" and "UnifiedLauncherV2" in __all__:
                launcher = UnifiedLauncherV2()
                launcher.start()
                print("✅ Unified system launched successfully")
            elif args.launch == "core" and "LauncherCore" in __all__:
                launcher = LauncherCore()
                launcher.start()
                print("✅ Core system launched successfully")
            elif (
                args.launch == "workspace" and "WorkspaceManagementLauncher" in __all__
            ):
                launcher = WorkspaceManagementLauncher()
                launcher.start()
                print("✅ Workspace management launched successfully")
            elif args.launch == "contract" and "ContractManagementLauncher" in __all__:
                launcher = ContractManagementLauncher()
                launcher.start()
                print("✅ Contract management launched successfully")
            elif args.launch == "onboarding" and "OnboardingSystemLauncher" in __all__:
                launcher = OnboardingSystemLauncher()
                launcher.start()
                print("✅ Onboarding system launched successfully")
            elif args.launch == "sprint" and "SprintManagementLauncher" in __all__:
                launcher = SprintManagementLauncher()
                launcher.start()
                print("✅ Sprint management launched successfully")
            else:
                print(f"❌ Launcher for {args.launch} not available")
                return 1
            return 0
        except Exception as e:
            print(f"❌ Launch failed: {e}")
            return 1

    elif args.list:
        print("📋 Available Launcher Components:")
        for component in __all__:
            print(f"  🚀 {component}")
        return 0

    else:
        parser.print_help()
        print(f"\n🚀 Launchers Module {__version__} - {__status__}")
        print("Use --help for more options!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
