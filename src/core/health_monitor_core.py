#!/usr/bin/env python3
"""
🔍 Health Monitor Core - Agent_Cellphone_V2

This component is responsible for core monitoring loop and coordination.
Following V2 coding standards: ≤200 LOC, OOP design, SRP.

Author: Foundation & Testing Specialist
License: MIT
"""

import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from typing import Dict, Any, Set, Callable
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logger = logging.getLogger(__name__)


class HealthMonitorCore:
    """
    Health Monitor Core - Single responsibility: Core monitoring loop and coordination.

    Follows V2 standards: ≤200 LOC, OOP design, SRP.
    """

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the health monitor core"""
        self.config = config or {}
        self.monitoring_active = False
        self.monitor_thread: threading.Thread = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.health_callbacks: Set[Callable] = set()

        # Monitoring intervals
        self.health_check_interval = self.config.get(
            "health_check_interval", 60
        )  # seconds
        self.metrics_interval = self.config.get("metrics_interval", 30)  # seconds
        self.alert_check_interval = self.config.get(
            "alert_check_interval", 15
        )  # seconds

        logger.info("HealthMonitorCore initialized")

    def start(self):
        """Start health monitoring"""
        if self.monitoring_active:
            logger.warning("Health monitoring already active")
            return

        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Health monitoring started")

    def stop(self):
        """Stop health monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self.executor.shutdown(wait=True)
        logger.info("Health monitoring stopped")

    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Perform health checks
                self._perform_health_checks()

                # Check for alerts
                self._check_alerts()

                # Update health scores
                self._update_health_scores()

                # Notify subscribers
                self._notify_health_updates()

                time.sleep(self.health_check_interval)

            except Exception as e:
                logger.error(f"Error in health monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying

    def _perform_health_checks(self):
        """Perform comprehensive health checks"""
        # This would integrate with the actual health check components
        # For now, we'll log that checks are being performed
        logger.debug("Performing health checks...")

    def _check_alerts(self):
        """Check and manage health alerts"""
        # This would integrate with the alert manager
        # For now, we'll log that alerts are being checked
        logger.debug("Checking health alerts...")

    def _update_health_scores(self):
        """Update health scores for all agents"""
        # This would integrate with the score calculator
        # For now, we'll log that scores are being updated
        logger.debug("Updating health scores...")

    def _notify_health_updates(self):
        """Notify subscribers of health updates"""
        for callback in self.health_callbacks:
            try:
                callback({}, {})  # Empty data for now
            except Exception as e:
                logger.error(f"Error in health update callback: {e}")

    def subscribe_to_health_updates(self, callback: Callable):
        """Subscribe to health update notifications"""
        self.health_callbacks.add(callback)
        logger.info("Health update subscription added")

    def unsubscribe_from_health_updates(self, callback: Callable):
        """Unsubscribe from health update notifications"""
        self.health_callbacks.discard(callback)
        logger.info("Health update subscription removed")

    def get_health_summary(self) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        return {
            "monitoring_active": self.monitoring_active,
            "last_update": datetime.now().isoformat(),
            "subscribers": len(self.health_callbacks),
            "intervals": {
                "health_check": self.health_check_interval,
                "metrics": self.metrics_interval,
                "alerts": self.alert_check_interval,
            },
        }

    def set_monitoring_interval(self, interval_type: str, value: int):
        """Set monitoring interval for a specific type"""
        if interval_type == "health_check":
            self.health_check_interval = value
        elif interval_type == "metrics":
            self.metrics_interval = value
        elif interval_type == "alerts":
            self.alert_check_interval = value
        else:
            logger.warning(f"Unknown interval type: {interval_type}")
            return

        logger.info(f"Monitoring interval updated: {interval_type} = {value}s")

    def get_monitoring_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "active": self.monitoring_active,
            "thread_alive": self.monitor_thread.is_alive()
            if self.monitor_thread
            else False,
            "subscriber_count": len(self.health_callbacks),
            "executor_active": not self.executor._shutdown,
        }

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthMonitorCore smoke test...")

            # Test basic initialization
            assert self.monitoring_active is False
            assert self.health_callbacks == set()
            logger.info("Basic initialization passed")

            # Test monitoring start
            self.start()
            assert self.monitoring_active is True
            assert self.monitor_thread is not None
            assert self.monitor_thread.is_alive()
            logger.info("Monitoring start passed")

            # Test monitoring stop
            self.stop()
            assert self.monitoring_active is False
            logger.info("Monitoring stop passed")

            # Test subscription management
            def test_callback(data, alerts):
                pass

            self.subscribe_to_health_updates(test_callback)
            assert len(self.health_callbacks) == 1
            assert test_callback in self.health_callbacks

            self.unsubscribe_from_health_updates(test_callback)
            assert len(self.health_callbacks) == 0
            logger.info("Subscription management passed")

            # Test health summary
            summary = self.get_health_summary()
            assert isinstance(summary, dict)
            assert "monitoring_active" in summary
            assert "last_update" in summary
            logger.info("Health summary passed")

            # Test monitoring status
            status = self.get_monitoring_status()
            assert isinstance(status, dict)
            assert "active" in status
            assert "thread_alive" in status
            logger.info("Monitoring status passed")

            # Test interval configuration
            self.set_monitoring_interval("health_check", 120)
            assert self.health_check_interval == 120
            logger.info("Interval configuration passed")

            logger.info("✅ HealthMonitorCore smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthMonitorCore smoke test FAILED: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")
            return False

    def shutdown(self):
        """Shutdown the health monitor core"""
        self.stop()
        logger.info("HealthMonitorCore shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Monitor Core CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--demo", action="store_true", help="Run demo mode")

    args = parser.parse_args()

    if args.test:
        core = HealthMonitorCore()
        success = core.run_smoke_test()
        core.shutdown()
        exit(0 if success else 1)

    elif args.demo:
        print("🚀 Starting Health Monitor Core Demo...")
        core = HealthMonitorCore()

        # Show initial status
        print(f"\n📊 Initial Status:")
        status = core.get_monitoring_status()
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Start monitoring
        print(f"\n▶️ Starting monitoring...")
        core.start()

        # Show running status
        print(f"\n📊 Running Status:")
        status = core.get_monitoring_status()
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Add a subscriber
        print(f"\n📡 Adding health update subscriber...")

        def health_callback(health_data, alerts):
            print(f"  📊 Health Update: {len(health_data)} agents, {len(alerts)} alerts")

        core.subscribe_to_health_updates(health_callback)

        # Show summary
        print(f"\n📋 Health Summary:")
        summary = core.get_health_summary()
        for key, value in summary.items():
            print(f"  {key}: {value}")

        # Wait a bit for monitoring
        print(f"\n⏳ Waiting for monitoring to process...")
        time.sleep(3)

        # Stop monitoring
        print(f"\n⏹️ Stopping monitoring...")
        core.stop()

        # Show final status
        print(f"\n📊 Final Status:")
        status = core.get_monitoring_status()
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Cleanup
        core.shutdown()
        print("\n✅ Demo completed")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
