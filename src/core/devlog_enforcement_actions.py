#!/usr/bin/env python3
"""
Devlog Enforcement Actions Module - V2 Compliant
===============================================

Modular component for handling devlog enforcement actions and violations.
Part of the refactored devlog enforcement system.

Author: Agent-7 - Web Development Specialist
License: MIT
"""



class DevlogEnforcementActions:
    """Handles devlog enforcement actions and violation management."""

    def __init__(self, enforcement_config: Dict[str, Any], devlog_system):
        """Initialize enforcement actions handler."""
        self.enforcement_config = enforcement_config
        self.devlog = devlog_system
        self.violation_log = []

    def enforce_devlog_usage(
        self,
        operation_type: str,
        agent_id: str,
        title: str,
        content: str,
        category: str = "progress",
    ) -> bool:
        """
        Enforce devlog usage by creating entry if missing.

        Args:
            operation_type: Type of operation
            agent_id: Agent performing operation
            title: Devlog entry title
            content: Devlog entry content
            category: Devlog category

        Returns:
            bool: True if devlog entry created successfully
        """
        if not self.enforcement_config["auto_devlog_fallback"]:
            return False

        try:
            # Create devlog entry
            success = self.devlog.create_entry(title, content, category)

            if success:
                get_logger(__name__).info(f"✅ DEVLOG ENFORCEMENT: Entry created for {operation_type}")
                return True
            else:
                get_logger(__name__).info(
                    f"❌ DEVLOG ENFORCEMENT: Failed to create entry for {operation_type}"
                )
                return False

        except Exception as e:
            get_logger(__name__).info(f"❌ DEVLOG ENFORCEMENT ERROR: {e}")
            return False

    def log_violation(
        self, agent_id: str, violation_type: str, details: str, operation_type: str
    ) -> None:
        """Log a devlog enforcement violation."""
        violation = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "violation_type": violation_type,
            "details": details,
            "operation_type": operation_type,
        }

        self.violation_log.append(violation)

        # Check if agent has exceeded violation threshold
        agent_violations = [v for v in self.violation_log if v["agent_id"] == agent_id]
        if len(agent_violations) >= self.enforcement_config["violation_threshold"]:
            self._trigger_enforcement_action(agent_id, agent_violations)

    def _trigger_enforcement_action(
        self, agent_id: str, violations: List[Dict[str, Any]]
    ) -> None:
        """Trigger enforcement action for repeated violations."""
        get_logger(__name__).info(
            f"🚨 DEVLOG ENFORCEMENT: Agent {agent_id} has {len(violations)} violations"
        )
        get_logger(__name__).info("   Mandatory devlog usage required for all operations")
        get_logger(__name__).info(
            '   Use: python scripts/devlog.py "Title" "Content" --category [category]'
        )

        # Could implement additional enforcement actions here
        # such as blocking operations, sending alerts, etc.

    def get_violation_summary(self) -> Dict[str, Any]:
        """Get summary of violations."""
        return {
            "total_violations": len(self.violation_log),
            "agents_with_violations": len(
                set(v["agent_id"] for v in self.violation_log)
            ),
            "recent_violations": self.violation_log[-5:] if self.violation_log else [],
        }

