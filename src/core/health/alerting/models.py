from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Any, Optional


class AlertSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class AlertStatus(Enum):
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    EXPIRED = "expired"
    SUPPRESSED = "suppressed"


class NotificationChannel(Enum):
    EMAIL = "email"
    SLACK = "slack"
    WEBHOOK = "webhook"
    SMS = "sms"
    PAGER_DUTY = "pager_duty"
    CONSOLE = "console"
    LOG = "log"


class EscalationLevel(Enum):
    LEVEL_1 = "level_1"
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"


@dataclass
class AlertRule:
    rule_id: str
    name: str
    description: str
    severity: AlertSeverity
    conditions: Dict[str, Any]
    enabled: bool = True
    cooldown_period: int = 300
    escalation_enabled: bool = True
    notification_channels: List[NotificationChannel] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class HealthAlert:
    alert_id: str
    agent_id: str
    severity: AlertSeverity
    message: str
    metric_type: str
    current_value: float
    threshold: float
    timestamp: datetime
    status: AlertStatus = AlertStatus.ACTIVE
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None
    resolved_by: Optional[str] = None
    resolved_at: Optional[datetime] = None
    escalation_level: EscalationLevel = EscalationLevel.LEVEL_1
    notification_sent: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NotificationConfig:
    channel: NotificationChannel
    enabled: bool = True
    recipients: List[str] = field(default_factory=list)
    template: str = ""
    retry_attempts: int = 3
    retry_delay: int = 60
    custom_parameters: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EscalationPolicy:
    level: EscalationLevel
    delay_minutes: int
    contacts: List[str]
    notification_channels: List[NotificationChannel]
    auto_escalate: bool = True
    require_acknowledgment: bool = False
