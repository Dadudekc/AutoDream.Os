"""Entry point for the dashboard backend service."""
from __future__ import annotations

import asyncio
import logging
import time
from typing import Any, List

from aiohttp import web

from .performance_monitor import MetricData, PerformanceMonitor
from .dashboard import routes

logger = logging.getLogger(__name__)


class DashboardBackend:
    """Minimal dashboard backend server."""

    def __init__(
        self,
        performance_monitor: PerformanceMonitor,
        host: str = "0.0.0.0",
        port: int = 8080,
    ) -> None:
        self.performance_monitor = performance_monitor
        self.host = host
        self.port = port
        self.running = False
        self.start_time = time.time()
        self.app = web.Application()
        self.websocket_handler = routes.setup_routes(self.app, performance_monitor)
        self.app["backend"] = self
        self.performance_monitor.metric_callbacks.append(self._on_metric_recorded)
        self.performance_monitor.alert_callbacks.append(self._on_alert_triggered)

    async def broadcast_metrics_update(self, metrics: List[MetricData]) -> None:
        await self.websocket_handler.broadcast_metrics_update(metrics)

    def _on_metric_recorded(self, metric_data: MetricData) -> None:
        if self.running:
            asyncio.create_task(self.broadcast_metrics_update([metric_data]))

    def _on_alert_triggered(self, alert: Any) -> None:
        if self.running:
            asyncio.create_task(self.websocket_handler.broadcast_alert(alert))

    async def start(self) -> None:
        if self.running:
            logger.warning("Dashboard backend is already running")
            return
        self.running = True
        self.start_time = time.time()
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        logger.info(f"Dashboard backend started on http://{self.host}:{self.port}")

    async def stop(self) -> None:
        if not self.running:
            return
        self.running = False
        for connection in list(self.websocket_handler.connections.values()):
            try:
                await connection.websocket.close()
            except Exception as exc:  # pragma: no cover - logging
                logger.error(f"Error closing WebSocket connection: {exc}")
        logger.info("Dashboard backend stopped")


__all__ = ["DashboardBackend"]
