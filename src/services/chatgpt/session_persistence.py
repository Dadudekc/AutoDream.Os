"""
Session Persistence Helper
===========================

Session data persistence operations extracted for V2 compliance.

Author: Agent-2 - Architecture & Design Specialist (V2 Refactor)
License: MIT
"""

import json
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class SessionPersistence:
    """Handles session data persistence operations."""

    @staticmethod
    async def load_session_data(
        session_dir: Path, cookie_cache: dict, session_data: dict, logger_instance
    ) -> None:
        """Load session data from disk."""
        try:
            cookie_file = session_dir / "cookies.json"

            if cookie_file.exists():
                with open(cookie_file) as f:
                    cookie_data = json.load(f)

                cookie_cache.update(cookie_data.get("cookies", {}))
                session_data.update(cookie_data.get("session_data", {}))

                logger_instance.info(f"Loaded session data from {cookie_file}")
            else:
                logger_instance.info("No existing session data found")

        except Exception as e:
            logger_instance.error(f"Failed to load session data: {e}")

    @staticmethod
    async def save_session_data(
        session_dir: Path, cookie_cache: dict, session_data: dict, logger_instance
    ) -> None:
        """Save session data to disk."""
        try:
            cookie_file = session_dir / "cookies.json"

            data_to_save = {
                "cookies": cookie_cache,
                "session_data": session_data,
                "timestamp": time.time(),
                "version": "2.0.0",
            }

            with open(cookie_file, "w") as f:
                json.dump(data_to_save, f, indent=2)

            logger_instance.info(f"Session data saved to {cookie_file}")

        except Exception as e:
            logger_instance.error(f"Failed to save session data: {e}")

    @staticmethod
    def clear_session_files(session_dir: Path, persistent: bool, logger_instance) -> bool:
        """Clear session files from disk."""
        try:
            if persistent and session_dir.exists():
                cookie_file = session_dir / "cookies.json"
                if cookie_file.exists():
                    cookie_file.unlink()
                    logger_instance.info("Session files cleared")
            return True
        except Exception as e:
            logger_instance.error(f"Failed to clear session files: {e}")
            return False
