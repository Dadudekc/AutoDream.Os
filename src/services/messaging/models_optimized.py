"""
Optimized Messaging Models
=========================

Refactored messaging models using base classes and shared imports.
Eliminates overcomplexity while maintaining functionality.
"""

from src.core.shared_imports import *
from src.core.base_classes import BaseModel, BaseConfig


# Simplified Enums (reduced from 6 to 3)
class MessageType(Enum):
    """Message types - simplified."""
    TEXT = "text"
    BROADCAST = "broadcast"
    ONBOARDING = "onboarding"
    AGENT_TO_AGENT = "agent_to_agent"


class MessagePriority(Enum):
    """Message priorities - simplified."""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"


class MessageTag(Enum):
    """Message tags - simplified."""
    GENERAL = "general"
    COORDINATION = "coordination"
    TASK = "task"
    STATUS = "status"


# Simplified Models (reduced from 7 to 3)
class Message(BaseModel):
    """Core message model - simplified."""
    
    def __init__(
        self,
        content: str,
        sender: str,
        recipient: str,
        message_type: MessageType = MessageType.TEXT,
        priority: MessagePriority = MessagePriority.NORMAL,
        tags: List[MessageTag] = None,
        metadata: Dict[str, Any] = None
    ):
        super().__init__()
        self.content = content
        self.sender = sender
        self.recipient = recipient
        self.message_type = message_type
        self.priority = priority
        self.tags = tags or []
        self.metadata = metadata or {}
        self.message_id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()


class MessageConfig(BaseConfig):
    """Message configuration - simplified."""
    
    def __init__(
        self,
        default_priority: MessagePriority = MessagePriority.NORMAL,
        max_retries: int = 3,
        timeout: int = 30
    ):
        super().__init__()
        self.default_priority = default_priority
        self.max_retries = max_retries
        self.timeout = timeout


class MessageResult(BaseModel):
    """Message result - simplified."""
    
    def __init__(
        self,
        success: bool,
        message: str = "",
        data: Any = None,
        error: Optional[str] = None
    ):
        super().__init__()
        self.success = success
        self.message = message
        self.data = data
        self.error = error


# Simplified Utilities (reduced parameters)
class MessageUtils:
    """Message utilities - simplified."""
    
    @staticmethod
    def create_message(
        content: str,
        sender: str,
        recipient: str,
        priority: str = "NORMAL"
    ) -> Message:
        """Create message with simplified parameters."""
        return Message(
            content=content,
            sender=sender,
            recipient=recipient,
            priority=MessagePriority(priority.lower())
        )
    
    @staticmethod
    def format_message(message: Message) -> str:
        """Format message for display."""
        return f"[{message.priority.value.upper()}] {message.sender} -> {message.recipient}: {message.content}"
    
    @staticmethod
    def validate_message(message: Message) -> bool:
        """Validate message content."""
        return bool(message.content and message.sender and message.recipient)


# Simplified Mappings (reduced complexity)
PRIORITY_MAP = {
    "low": MessagePriority.LOW,
    "normal": MessagePriority.NORMAL,
    "high": MessagePriority.HIGH,
    "urgent": MessagePriority.URGENT
}

TAG_MAP = {
    "general": MessageTag.GENERAL,
    "coordination": MessageTag.COORDINATION,
    "task": MessageTag.TASK,
    "status": MessageTag.STATUS
}


def map_priority(priority: str) -> MessagePriority:
    """Map priority string to enum."""
    return PRIORITY_MAP.get((priority or "normal").lower(), MessagePriority.NORMAL)


def map_tag(tag: str) -> MessageTag:
    """Map tag string to enum."""
    return TAG_MAP.get((tag or "general").lower(), MessageTag.GENERAL)
