"""ChatGPT Scraper Conversation Methods - V2 Compliance | Agent-5"""

import logging
from collections.abc import Callable
from pathlib import Path

logger = logging.getLogger(__name__)


class ScraperConversationMethods:
    """Large conversation extraction methods."""

    @staticmethod
    def extract_all_smart(
        scraper,
        limit: int | None,
        output_dir: str,
        progress_callback: Callable | None,
        skip_processed: bool,
    ) -> dict[str, int]:
        """SMART extraction method."""
        try:
            logger.info("🧠 Starting SMART conversation extraction...")
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            logger.info("📊 Step 1: Counting total conversations...")
            total_count = scraper._count_total_conversations()
            logger.info(f"✅ Found {total_count} total conversations")
            if limit:
                total_count = min(total_count, limit)
                logger.info(f"🔢 Limited to {total_count} conversations")
            logger.info("📝 Step 2: Extracting conversations as we discover them...")
            conversations = scraper._get_conversations_with_smart_extraction(
                total_count, output_dir, progress_callback, skip_processed
            )
            stats = {"total": total_count, "extracted": 0, "failed": 0, "skipped": 0, "errors": []}
            stats["extracted"] = len(
                [f for f in Path(output_dir).glob("conversation_*.json") if f.exists()]
            )
            logger.info("🔄 Step 3: Reversing file numbering for chronological order...")
            scraper._reverse_file_numbering(output_dir, total_count)
            logger.info(
                f"✅ SMART extraction complete: {stats['extracted']}/{stats['total']} successful"
            )
            return stats
        except Exception as e:
            logger.error(f"Failed SMART extraction: {e}")
            return {"total": 0, "extracted": 0, "failed": 0, "errors": [str(e)]}

    @staticmethod
    def extract_all_standard(
        scraper,
        limit: int | None,
        output_dir: str,
        progress_callback: Callable | None,
        skip_processed: bool,
    ) -> dict[str, int]:
        """Standard extraction method."""
        try:
            logger.info("🚀 Starting conversation extraction...")
            progress_stats = scraper.get_progress_stats()
            if progress_stats["total_processed"] > 0:
                logger.info(
                    f"📊 Resume mode: {progress_stats['successful']} conversations already processed"
                )
            conversations = scraper.get_conversation_list(progress_callback)
            if limit:
                conversations = conversations[:limit]
            if skip_processed:
                original_count = len(conversations)
                conversations = [
                    conv for conv in conversations if not scraper._is_conversation_processed(conv)
                ]
                skipped_count = original_count - len(conversations)
                if skipped_count > 0:
                    logger.info(f"⏭️ Skipping {skipped_count} already processed conversations")
            logger.info(f"📋 Found {len(conversations)} conversations to extract")
            if len(conversations) == 0:
                logger.info("✅ All conversations already processed!")
                return {
                    "total": 0,
                    "extracted": 0,
                    "failed": 0,
                    "skipped": progress_stats["total_processed"],
                    "errors": [],
                }
            stats = {
                "total": len(conversations),
                "extracted": 0,
                "failed": 0,
                "skipped": progress_stats["total_processed"],
                "errors": [],
            }
            total_conversations = len(conversations)
            for i, conversation in enumerate(conversations):
                try:
                    chronological_number = total_conversations - i
                    logger.info(
                        f"📝 Extracting conversation {i+1}/{total_conversations} (will be #{chronological_number} chronologically): {conversation.get('title', 'Unknown')}"
                    )
                    if scraper.extract_conversation(
                        conversation["url"], output_dir, chronological_number
                    ):
                        stats["extracted"] += 1
                        scraper._mark_conversation_processed(conversation, success=True)
                    else:
                        stats["failed"] += 1
                        scraper._mark_conversation_processed(conversation, success=False)
                        stats["errors"].append(
                            f"Failed to extract {conversation.get('id', 'unknown')}"
                        )
                    if progress_callback:
                        progress_callback(i + 1, total_conversations)
                except Exception as e:
                    stats["failed"] += 1
                    scraper._mark_conversation_processed(conversation, success=False)
                    stats["errors"].append(
                        f"Error extracting {conversation.get('id', 'unknown')}: {e}"
                    )
                    logger.error(f"Error extracting conversation: {e}")
            logger.info(f"✅ Extraction complete: {stats['extracted']}/{stats['total']} successful")
            return stats
        except Exception as e:
            logger.error(f"Failed to extract conversations: {e}")
            return {"total": 0, "extracted": 0, "failed": 0, "errors": [str(e)]}
