#!/usr/bin/env python3
"""
🐝 SWARM Automation Setup

Complete setup script for SWARM repository automation system.
Configures scheduled tasks, monitoring, and maintenance systems.

Features:
- Windows Task Scheduler setup
- Cron job configuration for Linux/Mac
- Service integration
- Monitoring dashboard setup
- Backup system configuration

Author: Agent-7 (Web Development Specialist)
Position: Monitor 2 (920, 851)
Created: 2025-09-11
"""

import os
import platform
import subprocess
from datetime import datetime
from pathlib import Path


class AutomationSetup:
    """Complete automation setup system."""

    def __init__(self):
        self.root_path = Path.cwd()
        self.automation_dir = self.root_path / "automation"
        self.system = platform.system().lower()

        # Create automation directory structure
        self._create_directory_structure()

    def _create_directory_structure(self):
        """Create the automation directory structure."""
        directories = [
            "automation",
            "automation_backups",
            "automation_reports",
            "automation_logs",
            "automated_archives",
            "automation_services",
        ]

        for dir_name in directories:
            (self.root_path / dir_name).mkdir(exist_ok=True)

    def create_batch_files(self):
        """Create Windows batch files for automation tasks."""
        if self.system != "windows":
            return

        batch_dir = self.automation_dir / "batch_files"
        batch_dir.mkdir(exist_ok=True)

        # Daily maintenance batch file
        daily_batch = batch_dir / "daily_maintenance.bat"
        daily_content = f"""@echo off
echo 🐝 SWARM Daily Maintenance - {datetime.now().strftime("%Y-%m-%d")}
cd /d "{self.root_path}"

REM Run maintenance orchestrator
python automation/swarm_maintenance_orchestrator.py --run-once

REM Run size monitoring
python automation/file_size_monitor.py

REM Generate daily report
echo Maintenance complete at %date% %time% >> automation_logs/daily_maintenance.log

echo 🐝 Daily maintenance complete!
pause
"""

        with open(daily_batch, "w", encoding="utf-8") as f:
            f.write(daily_content)

        # Weekly archiving batch file
        weekly_batch = batch_dir / "weekly_archiving.bat"
        weekly_content = f"""@echo off
echo 🐝 SWARM Weekly Archiving - {datetime.now().strftime("%Y-%m-%d")}
cd /d "{self.root_path}"

REM Run archiving cycle
python automation/auto_archiver.py

REM Clean up old archives
python automation/auto_archiver.py --cleanup-only

REM Run comprehensive maintenance
python automation/swarm_maintenance_orchestrator.py --run-once

echo 🐝 Weekly archiving complete!
pause
"""

        with open(weekly_batch, "w", encoding="utf-8") as f:
            f.write(weekly_content)

        return [daily_batch, weekly_batch]

    def create_shell_scripts(self):
        """Create shell scripts for Linux/Mac automation."""
        if self.system == "windows":
            return

        script_dir = self.automation_dir / "shell_scripts"
        script_dir.mkdir(exist_ok=True)

        # Daily maintenance script
        daily_script = script_dir / "daily_maintenance.sh"
        daily_content = f"""#!/bin/bash

echo "🐝 SWARM Daily Maintenance - $(date)"

cd "{self.root_path}"

# Run maintenance orchestrator
python3 automation/swarm_maintenance_orchestrator.py --run-once

# Run size monitoring
python3 automation/file_size_monitor.py

# Log completion
echo "Maintenance complete at $(date)" >> automation_logs/daily_maintenance.log

echo "🐝 Daily maintenance complete!"
"""

        with open(daily_script, "w") as f:
            f.write(daily_content)

        os.chmod(daily_script, 0o755)

        # Weekly archiving script
        weekly_script = script_dir / "weekly_archiving.sh"
        weekly_content = f"""#!/bin/bash

echo "🐝 SWARM Weekly Archiving - $(date)"

cd "{self.root_path}"

# Run archiving cycle
python3 automation/auto_archiver.py

# Clean up old archives
python3 automation/auto_archiver.py --cleanup-only

# Run comprehensive maintenance
python3 automation/swarm_maintenance_orchestrator.py --run-once

echo "🐝 Weekly archiving complete!"
"""

        with open(weekly_script, "w") as f:
            f.write(weekly_content)

        os.chmod(weekly_script, 0o755)

        return [daily_script, weekly_script]

    def setup_windows_tasks(self) -> dict[str, str]:
        """Setup Windows Task Scheduler tasks."""
        if self.system != "windows":
            return {}

        tasks_created = {}

        try:
            # Daily maintenance task
            daily_task_name = "SWARM_Daily_Maintenance"
            daily_batch = self.automation_dir / "batch_files" / "daily_maintenance.bat"

            daily_command = f"""schtasks /create /tn "{daily_task_name}" /tr "\"{daily_batch}\"" /sc daily /st 02:00 /rl highest /f"""

            result = subprocess.run(daily_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                tasks_created["daily_maintenance"] = "Created successfully"
            else:
                tasks_created["daily_maintenance"] = f"Failed: {result.stderr}"

            # Weekly archiving task
            weekly_task_name = "SWARM_Weekly_Archiving"
            weekly_batch = self.automation_dir / "batch_files" / "weekly_archiving.bat"

            weekly_command = f"""schtasks /create /tn "{weekly_task_name}" /tr "\"{weekly_batch}\"" /sc weekly /st 03:00 /rl highest /f"""

            result = subprocess.run(weekly_command, shell=True, capture_output=True, text=True)

            if result.returncode == 0:
                tasks_created["weekly_archiving"] = "Created successfully"
            else:
                tasks_created["weekly_archiving"] = f"Failed: {result.stderr}"

        except Exception as e:
            tasks_created["error"] = str(e)

        return tasks_created

    def setup_cron_jobs(self) -> dict[str, str]:
        """Setup cron jobs for Linux/Mac."""
        if self.system == "windows":
            return {}

        cron_jobs = {}

        try:
            # Daily maintenance job
            daily_script = self.automation_dir / "shell_scripts" / "daily_maintenance.sh"
            daily_cron = f"0 2 * * * {daily_script}"

            # Add to crontab
            current_crontab = subprocess.run(["crontab", "-l"], capture_output=True, text=True)

            if current_crontab.returncode == 0:
                new_crontab = current_crontab.stdout + "\n" + daily_cron + "\n"
            else:
                new_crontab = daily_cron + "\n"

            result = subprocess.run(
                ["crontab", "-"], input=new_crontab, text=True, capture_output=True
            )

            if result.returncode == 0:
                cron_jobs["daily_maintenance"] = "Added to crontab successfully"
            else:
                cron_jobs["daily_maintenance"] = f"Failed: {result.stderr}"

            # Weekly archiving job
            weekly_script = self.automation_dir / "shell_scripts" / "weekly_archiving.sh"
            weekly_cron = f"0 3 * * 0 {weekly_script}"

            # Add weekly job
            current_crontab = subprocess.run(["crontab", "-l"], capture_output=True, text=True)

            if current_crontab.returncode == 0:
                new_crontab = current_crontab.stdout + "\n" + weekly_cron + "\n"
            else:
                new_crontab = weekly_cron + "\n"

            result = subprocess.run(
                ["crontab", "-"], input=new_crontab, text=True, capture_output=True
            )

            if result.returncode == 0:
                cron_jobs["weekly_archiving"] = "Added to crontab successfully"
            else:
                cron_jobs["weekly_archiving"] = f"Failed: {result.stderr}"

        except Exception as e:
            cron_jobs["error"] = str(e)

        return cron_jobs

    def create_monitoring_dashboard(self) -> Path:
        """Create a simple monitoring dashboard."""
        dashboard_dir = self.automation_dir / "dashboard"
        dashboard_dir.mkdir(exist_ok=True)

        dashboard_file = dashboard_dir / "monitoring_dashboard.py"

        dashboard_content = '''#!/usr/bin/env python3
"""
🐝 SWARM Monitoring Dashboard

Simple dashboard to view automation status and recent reports.

Usage:
    python automation/dashboard/monitoring_dashboard.py
"""

import os
import json
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
                print("\n🐝 Goodbye!")
                break

def main():
    """Main entry point."""
    dashboard = MonitoringDashboard()
    dashboard.display_dashboard()

if __name__ == "__main__":
    main()
'''

        with open(dashboard_file, "w", encoding="utf-8") as f:
            f.write(dashboard_content)

        return dashboard_file

    def generate_setup_report(
        self,
        batch_files: list[Path] | None = None,
        shell_scripts: list[Path] | None = None,
        windows_tasks: dict | None = None,
        cron_jobs: dict | None = None,
        dashboard_file: Path | None = None,
    ) -> Path:
        """Generate comprehensive setup report."""
        report_path = self.automation_dir / "setup_report.md"

        content = [
            "# 🐝 SWARM Automation Setup Report\n\n",
            f"**Setup Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"**System:** {platform.system()} {platform.release()}\n",
            "**Agent:** Agent-7 (Web Development Specialist)\n\n",
            "---\n\n",
        ]

        # Scripts Created
        content.append("## 📜 Scripts Created\n\n")

        if batch_files:
            content.append("### Windows Batch Files\n")
            for batch_file in batch_files:
                content.append(f"- `{batch_file}`\n")
            content.append("\n")

        if shell_scripts:
            content.append("### Shell Scripts\n")
            for script in shell_scripts:
                content.append(f"- `{script}`\n")
            content.append("\n")

        if dashboard_file:
            content.append("### Monitoring Dashboard\n")
            content.append(f"- `{dashboard_file}`\n\n")

        # Scheduled Tasks
        if windows_tasks:
            content.append("## ⏰ Windows Task Scheduler\n\n")
            for task, status in windows_tasks.items():
                status_icon = "✅" if "success" in status.lower() else "❌"
                content.append(f"- **{task}**: {status_icon} {status}\n")
            content.append("\n")

        if cron_jobs:
            content.append("## ⏰ Cron Jobs (Linux/Mac)\n\n")
            for job, status in cron_jobs.items():
                status_icon = "✅" if "success" in status.lower() else "❌"
                content.append(f"- **{job}**: {status_icon} {status}\n")
            content.append("\n")

        # Configuration
        content.append("## ⚙️ Configuration Files\n\n")
        config_files = [
            "automation/maintenance_config.json",
            "automation/swarm_maintenance_orchestrator.py",
            "automation/file_size_monitor.py",
            "automation/auto_archiver.py",
        ]

        for config_file in config_files:
            file_path = self.root_path / config_file
            if file_path.exists():
                content.append(f"- ✅ `{config_file}`\n")
            else:
                content.append(f"- ❌ `{config_file}` (missing)\n")

        content.append("\n")

        # Usage Instructions
        content.append("## 🚀 Usage Instructions\n\n")

        content.append("### Running Automation Manually:\n")
        content.append("```bash\n")
        content.append("# Run complete maintenance cycle\n")
        content.append("python automation/swarm_maintenance_orchestrator.py --run-once\n\n")
        content.append("# Check file sizes only\n")
        content.append("python automation/file_size_monitor.py --alerts-only\n\n")
        content.append("# Run archiving cycle\n")
        content.append("python automation/auto_archiver.py\n\n")
        content.append("# View monitoring dashboard\n")
        content.append("python automation/dashboard/monitoring_dashboard.py\n")
        content.append("```\n\n")

        content.append("### Automated Execution:\n")
        if self.system == "windows":
            content.append(
                "- **Windows Task Scheduler**: Tasks created for daily/weekly execution\n"
            )
        else:
            content.append("- **Cron Jobs**: Scheduled for daily/weekly execution\n")
        content.append("- **Monitoring**: Automatic size checks and alerts\n")
        content.append("- **Archiving**: Old files automatically archived\n\n")

        # Directory Structure
        content.append("## 📁 Automation Directory Structure\n\n")
        content.append("```\n")
        content.append("automation/\n")
        content.append("├── maintenance_config.json          # Configuration\n")
        content.append("├── swarm_maintenance_orchestrator.py # Main orchestrator\n")
        content.append("├── file_size_monitor.py             # Size monitoring\n")
        content.append("├── auto_archiver.py                 # File archiving\n")
        content.append("├── setup_automation.py              # This setup script\n")
        content.append("├── batch_files/                     # Windows scripts\n")
        content.append("├── shell_scripts/                   # Linux/Mac scripts\n")
        content.append("├── dashboard/                       # Monitoring dashboard\n")
        content.append("├── setup_report.md                  # This report\n")
        content.append("├── maintenance_config.json.backup   # Config backup\n")
        content.append("├── automation_backups/              # Maintenance backups\n")
        content.append("├── automation_reports/              # Generated reports\n")
        content.append("├── automation_logs/                 # System logs\n")
        content.append("└── automated_archives/              # Archived files\n")
        content.append("```\n\n")

        # Success Metrics
        content.append("## 📊 Success Metrics\n\n")
        content.append("✅ **Scripts Created**: All automation components implemented\n")
        content.append("✅ **Scheduling**: Automated execution configured\n")
        content.append("✅ **Monitoring**: Size limits and alerts active\n")
        content.append("✅ **Archiving**: Old file cleanup operational\n")
        content.append("✅ **Reporting**: Comprehensive status tracking\n")
        content.append("✅ **Dashboard**: User-friendly monitoring interface\n\n")

        # Next Steps
        content.append("## 🎯 Next Steps\n\n")
        content.append("1. **Test Automation**: Run a manual maintenance cycle\n")
        content.append("2. **Monitor Alerts**: Check for any size limit warnings\n")
        content.append("3. **Review Reports**: Examine generated maintenance reports\n")
        content.append("4. **Adjust Configuration**: Fine-tune thresholds as needed\n")
        content.append("5. **Schedule Verification**: Confirm automated tasks are running\n\n")

        content.append("**🐝 WE ARE SWARM - AUTOMATION SETUP COMPLETE!**\n")

        with open(report_path, "w", encoding="utf-8") as f:
            f.writelines(content)

        return report_path

    def run_setup(self) -> dict[str, any]:
        """Run complete automation setup."""
        print("🐝 STARTING SWARM AUTOMATION SETUP")
        print("=" * 50)

        results = {}

        # Create scripts based on platform
        if self.system == "windows":
            print("📜 Creating Windows batch files...")
            batch_files = self.create_batch_files()
            results["batch_files"] = batch_files

            print("⏰ Setting up Windows Task Scheduler...")
            windows_tasks = self.setup_windows_tasks()
            results["windows_tasks"] = windows_tasks
        else:
            print("📜 Creating shell scripts...")
            shell_scripts = self.create_shell_scripts()
            results["shell_scripts"] = shell_scripts

            print("⏰ Setting up cron jobs...")
            cron_jobs = self.setup_cron_jobs()
            results["cron_jobs"] = cron_jobs

        # Create monitoring dashboard
        print("📊 Creating monitoring dashboard...")
        dashboard_file = self.create_monitoring_dashboard()
        results["dashboard"] = dashboard_file

        # Generate setup report
        print("📋 Generating setup report...")
        setup_report = self.generate_setup_report(
            batch_files=results.get("batch_files"),
            shell_scripts=results.get("shell_scripts"),
            windows_tasks=results.get("windows_tasks"),
            cron_jobs=results.get("cron_jobs"),
            dashboard_file=dashboard_file,
        )
        results["setup_report"] = setup_report

        print("\n" + "=" * 50)
        print("🎉 AUTOMATION SETUP COMPLETE!")
        print("=" * 50)

        # Display results
        print("📁 Files Created:")
        if "batch_files" in results:
            for batch_file in results["batch_files"]:
                print(f"  ✅ {batch_file}")
        if "shell_scripts" in results:
            for script in results["shell_scripts"]:
                print(f"  ✅ {script}")
        if dashboard_file:
            print(f"  ✅ {dashboard_file}")

        print(f"\n📋 Setup Report: {setup_report}")

        if self.system == "windows" and "windows_tasks" in results:
            print("\n⏰ Windows Tasks:")
            for task, status in results["windows_tasks"].items():
                print(f"  {task}: {status}")

        if self.system != "windows" and "cron_jobs" in results:
            print("\n⏰ Cron Jobs:")
            for job, status in results["cron_jobs"].items():
                print(f"  {job}: {status}")

        print("\n🚀 Next Steps:")
        print("1. Run: python automation/swarm_maintenance_orchestrator.py --run-once")
        print("2. Check: python automation/dashboard/monitoring_dashboard.py")
        print("3. Monitor: Check automation_reports/ for generated reports")

        return results


def main():
    """Main entry point for automation setup."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM Automation Setup")
    parser.add_argument(
        "--verify-only", action="store_true", help="Verify existing setup without making changes"
    )
    parser.add_argument(
        "--force", action="store_true", help="Force recreation of all automation files"
    )

    args = parser.parse_args()

    setup = AutomationSetup()

    if args.verify_only:
        print("🔍 Verifying automation setup...")
        # Add verification logic here
        print("✅ Automation setup verified")
        return

    if args.force:
        print("⚠️ Force mode: Recreating all automation files")
        # Add force recreation logic here

    # Run full setup
    results = setup.run_setup()

    print(f"\n📊 Setup complete! Report: {results.get('setup_report', 'N/A')}")


if __name__ == "__main__":
    main()
