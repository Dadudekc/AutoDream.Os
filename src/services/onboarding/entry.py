#!/usr/bin/env python3
"""
Onboarding Entry Module
=======================

Simple entry point for agent onboarding that can be called from Discord.
Reuses the CLI flow by invoking the agent onboarding script as a subprocess.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Simple in-proc registry of running onboarding jobs
_RUNNING: Dict[str, asyncio.Task] = {}

async def kickoff_onboarding(agent: str, mode: str = "manual", role: Optional[str] = None, dry_run: bool = False) -> None:
    """
    Launch onboarding for an agent by invoking the CLI:
      python tools/agent_onboarding.py --agent Agent-8 --mode manual
    This returns immediately after the subprocess starts.
    """
    if agent in _RUNNING and not _RUNNING[agent].done():
        logger.info(f"Onboarding already running for {agent}")
        return

    cmd = ["python", "tools/agent_onboarding.py", "--agent", agent, "--mode", mode]
    if role:
        cmd += ["--role", role]
    if dry_run:
        cmd += ["--dry-run"]

    async def _runner():
        logger.info(f"🎓 Onboarding start: {agent} mode={mode} role={role} dry={dry_run}")
        proc = await asyncio.create_subprocess_exec(*cmd)
        rc = await proc.wait()
        logger.info(f"🎓 Onboarding finished: {agent} rc={rc}")

    task = asyncio.create_task(_runner(), name=f"onboarding:{agent}")
    _RUNNING[agent] = task

def is_onboarding_running(agent: str) -> bool:
    """Check if onboarding is currently running for an agent."""
    t = _RUNNING.get(agent)
    return bool(t and not t.done())

async def wait_onboarding(agent: str, timeout: Optional[float] = None) -> None:
    """Wait for onboarding to complete for an agent."""
    t = _RUNNING.get(agent)
    if t:
        await asyncio.wait_for(t, timeout=timeout)

def get_running_onboarding() -> Dict[str, bool]:
    """Get status of all running onboarding processes."""
    return {agent: not task.done() for agent, task in _RUNNING.items() if not task.done()}

