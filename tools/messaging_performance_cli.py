#!/usr/bin/env python3
"""
Messaging Performance CLI Tool
===============================

Command-line interface for messaging performance monitoring and optimization.
Provides tools for real-time monitoring, bottleneck analysis, and performance optimization.

Author: Agent-5 (Business Intelligence Specialist)
Usage: python tools/messaging_performance_cli.py --monitor --dashboard
"""

import argparse
import json
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from services.messaging_performance_monitor import get_messaging_performance_monitor


class MessagingPerformanceCLI:
    """Command-line interface for messaging performance monitoring."""

    def __init__(self):
        self.monitor = get_messaging_performance_monitor()
        self.dashboard_process = None

    def start_monitoring(self, background: bool = False) -> None:
        pass
EXAMPLE USAGE:
==============

# Basic usage example
from tools.messaging_performance_cli import Messaging_Performance_Cli

# Initialize and use
instance = Messaging_Performance_Cli()
result = instance.execute()
print(f"Execution result: {result}")

# Advanced configuration
config = {
    "option1": "value1",
    "option2": True
}

instance = Messaging_Performance_Cli(config)
advanced_result = instance.execute_advanced()
print(f"Advanced result: {advanced_result}")

        """Start performance monitoring."""
        print("🚀 Starting messaging performance monitoring...")

        if background:
            # Start monitoring in background thread
            monitor_thread = threading.Thread(target=self._run_monitoring, daemon=True)
            monitor_thread.start()
            print("✅ Monitoring started in background")
        else:
            # Start monitoring and keep running
            self.monitor.start_monitoring()
            print("✅ Monitoring started (press Ctrl+C to stop)")

            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping monitoring...")
                self.stop_monitoring()

    def _run_monitoring(self) -> None:
        """Run monitoring in background thread."""
        self.monitor.start_monitoring()

    def stop_monitoring(self) -> None:
        """Stop performance monitoring."""
        self.monitor.stop_monitoring()
        print("✅ Monitoring stopped")

    def show_current_metrics(self) -> None:
        """Display current performance metrics."""
        print("📊 Current Messaging Performance Metrics")
        print("=" * 50)

        try:
            metrics = self.monitor.get_current_metrics()

            print(f"📅 Timestamp: {metrics.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"🏥 Health Score: {metrics.health_score:.1f}/100")

            print("\n⚡ Performance Metrics:")
            print(f"   CPU Usage: {metrics.cpu_usage_percent:.1f}%")
            print(f"   Memory Usage: {metrics.memory_usage_mb:.1f} MB")
            print(f"   Messages/sec: {metrics.messages_per_second:.2f}")
            print(f"   Queue Depth: {metrics.queue_depth}")

            print("\n📈 Reliability Metrics:")
            print(f"   Delivery Success Rate: {metrics.delivery_success_rate:.1f}%")
            print(f"   Error Rate: {metrics.error_rate_percent:.1f}%")
            print(f"   Messages Processed: {metrics.messages_processed}")
            print(f"   Delivery Errors: {metrics.delivery_errors}")

            if metrics.bottleneck_detected:
                print(f"\n🚨 Bottlenecks Detected: {metrics.bottleneck_description}")
                if metrics.optimization_recommendations:
                    print("🎯 Recommendations:")
                    for rec in metrics.optimization_recommendations:
                        print(f"   • {rec}")
            else:
                print("\n✅ No bottlenecks detected")

        except Exception as e:
            print(f"❌ Error retrieving metrics: {e}")

    def show_performance_summary(self, hours_back: int = 24) -> None:
        """Display performance summary."""
        print(f"📈 Messaging Performance Summary (Last {hours_back} hours)")
        print("=" * 60)

        try:
            summary = self.monitor.get_performance_summary(hours_back)

            if "error" in summary:
                print(f"❌ Error: {summary['error']}")
                return

            print(f"📊 Measurements: {summary['measurements_count']}")
            print(f"⏱️  Period: {summary['period_hours']} hours")

            print("\n📊 Average Performance:")
            averages = summary['averages']
            print(f"   Health Score: {averages['health_score']:.1f}/100")
            print(f"   CPU Usage: {averages['cpu_usage_percent']:.1f}%")
            print(f"   Memory Usage: {averages['memory_usage_mb']:.1f} MB")
            print(f"   Queue Depth: {averages['queue_depth']:.0f}")
            print(f"   Error Rate: {averages['error_rate_percent']:.2f}%")
            print(f"   Throughput: {averages['throughput_msg_per_sec']:.2f} msg/sec")

            print("\n📊 Peak Values:")
            peaks = summary['peaks']
            print(f"   CPU Usage: {peaks['cpu_usage_percent']:.1f}%")
            print(f"   Memory Usage: {peaks['memory_usage_mb']:.1f} MB")
            print(f"   Queue Depth: {peaks['queue_depth']:.0f}")
            print(f"   Error Rate: {peaks['error_rate_percent']:.2f}%")

            print("\n🚨 Threshold Violations:")
            violations = summary['threshold_violations']
            for threshold, count in violations.items():
                if count > 0:
                    print(f"   {threshold.replace('_', ' ').title()}: {count} violations")
                else:
                    print(f"   {threshold.replace('_', ' ').title()}: ✓ Within limits")

            print(f"\n🚨 Bottleneck Events: {summary['current_bottlenecks']}")

        except Exception as e:
            print(f"❌ Error retrieving performance summary: {e}")

    def show_bottleneck_analysis(self) -> None:
        """Display bottleneck analysis."""
        print("🔍 Messaging Bottleneck Analysis")
        print("=" * 40)

        try:
            # Get current metrics for bottleneck status
            current_metrics = self.monitor.get_current_metrics()
            patterns = self.monitor._analyze_bottleneck_patterns()
            summary = self.monitor.get_performance_summary(24)
            recommendations = self.monitor._generate_optimization_recommendations(summary)

            print(f"🚨 Current Status: {'Bottlenecks Detected' if current_metrics.bottleneck_detected else 'System Healthy'}")

            if current_metrics.bottleneck_detected:
                print(f"📝 Description: {current_metrics.bottleneck_description}")

            print("\n📊 Bottleneck Patterns (Last 24h):")
            if patterns:
                for bottleneck_type, count in patterns.items():
                    print(f"   {bottleneck_type.upper()}: {count} occurrences")
            else:
                print("   No bottleneck patterns detected")

            print("\n🎯 Optimization Recommendations:")
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec}")
            else:
                print("   No optimization recommendations at this time")

        except Exception as e:
            print(f"❌ Error retrieving bottleneck analysis: {e}")

    def generate_optimization_report(self, output_file: Optional[str] = None) -> None:
        """Generate comprehensive optimization report."""
        print("📋 Generating Messaging Optimization Report")
        print("=" * 50)

        try:
            report = self.monitor.generate_optimization_report()

            print(f"📅 Generated: {report['generated_at']}")
            print(f"🔍 Analysis Period: {report['analysis_period_hours']} hours")

            print("\n📊 Performance Summary:")
            summary = report['performance_summary']
            if "error" not in summary:
                averages = summary['averages']
                print(f"   Health Score: {averages['health_score']:.1f}/100")
                print(f"   CPU Usage: {averages['cpu_usage_percent']:.1f}%")
                print(f"   Throughput: {averages['throughput_msg_per_sec']:.2f} msg/sec")
                print(f"   Error Rate: {averages['error_rate_percent']:.2f}%")

            print("\n🔍 Bottleneck Analysis:")
            bottleneck_analysis = report['bottleneck_analysis']
            patterns = bottleneck_analysis['most_common_bottleneck_types']
            if patterns:
                print("   Most Common Bottlenecks:")
                for bottleneck_type, count in patterns.items():
                    print(f"     {bottleneck_type.upper()}: {count} times")
            else:
                print("   No significant bottleneck patterns detected")

            print("\n🎯 Optimization Recommendations:")
            recommendations = report['optimization_recommendations']
            if recommendations:
                for i, rec in enumerate(recommendations, 1):
                    print(f"   {i}. {rec}")
            else:
                print("   No optimization recommendations at this time")

            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(report, f, indent=2, default=str)
                print(f"\n💾 Report saved to: {output_file}")

        except Exception as e:
            print(f"❌ Error generating optimization report: {e}")

    def start_dashboard(self, background: bool = False) -> None:
        """Start the messaging performance dashboard."""
        print("🚀 Starting Messaging Performance Dashboard...")

        try:
            # Import dashboard module
            from web.messaging_performance_dashboard import MessagingPerformanceDashboard

            dashboard = MessagingPerformanceDashboard()

            if background:
                # Start dashboard in background process
                import multiprocessing
                dashboard_process = multiprocessing.Process(
                    target=dashboard.start,
                    kwargs={'host': 'localhost', 'port': 8002}
                )
                dashboard_process.start()
                self.dashboard_process = dashboard_process
                print("✅ Dashboard started in background on http://localhost:8002")
            else:
                # Start dashboard in foreground
                dashboard.start(host='localhost', port=8002)

        except ImportError:
            print("❌ Dashboard dependencies not available")
        except Exception as e:
            print(f"❌ Error starting dashboard: {e}")

    def stop_dashboard(self) -> None:
        """Stop the dashboard if running in background."""
        if self.dashboard_process:
            self.dashboard_process.terminate()
            self.dashboard_process.join(timeout=5)
            print("✅ Dashboard stopped")
        else:
            print("ℹ️  No background dashboard process found")

    def update_thresholds(self, thresholds: Dict[str, Any]) -> None:
        """Update performance monitoring thresholds."""
        try:
            self.monitor.update_thresholds(thresholds)
            print(f"✅ Thresholds updated: {thresholds}")
        except Exception as e:
            print(f"❌ Error updating thresholds: {e}")

    def record_test_metrics(self) -> None:
        """Record some test metrics for demonstration."""
        print("🧪 Recording test metrics for demonstration...")

        try:
            # Record some sample delivery times
            import random
            for i in range(10):
                delivery_time = random.uniform(0.1, 2.0)
                success = random.random() > 0.1  # 90% success rate
                self.monitor.record_message_delivery(delivery_time, success)
                time.sleep(0.1)

            print("✅ Test metrics recorded")
            print("   Hint: Run 'python tools/messaging_performance_cli.py --current' to see the metrics")

        except Exception as e:
            print(f"❌ Error recording test metrics: {e}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Messaging Performance CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start monitoring and show current metrics
  python tools/messaging_performance_cli.py --monitor --current

  # Show 24-hour performance summary
  python tools/messaging_performance_cli.py --summary --hours 24

  # Analyze bottlenecks and show recommendations
  python tools/messaging_performance_cli.py --bottlenecks

  # Generate optimization report
  python tools/messaging_performance_cli.py --report --output report.json

  # Start web dashboard
  python tools/messaging_performance_cli.py --dashboard

  # Update performance thresholds
  python tools/messaging_performance_cli.py --thresholds '{"max_cpu_usage_percent": 75}'

  # Record test metrics for demonstration
  python tools/messaging_performance_cli.py --test-metrics
        """
    )

    parser.add_argument(
        "--monitor", "-m",
        action="store_true",
        help="Start performance monitoring"
    )

    parser.add_argument(
        "--background", "-b",
        action="store_true",
        help="Run monitoring/dashboard in background"
    )

    parser.add_argument(
        "--current", "-c",
        action="store_true",
        help="Show current performance metrics"
    )

    parser.add_argument(
        "--summary", "-s",
        action="store_true",
        help="Show performance summary"
    )

    parser.add_argument(
        "--hours",
        type=int,
        default=24,
        help="Hours of data for summary (default: 24)"
    )

    parser.add_argument(
        "--bottlenecks",
        action="store_true",
        help="Show bottleneck analysis"
    )

    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate optimization report"
    )

    parser.add_argument(
        "--dashboard", "-d",
        action="store_true",
        help="Start web performance dashboard"
    )

    parser.add_argument(
        "--thresholds", "-t",
        help="Update performance thresholds (JSON string)"
    )

    parser.add_argument(
        "--test-metrics",
        action="store_true",
        help="Record test metrics for demonstration"
    )

    parser.add_argument(
        "--output", "-o",
        help="Output file for reports"
    )

    args = parser.parse_args()

    # Check if any action was specified
    actions = [args.monitor, args.current, args.summary, args.bottlenecks,
              args.report, args.dashboard, args.thresholds, args.test_metrics]
    if not any(actions):
        parser.print_help()
        return

    cli = MessagingPerformanceCLI()

    try:
        if args.thresholds:
            # Parse and update thresholds
            try:
                thresholds = json.loads(args.thresholds)
                cli.update_thresholds(thresholds)
            except json.JSONDecodeError:
                print("❌ Invalid JSON format for thresholds")
                return

        elif args.test_metrics:
            cli.record_test_metrics()

        elif args.dashboard:
            cli.start_dashboard(background=args.background)

        elif args.monitor:
            cli.start_monitoring(background=args.background)

        elif args.current:
            cli.show_current_metrics()

        elif args.summary:
            cli.show_performance_summary(args.hours)

        elif args.bottlenecks:
            cli.show_bottleneck_analysis()

        elif args.report:
            cli.generate_optimization_report(args.output)

    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        cli.stop_monitoring()
        cli.stop_dashboard()


if __name__ == "__main__":
    main()



