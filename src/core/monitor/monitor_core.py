#!/usr/bin/env python3
"""
Monitor Core - Agent Cellphone V2
=================================

Main monitoring class for agent status tracking.
Follows V2 standards: ≤200 LOC, SRP, OOP principles.
"""

import time
import json
import threading
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

from .monitor_types import AgentInfo, AgentStatus, MonitorConfig


class AgentStatusMonitor:
    """
    Real-time agent status tracking and monitoring system
    
    Responsibilities:
    - Track real-time agent status across swarm
    - Monitor agent health and performance
    - Provide continuous agent visibility
    - Update status in real-time
    """
    
    def __init__(self, config: MonitorConfig = None):
        self.config = config or MonitorConfig()
        self.logger = logging.getLogger(f"{__name__}.AgentStatusMonitor")
        self.workspace_path = Path("agent_workspaces")
        self.is_monitoring = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.agent_statuses: Dict[str, AgentInfo] = {}
        self.status_history: List[Dict[str, Any]] = []
        self.monitoring_callbacks: List[callable] = []
        
        # Ensure workspace exists
        self.workspace_path.mkdir(exist_ok=True)
        
        # Initialize agent discovery
        self._discover_agents()
    
    def start_monitoring(self):
        """Start real-time agent status monitoring"""
        if self.is_monitoring:
            self.logger.warning("Agent status monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitor_thread.start()
        
        self.logger.info("🚀 Agent status monitoring started - real-time updates every 5 seconds")
        print("🚀 AGENT STATUS MONITORING ACTIVATED!")
    
    def stop_monitoring(self):
        """Stop agent status monitoring"""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=5.0)
        
        self.logger.info("🛑 Agent status monitoring stopped")
        print("🛑 AGENT STATUS MONITORING DEACTIVATED!")
    
    def _monitoring_loop(self):
        """Main monitoring loop for real-time updates"""
        while self.is_monitoring:
            try:
                self._update_all_agent_statuses()
                self._check_agent_health()
                self._update_performance_metrics()
                self._save_status_history()
                
                # Notify callbacks
                for callback in self.monitoring_callbacks:
                    try:
                        callback(self.agent_statuses)
                    except Exception as e:
                        self.logger.error(f"Callback error: {e}")
                
                time.sleep(self.config.update_interval)
                
            except Exception as e:
                self.logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.config.update_interval)
    
    def _discover_agents(self):
        """Discover available agents in workspace"""
        try:
            agent_dirs = [d for d in self.workspace_path.iterdir() if d.is_dir()]
            for agent_dir in agent_dirs:
                agent_id = agent_dir.name
                if agent_id not in self.agent_statuses:
                    self.agent_statuses[agent_id] = AgentInfo(
                        agent_id=agent_id,
                        name=agent_id,
                        status=AgentStatus.OFFLINE,
                        capabilities=[],
                        last_seen=time.time(),
                        uptime=0.0,
                        performance_score=0.0,
                        current_task=None,
                        resource_usage={},
                        health_metrics={}
                    )
            self.logger.info(f"Discovered {len(agent_dirs)} agents")
        except Exception as e:
            self.logger.error(f"Agent discovery error: {e}")
    
    def _update_all_agent_statuses(self):
        """Update status for all discovered agents"""
        current_time = time.time()
        for agent_id, agent_info in self.agent_statuses.items():
            try:
                # Check if agent is still active
                if current_time - agent_info.last_seen > self.config.health_check_timeout:
                    agent_info.status = AgentStatus.OFFLINE
                else:
                    # Update uptime
                    agent_info.uptime = current_time - agent_info.last_seen
                    
            except Exception as e:
                self.logger.error(f"Status update error for {agent_id}: {e}")
                agent_info.status = AgentStatus.ERROR
    
    def _check_agent_health(self):
        """Check health metrics for all agents"""
        for agent_id, agent_info in self.agent_statuses.items():
            try:
                # Basic health check
                if agent_info.performance_score < self.config.performance_threshold:
                    agent_info.health_metrics['warning'] = 'Low performance detected'
                else:
                    agent_info.health_metrics['warning'] = None
                    
            except Exception as e:
                self.logger.error(f"Health check error for {agent_id}: {e}")
    
    def _update_performance_metrics(self):
        """Update performance metrics for all agents"""
        for agent_id, agent_info in self.agent_statuses.items():
            try:
                # Calculate performance based on uptime and status
                if agent_info.status == AgentStatus.ONLINE:
                    agent_info.performance_score = min(1.0, agent_info.uptime / 3600.0)
                elif agent_info.status == AgentStatus.BUSY:
                    agent_info.performance_score = 0.8
                elif agent_info.status == AgentStatus.IDLE:
                    agent_info.performance_score = 0.6
                else:
                    agent_info.performance_score = 0.0
            except Exception as e:
                self.logger.error(f"Performance update error for {agent_id}: {e}")
    
    def _save_status_history(self):
        """Save current status to history"""
        if len(self.status_history) >= self.config.max_history_size:
            self.status_history.pop(0)
        
        current_status = {
            'timestamp': time.time(),
            'agent_count': len(self.agent_statuses),
            'online_count': len([a for a in self.agent_statuses.values() if a.status == AgentStatus.ONLINE]),
            'statuses': {k: v.status.value for k, v in self.agent_statuses.items()}
        }
        
        self.status_history.append(current_status)
    
    def get_agent_status(self, agent_id: str) -> Optional[AgentInfo]:
        """Get current status for specific agent"""
        return self.agent_statuses.get(agent_id)
    
    def get_all_agent_statuses(self) -> Dict[str, AgentInfo]:
        """Get status for all agents"""
        return self.agent_statuses.copy()
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get comprehensive status summary"""
        online_count = len([a for a in self.agent_statuses.values() if a.status == AgentStatus.ONLINE])
        total_count = len(self.agent_statuses)
        
        return {
            'total_agents': total_count,
            'online_agents': online_count,
            'offline_agents': total_count - online_count,
            'monitoring_active': self.is_monitoring,
            'last_update': time.time(),
            'performance_average': sum(a.performance_score for a in self.agent_statuses.values()) / total_count if total_count > 0 else 0.0
        }
    
    def add_monitoring_callback(self, callback: callable):
        """Add callback for status updates"""
        if callback not in self.monitoring_callbacks:
            self.monitoring_callbacks.append(callback)
    
    def remove_monitoring_callback(self, callback: callable):
        """Remove monitoring callback"""
        if callback in self.monitoring_callbacks:
            self.monitoring_callbacks.remove(callback)
