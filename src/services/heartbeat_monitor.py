#!/usr/bin/env python3
"""
Heartbeat Monitor Service
=========================
Monitors agent heartbeats and system health status.
Follows 100 LOC limit and single responsibility principle.
"""

import logging
import time
import threading
import os

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, Any, Optional
from dataclasses import dataclass

from ..core.agent_manager import AgentManager, AgentStatus

logger = logging.getLogger(__name__)


@dataclass
class SystemStatus:
    """System operational status"""

    total_agents: int
    online_agents: int
    message_queue_size: int
    uptime: float
    last_heartbeat: float


class HeartbeatMonitor:
    """Monitors agent heartbeats and system health"""

    def __init__(self, agent_manager: AgentManager):
        self.agent_manager = agent_manager
        self.start_time = time.time()
        self.logger = logging.getLogger(f"{__name__}.HeartbeatMonitor")

        # Heartbeat configuration
        self._heartbeat_interval = float(
            os.environ.get("ACP_HEARTBEAT_SEC", "60") or 60
        )
        self._hb_stop = threading.Event()
        self._hb_thread: Optional[threading.Thread] = None

        self._start_heartbeat()

    def _start_heartbeat(self):
        """Start heartbeat monitoring thread"""
        if self._heartbeat_interval > 0:
            self._hb_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self._hb_thread.start()
            self.logger.info("Heartbeat monitoring started")

    def _heartbeat_loop(self):
        """Heartbeat monitoring loop"""
        while not self._hb_stop.is_set():
            try:
                self._emit_heartbeat()
                time.sleep(self._heartbeat_interval)
            except Exception as e:
                self.logger.error(f"Heartbeat error: {e}")
                time.sleep(5)

    def _emit_heartbeat(self):
        """Emit heartbeat for all online agents"""
        try:
            for agent_id in self.agent_manager.get_all_agents():
                if self.agent_manager.get_agent_status(agent_id) == AgentStatus.ONLINE:
                    self.agent_manager.update_agent_metadata(
                        agent_id, {"last_heartbeat": time.time()}
                    )
        except Exception as e:
            self.logger.error(f"Error emitting heartbeat: {e}")

    def get_system_status(self) -> SystemStatus:
        """Get comprehensive system status"""
        try:
            agents = self.agent_manager.get_all_agents()
            online_count = sum(
                1 for a in agents.values() if a.status == AgentStatus.ONLINE
            )
            return SystemStatus(
                total_agents=len(agents),
                online_agents=online_count,
                message_queue_size=0,
                uptime=time.time() - self.start_time,
                last_heartbeat=time.time(),
            )
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return SystemStatus(0, 0, 0, 0, 0)

    def stop(self):
        """Stop heartbeat monitoring"""
        self._hb_stop.set()
        if self._hb_thread and self._hb_thread.is_alive():
            self._hb_thread.join(timeout=1)
        self.logger.info("Heartbeat monitoring stopped")


if __name__ == "__main__":
    print("HeartbeatMonitor ready - use as imported service")
