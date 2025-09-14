import logging

logger = logging.getLogger(__name__)
"""
Performance CLI - V2 Compliance Module
======================================

Command-line interface for performance monitoring and optimization.
Provides easy access to performance metrics and controls.

Author: Agent-2 - Architecture & Design Specialist
License: MIT
"""
import argparse
import json
import sys

from .performance_dashboard import get_performance_dashboard
from .performance_monitoring_system import (
    get_performance_monitor,
    start_performance_monitoring,
    stop_performance_monitoring,
)
from .performance_optimization_engine import (
    get_optimization_engine,
    start_performance_optimization,
    stop_performance_optimization,
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Performance Monitoring and Optimization CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    monitor_parser = subparsers.add_parser("monitor", help="Performance monitoring commands")
    monitor_subparsers = monitor_parser.add_subparsers(dest="monitor_action")
    monitor_subparsers.add_parser("start", help="Start performance monitoring")
    monitor_subparsers.add_parser("stop", help="Stop performance monitoring")
    monitor_subparsers.add_parser("status", help="Get monitoring status")
    monitor_subparsers.add_parser("metrics", help="Get current metrics")
    opt_parser = subparsers.add_parser("optimize", help="Performance optimization commands")
    opt_subparsers = opt_parser.add_subparsers(dest="opt_action")
    opt_subparsers.add_parser("start", help="Start performance optimization")
    opt_subparsers.add_parser("stop", help="Stop performance optimization")
    opt_subparsers.add_parser("status", help="Get optimization status")
    opt_subparsers.add_parser("history", help="Get optimization history")
    dashboard_parser = subparsers.add_parser("dashboard", help="Performance dashboard commands")
    dashboard_subparsers = dashboard_parser.add_subparsers(dest="dashboard_action")
    dashboard_subparsers.add_parser("summary", help="Get dashboard summary")
    dashboard_subparsers.add_parser("trends", help="Get performance trends")
    dashboard_subparsers.add_parser("alerts", help="Get performance alerts")
    dashboard_subparsers.add_parser("export", help="Export performance data")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="Output format")
    parser.add_argument("--hours", type=int, default=24, help="Time period in hours")
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
    try:
        if args.command == "monitor":
            handle_monitor_command(args)
        elif args.command == "optimize":
            handle_optimize_command(args)
        elif args.command == "dashboard":
            handle_dashboard_command(args)
        else:
            logger.info(f"Unknown command: {args.command}")
            sys.exit(1)
    except Exception as e:
        logger.info(f"Error: {e}")
        sys.exit(1)


def handle_monitor_command(args):
    """Handle monitor commands."""
    monitor = get_performance_monitor()
    if args.monitor_action == "start":
        start_performance_monitoring()
        logger.info("Performance monitoring started")
    elif args.monitor_action == "stop":
        stop_performance_monitoring()
        logger.info("Performance monitoring stopped")
    elif args.monitor_action == "status":
        summary = monitor.get_performance_summary()
        if args.format == "json":
            logger.info(json.dumps(summary, indent=2))
        else:
            logger.info(f"Status: {summary.get('status', 'unknown')}")
            if summary.get("status") == "active":
                logger.info(f"CPU: {summary.get('cpu_percent', 0):.1f}%")
                logger.info(f"Memory: {summary.get('memory_percent', 0):.1f}%")
                logger.info(f"Metrics Count: {summary.get('metrics_count', 0)}")
    elif args.monitor_action == "metrics":
        summary = monitor.get_metrics_summary(hours=args.hours)
        if args.format == "json":
            logger.info(json.dumps(summary, indent=2))
        elif summary.get("status") == "no_data":
            logger.info("No metrics data available")
        else:
            for name, data in summary.items():
                if isinstance(data, dict) and "avg" in data:
                    logger.info(
                        f"{name}: avg={data['avg']:.2f}, min={data['min']:.2f}, max={data['max']:.2f}"
                    )
    else:
        logger.info("Unknown monitor action")


def handle_optimize_command(args):
    """Handle optimization commands."""
    optimizer = get_optimization_engine()
    if args.opt_action == "start":
        start_performance_optimization()
        logger.info("Performance optimization started")
    elif args.opt_action == "stop":
        stop_performance_optimization()
        logger.info("Performance optimization stopped")
    elif args.opt_action == "status":
        summary = optimizer.get_optimization_summary()
        if args.format == "json":
            logger.info(json.dumps(summary, indent=2))
        else:
            logger.info(f"Optimization Active: {summary.get('optimization_active', False)}")
            logger.info(
                f"Rules: {summary.get('enabled_rules', 0)}/{summary.get('rules_count', 0)} enabled"
            )
            logger.info(f"Total Optimizations: {summary.get('total_optimizations', 0)}")
            logger.info(f"Average Improvement: {summary.get('average_improvement', 0):.2f}%")
    elif args.opt_action == "history":
        history = optimizer.get_optimization_history(hours=args.hours)
        if args.format == "json":
            logger.info(json.dumps(history, indent=2))
        elif not history:
            logger.info("No optimization history available")
        else:
            for opt in history[-10:]:
                status = "✓" if opt["success"] else "✗"
                logger.info(
                    f"{status} {opt['rule_name']}: {opt['improvement_percent']:.2f}% improvement"
                )
    else:
        logger.info("Unknown optimization action")


def handle_dashboard_command(args):
    """Handle dashboard commands."""
    dashboard = get_performance_dashboard()
    if args.dashboard_action == "summary":
        summary = dashboard.get_dashboard_summary()
        if args.format == "json":
            logger.info(json.dumps(summary, indent=2))
        else:
            logger.info("=== Performance Dashboard Summary ===")
            logger.info(f"Status: {summary.get('dashboard_status', 'unknown')}")
            real_time = summary.get("real_time_metrics", {})
            if real_time.get("status") == "active":
                system = real_time.get("system", {})
                logger.info(f"CPU: {system.get('cpu_percent', 0):.1f}%")
                logger.info(f"Memory: {system.get('memory_percent', 0):.1f}%")
            alerts = summary.get("alerts", [])
            if alerts:
                logger.info(f"\nAlerts: {len(alerts)}")
                for alert in alerts:
                    logger.info(f"  - {alert['message']} ({alert['severity']})")
            else:
                logger.info("\nNo active alerts")
    elif args.dashboard_action == "trends":
        trends = dashboard.get_performance_trends(hours=args.hours)
        if args.format == "json":
            logger.info(json.dumps(trends, indent=2))
        elif trends.get("status") == "no_data":
            logger.info("No trend data available")
        else:
            logger.info("=== Performance Trends ===")
            cpu_trend = trends.get("trends", {}).get("cpu", {})
            mem_trend = trends.get("trends", {}).get("memory", {})
            logger.info(
                f"CPU: {cpu_trend.get('current', 0):.1f}% (trend: {cpu_trend.get('trend', 'unknown')})"
            )
            logger.info(
                f"Memory: {mem_trend.get('current', 0):.1f}% (trend: {mem_trend.get('trend', 'unknown')})"
            )
    elif args.dashboard_action == "alerts":
        alerts = dashboard.get_performance_alerts()
        if args.format == "json":
            logger.info(json.dumps(alerts, indent=2))
        elif not alerts:
            logger.info("No active alerts")
        else:
            logger.info("=== Performance Alerts ===")
            for alert in alerts:
                logger.info(f"{alert['severity'].upper()}: {alert['message']}")
    elif args.dashboard_action == "export":
        data = dashboard.export_performance_data(hours=args.hours)
        logger.info(data)
    else:
        logger.info("Unknown dashboard action")


if __name__ == "__main__":
    main()
