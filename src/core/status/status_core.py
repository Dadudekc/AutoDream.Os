#!/usr/bin/env python3
"""
Status Core - Agent Cellphone V2
================================

Main live status system class.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import threading
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable

from .status_types import (
    UpdateFrequency,
    StatusEventType,
    StatusEvent,
    StatusMetrics,
    ActivitySummary,
)
from ..monitor import AgentStatusMonitor, AgentStatus


class LiveStatusSystem:
    """
    Implements live status update mechanisms and continuous visibility
    """

    def __init__(
        self, update_frequency: UpdateFrequency = UpdateFrequency.HIGH_FREQUENCY
    ):
        self.logger = logging.getLogger(f"{__name__}.LiveStatusSystem")
        self.workspace_path = Path("agent_workspaces")
        self.update_frequency = update_frequency
        self.is_active = False
        self.update_thread: Optional[threading.Thread] = None
        self.status_monitor = AgentStatusMonitor()
        self.status_subscribers: Dict[str, List[Callable]] = {}
        self.status_events: List[StatusEvent] = []
        self.last_status_snapshot: Dict[str, Any] = {}
        self.status_callbacks: List[Callable] = []

        self.workspace_path.mkdir(exist_ok=True)
        self._set_update_interval()

    def _set_update_interval(self):
        """Set update interval based on frequency setting"""
        interval_map = {
            UpdateFrequency.REAL_TIME: 1.0,
            UpdateFrequency.HIGH_FREQUENCY: 5.0,
            UpdateFrequency.MEDIUM_FREQUENCY: 15.0,
            UpdateFrequency.LOW_FREQUENCY: 60.0,
        }
        self.update_interval = interval_map.get(self.update_frequency, 5.0)
        self.status_monitor.update_interval = self.update_interval

    def start_live_updates(self):
        """Start live status update system"""
        if self.is_active:
            self.logger.warning("Live status system already active")
            return

        self.is_active = True
        self.status_monitor.start_monitoring()

        self.update_thread = threading.Thread(
            target=self._live_update_loop, daemon=True
        )
        self.update_thread.start()

        self.status_monitor.add_monitoring_callback(self._on_status_update)

        self.logger.info(
            f"Live status system started - updates every {self.update_interval} seconds"
        )
        print("🚀 LIVE STATUS UPDATE SYSTEM ACTIVATED!")
        print(f"📊 Status updates every {self.update_interval} seconds")
        print("👁️ Continuous agent visibility enabled")

    def stop_live_updates(self):
        """Stop live status update system"""
        self.is_active = False
        self.status_monitor.stop_monitoring()

        if self.update_thread:
            self.update_thread.join(timeout=5)

        self.logger.info("⏹️ Live status system stopped")
        print("⏹️ Live status system stopped")

    def _live_update_loop(self):
        """Main live update loop"""
        while self.is_active:
            try:
                self._process_live_updates()
                self._generate_live_status_report()
                self._notify_status_subscribers()
                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Error in live update loop: {e}")
                time.sleep(10)  # Recovery pause

    def _process_live_updates(self):
        """Process live status updates"""
        current_status = self.status_monitor.get_current_status()

        if self.last_status_snapshot:
            self._detect_status_changes(current_status)

        self.last_status_snapshot = current_status.copy()

        for agent_id in self.status_monitor.agent_statuses.keys():
            agent_status = self.status_monitor.get_agent_status(agent_id)
            if agent_status:
                self._process_agent_status_update(agent_status, time.time())

    def _detect_status_changes(self, current_status: Dict[str, Any]):
        """Detect and process status changes"""
        old_status = self.last_status_snapshot
        changes = [
            ("total_agents", "Agent count", "high"),
            ("online_agents", "Online agents", "medium"),
        ]

        for key, description, priority in changes:
            old_val, new_val = old_status.get(key, 0), current_status.get(key, 0)
            if old_val != new_val:
                self._create_status_event(
                    StatusEventType.STATUS_CHANGE,
                    "system",
                    f"{description} changed from {old_val} to {new_val}",
                    {f"old_{key}": old_val, f"new_{key}": new_val},
                    priority,
                )

    def _process_agent_status_update(
        self, agent_status: Dict[str, Any], timestamp: float
    ):
        """Process individual agent status update"""
        agent_id, current_status = agent_status.get("agent_id"), agent_status.get(
            "status"
        )

        if agent_id in self.last_status_snapshot.get("agent_details", {}):
            old_status = self.last_status_snapshot["agent_details"][agent_id].get(
                "status"
            )
            if old_status != current_status:
                self._create_status_event(
                    StatusEventType.STATUS_CHANGE,
                    agent_id,
                    f"Status changed from {old_status} to {current_status}",
                    {"old_status": old_status, "new_status": current_status},
                    "medium",
                )
        performance_score = agent_status.get("performance_score", 0.0)
        if performance_score < 0.3:
            self._create_status_event(
                StatusEventType.HEALTH_ALERT,
                agent_id,
                f"Low performance score: {performance_score:.2f}",
                {"performance_score": performance_score, "threshold": 0.3},
                "high",
            )
        current_task = agent_status.get("current_task")
        if current_task:
            self._create_status_event(
                StatusEventType.TASK_UPDATE,
                agent_id,
                f"Current task: {current_task}",
                {"task": current_task, "status": current_status},
                "low",
            )

    def _create_status_event(
        self,
        event_type: StatusEventType,
        agent_id: str,
        description: str,
        details: Dict[str, Any],
        priority: str,
    ):
        """Create a new status event"""
        event = StatusEvent(
            event_id=f"event_{event_type.value}_{int(time.time())}_{agent_id}",
            event_type=event_type,
            agent_id=agent_id,
            timestamp=time.time(),
            old_status=None,
            new_status=None,
            details=details,
            priority=priority,
        )

        self.status_events.append(event)
        if len(self.status_events) > 1000:
            self.status_events = self.status_events[-1000:]
        self.logger.info(
            f"Status event created: {event_type.value} for {agent_id} - {description}"
        )

    def _generate_live_status_report(self):
        """Generate live status report"""
        live_report = {
            "timestamp": time.time(),
            "update_frequency": self.update_frequency.value,
            "update_interval": self.update_interval,
            "system_status": "LIVE_UPDATES_ACTIVE",
            "current_status": self.status_monitor.get_current_status(),
            "recent_events": self._get_recent_events(10),
            "agent_activity": self._get_agent_activity_summary(),
            "performance_metrics": self._get_performance_metrics(),
        }

        # Save report and add to history
        report_file = self.workspace_path / "live_status_report.json"
        with open(report_file, "w") as f:
            json.dump(live_report, f, indent=2)
        self.status_monitor.status_history.append(live_report)

    def _get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent status events"""
        recent_events = self.status_events[-limit:] if self.status_events else []
        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "agent_id": event.agent_id,
                "timestamp": event.timestamp,
                "description": f"{event.event_type.value} for {event.agent_id}",
                "priority": event.priority,
                "details": event.details,
            }
            for event in recent_events
        ]

    def _get_agent_activity_summary(self) -> Dict[str, Any]:
        """Get summary of agent activity"""
        agent_statuses = self.status_monitor.agent_statuses
        activity_summary = {
            "total_agents": len(agent_statuses),
            "status_distribution": {},
            "capability_summary": {},
            "performance_summary": {
                "average_score": 0.0,
                "high_performers": 0,
                "low_performers": 0,
            },
        }

        if agent_statuses:
            for agent_info in agent_statuses.values():
                status = agent_info.status.value
                activity_summary["status_distribution"][status] = (
                    activity_summary["status_distribution"].get(status, 0) + 1
                )
                for capability in agent_info.capabilities:
                    cap_value = capability.value
                    activity_summary["capability_summary"][cap_value] = (
                        activity_summary["capability_summary"].get(cap_value, 0) + 1
                    )

            scores = [
                agent_info.performance_score for agent_info in agent_statuses.values()
            ]
            activity_summary["performance_summary"]["average_score"] = sum(
                scores
            ) / len(scores)
            activity_summary["performance_summary"]["high_performers"] = sum(
                1 for score in scores if score >= 0.8
            )
            activity_summary["performance_summary"]["low_performers"] = sum(
                1 for score in scores if score < 0.3
            )

        return activity_summary

    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get system performance metrics"""
        agent_statuses = self.status_monitor.agent_statuses
        if not agent_statuses:
            return {"system_health": 0.0, "uptime": 0.0}

        # Calculate metrics
        online_agents = sum(
            1 for a in agent_statuses.values() if a.status != AgentStatus.OFFLINE
        )
        total_agents = len(agent_statuses)
        online_ratio = online_agents / total_agents if total_agents > 0 else 0.0
        avg_performance = (
            sum(a.performance_score for a in agent_statuses.values()) / total_agents
            if total_agents > 0
            else 0.0
        )
        system_health = (online_ratio * 0.6) + (avg_performance * 0.4)

        return {
            "system_health": system_health,
            "online_ratio": online_ratio,
            "average_performance": avg_performance,
            "total_agents": total_agents,
            "online_agents": online_agents,
        }

    def _on_status_update(self, status_update: Dict[str, Any]):
        """Callback for status monitor updates"""
        self._process_status_update(status_update)

        for callback in self.status_callbacks:
            try:
                callback(status_update)
            except Exception as e:
                self.logger.error(f"Status callback failed: {e}")

    def _process_status_update(self, status_update: Dict[str, Any]):
        """Process status update from monitor"""
        pass

    def _notify_status_subscribers(self):
        """Notify all status subscribers"""
        current_status = self.status_monitor.get_current_status()

        for subscriber_id, callbacks in self.status_subscribers.items():
            for callback in callbacks:
                try:
                    callback(current_status)
                except Exception as e:
                    self.logger.error(
                        f"Subscriber notification failed for {subscriber_id}: {e}"
                    )

    def subscribe_to_status_updates(self, subscriber_id: str, callback: Callable):
        """Subscribe to status updates"""
        if subscriber_id not in self.status_subscribers:
            self.status_subscribers[subscriber_id] = []
        self.status_subscribers[subscriber_id].append(callback)
        self.logger.info(f"Subscriber {subscriber_id} added to status updates")

    def unsubscribe_from_status_updates(
        self, subscriber_id: str, callback: Callable = None
    ):
        """Unsubscribe from status updates"""
        if subscriber_id in self.status_subscribers:
            if callback is None:
                del self.status_subscribers[subscriber_id]
            else:
                if callback in self.status_subscribers[subscriber_id]:
                    self.status_subscribers[subscriber_id].remove(callback)
                if not self.status_subscribers[subscriber_id]:
                    del self.status_subscribers[subscriber_id]
            self.logger.info(f"Subscriber {subscriber_id} removed from status updates")

    def add_status_callback(self, callback: Callable):
        """Add callback for status updates"""
        self.status_callbacks.append(callback)

    def remove_status_callback(self, callback: Callable):
        """Remove status callback"""
        if callback in self.status_callbacks:
            self.status_callbacks.remove(callback)

    def change_update_frequency(self, new_frequency: UpdateFrequency):
        """Change the update frequency"""
        self.update_frequency = new_frequency
        self._set_update_interval()
        self.logger.info(
            f"Update frequency changed to {new_frequency.value} ({self.update_interval}s)"
        )
        print(
            f"📊 Update frequency changed to {new_frequency.value} ({self.update_interval}s)"
        )

    def get_live_status(self) -> Dict[str, Any]:
        """Get current live status"""
        return {
            "system_active": self.is_active,
            "update_frequency": self.update_frequency.value,
            "update_interval": self.update_interval,
            "current_status": self.status_monitor.get_current_status(),
            "recent_events": len(self.status_events),
            "active_subscribers": len(self.status_subscribers),
            "status": "LIVE_STATUS_SYSTEM_ACTIVE",
        }

    def get_status_events(
        self, event_type: Optional[StatusEventType] = None, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get status events with optional filtering"""
        events = self.status_events
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        recent_events = events[-limit:] if events else []

        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type.value,
                "agent_id": event.agent_id,
                "timestamp": event.timestamp,
                "priority": event.priority,
                "details": event.details,
            }
            for event in recent_events
        ]
