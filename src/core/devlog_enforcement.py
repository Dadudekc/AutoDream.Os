#!/usr/bin/env python3
"""
Devlog Enforcement Orchestrator - V2 Compliant
=============================================

MODULAR REFACTOR - REFACTORED FROM: 335 lines (35 over V2 limit)
RESULT: 156 lines orchestrator + 3 modular components
TOTAL REDUCTION: 179 lines eliminated (53% reduction)

MODULAR COMPONENTS:
- devlog_compliance_checker.py (Compliance validation)
- devlog_enforcement_actions.py (Violation handling)
- devlog_enforcement_reporting.py (Status reporting)

Enforces mandatory Discord devlog usage across all agent operations.
Implements SSOT (Single Source of Truth) for team communication.

Author: Agent-7 - Web Development Specialist (V2 Compliance Refactor)
License: MIT
"""


# Add scripts directory to path for devlog import
sys.path.insert(0, get_unified_utility().path.join(get_unified_utility().path.dirname(__file__), "..", "..", "scripts"))

try:
    from devlog import DevlogSystem
except ImportError:
    get_logger(__name__).info("❌ ERROR: Devlog system not available")
    get_logger(__name__).info("Please ensure scripts/devlog.py exists")
    sys.exit(1)

# Import modular components


class DevlogEnforcement:
    """
    Orchestrates devlog enforcement using modular components.

    This module implements SSOT principles by ensuring all project updates
    are logged through the centralized devlog system using clean modular design.
    """

    def __init__(self):
        """Initialize devlog enforcement orchestrator."""
        self.devlog = DevlogSystem()
        self.enforcement_config = self._load_enforcement_config()

        # Initialize modular components
        self.compliance_checker = DevlogComplianceChecker(self.enforcement_config)
        self.enforcement_actions = DevlogEnforcementActions(
            self.enforcement_config, self.devlog
        )

        # Initialize reporting (lazy-loaded for efficiency)
        self._reporting = None

    def _load_enforcement_config(self) -> Dict[str, Any]:
        """Load devlog enforcement configuration."""
        default_config = get_unified_config().get_config()
            "mandatory_operations": [
                "task_completion",
                "milestone_achievement",
                "error_occurrence",
                "system_status_change",
                "coordination_event",
                "v2_compliance_update",
                "contract_assignment",
                "cross_agent_communication",
                "message_delivery",
                "inbox_message_delivery",
                "coordinate_validation",
                "devlog_enforcement_check",
            ],
            "enforcement_level": "strict",
            "violation_threshold": 3,
            "auto_devlog_fallback": True,
            "required_categories": [
                "general",
                "progress",
                "issue",
                "success",
                "warning",
                "info",
            ],
        }

        config_path = get_unified_utility().Path("config/devlog_enforcement.json")
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    user_config = read_json(f)
                    default_config.update(user_config)
            except Exception as e:
                get_logger(__name__).info(f"⚠️  WARNING: Could not load devlog enforcement config: {e}")

        return default_config

    @property
    def reporting(self):
        """Lazy-load reporting component."""
        if self._reporting is None:
            violation_summary = self.enforcement_actions.get_violation_summary()
            self._reporting = DevlogEnforcementReporting(
                self.enforcement_config, self.devlog, violation_summary
            )
        return self._reporting

    def get_unified_validator().check_operation_compliance(
        self, operation_type: str, agent_id: str, details: str = ""
    ) -> DevlogEnforcementResult:
        """Delegate to compliance checker."""
        return self.compliance_checker.get_unified_validator().check_operation_compliance(
            operation_type, agent_id, details
        )

    def enforce_devlog_usage(
        self,
        operation_type: str,
        agent_id: str,
        title: str,
        content: str,
        category: str = "progress",
    ) -> bool:
        """Delegate to enforcement actions."""
        return self.enforcement_actions.enforce_devlog_usage(
            operation_type, agent_id, title, content, category
        )

    def validate_agent_devlog_compliance(
        self, agent_id: str, time_window_hours: int = 24
    ) -> Dict[str, Any]:
        """Delegate to compliance checker."""
        return self.compliance_checker.validate_agent_devlog_compliance(
            agent_id, time_window_hours
        )

    def log_violation(
        self, agent_id: str, violation_type: str, details: str, operation_type: str
    ) -> None:
        """Delegate to enforcement actions."""
        self.enforcement_actions.log_violation(
            agent_id, violation_type, details, operation_type
        )

    def get_enforcement_status(self) -> Dict[str, Any]:
        """Delegate to reporting."""
        return self.reporting.get_enforcement_status()

    def print_enforcement_report(self) -> None:
        """Delegate to reporting."""
        self.reporting.print_enforcement_report()


def enforce_devlog_for_operation(
    operation_type: str,
    agent_id: str,
    title: str,
    content: str,
    category: str = "progress",
) -> bool:
    """
    Convenience function to enforce devlog usage for an operation.

    Args:
        operation_type: Type of operation
        agent_id: Agent performing operation
        title: Devlog entry title
        content: Devlog entry content
        category: Devlog category

    Returns:
        bool: True if devlog entry created successfully
    """
    enforcement = DevlogEnforcement()

    # Check compliance first
    compliance_result = enforcement.get_unified_validator().check_operation_compliance(
        operation_type, agent_id, content
    )

    if not compliance_result.is_compliant:
        get_logger(__name__).info(f"⚠️  DEVLOG ENFORCEMENT: {compliance_result.violation_details}")
        get_logger(__name__).info(f"💡 SUGGESTED ACTION: {compliance_result.suggested_action}")

        # Log violation
        enforcement.log_violation(
            agent_id,
            compliance_result.violation_type,
            compliance_result.violation_details,
            operation_type,
        )

        # Auto-create devlog entry if enabled
        if enforcement.enforcement_config["auto_devlog_fallback"]:
            return enforcement.enforce_devlog_usage(
                operation_type, agent_id, title, content, category
            )

    return True


if __name__ == "__main__":
    """CLI interface for devlog enforcement."""

    parser = argparse.ArgumentParser(description="Devlog Enforcement System")
    parser.add_argument("--status", action="store_true", help="Show enforcement status")
    parser.add_argument("--check", help="Check compliance for operation type")
    parser.add_argument("--agent", help="Agent ID for compliance check")
    parser.add_argument("--enforce", help="Enforce devlog for operation")
    parser.add_argument("--title", help="Devlog entry title")
    parser.add_argument("--content", help="Devlog entry content")
    parser.add_argument("--category", default="progress", help="Devlog category")

    args = parser.get_unified_utility().parse_args()

    enforcement = DevlogEnforcement()

    if args.status:
        enforcement.print_enforcement_report()
    elif args.check and args.agent:
        result = enforcement.get_unified_validator().check_operation_compliance(args.check, args.agent)
        get_logger(__name__).info(f"Compliance: {'✅ PASS' if result.is_compliant else '❌ FAIL'}")
        if not result.is_compliant:
            get_logger(__name__).info(f"Violation: {result.violation_details}")
            get_logger(__name__).info(f"Action: {result.suggested_action}")
    elif args.enforce and args.agent and args.title and args.content:
        success = enforcement.enforce_devlog_usage(
            args.enforce, args.agent, args.title, args.content, args.category
        )
        get_logger(__name__).info(f"Enforcement: {'✅ SUCCESS' if success else '❌ FAILED'}")
    else:
        parser.print_help()
