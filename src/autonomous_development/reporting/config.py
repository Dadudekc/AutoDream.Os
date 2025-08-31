
# MIGRATED: This file has been migrated to the centralized configuration system
"""Reporting module configuration constants.

This module provides a single source of truth for templates, icon
mappings and filesystem paths used by the reporting subsystem.
"""
from __future__ import annotations

from typing import Dict

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
# Directory where report artifacts can be persisted if a file based backend
# is used.  Modules can import this constant instead of hard coding paths.
DEFAULT_REPORT_ARCHIVE_PATH = "reports"

# ---------------------------------------------------------------------------
# Icon mappings
# ---------------------------------------------------------------------------
PRIORITY_ICONS: Dict[str, str] = {
    "high": "🔴",
    "medium": "🟡",
    "low": "🟢",
}

COMPLEXITY_ICONS: Dict[str, str] = {
    "high": "🔥",
    "medium": "⚡",
    "low": "💡",
}

STATUS_ICONS: Dict[str, str] = {
    "available": "🟢",
    "claimed": "🟡",
    "in_progress": "🔄",
    "completed": "✅",
    "blocked": "🚫",
}

# ---------------------------------------------------------------------------
# Message templates
# ---------------------------------------------------------------------------
# These templates are used by the formatting helpers.  Keeping them here
# avoids duplication and makes it easy to tweak messaging from one place.
WORKFLOW_START_TEMPLATE = """🚀 AUTONOMOUS OVERNIGHT DEVELOPMENT WORKFLOW STARTED!

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

AGENT1_TEMPLATE = """🎯 AGENT-1: You are now the Task Manager!

Your responsibilities:
1. 📋 Monitor task list and create new tasks as needed
2. 📊 Track progress and identify bottlenecks
3. 🔄 Coordinate workflow and resolve conflicts
4. 📈 Optimize task distribution and priorities
5. 🚨 Handle emergencies and blocked tasks

Start by reviewing the current task list and identifying areas for improvement!"""

NO_TASKS_TEMPLATE = """📋 NO TASKS AVAILABLE

🎯 All current tasks have been claimed or completed!
⏰ Waiting for Agent-1 to create new tasks...

🔄 Next cycle will focus on:
   • Progress monitoring
   • Task completion
   • New task creation by Agent-1

Stay ready for new development opportunities! 🚀"""

TASK_CLAIMED_TEMPLATE = """🎯 TASK CLAIMED: {title}

📋 Task Details:
   • ID: {task_id}
   • Priority: {priority}
   • Complexity: {complexity}
   • Estimated Time: {estimated_hours}h
   • Required Skills: {skills}

🚀 Status: Ready to start work
⏰ Next: Begin task execution in next cycle

Good luck with your autonomous development! 🚀"""

PROGRESS_UPDATE_BLOCKERS_TEMPLATE = """⚠️ PROGRESS UPDATE - BLOCKERS DETECTED

📊 Task: {title}
📈 Progress: {progress:.1f}%
🚫 Blockers: {blockers}

🔧 Action Required: Address blockers before continuing
⏰ Next Update: In next cycle"""

PROGRESS_UPDATE_TEMPLATE = """📊 PROGRESS UPDATE

📋 Task: {title}
📈 Progress: {progress:.1f}%
✅ Status: Making good progress

🚀 Continue autonomous development!
⏰ Next Update: In next cycle"""

WORKFLOW_COMPLETE_TEMPLATE = """🌅 OVERNIGHT WORKFLOW COMPLETE

📊 Final Summary:
   • Total Cycles: {overnight_cycles}
   • Autonomous Hours: {autonomous_hours}
   • Tasks Completed: {total_tasks_completed}

🎯 Great work on autonomous development!
🔄 System ready for next overnight session

Good morning! ☀️"""

REMAINING_TASKS_TEMPLATE = "📋 {count} tasks still available for claiming in next cycle."

__all__ = [
    "DEFAULT_REPORT_ARCHIVE_PATH",
    "PRIORITY_ICONS",
    "COMPLEXITY_ICONS",
    "STATUS_ICONS",
    "WORKFLOW_START_TEMPLATE",
    "AGENT1_TEMPLATE",
    "NO_TASKS_TEMPLATE",
    "TASK_CLAIMED_TEMPLATE",
    "PROGRESS_UPDATE_BLOCKERS_TEMPLATE",
    "PROGRESS_UPDATE_TEMPLATE",
    "WORKFLOW_COMPLETE_TEMPLATE",
    "REMAINING_TASKS_TEMPLATE",
]
