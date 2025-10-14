"""
Recovery State
==============

State management for recovery system.

Author: Agent-6 (Quality Gates & VSCode Forking Specialist)
Refactored from: recovery.py (RecoverySystem class split)
License: MIT
"""


class RecoveryState:
    """Manages recovery system state."""

    def __init__(self, config: dict):
        """Initialize recovery state."""
        recovery_config = config.get("overnight", {}).get("recovery", {})

        # Configuration
        self.max_retries = recovery_config.get("max_retries", 3)
        self.escalation_threshold = recovery_config.get("escalation_threshold", 5)
        self.auto_recovery = recovery_config.get("auto_recovery", True)
        self.agent_rescue = recovery_config.get("agent_rescue", True)

        # State tracking
        self.recovery_attempts = {}
        self.failure_history = []
        self.escalated_issues = set()
        self.last_recovery_time = 0

    def initialize_agents(self) -> None:
        """Initialize agent recovery tracking."""
        self.recovery_attempts = {f"Agent-{i}": 0 for i in range(1, 9)}

    def get_status(self) -> dict:
        """Get current recovery status."""
        return {
            "max_retries": self.max_retries,
            "escalation_threshold": self.escalation_threshold,
            "auto_recovery": self.auto_recovery,
            "agent_rescue": self.agent_rescue,
            "recovery_attempts": self.recovery_attempts,
            "failure_history_count": len(self.failure_history),
            "escalated_issues_count": len(self.escalated_issues),
            "last_recovery_time": self.last_recovery_time,
        }
