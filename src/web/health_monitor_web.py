"""
Web Interface for Agent Health Monitoring System

This module provides a web-based interface for monitoring agent health,
including real-time updates, health dashboards, and alert management.

Author: Agent-1
License: MIT
"""

import json
import logging
import threading
import time

from src.utils.stability_improvements import stability_manager, safe_import
from datetime import datetime
from typing import Dict, List, Any, Optional
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthMonitorWebInterface:
    """
    Web interface for agent health monitoring

    Features:
    - Real-time health dashboard
    - Alert management interface
    - Health metrics visualization
    - Agent status overview
    - Health recommendations display
    """

    def __init__(self, health_monitor=None, config: Dict[str, Any] = None):
        """Initialize the web interface"""
        self.config = config or {}
        self.health_monitor = health_monitor
        self.app = Flask(__name__)
        self.app.config["SECRET_KEY"] = self.config.get(
            "secret_key", "health_monitor_secret"
        )
        self.app.config["DEBUG"] = self.config.get("debug", False)

        # Initialize Flask extensions
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        CORS(self.app)

        # Web interface state
        self.update_interval = self.config.get("update_interval", 5)  # seconds
        self.update_thread: Optional[threading.Thread] = None
        self.running = False

        # Setup routes and WebSocket events
        self._setup_routes()
        self._setup_websocket_events()

        logger.info("HealthMonitorWebInterface initialized")

    def _setup_routes(self):
        """Setup Flask routes"""

        @self.app.route("/")
        def index():
            """Main health dashboard"""
            return render_template("health_dashboard.html")

        @self.app.route("/api/health/summary")
        def health_summary():
            """Get health summary data"""
            try:
                if self.health_monitor:
                    summary = self.health_monitor.get_health_summary()
                    return jsonify(summary)
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting health summary: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/agents")
        def agent_health():
            """Get health data for all agents"""
            try:
                if self.health_monitor:
                    agents = self.health_monitor.get_all_agent_health()
                    # Convert to serializable format
                    serializable_agents = {}
                    for agent_id, snapshot in agents.items():
                        serializable_agents[agent_id] = {
                            "agent_id": snapshot.agent_id,
                            "timestamp": snapshot.timestamp.isoformat(),
                            "overall_status": snapshot.overall_status.value,
                            "health_score": snapshot.health_score,
                            "metrics": {
                                metric_type.value: {
                                    "value": metric.value,
                                    "unit": metric.unit,
                                    "timestamp": metric.timestamp.isoformat(),
                                    "status": metric.status.value,
                                }
                                for metric_type, metric in snapshot.metrics.items()
                            },
                            "recommendations": snapshot.recommendations,
                        }
                    return jsonify(serializable_agents)
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting agent health: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/alerts")
        def health_alerts():
            """Get health alerts"""
            try:
                if self.health_monitor:
                    severity_filter = request.args.get("severity")
                    agent_filter = request.args.get("agent_id")

                    alerts = self.health_monitor.get_health_alerts(
                        severity=severity_filter, agent_id=agent_filter
                    )

                    # Convert to serializable format
                    serializable_alerts = []
                    for alert in alerts:
                        serializable_alerts.append(
                            {
                                "alert_id": alert.alert_id,
                                "agent_id": alert.agent_id,
                                "severity": alert.severity.value,
                                "message": alert.message,
                                "metric_type": alert.metric_type.value,
                                "current_value": alert.current_value,
                                "threshold": alert.threshold,
                                "timestamp": alert.timestamp.isoformat(),
                                "acknowledged": alert.acknowledged,
                                "resolved": alert.resolved,
                            }
                        )

                    return jsonify(serializable_alerts)
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting health alerts: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/alerts/<alert_id>/acknowledge", methods=["POST"])
        def acknowledge_alert(alert_id):
            """Acknowledge a health alert"""
            try:
                if self.health_monitor:
                    self.health_monitor.acknowledge_alert(alert_id)
                    return jsonify(
                        {"success": True, "message": f"Alert {alert_id} acknowledged"}
                    )
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error acknowledging alert: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/alerts/<alert_id>/resolve", methods=["POST"])
        def resolve_alert(alert_id):
            """Resolve a health alert"""
            try:
                if self.health_monitor:
                    self.health_monitor.resolve_alert(alert_id)
                    return jsonify(
                        {"success": True, "message": f"Alert {alert_id} resolved"}
                    )
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error resolving alert: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/metrics/<agent_id>")
        def agent_metrics(agent_id):
            """Get detailed metrics for a specific agent"""
            try:
                if self.health_monitor:
                    health = self.health_monitor.get_agent_health(agent_id)
                    if health:
                        # Convert to serializable format
                        serializable_health = {
                            "agent_id": health.agent_id,
                            "timestamp": health.timestamp.isoformat(),
                            "overall_status": health.overall_status.value,
                            "health_score": health.health_score,
                            "metrics": {
                                metric_type.value: {
                                    "value": metric.value,
                                    "unit": metric.unit,
                                    "timestamp": metric.timestamp.isoformat(),
                                    "status": metric.status.value,
                                }
                                for metric_type, metric in health.metrics.items()
                            },
                            "recommendations": health.recommendations,
                        }
                        return jsonify(serializable_health)
                    else:
                        return jsonify({"error": "Agent not found"}), 404
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting agent metrics: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/thresholds")
        def get_thresholds():
            """Get health thresholds configuration"""
            try:
                if self.health_monitor and hasattr(self.health_monitor, "thresholds"):
                    thresholds = {}
                    for (
                        metric_type,
                        threshold,
                    ) in self.health_monitor.thresholds.items():
                        thresholds[metric_type.value] = {
                            "warning_threshold": threshold.warning_threshold,
                            "critical_threshold": threshold.critical_threshold,
                            "unit": threshold.unit,
                            "description": threshold.description,
                        }
                    return jsonify(thresholds)
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting thresholds: {e}")
                return jsonify({"error": str(e)}), 500

        @self.app.route("/api/health/status")
        def health_status():
            """Get overall health monitoring status"""
            try:
                if self.health_monitor:
                    status = {
                        "monitoring_active": self.health_monitor.monitoring_active,
                        "total_agents": len(self.health_monitor.health_data)
                        if hasattr(self.health_monitor, "health_data")
                        else 0,
                        "active_alerts": len(
                            [
                                a
                                for a in self.health_monitor.alerts.values()
                                if not a.resolved
                            ]
                        )
                        if hasattr(self.health_monitor, "alerts")
                        else 0,
                        "last_update": datetime.now().isoformat(),
                    }
                    return jsonify(status)
                else:
                    return jsonify({"error": "Health monitor not available"}), 500
            except Exception as e:
                logger.error(f"Error getting health status: {e}")
                return jsonify({"error": str(e)}), 500

    def _setup_websocket_events(self):
        """Setup WebSocket events for real-time updates"""

        @self.socketio.on("connect")
        def handle_connect():
            """Handle client connection"""
            logger.info(f"Client connected: {request.sid}")
            emit("connected", {"message": "Connected to health monitor"})

        @self.socketio.on("disconnect")
        def handle_disconnect():
            """Handle client disconnection"""
            logger.info(f"Client disconnected: {request.sid}")

        @self.socketio.on("subscribe_to_health_updates")
        def handle_subscription(data):
            """Handle health update subscription"""
            logger.info(f"Client {request.sid} subscribed to health updates")
            emit("subscription_confirmed", {"message": "Subscribed to health updates"})

        @self.socketio.on("request_health_update")
        def handle_health_update_request():
            """Handle manual health update request"""
            if self.health_monitor:
                try:
                    summary = self.health_monitor.get_health_summary()
                    emit("health_update", summary)
                except Exception as e:
                    logger.error(f"Error sending health update: {e}")
                    emit("error", {"message": str(e)})

    def _on_health_update(self, health_data, alerts):
        """Handle health updates from the monitor"""
        try:
            # Prepare update data
            update_data = {
                "timestamp": datetime.now().isoformat(),
                "health_summary": self.health_monitor.get_health_summary()
                if self.health_monitor
                else {},
                "active_alerts": len([a for a in alerts if not a.resolved])
                if alerts
                else 0,
            }

            # Broadcast to all connected clients
            self.socketio.emit("health_update", update_data)

        except Exception as e:
            logger.error(f"Error broadcasting health update: {e}")

    def start(self):
        """Start the web interface"""
        if self.running:
            logger.warning("Web interface already running")
            return

        self.running = True

        # Subscribe to health updates if monitor is available
        if self.health_monitor:
            self.health_monitor.subscribe_to_health_updates(self._on_health_update)

        # Start update thread
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

        logger.info("Health monitor web interface started")

    def stop(self):
        """Stop the web interface"""
        self.running = False

        # Unsubscribe from health updates
        if self.health_monitor:
            self.health_monitor.unsubscribe_from_health_updates(self._on_health_update)

        if self.update_thread:
            self.update_thread.join(timeout=5)

        logger.info("Health monitor web interface stopped")

    def _update_loop(self):
        """Main update loop for periodic data refresh"""
        while self.running:
            try:
                time.sleep(self.update_interval)

                # Send periodic updates to connected clients
                if self.health_monitor:
                    try:
                        summary = self.health_monitor.get_health_summary()
                        self.socketio.emit("periodic_update", summary)
                    except Exception as e:
                        logger.error(f"Error sending periodic update: {e}")

            except Exception as e:
                logger.error(f"Error in update loop: {e}")
                time.sleep(10)  # Wait before retrying

    def run(
        self, host: str = "127.0.0.1", port: int = 5001, debug: bool = False
    ):  # SECURITY: Localhost only
        """Run the Flask application"""
        try:
            logger.info(f"Starting health monitor web interface on {host}:{port}")
            self.socketio.run(self.app, host=host, port=port, debug=debug)
        except Exception as e:
            logger.error(f"Error running web interface: {e}")
            raise

    def run_smoke_test(self) -> bool:
        """Run smoke test to verify basic functionality"""
        try:
            logger.info("Running HealthMonitorWebInterface smoke test...")

            # Test basic initialization
            assert self.app is not None
            assert self.socketio is not None
            assert self.running is False

            # Test route setup
            routes = [rule.rule for rule in self.app.url_map.iter_rules()]
            expected_routes = [
                "/",
                "/api/health/summary",
                "/api/health/agents",
                "/api/health/alerts",
            ]

            for route in expected_routes:
                assert route in routes, f"Route {route} not found"

            logger.info("✅ HealthMonitorWebInterface smoke test PASSED")
            return True

        except Exception as e:
            logger.error(f"❌ HealthMonitorWebInterface smoke test FAILED: {e}")
            return False

    def shutdown(self):
        """Shutdown the web interface"""
        self.stop()
        logger.info("HealthMonitorWebInterface shutdown complete")


def main():
    """CLI testing function"""
    import argparse

    parser = argparse.ArgumentParser(description="Health Monitor Web Interface CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument(
        "--host", default="127.0.0.1", help="Host to bind to (SECURITY: Localhost only)"
    )
    parser.add_argument("--port", type=int, default=5001, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    if args.test:
        interface = HealthMonitorWebInterface()
        success = interface.run_smoke_test()
        interface.shutdown()
        exit(0 if success else 1)

    else:
        print("🚀 Starting Health Monitor Web Interface...")
        interface = HealthMonitorWebInterface()

        try:
            interface.run(host=args.host, port=args.port, debug=args.debug)
        except KeyboardInterrupt:
            print("\n⏹️ Web interface interrupted by user")
        finally:
            interface.shutdown()
            print("✅ Web interface shutdown complete")


if __name__ == "__main__":
    main()
