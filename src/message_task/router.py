#!/usr/bin/env python3
"""
Message-Task Router
===================

Routes messages to tasks using 3-tier parser cascade.

Author: Agent-7 - Repository Cloning Specialist
Created: 2025-10-13
"""

import logging

from .dedupe import task_fingerprint
from .fsm_bridge import transition_on_create
from .parsers.ai_parser import AIParser
from .parsers.fallback_regex import FallbackRegexParser
from .parsers.structured_parser import StructuredParser
from .schemas import InboundMessage, ParsedTask

logger = logging.getLogger(__name__)


class MessageTaskRouter:
    """Routes messages to tasks with deduplication."""

    def __init__(self, task_repository):
        """
        Initialize router.

        Args:
            task_repository: SqliteTaskRepository instance
        """
        self.repo = task_repository
        self.parsers = [
            ("structured", StructuredParser.parse),
            ("ai", AIParser.parse),
            ("fallback", FallbackRegexParser.parse),
        ]

    def parse(self, msg: InboundMessage) -> ParsedTask | None:
        """
        Parse message using 3-tier cascade.

        Args:
            msg: Inbound message

        Returns:
            ParsedTask or None
        """
        for parser_name, parser_func in self.parsers:
            try:
                result = parser_func(msg.content)
                if result:
                    result.source_msg_id = msg.id
                    logger.info(f"✅ Parsed via {parser_name}: {result.title[:50]}")

                    # Observability: Log parser used
                    try:
                        from src.obs.metrics import log_parser_used

                        log_parser_used(parser_name)
                    except ImportError:
                        pass

                    return result
            except Exception as e:
                logger.warning(f"Parser {parser_name} failed: {e}")
                continue

        logger.warning(f"All parsers failed for message {msg.id}")
        return None

    def ingest(self, msg: InboundMessage) -> str | None:
        """
        Ingest message and create task.

        Args:
            msg: Inbound message

        Returns:
            Task ID or None if failed
        """
        # Parse message
        parsed = self.parse(msg)
        if not parsed:
            logger.info(f"Message {msg.id} not parsed as task")
            return None

        # Generate fingerprint for deduplication
        fp = task_fingerprint(parsed.to_dict())

        # Check for existing task with same fingerprint
        try:
            existing = self.repo.find_by_fingerprint(fp)
            if existing:
                logger.info(f"Duplicate task detected: {existing.id} (fingerprint: {fp[:8]}...)")

                # Observability: Log duplicate
                try:
                    from src.obs.metrics import log_ingest_duplicate

                    log_ingest_duplicate()
                except ImportError:
                    pass

                return str(existing.id)
        except AttributeError:
            # Repository doesn't have find_by_fingerprint yet - continue
            logger.debug("Repository doesn't support find_by_fingerprint")

        # Create new task
        state, event = transition_on_create()

        # Prepare source metadata
        source_data = {
            "channel": msg.channel,
            "author": msg.author,
            "msg_id": msg.id,
            "fingerprint": fp,
            "event": event.value,
        }

        try:
            # Create task in repository
            task_id = self.repo.create_from_message(
                title=parsed.title,
                description=parsed.description,
                priority=parsed.priority,
                assignee=parsed.assignee,
                state=state.value,
                source=source_data,
                tags=parsed.tags,
                parent_id=parsed.parent_id,
                due_timestamp=parsed.due_timestamp,
                fingerprint=fp,
            )

            logger.info(f"✅ Task created: {task_id} (fingerprint: {fp[:8]}...)")

            # Observability: Log success
            try:
                from src.obs.metrics import log_ingest_success

                log_ingest_success()
            except ImportError:
                pass

            return task_id

        except Exception as e:
            logger.error(f"❌ Failed to create task: {e}")

            # Observability: Log failure
            try:
                from src.obs.metrics import log_ingest_failure

                log_ingest_failure()
            except ImportError:
                pass

            return None
