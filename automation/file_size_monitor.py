#!/usr/bin/env python3
"""
🐝 SWARM File Size Monitor

Monitors file and directory sizes against configured limits.
Provides alerts and recommendations for size management.

Features:
- Real-time size monitoring
- Configurable thresholds and alerts
- Size trend analysis
- Automated recommendations
- Integration with maintenance orchestrator

Author: Agent-7 (Web Development Specialist)
Position: Monitor 2 (920, 851)
Created: 2025-09-11
"""

import json
import logging
from collections import defaultdict
from datetime import datetime
from pathlib import Path


class FileSizeMonitor:
    """Advanced file size monitoring and alerting system."""

    def __init__(self, config_path: str = "automation/maintenance_config.json"):
        self.config_path = Path(config_path)
        self.root_path = Path.cwd()
        self.history_file = Path("automation/size_history.json")
        self.alerts_log = Path("automation/size_alerts.log")

        # Load configuration
        self.config = self._load_config()

        # Setup logging
        self._setup_logging()

        # Load size history
        self.size_history = self._load_size_history()

    def _load_config(self) -> dict:
        """Load configuration from file."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                return json.load(f)
        return {}

    def _setup_logging(self):
        """Setup logging for size monitoring."""
        logging.basicConfig(
            filename=self.alerts_log,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def _load_size_history(self) -> dict:
        """Load historical size data."""
        if self.history_file.exists():
            try:
                with open(self.history_file) as f:
                    return json.load(f)
            except Exception:
                pass
        return {"directories": {}, "files": {}}

    def _save_size_history(self):
        """Save current size data to history."""
        with open(self.history_file, "w") as f:
            json.dump(self.size_history, f, indent=2)

    def scan_directory_sizes(self) -> dict[str, dict]:
        """Scan and calculate directory sizes."""
        self.logger.info("Scanning directory sizes...")

        dir_sizes = {}
        exclusions = self.config.get("exclusions", {}).get("skip_directories", [])

        for dir_path in self.root_path.rglob("*"):
            if dir_path.is_dir():
                # Skip excluded directories
                if any(skip in str(dir_path) for skip in exclusions):
                    continue

                try:
                    total_size = sum(
                        f.stat().st_size
                        for f in dir_path.rglob("*")
                        if f.is_file() and not any(skip in str(f) for skip in exclusions)
                    )

                    dir_sizes[str(dir_path.relative_to(self.root_path))] = {
                        "size_bytes": total_size,
                        "size_mb": round(total_size / (1024 * 1024), 2),
                        "file_count": len(list(dir_path.rglob("*"))),
                        "last_modified": datetime.fromtimestamp(
                            dir_path.stat().st_mtime
                        ).isoformat(),
                    }

                except Exception as e:
                    self.logger.error(f"Error scanning directory {dir_path}: {e}")

        return dir_sizes

    def scan_file_sizes(self) -> dict[str, dict]:
        """Scan individual file sizes."""
        self.logger.info("Scanning file sizes...")

        file_sizes = {}
        size_limits = self.config.get("file_size_limits", {})
        max_file_size = size_limits.get("max_file_size_mb", 10) * 1024 * 1024
        exclusions = self.config.get("exclusions", {}).get("skip_files", [])

        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                # Skip excluded files
                if any(skip in str(file_path.name) for skip in exclusions):
                    continue

                try:
                    size_bytes = file_path.stat().st_size

                    if size_bytes > max_file_size:
                        file_sizes[str(file_path.relative_to(self.root_path))] = {
                            "size_bytes": size_bytes,
                            "size_mb": round(size_bytes / (1024 * 1024), 2),
                            "last_modified": datetime.fromtimestamp(
                                file_path.stat().st_mtime
                            ).isoformat(),
                            "extension": file_path.suffix,
                        }

                except Exception as e:
                    self.logger.error(f"Error scanning file {file_path}: {e}")

        return file_sizes

    def analyze_size_trends(self, current_sizes: dict[str, dict]) -> dict[str, list]:
        """Analyze size trends over time."""
        trends = {"growing": [], "shrinking": [], "stable": []}

        for path, current_data in current_sizes.items():
            if path in self.size_history.get("directories", {}):
                previous_data = self.size_history["directories"][path]
                current_size = current_data["size_bytes"]
                previous_size = previous_data["size_bytes"]

                change_percent = (
                    ((current_size - previous_size) / previous_size) * 100
                    if previous_size > 0
                    else 0
                )

                if change_percent > 10:
                    trends["growing"].append(
                        {
                            "path": path,
                            "change_percent": round(change_percent, 2),
                            "current_mb": current_data["size_mb"],
                            "previous_mb": round(previous_size / (1024 * 1024), 2),
                        }
                    )
                elif change_percent < -10:
                    trends["shrinking"].append(
                        {
                            "path": path,
                            "change_percent": round(change_percent, 2),
                            "current_mb": current_data["size_mb"],
                            "previous_mb": round(previous_size / (1024 * 1024), 2),
                        }
                    )
                else:
                    trends["stable"].append(
                        {"path": path, "change_percent": round(change_percent, 2)}
                    )

        return trends

    def generate_alerts(
        self, dir_sizes: dict[str, dict], file_sizes: dict[str, dict], trends: dict[str, list]
    ) -> list[dict]:
        """Generate alerts based on size limits and trends."""
        alerts = []
        size_limits = self.config.get("file_size_limits", {})

        # Directory size alerts
        max_dir_size = size_limits.get("max_directory_size_mb", 100) * 1024 * 1024
        alert_threshold = size_limits.get("alert_threshold_percent", 80) / 100
        critical_threshold = size_limits.get("critical_threshold_percent", 95) / 100

        for path, data in dir_sizes.items():
            size_bytes = data["size_bytes"]

            if size_bytes > max_dir_size:
                alerts.append(
                    {
                        "type": "directory_critical",
                        "severity": "CRITICAL",
                        "path": path,
                        "size_mb": data["size_mb"],
                        "limit_mb": size_limits.get("max_directory_size_mb", 100),
                        "recommendation": "Immediate cleanup or archiving required",
                    }
                )
            elif size_bytes > (max_dir_size * critical_threshold):
                alerts.append(
                    {
                        "type": "directory_warning",
                        "severity": "WARNING",
                        "path": path,
                        "size_mb": data["size_mb"],
                        "limit_mb": size_limits.get("max_directory_size_mb", 100),
                        "recommendation": "Monitor closely, plan cleanup",
                    }
                )
            elif size_bytes > (max_dir_size * alert_threshold):
                alerts.append(
                    {
                        "type": "directory_monitor",
                        "severity": "INFO",
                        "path": path,
                        "size_mb": data["size_mb"],
                        "limit_mb": size_limits.get("max_directory_size_mb", 100),
                        "recommendation": "Approaching limit, consider optimization",
                    }
                )

        # File size alerts
        for path, data in file_sizes.items():
            alerts.append(
                {
                    "type": "file_oversized",
                    "severity": "WARNING",
                    "path": path,
                    "size_mb": data["size_mb"],
                    "limit_mb": size_limits.get("max_file_size_mb", 10),
                    "recommendation": "Consider splitting or archiving this file",
                }
            )

        # Trend alerts
        for item in trends["growing"]:
            if item["change_percent"] > 50:
                alerts.append(
                    {
                        "type": "growth_alert",
                        "severity": "WARNING",
                        "path": item["path"],
                        "change_percent": item["change_percent"],
                        "recommendation": "Rapid growth detected, investigate usage",
                    }
                )

        return alerts

    def generate_recommendations(self, alerts: list[dict]) -> list[dict]:
        """Generate specific recommendations based on alerts."""
        recommendations = []

        alert_counts = defaultdict(int)
        for alert in alerts:
            alert_counts[alert["type"]] += 1

        # Directory recommendations
        if alert_counts["directory_critical"] > 0:
            recommendations.append(
                {
                    "priority": "HIGH",
                    "action": "Immediate Cleanup",
                    "description": f"Clean up {alert_counts['directory_critical']} directories exceeding size limits",
                    "commands": [
                        "python automation/swarm_maintenance_orchestrator.py --run-once",
                        "Review and archive old files in oversized directories",
                    ],
                }
            )

        if alert_counts["directory_warning"] > 0:
            recommendations.append(
                {
                    "priority": "MEDIUM",
                    "action": "Monitor Growth",
                    "description": f"Monitor {alert_counts['directory_warning']} directories approaching limits",
                    "commands": [
                        "python automation/file_size_monitor.py",
                        "Set up regular size monitoring alerts",
                    ],
                }
            )

        # File recommendations
        if alert_counts["file_oversized"] > 0:
            recommendations.append(
                {
                    "priority": "MEDIUM",
                    "action": "File Optimization",
                    "description": f"Optimize {alert_counts['file_oversized']} oversized files",
                    "commands": [
                        "Consider splitting large files",
                        "Archive old file versions",
                        "Implement file compression where appropriate",
                    ],
                }
            )

        # Growth recommendations
        if alert_counts["growth_alert"] > 0:
            recommendations.append(
                {
                    "priority": "HIGH",
                    "action": "Investigate Growth",
                    "description": f"Investigate {alert_counts['growth_alert']} rapidly growing directories",
                    "commands": [
                        "Analyze recent file additions",
                        "Review usage patterns",
                        "Implement size quotas if needed",
                    ],
                }
            )

        return recommendations

    def generate_report(
        self,
        dir_sizes: dict[str, dict],
        file_sizes: dict[str, dict],
        alerts: list[dict],
        trends: dict[str, list],
        recommendations: list[dict],
    ) -> Path:
        """Generate comprehensive size monitoring report."""
        reports_dir = Path("automation_reports")
        reports_dir.mkdir(exist_ok=True)

        report_path = (
            reports_dir / f"size_monitor_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        )

        content = [
            "# 🐝 SWARM File Size Monitor Report\n\n",
            f"**Report Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            "**Agent:** Agent-7 (Web Development Specialist)\n",
            "**Position:** Monitor 2 (920, 851)\n\n",
            "---\n\n",
        ]

        # Summary
        content.append("## 📊 Summary\n\n")
        content.append(f"- **Directories Scanned:** {len(dir_sizes)}\n")
        content.append(f"- **Oversized Files:** {len(file_sizes)}\n")
        content.append(f"- **Active Alerts:** {len(alerts)}\n")
        content.append(f"- **Growing Directories:** {len(trends['growing'])}\n\n")

        # Top 10 largest directories
        content.append("## 📁 Largest Directories\n\n")
        sorted_dirs = sorted(dir_sizes.items(), key=lambda x: x[1]["size_bytes"], reverse=True)[:10]

        content.append("| Directory | Size (MB) | Files | Last Modified |\n")
        content.append("|-----------|-----------|-------|---------------|\n")

        for path, data in sorted_dirs:
            content.append(
                f"| {path} | {data['size_mb']} | {data['file_count']} | {data['last_modified'][:10]} |\n"
            )

        content.append("\n")

        # Alerts
        if alerts:
            content.append("## 🚨 Active Alerts\n\n")
            for alert in alerts:
                severity_icon = (
                    "🔴"
                    if alert["severity"] == "CRITICAL"
                    else "🟡"
                    if alert["severity"] == "WARNING"
                    else "ℹ️"
                )
                content.append(f"### {severity_icon} {alert['type'].replace('_', ' ').title()}\n")
                content.append(f"- **Path:** {alert['path']}\n")
                content.append(f"- **Size:** {alert.get('size_mb', 'N/A')} MB\n")
                content.append(f"- **Recommendation:** {alert['recommendation']}\n\n")

        # Trends
        content.append("## 📈 Size Trends\n\n")

        for trend_type, items in trends.items():
            if items:
                content.append(f"### {trend_type.title()} Directories ({len(items)})\n\n")
                for item in items[:5]:  # Show top 5
                    content.append(
                        f"- **{item['path']}**: {item.get('change_percent', 0)}% change "
                    )
                    if "current_mb" in item:
                        content.append(f"({item['current_mb']} MB)\n")
                    else:
                        content.append("\n")
                content.append("\n")

        # Recommendations
        if recommendations:
            content.append("## 💡 Recommendations\n\n")
            for rec in recommendations:
                priority_icon = (
                    "🔴"
                    if rec["priority"] == "HIGH"
                    else "🟡"
                    if rec["priority"] == "MEDIUM"
                    else "🟢"
                )
                content.append(f"### {priority_icon} {rec['action']} ({rec['priority']})\n")
                content.append(f"{rec['description']}\n\n")
                if "commands" in rec:
                    content.append("**Commands:**\n")
                    for cmd in rec["commands"]:
                        content.append(f"- `{cmd}`\n")
                content.append("\n")

        # Configuration
        content.append("## ⚙️ Configuration\n\n")
        size_limits = self.config.get("file_size_limits", {})
        content.append(
            f"- **Max Directory Size:** {size_limits.get('max_directory_size_mb', 100)} MB\n"
        )
        content.append(f"- **Max File Size:** {size_limits.get('max_file_size_mb', 10)} MB\n")
        content.append(
            f"- **Alert Threshold:** {size_limits.get('alert_threshold_percent', 80)}%\n"
        )
        content.append(
            f"- **Critical Threshold:** {size_limits.get('critical_threshold_percent', 95)}%\n\n"
        )

        content.append("**🐝 WE ARE SWARM - SIZE MONITORING COMPLETE**\n")

        with open(report_path, "w", encoding="utf-8") as f:
            f.writelines(content)

        return report_path

    def run_monitoring_cycle(self) -> dict[str, any]:
        """Run complete size monitoring cycle."""
        self.logger.info("Starting size monitoring cycle...")

        # Scan sizes
        dir_sizes = self.scan_directory_sizes()
        file_sizes = self.scan_file_sizes()

        # Analyze trends
        trends = self.analyze_size_trends(dir_sizes)

        # Generate alerts
        alerts = self.generate_alerts(dir_sizes, file_sizes, trends)

        # Generate recommendations
        recommendations = self.generate_recommendations(alerts)

        # Generate report
        report_path = self.generate_report(dir_sizes, file_sizes, alerts, trends, recommendations)

        # Update history
        self.size_history = {
            "directories": dir_sizes,
            "files": file_sizes,
            "last_update": datetime.now().isoformat(),
        }
        self._save_size_history()

        results = {
            "directories_scanned": len(dir_sizes),
            "oversized_files": len(file_sizes),
            "alerts": alerts,
            "trends": trends,
            "recommendations": recommendations,
            "report_path": report_path,
            "timestamp": datetime.now().isoformat(),
        }

        self.logger.info(f"Size monitoring cycle complete. Report: {report_path}")
        return results


def main():
    """Main entry point for file size monitor."""
    import argparse

    parser = argparse.ArgumentParser(description="SWARM File Size Monitor")
    parser.add_argument(
        "--config", default="automation/maintenance_config.json", help="Path to configuration file"
    )
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    parser.add_argument("--alerts-only", action="store_true", help="Show alerts only")

    args = parser.parse_args()

    monitor = FileSizeMonitor(args.config)
    results = monitor.run_monitoring_cycle()

    if args.alerts_only:
        if results["alerts"]:
            print("\n🐝 SIZE ALERTS:")
            for alert in results["alerts"]:
                print(f"  {alert['severity']}: {alert['path']} ({alert.get('size_mb', 'N/A')} MB)")
        else:
            print("✅ No size alerts")
    else:
        print(f"📊 Size monitoring complete. Report: {results['report_path']}")
        print(f"📁 Directories scanned: {results['directories_scanned']}")
        print(f"🚨 Active alerts: {len(results['alerts'])}")
        print(f"📈 Growing directories: {len(results['trends']['growing'])}")


if __name__ == "__main__":
    main()
