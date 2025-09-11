#!/usr/bin/env python3
"""
🐝 SWARM Monitoring Dashboard

Simple dashboard to view automation status and recent reports.

Usage:
    python automation/dashboard/monitoring_dashboard.py
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List


class MonitoringDashboard:
    """Simple monitoring dashboard for automation status."""

    def __init__(self):
        self.root_path = Path.cwd()
        self.reports_dir = self.root_path / "automation_reports"
        self.logs_dir = self.root_path / "automation_logs"
        self.archive_dir = self.root_path / "automated_archives"

    def get_recent_reports(self) -> List[Path]:
        """Get recent automation reports."""
        if not self.reports_dir.exists():
            return []

        reports = list(self.reports_dir.glob("*.md"))
        # Sort by modification time, most recent first
        reports.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return reports[:10]

    def get_system_status(self) -> Dict:
        """Get current system status."""
        status = {
            "automation_active": False,
            "recent_reports": 0,
            "archive_count": 0,
            "total_archived_size": 0,
            "last_maintenance": None
        }

        # Check for recent reports
        if self.reports_dir.exists():
            reports = list(self.reports_dir.glob("*maintenance_report*.md"))
            status["recent_reports"] = len(reports)

            if reports:
                latest_report = max(reports, key=lambda x: x.stat().st_mtime)
                status["last_maintenance"] = datetime.fromtimestamp(
                    latest_report.stat().st_mtime
                ).strftime("%Y-%m-%d %H:%M:%S")

        # Check archive status
        if self.archive_dir.exists():
            archives = list(self.archive_dir.rglob("*"))
            status["archive_count"] = len(archives)

            # Calculate total archived size
            total_size = 0
            for archive in archives:
                if archive.is_file():
                    total_size += archive.stat().st_size
            status["total_archived_size"] = total_size

        # Check if automation is active (has recent logs)
        if self.logs_dir.exists():
            recent_logs = []
            cutoff = datetime.now() - timedelta(hours=24)

            for log_file in self.logs_dir.glob("*.log"):
                if datetime.fromtimestamp(log_file.stat().st_mtime) > cutoff:
                    recent_logs.append(log_file)

            status["automation_active"] = len(recent_logs) > 0

        return status

    def display_dashboard(self):
        """Display the monitoring dashboard."""
        status = self.get_system_status()
        recent_reports = self.get_recent_reports()

        print("🐝 SWARM MONITORING DASHBOARD")
        print("=" * 50)
        print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # System Status
        print("📊 SYSTEM STATUS")
        print("-" * 20)
        automation_status = "✅ ACTIVE" if status["automation_active"] else "❌ INACTIVE"
        print(f"Automation: {automation_status}")
        print(f"Recent Reports: {status['recent_reports']}")
        print(f"Archive Count: {status['archive_count']}")
        if status["total_archived_size"] > 0:
            size_mb = status["total_archived_size"] / (1024 * 1024)
            print(f"Archived Size: {size_mb:.2f} MB")
        if status["last_maintenance"]:
            print(f"Last Maintenance: {status['last_maintenance']}")
        print()

        # Recent Reports
        if recent_reports:
            print("📋 RECENT REPORTS")
            print("-" * 20)
            for i, report in enumerate(recent_reports[:5], 1):
                report_date = datetime.fromtimestamp(report.stat().st_mtime)
                print(f"{i}. {report.name}")
                print(f"   {report_date.strftime('%Y-%m-%d %H:%M:%S')}")
            print()

        # Quick Actions
        print("⚡ QUICK ACTIONS")
        print("-" * 20)
        print("1. Run maintenance cycle")
        print("2. Check file sizes")
        print("3. Run archiving")
        print("4. View latest report")
        print("5. Exit")
        print()

        while True:
            try:
                choice = input("Choose action (1-5): ").strip()

                if choice == "1":
                    print("Running maintenance cycle...")
                    os.system("python automation/swarm_maintenance_orchestrator.py --run-once")
                elif choice == "2":
                    print("Checking file sizes...")
                    os.system("python automation/file_size_monitor.py")
                elif choice == "3":
                    print("Running archiving...")
                    os.system("python automation/auto_archiver.py")
                elif choice == "4":
                    if recent_reports:
                        print(f"Opening latest report: {recent_reports[0]}")
                        if sys.platform == "win32":
                            os.startfile(recent_reports[0])
                        else:
                            os.system(f"open {recent_reports[0]}")
                    else:
                        print("No recent reports found")
                elif choice == "5":
                    print("🐝 Goodbye!")
                    break
                else:
                    print("Invalid choice. Please select 1-5.")

                print()
                input("Press Enter to continue...")

            except KeyboardInterrupt:
                print("
🐝 Goodbye!")
                break

def main():
    """Main entry point."""
    dashboard = MonitoringDashboard()
    dashboard.display_dashboard()

if __name__ == "__main__":
    main()
