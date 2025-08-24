#!/usr/bin/env python3
"""
Autonomous Development System - Overnight Agent Coordination
===========================================================

This system enables agents to work autonomously overnight with:
- Task list management by Agent-1
- Autonomous task claiming by Agents 2-8
- Continuous workflow without human intervention
- Progress monitoring and reporting
- Self-managing development cycles

Features:
- Task prioritization and complexity assessment
- Autonomous task claiming system
- Progress tracking and reporting
- Continuous overnight operation
- Agent coordination and conflict resolution
"""

import asyncio
import json
import time
import logging
import argparse
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime, timedelta
import random

# Use type hints with strings to avoid circular imports
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.task_manager import DevelopmentTaskManager as TaskManager
    from src.autonomous_development.core import DevelopmentTask
    from src.services.messaging import UnifiedMessagingService as RealAgentCommunicationSystem

# Import our unified messaging system
from src.services.messaging import UnifiedMessagingService as RealAgentCommunicationSystem  # Backward compatibility alias

# Import extracted modules
from autonomous_development.workflow.manager import AutonomousWorkflowManager
from autonomous_development.agents.coordinator import AgentCoordinator
from autonomous_development.tasks.handler import TaskHandler
from autonomous_development.reporting.manager import ReportingManager


class AutonomousDevelopmentSystem:
    """Main autonomous development system that orchestrates all modules"""

    def __init__(self):
        self.comm_system = RealAgentCommunicationSystem()
        # Initialize task manager dynamically to avoid circular imports
        from src.core.task_manager import DevelopmentTaskManager as TaskManager
        self.task_manager = TaskManager()
        self.workflow_manager = AutonomousWorkflowManager(self.comm_system, self.task_manager)
        self.agent_coordinator = AgentCoordinator()
        self.task_handler = TaskHandler(self.task_manager)
        self.reporting_manager = ReportingManager(self.task_manager)
        self.logger = logging.getLogger(__name__)

    async def start_overnight_workflow(self) -> bool:
        """Start autonomous overnight development workflow"""
        return await self.workflow_manager.start_overnight_workflow()

    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        await self.workflow_manager.stop_overnight_workflow()

    def get_task_summary(self) -> Dict[str, Any]:
        """Get current task summary"""
        return self.task_manager.get_task_summary()

    def create_development_task(
        self,
        title: str,
        description: str,
        complexity: str,
        priority: int,
        estimated_hours: float,
        required_skills: List[str] = None,
    ) -> str:
        """Create a new development task"""
        return self.task_handler.create_development_task(
            title, description, complexity, priority, estimated_hours, required_skills
        )

    def get_agent_workload_summary(self, agent_id: str) -> Dict[str, Any]:
        """Get workload summary for a specific agent"""
        return self.agent_coordinator.get_agent_workload_summary(agent_id)

    def get_all_agents_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get workload summary for all agents"""
        return self.agent_coordinator.get_all_agents_summary()

    def get_task_statistics(self) -> Dict[str, Any]:
        """Get comprehensive task statistics"""
        return self.task_handler.get_task_statistics()

    def generate_performance_report(self) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        return self.reporting_manager.generate_performance_report()


class CLIInterface:
    """Command-line interface for autonomous development system"""

    def __init__(self):
        self.parser = self.setup_argument_parser()

    def setup_argument_parser(self):
        """Setup command-line argument parser"""
        parser = argparse.ArgumentParser(
            description="Autonomous Development System - Overnight Agent Coordination",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Examples:
  # Start overnight autonomous workflow
  python autonomous_development_system.py --start-overnight

  # Show current task status
  python autonomous_development_system.py --show-tasks

  # Create new development task
  python autonomous_development_system.py --create-task "Task Title" "Description" medium 8 2.5

  # Show workflow statistics
  python autonomous_development_system.py --show-stats

  # Test autonomous workflow (short cycle)
  python autonomous_development_system.py --test-workflow
            """,
        )

        # Main operation modes
        parser.add_argument(
            "--start-overnight",
            action="store_true",
            help="Start autonomous overnight development workflow",
        )
        parser.add_argument(
            "--show-tasks",
            action="store_true",
            help="Show current task status and progress",
        )
        parser.add_argument(
            "--create-task",
            nargs=5,
            metavar=("TITLE", "DESCRIPTION", "COMPLEXITY", "PRIORITY", "HOURS"),
            help="Create new development task",
        )
        parser.add_argument(
            "--show-stats", action="store_true", help="Show workflow statistics"
        )
        parser.add_argument(
            "--test-workflow",
            action="store_true",
            help="Test autonomous workflow with short cycles",
        )

        return parser

    def parse_arguments(self):
        """Parse command-line arguments"""
        return self.parser.parse_args()

    def display_help(self):
        """Display help information"""
        self.parser.print_help()


async def main():
    """Main function for autonomous development system"""
    cli = CLIInterface()
    args = cli.parse_arguments()

    # Initialize the autonomous development system
    system = AutonomousDevelopmentSystem()

    # Handle different CLI modes
    if args.start_overnight:
        # Start overnight autonomous workflow
        print("🌙 Starting autonomous overnight development workflow...")
        print("This will run continuously until stopped.")
        print("Press Ctrl+C to stop the workflow.\n")

        try:
            success = await system.start_overnight_workflow()
            if success:
                print("✅ Overnight workflow completed successfully!")
            else:
                print("❌ Overnight workflow failed!")
        except KeyboardInterrupt:
            print("\n🛑 Stopping overnight workflow...")
            await system.stop_overnight_workflow()
            print("✅ Overnight workflow stopped.")

        sys.exit(0)

    elif args.show_tasks:
        # Show current task status
        print(system.reporting_manager.format_detailed_task_status())
        sys.exit(0)

    elif args.create_task:
        # Create new development task
        title, description, complexity, priority, hours = args.create_task

        try:
            priority = int(priority)
            hours = float(hours)

            if complexity not in ["low", "medium", "high"]:
                print("❌ Complexity must be 'low', 'medium', or 'high'")
                sys.exit(1)

            if not (1 <= priority <= 10):
                print("❌ Priority must be between 1 and 10")
                sys.exit(1)

            if hours <= 0:
                print("❌ Hours must be positive")
                sys.exit(1)

            task_id = system.create_development_task(
                title=title,
                description=description,
                complexity=complexity,
                priority=priority,
                estimated_hours=hours,
            )

            print(f"✅ Created task {task_id}: {title}")
            print(f"   Complexity: {complexity}")
            print(f"   Priority: {priority}")
            print(f"   Estimated Hours: {hours}")

        except ValueError:
            print("❌ Invalid priority or hours value")
            sys.exit(1)

        sys.exit(0)

    elif args.show_stats:
        # Show workflow statistics
        print(system.reporting_manager.format_workflow_statistics())
        sys.exit(0)

    elif args.test_workflow:
        # Test autonomous workflow with short cycles
        print("🧪 Testing autonomous workflow with short cycles...")
        print("This will run 3 test cycles with 30-second intervals.\n")

        # Temporarily set short cycle duration for testing
        original_cycle_duration = system.workflow_manager.cycle_duration
        system.workflow_manager.cycle_duration = 30  # 30 seconds for testing

        try:
            # Run 3 test cycles
            for cycle in range(1, 4):
                print(f"🔄 Test Cycle {cycle}/3 starting...")
                await system.workflow_manager._execute_workflow_cycle()

                if cycle < 3:
                    print(f"⏰ Waiting 30 seconds before next cycle...")
                    await asyncio.sleep(30)

            print("✅ Test workflow completed successfully!")

        except Exception as e:
            print(f"❌ Test workflow failed: {e}")
        finally:
            # Restore original cycle duration
            system.workflow_manager.cycle_duration = original_cycle_duration

        sys.exit(0)

    else:
        # Interactive mode (default)
        print("🌙 AUTONOMOUS DEVELOPMENT SYSTEM - OVERNIGHT AGENT COORDINATION")
        print("=" * 80)
        print("This system enables agents to work autonomously overnight with:")
        print("• Task list management by Agent-1")
        print("• Autonomous task claiming by Agents 2-8")
        print("• Continuous workflow without human intervention")
        print("• Progress monitoring and reporting")
        print("• Self-managing development cycles")
        print("=" * 80)

        # Show current system status
        summary = system.get_task_summary()
        print(f"📊 Current System Status:")
        print(f"   Total Tasks: {summary['total_tasks']}")
        print(f"   Available: {summary['available_tasks']}")
        print(f"   In Progress: {summary['in_progress_tasks']}")
        print(f"   Completed: {summary['completed_tasks']}")

        print(f"\n🎯 Available Commands:")
        print(f"   --start-overnight    Start autonomous overnight workflow")
        print(f"   --show-tasks         Show current task status")
        print(f"   --create-task        Create new development task")
        print(f"   --show-stats         Show workflow statistics")
        print(f"   --test-workflow      Test autonomous workflow")

        print(f"\n🚀 Ready for autonomous development!")
        return "SUCCESS"


if __name__ == "__main__":
    print("🌙 Starting Autonomous Development System...")
    print("This system enables overnight autonomous agent coordination!")
    print("Use --help for command-line options.\n")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⚠️ System interrupted by user")
    except Exception as e:
        print(f"\n❌ System failed with error: {e}")
        sys.exit(1)
