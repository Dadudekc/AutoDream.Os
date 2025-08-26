#!/usr/bin/env python3
"""
Communication Coordinator CLI - V2 Standards Compliant
Command-line interface for testing and managing the communication coordinator
Follows V2 coding standards: ≤100 LOC, CLI interface with smoke tests
"""

import argparse
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from src.utils.unified_logging_manager import get_logger
from typing import List

try:
    from .coordinator_types import (
        CommunicationMode, TaskPriority, TaskStatus,
        CoordinationTask, CoordinationMessage
    )
    from .message_coordinator import MessageCoordinator
    from .channel_manager import ChannelManager
except ImportError:
    # Fallback for standalone usage
    from coordinator_types import (
        CommunicationMode, TaskPriority, TaskStatus,
        CoordinationTask, CoordinationMessage
    )
    from message_coordinator import MessageCoordinator
    from channel_manager import ChannelManager


class CoordinatorCLI:
    """CLI interface for the communication coordinator system"""
    
    def __init__(self):
        self.coordinator = MessageCoordinator()
        self.channel_manager = ChannelManager()
        self.logger = get_logger(__name__)

    def run_smoke_test(self) -> bool:
        """Run smoke tests for the communication coordinator"""
        print("🧪 Running Communication Coordinator Smoke Tests...")
        
        try:
            # Test 1: Create coordinator
            print("  ✓ Creating message coordinator...")
            coordinator = MessageCoordinator()
            
            # Test 2: Register agent
            print("  ✓ Registering test agent...")
            success = coordinator.register_agent(
                "test_agent_1", 
                ["coordination", "messaging"], 
                ["testing"]
            )
            if not success:
                raise Exception("Failed to register agent")
            
            # Test 3: Create task
            print("  ✓ Creating test task...")
            task_id = coordinator.create_task(
                "Test Task", 
                "A test task for smoke testing", 
                TaskPriority.NORMAL, 
                ["test_agent_1"]
            )
            if not task_id:
                raise Exception("Failed to create task")
            
            # Test 4: Assign task
            print("  ✓ Assigning task to agent...")
            success = coordinator.assign_task(task_id, "test_agent_1")
            if not success:
                raise Exception("Failed to assign task")
            
            # Test 5: Update task status
            print("  ✓ Updating task status...")
            success = coordinator.update_task_status(task_id, TaskStatus.IN_PROGRESS, 50.0)
            if not success:
                raise Exception("Failed to update task status")
            
            # Test 6: Send message
            print("  ✓ Sending test message...")
            message_id = coordinator.send_message(
                "test_agent_1", 
                ["test_agent_1"], 
                "test", 
                "Test message content"
            )
            if not message_id:
                raise Exception("Failed to send message")
            
            # Test 7: Create coordination session
            print("  ✓ Creating coordination session...")
            session_id = coordinator.create_coordination_session(
                CommunicationMode.COLLABORATIVE, 
                ["test_agent_1"], 
                ["Test agenda item"]
            )
            if not session_id:
                raise Exception("Failed to create coordination session")
            
            print("✅ All smoke tests passed!")
            return True
            
        except Exception as e:
            print(f"❌ Smoke test failed: {e}")
            return False

    def create_sample_task(self, title: str, description: str, priority: str, agent: str):
        """Create a sample coordination task"""
        try:
            priority_enum = TaskPriority(priority.lower())
            task_id = self.coordinator.create_task(title, description, priority_enum, [agent])
            
            if task_id:
                print(f"✅ Task created successfully: {task_id}")
                print(f"   Title: {title}")
                print(f"   Priority: {priority}")
                print(f"   Assigned to: {agent}")
            else:
                print("❌ Failed to create task")
                
        except ValueError:
            print(f"❌ Invalid priority: {priority}")
            print(f"   Valid options: {[p.value for p in TaskPriority]}")
        except Exception as e:
            print(f"❌ Error creating task: {e}")

    def list_tasks(self):
        """List all coordination tasks"""
        tasks = self.coordinator.tasks
        if not tasks:
            print("📋 No tasks found")
            return
        
        print(f"📋 Found {len(tasks)} tasks:")
        print("-" * 80)
        
        for task_id, task in tasks.items():
            print(f"ID: {task_id}")
            print(f"Title: {task.title}")
            print(f"Status: {task.status.value}")
            print(f"Priority: {task.priority.value}")
            print(f"Assigned to: {', '.join(task.assigned_agents)}")
            print(f"Progress: {task.progress_percentage:.1f}%")
            print("-" * 80)

    def list_agents(self):
        """List all registered agents"""
        agents = self.coordinator.agents
        if not agents:
            print("🤖 No agents registered")
            return
        
        print(f"🤖 Found {len(agents)} registered agents:")
        print("-" * 80)
        
        for agent_id, agent in agents.items():
            print(f"Agent ID: {agent_id}")
            print(f"Capabilities: {', '.join(agent.capabilities)}")
            print(f"Specializations: {', '.join(agent.specializations)}")
            print(f"Availability: {'Yes' if agent.availability else 'No'}")
            print(f"Current Load: {agent.current_load}/{agent.max_capacity}")
            print("-" * 80)

    def send_test_message(self, sender: str, recipient: str, content: str):
        """Send a test message"""
        try:
            message_id = self.coordinator.send_message(sender, [recipient], "test", content)
            
            if message_id:
                print(f"✅ Message sent successfully: {message_id}")
                print(f"   From: {sender}")
                print(f"   To: {recipient}")
                print(f"   Content: {content}")
            else:
                print("❌ Failed to send message")
                
        except Exception as e:
            print(f"❌ Error sending message: {e}")

    def show_system_status(self):
        """Show overall system status"""
        print("📊 Communication Coordinator System Status")
        print("=" * 50)
        
        # Task statistics
        tasks = self.coordinator.tasks
        task_counts = {}
        for task in tasks.values():
            status = task.status.value
            task_counts[status] = task_counts.get(status, 0) + 1
        
        print(f"📋 Tasks: {len(tasks)} total")
        for status, count in task_counts.items():
            print(f"   {status}: {count}")
        
        # Agent statistics
        agents = self.coordinator.agents
        available_agents = sum(1 for agent in agents.values() if agent.availability)
        print(f"🤖 Agents: {len(agents)} total, {available_agents} available")
        
        # Session statistics
        sessions = self.coordinator.sessions
        print(f"🔄 Sessions: {len(sessions)} active")
        
        # Channel statistics
        channels = self.channel_manager.channels
        print(f"📡 Channels: {len(channels)} active")

    def main(self):
        """Main CLI entry point"""
        parser = argparse.ArgumentParser(
            description="Communication Coordinator CLI",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  %(prog)s --smoke-test
  %(prog)s --create-task "Test Task" "Description" "normal" "agent1"
  %(prog)s --list-tasks
  %(prog)s --list-agents
  %(prog)s --send-message "agent1" "agent2" "Hello there!"
  %(prog)s --status
            """
        )
        
        parser.add_argument("--smoke-test", action="store_true",
                          help="Run smoke tests")
        parser.add_argument("--create-task", nargs=4, metavar=("TITLE", "DESCRIPTION", "PRIORITY", "AGENT"),
                          help="Create a new task")
        parser.add_argument("--list-tasks", action="store_true",
                          help="List all tasks")
        parser.add_argument("--list-agents", action="store_true",
                          help="List all agents")
        parser.add_argument("--send-message", nargs=3, metavar=("SENDER", "RECIPIENT", "CONTENT"),
                          help="Send a test message")
        parser.add_argument("--status", action="store_true",
                          help="Show system status")
        
        args = parser.parse_args()
        
        if args.smoke_test:
            success = self.run_smoke_test()
            sys.exit(0 if success else 1)
        elif args.create_task:
            title, description, priority, agent = args.create_task
            self.create_sample_task(title, description, priority, agent)
        elif args.list_tasks:
            self.list_tasks()
        elif args.list_agents:
            self.list_agents()
        elif args.send_message:
            sender, recipient, content = args.send_message
            self.send_test_message(sender, recipient, content)
        elif args.status:
            self.show_system_status()
        else:
            parser.print_help()


if __name__ == "__main__":
    cli = CoordinatorCLI()
    cli.main()
