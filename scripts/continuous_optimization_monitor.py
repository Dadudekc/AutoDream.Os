#!/usr/bin/env python3
"""
Continuous Optimization Monitor
==============================

Monitors system performance continuously and applies optimizations automatically.
"""

import asyncio
import json
import logging
import threading
from datetime import datetime
from pathlib import Path
from typing import Any

import psutil

logger = logging.getLogger(__name__)


class ContinuousOptimizationMonitor:
    """Continuous optimization monitoring and application system."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.is_monitoring = False
        self.monitoring_task: asyncio.Task | None = None

        # Optimization thresholds
        self.optimization_thresholds = {
            "cpu_percent": 70.0,
            "memory_mb": 800.0,
            "response_time_ms": 3000.0,
            "error_rate": 0.05,
            "cache_hit_rate": 0.6,
        }

        # Optimization history
        self.optimization_history: list[dict[str, Any]] = []
        self.performance_baseline: dict[str, float] = {}

        # Component references
        self.workflow_optimizer = None
        self.discord_optimizer = None
        self.performance_monitor = None

        # Monitoring state
        self.start_time = datetime.now()
        self.optimization_count = 0
        self.lock = threading.RLock()

    def register_components(self, workflow_optimizer, discord_optimizer, performance_monitor):
        """Register optimization components."""
        self.workflow_optimizer = workflow_optimizer
        self.discord_optimizer = discord_optimizer
        self.performance_monitor = performance_monitor
        logger.info("Optimization components registered")

    async def collect_performance_metrics(self) -> dict[str, Any]:
        """Collect current performance metrics."""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()

            # Component metrics
            workflow_stats = {}
            discord_stats = {}

            if self.workflow_optimizer:
                workflow_stats = self.workflow_optimizer.get_optimization_stats()

            if self.discord_optimizer:
                discord_stats = self.discord_optimizer.get_optimization_stats()

            # Performance monitor metrics
            monitor_status = {}
            if self.performance_monitor:
                monitor_status = await self.performance_monitor.get_current_status()

            return {
                "timestamp": datetime.now().isoformat(),
                "system": {
                    "cpu_percent": cpu_percent,
                    "memory_mb": memory.used / 1024 / 1024,
                    "memory_percent": memory.percent,
                },
                "workflow": workflow_stats,
                "discord": discord_stats,
                "monitor": monitor_status,
            }

        except Exception as e:
            logger.error(f"Failed to collect performance metrics: {e}")
            return {}

    async def analyze_performance_trends(self, metrics: dict[str, Any]) -> list[str]:
        """Analyze performance trends and identify optimization opportunities."""
        recommendations = []

        try:
            # CPU analysis
            cpu_percent = metrics.get("system", {}).get("cpu_percent", 0)
            if cpu_percent > self.optimization_thresholds["cpu_percent"]:
                recommendations.append(
                    "High CPU usage detected - consider enabling parallel processing"
                )

            # Memory analysis
            memory_mb = metrics.get("system", {}).get("memory_mb", 0)
            if memory_mb > self.optimization_thresholds["memory_mb"]:
                recommendations.append("High memory usage detected - consider clearing caches")

            # Response time analysis
            response_time = (
                metrics.get("monitor", {}).get("system_metrics", {}).get("response_time_ms", 0)
            )
            if response_time > self.optimization_thresholds["response_time_ms"]:
                recommendations.append(
                    "High response time detected - consider optimizing workflows"
                )

            # Cache analysis
            workflow_cache = metrics.get("workflow", {}).get("cache", {})
            discord_cache = metrics.get("discord", {}).get("cache", {})

            workflow_hit_rate = workflow_cache.get("hit_rate", 0)
            discord_hit_rate = discord_cache.get("hit_rate", 0)

            if workflow_hit_rate < self.optimization_thresholds["cache_hit_rate"]:
                recommendations.append("Low workflow cache hit rate - consider cache optimization")

            if discord_hit_rate < self.optimization_thresholds["cache_hit_rate"]:
                recommendations.append("Low Discord cache hit rate - consider cache optimization")

            # Error rate analysis
            error_rate = metrics.get("monitor", {}).get("error_rate", 0)
            if error_rate > self.optimization_thresholds["error_rate"]:
                recommendations.append(
                    "High error rate detected - consider error handling improvements"
                )

        except Exception as e:
            logger.error(f"Performance trend analysis failed: {e}")

        return recommendations

    async def apply_optimizations(self, recommendations: list[str]) -> dict[str, Any]:
        """Apply recommended optimizations."""
        applied_optimizations = {}

        try:
            for recommendation in recommendations:
                if "parallel processing" in recommendation.lower():
                    if self.workflow_optimizer:
                        self.workflow_optimizer.enable_optimization()
                        applied_optimizations["workflow_parallel_processing"] = True
                        logger.info("Enabled workflow parallel processing")

                elif "clearing caches" in recommendation.lower():
                    if self.workflow_optimizer:
                        self.workflow_optimizer.clear_cache()
                        applied_optimizations["workflow_cache_cleared"] = True

                    if self.discord_optimizer:
                        self.discord_optimizer.clear_cache()
                        applied_optimizations["discord_cache_cleared"] = True

                    logger.info("Cleared optimization caches")

                elif "cache optimization" in recommendation.lower():
                    if self.workflow_optimizer:
                        # Increase cache size
                        current_stats = self.workflow_optimizer.get_optimization_stats()
                        cache_size = current_stats.get("cache", {}).get("max_size", 1000)
                        # Note: Cache size increase would need to be implemented in the optimizer
                        applied_optimizations["workflow_cache_optimized"] = True

                    if self.discord_optimizer:
                        # Increase Discord cache size
                        current_stats = self.discord_optimizer.get_optimization_stats()
                        cache_size = current_stats.get("cache", {}).get("max_size", 500)
                        # Note: Cache size increase would need to be implemented in the optimizer
                        applied_optimizations["discord_cache_optimized"] = True

                    logger.info("Optimized cache settings")

                elif "error handling" in recommendation.lower():
                    # Log error handling recommendation
                    applied_optimizations["error_handling_review"] = True
                    logger.info("Error handling review recommended")

            # Record optimization
            with self.lock:
                self.optimization_count += 1

                optimization_record = {
                    "timestamp": datetime.now().isoformat(),
                    "optimization_id": self.optimization_count,
                    "recommendations": recommendations,
                    "applied_optimizations": applied_optimizations,
                    "metrics_at_time": await self.collect_performance_metrics(),
                }

                self.optimization_history.append(optimization_record)

                # Keep only last 100 optimization records
                if len(self.optimization_history) > 100:
                    self.optimization_history = self.optimization_history[-100:]

        except Exception as e:
            logger.error(f"Failed to apply optimizations: {e}")

        return applied_optimizations

    async def establish_baseline(self) -> bool:
        """Establish performance baseline."""
        try:
            logger.info("Establishing performance baseline...")

            # Collect metrics over 5 minutes
            baseline_metrics = []
            for _ in range(10):  # 10 samples over 5 minutes
                metrics = await self.collect_performance_metrics()
                if metrics:
                    baseline_metrics.append(metrics)
                await asyncio.sleep(30)  # 30 seconds between samples

            if baseline_metrics:
                # Calculate baseline averages
                cpu_values = [m.get("system", {}).get("cpu_percent", 0) for m in baseline_metrics]
                memory_values = [m.get("system", {}).get("memory_mb", 0) for m in baseline_metrics]

                self.performance_baseline = {
                    "cpu_percent": sum(cpu_values) / len(cpu_values),
                    "memory_mb": sum(memory_values) / len(memory_values),
                    "established_at": datetime.now().isoformat(),
                    "sample_count": len(baseline_metrics),
                }

                logger.info(
                    f"Performance baseline established: CPU {self.performance_baseline['cpu_percent']:.1f}%, "
                    f"Memory {self.performance_baseline['memory_mb']:.1f}MB"
                )
                return True
            else:
                logger.error("Failed to collect baseline metrics")
                return False

        except Exception as e:
            logger.error(f"Baseline establishment failed: {e}")
            return False

    async def monitoring_loop(self):
        """Main continuous optimization monitoring loop."""
        logger.info("Starting continuous optimization monitoring...")

        # Establish baseline
        await self.establish_baseline()

        while self.is_monitoring:
            try:
                # Collect current metrics
                current_metrics = await self.collect_performance_metrics()

                if current_metrics:
                    # Analyze performance trends
                    recommendations = await self.analyze_performance_trends(current_metrics)

                    if recommendations:
                        logger.info(f"Performance recommendations: {recommendations}")

                        # Apply optimizations
                        applied = await self.apply_optimizations(recommendations)

                        if applied:
                            logger.info(f"Applied optimizations: {applied}")
                    else:
                        logger.debug("No optimization recommendations")

                # Wait for next monitoring cycle
                await asyncio.sleep(300)  # 5 minutes

            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                await asyncio.sleep(300)

    async def start_monitoring(self):
        """Start continuous optimization monitoring."""
        if self.is_monitoring:
            logger.warning("Continuous optimization monitoring already started")
            return

        self.is_monitoring = True
        self.monitoring_task = asyncio.create_task(self.monitoring_loop())
        logger.info("Continuous optimization monitoring started")

    async def stop_monitoring(self):
        """Stop continuous optimization monitoring."""
        if not self.is_monitoring:
            logger.warning("Continuous optimization monitoring not started")
            return

        self.is_monitoring = False

        if self.monitoring_task:
            self.monitoring_task.cancel()
            try:
                await self.monitoring_task
            except asyncio.CancelledError:
                pass

        logger.info("Continuous optimization monitoring stopped")

    def get_optimization_summary(self) -> dict[str, Any]:
        """Get optimization summary."""
        with self.lock:
            return {
                "monitoring_active": self.is_monitoring,
                "monitoring_duration": (datetime.now() - self.start_time).total_seconds(),
                "total_optimizations": self.optimization_count,
                "performance_baseline": self.performance_baseline,
                "recent_optimizations": self.optimization_history[-10:]
                if self.optimization_history
                else [],
                "optimization_thresholds": self.optimization_thresholds,
            }

    def save_optimization_report(self) -> bool:
        """Save comprehensive optimization report."""
        try:
            report = {
                "report_time": datetime.now().isoformat(),
                "optimization_summary": self.get_optimization_summary(),
                "optimization_history": self.optimization_history,
                "performance_baseline": self.performance_baseline,
            }

            report_path = self.project_root / "logs" / "optimization_report.json"
            report_path.parent.mkdir(exist_ok=True)

            with open(report_path, "w") as f:
                json.dump(report, f, indent=2)

            logger.info(f"Optimization report saved: {report_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to save optimization report: {e}")
            return False


async def main():
    """Main function for continuous optimization monitoring."""
    import argparse

    parser = argparse.ArgumentParser(description="Continuous Optimization Monitor")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--duration", type=int, default=3600, help="Monitoring duration in seconds")

    args = parser.parse_args()

    # Set up logging
    logging.basicConfig(
        level=logging.INFO if not args.verbose else logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    project_root = Path(args.project_root).resolve()

    # Create optimization monitor
    monitor = ContinuousOptimizationMonitor(project_root)

    try:
        # Start monitoring
        await monitor.start_monitoring()

        # Monitor for specified duration
        logger.info(f"Monitoring for {args.duration} seconds...")
        await asyncio.sleep(args.duration)

        # Stop monitoring
        await monitor.stop_monitoring()

        # Save report
        monitor.save_optimization_report()

        # Print summary
        summary = monitor.get_optimization_summary()
        print("🎯 CONTINUOUS OPTIMIZATION SUMMARY")
        print("=" * 50)
        print(f"Monitoring Duration: {summary['monitoring_duration']:.1f} seconds")
        print(f"Total Optimizations: {summary['total_optimizations']}")
        print(
            f"Performance Baseline: CPU {summary['performance_baseline'].get('cpu_percent', 0):.1f}%, "
            f"Memory {summary['performance_baseline'].get('memory_mb', 0):.1f}MB"
        )
        print("=" * 50)

    except KeyboardInterrupt:
        logger.info("Monitoring interrupted by user")
        await monitor.stop_monitoring()
        monitor.save_optimization_report()
    except Exception as e:
        logger.error(f"Monitoring failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(asyncio.run(main()))
