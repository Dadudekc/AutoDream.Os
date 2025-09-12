#!/usr/bin/env python3
"""
Message Archive System for Enhanced Inter-Agent Coordination
===========================================================

Provides comprehensive message archiving capabilities for the swarm communication
improvement initiative. Supports proper archiving of processed messages and
coordination history tracking.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import json
import logging
import os
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class MessageType(Enum):
    """Message types for archiving"""
    COORDINATION = "coordination"
    STATUS_UPDATE = "status_update"
    PERFORMANCE_ALERT = "performance_alert"
    INFRASTRUCTURE = "infrastructure"
    QUALITY_ASSURANCE = "quality_assurance"
    GENERAL = "general"


class MessagePriority(Enum):
    """Message priorities for archiving"""
    URGENT = "urgent"
    HIGH = "high"
    NORMAL = "normal"
    LOW = "low"


@dataclass
class ArchivedMessage:
    """Archived message data structure"""
    message_id: str
    timestamp: datetime
    sender: str
    recipient: str
    message_type: MessageType
    priority: MessagePriority
    subject: str
    content: str
    status: str = "archived"
    processed_at: Optional[datetime] = None
    processing_notes: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class MessageArchive:
    """Comprehensive message archiving system"""

    def __init__(self, archive_dir: str = "message_archive"):
        self.archive_dir = Path(archive_dir)
        self.archive_dir.mkdir(exist_ok=True)
        self.messages: Dict[str, ArchivedMessage] = {}
        self.load_existing_archive()

    def archive_message(
        self,
        message_id: str,
        sender: str,
        recipient: str,
        message_type: MessageType,
        priority: MessagePriority,
        subject: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Archive a message with full metadata"""

        archived_msg = ArchivedMessage(
            message_id=message_id,
            timestamp=datetime.now(),
            sender=sender,
            recipient=recipient,
            message_type=message_type,
            priority=priority,
            subject=subject,
            content=content,
            metadata=metadata or {}
        )

        self.messages[message_id] = archived_msg
        self._save_to_file(archived_msg)

        logger.info(f"Message archived: {message_id} ({message_type.value})")
        return message_id

    def update_message_status(
        self,
        message_id: str,
        status: str,
        processing_notes: Optional[str] = None
    ) -> bool:
        """Update the status of an archived message"""

        if message_id not in self.messages:
            logger.warning(f"Message not found for status update: {message_id}")
            return False

        message = self.messages[message_id]
        message.status = status
        message.processed_at = datetime.now()
        if processing_notes:
            message.processing_notes = processing_notes

        self._save_to_file(message)
        logger.info(f"Message status updated: {message_id} -> {status}")
        return True

    def get_messages_by_type(self, message_type: MessageType) -> List[ArchivedMessage]:
        """Get all messages of a specific type"""
        return [msg for msg in self.messages.values() if msg.message_type == message_type]

    def get_messages_by_sender(self, sender: str) -> List[ArchivedMessage]:
        """Get all messages from a specific sender"""
        return [msg for msg in self.messages.values() if msg.sender == sender]

    def get_messages_by_priority(self, priority: MessagePriority) -> List[ArchivedMessage]:
        """Get all messages of a specific priority"""
        return [msg for msg in self.messages.values() if msg.priority == priority]

    def get_recent_messages(self, hours: int = 24) -> List[ArchivedMessage]:
        """Get messages from the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        return [msg for msg in self.messages.values() if msg.timestamp > cutoff]

    def get_unprocessed_messages(self) -> List[ArchivedMessage]:
        """Get messages that haven't been processed yet"""
        return [msg for msg in self.messages.values() if msg.status != "processed"]

    def archive_coordination_message(
        self,
        sender: str,
        recipient: str,
        subject: str,
        content: str,
        priority: str = "normal"
    ) -> str:
        """Convenience method for archiving coordination messages"""

        message_id = f"coord_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{sender}_{recipient}"

        try:
            priority_enum = MessagePriority(priority.upper())
        except ValueError:
            priority_enum = MessagePriority.NORMAL

        return self.archive_message(
            message_id=message_id,
            sender=sender,
            recipient=recipient,
            message_type=MessageType.COORDINATION,
            priority=priority_enum,
            subject=subject,
            content=content
        )

    def generate_archive_report(self) -> str:
        """Generate a comprehensive archive report"""

        total_messages = len(self.messages)
        recent_messages = len(self.get_recent_messages(24))
        unprocessed = len(self.get_unprocessed_messages())

        # Message type breakdown
        type_breakdown = {}
        for msg_type in MessageType:
            count = len(self.get_messages_by_type(msg_type))
            if count > 0:
                type_breakdown[msg_type.value] = count

        # Priority breakdown
        priority_breakdown = {}
        for priority in MessagePriority:
            count = len(self.get_messages_by_priority(priority))
            if count > 0:
                priority_breakdown[priority.value] = count

        report = []
        report.append("=" * 60)
        report.append("MESSAGE ARCHIVE SYSTEM REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")

        report.append("ARCHIVE STATISTICS:")
        report.append("-" * 20)
        report.append(f"Total Messages: {total_messages}")
        report.append(f"Recent (24h): {recent_messages}")
        report.append(f"Unprocessed: {unprocessed}")
        report.append("")

        if type_breakdown:
            report.append("MESSAGES BY TYPE:")
            report.append("-" * 18)
            for msg_type, count in type_breakdown.items():
                report.append(f"{msg_type.title()}: {count}")
            report.append("")

        if priority_breakdown:
            report.append("MESSAGES BY PRIORITY:")
            report.append("-" * 22)
            for priority, count in priority_breakdown.items():
                report.append(f"{priority.title()}: {count}")
            report.append("")

        report.append("COORDINATION STATUS:")
        report.append("-" * 20)
        if unprocessed > 0:
            report.append(f"⚠️  {unprocessed} messages awaiting processing")
        else:
            report.append("✅ All messages processed")
        report.append("")

        report.append("=" * 60)

        return "\n".join(report)

    def cleanup_old_messages(self, days_to_keep: int = 30):
        """Clean up messages older than specified days"""

        cutoff = datetime.now() - timedelta(days=days_to_keep)
        to_remove = []

        for message_id, message in self.messages.items():
            if message.timestamp < cutoff:
                to_remove.append(message_id)

        for message_id in to_remove:
            del self.messages[message_id]
            archive_file = self.archive_dir / f"{message_id}.json"
            if archive_file.exists():
                archive_file.unlink()

        logger.info(f"Cleaned up {len(to_remove)} old messages")
        return len(to_remove)

    def _save_to_file(self, message: ArchivedMessage):
        """Save message to archive file"""

        archive_file = self.archive_dir / f"{message.message_id}.json"

        data = {
            'message_id': message.message_id,
            'timestamp': message.timestamp.isoformat(),
            'sender': message.sender,
            'recipient': message.recipient,
            'message_type': message.message_type.value,
            'priority': message.priority.value,
            'subject': message.subject,
            'content': message.content,
            'status': message.status,
            'processed_at': message.processed_at.isoformat() if message.processed_at else None,
            'processing_notes': message.processing_notes,
            'metadata': message.metadata
        }

        with open(archive_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_existing_archive(self):
        """Load existing archived messages"""

        if not self.archive_dir.exists():
            return

        loaded_count = 0
        for archive_file in self.archive_dir.glob("*.json"):
            try:
                with open(archive_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                message = ArchivedMessage(
                    message_id=data['message_id'],
                    timestamp=datetime.fromisoformat(data['timestamp']),
                    sender=data['sender'],
                    recipient=data['recipient'],
                    message_type=MessageType(data['message_type']),
                    priority=MessagePriority(data['priority']),
                    subject=data['subject'],
                    content=data['content'],
                    status=data['status'],
                    processed_at=datetime.fromisoformat(data['processed_at']) if data.get('processed_at') else None,
                    processing_notes=data.get('processing_notes'),
                    metadata=data.get('metadata', {})
                )

                self.messages[message.message_id] = message
                loaded_count += 1

            except Exception as e:
                logger.warning(f"Failed to load archived message {archive_file}: {e}")

        logger.info(f"Loaded {loaded_count} archived messages")


# Global message archive instance
message_archive = MessageArchive()


def archive_coordination_message(
    sender: str,
    recipient: str,
    subject: str,
    content: str,
    priority: str = "normal"
) -> str:
    """Convenience function for archiving coordination messages"""
    return message_archive.archive_coordination_message(sender, recipient, subject, content, priority)


def update_message_status(
    message_id: str,
    status: str,
    processing_notes: Optional[str] = None
) -> bool:
    """Convenience function for updating message status"""
    return message_archive.update_message_status(message_id, status, processing_notes)


def get_archive_report() -> str:
    """Convenience function for getting archive report"""
    return message_archive.generate_archive_report()


if __name__ == "__main__":
    # Example usage
    print("Testing Message Archive System...")

    # Archive a coordination message
    msg_id = archive_coordination_message(
        sender="Agent-1",
        recipient="Agent-2",
        subject="Communication Improvement Coordination",
        content="Supporting enhanced inter-agent communication protocols",
        priority="urgent"
    )
    print(f"Archived message: {msg_id}")

    # Update status
    update_message_status(msg_id, "processed", "Coordination protocols enhanced")
    print("Message status updated")

    # Generate report
    report = get_archive_report()
    print("\nArchive Report:")
    print(report)

    print("Message Archive System ready for swarm coordination!")
