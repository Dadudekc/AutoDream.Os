#!/usr/bin/env python3
"""
🐝 SWARM MONITORING ACTIVATION SCRIPT
Agent-8 Operations & Support Specialist

Activates comprehensive monitoring and alerting for the SWARM messaging
system restoration mission. This script initializes the unified monitoring
coordinator and provides real-time status updates.
"""

import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.unified_monitoring_coordinator import get_monitoring_coordinator


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('swarm_monitoring.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )


def create_status_report(coordinator):
    """Create a comprehensive status report."""
    report = coordinator.get_monitoring_report()

    # Save detailed report
    report_file = Path("swarm_monitoring_report.json")
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)

    # Create human-readable summary
    summary = f"""
🐝 **SWARM MONITORING STATUS REPORT**
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 **SYSTEM HEALTH STATUS:**
• Messaging System: {report['monitoring_status']['messaging_system'].upper()}
• PyAutoGUI Integration: {report['monitoring_status']['pyautogui_integration'].upper()}
• Inbox System: {report['monitoring_status']['inbox_system'].upper()}
• Agent Coordination: {report['monitoring_status']['agent_coordination'].upper()}
• Coordinate System: {report['monitoring_status']['coordinate_system'].upper()}
• Message Queue: {report['monitoring_status']['message_queue'].upper()}

🚨 **ACTIVE ALERTS: {len(report['active_alerts'])}**
"""

    if report['active_alerts']:
        for alert in report['active_alerts']:
            summary += f"• [{alert['level'].upper()}] {alert['component']}: {alert['message']}\n"
    else:
        summary += "• No active alerts - All systems operational ✅\n"

    summary += ".1f"".1f"f"""
⚙️ **ALERT THRESHOLDS:**
• Response Time Max: {report['alert_thresholds']['response_time_max']}s
• Message Delivery Rate Min: {report['alert_thresholds']['message_delivery_rate_min']}%
• System Uptime Min: {report['alert_thresholds']['system_uptime_min']}%
• Queue Size Max: {report['alert_thresholds']['queue_size_max']} messages

📈 **HISTORICAL DATA:**
• Total Alerts: {report['alert_history_count']}
• Last Updated: {report['monitoring_status']['last_updated']}
"""

    # Save summary report
    summary_file = Path("swarm_monitoring_summary.md")
    with open(summary_file, 'w') as f:
        f.write(summary)

    return summary


def main():
    """Main monitoring activation function."""
    print("🐝 **SWARM MONITORING ACTIVATION**")
    print("Agent-8 Operations & Support Specialist")
    print("=" * 50)

    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        # Initialize monitoring coordinator
        logger.info("Initializing unified monitoring coordinator...")
        coordinator = get_monitoring_coordinator()

        # Start monitoring
        logger.info("Starting monitoring system...")
        coordinator.start_monitoring(interval_seconds=30)

        print("✅ Monitoring system activated successfully!")
        print("📊 Monitoring all SWARM components every 30 seconds")
        print("📋 Status reports will be generated automatically")
        print("\n" + "=" * 50)

        # Run for 2 minutes (4 monitoring cycles) to demonstrate
        start_time = time.time()
        cycle_count = 0

        while time.time() - start_time < 120:  # 2 minutes
            time.sleep(30)  # Wait for monitoring cycle
            cycle_count += 1

            # Generate status report
            summary = create_status_report(coordinator)
            print(f"\n📊 **MONITORING CYCLE {cycle_count} COMPLETE**")
            print("Status report generated successfully!")

            # Show brief status
            report = coordinator.get_monitoring_report()
            active_alerts = len(report['active_alerts'])
            status_emoji = "✅" if active_alerts == 0 else "⚠️"
            print(f"{status_emoji} Active Alerts: {active_alerts}")

        # Final report
        print("\n" + "=" * 50)
        print("🏁 **MONITORING DEMONSTRATION COMPLETE**")
        print("📋 Final status report generated")
        print("📊 Check swarm_monitoring_report.json for detailed data")
        print("📝 Check swarm_monitoring_summary.md for executive summary")

        # Stop monitoring
        coordinator.stop_monitoring()

    except Exception as e:
        logger.error(f"Monitoring activation failed: {e}")
        print(f"❌ Monitoring activation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
