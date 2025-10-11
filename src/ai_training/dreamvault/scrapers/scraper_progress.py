"""ChatGPT Scraper Progress Tracking - V2 Compliance | Agent-5"""

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ScraperProgressTracker:
    """Tracks scraper progress and resume functionality."""

    def __init__(self, progress_file: str):
        """Initialize progress tracker."""
        self.progress_file = progress_file
        self.processed_conversations = self._load_progress()

    def _load_progress(self) -> dict[str, dict]:
        """Load progress from file."""
        try:
            progress_path = Path(self.progress_file)
            if progress_path.exists():
                with open(progress_path) as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading progress: {e}")
            return {}

    def _save_progress(self):
        """Save progress to file."""
        try:
            progress_path = Path(self.progress_file)
            progress_path.parent.mkdir(parents=True, exist_ok=True)
            with open(progress_path, "w") as f:
                json.dump(self.processed_conversations, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving progress: {e}")

    def _get_conversation_hash(self, conversation: dict) -> str:
        """Get unique hash for conversation."""
        conv_id = conversation.get("id", "")
        conv_title = conversation.get("title", "")
        return hashlib.md5(f"{conv_id}:{conv_title}".encode()).hexdigest()

    def _is_conversation_processed(self, conversation: dict) -> bool:
        """Check if conversation has been processed."""
        conv_hash = self._get_conversation_hash(conversation)
        return conv_hash in self.processed_conversations

    def _mark_conversation_processed(self, conversation: dict, success: bool = True):
        """Mark conversation as processed."""
        conv_hash = self._get_conversation_hash(conversation)
        self.processed_conversations[conv_hash] = {
            "title": conversation.get("title", "Unknown"),
            "id": conversation.get("id", ""),
            "processed_at": str(datetime.now()),
            "success": success,
        }
        self._save_progress()

    def reset_progress(self):
        """Reset progress tracking."""
        self.processed_conversations = {}
        self._save_progress()
        logger.info("✅ Progress reset")

    def get_progress_stats(self) -> dict[str, any]:
        """Get progress statistics."""
        total = len(self.processed_conversations)
        successful = sum(
            1 for p in self.processed_conversations.values() if p.get("success", False)
        )
        return {
            "total_processed": total,
            "successful": successful,
            "failed": total - successful,
            "success_rate": (successful / total * 100) if total > 0 else 0,
        }
