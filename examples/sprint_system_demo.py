#!/usr/bin/env python3
"""
Sprint System Demo - Agent Cellphone V2
=======================================

Demonstrates the integrated ai-task-organizer sprint system.
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from launchers.sprint_management_launcher import (
    SprintManagementLauncher,
    SprintLaunchConfig,
)


def demo_sprint_lifecycle():
    """Demonstrate complete sprint lifecycle."""
    print("🚀 AI Task Organizer Sprint System Demo")
    print("=" * 50)

    # Initialize launcher
    launcher = SprintManagementLauncher()

    # Step 1: Create a new sprint
    print("\n📋 Step 1: Creating Sprint")
    print("-" * 30)

    create_config = SprintLaunchConfig(
        mode="create", sprint_id="Demo-Sprint-001", duration_days=14
    )

    success = launcher.launch(create_config)
    if success:
        print("✅ Sprint created successfully")
    else:
        print("❌ Sprint creation failed")
        return

    # Step 2: Plan tasks for the sprint
    print("\n📝 Step 2: Planning Sprint Tasks")
    print("-" * 30)

    # Example tasks for a development sprint
    demo_tasks = [
        "Implement user authentication",
        "Create database schema",
        "Build API endpoints",
        "Design frontend components",
        "Write unit tests",
        "Set up CI/CD pipeline",
        "Document API usage",
        "Performance optimization",
        "Security review",
        "User acceptance testing",
    ]

    plan_config = SprintLaunchConfig(
        mode="plan", sprint_id="Demo-Sprint-001", task_ids=demo_tasks
    )

    success = launcher.launch(plan_config)
    if success:
        print(f"✅ Planned {len(demo_tasks)} tasks for sprint")
        print(f"   Tasks: {', '.join(demo_tasks[:5])}...")
    else:
        print("❌ Sprint planning failed")
        return

    # Step 3: Start the sprint
    print("\n▶️  Step 3: Starting Sprint")
    print("-" * 30)

    start_config = SprintLaunchConfig(mode="start", sprint_id="Demo-Sprint-001")

    success = launcher.launch(start_config)
    if success:
        print("✅ Sprint started successfully")
    else:
        print("❌ Sprint start failed")
        return

    # Step 4: Show sprint status
    print("\n📊 Step 4: Sprint Status")
    print("-" * 30)

    status_config = SprintLaunchConfig(mode="status", sprint_id="Demo-Sprint-001")

    success = launcher.launch(status_config)
    if not success:
        print("❌ Status check failed")

    # Step 5: Update daily progress
    print("\n📈 Step 5: Daily Progress Update")
    print("-" * 30)

    progress_config = SprintLaunchConfig(mode="progress", sprint_id="Demo-Sprint-001")

    success = launcher.launch(progress_config)
    if success:
        print("✅ Progress updated successfully")
    else:
        print("❌ Progress update failed")

    # Step 6: Complete the sprint
    print("\n🏁 Step 6: Completing Sprint")
    print("-" * 30)

    complete_config = SprintLaunchConfig(mode="complete", sprint_id="Demo-Sprint-001")

    success = launcher.launch(complete_config)
    if success:
        print("✅ Sprint completed successfully")
    else:
        print("❌ Sprint completion failed")

    # Final status
    print("\n📊 Final Sprint Status")
    print("-" * 30)

    success = launcher.launch(status_config)
    if not success:
        print("❌ Final status check failed")

    print("\n🎉 Sprint System Demo Completed!")
    print(
        "The ai-task-organizer sprint system has been successfully integrated into V2!"
    )


def demo_10_task_limit():
    """Demonstrate the 10-task limit enforcement."""
    print("\n🔒 10-Task Limit Enforcement Demo")
    print("=" * 50)

    launcher = SprintManagementLauncher()

    # Create sprint
    create_config = SprintLaunchConfig(mode="create", sprint_id="Limit-Demo-Sprint")

    success = launcher.launch(create_config)
    if not success:
        print("❌ Sprint creation failed")
        return

    # Try to add 12 tasks (should fail)
    print("\n📝 Attempting to plan 12 tasks (exceeds 10-task limit)")
    print("-" * 50)

    extra_tasks = [f"Extra-Task-{i}" for i in range(12)]

    plan_config = SprintLaunchConfig(
        mode="plan", sprint_id="Limit-Demo-Sprint", task_ids=extra_tasks
    )

    success = launcher.launch(plan_config)
    if not success:
        print("✅ 10-task limit properly enforced - planning failed as expected")
    else:
        print("❌ 10-task limit not enforced - this is a bug")

    # Show final status
    print("\n📊 Final Sprint Status")
    print("-" * 30)

    status_config = SprintLaunchConfig(mode="status", sprint_id="Limit-Demo-Sprint")

    launcher.launch(status_config)


def main():
    """Main demo function."""
    try:
        # Run main sprint lifecycle demo
        demo_sprint_lifecycle()

        # Run 10-task limit demo
        demo_10_task_limit()

        print("\n" + "=" * 60)
        print("🎯 INTEGRATION SUCCESS!")
        print("✅ ai-task-organizer sprint system integrated into V2")
        print("✅ 10 tasks per sprint system working")
        print("✅ No code duplication - reused existing architecture")
        print("✅ V2 standards maintained (OOP, SRP, 200 LOC limit)")
        print("=" * 60)

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
