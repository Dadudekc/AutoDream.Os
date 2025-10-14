#!/usr/bin/env python3
"""
Task Creator - Extracted from Swarm Orchestrator
================================================

Creates autonomous task files in agent inboxes.

Author: Agent-8 (SSOT & System Integration) - Lean Excellence Refactor
License: MIT
"""

from datetime import datetime
from pathlib import Path
from typing import Any


def create_inbox_task(
    agent: str, opportunity: dict[str, Any], roi: float, agent_workspaces: Path
) -> str:
    """
    Create task in agent's inbox.

    Args:
        agent: Target agent ID (e.g., "Agent-1")
        opportunity: Opportunity details dict
        roi: Calculated ROI value
        agent_workspaces: Path to agent workspaces directory

    Returns:
        Path to created task file
    """
    inbox_dir = agent_workspaces / agent / "inbox"
    inbox_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    task_file = inbox_dir / f"AUTO_TASK_{timestamp}.md"

    task_content = f"""# [AUTO] Autonomous Task Assignment

**From:** Swarm Orchestrator (Gas Station)  
**To:** {agent}  
**Date:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}  
**Priority:** Auto-Generated  
**ROI:** {roi:.2f}

---

## 🎯 **OPPORTUNITY DETECTED**

**Type:** {opportunity.get('type', 'Unknown')}  
**File:** {opportunity.get('file', 'N/A')}  
**Line:** {opportunity.get('line', 'N/A')}  
**Points:** {opportunity.get('points', 100)}  
**Complexity:** {opportunity.get('complexity', 50)}  
**ROI:** {roi:.2f}

---

## 📋 **TASK DESCRIPTION**

{opportunity.get('description', 'Fix the identified issue')}

**Details:**
```
{opportunity.get('content', 'See file for details')}
```

---

## ✅ **ACCEPTANCE CRITERIA**

1. Issue resolved in identified file
2. Tests passing (if applicable)
3. V2 compliance maintained
4. Documentation updated (if needed)
5. Tag completion: #DONE-AUTO-{agent}

---

## 🚀 **GET STARTED**

This task was automatically assigned based on:
- Your specialty match
- Current idle status
- ROI optimization ({roi:.2f})

**Ready to execute!** 🐝⚡

---

*Autonomous Gas Delivery System - Keeping the swarm moving!* 🏭
"""

    task_file.write_text(task_content)
    print(f"  ✅ Created inbox task: {task_file.name}")

    return str(task_file)


__all__ = ["create_inbox_task"]
