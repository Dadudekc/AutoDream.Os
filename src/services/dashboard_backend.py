"""
Dashboard Backend for Agent_Cellphone_V2_Repository
Real-time dashboard backend with REST API and WebSocket support.
"""

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path
import uuid
import aiohttp
from aiohttp import web, WSMsgType
import weakref

# Import from our performance monitor
from .performance_monitor import PerformanceMonitor, MetricData, MetricSeries

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DashboardRoute(Enum):
    """Dashboard API routes."""

    METRICS = "/api/metrics"
    HEALTH = "/api/health"
    STATUS = "/api/status"
    ALERTS = "/api/alerts"
    COLLECTORS = "/api/collectors"
    WEBSOCKET = "/ws"


@dataclass
class DashboardEndpoint:
    """Dashboard API endpoint definition."""

    path: str
    method: str
    handler: Callable
    description: str = ""
    requires_auth: bool = False


@dataclass
class WebSocketConnection:
    """WebSocket connection wrapper."""

    connection_id: str
    websocket: web.WebSocketResponse
    subscriptions: List[str] = field(default_factory=list)
    last_ping: float = field(default_factory=time.time)

    async def send_json(self, data: Dict[str, Any]):
        """Send JSON data to WebSocket client."""
        try:
            await self.websocket.send_str(json.dumps(data))
        except Exception as e:
            logger.error(f"Error sending WebSocket message: {e}")

    async def ping(self):
        """Send ping to keep connection alive."""
        try:
            await self.websocket.ping()
            self.last_ping = time.time()
        except Exception as e:
            logger.error(f"Error pinging WebSocket: {e}")


class DashboardAPI:
    """REST API handlers for dashboard."""

    def __init__(self, performance_monitor: PerformanceMonitor):
        self.performance_monitor = performance_monitor

    async def get_metrics(self, request: web.Request) -> web.Response:
        """Get metrics data."""
        try:
            # Parse query parameters
            metric_name = request.query.get("metric_name")
            start_time = request.query.get("start_time")
            end_time = request.query.get("end_time")
            aggregation = request.query.get("aggregation", "raw")

            # Convert time parameters
            start_time_float = float(start_time) if start_time else None
            end_time_float = float(end_time) if end_time else None

            if metric_name:
                # Get specific metric
                if aggregation == "raw":
                    series = self.performance_monitor.get_metric_series(
                        metric_name, start_time_float, end_time_float
                    )
                    if series:
                        data = {
                            "metric_name": series.metric_name,
                            "metric_type": series.metric_type.value,
                            "data_points": [
                                {
                                    "value": point.value,
                                    "timestamp": point.timestamp,
                                    "tags": point.tags,
                                    "unit": point.unit,
                                }
                                for point in series.data_points
                            ],
                            "unit": series.unit,
                            "description": series.description,
                        }
                    else:
                        data = None
                else:
                    # Get aggregated metric
                    value = self.performance_monitor.aggregate_metrics(
                        metric_name, aggregation, start_time_float, end_time_float
                    )
                    data = {
                        "metric_name": metric_name,
                        "aggregation": aggregation,
                        "value": value,
                        "start_time": start_time_float,
                        "end_time": end_time_float,
                    }
            else:
                # Get all metric names
                metric_names = (
                    self.performance_monitor.metrics_storage.get_all_metric_names()
                )
                data = {"metrics": metric_names}

            return web.json_response(
                {"status": "success", "data": data, "timestamp": time.time()}
            )

        except Exception as e:
            logger.error(f"Error in get_metrics: {e}")
            return web.json_response(
                {"status": "error", "message": str(e), "timestamp": time.time()},
                status=500,
            )

    async def get_health(self, request: web.Request) -> web.Response:
        """Get system health status."""
        try:
            status = self.performance_monitor.get_system_status()
            return web.json_response(
                {"status": "success", "data": status, "timestamp": time.time()}
            )

        except Exception as e:
            logger.error(f"Error in get_health: {e}")
            return web.json_response(
                {"status": "error", "message": str(e), "timestamp": time.time()},
                status=500,
            )

    async def get_status(self, request: web.Request) -> web.Response:
        """Get dashboard status."""
        try:
            data = {
                "dashboard_running": True,
                "performance_monitor_running": self.performance_monitor.running,
                "collectors_count": len(self.performance_monitor.collectors),
                "active_alerts": len(self.performance_monitor.active_alerts),
                "uptime": time.time() - getattr(self, "start_time", time.time()),
            }

            return web.json_response(
                {"status": "success", "data": data, "timestamp": time.time()}
            )

        except Exception as e:
            logger.error(f"Error in get_status: {e}")
            return web.json_response(
                {"status": "error", "message": str(e), "timestamp": time.time()},
                status=500,
            )

    async def get_alerts(self, request: web.Request) -> web.Response:
        """Get active alerts."""
        try:
            alerts_data = []
            for alert_id, alert in self.performance_monitor.active_alerts.items():
                alerts_data.append(
                    {
                        "alert_id": alert.alert_id,
                        "rule_name": alert.rule_name,
                        "metric_name": alert.metric_name,
                        "current_value": alert.current_value,
                        "threshold": alert.threshold,
                        "severity": alert.severity.value,
                        "message": alert.message,
                        "timestamp": alert.timestamp,
                        "tags": alert.tags,
                        "resolved": alert.resolved,
                    }
                )

            return web.json_response(
                {
                    "status": "success",
                    "data": {"alerts": alerts_data},
                    "timestamp": time.time(),
                }
            )

        except Exception as e:
            logger.error(f"Error in get_alerts: {e}")
            return web.json_response(
                {"status": "error", "message": str(e), "timestamp": time.time()},
                status=500,
            )

    async def get_collectors(self, request: web.Request) -> web.Response:
        """Get metrics collectors status."""
        try:
            collectors_data = []
            for collector in self.performance_monitor.collectors:
                collectors_data.append(
                    {
                        "name": collector.__class__.__name__,
                        "enabled": collector.enabled,
                        "collection_interval": collector.collection_interval,
                        "running": collector.running,
                    }
                )

            return web.json_response(
                {
                    "status": "success",
                    "data": {"collectors": collectors_data},
                    "timestamp": time.time(),
                }
            )

        except Exception as e:
            logger.error(f"Error in get_collectors: {e}")
            return web.json_response(
                {"status": "error", "message": str(e), "timestamp": time.time()},
                status=500,
            )


class DashboardWebSocket:
    """WebSocket handler for real-time updates."""

    def __init__(self, dashboard_backend: "DashboardBackend"):
        self.dashboard_backend = dashboard_backend
        self.connections: Dict[str, WebSocketConnection] = {}

    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        """Handle WebSocket connections."""
        ws = web.WebSocketResponse(heartbeat=30)
        await ws.prepare(request)

        connection_id = str(uuid.uuid4())
        connection = WebSocketConnection(connection_id=connection_id, websocket=ws)

        self.connections[connection_id] = connection
        logger.info(f"WebSocket connection established: {connection_id}")

        try:
            # Send initial connection message
            await connection.send_json(
                {
                    "type": "connection",
                    "connection_id": connection_id,
                    "timestamp": time.time(),
                    "message": "Connected to dashboard",
                }
            )

            # Handle incoming messages
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        data = json.loads(msg.data)
                        await self._handle_websocket_message(connection, data)
                    except json.JSONDecodeError as e:
                        await connection.send_json(
                            {
                                "type": "error",
                                "message": f"Invalid JSON: {e}",
                                "timestamp": time.time(),
                            }
                        )
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break

        except Exception as e:
            logger.error(f"Error in WebSocket handler: {e}")

        finally:
            # Clean up connection
            if connection_id in self.connections:
                del self.connections[connection_id]
            logger.info(f"WebSocket connection closed: {connection_id}")

        return ws

    async def _handle_websocket_message(
        self, connection: WebSocketConnection, data: Dict[str, Any]
    ):
        """Handle incoming WebSocket messages."""
        message_type = data.get("type")

        if message_type == "subscribe":
            # Subscribe to metric updates
            metric_name = data.get("metric_name")
            if metric_name and metric_name not in connection.subscriptions:
                connection.subscriptions.append(metric_name)
                await connection.send_json(
                    {
                        "type": "subscription_confirmed",
                        "metric_name": metric_name,
                        "timestamp": time.time(),
                    }
                )

        elif message_type == "unsubscribe":
            # Unsubscribe from metric updates
            metric_name = data.get("metric_name")
            if metric_name in connection.subscriptions:
                connection.subscriptions.remove(metric_name)
                await connection.send_json(
                    {
                        "type": "subscription_removed",
                        "metric_name": metric_name,
                        "timestamp": time.time(),
                    }
                )

        elif message_type == "get_metrics":
            # Send current metrics
            metric_names = data.get("metric_names", [])
            if not metric_names:
                metric_names = (
                    self.dashboard_backend.performance_monitor.metrics_storage.get_all_metric_names()
                )

            metrics_data = {}
            for metric_name in metric_names:
                series = self.dashboard_backend.performance_monitor.get_metric_series(
                    metric_name
                )
                if series and series.data_points:
                    # Send only the latest data point
                    latest_point = series.data_points[-1]
                    metrics_data[metric_name] = {
                        "value": latest_point.value,
                        "timestamp": latest_point.timestamp,
                        "unit": latest_point.unit,
                        "tags": latest_point.tags,
                    }

            await connection.send_json(
                {"type": "metrics_data", "data": metrics_data, "timestamp": time.time()}
            )

        elif message_type == "ping":
            # Respond to ping
            await connection.send_json({"type": "pong", "timestamp": time.time()})

    async def broadcast_metrics_update(self, metrics: List[MetricData]):
        """Broadcast metrics update to subscribed clients."""
        if not self.connections:
            return

        # Group metrics by name
        metrics_by_name = {}
        for metric in metrics:
            metrics_by_name[metric.metric_name] = {
                "value": metric.value,
                "timestamp": metric.timestamp,
                "unit": metric.unit,
                "tags": metric.tags,
            }

        # Send to subscribed connections
        disconnected_connections = []
        for connection_id, connection in self.connections.items():
            try:
                # Check if connection is still alive
                if connection.websocket.closed:
                    disconnected_connections.append(connection_id)
                    continue

                # Send metrics for subscribed metric names
                relevant_metrics = {}
                for metric_name in connection.subscriptions:
                    if metric_name in metrics_by_name:
                        relevant_metrics[metric_name] = metrics_by_name[metric_name]

                if relevant_metrics:
                    await connection.send_json(
                        {
                            "type": "metrics_update",
                            "data": relevant_metrics,
                            "timestamp": time.time(),
                        }
                    )

            except Exception as e:
                logger.error(f"Error broadcasting to connection {connection_id}: {e}")
                disconnected_connections.append(connection_id)

        # Clean up disconnected connections
        for connection_id in disconnected_connections:
            if connection_id in self.connections:
                del self.connections[connection_id]
                logger.info(
                    f"Removed disconnected WebSocket connection: {connection_id}"
                )

    async def broadcast_alert(self, alert):
        """Broadcast alert to all connected clients."""
        alert_data = {
            "alert_id": alert.alert_id,
            "rule_name": alert.rule_name,
            "metric_name": alert.metric_name,
            "current_value": alert.current_value,
            "threshold": alert.threshold,
            "severity": alert.severity.value,
            "message": alert.message,
            "timestamp": alert.timestamp,
            "tags": alert.tags,
        }

        disconnected_connections = []
        for connection_id, connection in self.connections.items():
            try:
                if connection.websocket.closed:
                    disconnected_connections.append(connection_id)
                    continue

                await connection.send_json(
                    {"type": "alert", "data": alert_data, "timestamp": time.time()}
                )

            except Exception as e:
                logger.error(
                    f"Error broadcasting alert to connection {connection_id}: {e}"
                )
                disconnected_connections.append(connection_id)

        # Clean up disconnected connections
        for connection_id in disconnected_connections:
            if connection_id in self.connections:
                del self.connections[connection_id]


class DashboardBackend:
    """Main dashboard backend server."""

    def __init__(
        self,
        performance_monitor: PerformanceMonitor,
        host: str = "0.0.0.0",
        port: int = 8080,
    ):
        self.performance_monitor = performance_monitor
        self.host = host
        self.port = port
        self.running = False
        self.start_time = time.time()

        # Web application
        self.app = web.Application()
        self.api = DashboardAPI(performance_monitor)
        self.websocket_handler = DashboardWebSocket(self)

        # API endpoints
        self.api_endpoints: List[DashboardEndpoint] = []
        self.websocket_connections: List[WebSocketConnection] = []

        # Register default endpoints
        self._register_default_endpoints()

        # Register callback for real-time updates
        self.performance_monitor.metric_callbacks.append(self._on_metric_recorded)
        self.performance_monitor.alert_callbacks.append(self._on_alert_triggered)

        logger.info(f"Dashboard backend initialized on {host}:{port}")

    def _register_default_endpoints(self):
        """Register default API endpoints."""
        endpoints = [
            DashboardEndpoint(
                "/api/metrics", "GET", self.api.get_metrics, "Get metrics data"
            ),
            DashboardEndpoint(
                "/api/health", "GET", self.api.get_health, "Get system health"
            ),
            DashboardEndpoint(
                "/api/status", "GET", self.api.get_status, "Get dashboard status"
            ),
            DashboardEndpoint(
                "/api/alerts", "GET", self.api.get_alerts, "Get active alerts"
            ),
            DashboardEndpoint(
                "/api/collectors",
                "GET",
                self.api.get_collectors,
                "Get collectors status",
            ),
        ]

        for endpoint in endpoints:
            self.register_endpoint(endpoint)

        # Register WebSocket endpoint
        self.app.router.add_get("/ws", self.websocket_handler.handle_websocket)

        # Register static files (for dashboard frontend)
        self.app.router.add_static("/", path="static", name="static")

    def register_endpoint(self, endpoint: DashboardEndpoint):
        """Register an API endpoint."""
        if endpoint.method.upper() == "GET":
            self.app.router.add_get(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "POST":
            self.app.router.add_post(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "PUT":
            self.app.router.add_put(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "DELETE":
            self.app.router.add_delete(endpoint.path, endpoint.handler)

        self.api_endpoints.append(endpoint)
        logger.info(f"Registered API endpoint: {endpoint.method} {endpoint.path}")

    async def add_websocket_connection(self, websocket):
        """Add WebSocket connection."""
        # This is handled by the WebSocket handler
        pass

    async def remove_websocket_connection(self, websocket):
        """Remove WebSocket connection."""
        # This is handled by the WebSocket handler
        pass

    async def broadcast_metrics_update(self, metrics: List[MetricData]):
        """Broadcast metrics update to WebSocket clients."""
        await self.websocket_handler.broadcast_metrics_update(metrics)

    def _on_metric_recorded(self, metric_data: MetricData):
        """Callback for when a metric is recorded."""
        # Create a task to broadcast the update
        if self.running:
            asyncio.create_task(self.broadcast_metrics_update([metric_data]))

    def _on_alert_triggered(self, alert):
        """Callback for when an alert is triggered."""
        # Create a task to broadcast the alert
        if self.running:
            asyncio.create_task(self.websocket_handler.broadcast_alert(alert))

    async def start(self):
        """Start the dashboard backend server."""
        if self.running:
            logger.warning("Dashboard backend is already running")
            return

        self.running = True
        self.start_time = time.time()

        # Start the web server
        runner = web.AppRunner(self.app)
        await runner.setup()

        site = web.TCPSite(runner, self.host, self.port)
        await site.start()

        logger.info(f"Dashboard backend started on http://{self.host}:{self.port}")

    async def stop(self):
        """Stop the dashboard backend server."""
        if not self.running:
            return

        self.running = False

        # Close all WebSocket connections
        for connection in list(self.websocket_handler.connections.values()):
            try:
                await connection.websocket.close()
            except Exception as e:
                logger.error(f"Error closing WebSocket connection: {e}")

        logger.info("Dashboard backend stopped")

    def get_metrics_endpoint(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get metrics endpoint (for testing)."""
        metric_name = params.get("metric_name")
        start_time = params.get("start_time")
        end_time = params.get("end_time")

        if metric_name:
            start_time_float = float(start_time) if start_time else None
            end_time_float = float(end_time) if end_time else None

            series = self.performance_monitor.get_metric_series(
                metric_name, start_time_float, end_time_float
            )

            if series:
                data = [
                    {
                        "value": point.value,
                        "timestamp": point.timestamp,
                        "tags": point.tags,
                        "unit": point.unit,
                    }
                    for point in series.data_points
                ]
            else:
                data = []
        else:
            data = self.performance_monitor.metrics_storage.get_all_metric_names()

        return {"status": "success", "data": data, "timestamp": time.time()}


# Export all classes
__all__ = [
    "DashboardRoute",
    "DashboardEndpoint",
    "WebSocketConnection",
    "DashboardAPI",
    "DashboardWebSocket",
    "DashboardBackend",
]
