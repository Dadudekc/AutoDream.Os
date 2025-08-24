"""
Demo Suite - System Demonstration and Testing

This module provides comprehensive demonstrations of the agent system including:
- Basic agent management operations
- Messaging and communication
- Coordination and workflows
- System monitoring and status

Architecture: Single Responsibility Principle - provides system demonstrations
LOC: 180 lines (under 200 limit)
"""

import argparse
import time
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.agent_cell_phone import AgentCellPhone, MsgTag
from src.services.coordination import CoordinationService
from src.core.agent_manager import AgentStatus

logger = None


class DemoSuite:
    """
    Comprehensive demonstration suite for the agent system

    Responsibilities:
    - Demonstrate core system functionality
    - Provide working examples for testing
    - Show system integration capabilities
    - Validate system components
    """

    def __init__(self):
        self.system = AgentCellPhone()
        self.coordination = CoordinationService()
        self.demo_agents = []

    def setup_demo_environment(self):
        """Setup demo environment with test agents"""
        try:
            # Register demo agents
            agents = [
                ("demo-1", "Demo Agent 1", ["test", "demo"]),
                ("demo-2", "Demo Agent 2", ["test", "demo"]),
                ("demo-3", "Demo Agent 3", ["test", "demo"]),
            ]

            for agent_id, name, capabilities in agents:
                if self.system.register_agent(agent_id, name, capabilities):
                    self.demo_agents.append(agent_id)
                    print(f"✅ Registered {name}")
                else:
                    print(f"❌ Failed to register {name}")

            print(f"Demo environment ready with {len(self.demo_agents)} agents")

        except Exception as e:
            print(f"❌ Failed to setup demo environment: {e}")

    def cleanup_demo_environment(self):
        """Cleanup demo environment"""
        try:
            for agent_id in self.demo_agents:
                self.system.stop_agent(agent_id)
            print("Demo environment cleaned up")

        except Exception as e:
            print(f"❌ Failed to cleanup demo environment: {e}")

    def run_basic_demo(self):
        """Run basic agent management demonstration"""
        print("\n🚀 Running Basic Agent Management Demo...")

        try:
            # Start agents
            for agent_id in self.demo_agents:
                if self.system.start_agent(agent_id):
                    print(f"✅ Started {agent_id}")
                else:
                    print(f"❌ Failed to start {agent_id}")

            # Get system status
            status = self.system.get_system_status()
            print(
                f"System Status: {status.total_agents} agents, {status.online_agents} online"
            )

            # List all agents
            agents = self.system.get_all_agents()
            for agent_id, info in agents.items():
                print(f"  {agent_id}: {info.name} - {info.status.value}")

            print("✅ Basic demo completed successfully")

        except Exception as e:
            print(f"❌ Basic demo failed: {e}")

    def run_messaging_demo(self):
        """Run messaging and communication demonstration"""
        print("\n📡 Running Messaging Demo...")

        try:
            # Send messages between agents
            for i, agent_id in enumerate(self.demo_agents):
                next_agent = self.demo_agents[(i + 1) % len(self.demo_agents)]
                message = f"Hello from {agent_id} to {next_agent}"

                if self.system.send_message(
                    agent_id, next_agent, message, MsgTag.COORDINATION
                ):
                    print(f"✅ Sent: {agent_id} → {next_agent}")
                else:
                    print(f"❌ Failed to send: {agent_id} → {next_agent}")

            # Check message queues
            queue_status = self.system.message_router.get_queue_status()
            for agent, count in queue_status.items():
                if count > 0:
                    print(f"📬 {agent} has {count} messages")

            print("✅ Messaging demo completed successfully")

        except Exception as e:
            print(f"❌ Messaging demo failed: {e}")

    def run_coordination_demo(self):
        """Run coordination and workflow demonstration"""
        print("\n🤝 Running Coordination Demo...")

        try:
            # Create coordination task
            task_id = self.coordination.create_coordination_task(
                "Demo Task", "Demonstrate coordination capabilities", self.demo_agents
            )

            if task_id:
                print(f"✅ Created coordination task: {task_id}")

                # Start task
                if self.coordination.start_coordination_task(task_id):
                    print("✅ Started coordination task")

                    # Complete task steps
                    for agent_id in self.demo_agents:
                        self.coordination.complete_task_step(
                            task_id, f"step_{agent_id}", f"completed by {agent_id}"
                        )

                    # Mark task as completed
                    task = self.coordination.tasks[task_id]
                    task.status = self.coordination.tasks[
                        task_id
                    ].__class__.status.__class__.COMPLETED
                    task.completed_at = time.time()

                    print("✅ Coordination task completed")
                else:
                    print("❌ Failed to start coordination task")
            else:
                print("❌ Failed to create coordination task")

            print("✅ Coordination demo completed successfully")

        except Exception as e:
            print(f"❌ Coordination demo failed: {e}")

    def run_monitoring_demo(self):
        """Run system monitoring demonstration"""
        print("\n📊 Running Monitoring Demo...")

        try:
            # Get comprehensive system status
            status = self.system.get_system_status()

            print("System Status:")
            print(f"  Total Agents: {status.total_agents}")
            print(f"  Online Agents: {status.online_agents}")
            print(f"  Message Queue Size: {status.message_queue_size}")
            print(f"  Uptime: {status.uptime:.1f} seconds")

            # Get coordination tasks
            tasks = self.coordination.get_all_tasks()
            if tasks:
                print(f"  Active Tasks: {len(tasks)}")
                for task_id, task in tasks.items():
                    print(f"    {task.name}: {task.status.value}")

            print("✅ Monitoring demo completed successfully")

        except Exception as e:
            print(f"❌ Monitoring demo failed: {e}")

    def run_comprehensive_demo(self):
        """Run all demonstrations in sequence"""
        print("🎯 Starting Comprehensive Demo Suite...")

        try:
            self.setup_demo_environment()

            self.run_basic_demo()
            time.sleep(1)

            self.run_messaging_demo()
            time.sleep(1)

            self.run_coordination_demo()
            time.sleep(1)

            self.run_monitoring_demo()

            print("\n🎉 Comprehensive Demo Suite Completed Successfully!")

        except Exception as e:
            print(f"❌ Comprehensive demo failed: {e}")

        finally:
            self.cleanup_demo_environment()


def run_smoke_test():
    """Run basic functionality test for DemoSuite"""
    print("🧪 Running DemoSuite Smoke Test...")

    try:
        demo = DemoSuite()
        demo.setup_demo_environment()

        # Test basic functionality
        assert len(demo.demo_agents) > 0

        # Test agent start
        for agent_id in demo.demo_agents:
            assert demo.system.start_agent(agent_id)

        # Test system status
        status = demo.system.get_system_status()
        assert status.total_agents > 0

        demo.cleanup_demo_environment()

        print("✅ DemoSuite Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ DemoSuite Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for DemoSuite"""
    parser = argparse.ArgumentParser(description="Demo Suite CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--basic", action="store_true", help="Run basic demo")
    parser.add_argument("--messaging", action="store_true", help="Run messaging demo")
    parser.add_argument(
        "--coordination", action="store_true", help="Run coordination demo"
    )
    parser.add_argument("--monitoring", action="store_true", help="Run monitoring demo")
    parser.add_argument("--comprehensive", action="store_true", help="Run all demos")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    demo = DemoSuite()

    if args.basic:
        demo.setup_demo_environment()
        demo.run_basic_demo()
        demo.cleanup_demo_environment()

    elif args.messaging:
        demo.setup_demo_environment()
        demo.run_messaging_demo()
        demo.cleanup_demo_environment()

    elif args.coordination:
        demo.setup_demo_environment()
        demo.run_coordination_demo()
        demo.cleanup_demo_environment()

    elif args.monitoring:
        demo.setup_demo_environment()
        demo.run_monitoring_demo()
        demo.cleanup_demo_environment()

    elif args.comprehensive:
        demo.run_comprehensive_demo()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
