from pathlib import Path
import argparse
import sys

            from examples.demo_suite import run_demo
            from tests.run_tests import run_all_tests
            from tests.v2_standards_checker import validate_v2_standards

"""
🚀 Agent_Cellphone_V2 - Main Package

This is the main package for the Agent_Cellphone_V2 system, following V2 coding standards:
- ≤300 LOC per file, OOP design, SRP
- CLI interfaces for all components
- Comprehensive testing infrastructure
- Agent-friendly design

Usage:
    python -m src --help                    # Show main help
    python -m src.core --help               # Show core module help
    python -m src.services --help           # Show services module help
    python -m src.launchers --help          # Show launchers module help
    python -m src.utils --help              # Show utils module help
"""

__version__ = "2.0.0"
__author__ = "Agent_Cellphone_V2 Development Team"
__status__ = "ACTIVE - V2 STANDARDS COMPLIANT"


# Stability improvements are available but not auto-imported to avoid circular imports
# from src.utils.stability_improvements import stability_manager, safe_import

# Add src to path for imports
src_path = Path(__file__).parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))


def main():
    """Main CLI interface for the V2 system"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 - Main System Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src --test                    # Run all tests
    python -m src --demo                    # Run demo mode
    python -m src.core --help               # Core module help
    python -m src.services --help           # Services module help
    python -m src.launchers --help          # Launchers module help
    python -m src.utils --help              # Utils module help
        """,
    )

    parser.add_argument(
        "--test", action="store_true", help="Run comprehensive test suite"
    )
    parser.add_argument("--demo", action="store_true", help="Run system demo")
    parser.add_argument("--status", action="store_true", help="Show system status")
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate V2 coding standards compliance",
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running comprehensive test suite...")
        # Import and run test suite
        try:

            success = run_all_tests()
            if success:
                print("✅ All tests passed!")
                return 0
            else:
                print("❌ Some tests failed!")
                return 1
        except ImportError:
            print("⚠️ Test suite not available")
            return 1

    elif args.demo:
        print("🚀 Starting Agent_Cellphone_V2 demo...")
        # Import and run demo
        try:

            run_demo()
            return 0
        except ImportError:
            print("⚠️ Demo not available")
            return 1

    elif args.status:
        print("📊 Agent_Cellphone_V2 System Status")
        print("=" * 40)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Author: {__author__}")
        print("\n📁 Package Structure:")
        print("  src/")
        print("  ├── core/           # Core systems")
        print("  ├── services/       # Business logic")
        print("  ├── launchers/      # Entry points")
        print("  └── utils/          # Utilities")
        print("\n🧪 Testing:")
        print("  tests/")
        print("  ├── smoke/          # Smoke tests")
        print("  ├── unit/           # Unit tests")
        print("  └── integration/    # Integration tests")
        return 0

    elif args.validate:
        print("🔍 Validating V2 coding standards compliance...")
        # Import and run validation
        try:

            results = validate_v2_standards()
            if results["overall_compliance"]:
                print("✅ V2 standards compliance validated!")
                return 0
            else:
                print("❌ V2 standards violations found!")
                return 1
        except ImportError:
            print("⚠️ Standards checker not available")
            return 1

    else:
        parser.print_help()
        print(f"\n🎯 Agent_Cellphone_V2 {__version__} - {__status__}")
        print("Use --help for more options or --demo to see the system in action!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
