"""
Predictive Analytics CLI
========================

Command-line interface for the Predictive Analytics Engine.
Provides real-time performance analysis, capacity planning, and anomaly detection.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from analytics.predictive_engine import PerformanceMetrics, PredictiveAnalyticsEngine


def create_sample_metrics(
    cpu: float = 50.0, memory: float = 60.0, response_time: float = 200.0, error_rate: float = 0.01
) -> PerformanceMetrics:
    """Create sample performance metrics for testing."""
    return PerformanceMetrics(
        timestamp=datetime.now(),
        cpu_usage=cpu,
        memory_usage=memory,
        disk_io=30.0,
        network_io=40.0,
        response_time=response_time,
        throughput=1000.0,
        error_rate=error_rate,
        active_connections=50,
    )


def analyze_current_performance(
    engine: PredictiveAnalyticsEngine, metrics: PerformanceMetrics
) -> dict:
    """Analyze current performance and return results."""
    return engine.analyze_performance(metrics)


def display_analysis(analysis: dict) -> None:
    """Display analysis results in a formatted way."""
    print("\n" + "=" * 60)
    print("🔮 PREDICTIVE ANALYTICS REPORT")
    print("=" * 60)

    # Current metrics
    current = analysis["current_metrics"]
    print("\n📊 CURRENT METRICS:")
    print(f"   CPU Usage:     {current['cpu_usage']:.1f}%")
    print(f"   Memory Usage:  {current['memory_usage']:.1f}%")
    print(f"   Response Time: {current['response_time']:.1f}ms")
    print(f"   Error Rate:    {current['error_rate']:.3f}")
    print(f"   Throughput:    {current['throughput']:.0f} req/s")

    # Overall health
    health = analysis["overall_health"]
    status_emoji = {"excellent": "🟢", "good": "🟡", "fair": "🟠", "poor": "🔴"}

    print(
        f"\n🏥 OVERALL HEALTH: {status_emoji.get(health['status'], '❓')} {health['status'].upper()}"
    )
    print(f"   Health Score: {health['score']:.1f}/100")

    components = health["components"]
    print(f"   CPU Health:    {components['cpu_health']:.1f}%")
    print(f"   Memory Health: {components['memory_health']:.1f}%")
    print(f"   Response Health: {components['response_health']:.1f}%")
    print(f"   Error Health:  {components['error_health']:.1f}%")

    # Load forecast
    load_forecast = analysis["predictions"]["load_forecast"]
    trend_emoji = {"increasing": "📈", "decreasing": "📉", "stable": "➡️"}

    print("\n🔮 LOAD FORECAST (1 hour ahead):")
    print(f"   Predicted Load: {load_forecast['predicted_value']:.1f}%")
    print(f"   Confidence:     {load_forecast['confidence']:.1%}")
    print(
        f"   Trend:          {trend_emoji.get(load_forecast['trend'], '❓')} {load_forecast['trend']}"
    )
    print(f"   Anomaly Score:  {load_forecast['anomaly_score']:.2f}")

    if load_forecast["recommendations"]:
        print("   Recommendations:")
        for rec in load_forecast["recommendations"]:
            print(f"     • {rec}")

    # Capacity forecasts
    capacity_forecasts = analysis["predictions"]["capacity_forecasts"]
    print("\n📈 CAPACITY FORECASTS:")
    for forecast in capacity_forecasts:
        time_to_limit = forecast.get("time_to_limit")
        time_str = f"{time_to_limit:.1f}h" if time_to_limit else "N/A"

        print(f"   {forecast['resource']}:")
        print(f"     Current:  {forecast['current_usage']:.1f}%")
        print(f"     Predicted: {forecast['predicted_usage']:.1f}%")
        print(f"     Time to 80%: {time_str}")
        print(f"     Recommendation: {forecast['scaling_recommendation']}")
        print(f"     Confidence: {forecast['confidence']:.1%}")

    # Anomalies
    anomalies = analysis["predictions"]["anomalies"]
    if anomalies:
        print("\n⚠️  DETECTED ANOMALIES:")
        for anomaly in anomalies:
            print(f"   {anomaly['metric']}:")
            print(f"     Value: {anomaly['value']:.2f}")
            print(f"     Anomaly Score: {anomaly['anomaly_score']:.2f}")
            print(f"     Confidence: {anomaly['confidence']:.1%}")
            if anomaly["recommendations"]:
                print("     Recommendations:")
                for rec in anomaly["recommendations"]:
                    print(f"       • {rec}")
    else:
        print("\n✅ NO ANOMALIES DETECTED")

    print("\n" + "=" * 60)


def simulate_time_series(engine: PredictiveAnalyticsEngine, duration_hours: int = 6) -> None:
    """Simulate time series data for demonstration."""
    print(f"\n🎬 SIMULATING {duration_hours} HOURS OF DATA...")

    base_time = datetime.now() - timedelta(hours=duration_hours)

    # Simulate increasing load scenario
    for hour in range(duration_hours):
        # Simulate gradual load increase with some noise
        cpu_base = 40.0 + (hour * 8)  # 40% to 88%
        memory_base = 50.0 + (hour * 6)  # 50% to 80%

        # Add some noise
        import random

        cpu_noise = random.uniform(-5, 5)
        memory_noise = random.uniform(-3, 3)

        metrics = create_sample_metrics(
            cpu=cpu_base + cpu_noise,
            memory=memory_base + memory_noise,
            response_time=150.0 + (hour * 20),
            error_rate=0.005 + (hour * 0.002),
        )

        # Set timestamp
        metrics.timestamp = base_time + timedelta(hours=hour)

        print(
            f"   Hour {hour + 1}: CPU={metrics.cpu_usage:.1f}%, Memory={metrics.memory_usage:.1f}%"
        )
        engine.analyze_performance(metrics)

    # Analyze final state
    final_metrics = create_sample_metrics(
        cpu=85.0, memory=78.0, response_time=300.0, error_rate=0.02
    )

    print("\n📊 FINAL ANALYSIS:")
    analysis = engine.analyze_performance(final_metrics)
    display_analysis(analysis)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Predictive Analytics Engine CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze current performance with sample data
  python tools/predictive_analytics_cli.py analyze --cpu 70 --memory 75

  # Simulate time series data
  python tools/predictive_analytics_cli.py simulate --hours 8

  # Analyze with high load scenario
  python tools/predictive_analytics_cli.py analyze --cpu 90 --memory 85 --response-time 1000

  # Save analysis to file
  python tools/predictive_analytics_cli.py analyze --cpu 60 --memory 70 --output analysis.json
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze current performance")
    analyze_parser.add_argument("--cpu", type=float, default=50.0, help="CPU usage percentage")
    analyze_parser.add_argument(
        "--memory", type=float, default=60.0, help="Memory usage percentage"
    )
    analyze_parser.add_argument(
        "--response-time", type=float, default=200.0, help="Response time in ms"
    )
    analyze_parser.add_argument("--error-rate", type=float, default=0.01, help="Error rate (0-1)")
    analyze_parser.add_argument("--output", type=str, help="Save analysis to JSON file")

    # Simulate command
    simulate_parser = subparsers.add_parser("simulate", help="Simulate time series data")
    simulate_parser.add_argument("--hours", type=int, default=6, help="Hours of data to simulate")

    # History command
    history_parser = subparsers.add_parser("history", help="Show prediction history")
    history_parser.add_argument(
        "--limit", type=int, default=10, help="Number of recent analyses to show"
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize engine
    engine = PredictiveAnalyticsEngine()

    try:
        if args.command == "analyze":
            # Create metrics from arguments
            metrics = create_sample_metrics(
                cpu=args.cpu,
                memory=args.memory,
                response_time=args.response_time,
                error_rate=args.error_rate,
            )

            # Analyze performance
            analysis = analyze_current_performance(engine, metrics)

            # Display results
            display_analysis(analysis)

            # Save to file if requested
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(analysis, f, indent=2, default=str)
                print(f"\n💾 Analysis saved to {args.output}")

        elif args.command == "simulate":
            simulate_time_series(engine, args.hours)

        elif args.command == "history":
            history = engine.get_prediction_history(limit=args.limit)

            if not history:
                print("📭 No prediction history available")
                return

            print(f"\n📚 PREDICTION HISTORY (Last {len(history)} analyses):")
            print("-" * 60)

            for i, analysis in enumerate(history, 1):
                health = analysis["overall_health"]
                timestamp = analysis["timestamp"]

                print(f"{i:2d}. {timestamp}")
                print(f"    Health: {health['status'].upper()} ({health['score']:.1f}/100)")

                load_forecast = analysis["predictions"]["load_forecast"]
                print(
                    f"    Load: {load_forecast['predicted_value']:.1f}% ({load_forecast['trend']})"
                )

                anomalies = analysis["predictions"]["anomalies"]
                if anomalies:
                    print(f"    Anomalies: {len(anomalies)} detected")
                else:
                    print("    Anomalies: None")
                print()

    except KeyboardInterrupt:
        print("\n\n⏹️  Analysis interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
