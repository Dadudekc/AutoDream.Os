#!/usr/bin/env python3
"""
Devlog Enforcement Reporting Module - V2 Compliant
================================================

Modular component for devlog enforcement reporting and status display.
Part of the refactored devlog enforcement system.

Author: Agent-7 - Web Development Specialist
License: MIT
"""



class DevlogEnforcementReporting:
    """Handles devlog enforcement reporting and status display."""

    def __init__(
        self,
        enforcement_config: Dict[str, Any],
        devlog_system,
        violation_summary: Dict[str, Any],
    ):
        """Initialize reporting handler."""
        self.enforcement_config = enforcement_config
        self.devlog = devlog_system
        self.violation_summary = violation_summary

    def get_enforcement_status(self) -> Dict[str, Any]:
        """Get current enforcement system status."""
        return {
            "enforcement_level": self.enforcement_config["enforcement_level"],
            "mandatory_operations": self.enforcement_config["mandatory_operations"],
            "total_violations": self.violation_summary["total_violations"],
            "auto_devlog_fallback": self.enforcement_config["auto_devlog_fallback"],
            "devlog_system_status": self.devlog.get_status(),
        }

    def print_enforcement_report(self) -> None:
        """Print comprehensive enforcement report."""
        get_logger(__name__).info("🔍 DEVLOG ENFORCEMENT REPORT")
        get_logger(__name__).info("=" * 50)

        status = self.get_enforcement_status()

        get_logger(__name__).info(f"📊 Enforcement Level: {status['enforcement_level'].upper()}")
        get_logger(__name__).info(f"📝 Mandatory Operations: {len(status['mandatory_operations'])}")
        get_logger(__name__).info(f"⚠️  Total Violations: {status['total_violations']}")
        get_logger(__name__).info(
            f"🤖 Auto Devlog Fallback: {'✅ Enabled' if status['auto_devlog_fallback'] else '❌ Disabled'}"
        )

        get_logger(__name__).info("\n📋 MANDATORY OPERATIONS:")
        for operation in status["mandatory_operations"]:
            get_logger(__name__).info(f"  • {operation}")

        get_logger(__name__).info("\n📂 REQUIRED CATEGORIES:")
        for category in self.enforcement_config["required_categories"]:
            get_logger(__name__).info(f"  • {category}")

        if status["total_violations"] > 0:
            get_logger(__name__).info(f"\n⚠️  RECENT VIOLATIONS:")
            recent_violations = self.violation_summary["recent_violations"]
            for violation in recent_violations:
                get_logger(__name__).info(f"  • {violation['agent_id']}: {violation['violation_type']}")

        get_logger(__name__).info("\n💡 USAGE:")
        get_logger(__name__).info('  python scripts/devlog.py "Title" "Content" --category [category]')
        get_logger(__name__).info('  python -m src.core.devlog_cli create "Title" "Content" [category]')

    def print_quick_status(self) -> None:
        """Print quick enforcement status."""
        status = self.get_enforcement_status()
        violations = self.violation_summary["total_violations"]

        status_icon = "✅" if violations == 0 else "⚠️"
        get_logger(__name__).info(
            f"{status_icon} Devlog Enforcement: {status['enforcement_level'].upper()} | Violations: {violations}"
        )

