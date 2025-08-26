"""
🚀 Services Package - Agent_Cellphone_V2

This package contains the business logic services for the Agent_Cellphone_V2 system:
- Agent management services
- Communication services
- Integration services
- Business workflow services

Following V2 coding standards: ≤300 LOC per file, OOP design, SRP.
"""

__version__ = "2.0.0"
__author__ = "Services & Integration Team"
__status__ = "ACTIVE"

import argparse
import sys

from src.utils.stability_improvements import stability_manager, safe_import

# Services component imports
try:
    from .agent_cell_phone import AgentCellPhone
    from .sprint_management_service import SprintManagementService, Sprint, SprintStatus
    from .sprint_workflow_service import SprintWorkflowService, WorkflowStage

    __all__ = [
        "AgentCellPhone",
        "SprintManagementService",
        "SprintWorkflowService",
        "Sprint",
        "SprintStatus",
        "WorkflowStage",
    ]

except Exception as e:
    print(f"⚠️ Warning: Some services components not available: {e}")
    __all__ = []


def main():
    """CLI interface for services module"""
    parser = argparse.ArgumentParser(
        description="Agent_Cellphone_V2 Services Module",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python -m src.services --test                    # Run services tests
    python -m src.services --status                 # Show services status
    python -m src.services --demo                   # Run services demo
        """,
    )

    parser.add_argument("--test", action="store_true", help="Run services module tests")
    parser.add_argument(
        "--status", action="store_true", help="Show services module status"
    )
    parser.add_argument("--demo", action="store_true", help="Run services module demo")
    parser.add_argument(
        "--list", action="store_true", help="List available services components"
    )

    args = parser.parse_args()

    if args.test:
        print("🧪 Running services module tests...")
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
        print("📊 Services Module Status")
        print("=" * 28)
        print(f"Version: {__version__}")
        print(f"Status: {__status__}")
        print(f"Components: {len(__all__)}")
        print("\n🚀 Available Services:")
        for component in __all__:
            print(f"  ✅ {component}")
        return 0

    elif args.demo:
        print("🚀 Starting services module demo...")
        try:
            # Create instances and demonstrate functionality
            if "AgentCellPhone" in __all__:
                service = AgentCellPhone()
                print("✅ AgentCellPhone service created")

            print("🎯 Services module demo completed")
            return 0
        except Exception as e:
            print(f"❌ Demo failed: {e}")
            return 1

    elif args.list:
        print("📋 Available Services Components:")
        for component in __all__:
            print(f"  🚀 {component}")
        return 0

    else:
        parser.print_help()
        print(f"\n🚀 Services Module {__version__} - {__status__}")
        print("Use --help for more options!")
        return 0


if __name__ == "__main__":
    sys.exit(main())
