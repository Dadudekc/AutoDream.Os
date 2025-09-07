"""Routing handlers for the dashboard service."""
from __future__ import annotations

import json
import logging
import uuid
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List

from aiohttp import WSMsgType, web

from . import data, formatting
from ..performance_monitor import MetricData, PerformanceMonitor

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

    async def send_json(self, payload: Dict[str, Any]) -> None:
        await self.websocket.send_str(json.dumps(payload))

    async def ping(self) -> None:
        await self.websocket.ping()
        self.last_ping = time.time()


class DashboardAPI:
    """REST API handlers for dashboard."""

    def __init__(self, performance_monitor: PerformanceMonitor):
        self.performance_monitor = performance_monitor

    async def get_metrics(self, request: web.Request) -> web.Response:
        try:
            metric_name = request.query.get("metric_name")
            start_time = request.query.get("start_time")
            end_time = request.query.get("end_time")
            aggregation = request.query.get("aggregation", "raw")
            payload = data.get_metrics(
                self.performance_monitor,
                metric_name,
                start_time,
                end_time,
                aggregation,
            )
            return web.json_response(formatting.success(payload))
        except Exception as exc:  # pragma: no cover - logging
            logger.error(f"Error in get_metrics: {exc}")
            return web.json_response(formatting.error(str(exc)), status=500)

    async def get_health(self, request: web.Request) -> web.Response:
        try:
            payload = data.get_health(self.performance_monitor)
            return web.json_response(formatting.success(payload))
        except Exception as exc:  # pragma: no cover - logging
            logger.error(f"Error in get_health: {exc}")
            return web.json_response(formatting.error(str(exc)), status=500)

    async def get_status(self, request: web.Request) -> web.Response:
        try:
            backend = request.app.get("backend")
            start_time = backend.start_time if backend else time.time()
            payload = data.get_status(self.performance_monitor, start_time)
            return web.json_response(formatting.success(payload))
        except Exception as exc:  # pragma: no cover - logging
            logger.error(f"Error in get_status: {exc}")
            return web.json_response(formatting.error(str(exc)), status=500)

    async def get_alerts(self, request: web.Request) -> web.Response:
        try:
            payload = data.get_alerts(self.performance_monitor)
            return web.json_response(formatting.success(payload))
        except Exception as exc:  # pragma: no cover - logging
            logger.error(f"Error in get_alerts: {exc}")
            return web.json_response(formatting.error(str(exc)), status=500)

    async def get_collectors(self, request: web.Request) -> web.Response:
        try:
            payload = data.get_collectors(self.performance_monitor)
            return web.json_response(formatting.success(payload))
        except Exception as exc:  # pragma: no cover - logging
            logger.error(f"Error in get_collectors: {exc}")
            return web.json_response(formatting.error(str(exc)), status=500)


class DashboardWebSocket:
    """WebSocket handler for real-time updates."""

    def __init__(self, performance_monitor: PerformanceMonitor):
        self.performance_monitor = performance_monitor
        self.connections: Dict[str, WebSocketConnection] = {}

    async def handle_websocket(self, request: web.Request) -> web.WebSocketResponse:
        ws = web.WebSocketResponse(heartbeat=30)
        await ws.prepare(request)

        connection_id = str(uuid.uuid4())
        connection = WebSocketConnection(connection_id=connection_id, websocket=ws)
        self.connections[connection_id] = connection
        logger.info(f"WebSocket connection established: {connection_id}")

        await connection.send_json(
            formatting.websocket_message(
                "connection",
                {
                    "connection_id": connection_id,
                    "message": "Connected to dashboard",
                },
            )
        )

        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    try:
                        payload = json.loads(msg.data)
                        await self._handle_message(connection, payload)
                    except json.JSONDecodeError as exc:
                        await connection.send_json(
                            formatting.websocket_message(
                                "error", {"message": f"Invalid JSON: {exc}"}
                            )
                        )
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f"WebSocket error: {ws.exception()}")
                    break
        finally:
            self.connections.pop(connection_id, None)
            logger.info(f"WebSocket connection closed: {connection_id}")

        return ws

    async def _handle_message(
        self, connection: WebSocketConnection, payload: Dict[str, Any]
    ) -> None:
        message_type = payload.get("type")

        if message_type == "subscribe":
            metric_name = payload.get("metric_name")
            if metric_name and metric_name not in connection.subscriptions:
                connection.subscriptions.append(metric_name)
                await connection.send_json(
                    formatting.websocket_message(
                        "subscription_confirmed", {"metric_name": metric_name}
                    )
                )
        elif message_type == "unsubscribe":
            metric_name = payload.get("metric_name")
            if metric_name in connection.subscriptions:
                connection.subscriptions.remove(metric_name)
                await connection.send_json(
                    formatting.websocket_message(
                        "subscription_removed", {"metric_name": metric_name}
                    )
                )
        elif message_type == "get_metrics":
            metric_names = payload.get("metric_names", [])
            if not metric_names:
                metric_names = (
                    self.performance_monitor.metrics_storage.get_all_metric_names()
                )
            metrics_data = {}
            for name in metric_names:
                series = self.performance_monitor.get_metric_series(name)
                if series and series.data_points:
                    latest = series.data_points[-1]
                    metrics_data[name] = {
                        "value": latest.value,
                        "timestamp": latest.timestamp,
                        "unit": latest.unit,
                        "tags": latest.tags,
                    }
            await connection.send_json(
                formatting.websocket_message("metrics_data", metrics_data)
            )
        elif message_type == "ping":
            await connection.send_json(formatting.websocket_message("pong"))

    async def broadcast_metrics_update(self, metrics: List[MetricData]) -> None:
        if not self.connections:
            return

        metrics_by_name = {
            m.metric_name: {
                "value": m.value,
                "timestamp": m.timestamp,
                "unit": m.unit,
                "tags": m.tags,
            }
            for m in metrics
        }

        disconnected: List[str] = []
        for connection_id, connection in self.connections.items():
            if connection.websocket.closed:
                disconnected.append(connection_id)
                continue
            relevant = {
                name: metrics_by_name[name]
                for name in connection.subscriptions
                if name in metrics_by_name
            }
            if relevant:
                await connection.send_json(
                    formatting.websocket_message("metrics_update", relevant)
                )

        for connection_id in disconnected:
            self.connections.pop(connection_id, None)
            logger.info(f"Removed disconnected WebSocket connection: {connection_id}")

    async def broadcast_alert(self, alert: Any) -> None:
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

        disconnected: List[str] = []
        for connection_id, connection in self.connections.items():
            if connection.websocket.closed:
                disconnected.append(connection_id)
                continue
            await connection.send_json(
                formatting.websocket_message("alert", alert_data)
            )

        for connection_id in disconnected:
            self.connections.pop(connection_id, None)


def setup_routes(
    app: web.Application, performance_monitor: PerformanceMonitor
) -> DashboardWebSocket:
    """Register dashboard routes and return WebSocket handler."""
    api = DashboardAPI(performance_monitor)
    websocket = DashboardWebSocket(performance_monitor)

    endpoints = [
        DashboardEndpoint(DashboardRoute.METRICS.value, "GET", api.get_metrics),
        DashboardEndpoint(DashboardRoute.HEALTH.value, "GET", api.get_health),
        DashboardEndpoint(DashboardRoute.STATUS.value, "GET", api.get_status),
        DashboardEndpoint(DashboardRoute.ALERTS.value, "GET", api.get_alerts),
        DashboardEndpoint(DashboardRoute.COLLECTORS.value, "GET", api.get_collectors),
    ]

    for endpoint in endpoints:
        if endpoint.method.upper() == "GET":
            app.router.add_get(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "POST":
            app.router.add_post(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "PUT":
            app.router.add_put(endpoint.path, endpoint.handler)
        elif endpoint.method.upper() == "DELETE":
            app.router.add_delete(endpoint.path, endpoint.handler)

    app.router.add_get(DashboardRoute.WEBSOCKET.value, websocket.handle_websocket)
    app.router.add_static("/", path="static", name="static")
    return websocket
