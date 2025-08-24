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
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from datetime import datetime, timedelta
import random

from core.task_manager import DevelopmentTaskManager as TaskManager
from autonomous_development.core import DevelopmentTask

# Import our existing communication system
from core.real_agent_communication_system import RealAgentCommunicationSystem




class AutonomousWorkflowManager:
    """Manages autonomous overnight development workflow"""

    def __init__(
        self, comm_system: RealAgentCommunicationSystem, task_manager: TaskManager
    ):
        self.comm_system = comm_system
        self.task_manager = task_manager
        self.logger = logging.getLogger(__name__)
        self.workflow_active = False
        self.cycle_duration = 3600  # 1 hour cycles
        self.agent_workloads = {}

        # Initialize agent workloads
        for i in range(2, 9):  # Agents 2-8
            agent_id = f"Agent-{i}"
            self.agent_workloads[agent_id] = {
                "current_task": None,
                "completed_tasks": [],
                "total_hours_worked": 0.0,
                "skills": self._generate_agent_skills(agent_id),
                "availability": "available",
            }

    def _generate_agent_skills(self, agent_id: str) -> List[str]:
        """Generate skills for each agent"""
        all_skills = [
            "git",
            "code_analysis",
            "optimization",
            "documentation",
            "markdown",
            "api_docs",
            "debugging",
            "testing",
            "feature_development",
            "performance_analysis",
            "profiling",
            "test_automation",
            "coverage_analysis",
            "code_review",
            "refactoring",
            "architecture",
            "dependency_management",
            "compatibility_testing",
            "security_analysis",
            "vulnerability_assessment",
            "security_fixes",
        ]

        # Each agent gets 5-8 random skills
        num_skills = random.randint(5, 8)
        return random.sample(all_skills, num_skills)

    async def start_overnight_workflow(self) -> bool:
        """Start autonomous overnight development workflow"""
        self.logger.info("🌙 Starting autonomous overnight development workflow...")
        self.workflow_active = True

        # Initial broadcast to all agents
        await self._broadcast_workflow_start()

        # Start continuous workflow cycle
        try:
            while self.workflow_active:
                await self._execute_workflow_cycle()
                await asyncio.sleep(self.cycle_duration)
        except Exception as e:
            self.logger.error(f"❌ Workflow error: {e}")
            self.workflow_active = False
            return False

        return True

    async def _broadcast_workflow_start(self):
        """Broadcast workflow start message"""
        message = """🚀 AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED!

📋 AGENT-1: Task Manager Role
   - Building and updating task list
   - Monitoring progress and coordination
   - Managing task priorities

🔍 AGENTS 2-8: Autonomous Workforce
   - Review available tasks
   - Claim tasks based on skills and availability
   - Work autonomously and report progress
   - Complete tasks and claim new ones

🔄 WORKFLOW CYCLE:
   1. Task review and claiming
   2. Autonomous work execution
   3. Progress reporting
   4. Task completion and new task claiming
   5. Repeat cycle

⏰ CYCLE DURATION: 1 hour
🌙 OPERATION: Continuous overnight
🎯 GOAL: Maximize autonomous development progress

Ready to begin autonomous development! 🚀"""

        # Send to all agents with line breaks
        await self.comm_system.send_message_to_all_agents_with_line_breaks(message)

        # Special message to Agent-1 with line breaks
        agent1_message = """🎯 AGENT-1: You are now the Task Manager!

Your responsibilities:
1. 📋 Monitor task list and create new tasks as needed
2. 📊 Track progress and identify bottlenecks
3. 🔄 Coordinate workflow and resolve conflicts
4. 📈 Optimize task distribution and priorities
5. 🚨 Handle emergencies and blocked tasks

Start by reviewing the current task list and identifying areas for improvement!"""

        await self.comm_system.send_message_to_agent_with_line_breaks(
            "Agent-1", agent1_message, "workspace_box"
        )

    async def _execute_workflow_cycle(self):
        """Execute one workflow cycle"""
        self.logger.info("🔄 Executing workflow cycle...")

        # Update workflow stats
        self.task_manager.workflow_stats["overnight_cycles"] += 1
        self.task_manager.workflow_stats["autonomous_hours"] += 1

        # 1. Task Review and Claiming Phase
        await self._task_review_and_claiming_phase()

        # 2. Work Execution Phase
        await self._work_execution_phase()

        # 3. Progress Reporting Phase
        await self._progress_reporting_phase()

        # 4. Cycle Summary
        await self._cycle_summary_phase()

    async def _task_review_and_claiming_phase(self):
        """Phase 1: Agents review and claim tasks"""
        self.logger.info("📋 Phase 1: Task Review and Claiming")

        available_tasks = self.task_manager.get_available_tasks()
        if not available_tasks:
            await self._broadcast_no_tasks_available()
            return

        # Broadcast available tasks to Agents 2-8 with line breaks
        task_list_message = self._format_task_list_for_agents(available_tasks)
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📋 AVAILABLE TASKS FOR CLAIMING:\n\n{task_list_message}", "workspace_box"
        )

        # Simulate autonomous task claiming
        await self._simulate_autonomous_task_claiming(available_tasks)

    async def _work_execution_phase(self):
        """Phase 2: Agents work on claimed tasks"""
        self.logger.info("🚀 Phase 2: Work Execution")

        # Get all claimed and in-progress tasks
        active_tasks = [
            t
            for t in self.task_manager.tasks.values()
            if t.status in ["claimed", "in_progress"]
        ]

        if not active_tasks:
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                "⏸️ No active tasks to work on. Waiting for new tasks...", "status_box"
            )
            return

        # Simulate work progress
        await self._simulate_work_progress(active_tasks)

    async def _progress_reporting_phase(self):
        """Phase 3: Agents report progress"""
        self.logger.info("📊 Phase 3: Progress Reporting")

        # Get progress updates from all active tasks
        progress_message = self._format_progress_summary()
        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            f"📊 PROGRESS SUMMARY:\n\n{progress_message}", "status_box"
        )

    async def _cycle_summary_phase(self):
        """Phase 4: Cycle summary and next steps"""
        self.logger.info("📈 Phase 4: Cycle Summary")

        summary = self.task_manager.get_task_summary()
        cycle_message = f"""🔄 CYCLE COMPLETE - SUMMARY:

📊 Task Status:
   • Total Tasks: {summary['total_tasks']}
   • Available: {summary['available_tasks']}
   • Claimed: {summary['claimed_tasks']}
   • In Progress: {summary['in_progress_tasks']}
   • Completed: {summary['completed_tasks']}
   • Completion Rate: {summary['completion_rate']:.1f}%

⏰ Overnight Progress:
   • Cycles Completed: {summary['workflow_stats']['overnight_cycles']}
   • Autonomous Hours: {summary['workflow_stats']['autonomous_hours']}
   • Total Tasks Completed: {summary['workflow_stats']['total_tasks_completed']}

🎯 Next Cycle: Task review and claiming phase begins..."""

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            cycle_message, "workspace_box"
        )

    def _format_task_list_for_agents(self, tasks: List[DevelopmentTask]) -> str:
        """Format task list for agent review"""
        if not tasks:
            return "No tasks available for claiming."

        task_lines = []
        for task in sorted(tasks, key=lambda t: t.priority, reverse=True):
            priority_icon = (
                "🔴" if task.priority >= 8 else "🟡" if task.priority >= 5 else "🟢"
            )
            complexity_icon = (
                "🔥"
                if task.complexity == "high"
                else "⚡"
                if task.complexity == "medium"
                else "💡"
            )

            task_lines.append(
                f"{priority_icon} **{task.title}** (Priority: {task.priority})\n"
                f"   {complexity_icon} Complexity: {task.complexity.title()}\n"
                f"   ⏱️ Estimated: {task.estimated_hours}h\n"
                f"   🎯 Skills: {', '.join(task.required_skills)}\n"
                f"   📝 {task.description}\n"
                f"   🆔 Task ID: {task.task_id}\n"
            )

        return "\n".join(task_lines)

    async def _simulate_autonomous_task_claiming(
        self, available_tasks: List[DevelopmentTask]
    ):
        """Simulate agents autonomously claiming tasks"""
        self.logger.info("🎯 Simulating autonomous task claiming...")

        # Simulate Agents 2-8 claiming tasks based on skills
        for agent_id in [f"Agent-{i}" for i in range(2, 9)]:
            if not available_tasks:
                break

            # Find best matching task for this agent
            best_task = self._find_best_task_for_agent(agent_id, available_tasks)
            if best_task:
                # Claim the task
                if self.task_manager.claim_task(best_task.task_id, agent_id):
                    available_tasks.remove(best_task)

                    # Notify agent of claimed task with proper line breaks
                    claim_message = f"""🎯 TASK CLAIMED: {best_task.title}

📋 Task Details:
   • ID: {best_task.task_id}
   • Priority: {best_task.priority}
   • Complexity: {best_task.complexity}
   • Estimated Time: {best_task.estimated_hours}h
   • Required Skills: {', '.join(best_task.required_skills)}

🚀 Status: Ready to start work
⏰ Next: Begin task execution in next cycle

Good luck with your autonomous development! 🚀"""

                    # Send with line break handling
                    await self.comm_system.send_message_to_agent_with_line_breaks(
                        agent_id, claim_message, "workspace_box"
                    )

                    self.logger.info(f"✅ {agent_id} claimed task {best_task.task_id}")

        # Update remaining available tasks
        remaining_count = len(available_tasks)
        if remaining_count > 0:
            await self.comm_system.send_message_to_all_agents_with_line_breaks(
                f"📋 {remaining_count} tasks still available for claiming in next cycle.",
                "status_box",
            )

    def _find_best_task_for_agent(
        self, agent_id: str, available_tasks: List[DevelopmentTask]
    ) -> Optional[DevelopmentTask]:
        """Find the best matching task for an agent based on skills and preferences"""
        agent_skills = self.agent_workloads[agent_id]["skills"]

        # Score tasks based on skill match and priority
        scored_tasks = []
        for task in available_tasks:
            skill_match = len(set(agent_skills) & set(task.required_skills))
            priority_score = task.priority
            complexity_bonus = (
                2
                if task.complexity == "medium"
                else 3
                if task.complexity == "high"
                else 1
            )

            total_score = (skill_match * 10) + priority_score + complexity_bonus
            scored_tasks.append((task, total_score))

        # Return highest scoring task
        if scored_tasks:
            scored_tasks.sort(key=lambda x: x[1], reverse=True)
            return scored_tasks[0][0]

        return None

    async def _simulate_work_progress(self, active_tasks: List[DevelopmentTask]):
        """Simulate agents working on claimed tasks"""
        self.logger.info("🚀 Simulating work progress...")

        for task in active_tasks:
            if task.status == "claimed":
                # Start work on claimed task
                self.task_manager.start_task_work(task.task_id)

            if task.status == "in_progress":
                # Simulate progress
                current_progress = task.progress_percentage
                progress_increment = random.uniform(
                    10.0, 30.0
                )  # 10-30% progress per cycle
                new_progress = min(100.0, current_progress + progress_increment)

                # Random blockers
                blockers = []
                if random.random() < 0.2:  # 20% chance of blocker
                    possible_blockers = [
                        "Waiting for dependency update",
                        "Need clarification on requirements",
                        "Technical issue encountered",
                        "Waiting for code review",
                        "Integration testing needed",
                    ]
                    blockers = random.sample(possible_blockers, random.randint(1, 2))

                self.task_manager.update_task_progress(
                    task.task_id, new_progress, blockers
                )

                # Notify agent of progress
                if blockers:
                    progress_message = f"""⚠️ PROGRESS UPDATE - BLOCKERS DETECTED

📊 Task: {task.title}
📈 Progress: {new_progress:.1f}%
🚫 Blockers: {', '.join(blockers)}

🔧 Action Required: Address blockers before continuing
⏰ Next Update: In next cycle"""
                else:
                    progress_message = f"""📊 PROGRESS UPDATE

📋 Task: {task.title}
📈 Progress: {new_progress:.1f}%
✅ Status: Making good progress

🚀 Continue autonomous development!
⏰ Next Update: In next cycle"""

                await self.comm_system.send_message_to_agent(
                    task.claimed_by, progress_message, "status_box"
                )

    def _format_progress_summary(self) -> str:
        """Format progress summary for all agents"""
        active_tasks = [
            t
            for t in self.task_manager.tasks.values()
            if t.status in ["claimed", "in_progress"]
        ]

        if not active_tasks:
            return "No active tasks to report progress on."

        progress_lines = []
        for task in active_tasks:
            status_icon = "🔄" if task.status == "in_progress" else "⏳"
            progress_lines.append(
                f"{status_icon} **{task.title}** (Agent: {task.claimed_by})\n"
                f"   📊 Progress: {task.progress_percentage:.1f}%\n"
                f"   🚫 Blockers: {', '.join(task.blockers) if task.blockers else 'None'}\n"
            )

        return "\n".join(progress_lines)

    async def _broadcast_no_tasks_available(self):
        """Broadcast when no tasks are available"""
        message = """📋 NO TASKS AVAILABLE

🎯 All current tasks have been claimed or completed!
⏰ Waiting for Agent-1 to create new tasks...

🔄 Next cycle will focus on:
   • Progress monitoring
   • Task completion
   • New task creation by Agent-1

Stay ready for new development opportunities! 🚀"""

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            message, "status_box"
        )

    async def stop_overnight_workflow(self):
        """Stop autonomous overnight workflow"""
        self.logger.info("🛑 Stopping autonomous overnight workflow...")
        self.workflow_active = False

        # Final broadcast
        final_message = """🌅 OVERNIGHT WORKFLOW COMPLETE

📊 Final Summary:
   • Total Cycles: {self.task_manager.workflow_stats['overnight_cycles']}
   • Autonomous Hours: {self.task_manager.workflow_stats['autonomous_hours']}
   • Tasks Completed: {self.task_manager.workflow_stats['total_tasks_completed']}

🎯 Great work on autonomous development!
🔄 System ready for next overnight session

Good morning! ☀️"""

        await self.comm_system.send_message_to_all_agents_with_line_breaks(
            final_message, "workspace_box"
        )


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
    comm_system = RealAgentCommunicationSystem()
    task_manager = TaskManager()
    workflow_manager = AutonomousWorkflowManager(comm_system, task_manager)

    # Handle different CLI modes
    if args.start_overnight:
        # Start overnight autonomous workflow
        print("🌙 Starting autonomous overnight development workflow...")
        print("This will run continuously until stopped.")
        print("Press Ctrl+C to stop the workflow.\n")

        try:
            success = await workflow_manager.start_overnight_workflow()
            if success:
                print("✅ Overnight workflow completed successfully!")
            else:
                print("❌ Overnight workflow failed!")
        except KeyboardInterrupt:
            print("\n🛑 Stopping overnight workflow...")
            await workflow_manager.stop_overnight_workflow()
            print("✅ Overnight workflow stopped.")

        sys.exit(0)

    elif args.show_tasks:
        # Show current task status
        print("📋 Current Development Task Status:")
        print("=" * 60)

        summary = task_manager.get_task_summary()
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Available: {summary['available_tasks']}")
        print(f"Claimed: {summary['claimed_tasks']}")
        print(f"In Progress: {summary['in_progress_tasks']}")
        print(f"Completed: {summary['completed_tasks']}")
        print(f"Completion Rate: {summary['completion_rate']:.1f}%")

        print("\n📊 Detailed Task List:")
        for task in task_manager.tasks.values():
            status_icon = {
                "available": "🟢",
                "claimed": "🟡",
                "in_progress": "🔄",
                "completed": "✅",
                "blocked": "🚫",
            }.get(task.status, "❓")

            print(f"{status_icon} {task.task_id}: {task.title}")
            print(f"   Status: {task.status}")
            if task.claimed_by:
                print(f"   Agent: {task.claimed_by}")
            if task.progress_percentage > 0:
                print(f"   Progress: {task.progress_percentage:.1f}%")
            print()

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

            # Generate skills based on complexity
            skills = []
            if complexity == "low":
                skills = random.sample(
                    ["documentation", "markdown", "testing", "git"], 2
                )
            elif complexity == "medium":
                skills = random.sample(
                    ["code_analysis", "optimization", "debugging", "refactoring"], 3
                )
            else:  # high
                skills = random.sample(
                    [
                        "performance_analysis",
                        "security_analysis",
                        "architecture",
                        "profiling",
                    ],
                    4,
                )

            task_id = task_manager.create_task(
                title=title,
                description=description,
                complexity=complexity,
                priority=priority,
                estimated_hours=hours,
                required_skills=skills,
            )

            print(f"✅ Created task {task_id}: {title}")
            print(f"   Complexity: {complexity}")
            print(f"   Priority: {priority}")
            print(f"   Estimated Hours: {hours}")
            print(f"   Required Skills: {', '.join(skills)}")

        except ValueError:
            print("❌ Invalid priority or hours value")
            sys.exit(1)

        sys.exit(0)

    elif args.show_stats:
        # Show workflow statistics
        print("📊 Autonomous Development Workflow Statistics:")
        print("=" * 60)

        summary = task_manager.get_task_summary()
        stats = summary["workflow_stats"]

        print(f"📋 Task Statistics:")
        print(f"   Total Tasks Created: {stats['total_tasks_created']}")
        print(f"   Total Tasks Completed: {stats['total_tasks_completed']}")
        print(f"   Total Tasks Claimed: {stats['total_tasks_claimed']}")

        print(f"\n🌙 Overnight Statistics:")
        print(f"   Overnight Cycles: {stats['overnight_cycles']}")
        print(f"   Autonomous Hours: {stats['autonomous_hours']}")

        if stats["total_tasks_created"] > 0:
            completion_rate = (
                stats["total_tasks_completed"] / stats["total_tasks_created"]
            ) * 100
            print(f"   Overall Completion Rate: {completion_rate:.1f}%")

        sys.exit(0)

    elif args.test_workflow:
        # Test autonomous workflow with short cycles
        print("🧪 Testing autonomous workflow with short cycles...")
        print("This will run 3 test cycles with 30-second intervals.\n")

        # Temporarily set short cycle duration for testing
        original_cycle_duration = workflow_manager.cycle_duration
        workflow_manager.cycle_duration = 30  # 30 seconds for testing

        try:
            # Run 3 test cycles
            for cycle in range(1, 4):
                print(f"🔄 Test Cycle {cycle}/3 starting...")
                await workflow_manager._execute_workflow_cycle()

                if cycle < 3:
                    print(f"⏰ Waiting 30 seconds before next cycle...")
                    await asyncio.sleep(30)

            print("✅ Test workflow completed successfully!")

        except Exception as e:
            print(f"❌ Test workflow failed: {e}")
        finally:
            # Restore original cycle duration
            workflow_manager.cycle_duration = original_cycle_duration

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
        summary = task_manager.get_task_summary()
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
