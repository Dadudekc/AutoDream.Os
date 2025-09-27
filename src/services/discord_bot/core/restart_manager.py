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
from .security_utils import security_utils

logger = logging.getLogger(__name__)


class RestartManager:
    """Manages bot restart operations."""

    def __init__(self):
        self.restart_pending = False
        self.restart_reason = ""
        self._lock = asyncio.Lock()

    def _resolve_entrypoint(self) -> Optional[Path]:
        """Resolve project root robustly with security validation."""
        here = Path(__file__).resolve()
        for p in [here, *here.parents]:
            candidate = p.parent.parent.parent.parent / "run_discord_commander.py" if p.name == "core" else p / "run_discord_commander.py"
            
            # Security validation
            if candidate.exists() and security_utils.validate_path(str(candidate)):
                return candidate
            elif candidate.exists():
                logger.error(f"[RESTART] Security validation failed for path: {candidate}")
                return None
        return None

    async def restart_bot(self, reason: str = "Manual restart requested") -> bool:
        async with self._lock:
            if self.restart_pending:
                logger.warning("[RESTART] Ignored: restart already pending (%s)", self.restart_reason)
                return True  # treat as success: one restart is enough

            logger.info("[RESTART] Initiating bot restart: %s", security_utils.mask_sensitive_data(reason))
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
            
            # Sanitize command arguments
            cmd = security_utils.sanitize_command_args(cmd)
            
            # Log sanitized command (no sensitive data)
            logger.info("[RESTART] Process starting with sanitized arguments")

            # Create secure environment for subprocess
            env = security_utils.create_secure_environment()
            
            # Ensure critical variables exist
            if not env.get("DISCORD_BOT_TOKEN"):
                logger.warning("[RESTART] DISCORD_BOT_TOKEN not present in secure environment for child process")

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
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
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
                # Capture stdout and stderr for debugging
                try:
                    stdout, stderr = process.communicate(timeout=1)
                    stdout_str = stdout.decode('utf-8', errors='replace') if stdout else ""
                    stderr_str = stderr.decode('utf-8', errors='replace') if stderr else ""
                    
                    logger.error("[RESTART] New process exited early with code: %s", rc)
                    if stdout_str:
                        logger.error("[RESTART] STDOUT: %s", stdout_str.strip())
                    if stderr_str:
                        logger.error("[RESTART] STDERR: %s", stderr_str.strip())
                except subprocess.TimeoutExpired:
                    logger.error("[RESTART] New process exited early with code: %s (timeout reading output)", rc)
                except Exception as e:
                    logger.error("[RESTART] New process exited early with code: %s (error reading output: %s)", rc, e)
                
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
