#!/usr/bin/env python3
"""
Agent Cycle Devlog Tool (Webhook-Only)
=====================================

Posts directly to agent Discord channels via Webhooks (no bot activation).
Also writes a local devlog file under agent_workspaces/<agent>/devlogs/.

Usage:
  python tools/agent_cycle_devlog.py --agent Agent-4 --action "Tools cleanup completed" --status completed
  python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-start --focus "Architecture review"
  python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-complete --action "Coordination" --results "All agents coordinated"
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional, Tuple

# Optional .env support
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

# Optional async HTTP; fall back to sync requests in thread if missing
try:
    import aiohttp
    _HAS_AIOHTTP = True
except Exception:
    _HAS_AIOHTTP = False
import functools
import concurrent.futures

LOG = logging.getLogger("agent_devlog_webhook")

AGENTS = [f"Agent-{i}" for i in range(1, 9)]
RUNTIME_WEBHOOKS = Path("runtime/discord/webhooks.json")


@dataclass
class DevlogResult:
    path: Optional[Path]
    posted: bool


def _timestamp() -> str:
    return time.strftime("%Y%m%d_%H%M%S")


def _agent_devlog_dir(agent: str) -> Path:
    p = Path(f"agent_workspaces/{agent}/devlogs")
    p.mkdir(parents=True, exist_ok=True)
    return p


def _load_webhooks_from_file() -> Dict[str, str]:
    if RUNTIME_WEBHOOKS.exists():
        try:
            return json.loads(RUNTIME_WEBHOOKS.read_text(encoding="utf-8"))
        except Exception as e:
            LOG.warning("Failed reading %s: %s", RUNTIME_WEBHOOKS, e)
    return {}


def _env_key_for(agent: str) -> str:
    # e.g., Agent-4 -> DISCORD_WEBHOOK_Agent_4
    return f"DISCORD_WEBHOOK_{agent.replace('-', '_')}"


def resolve_webhook(agent: str) -> Optional[str]:
    # Priority 1: environment variable per agent
    env_key = _env_key_for(agent)
    if os.getenv(env_key):
        return os.getenv(env_key)

    # Priority 2: generic env map as JSON
    if os.getenv("DISCORD_WEBHOOK_MAP_JSON"):
        try:
            m = json.loads(os.getenv("DISCORD_WEBHOOK_MAP_JSON", "{}"))
            if agent in m:
                return m[agent]
        except Exception as e:
            LOG.warning("Invalid DISCORD_WEBHOOK_MAP_JSON: %s", e)

    # Priority 3: runtime/discord/webhooks.json { "Agent-4": "https://discord.com/api/webhooks/..." }
    file_map = _load_webhooks_from_file()
    return file_map.get(agent)


def build_message_content(
    agent: str,
    *,
    basic_action: Optional[str],
    status: str,
    details: Optional[str],
    cycle_start: bool,
    focus: Optional[str],
    cycle_complete: bool,
    results: Optional[str],
    task_assignment: bool,
    task: Optional[str],
    assigned_by: Optional[str],
    coordination: bool,
    message: Optional[str],
    target: Optional[str],
) -> Tuple[str, Dict]:
    """
    Returns (plain_text, embed_dict_or_empty)
    """
    title = ""
    body_lines = []
    embed: Dict = {}

    if cycle_start:
        title = f"🚀 Cycle Start — {agent}"
        if not focus:
            raise ValueError("--focus required for cycle start")
        body_lines += [
            f"**Agent:** {agent}",
            f"**Focus:** {focus}",
            f"**Status:** in_progress",
        ]
    elif cycle_complete:
        title = f"✅ Cycle Complete — {agent}"
        if not basic_action or not results:
            raise ValueError("--action and --results required for cycle completion")
        body_lines += [
            f"**Agent:** {agent}",
            f"**Action:** {basic_action}",
            f"**Results:** {results}",
            f"**Status:** completed",
        ]
    elif task_assignment:
        title = f"📋 Task Assignment — {agent}"
        if not task or not assigned_by:
            raise ValueError("--task and --assigned-by required for task assignment")
        body_lines += [
            f"**Assigned By:** {assigned_by}",
            f"**Task:** {task}",
            f"**Status:** assigned",
        ]
    elif coordination:
        title = f"🤝 Coordination — {agent}"
        if not message or not target:
            raise ValueError("--message and --target required for coordination")
        body_lines += [
            f"**From:** {agent}",
            f"**To:** {target}",
            f"**Message:** {message}",
            f"**Status:** info",
        ]
    else:
        # Basic devlog
        if not basic_action:
            raise ValueError("--action required for basic devlog creation")
        title = f"📝 Devlog — {agent}"
        body_lines += [
            f"**Agent:** {agent}",
            f"**Action:** {basic_action}",
            f"**Status:** {status}",
        ]
        if details:
            body_lines.append(f"**Details:** {details}")

    plain = f"**{title}**\n" + "\n".join(body_lines)

    # Simple embed for nicer rendering
    embed = {
        "title": title,
        "description": "\n".join(body_lines),
    }
    return plain, {"embeds": [embed]}


def write_devlog_file(agent: str, title_line: str, content: str) -> Path:
    ts = _timestamp()
    file_name = f"{ts}_{title_line.replace(' ', '_').replace('—','-')}.md"
    p = _agent_devlog_dir(agent) / file_name
    p.write_text(content + "\n", encoding="utf-8")
    return p


async def post_webhook_async(url: str, payload: Dict) -> bool:
    # Prefer aiohttp if present; else run sync requests in a thread
    if _HAS_AIOHTTP:
        try:
            timeout = aiohttp.ClientTimeout(total=10)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload) as resp:
                    ok = 200 <= resp.status < 300
                    if not ok:
                        LOG.warning("Webhook post failed: %s %s", resp.status, await resp.text())
                    return ok
        except Exception as e:
            LOG.warning("Webhook error: %s", e)
            return False
    else:
        import requests
        loop = asyncio.get_running_loop()
        def _post():
            try:
                r = requests.post(url, json=payload, timeout=10)
                return r.status_code >= 200 and r.status_code < 300
            except Exception:
                return False
        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
            return await loop.run_in_executor(ex, _post)


async def main():
    parser = argparse.ArgumentParser(
        description="Agent Cycle Devlog Tool (Webhook-Only)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python tools/agent_cycle_devlog.py --agent Agent-4 --action "Mission completed" --status completed
  python tools/agent_cycle_devlog.py --agent Agent-2 --cycle-start --focus "Architecture review"
  python tools/agent_cycle_devlog.py --agent Agent-6 --cycle-complete --action "Coordination" --results "All agents coordinated"
  python tools/agent_cycle_devlog.py --agent Agent-1 --task-assignment --task "System integration" --assigned-by "Agent-4"
  python tools/agent_cycle_devlog.py --agent Agent-4 --coordination --message "Status update needed" --target Agent-2
        """
    )

    parser.add_argument("--agent", required=True, choices=AGENTS, help="Agent ID (Agent-1..Agent-8)")
    parser.add_argument("--action", type=str, help="Action description for devlog")
    parser.add_argument("--status", type=str, default="completed",
                        choices=["completed", "in_progress", "assigned", "failed"], help="Status")
    parser.add_argument("--details", type=str, help="Additional details")

    parser.add_argument("--cycle-start", action="store_true", help="Create cycle start devlog")
    parser.add_argument("--focus", type=str, help="Focus area for cycle start")

    parser.add_argument("--cycle-complete", action="store_true", help="Create cycle completion devlog")
    parser.add_argument("--results", type=str, help="Results for cycle completion")

    parser.add_argument("--task-assignment", action="store_true", help="Create task assignment devlog")
    parser.add_argument("--task", type=str, help="Task description for assignment")
    parser.add_argument("--assigned-by", type=str, help="Agent who assigned the task")

    parser.add_argument("--coordination", action="store_true", help="Create coordination devlog")
    parser.add_argument("--message", type=str, help="Coordination message")
    parser.add_argument("--target", type=str, help="Target agent for coordination")

    parser.add_argument("--no-discord", action="store_true", help="Write file only, do not post to Discord")
    parser.add_argument("--verbose", action="store_true", help="Verbose logging")

    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    try:
        content, embed_payload = build_message_content(
            args.agent,
            basic_action=args.action,
            status=args.status,
            details=args.details,
            cycle_start=args.cycle_start,
            focus=args.focus,
            cycle_complete=args.cycle_complete,
            results=args.results,
            task_assignment=args.task_assignment,
            task=args.task,
            assigned_by=args.assigned_by,
            coordination=args.coordination,
            message=args.message,
            target=args.target,
        )

        # Write devlog file first (SSOT artifact)
        title_line = content.splitlines()[0].strip("* ")
        devlog_path = write_devlog_file(args.agent, title_line, content)

        posted = False
        if not args.no_discord:
            url = resolve_webhook(args.agent)
            if not url:
                LOG.error("No webhook configured for %s. Set %s or provide %s with mapping.",
                          args.agent, _env_key_for(args.agent), RUNTIME_WEBHOOKS)
            else:
                payload = {"content": None, **embed_payload}  # embed only; or set "content": content for plain text
                # To include plain text + embed, set "content": content
                payload["content"] = content
                posted = await post_webhook_async(url, payload)

        # CLI summary
        print(f"✅ Devlog created: {devlog_path.name}")
        if args.no_discord:
            print("📄 File-only mode (Discord posting disabled)")
        else:
            if posted:
                print(f"📢 Posted to {args.agent}'s Discord channel via webhook")
            else:
                print("⚠️ Discord posting failed or webhook missing")

        return 0
    except Exception as e:
        LOG.error("Error: %s", e)
        print(f"❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
