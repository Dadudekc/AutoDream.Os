"""
Messaging Status Tracker

Handles message status tracking, reporting, and analytics for the messaging system.
"""

from .unified_messaging_imports import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from collections import defaultdict

from .models.messaging_models import (
    UnifiedMessage as Message,
    UnifiedMessagePriority as MessagePriority,
    UnifiedMessageType as MessageType,
    UnifiedMessageStatus as MessageStatus
)

logger = logging.getLogger(__name__)

class MessagingStatusTracker:
    """
    Tracks message status, generates reports, and provides analytics.
    """

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        # Status tracking
        self.message_status = {}
        self.delivery_history = []

        # Statistics
        self.stats = {
            'total_messages': 0,
            'delivered_messages': 0,
            'failed_messages': 0,
            'pending_messages': 0,
            'messages_by_type': defaultdict(int),
            'messages_by_priority': defaultdict(int),
            'messages_by_agent': defaultdict(int),
            'delivery_times': [],
            'failure_reasons': defaultdict(int)
        }

    def track_message_status(self, message: Message, status: MessageStatus,
                           error_message: str = None) -> None:
        """
        Track message status update.

        Args:
            message: Message being tracked
            status: New status
            error_message: Error message if applicable
        """
        try:
            message_id = get_unified_validator().safe_getattr(message, 'id', str(id(message)))

            # Update message status
            if message_id not in self.message_status:
                self.message_status[message_id] = {
                    'message': message,
                    'status_history': [],
                    'created_at': datetime.now().isoformat()
                }

            # Add status update
            status_update = {
                'status': status,
                'timestamp': datetime.now().isoformat(),
                'error_message': error_message
            }

            self.message_status[message_id]['status_history'].append(status_update)
            self.message_status[message_id]['current_status'] = status.value
            self.message_status[message_id]['updated_at'] = datetime.now().isoformat()

            # Update statistics
            self._update_statistics(message, status, error_message)

            self.get_logger(__name__).debug(f"📊 Status tracked for message {message_id}: {status.value}")

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error tracking message status: {e}")

    def _update_statistics(self, message: Message, status: MessageStatus,
                          error_message: str = None) -> None:
        """
        Update internal statistics based on message status.

        Args:
            message: Message being tracked
            status: New status
            error_message: Error message if applicable
        """
        try:
            # Update message counts
            self.stats['total_messages'] += 1

            if status == MessageStatus.DELIVERED:
                self.stats['delivered_messages'] += 1
                self.stats['pending_messages'] = max(0, self.stats['pending_messages'] - 1)
            elif status == MessageStatus.FAILED:
                self.stats['failed_messages'] += 1
                self.stats['pending_messages'] = max(0, self.stats['pending_messages'] - 1)
            elif status == MessageStatus.PENDING:
                self.stats['pending_messages'] += 1

            # Update type statistics
            self.stats['messages_by_type'][message.message_type.value] += 1

            # Update priority statistics
            self.stats['messages_by_priority'][message.priority.value] += 1

            # Update agent statistics
            self.stats['messages_by_agent'][message.sender] += 1
            self.stats['messages_by_agent'][message.recipient] += 1

            # Track failure reasons
            if status == MessageStatus.FAILED and error_message:
                self.stats['failure_reasons'][error_message] += 1

            # Track delivery times
            if status == MessageStatus.DELIVERED:
                created_time = datetime.fromisoformat(message.created_at)
                delivered_time = datetime.now()
                delivery_time = (delivered_time - created_time).total_seconds()

                if delivery_time > 0 and delivery_time < 3600:  # Under 1 hour
                    self.stats['delivery_times'].append(delivery_time)

                    # Keep only last 1000 delivery times
                    if len(self.stats['delivery_times']) > 1000:
                        self.stats['delivery_times'] = self.stats['delivery_times'][-1000:]

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error updating statistics: {e}")

    def get_message_status(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get status information for a specific message.

        Args:
            message_id: Message identifier

        Returns:
            Message status information or None
        """
        try:
            if message_id in self.message_status:
                return self.message_status[message_id].copy()
            return None

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error getting message status: {e}")
            return None

    def get_delivery_report(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate delivery report for the specified time range.

        Args:
            time_range_hours: Number of hours to look back

        Returns:
            Delivery report dictionary
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=time_range_hours)

            # Filter recent messages
            recent_messages = []
            for message_id, status_info in self.message_status.items():
                updated_time = datetime.fromisoformat(status_info['updated_at'])
                if updated_time >= cutoff_time:
                    recent_messages.append(status_info)

            # Calculate metrics
            total_recent = len(recent_messages)
            delivered_recent = sum(1 for msg in recent_messages
                                 if msg.get('current_status') == MessageStatus.DELIVERED.value)
            failed_recent = sum(1 for msg in recent_messages
                              if msg.get('current_status') == MessageStatus.FAILED.value)

            delivery_rate = (delivered_recent / total_recent * 100) if total_recent > 0 else 0

            # Calculate average delivery time
            delivery_times = []
            for msg in recent_messages:
                if msg.get('current_status') == MessageStatus.DELIVERED.value:
                    for status_update in msg['status_history']:
                        if status_update['status'] == MessageStatus.DELIVERED:
                            created_time = datetime.fromisoformat(msg['created_at'])
                            delivered_time = datetime.fromisoformat(status_update['timestamp'])
                            delivery_time = (delivered_time - created_time).total_seconds()
                            if delivery_time > 0 and delivery_time < 3600:
                                delivery_times.append(delivery_time)

            avg_delivery_time = sum(delivery_times) / len(delivery_times) if delivery_times else 0

            report = {
                'time_range_hours': time_range_hours,
                'total_messages': total_recent,
                'delivered_messages': delivered_recent,
                'failed_messages': failed_recent,
                'delivery_rate_percent': round(delivery_rate, 2),
                'average_delivery_time_seconds': round(avg_delivery_time, 2),
                'generated_at': datetime.now().isoformat()
            }

            return report

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error generating delivery report: {e}")
            return {}

    def get_agent_activity_report(self, agent_id: str,
                                time_range_hours: int = 24) -> Dict[str, Any]:
        """
        Generate activity report for a specific agent.

        Args:
            agent_id: Agent identifier
            time_range_hours: Number of hours to look back

        Returns:
            Agent activity report
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=time_range_hours)

            # Filter messages involving this agent
            agent_messages = []
            for message_id, status_info in self.message_status.items():
                message = status_info['message']
                if message.sender == agent_id or message.recipient == agent_id:
                    updated_time = datetime.fromisoformat(status_info['updated_at'])
                    if updated_time >= cutoff_time:
                        agent_messages.append(status_info)

            # Calculate metrics
            sent_messages = sum(1 for msg in agent_messages
                              if msg['message'].sender == agent_id)
            received_messages = sum(1 for msg in agent_messages
                                   if msg['message'].recipient == agent_id)

            successful_deliveries = sum(1 for msg in agent_messages
                                      if msg.get('current_status') == MessageStatus.DELIVERED.value
                                      and msg['message'].sender == agent_id)

            delivery_rate = (successful_deliveries / sent_messages * 100) if sent_messages > 0 else 0

            report = {
                'agent_id': agent_id,
                'time_range_hours': time_range_hours,
                'messages_sent': sent_messages,
                'messages_received': received_messages,
                'successful_deliveries': successful_deliveries,
                'delivery_rate_percent': round(delivery_rate, 2),
                'generated_at': datetime.now().isoformat()
            }

            return report

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error generating agent activity report: {e}")
            return {}

    def get_system_health_report(self) -> Dict[str, Any]:
        """
        Generate system health report.

        Returns:
            System health report
        """
        try:
            # Overall statistics
            total_messages = self.stats['total_messages']
            delivered_messages = self.stats['delivered_messages']
            failed_messages = self.stats['failed_messages']
            pending_messages = self.stats['pending_messages']

            # Calculate rates
            overall_delivery_rate = (delivered_messages / total_messages * 100) if total_messages > 0 else 0

            # Average delivery time
            avg_delivery_time = (sum(self.stats['delivery_times']) /
                               len(self.stats['delivery_times'])) if self.stats['delivery_times'] else 0

            # Top failure reasons
            top_failures = sorted(self.stats['failure_reasons'].items(),
                                key=lambda x: x[1], reverse=True)[:5]

            report = {
                'overall_stats': {
                    'total_messages': total_messages,
                    'delivered_messages': delivered_messages,
                    'failed_messages': failed_messages,
                    'pending_messages': pending_messages,
                    'delivery_rate_percent': round(overall_delivery_rate, 2),
                    'average_delivery_time_seconds': round(avg_delivery_time, 2)
                },
                'message_distribution': {
                    'by_type': dict(self.stats['messages_by_type']),
                    'by_priority': dict(self.stats['messages_by_priority'])
                },
                'top_failure_reasons': dict(top_failures),
                'active_agents': len(self.stats['messages_by_agent']),
                'generated_at': datetime.now().isoformat()
            }

            return report

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error generating system health report: {e}")
            return {}

    def cleanup_old_records(self, max_age_hours: int = 168) -> int:  # 1 week
        """
        Clean up old message records.

        Args:
            max_age_hours: Maximum age in hours for records to keep

        Returns:
            Number of records cleaned up
        """
        try:
            cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
            cleaned_count = 0

            # Clean message status records
            to_remove = []
            for message_id, status_info in self.message_status.items():
                updated_time = datetime.fromisoformat(status_info['updated_at'])
                if updated_time < cutoff_time:
                    to_remove.append(message_id)

            for message_id in to_remove:
                del self.message_status[message_id]
                cleaned_count += 1

            # Clean delivery history
            self.delivery_history = [
                record for record in self.delivery_history
                if datetime.fromisoformat(record.get('timestamp', '1970-01-01T00:00:00')) >= cutoff_time
            ]

            # Reset statistics (they'll rebuild from remaining records)
            self._rebuild_statistics()

            if cleaned_count > 0:
                self.get_logger(__name__).info(f"🧹 Cleaned up {cleaned_count} old message records")

            return cleaned_count

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error cleaning up old records: {e}")
            return 0

    def _rebuild_statistics(self) -> None:
        """
        Rebuild statistics from current message records.
        """
        try:
            # Reset statistics
            self.stats = {
                'total_messages': 0,
                'delivered_messages': 0,
                'failed_messages': 0,
                'pending_messages': 0,
                'messages_by_type': defaultdict(int),
                'messages_by_priority': defaultdict(int),
                'messages_by_agent': defaultdict(int),
                'delivery_times': [],
                'failure_reasons': defaultdict(int)
            }

            # Rebuild from current records
            for message_id, status_info in self.message_status.items():
                message = status_info['message']
                current_status = status_info.get('current_status')

                # Update counts
                self.stats['total_messages'] += 1

                if current_status == MessageStatus.DELIVERED.value:
                    self.stats['delivered_messages'] += 1
                elif current_status == MessageStatus.FAILED.value:
                    self.stats['failed_messages'] += 1
                elif current_status == MessageStatus.PENDING.value:
                    self.stats['pending_messages'] += 1

                # Update distributions
                self.stats['messages_by_type'][message.message_type.value] += 1
                self.stats['messages_by_priority'][message.priority.value] += 1
                self.stats['messages_by_agent'][message.sender] += 1
                self.stats['messages_by_agent'][message.recipient] += 1

                # Update failure reasons
                if current_status == MessageStatus.FAILED.value:
                    for status_update in status_info['status_history']:
                        if (status_update['status'] == MessageStatus.FAILED and
                            status_update.get('error_message')):
                            self.stats['failure_reasons'][status_update['error_message']] += 1

            self.get_logger(__name__).info("🔄 Statistics rebuilt from current records")

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error rebuilding statistics: {e}")

    def export_statistics(self, file_path: str) -> bool:
        """
        Export statistics to a file.

        Args:
            file_path: Path to save the statistics

        Returns:
            True if successful, False otherwise
        """
        try:
            export_data = {
                'statistics': self.stats,
                'export_timestamp': datetime.now().isoformat(),
                'total_tracked_messages': len(self.message_status)
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                write_json(export_data, f, indent=2, ensure_ascii=False)

            self.get_logger(__name__).info(f"📊 Statistics exported to {file_path}")
            return True

        except Exception as e:
            self.get_logger(__name__).error(f"❌ Error exporting statistics: {e}")
            return False

