#!/usr/bin/env python3
"""
Swarm Workflow Orchestrator - Utils
====================================

Utility functions for message handling and file operations.

Author: Agent-7 (Implementation Specialist)
License: MIT
V2 Compliance: ≤400 lines, modular design, utility functions
"""

import json
from datetime import datetime
from pathlib import Path


class SwarmWorkflowUtils:
    """Utility functions for swarm workflow operations"""

    def __init__(self, agent_workspaces: Path, devlogs: Path):
        self.agent_workspaces = agent_workspaces
        self.devlogs = devlogs

    def send_agent_message(self, agent: str, message: str, priority: str, tags: list[str]) -> str:
        """Send a message to a specific agent."""
        agent_inbox = self.agent_workspaces / agent / "inbox"
        agent_inbox.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        message_file = agent_inbox / f"{timestamp}_swarm_orchestrator_message.txt"

        message_content = f"""============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Swarm Workflow Orchestrator
📥 TO: {agent}
Priority: {priority}
Tags: {'|'.join(tags)}
------------------------------------------------------------
{message}
------------------------------------------------------------
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory
------------------------------------------------------------"""

        with open(message_file, "w", encoding="utf-8") as f:
            f.write(message_content)

        return f"Message sent to {agent}"

    def create_task_file(self, agent: str, tasks: list[dict], priority: str) -> str:
        """Create a task file for an agent."""
        task_file = self.agent_workspaces / agent / "future_tasks.json"

        task_data = {
            "agent_id": agent,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "tasks": tasks,
        }

        with open(task_file, "w", encoding="utf-8") as f:
            json.dump(task_data, f, indent=2)

        return f"Task file created for {agent} with {len(tasks)} tasks"

    def create_devlog(self, title: str, content: str, priority: str) -> str:
        """Create a devlog entry."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        devlog_file = (
            self.devlogs / f"swarm_orchestrator_{title.lower().replace(' ', '_')}_{timestamp}.md"
        )

        devlog_content = f"""# {title}

**Date:** {datetime.now().strftime('%Y-%m-%d')}
**From:** Swarm Workflow Orchestrator
**Priority:** {priority}
**Tags:** SWARM_ORCHESTRATOR|WORKFLOW|COORDINATION

{content}

**🐝 WE. ARE. SWARM.** - Orchestrated by Swarm Workflow Orchestrator
"""

        with open(devlog_file, "w", encoding="utf-8") as f:
            f.write(devlog_content)

        return f"Devlog created: {devlog_file.name}"

    def wait_for_agent_completion(self, agent: str, timeout: int) -> str:
        """Wait for an agent to complete their tasks."""
        # This would implement actual waiting logic
        # For now, just return a placeholder
        return f"Waited for {agent} completion (timeout: {timeout}s)"
