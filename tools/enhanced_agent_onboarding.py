#!/usr/bin/env python3
"""
Enhanced Agent Onboarding System
================================

Provides complete project context to agents during onboarding.
Ensures full awareness of project dynamics and current status.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ProjectContextLoader:
    """Load project context for agent onboarding"""

    def __init__(self):
        """Initialize context loader"""
        self.project_root = Path(".")

    def get_system_health(self) -> dict[str, Any]:
        """Get current system health from watchdog"""
        health_report = self.project_root / "reports" / "health_report.json"
        if health_report.exists():
            with open(health_report) as f:
                return json.load(f)
        return {"status": "unknown", "health_score": 0}

    def get_quality_status(self) -> dict[str, Any]:
        """Get current quality status"""
        quality_report = self.project_root / "current_quality_status.json"
        if quality_report.exists():
            with open(quality_report) as f:
                data = json.load(f)
                return {
                    "compliance_rate": data.get("compliance_rate", 0),
                    "total_files": data.get("total_files", 0),
                    "violations": data.get("total_violations", 0),
                }
        return {"compliance_rate": 0, "total_files": 0, "violations": 0}

    def get_agent_statuses(self) -> list[dict[str, Any]]:
        """Get all agent statuses"""
        statuses = []
        workspace_dir = self.project_root / "agent_workspaces"

        for agent_id in [f"Agent-{i}" for i in range(1, 9)]:
            status_file = workspace_dir / agent_id / "status.json"
            if status_file.exists():
                with open(status_file) as f:
                    status = json.load(f)
                    statuses.append(
                        {
                            "agent_id": agent_id,
                            "status": status.get("status", "UNKNOWN"),
                            "role": status.get("current_role", "NONE"),
                            "health": status.get("health_score", 0),
                        }
                    )

        return statuses

    def get_current_initiatives(self) -> list[str]:
        """Get current active initiatives"""
        return [
            "Memory Leak Phase 1 Integration",
            "V2 Compliance Enforcement (43.3% → 77% target)",
            "Watchdog & Reporting System (OPERATIONAL)",
            "Quality Coordination Framework (DEPLOYED)",
            "High-Efficiency Protocol (20-30 issues/cycle target)",
        ]

    def get_critical_files(self) -> list[str]:
        """Get list of critical files to review"""
        return [
            "AGENTS.md",
            "config/agent_capabilities.json",
            "chatgpt_project_context.json",
            "project_analysis.json",
            "AGENT_USABILITY_REPORT.md",
            "AGENT_ONBOARDING_CONTEXT_PACKAGE.md",
        ]


class OnboardingContextBuilder:
    """Build comprehensive onboarding context"""

    def __init__(self, agent_id: str, assigned_role: str = "TASK_EXECUTOR"):
        """Initialize context builder"""
        self.agent_id = agent_id
        self.assigned_role = assigned_role
        self.context_loader = ProjectContextLoader()

    def build_onboarding_context(self) -> dict[str, Any]:
        """Build complete onboarding context"""
        return {
            "agent_info": {
                "agent_id": self.agent_id,
                "assigned_role": self.assigned_role,
                "onboarding_time": datetime.now().isoformat(),
            },
            "system_health": self.context_loader.get_system_health(),
            "quality_status": self.context_loader.get_quality_status(),
            "agent_statuses": self.context_loader.get_agent_statuses(),
            "current_initiatives": self.context_loader.get_current_initiatives(),
            "critical_files": self.context_loader.get_critical_files(),
        }

    def create_context_summary(self) -> str:
        """Create human-readable context summary"""
        context = self.build_onboarding_context()

        lines = []
        lines.append(f"🤖 ONBOARDING CONTEXT: {self.agent_id}")
        lines.append("=" * 60)
        lines.append("")

        # System Health
        health = context["system_health"]
        if "system_health" in health:
            sh = health["system_health"]
            lines.append("📊 SYSTEM HEALTH:")
            lines.append(f"  Status: {sh.get('overall_status', 'UNKNOWN')}")
            lines.append(f"  Health Score: {sh.get('health_score', 0):.1f}/100")
            lines.append(
                f"  Active Agents: {sh.get('active_agents', 0)}/{sh.get('total_agents', 0)}"
            )
            lines.append("")

        # Quality Status
        quality = context["quality_status"]
        lines.append("🎯 QUALITY STATUS:")
        lines.append(f"  V2 Compliance: {quality.get('compliance_rate', 0):.1f}%")
        lines.append(f"  Total Files: {quality.get('total_files', 0)}")
        lines.append(f"  Violations: {quality.get('violations', 0)}")
        lines.append("")

        # Agent Statuses
        lines.append("🤖 AGENT STATUS:")
        for agent in context["agent_statuses"]:
            status_emoji = "✅" if agent["status"] == "ACTIVE" else "❌"
            lines.append(
                f"  {status_emoji} {agent['agent_id']}: {agent['status']} | {agent['role']}"
            )
        lines.append("")

        # Current Initiatives
        lines.append("🚀 CURRENT INITIATIVES:")
        for initiative in context["current_initiatives"]:
            lines.append(f"  • {initiative}")
        lines.append("")

        # Critical Files
        lines.append("📚 CRITICAL FILES TO REVIEW:")
        for file in context["critical_files"]:
            lines.append(f"  • {file}")
        lines.append("")

        lines.append("✅ CONTEXT LOADED - READY FOR ACTIVATION")

        return "\n".join(lines)

    def save_context_package(self, output_dir: str = None) -> Path:
        """Save context package to agent workspace"""
        if not output_dir:
            output_dir = f"agent_workspaces/{self.agent_id}"

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save JSON context
        context_file = output_path / "onboarding_context.json"
        context = self.build_onboarding_context()
        with open(context_file, "w") as f:
            json.dump(context, f, indent=2)

        # Save summary
        summary_file = output_path / "onboarding_summary.txt"
        summary = self.create_context_summary()
        with open(summary_file, "w") as f:
            f.write(summary)

        logger.info(f"Onboarding context saved for {self.agent_id}")
        return context_file


class EnhancedOnboardingService:
    """Enhanced onboarding service with full context delivery"""

    def __init__(self):
        """Initialize enhanced onboarding service"""
        self.context_loader = ProjectContextLoader()

    def onboard_agent(self, agent_id: str, assigned_role: str = "TASK_EXECUTOR") -> dict[str, Any]:
        """Onboard agent with full context"""
        logger.info(f"Starting enhanced onboarding for {agent_id}")

        # Build context
        context_builder = OnboardingContextBuilder(agent_id, assigned_role)
        context = context_builder.build_onboarding_context()

        # Save context package
        context_file = context_builder.save_context_package()

        # Create onboarding message
        message = self._create_enhanced_onboarding_message(agent_id, assigned_role, context)

        # Save message to inbox
        self._save_to_inbox(agent_id, message)

        return {
            "success": True,
            "agent_id": agent_id,
            "assigned_role": assigned_role,
            "context_file": str(context_file),
            "message_delivered": True,
            "timestamp": datetime.now().isoformat(),
        }

    def _create_enhanced_onboarding_message(self, agent_id: str, role: str, context: dict) -> str:
        """Create enhanced onboarding message with context"""
        health = context.get("system_health", {}).get("system_health", {})
        quality = context.get("quality_status", {})

        return f"""🤖 ENHANCED ONBOARDING - {agent_id}
============================================================
[A2A] ONBOARDING WITH FULL PROJECT CONTEXT
============================================================
📤 FROM: Onboarding System
📥 TO: {agent_id}
🎭 ROLE: {role}
Priority: HIGH
Tags: ONBOARDING, CONTEXT_DELIVERY
-------------------------------------------------------------

✅ WELCOME TO V2_SWARM - FULL CONTEXT LOADED

📊 CURRENT PROJECT STATUS (IMMEDIATE AWARENESS):

System Health: {health.get('overall_status', 'UNKNOWN')} ({health.get('health_score', 0):.1f}/100)
Active Agents: {health.get('active_agents', 0)}/{health.get('total_agents', 0)}
V2 Compliance: {quality.get('compliance_rate', 0):.1f}%
Critical Violations: {quality.get('violations', 0)}

🎯 YOUR MISSION:
- Role: {role}
- Priority: Contribute to system health improvement
- Focus: V2 compliance enforcement & quality improvement
- Target: Help increase compliance from 43.3% to 77%

📚 CONTEXT FILES LOADED IN YOUR WORKSPACE:
✅ onboarding_context.json - Complete project context
✅ onboarding_summary.txt - Human-readable summary

📖 CRITICAL READING (REVIEW THESE FIRST):
1. AGENT_ONBOARDING_CONTEXT_PACKAGE.md - Full onboarding guide
2. AGENTS.md - System architecture & General Cycle
3. config/agent_capabilities.json - Your capabilities
4. AGENT_USABILITY_REPORT.md - Current project status

🛠️ IMMEDIATE ACTIONS:
1. Review your workspace: agent_workspaces/{agent_id}/
2. Check onboarding_context.json for full project state
3. Run: python watchdog.py (verify system health)
4. Query Swarm Brain for role patterns
5. Send confirmation to Captain Agent-4

⚡ QUICK START:
python watchdog.py  # Check system
cat agent_workspaces/{agent_id}/onboarding_context.json  # Your context
python tools/captain_cli.py status  # Agent statuses

🎯 COMPLETE ONBOARDING BY:
1. Reading all critical files
2. Understanding current priorities
3. Testing essential tools
4. Sending confirmation to Captain
5. Claiming your first task

-------------------------------------------------------------
✅ CONTEXT DELIVERY: COMPLETE
📊 Project Awareness: 100%
🤖 System Status: UNDERSTOOD
🎯 Role Clarity: DEFINED

🐝 WE ARE SWARM - {agent_id} onboarding with full context!
============================================================"""

    def _save_to_inbox(self, agent_id: str, message: str) -> None:
        """Save onboarding message to agent inbox"""
        inbox_dir = Path(f"agent_workspaces/{agent_id}/inbox")
        inbox_dir.mkdir(parents=True, exist_ok=True)

        message_file = inbox_dir / f"onboarding_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(message_file, "w") as f:
            f.write(message)


def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced Agent Onboarding")
    parser.add_argument("--agent", required=True, help="Agent ID (e.g., Agent-1)")
    parser.add_argument("--role", default="TASK_EXECUTOR", help="Assigned role")
    parser.add_argument(
        "--context-only", action="store_true", help="Only generate context, don't send message"
    )

    args = parser.parse_args()

    print(f"🤖 ENHANCED ONBOARDING: {args.agent}")
    print("=" * 60)

    # Initialize service
    service = EnhancedOnboardingService()

    if args.context_only:
        # Just build and save context
        builder = OnboardingContextBuilder(args.agent, args.role)
        context_file = builder.save_context_package()
        summary = builder.create_context_summary()

        print("\n📊 PROJECT CONTEXT LOADED:")
        print(summary)
        print(f"\n💾 Context saved to: {context_file}")
    else:
        # Full onboarding
        result = service.onboard_agent(args.agent, args.role)

        if result["success"]:
            print("\n✅ ONBOARDING COMPLETE:")
            print(f"  Agent: {result['agent_id']}")
            print(f"  Role: {result['assigned_role']}")
            print(f"  Context File: {result['context_file']}")
            print(f"  Message Delivered: {result['message_delivered']}")
            print(f"  Timestamp: {result['timestamp']}")

            # Load and display summary
            summary_file = Path(f"agent_workspaces/{args.agent}/onboarding_summary.txt")
            if summary_file.exists():
                print(f"\n{summary_file.read_text()}")
        else:
            print("❌ Onboarding failed")

    print("\n✅ Enhanced onboarding process complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
