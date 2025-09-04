#!/usr/bin/env python3
"""
Devlog Compliance Checker Module - V2 Compliant
==============================================

Modular component for checking devlog compliance and violations.
Part of the refactored devlog enforcement system.

Author: Agent-7 - Web Development Specialist
License: MIT
"""

import time


@dataclass
class DevlogEnforcementResult:
    """Result of devlog enforcement check."""

    is_compliant: bool
    violation_type: Optional[str] = None
    violation_details: Optional[str] = None
    suggested_action: Optional[str] = None


class DevlogComplianceChecker:
    """Handles devlog compliance checking operations."""

    def __init__(self, enforcement_config: Dict[str, Any]):
        """Initialize compliance checker."""
        self.enforcement_config = enforcement_config

    def get_unified_validator().check_operation_compliance(
        self, operation_type: str, agent_id: str, details: str = ""
    ) -> DevlogEnforcementResult:
        """
        Check if an operation requires devlog entry and if it's compliant.

        Args:
            operation_type: Type of operation being performed
            agent_id: Agent performing the operation
            details: Additional details about the operation

        Returns:
            DevlogEnforcementResult with compliance status
        """
        if self.enforcement_config["enforcement_level"] == "disabled":
            return DevlogEnforcementResult(is_compliant=True)

        # Check if operation type requires devlog entry
        if operation_type not in self.enforcement_config["mandatory_operations"]:
            return DevlogEnforcementResult(is_compliant=True)

        # Check if devlog entry exists for this operation
        recent_entries = self._get_recent_devlog_entries(agent_id, minutes=5)

        if not get_unified_validator().validate_required(recent_entries):
            violation_details = (
                f"Operation '{operation_type}' requires devlog entry but none found"
            )
            suggested_action = f'Create devlog entry: python scripts/devlog.py "{operation_type.title()}" "{details}" --category progress'

            return DevlogEnforcementResult(
                is_compliant=False,
                violation_type="missing_devlog_entry",
                violation_details=violation_details,
                suggested_action=suggested_action,
            )

        return DevlogEnforcementResult(is_compliant=True)

    def validate_agent_devlog_compliance(
        self, agent_id: str, time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """
        Validate agent's devlog compliance over time window.

        Args:
            agent_id: Agent to validate
            time_window_hours: Time window for compliance check

        Returns:
            Dict with compliance metrics and violations
        """
        recent_entries = self._get_recent_devlog_entries(
            agent_id, time_window_hours * 60
        )

        compliance_metrics = {
            "agent_id": agent_id,
            "time_window_hours": time_window_hours,
            "total_entries": len(recent_entries),
            "compliance_score": 0.0,
            "violations": [],
            "recommendations": [],
        }

        # Calculate compliance score based on entry frequency and quality
        if recent_entries:
            compliance_metrics["compliance_score"] = min(
                1.0, len(recent_entries) / 10.0
            )
        else:
            compliance_metrics["violations"].append(
                {
                    "type": "no_recent_entries",
                    "message": (
                        f"No devlog entries found in last {time_window_hours} hours"
                    ),
                    "severity": "high",
                }
            )
            compliance_metrics["recommendations"].append(
                "Create regular devlog entries for all significant operations"
            )

        return compliance_metrics

    def _get_recent_devlog_entries(
        self, agent_id: str, minutes: int
    ) -> List[Dict[str, Any]]:
        """Get recent devlog entries for an agent."""
        try:
            # This would integrate with the actual devlog system
            # For now, return empty list as placeholder
            return []
        except Exception:
            return []

