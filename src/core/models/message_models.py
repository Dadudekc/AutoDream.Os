#!/usr/bin/env python3
"""
Message Models Module - Agent Cellphone V2

Provides communication and messaging models for the unified framework.

Author: Agent-3 Integration & Testing Specialist
Task: TASK 3J - Model & Enum Consolidation (V2 Compliance Refactoring)
V2 Standards: ≤400 LOC, SRP, OOP principles
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

try:
    from src.core.models.base_models import StatusModel, TypedModel
    from src.core.models.unified_enums import UnifiedStatus, UnifiedPriority, UnifiedType
except ImportError:
    from base_models import StatusModel, TypedModel
    from unified_enums import UnifiedStatus, UnifiedPriority, UnifiedType

logger = logging.getLogger(__name__)

# ============================================================================
# MESSAGE MODELS - Communication implementations
# ============================================================================

@dataclass
class MessageModel(StatusModel, TypedModel):
    """Communication model with sender, recipient, content, and status tracking"""
    
    sender: str = ""
    recipient: str = ""
    subject: str = ""
    content: str = ""
    message_type: str = "text"
    priority: UnifiedPriority = UnifiedPriority.MEDIUM
    delivery_status: str = "pending"
    read_status: bool = False
    attachments: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.MESSAGE
        self.category = "communication"
    
    def mark_as_read(self) -> None:
        """Mark message as read"""
        if not self.read_status:
            self.read_status = True
            self.update_timestamp()
            self.update_status(UnifiedStatus.COMPLETED, "Message read")
    
    def update_delivery_status(self, status: str, details: str = None) -> None:
        """Update message delivery status"""
        self.delivery_status = status
        self.update_timestamp()
        
        # Update overall status based on delivery
        if status == "delivered":
            self.update_status(UnifiedStatus.COMPLETED, "Message delivered")
        elif status == "failed":
            self.update_status(UnifiedStatus.FAILED, f"Delivery failed: {details}")
        elif status == "pending":
            self.update_status(UnifiedStatus.PENDING, "Delivery pending")
    
    def add_attachment(self, attachment_id: str) -> None:
        """Add an attachment to the message"""
        if attachment_id not in self.attachments:
            self.attachments.append(attachment_id)
            self.update_timestamp()
    
    def get_message_summary(self) -> Dict[str, Any]:
        """Get comprehensive message summary"""
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "subject": self.subject,
            "message_type": self.message_type,
            "priority": self.priority.value,
            "delivery_status": self.delivery_status,
            "read_status": self.read_status,
            "attachments_count": len(self.attachments),
            "content_length": len(self.content)
        }


@dataclass
class NotificationModel(StatusModel, TypedModel):
    """Notification model for system alerts and user notifications"""
    
    notification_type: str = "info"
    title: str = ""
    message: str = ""
    target_user: str = ""
    target_system: str = ""
    action_required: bool = False
    action_url: Optional[str] = None
    expires_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Post-initialization setup"""
        super().__post_init__()
        self.model_type = UnifiedType.ALERT
        self.category = "notification"
    
    def mark_as_read(self) -> None:
        """Mark notification as read"""
        self.update_status(UnifiedStatus.COMPLETED, "Notification read")
    
    def is_expired(self) -> bool:
        """Check if notification has expired"""
        if self.expires_at:
            return datetime.now() > self.expires_at
        return False
    
    def get_notification_summary(self) -> Dict[str, Any]:
        """Get comprehensive notification summary"""
        return {
            "notification_type": self.notification_type,
            "title": self.title,
            "target_user": self.target_user,
            "target_system": self.target_system,
            "action_required": self.action_required,
            "action_url": self.action_url,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "is_expired": self.is_expired()
        }


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def create_message_model(**kwargs) -> MessageModel:
    """Create a message model with specified parameters"""
    return MessageModel(**kwargs)


def create_notification_model(**kwargs) -> NotificationModel:
    """Create a notification model with specified parameters"""
    return NotificationModel(**kwargs)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for message models module"""
    print("🚀 MESSAGE MODELS MODULE - TASK 3J V2 Refactoring")
    print("=" * 55)
    
    # Create example models
    message_model = create_message_model(subject="Test Message", sender="Agent-3")
    notification_model = create_notification_model(title="System Alert", message="System ready")
    
    print(f"✅ Message Model Created: {message_model.id}")
    print(f"✅ Notification Model Created: {notification_model.id}")
    
    # Test functionality
    message_model.mark_as_read()
    notification_model.mark_as_read()
    
    print(f"\n✅ Message Read: {message_model.read_status}")
    print(f"✅ Notification Status: {notification_model.status.value}")
    
    print("\n🎯 Message Models Module Ready!")
    return 0


if __name__ == "__main__":
    exit(main())
