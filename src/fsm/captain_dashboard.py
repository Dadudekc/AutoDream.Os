#!/usr/bin/env python3
"""
Captain Dashboard - V2 Compliant
===============================

Captain dashboard for monitoring agent status and activity.
Provides comprehensive view of agent states and inactivity.

Author: Agent-4 (Captain & Operations Coordinator)
License: MIT
"""

from datetime import datetime
from pathlib import Path

from .activity_monitor import get_activity_monitor
from .fsm_registry import get_state_summary

# V2 Compliance: File under 400 lines, functions under 30 lines


class CaptainDashboard:
    """Captain dashboard for agent monitoring and management."""

    def __init__(self):
        """Initialize captain dashboard."""
        self.activity_monitor = get_activity_monitor()

    def get_agent_status_report(self) -> dict[str, dict]:
        """Get comprehensive agent status report."""
        activity_summary = self.activity_monitor.get_agent_activity_summary()
        state_summary = get_state_summary()

        report = {}
        for agent_id, activity_data in activity_summary.items():
            current_state = activity_data["current_state"]
            is_inactive = activity_data["is_inactive"]
            is_messaging_inactive = activity_data["is_messaging_inactive"]

            # Determine status
            if is_inactive:
                status = "INACTIVE"
                status_color = "🔴"
                action_needed = "ONBOARD_OR_HIGH_PRIORITY_MESSAGE"
            elif is_messaging_inactive:
                status = "MESSAGING_INACTIVE"
                status_color = "🟡"
                action_needed = "SEND_HIGH_PRIORITY_MESSAGE"
            else:
                status = "ACTIVE"
                status_color = "🟢"
                action_needed = "NONE"

            report[agent_id] = {
                "status": status,
                "status_color": status_color,
                "current_state": current_state,
                "is_inactive": is_inactive,
                "is_messaging_inactive": is_messaging_inactive,
                "inactivity_reason": activity_data["inactivity_reason"],
                "messaging_reason": activity_data["messaging_reason"],
                "last_activity": activity_data["last_activity"],
                "activity_count": activity_data["activity_count"],
                "action_needed": action_needed,
            }

        return report

    def get_inactive_agents(self) -> list[dict[str, str]]:
        """Get list of inactive agents with details."""
        inactive_agents = []
        report = self.get_agent_status_report()

        for agent_id, data in report.items():
            if data["is_inactive"] or data["is_messaging_inactive"]:
                inactive_agents.append(
                    {
                        "agent_id": agent_id,
                        "status": data["status"],
                        "reason": data["inactivity_reason"]
                        if data["is_inactive"]
                        else data["messaging_reason"],
                        "action_needed": data["action_needed"],
                        "last_activity": data["last_activity"],
                    }
                )

        return inactive_agents

    def get_swarm_health_summary(self) -> dict[str, any]:
        """Get swarm health summary."""
        state_summary = get_state_summary()
        inactive_agents = self.get_inactive_agents()

        total_agents = state_summary["total_agents"]
        active_agents = state_summary["active_agents"]
        inactive_count = len(inactive_agents)

        health_percentage = (active_agents / total_agents * 100) if total_agents > 0 else 0

        return {
            "total_agents": total_agents,
            "active_agents": active_agents,
            "inactive_agents": inactive_count,
            "health_percentage": health_percentage,
            "swarm_state": state_summary["swarm_state"],
            "state_counts": state_summary["state_counts"],
            "health_status": "HEALTHY"
            if health_percentage >= 75
            else "DEGRADED"
            if health_percentage >= 50
            else "CRITICAL",
        }

    def generate_captain_report(self) -> str:
        """Generate comprehensive captain report."""
        health_summary = self.get_swarm_health_summary()
        inactive_agents = self.get_inactive_agents()
        report_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        report = f"""
🎯 CAPTAIN DASHBOARD REPORT
============================================================
📊 Report Time: {report_time}
🐝 Swarm State: {health_summary['swarm_state']}
📈 Health Status: {health_summary['health_status']} ({health_summary['health_percentage']:.1f}%)

📊 AGENT STATUS SUMMARY:
• Total Agents: {health_summary['total_agents']}
• Active Agents: {health_summary['active_agents']}
• Inactive Agents: {health_summary['inactive_agents']}

📋 STATE DISTRIBUTION:
"""

        for state, count in health_summary["state_counts"].items():
            report += f"• {state}: {count} agents\n"

        if inactive_agents:
            report += "\n🚨 INACTIVE AGENTS REQUIRING ATTENTION:\n"
            for agent in inactive_agents:
                report += f"• {agent['agent_id']}: {agent['status']} - {agent['reason']}\n"
                report += f"  Action Needed: {agent['action_needed']}\n"
                report += f"  Last Activity: {agent['last_activity'] or 'Never'}\n"
        else:
            report += "\n✅ ALL AGENTS ACTIVE - NO ACTION NEEDED\n"

        report += "\n🎯 RECOMMENDED ACTIONS:\n"
        if inactive_agents:
            for agent in inactive_agents:
                if agent["action_needed"] == "ONBOARD_OR_HIGH_PRIORITY_MESSAGE":
                    report += f"• {agent['agent_id']}: Send high-priority message or onboard\n"
                elif agent["action_needed"] == "SEND_HIGH_PRIORITY_MESSAGE":
                    report += f"• {agent['agent_id']}: Send high-priority message\n"
        else:
            report += "• No immediate actions required\n"

        report += "\n============================================================"

        return report

    def save_report(self, report: str, filename: str | None = None) -> str:
        """Save captain report to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captain_report_{timestamp}.md"

        report_path = Path("swarm_coordination/reports") / filename
        report_path.parent.mkdir(parents=True, exist_ok=True)

        report_path.write_text(report, encoding="utf-8")
        return str(report_path)

    def get_high_priority_message_template(self, agent_id: str, reason: str) -> str:
        """Get high-priority message template for inactive agent."""
        return f"""🚨 HIGH PRIORITY MESSAGE - AGENT ACTIVITY REQUIRED

Agent {agent_id}, you have been marked as inactive.

📊 INACTIVITY DETAILS:
• Reason: {reason}
• Action Required: Immediate response needed
• Priority: HIGH - Bypassing normal message queue

🎯 REQUIRED ACTIONS:
1. Check your inbox for pending messages
2. Update your status file
3. Report current task status
4. Confirm receipt of this message

📝 RESPONSE REQUIRED:
Please respond immediately to confirm you are active and operational.

🚨 This message was sent with high priority to bypass normal message queue.

"""


def get_captain_dashboard() -> CaptainDashboard:
    """Get singleton captain dashboard instance."""
    if not hasattr(get_captain_dashboard, "_instance"):
        get_captain_dashboard._instance = CaptainDashboard()
    return get_captain_dashboard._instance
