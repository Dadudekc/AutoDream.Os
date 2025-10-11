#!/usr/bin/env python3
"""
Messaging Inbox Rotation - Memory Leak Fix
==========================================

Prevents inbox files from growing indefinitely by implementing rotation.
Fixes memory sink in messaging system.

Author: Agent-1 (Integration & Core Systems Specialist) - Proactive Memory Leak Fix
Created: 2025-10-10
License: MIT
"""

import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# Configuration
MAX_INBOX_SIZE_KB = 500  # Rotate when inbox exceeds 500KB
MAX_INBOX_MESSAGES = 100  # Or rotate after 100 messages
ARCHIVE_DIR = "archive"


class InboxRotationManager:
    """Manages inbox file rotation to prevent unbounded growth."""

    def __init__(
        self, max_size_kb: int = MAX_INBOX_SIZE_KB, max_messages: int = MAX_INBOX_MESSAGES
    ):
        """Initialize inbox rotation manager."""
        self.max_size_kb = max_size_kb
        self.max_messages = max_messages
        self.logger = logging.getLogger(__name__)

    def should_rotate(self, inbox_path: Path) -> bool:
        """Check if inbox should be rotated."""
        if not inbox_path.exists():
            return False

        # Check file size
        size_kb = inbox_path.stat().st_size / 1024
        if size_kb > self.max_size_kb:
            self.logger.info(
                f"Inbox {inbox_path.name} exceeds size limit ({size_kb:.1f}KB > {self.max_size_kb}KB)"
            )
            return True

        # Check message count
        try:
            with open(inbox_path, encoding="utf-8") as f:
                content = f.read()
                message_count = content.count("# 🚨 CAPTAIN MESSAGE")
                if message_count > self.max_messages:
                    self.logger.info(
                        f"Inbox {inbox_path.name} exceeds message limit ({message_count} > {self.max_messages})"
                    )
                    return True
        except Exception as e:
            self.logger.error(f"Failed to count messages: {e}")

        return False

    def rotate_inbox(self, inbox_path: Path) -> bool:
        """Rotate inbox file to archive."""
        try:
            if not inbox_path.exists():
                return False

            # Create archive directory
            archive_dir = inbox_path.parent / ARCHIVE_DIR
            archive_dir.mkdir(parents=True, exist_ok=True)

            # Generate archive filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{inbox_path.stem}_{timestamp}.txt"
            archive_path = archive_dir / archive_name

            # Move current inbox to archive
            inbox_path.rename(archive_path)

            self.logger.info(f"✅ Rotated inbox to: {archive_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to rotate inbox: {e}")
            return False

    def check_and_rotate(self, inbox_path: Path) -> bool:
        """Check if rotation needed and execute if necessary."""
        if self.should_rotate(inbox_path):
            return self.rotate_inbox(inbox_path)
        return False

    def rotate_all_inboxes(self, base_dir: str = "agent_workspaces") -> int:
        """Rotate all agent inboxes that exceed limits."""
        rotated_count = 0

        try:
            base_path = Path(base_dir)
            for inbox_file in base_path.rglob("*_inbox.txt"):
                if self.check_and_rotate(inbox_file):
                    rotated_count += 1

            if rotated_count > 0:
                self.logger.info(f"✅ Rotated {rotated_count} inbox files")

            return rotated_count

        except Exception as e:
            self.logger.error(f"Failed to rotate inboxes: {e}")
            return rotated_count

    def cleanup_old_archives(
        self, max_age_days: int = 30, base_dir: str = "agent_workspaces"
    ) -> int:
        """Clean up archive files older than specified days."""
        deleted_count = 0

        try:
            base_path = Path(base_dir)
            cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 60 * 60)

            for archive_file in base_path.rglob(f"{ARCHIVE_DIR}/*_inbox_*.txt"):
                if archive_file.stat().st_mtime < cutoff_time:
                    archive_file.unlink()
                    deleted_count += 1
                    self.logger.info(f"Deleted old archive: {archive_file.name}")

            if deleted_count > 0:
                self.logger.info(f"✅ Cleaned {deleted_count} old archive files")

            return deleted_count

        except Exception as e:
            self.logger.error(f"Failed to cleanup archives: {e}")
            return deleted_count


# Singleton instance
_rotation_manager: InboxRotationManager | None = None


def get_rotation_manager() -> InboxRotationManager:
    """Get global inbox rotation manager instance."""
    global _rotation_manager
    if _rotation_manager is None:
        _rotation_manager = InboxRotationManager()
    return _rotation_manager


__all__ = [
    "InboxRotationManager",
    "get_rotation_manager",
    "MAX_INBOX_SIZE_KB",
    "MAX_INBOX_MESSAGES",
]
