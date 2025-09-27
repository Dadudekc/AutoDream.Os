#!/usr/bin/env python3
"""
Restart Manager
===============

Handles bot restart functionality for the Discord Commander.
"""

import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class RestartManager:
    """Manages bot restart operations."""

    def __init__(self):
        self.restart_pending = False
        self.restart_reason = ""
        self._lock = asyncio.Lock()

    def _resolve_entrypoint(self) -> Optional[Path]:
        # Resolve project root robustly: go up until we find run_discord_commander.py
        here = Path(__file__).resolve()
        for p in [here, *here.parents]:
            candidate = p.parent.parent.parent.parent / "run_discord_commander.py" if p.name == "core" else p / "run_discord_commander.py"
            if candidate.exists():
                return candidate
        return None

    async def restart_bot(self, reason: str = "Manual restart requested") -> bool:
        async with self._lock:
            if self.restart_pending:
                logger.warning("[RESTART] Ignored: restart already pending (%s)", self.restart_reason)
                return True  # treat as success: one restart is enough

            logger.info("[RESTART] Initiating bot restart: %s", reason)
            self.restart_pending = True
            self.restart_reason = reason

            entry = self._resolve_entrypoint()
            if not entry:
                logger.error("[RESTART] Script not found (run_discord_commander.py). Check path resolution.")
                self.restart_pending = False
                return False

            python_executable = sys.executable
            # -u = unbuffered, so startup logs flush immediately
            cmd = [python_executable, "-u", str(entry)]
            logger.info("[RESTART] Executing: %s", " ".join(cmd))

            # Inherit env; force UTF-8; ensure critical vars exist (adjust as needed)
            env = os.environ.copy()
            env.setdefault("PYTHONUTF8", "1")
            env.setdefault("PYTHONIOENCODING", "utf-8")
            # Example: ensure DISCORD_TOKEN survives; warn if missing
            if not env.get("DISCORD_BOT_TOKEN"):
                logger.warning("[RESTART] DISCORD_BOT_TOKEN not present in environment for child process")

            creationflags = 0
            start_new_session = False
            if os.name == "nt":
                DETACHED_PROCESS = 0x00000008
                CREATE_NEW_PROCESS_GROUP = 0x00000200
                creationflags = DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
            else:
                # POSIX: start new session so child is independent
                start_new_session = True

            try:
                process = subprocess.Popen(
                    cmd,
                    cwd=str(entry.parent),
                    env=env,
                    shell=False,
                    stdin=subprocess.DEVNULL,
                    stdout=None,
                    stderr=None,
                    close_fds=(os.name != "nt"),
                    creationflags=creationflags,
                    start_new_session=start_new_session,  # no-op on Windows
                )
            except Exception as e:
                logger.exception("[RESTART] Popen failed: %s", e)
                self.restart_pending = False
                return False

            # Give it a moment to crash fast if it will
            await asyncio.sleep(3.0)

            rc = process.poll()
            if rc is None:
                logger.info("[RESTART] New bot process spawned successfully (pid=%s)", process.pid)
                asyncio.create_task(self._shutdown_current_process())
                return True
            else:
                logger.error("[RESTART] New process exited early with code: %s", rc)
                self.restart_pending = False
                return False

    async def _shutdown_current_process(self):
        try:
            logger.info("[RESTART] Shutting down current process...")
            await asyncio.sleep(1.0)
            logger.info("[RESTART] Exiting current process")
            os._exit(0)
        except Exception as e:
            logger.exception("[RESTART] Error during shutdown: %s", e)
            os._exit(1)

    def is_restart_pending(self) -> bool:
        return self.restart_pending

    def get_restart_reason(self) -> str:
        return self.restart_reason


restart_manager = RestartManager()
