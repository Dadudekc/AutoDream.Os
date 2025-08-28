#!/usr/bin/env python3
"""
Enterprise Integration Demo - Simple Version
"""

import json
import time

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime

# Import our services
from metrics_visualization import MetricsVisualizer
from discord_integration_service import DiscordIntegrationService
from beta_transformation_service import BetaTransformationService

def run_integration_demo():
    """Run a simple integration demo"""
    print("🚀 ENTERPRISE INTEGRATION DEMO")
    print("=" * 50)

    # Initialize services
    print("📊 Initializing services...")
    metrics = MetricsVisualizer()
    discord = DiscordIntegrationService()
    transformation = BetaTransformationService()

    # Phase 1: Agent Coordination
    print("\\n💬 Phase 1: Agent Coordination")
    discord.register_agent("agent-1", "Repository Scanner")
    discord.register_agent("agent-2", "Quality Analyzer")
    discord.send_message("system", "status", "All agents ready")

    # Phase 2: Metrics Collection
    print("\\n📈 Phase 2: Metrics Collection")
    metrics.record_metric("system.cpu", 45.2)
    metrics.record_agent_metric("agent-1", "scan_speed", 150)
    metrics.record_agent_metric("agent-2", "accuracy", 94.5)

    # Phase 3: Transformation
    print("\\n⚙️ Phase 3: Transformation")
    trans_id = transformation.create_transformation("Quality Enhancement", "Improve code quality")
    transformation.execute_transformation(trans_id)

    # Phase 4: Integration Report
    print("\\n�� Phase 4: Integration Report")
    metrics_summary = metrics.get_performance_summary()
    discord_status = discord.get_status()
    transformation_status = transformation.get_status()

    report = {
        "timestamp": datetime.now().isoformat(),
        "metrics": metrics_summary,
        "discord": discord_status,
        "transformation": transformation_status
    }

    print(f"🏥 Health Score: {metrics_summary[\"system_health_score\"]:.1f}/100")
    print(f"🤖 Agents: {discord_status[\"agents_registered\"]}")
    print(f"⚙️ Transformations: {transformation_status[\"transformations\"]}")

    # Save report
    with open("integration_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print("\\n✅ Integration demo completed!")
    print("📁 Report saved to: integration_report.json")

if __name__ == "__main__":
    run_integration_demo()
