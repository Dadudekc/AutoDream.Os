"""
🔧 Utils Package - Agent_Cellphone_V2

This package contains utility components for the Agent_Cellphone_V2 system:
- Configuration utilities
- Logging utilities
- System utilities
- Validation utilities
- File utilities

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Utilities & Support Team"
__status__ = "ACTIVE"

import argparse
import sys

# Stability improvements are available but not auto-imported to avoid circular imports
# from src.utils.stability_improvements import stability_manager, safe_import

# Utils component imports
try:
    from .config_loader import ConfigLoader
    from .logging_setup import LoggingSetup
    from .system_info import SystemInfo
    from .performance_monitor import PerformanceMonitor
    from .dependency_checker import DependencyChecker
    from .cli_utils import CLIUtils
    from .file_utils import FileUtils
    from .message_builder import MessageBuilder
    from .onboarding_utils import OnboardingUtils
    from .onboarding_coordinator import OnboardingCoordinator
    from .onboarding_orchestrator import OnboardingOrchestrator
    from .config_utils_coordinator import ConfigUtilsCoordinator
    from .system_utils_coordinator import SystemUtilsCoordinator
    from .environment_overrides import EnvironmentOverrides
    from .serializable import SerializableMixin

    __all__ = [
        "ConfigLoader",
        "LoggingSetup",
        "SystemInfo",
        "PerformanceMonitor",
        "DependencyChecker",
        "CLIUtils",
        "FileUtils",
        "MessageBuilder",
        "OnboardingUtils",
        "OnboardingCoordinator",
        "OnboardingOrchestrator",
        "ConfigUtilsCoordinator",
        "SystemUtilsCoordinator",
        "EnvironmentOverrides",
        "SerializableMixin",
    ]

except ImportError as e:
    print(f"⚠️ Warning: Some utils components not available: {e}")
    __all__ = []


def main():
    """CLI interface for utils module"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 Utils Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.utils --test                    # Run utils tests
    python -m src.utils --status                 # Show utils status
    python -m src.utils --demo                   # Run utils demo
    python -m src.utils --check-deps             # Check dependencies
    python -m src.utils --system-info            # Show system information
        """,
    )

    parser.add_argument("--test", action="store_true", help="Run utils module tests")
    parser.add_argument(
        "--status", action="store_true", help="Show utils module status"
    )
    parser.add_argument("--demo", action="store_true", help="Run utils module demo")
    parser.add_argument(
        "--list", action="store_true", help="List available utils components"
    )
    parser.add_argument(
        "--check-deps", action="store_true", help="Check system dependencies"
    )
    parser.add_argument(
        "--system-info", action="store_true", help="Show system information"
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running utils module tests...")
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
        print("📊 Utils Module Status")
        print("=" * 25)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Components: {len(__all__)}")
        print("\n🔧 Available Utilities:")
        for component in __all__:
            print(f"  ✅ {component}")
        return 0

    elif args.demo:
        print("🚀 Starting utils module demo...")
        try:
            # Create instances and demonstrate functionality
            if "SystemInfo" in __all__:
                info = SystemInfo()
                print("✅ SystemInfo created")

            if "PerformanceMonitor" in __all__:
                monitor = PerformanceMonitor()
                print("✅ PerformanceMonitor created")

            if "DependencyChecker" in __all__:
                checker = DependencyChecker()
                print("✅ DependencyChecker created")

            print("🎯 Utils module demo completed")
            return 0
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return 1

    elif args.check_deps:
        print("🔍 Checking system dependencies...")
        try:
            if "DependencyChecker" in __all__:
                checker = DependencyChecker()
                results = checker.check_all_dependencies()
                print("📋 Dependency Check Results:")
                for dep, status in results.items():
                    print(f"  {'✅' if status else '❌'} {dep}")
                return 0
            else:
                print("❌ DependencyChecker not available")
                return 1
        except Exception as e:
            print(f"❌ Dependency check failed: {e}")
            return 1

    elif args.system_info:
        print("💻 System Information:")
        try:
            if "SystemInfo" in __all__:
                info = SystemInfo()
                system_data = info.get_system_info()
                for key, value in system_data.items():
                    print(f"  {key}: {value}")
                return 0
            else:
                print("❌ SystemInfo not available")
                return 1
        except Exception as e:
            print(f"❌ System info failed: {e}")
            return 1

    elif args.list:
        print("📋 Available Utils Components:")
        for component in __all__:
            print(f"  🔧 {component}")
        return 0

    else:
        parser.print_help()
        print(f"\n🔧 Utils Module {__version__} - {__status__}")
        print("Use --help for more options!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
