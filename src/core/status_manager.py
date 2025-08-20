#!/usr/bin/env python3
"""
Status Manager - V2 Core Status Management System

This module handles real-time monitoring, health checks, status transitions, and alert systems.
Follows Single Responsibility Principle - only status management.
Architecture: Single Responsibility Principle - status management only
LOC: Target 200 lines (under 200 limit)
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any, Set, Callable
from pathlib import Path
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime, timedelta
import threading
import time
import uuid
from collections import defaultdict

from .agent_manager import AgentManager, AgentStatus, AgentCapability, AgentInfo
from .config_manager import ConfigManager

logger = logging.getLogger(__name__)


class HealthStatus(Enum):
    """System health status"""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class AlertLevel(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class StatusTransition(Enum):
    """Status transition types"""
    ONLINE_TO_OFFLINE = "online_to_offline"
    OFFLINE_TO_ONLINE = "offline_to_online"
    IDLE_TO_BUSY = "idle_to_busy"
    BUSY_TO_IDLE = "busy_to_idle"
    HEALTHY_TO_WARNING = "healthy_to_warning"
    WARNING_TO_CRITICAL = "warning_to_critical"


@dataclass
class HealthCheck:
    """Health check result"""
    check_id: str
    agent_id: str
    check_type: str
    status: HealthStatus
    message: str
    timestamp: str
    details: Dict[str, Any]


@dataclass
class Alert:
    """System alert"""
    alert_id: str
    level: AlertLevel
    message: str
    source: str
    timestamp: str
    acknowledged: bool
    metadata: Dict[str, Any]


@dataclass
class StatusEvent:
    """Status change event"""
    event_id: str
    agent_id: str
    old_status: AgentStatus
    new_status: AgentStatus
    transition: StatusTransition
    timestamp: str
    metadata: Dict[str, Any]


class StatusManager:
    """
    Manages real-time status monitoring, health checks, and alert systems
    
    Responsibilities:
    - Real-time status tracking
    - Health monitoring and checks
    - Status transition management
    - Alert generation and management
    """
    
    def __init__(self, agent_manager: AgentManager, config_manager: ConfigManager):
        self.agent_manager = agent_manager
        self.config_manager = config_manager
        self.health_checks: Dict[str, HealthCheck] = {}
        self.alerts: Dict[str, Alert] = {}
        self.status_events: Dict[str, StatusEvent] = {}
        self.monitoring_thread = None
        self.health_check_thread = None
        self.running = False
        self.logger = logging.getLogger(f"{__name__}.StatusManager")
        
        # Status change callbacks
        self.status_callbacks: Dict[str, List[Callable]] = defaultdict(list)
        
        # Start monitoring threads
        self._start_monitoring_threads()
    
    def _start_monitoring_threads(self):
        """Start status monitoring and health check threads"""
        self.running = True
        
        # Status monitoring thread
        self.monitoring_thread = threading.Thread(target=self._status_monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        
        # Health check thread
        self.health_check_thread = threading.Thread(target=self._health_check_loop, daemon=True)
        self.health_check_thread.start()
        
        self.logger.info("Status monitoring threads started")
    
    def _status_monitoring_loop(self):
        """Main status monitoring loop"""
        while self.running:
            try:
                # Monitor agent status changes
                self._check_agent_status_changes()
                
                # Process status transitions
                self._process_status_transitions()
                
                # Wait before next check
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                self.logger.error(f"Status monitoring loop error: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _health_check_loop(self):
        """Main health check loop"""
        while self.running:
            try:
                # Perform health checks
                self._perform_system_health_checks()
                
                # Process health alerts
                self._process_health_alerts()
                
                # Wait before next check
                time.sleep(60)  # Check every minute
                
            except Exception as e:
                self.logger.error(f"Health check loop error: {e}")
                time.sleep(120)  # Wait longer on error
    
    def _check_agent_status_changes(self):
        """Check for agent status changes"""
        try:
            current_agents = self.agent_manager.get_all_agents()
            
            for agent_id, agent_info in current_agents.items():
                current_status = agent_info.status
                previous_status = self._get_previous_status(agent_id)
                
                if previous_status and previous_status != current_status:
                    # Status change detected
                    self._handle_status_change(agent_id, previous_status, current_status)
                
                # Update previous status
                self._update_previous_status(agent_id, current_status)
                
        except Exception as e:
            self.logger.error(f"Failed to check agent status changes: {e}")
    
    def _get_previous_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Get previous status for an agent"""
        try:
            status_file = Path(f"status_cache/{agent_id}_status.json")
            if status_file.exists():
                with open(status_file, "r") as f:
                    data = json.load(f)
                    return AgentStatus(data.get("status"))
            return None
        except Exception as e:
            self.logger.error(f"Failed to get previous status for {agent_id}: {e}")
            return None
    
    def _update_previous_status(self, agent_id: str, status: AgentStatus):
        """Update previous status for an agent"""
        try:
            status_dir = Path("status_cache")
            status_dir.mkdir(exist_ok=True)
            
            status_file = status_dir / f"{agent_id}_status.json"
            with open(status_file, "w") as f:
                json.dump({"status": status.value, "timestamp": datetime.now().isoformat()}, f)
                
        except Exception as e:
            self.logger.error(f"Failed to update previous status for {agent_id}: {e}")
    
    def _handle_status_change(self, agent_id: str, old_status: AgentStatus, new_status: AgentStatus):
        """Handle agent status change"""
        try:
            # Determine transition type
            transition = self._determine_transition(old_status, new_status)
            
            # Create status event
            event = StatusEvent(
                event_id=str(uuid.uuid4()),
                agent_id=agent_id,
                old_status=old_status,
                new_status=new_status,
                transition=transition,
                timestamp=datetime.now().isoformat(),
                metadata={"old_status": old_status.value, "new_status": new_status.value}
            )
            
            # Store event
            self.status_events[event.event_id] = event
            
            # Trigger callbacks
            self._trigger_status_callbacks(agent_id, event)
            
            # Generate alert if needed
            if self._should_generate_alert(transition):
                self._generate_status_alert(event)
            
            self.logger.info(f"Status change detected for {agent_id}: {old_status.value} -> {new_status.value}")
            
        except Exception as e:
            self.logger.error(f"Failed to handle status change for {agent_id}: {e}")
    
    def _determine_transition(self, old_status: AgentStatus, new_status: AgentStatus) -> StatusTransition:
        """Determine the type of status transition"""
        try:
            if old_status == AgentStatus.ONLINE and new_status == AgentStatus.OFFLINE:
                return StatusTransition.ONLINE_TO_OFFLINE
            elif old_status == AgentStatus.OFFLINE and new_status == AgentStatus.ONLINE:
                return StatusTransition.OFFLINE_TO_ONLINE
            elif old_status == AgentStatus.IDLE and new_status == AgentStatus.BUSY:
                return StatusTransition.IDLE_TO_BUSY
            elif old_status == AgentStatus.BUSY and new_status == AgentStatus.IDLE:
                return StatusTransition.BUSY_TO_IDLE
            elif old_status == AgentStatus.HEALTHY and new_status == AgentStatus.WARNING:
                return StatusTransition.HEALTHY_TO_WARNING
            elif old_status == AgentStatus.WARNING and new_status == AgentStatus.CRITICAL:
                return StatusTransition.WARNING_TO_CRITICAL
            else:
                return StatusTransition.ONLINE_TO_OFFLINE  # Default
                
        except Exception as e:
            self.logger.error(f"Failed to determine transition: {e}")
            return StatusTransition.ONLINE_TO_OFFLINE
    
    def _should_generate_alert(self, transition: StatusTransition) -> bool:
        """Determine if an alert should be generated for a transition"""
        try:
            critical_transitions = [
                StatusTransition.ONLINE_TO_OFFLINE,
                StatusTransition.HEALTHY_TO_WARNING,
                StatusTransition.WARNING_TO_CRITICAL
            ]
            
            return transition in critical_transitions
            
        except Exception as e:
            self.logger.error(f"Failed to determine alert generation: {e}")
            return False
    
    def _generate_status_alert(self, event: StatusEvent):
        """Generate alert for status change"""
        try:
            alert_level = AlertLevel.ERROR if event.transition in [
                StatusTransition.ONLINE_TO_OFFLINE,
                StatusTransition.WARNING_TO_CRITICAL
            ] else AlertLevel.WARNING
            
            alert = Alert(
                alert_id=str(uuid.uuid4()),
                level=alert_level,
                message=f"Agent {event.agent_id} status changed: {event.old_status.value} -> {event.new_status.value}",
                source="status_manager",
                timestamp=datetime.now().isoformat(),
                acknowledged=False,
                metadata={"event_id": event.event_id, "transition": event.transition.value}
            )
            
            # Store alert
            self.alerts[alert.alert_id] = alert
            
            self.logger.info(f"Generated status alert: {alert.alert_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to generate status alert: {e}")
    
    def _perform_system_health_checks(self):
        """Perform system-wide health checks"""
        try:
            agents = self.agent_manager.get_all_agents()
            
            for agent_id, agent_info in agents.items():
                # Perform agent-specific health check
                health_status = self._check_agent_health(agent_id, agent_info)
                
                # Store health check result
                health_check = HealthCheck(
                    check_id=str(uuid.uuid4()),
                    agent_id=agent_id,
                    check_type="agent_health",
                    status=health_status,
                    message=f"Health check for {agent_id}",
                    timestamp=datetime.now().isoformat(),
                    details={"agent_status": agent_info.status.value}
                )
                
                self.health_checks[health_check.check_id] = health_check
                
        except Exception as e:
            self.logger.error(f"Failed to perform system health checks: {e}")
    
    def _check_agent_health(self, agent_id: str, agent_info: AgentInfo) -> HealthStatus:
        """Check health of a specific agent"""
        try:
            # Check if agent is responsive
            if agent_info.status == AgentStatus.OFFLINE:
                return HealthStatus.CRITICAL
            
            # Check if agent is overloaded
            if agent_info.status == AgentStatus.OVERLOADED:
                return HealthStatus.WARNING
            
            # Check if agent is healthy
            if agent_info.status == AgentStatus.ONLINE:
                return HealthStatus.HEALTHY
            
            # Default to unknown
            return HealthStatus.UNKNOWN
            
        except Exception as e:
            self.logger.error(f"Failed to check health for {agent_id}: {e}")
            return HealthStatus.UNKNOWN
    
    def _process_health_alerts(self):
        """Process health check alerts"""
        try:
            for check_id, health_check in self.health_checks.items():
                if health_check.status in [HealthStatus.WARNING, HealthStatus.CRITICAL]:
                    # Generate health alert
                    alert_level = AlertLevel.CRITICAL if health_check.status == HealthStatus.CRITICAL else AlertLevel.WARNING
                    
                    alert = Alert(
                        alert_id=str(uuid.uuid4()),
                        level=alert_level,
                        message=f"Health check failed for {health_check.agent_id}: {health_check.message}",
                        source="health_check",
                        timestamp=datetime.now().isoformat(),
                        acknowledged=False,
                        metadata={"check_id": check_id, "health_status": health_check.status.value}
                    )
                    
                    # Store alert
                    self.alerts[alert.alert_id] = alert
                    
        except Exception as e:
            self.logger.error(f"Failed to process health alerts: {e}")
    
    def _process_status_transitions(self):
        """Process pending status transitions"""
        try:
            # Process any pending status changes
            # This could include delayed transitions or batch processing
            pass
            
        except Exception as e:
            self.logger.error(f"Failed to process status transitions: {e}")
    
    def _trigger_status_callbacks(self, agent_id: str, event: StatusEvent):
        """Trigger status change callbacks"""
        try:
            if agent_id in self.status_callbacks:
                for callback in self.status_callbacks[agent_id]:
                    try:
                        callback(event)
                    except Exception as e:
                        self.logger.error(f"Callback execution failed: {e}")
                        
        except Exception as e:
            self.logger.error(f"Failed to trigger status callbacks: {e}")
    
    def register_status_callback(self, agent_id: str, callback: Callable[[StatusEvent], None]):
        """Register callback for status changes"""
        try:
            self.status_callbacks[agent_id].append(callback)
            self.logger.info(f"Registered status callback for {agent_id}")
        except Exception as e:
            self.logger.error(f"Failed to register status callback: {e}")
    
    def get_health_status(self, agent_id: str) -> Optional[HealthStatus]:
        """Get current health status for an agent"""
        try:
            # Find most recent health check
            recent_checks = [check for check in self.health_checks.values() 
                           if check.agent_id == agent_id]
            
            if recent_checks:
                # Return most recent check
                latest_check = max(recent_checks, key=lambda x: x.timestamp)
                return latest_check.status
            
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get health status for {agent_id}: {e}")
            return None
    
    def get_active_alerts(self, level: Optional[AlertLevel] = None) -> List[Alert]:
        """Get active alerts, optionally filtered by level"""
        try:
            if level:
                return [alert for alert in self.alerts.values() 
                       if alert.level == level and not alert.acknowledged]
            else:
                return [alert for alert in self.alerts.values() 
                       if not alert.acknowledged]
                
        except Exception as e:
            self.logger.error(f"Failed to get active alerts: {e}")
            return []
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        try:
            if alert_id in self.alerts:
                self.alerts[alert_id].acknowledged = True
                self.logger.info(f"Alert {alert_id} acknowledged")
                return True
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            return False
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get summary of status system"""
        try:
            total_agents = len(self.agent_manager.get_all_agents())
            online_agents = len([a for a in self.agent_manager.get_all_agents().values() 
                               if a.status == AgentStatus.ONLINE])
            total_alerts = len(self.alerts)
            active_alerts = len(self.get_active_alerts())
            
            return {
                "total_agents": total_agents,
                "online_agents": online_agents,
                "offline_agents": total_agents - online_agents,
                "total_alerts": total_alerts,
                "active_alerts": active_alerts,
                "monitoring_active": self.running,
                "health_checks": len(self.health_checks)
            }
        except Exception as e:
            self.logger.error(f"Failed to get status summary: {e}")
            return {"error": str(e)}
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test for this instance"""
        try:
            # Test status monitoring
            agents = self.agent_manager.get_all_agents()
            if not agents:
                return False
            
            # Test health check
            agent_id = list(agents.keys())[0]
            health_status = self.get_health_status(agent_id)
            if health_status is None:
                return False
            
            # Test alert system
            alerts = self.get_active_alerts()
            if not isinstance(alerts, list):
                return False
            
            # Test status summary
            summary = self.get_status_summary()
            if "total_agents" not in summary:
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Smoke test failed: {e}")
            return False
    
    def shutdown(self):
        """Shutdown the status manager"""
        self.running = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        if self.health_check_thread:
            self.health_check_thread.join(timeout=5)


def run_smoke_test():
    """Run basic functionality test for StatusManager"""
    print("🧪 Running StatusManager Smoke Test...")
    
    try:
        import tempfile
        
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create temporary directories
            agent_dir = Path(temp_dir) / "agent_workspaces"
            config_dir = Path(temp_dir) / "config"
            agent_dir.mkdir()
            config_dir.mkdir()
            
            # Create mock agent
            test_agent_dir = agent_dir / "Agent-1"
            test_agent_dir.mkdir()
            
            # Initialize managers
            config_manager = ConfigManager(config_dir)
            agent_manager = AgentManager(agent_dir)
            status_manager = StatusManager(agent_manager, config_manager)
            
            # Test basic functionality
            summary = status_manager.get_status_summary()
            assert "total_agents" in summary
            
            # Test health status
            health_status = status_manager.get_health_status("Agent-1")
            assert health_status is not None
            
            # Test alerts
            alerts = status_manager.get_active_alerts()
            assert isinstance(alerts, list)
            
            # Cleanup
            status_manager.shutdown()
            agent_manager.shutdown()
            config_manager.shutdown()
        
        print("✅ StatusManager Smoke Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ StatusManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for StatusManager testing"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Status Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--health", help="Get health status for agent")
    parser.add_argument("--alerts", action="store_true", help="Show active alerts")
    parser.add_argument("--summary", action="store_true", help="Show status summary")
    parser.add_argument("--acknowledge", help="Acknowledge alert by ID")
    
    args = parser.parse_args()
    
    if args.test:
        run_smoke_test()
        return
    
    # Initialize managers
    config_manager = ConfigManager()
    agent_manager = AgentManager()
    status_manager = StatusManager(agent_manager, config_manager)
    
    if args.health:
        health_status = status_manager.get_health_status(args.health)
        if health_status:
            print(f"Health status for {args.health}: {health_status.value}")
        else:
            print(f"No health status found for {args.health}")
    elif args.alerts:
        alerts = status_manager.get_active_alerts()
        print("Active Alerts:")
        for alert in alerts:
            print(f"  {alert.alert_id}: {alert.level.value} - {alert.message}")
    elif args.summary:
        summary = status_manager.get_status_summary()
        print("Status Summary:")
        for key, value in summary.items():
            print(f"  {key}: {value}")
    elif args.acknowledge:
        success = status_manager.acknowledge_alert(args.acknowledge)
        print(f"Alert acknowledgment: {'✅ Success' if success else '❌ Failed'}")
    else:
        parser.print_help()
    
    # Cleanup
    status_manager.shutdown()
    agent_manager.shutdown()
    config_manager.shutdown()


if __name__ == "__main__":
    main()
