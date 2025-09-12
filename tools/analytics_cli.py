#!/usr/bin/env python3
"""
Advanced Analytics CLI Tool
============================

Command-line interface for the Advanced Analytics and Reporting System.
Provides tools for data collection, dashboard generation, report creation, and analytics insights.

Author: Agent-5 (Business Intelligence Specialist)
Usage: python tools/analytics_cli.py --dashboard overview
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.advanced_analytics_service import get_analytics_service


class AnalyticsCLI:
    """Command-line interface for advanced analytics system."""

    def __init__(self):
        self.analytics_service = get_analytics_service()
        self.analytics_service.start()

    def show_dashboard(self, dashboard_type: str = "overview") -> None:
        """Display dashboard data in terminal."""
        print(f"🐝 Advanced Analytics Dashboard - {dashboard_type.upper()}")
        print("=" * 60)

        try:
            data = self.analytics_service.get_dashboard_data(dashboard_type)

            if "error" in data:
                print(f"❌ Error: {data['error']}")
                return

            if dashboard_type == "overview":
                self._display_overview_dashboard(data)
            elif dashboard_type == "performance":
                self._display_performance_dashboard(data)
            elif dashboard_type == "usage":
                self._display_usage_dashboard(data)
            elif dashboard_type == "quality":
                self._display_quality_dashboard(data)
            else:
                print(f"❌ Unknown dashboard type: {dashboard_type}")

        except Exception as e:
            print(f"❌ Failed to load dashboard: {e}")

    def _display_overview_dashboard(self, data: Dict[str, Any]) -> None:
        """Display overview dashboard in terminal."""
        kpis = data.get("kpis", {})

        print("📊 Key Performance Indicators:"        print(".1f")
        print(".2f")
        print(".1f")
        print(f"   Active Agents: {kpis.get('active_agents', 'N/A')}")

        alerts = data.get("alerts", [])
        if alerts:
            print("\n🚨 Active Alerts:"            for alert in alerts:
                print(f"   {alert['level'].upper()}: {alert['message']}")

        insights = data.get("insights", [])
        if insights:
            print("\n💡 AI Insights:"            for insight in insights:
                print(f"   • {insight}")

    def _display_performance_dashboard(self, data: Dict[str, Any]) -> None:
        """Display performance dashboard in terminal."""
        metrics = data.get("metrics", {})

        print("⚡ Performance Metrics:"        print("   Response Times: Coming soon...")
        print("   Throughput: Coming soon...")
        print("   Resource Usage: Coming soon...")

        recommendations = data.get("recommendations", [])
        if recommendations:
            print("\n🎯 Performance Recommendations:"            for rec in recommendations:
                print(f"   • {rec}")

    def _display_usage_dashboard(self, data: Dict[str, Any]) -> None:
        """Display usage analytics dashboard in terminal."""
        usage_metrics = data.get("usage_metrics", {})
        rankings = data.get("agent_rankings", {})

        print("📈 Usage Analytics:"        print(f"   Total Activities (24h): {usage_metrics.get('total_system_activity', 'N/A')}")
        print(f"   Tasks Completed (24h): {usage_metrics.get('total_system_tasks', 'N/A')}")
        print(".2f")
        print(".1f")

        if "most_active_agents" in rankings:
            print("\n🏆 Most Active Agents:"            for agent in rankings["most_active_agents"][:3]:
                print(f"   {agent['agent']}: {agent['activities']} activities")

        if "most_efficient_agents" in rankings:
            print("\n⚡ Most Efficient Agents:"            for agent in rankings["most_efficient_agents"][:3]:
                print(".2f")

    def _display_quality_dashboard(self, data: Dict[str, Any]) -> None:
        """Display quality dashboard in terminal."""
        metrics = data.get("metrics", {})

        print("🔍 Code Quality Metrics:"        print("   Violation Trends: Coming soon...")
        print("   Compliance Progress: Coming soon...")

        alerts = data.get("alerts", [])
        if alerts:
            print("\n🚨 Quality Alerts:"            for alert in alerts:
                print(f"   {alert['level'].upper()}: {alert['message']}")

    def generate_report(self, report_type: str = "daily", output_file: Optional[str] = None) -> None:
        """Generate and display/save business intelligence report."""
        print(f"📈 Generating {report_type} business intelligence report...")
        print("-" * 60)

        try:
            report = self.analytics_service.generate_report(report_type)

            if "error" in report:
                print(f"❌ Error generating report: {report['error']}")
                return

            # Display report summary
            self._display_report_summary(report, report_type)

            # Save to file if requested
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                print(f"\n💾 Report saved to: {output_file}")

        except Exception as e:
            print(f"❌ Failed to generate report: {e}")

    def _display_report_summary(self, report: Dict[str, Any], report_type: str) -> None:
        """Display report summary in terminal."""
        print(f"📊 {report_type.title()} Business Intelligence Report")
        print(f"Generated: {report.get('generated_at', 'Unknown')}")
        print(f"Period: {report.get('period', 'Unknown')}")

        if "executive_summary" in report:
            summary = report["executive_summary"]
            print("\n📈 Executive Summary:"            print(".2f")
            print(".1f")
            print(f"   Tasks Completed: {summary.get('tasks_completed', 'N/A')}")

        if "key_insights" in report and report["key_insights"]:
            print("\n💡 Key Insights:"            for insight in report["key_insights"]:
                print(f"   • {insight}")

        if "recommendations" in report and report["recommendations"]:
            print("\n🎯 Strategic Recommendations:"            for rec in report["recommendations"]:
                print(f"   • {rec}")

    def show_usage_analytics(self, agent_id: Optional[str] = None, hours_back: int = 24) -> None:
        """Display usage analytics for agent or system."""
        print(f"📊 Usage Analytics {'for ' + agent_id if agent_id else '(System-wide)'}")
        print("-" * 60)

        try:
            data = self.analytics_service.get_usage_analytics(agent_id, hours_back)

            if agent_id:
                self._display_agent_usage_analytics(data, agent_id)
            else:
                self._display_system_usage_analytics(data)

        except Exception as e:
            print(f"❌ Failed to load usage analytics: {e}")

    def _display_agent_usage_analytics(self, data: Dict[str, Any], agent_id: str) -> None:
        """Display agent-specific usage analytics."""
        metrics = data.get("usage_metrics", {})

        print(f"🤖 Agent: {agent_id}")
        print(f"Analysis Period: {data.get('analysis_period_hours', 'N/A')} hours")
        print("
📈 Usage Metrics:"        print(f"   Total Activities: {metrics.get('total_activities', 'N/A')}")
        print(f"   Tasks Completed: {metrics.get('tasks_completed', 'N/A')}")
        print(".2f")
        print(".1f")

        patterns = data.get("patterns", {})
        if patterns.get("peak_usage_hours"):
            print(f"   Peak Hours: {', '.join(map(str, patterns['peak_usage_hours']))}")

        insights = data.get("insights", [])
        if insights:
            print("\n💡 Insights:"            for insight in insights:
                print(f"   • {insight}")

    def _display_system_usage_analytics(self, data: Dict[str, Any]) -> None:
        """Display system-wide usage analytics."""
        metrics = data.get("system_metrics", {})

        print("🌐 System-wide Analytics"        print(f"Analysis Period: {data.get('analysis_period_hours', 'N/A')} hours")
        print("
📊 System Metrics:"        print(f"   Total Agents: {metrics.get('total_agents', 'N/A')}")
        print(f"   Total Activities: {metrics.get('total_system_activity', 'N/A')}")
        print(f"   Total Tasks: {metrics.get('total_system_tasks', 'N/A')}")
        print(".2f")
        print(".1f")

        rankings = data.get("agent_rankings", {})

        if "most_active_agents" in rankings:
            print("\n🏆 Most Active Agents:"            for agent in rankings["most_active_agents"][:3]:
                print(f"   {agent['agent']}: {agent['activities']} activities")

        if "most_efficient_agents" in rankings:
            print("\n⚡ Most Efficient Agents:"            for agent in rankings["most_efficient_agents"][:3]:
                print(".2f")

        insights = data.get("system_insights", [])
        if insights:
            print("\n💡 System Insights:"            for insight in insights:
                print(f"   • {insight}")

    def collect_custom_metric(self, name: str, value: Any, tags: Optional[Dict[str, str]] = None) -> None:
        """Collect a custom metric."""
        try:
            self.analytics_service.collect_custom_metric(name, value, tags)
            print(f"✅ Collected custom metric: {name} = {value}")
            if tags:
                print(f"   Tags: {tags}")
        except Exception as e:
            print(f"❌ Failed to collect custom metric: {e}")

    def show_service_status(self) -> None:
        """Display analytics service status."""
        print("🔧 Advanced Analytics Service Status")
        print("-" * 40)

        try:
            status = self.analytics_service.get_service_status()

            print(f"Service Status: {'🟢 RUNNING' if status.get('service_status') == 'running' else '🔴 STOPPED'}")
            print(f"Metrics Collected: {status.get('metrics_collected', 'N/A')}")
            print(f"Active Metrics: {status.get('active_metrics', 'N/A')}")
            print(f"Uptime: {status.get('uptime', 'N/A')}")

            if status.get('last_collection'):
                print(f"Last Collection: {status['last_collection']}")

        except Exception as e:
            print(f"❌ Failed to get service status: {e}")

    def run_health_check(self) -> None:
        """Run comprehensive health check."""
        print("🏥 Analytics System Health Check")
        print("-" * 40)

        issues = []

        # Check service status
        try:
            status = self.analytics_service.get_service_status()
            if status.get('service_status') != 'running':
                issues.append("Analytics service is not running")
        except Exception as e:
            issues.append(f"Cannot access analytics service: {e}")

        # Check dashboard access
        try:
            dashboard_data = self.analytics_service.get_dashboard_data("overview")
            if "error" in dashboard_data:
                issues.append(f"Dashboard error: {dashboard_data['error']}")
        except Exception as e:
            issues.append(f"Cannot access dashboard: {e}")

        # Check metrics collection
        try:
            stats = self.analytics_service.get_metrics_stats("system.cpu_usage", 1)
            if "error" in stats:
                issues.append(f"Metrics collection error: {stats['error']}")
        except Exception as e:
            issues.append(f"Cannot access metrics: {e}")

        if issues:
            print("❌ Health Check Failed - Issues Found:")
            for issue in issues:
                print(f"   • {issue}")
        else:
            print("✅ Health Check Passed - All systems operational")

    def shutdown(self) -> None:
        """Shutdown the analytics service."""
        print("🛑 Shutting down analytics service...")
        self.analytics_service.stop()
        print("✅ Analytics service stopped")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced Analytics CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Show overview dashboard
  python tools/analytics_cli.py --dashboard overview

  # Generate daily business intelligence report
  python tools/analytics_cli.py --report daily

  # Show usage analytics for specific agent
  python tools/analytics_cli.py --usage --agent Agent-5

  # Collect custom metric
  python tools/analytics_cli.py --collect-metric response_time 150 --tags component=api

  # Check service health
  python tools/analytics_cli.py --health
        """
    )

    parser.add_argument(
        "--dashboard", "-d",
        choices=["overview", "performance", "usage", "quality"],
        help="Display specified dashboard"
    )

    parser.add_argument(
        "--report", "-r",
        choices=["daily", "weekly", "monthly"],
        help="Generate specified business intelligence report"
    )

    parser.add_argument(
        "--usage", "-u",
        action="store_true",
        help="Show usage analytics"
    )

    parser.add_argument(
        "--agent", "-a",
        help="Specific agent for usage analytics (requires --usage)"
    )

    parser.add_argument(
        "--collect-metric", "-c",
        nargs=2,
        metavar=("NAME", "VALUE"),
        help="Collect custom metric (name value)"
    )

    parser.add_argument(
        "--tags",
        help="Tags for custom metric as JSON string (requires --collect-metric)"
    )

    parser.add_argument(
        "--status", "-s",
        action="store_true",
        help="Show analytics service status"
    )

    parser.add_argument(
        "--health",
        action="store_true",
        help="Run comprehensive health check"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file for reports"
    )

    parser.add_argument(
        "--hours-back",
        type=int,
        default=24,
        help="Hours of data to analyze (default: 24)"
    )

    args = parser.parse_args()

    if not any([args.dashboard, args.report, args.usage, args.collect_metric, args.status, args.health]):
        parser.print_help()
        return

    cli = AnalyticsCLI()

    try:
        if args.dashboard:
            cli.show_dashboard(args.dashboard)

        elif args.report:
            cli.generate_report(args.report, args.output)

        elif args.usage:
            cli.show_usage_analytics(args.agent, args.hours_back)

        elif args.collect_metric:
            name, value_str = args.collect_metric
            # Try to parse value as number
            try:
                value = float(value_str)
            except ValueError:
                value = value_str

            tags = None
            if args.tags:
                try:
                    tags = json.loads(args.tags)
                except json.JSONDecodeError:
                    print("❌ Invalid tags JSON format")
                    return

            cli.collect_custom_metric(name, value, tags)

        elif args.status:
            cli.show_service_status()

        elif args.health:
            cli.run_health_check()

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        cli.shutdown()


if __name__ == "__main__":
    main()
