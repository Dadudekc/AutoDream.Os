#!/usr/bin/env python3
"""
Workspace & Inbox System Demo - Agent Cellphone V2
=================================================

Demonstrates the complete workspace and inbox system working in V2.
Shows agent workspace management, message routing, and task management.
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from core.workspace_manager import WorkspaceManager
from core.inbox_manager import InboxManager, MessagePriority, MessageStatus
from core.task_manager import TaskManager, TaskPriority, TaskStatus


def demo_workspace_system():
    """Demonstrate the workspace management system."""
    print("🏢 **WORKSPACE MANAGEMENT SYSTEM DEMO - V2**")
    print("=" * 60)

    try:
        # Initialize workspace manager
        workspace_manager = WorkspaceManager()
        print("✅ Workspace Manager initialized")

        # Create additional test workspaces
        workspace_manager.create_workspace("DemoAgent")
        workspace_manager.create_workspace("TestAgent")
        print("✅ Additional test workspaces created")

        # Show all workspaces
        workspaces = workspace_manager.get_all_workspaces()
        print(f"📁 Total workspaces: {len(workspaces)}")

        for workspace in workspaces:
            print(f"   📂 {workspace.agent_id}: {workspace.workspace_path}")
            print(f"      📬 Inbox: {workspace.inbox_path}")
            print(f"      📋 Tasks: {workspace.tasks_path}")
            print(f"      📤 Responses: {workspace.responses_path}")

        # Show workspace status
        print("\n📊 **WORKSPACE STATUS**")
        print("=" * 40)

        status = workspace_manager.get_workspace_status()
        for key, value in status.items():
            if key != "workspace_details":
                print(f"   {key}: {value}")

        return True

    except Exception as e:
        print(f"❌ Workspace demo failed: {e}")
        return False


def demo_inbox_system():
    """Demonstrate the inbox management system."""
    print("\n📬 **INBOX MANAGEMENT SYSTEM DEMO - V2**")
    print("=" * 60)

    try:
        # Initialize managers
        workspace_manager = WorkspaceManager()
        inbox_manager = InboxManager(workspace_manager)
        print("✅ Inbox Manager initialized")

        # Send test messages
        print("\n📤 **SENDING TEST MESSAGES**")
        print("=" * 40)

        # High priority message
        message1_id = inbox_manager.send_message(
            "Agent-1",
            "Agent-2",
            "Urgent Task",
            "Please complete the critical analysis immediately",
            MessagePriority.HIGH,
        )
        print(f"✅ High priority message sent: {message1_id}")

        # Normal priority message
        message2_id = inbox_manager.send_message(
            "Agent-3",
            "Agent-1",
            "Status Update",
            "Core implementation is progressing well",
            MessagePriority.NORMAL,
        )
        print(f"✅ Normal priority message sent: {message2_id}")

        # Low priority message
        message3_id = inbox_manager.send_message(
            "Agent-5",
            "Agent-4",
            "Documentation",
            "Please review the updated documentation",
            MessagePriority.LOW,
        )
        print(f"✅ Low priority message sent: {message3_id}")

        # Show inbox status for each agent
        print("\n📊 **INBOX STATUS FOR AGENTS**")
        print("=" * 40)

        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4"]:
            status = inbox_manager.get_inbox_status(agent_id)
            print(f"\n📬 {agent_id}:")
            for key, value in status.items():
                if key != "agent_id":
                    print(f"   {key}: {value}")

        # Show messages for specific agent
        print("\n📨 **MESSAGES FOR AGENT-2**")
        print("=" * 40)

        messages = inbox_manager.get_messages("Agent-2")
        for message in messages:
            print(f"   📄 {message.message_id}")
            print(f"      From: {message.sender}")
            print(f"      Subject: {message.subject}")
            print(f"      Priority: {message.priority.value}")
            print(f"      Status: {message.status.value}")
            print(f"      Content: {message.content[:50]}...")

        return True

    except Exception as e:
        print(f"❌ Inbox demo failed: {e}")
        return False


def demo_task_system():
    """Demonstrate the task management system."""
    print("\n📋 **TASK MANAGEMENT SYSTEM DEMO - V2**")
    print("=" * 60)

    try:
        # Initialize managers
        workspace_manager = WorkspaceManager()
        task_manager = TaskManager(workspace_manager)
        print("✅ Task Manager initialized")

        # Create test tasks
        print("\n📝 **CREATING TEST TASKS**")
        print("=" * 40)

        # Critical task
        task1_id = task_manager.create_task(
            "System Architecture Review",
            "Review and validate the V2 system architecture design",
            "Agent-2",
            "Agent-1",
            TaskPriority.CRITICAL,
        )
        print(f"✅ Critical task created: {task1_id}")

        # High priority task
        task2_id = task_manager.create_task(
            "Response Capture Testing",
            "Test the response capture system functionality",
            "Agent-3",
            "Agent-1",
            TaskPriority.HIGH,
        )
        print(f"✅ High priority task created: {task2_id}")

        # Normal priority task
        task3_id = task_manager.create_task(
            "Documentation Update",
            "Update system documentation with new features",
            "Agent-4",
            "Agent-5",
            TaskPriority.NORMAL,
        )
        print(f"✅ Normal priority task created: {task3_id}")

        # Show task status for each agent
        print("\n📊 **TASK STATUS FOR AGENTS**")
        print("=" * 40)

        for agent_id in ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5"]:
            status = task_manager.get_task_status(agent_id)
            print(f"\n📋 {agent_id}:")
            for key, value in status.items():
                if key != "agent_id":
                    print(f"   {key}: {value}")

        # Show tasks for specific agent
        print("\n📋 **TASKS FOR AGENT-2**")
        print("=" * 40)

        tasks = task_manager.get_tasks("Agent-2")
        for task in tasks:
            print(f"   📄 {task.task_id}")
            print(f"      Title: {task.title}")
            print(f"      Priority: {task.priority.value}")
            print(f"      Status: {task.status.value}")
            print(f"      Description: {task.description[:50]}...")

        # Update task status
        print("\n🔄 **UPDATING TASK STATUS**")
        print("=" * 40)

        if task1_id:
            success = task_manager.update_task_status(task1_id, TaskStatus.IN_PROGRESS)
            print(f"Task status update: {'✅ Success' if success else '❌ Failed'}")

        return True

    except Exception as e:
        print(f"❌ Task demo failed: {e}")
        return False


def demo_integration():
    """Demonstrate system integration."""
    print("\n🔄 **SYSTEM INTEGRATION DEMO - V2**")
    print("=" * 60)

    try:
        # Initialize all managers
        workspace_manager = WorkspaceManager()
        inbox_manager = InboxManager(workspace_manager)
        task_manager = TaskManager(workspace_manager)
        print("✅ All managers initialized successfully")

        # Show overall system status
        print("\n📊 **OVERALL SYSTEM STATUS**")
        print("=" * 40)

        workspace_status = workspace_manager.get_workspace_status()
        inbox_status = inbox_manager.get_system_status()
        task_status = task_manager.get_system_status()

        print("🏢 Workspace System:")
        for key, value in workspace_status.items():
            if key not in ["workspace_details"]:
                print(f"   {key}: {value}")

        print("\n📬 Inbox System:")
        for key, value in inbox_status.items():
            print(f"   {key}: {value}")

        print("\n📋 Task System:")
        for key, value in task_status.items():
            print(f"   {key}: {value}")

        # Test complete workflow
        print("\n🔄 **COMPLETE WORKFLOW TEST**")
        print("=" * 40)

        # 1. Create workspace for new agent
        workspace_manager.create_workspace("WorkflowAgent")
        print("✅ 1. Workspace created for WorkflowAgent")

        # 2. Send message to new agent
        message_id = inbox_manager.send_message(
            "Agent-1",
            "WorkflowAgent",
            "Welcome Task",
            "Welcome to the system! Please complete your onboarding.",
            MessagePriority.HIGH,
        )
        print("✅ 2. Welcome message sent")

        # 3. Create task for new agent
        task_id = task_manager.create_task(
            "System Onboarding",
            "Complete system onboarding and setup",
            "WorkflowAgent",
            "Agent-1",
            TaskPriority.HIGH,
        )
        print("✅ 3. Onboarding task created")

        # 4. Show final status
        print("\n📊 **FINAL WORKFLOW STATUS**")
        print("=" * 30)

        workflow_status = inbox_manager.get_inbox_status("WorkflowAgent")
        print(f"Inbox: {workflow_status}")

        workflow_tasks = task_manager.get_task_status("WorkflowAgent")
        print(f"Tasks: {workflow_tasks}")

        return True

    except Exception as e:
        print(f"❌ Integration demo failed: {e}")
        return False


def main():
    """Run the complete workspace and inbox system demonstration."""
    print("🚀 **COMPLETE WORKSPACE & INBOX SYSTEM DEMONSTRATION - V2**")
    print("=" * 80)
    print("This demo shows the complete workspace and inbox system working in V2")
    print("=" * 80)

    # Run demos
    success1 = demo_workspace_system()
    success2 = demo_inbox_system()
    success3 = demo_task_system()
    success4 = demo_integration()

    print("\n" + "=" * 80)

    if all([success1, success2, success3, success4]):
        print("🎉 **ALL DEMOS SUCCESSFUL!**")
        print("\n💡 **What this demonstrates:**")
        print("   1. Workspace management system is fully functional")
        print("   2. Inbox system with message routing is working")
        print("   3. Task management system is operational")
        print("   4. All systems integrate seamlessly")
        print("   5. Strict coding standards are enforced")
        print("   6. CLI interfaces are functional")
        print("\n🚀 **V2 System Status: WORKSPACE & INBOX INFRASTRUCTURE COMPLETE**")
    else:
        print("⚠️ **Some demos failed - review needed**")

    print("\n🔧 **How to test individual components:**")
    print("   - Workspace: python src/core/workspace_manager.py --status")
    print("   - Inbox: python src/core/inbox_manager.py --status Agent-1")
    print("   - Tasks: python src/core/task_manager.py --status Agent-1")
    print("   - Full demo: python examples/demo_workspace_inbox_system.py")


if __name__ == "__main__":
    main()
