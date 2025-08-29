#!/usr/bin/env python3
"""
Workflow Monitor - Agent Cellphone V2
====================================

Monitors and reports on workflow execution.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import time

from src.utils.stability_improvements import stability_manager, safe_import
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from ..core.enums import WorkflowState, TaskStatus
from ..core.models import DevelopmentTask


@dataclass
class MonitoringEvent:
    """Workflow monitoring event"""
    event_id: str
    event_type: str
    timestamp: datetime
    source: str
    details: Dict
    severity: str = "info"


class WorkflowMonitor:
    """Monitors workflow execution and provides reporting"""
    
    def __init__(self):
        self.events: List[MonitoringEvent] = []
        self.event_counter = 0
        self.logger = logging.getLogger(__name__)
        self.monitoring_callbacks: List[Callable] = []
        self.alert_thresholds = {
            "task_stuck_minutes": 60,
            "workflow_cycle_timeout_seconds": 300,
            "agent_inactivity_minutes": 30,
            "error_rate_threshold": 0.1
        }
    
    def add_event(self, event_type: str, source: str, details: Dict, severity: str = "info") -> str:
        """Add a monitoring event"""
        self.event_counter += 1
        event_id = f"event_{self.event_counter:06d}"
        
        event = MonitoringEvent(
            event_id=event_id,
            event_type=event_type,
            timestamp=datetime.now(),
            source=source,
            details=details,
            severity=severity
        )
        
        self.events.append(event)
        
        # Log the event
        log_message = f"📊 [{event_type.upper()}] {source}: {details}"
        if severity == "error":
            self.logger.error(log_message)
        elif severity == "warning":
            self.logger.warning(log_message)
        else:
            self.logger.info(log_message)
        
        # Notify monitoring callbacks
        self._notify_callbacks(event)
        
        return event_id
    
    def add_monitoring_callback(self, callback: Callable):
        """Add a callback for monitoring events"""
        self.monitoring_callbacks.append(callback)
    
    def remove_monitoring_callback(self, callback: Callable):
        """Remove a monitoring callback"""
        if callback in self.monitoring_callbacks:
            self.monitoring_callbacks.remove(callback)
    
    def _notify_callbacks(self, event: MonitoringEvent):
        """Notify all monitoring callbacks"""
        for callback in self.monitoring_callbacks:
            try:
                callback(event)
            except Exception as e:
                self.logger.error(f"Monitoring callback failed: {e}")
    
    def monitor_task_execution(self, task: DevelopmentTask, agent_id: str) -> Dict[str, any]:
        """Monitor task execution and detect issues"""
        monitoring_result = {
            "task_id": task.task_id,
            "agent_id": agent_id,
            "status": task.status.value,
            "progress": task.progress_percentage,
            "issues": []
        }
        
        # Check for stuck tasks
        if task.status == TaskStatus.IN_PROGRESS:
            elapsed_time = task.get_elapsed_time()
            if elapsed_time and elapsed_time > (self.alert_thresholds["task_stuck_minutes"] / 60):
                issue = {
                    "type": "task_stuck",
                    "severity": "warning",
                    "message": f"Task stuck for {elapsed_time:.1f} hours",
                    "elapsed_hours": elapsed_time
                }
                monitoring_result["issues"].append(issue)
                
                # Add monitoring event
                self.add_event(
                    "task_stuck",
                    f"agent_{agent_id}",
                    {"task_id": task.task_id, "elapsed_hours": elapsed_time},
                    "warning"
                )
        
        # Check for blocked tasks
        if task.status == TaskStatus.BLOCKED:
            issue = {
                "type": "task_blocked",
                "severity": "info",
                "message": f"Task blocked: {', '.join(task.blockers)}",
                "blockers": task.blockers
            }
            monitoring_result["issues"].append(issue)
        
        # Check for overdue tasks
        if task.claimed_at:
            estimated_completion = task.estimated_hours
            elapsed_time = task.get_elapsed_time() or 0
            if elapsed_time > estimated_completion * 1.5:  # 50% over estimated time
                issue = {
                    "type": "task_overdue",
                    "severity": "warning",
                    "message": f"Task overdue by {elapsed_time - estimated_completion:.1f} hours",
                    "estimated_hours": estimated_completion,
                    "elapsed_hours": elapsed_time
                }
                monitoring_result["issues"].append(issue)
        
        return monitoring_result
    
    def monitor_workflow_health(self, workflow_engine) -> Dict[str, any]:
        """Monitor overall workflow health"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_health": "healthy",
            "issues": [],
            "metrics": {}
        }
        
        try:
            # Get workflow status
            workflow_status = workflow_engine.get_workflow_status()
            health_status["workflow_state"] = workflow_status["state"]
            
            # Check for workflow errors
            if workflow_status["state"] == "error":
                health_status["overall_health"] = "critical"
                health_status["issues"].append({
                    "type": "workflow_error",
                    "severity": "critical",
                    "message": "Workflow engine in error state"
                })
            
            # Check cycle performance
            if workflow_status["workflow_stats"]["last_cycle_time"]:
                cycle_time = workflow_status["workflow_stats"]["last_cycle_time"].total_seconds()
                health_status["metrics"]["last_cycle_time_seconds"] = cycle_time
                
                if cycle_time > self.alert_thresholds["workflow_cycle_timeout_seconds"]:
                    health_status["overall_health"] = "warning"
                    health_status["issues"].append({
                        "type": "slow_cycle",
                        "severity": "warning",
                        "message": f"Workflow cycle taking {cycle_time:.1f}s (threshold: {self.alert_thresholds['workflow_cycle_timeout_seconds']}s)"
                    })
            
            # Check task distribution
            task_stats = workflow_status["task_stats"]
            health_status["metrics"]["task_distribution"] = {
                "total": task_stats["total_tasks"],
                "available": task_stats["available_tasks"],
                "in_progress": task_stats["in_progress_tasks"],
                "completed": task_stats["completed_tasks"],
                "blocked": task_stats["blocked_tasks"]
            }
            
            # Check for task bottlenecks
            if task_stats["blocked_tasks"] > task_stats["total_tasks"] * 0.3:  # More than 30% blocked
                health_status["overall_health"] = "warning"
                health_status["issues"].append({
                    "type": "task_bottleneck",
                    "severity": "warning",
                    "message": f"High number of blocked tasks: {task_stats['blocked_tasks']}/{task_stats['total_tasks']}"
                })
            
            # Check agent health
            agent_stats = workflow_status["agent_stats"]
            health_status["metrics"]["agent_health"] = {
                "total": agent_stats["total_agents"],
                "active": agent_stats["active_agents"],
                "inactive": agent_stats["inactive_agents"]
            }
            
            if agent_stats["inactive_agents"] > 0:
                health_status["overall_health"] = "warning"
                health_status["issues"].append({
                    "type": "inactive_agents",
                    "severity": "warning",
                    "message": f"Inactive agents: {agent_stats['inactive_agents']}"
                })
            
        except Exception as e:
            health_status["overall_health"] = "critical"
            health_status["issues"].append({
                "type": "monitoring_error",
                "severity": "critical",
                "message": f"Error monitoring workflow: {e}"
            })
        
        return health_status
    
    def generate_health_report(self, workflow_engine) -> Dict[str, any]:
        """Generate comprehensive health report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {},
            "workflow_health": self.monitor_workflow_health(workflow_engine),
            "recent_events": self.get_recent_events(limit=20),
            "recommendations": []
        }
        
        # Generate summary
        workflow_status = workflow_engine.get_workflow_status()
        report["summary"] = {
            "workflow_state": workflow_status["state"],
            "total_cycles": workflow_status["workflow_stats"]["cycles_completed"],
            "total_tasks": workflow_status["task_stats"]["total_tasks"],
            "active_agents": workflow_status["agent_stats"]["active_agents"],
            "overall_health": report["workflow_health"]["overall_health"]
        }
        
        # Generate recommendations based on issues
        issues = report["workflow_health"]["issues"]
        for issue in issues:
            if issue["type"] == "task_bottleneck":
                report["recommendations"].append({
                    "priority": "high",
                    "action": "Review blocked tasks and resolve dependencies",
                    "reason": "High number of blocked tasks indicates workflow bottlenecks"
                })
            elif issue["type"] == "slow_cycle":
                report["recommendations"].append({
                    "priority": "medium",
                    "action": "Investigate slow workflow cycles",
                    "reason": "Slow cycles may indicate performance issues"
                })
            elif issue["type"] == "inactive_agents":
                report["recommendations"].append({
                    "priority": "medium",
                    "action": "Check agent connectivity and health",
                    "reason": "Inactive agents reduce workflow capacity"
                })
        
        return report
    
    def get_recent_events(self, limit: int = 50) -> List[Dict]:
        """Get recent monitoring events"""
        recent_events = sorted(self.events, key=lambda x: x.timestamp, reverse=True)
        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp.isoformat(),
                "source": event.source,
                "details": event.details,
                "severity": event.severity
            }
            for event in recent_events[:limit]
        ]
    
    def get_events_by_type(self, event_type: str) -> List[MonitoringEvent]:
        """Get events by type"""
        return [event for event in self.events if event.event_type == event_type]
    
    def get_events_by_severity(self, severity: str) -> List[MonitoringEvent]:
        """Get events by severity"""
        return [event for event in self.events if event.severity == severity]
    
    def cleanup_old_events(self, days_old: int = 7) -> int:
        """Remove old monitoring events"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        removed_count = 0
        
        events_to_remove = []
        for event in self.events:
            if event.timestamp < cutoff_date:
                events_to_remove.append(event)
        
        for event in events_to_remove:
            self.events.remove(event)
            removed_count += 1
        
        self.logger.info(f"🧹 Cleaned up {removed_count} old monitoring events")
        return removed_count
    
    def export_events(self) -> List[Dict]:
        """Export events to dictionary format"""
        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "timestamp": event.timestamp.isoformat(),
                "source": event.source,
                "details": event.details,
                "severity": event.severity
            }
            for event in self.events
        ]
