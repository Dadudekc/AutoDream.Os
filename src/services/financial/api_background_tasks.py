from datetime import datetime, timedelta
from typing import TYPE_CHECKING
import asyncio
import logging

    from .unified_financial_api import UnifiedFinancialAPI


if TYPE_CHECKING:

logger = logging.getLogger(__name__)


class BackgroundTasks:
    """Run periodic maintenance tasks for UnifiedFinancialAPI."""

    def __init__(self, api: "UnifiedFinancialAPI") -> None:
        self.api = api

    def start(self) -> None:
        """Launch asynchronous background tasks."""
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:  # pragma: no cover - no event loop
            logger.error("Error starting background tasks: no running event loop")
            return

        loop.create_task(self.monitor_agent_heartbeats())
        loop.create_task(self.monitor_system_performance())
        loop.create_task(self.cleanup_old_data())
        logger.info("Background tasks started successfully")

    async def monitor_agent_heartbeats(self) -> None:
        """Monitor agent heartbeats and mark inactive ones."""
        while True:
            try:
                current_time = datetime.now()
                inactive_threshold = timedelta(minutes=5)
                for agent_id, agent in self.api.registered_agents.items():
                    if current_time - agent.last_heartbeat > inactive_threshold:
                        agent.status = "INACTIVE"
                        logger.warning("Agent %s marked as inactive", agent_id)
                await asyncio.sleep(30)
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error in heartbeat monitoring: %s", exc)
                await asyncio.sleep(60)

    async def monitor_system_performance(self) -> None:
        """Periodically update system performance metrics."""
        while True:
            try:
                self.api.update_system_health_metrics()
                await asyncio.sleep(60)
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error in performance monitoring: %s", exc)
                await asyncio.sleep(120)

    async def cleanup_old_data(self) -> None:
        """Purge stale request and performance data."""
        while True:
            try:
                if len(self.api.request_history) > 1000:
                    self.api.request_history = self.api.request_history[-1000:]

                cutoff_time = datetime.now() - timedelta(days=7)
                for agent_id in list(self.api.performance_metrics.keys()):
                    metrics = self.api.performance_metrics[agent_id]
                    last_updated = metrics.get("last_updated")
                    if last_updated:
                        ts = datetime.fromisoformat(last_updated)
                        if ts < cutoff_time:
                            del self.api.performance_metrics[agent_id]
                await asyncio.sleep(300)
            except Exception as exc:  # pragma: no cover - runtime safety
                logger.error("Error in cleanup task: %s", exc)
                await asyncio.sleep(600)
