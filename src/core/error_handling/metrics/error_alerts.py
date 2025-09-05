"""
Error Alerts - V2 Compliance Module
==================================

Error alerts functionality for error handling system.

V2 Compliance: < 300 lines, single responsibility, error alerts.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

from datetime import datetime
from dataclasses import dataclass, field
from typing import Dict, Any, List

from ..error_models_enums import ErrorSeverity


@dataclass
class ErrorAlert:
    """Error alert with V2 compliance."""
    alert_id: str
    error_id: str
    severity: ErrorSeverity
    message: str
    recipients: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    acknowledged: bool = False
    acknowledged_by: str = None
    acknowledged_at: datetime = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Post-initialization validation."""
        if not self.alert_id:
            raise ValueError("alert_id is required")
        if not self.error_id:
            raise ValueError("error_id is required")
        if not self.message:
            raise ValueError("message is required")
    
    def acknowledge(self, acknowledged_by: str) -> None:
        """Acknowledge the alert."""
        self.acknowledged = True
        self.acknowledged_by = acknowledged_by
        self.acknowledged_at = datetime.now()
    
    def add_recipient(self, recipient: str) -> None:
        """Add recipient to alert."""
        if recipient not in self.recipients:
            self.recipients.append(recipient)
    
    def remove_recipient(self, recipient: str) -> None:
        """Remove recipient from alert."""
        if recipient in self.recipients:
            self.recipients.remove(recipient)
    
    def is_high_priority(self) -> bool:
        """Check if alert is high priority."""
        return self.severity in [ErrorSeverity.CRITICAL, ErrorSeverity.HIGH]
    
    def get_summary(self) -> Dict[str, Any]:
        """Get alert summary."""
        return {
            "alert_id": self.alert_id,
            "error_id": self.error_id,
            "severity": self.severity.value,
            "message": self.message,
            "acknowledged": self.acknowledged,
            "recipients_count": len(self.recipients),
            "created_at": self.created_at.isoformat()
        }
