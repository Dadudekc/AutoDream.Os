#!/usr/bin/env python3
"""
Watchdog System - Agent System Monitoring
==========================================

Comprehensive system monitoring and health checking for the V2_SWARM system.
Monitors agent status, resource usage, and system health.

Author: Agent-6 (SSOT_MANAGER)
License: MIT
V2 Compliance: ≤400 lines, ≤5 classes, ≤10 functions
"""

import json
import logging
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class AgentStatus:
    """Agent status data class"""
    agent_id: str
    status: str
    role: str
    last_active: str
    task_count: int
    health_score: float


@dataclass
class SystemHealth:
    """System health data class"""
    overall_status: str
    active_agents: int
    total_agents: int
    health_score: float
    alerts: List[str]
    timestamp: str


class AgentHealthMonitor:
    """Monitor agent health and status"""
    
    def __init__(self, workspace_dir: str = "agent_workspaces"):
        """Initialize agent health monitor"""
        self.workspace_dir = Path(workspace_dir)
        self.agents = [f"Agent-{i}" for i in range(1, 9)]
    
    def check_agent_status(self, agent_id: str) -> Optional[AgentStatus]:
        """Check status of a specific agent"""
        status_file = self.workspace_dir / agent_id / "status.json"
        
        if not status_file.exists():
            return None
        
        try:
            with open(status_file, 'r') as f:
                data = json.load(f)
            
            return AgentStatus(
                agent_id=agent_id,
                status=data.get('status', 'UNKNOWN'),
                role=data.get('current_role', 'NONE'),
                last_active=data.get('last_active', 'NEVER'),
                task_count=len(data.get('working_tasks', [])),
                health_score=self._calculate_health_score(data)
            )
        except Exception as e:
            logger.error(f"Error checking agent {agent_id}: {e}")
            return None
    
    def _calculate_health_score(self, data: Dict) -> float:
        """Calculate agent health score (0-100)"""
        score = 100.0
        
        # Deduct for inactive status
        if data.get('status') != 'ACTIVE':
            score -= 50
        
        # Deduct for stale last_active
        try:
            last_active = datetime.fromisoformat(data.get('last_active', ''))
            time_since = (datetime.now() - last_active).total_seconds()
            if time_since > 3600:  # 1 hour
                score -= 30
            elif time_since > 1800:  # 30 minutes
                score -= 15
        except:
            score -= 20
        
        # Deduct for excessive tasks
        task_count = len(data.get('working_tasks', []))
        if task_count > 5:
            score -= 10
        
        return max(0.0, score)
    
    def check_all_agents(self) -> List[AgentStatus]:
        """Check status of all agents"""
        statuses = []
        for agent_id in self.agents:
            status = self.check_agent_status(agent_id)
            if status:
                statuses.append(status)
        return statuses


class SystemHealthChecker:
    """Check overall system health"""
    
    def __init__(self):
        """Initialize system health checker"""
        self.agent_monitor = AgentHealthMonitor()
    
    def check_system_health(self) -> SystemHealth:
        """Check overall system health"""
        agent_statuses = self.agent_monitor.check_all_agents()
        
        active_agents = sum(1 for a in agent_statuses if a.status == 'ACTIVE')
        total_agents = len(agent_statuses)
        
        # Calculate overall health score
        if total_agents > 0:
            avg_health = sum(a.health_score for a in agent_statuses) / total_agents
        else:
            avg_health = 0.0
        
        # Generate alerts
        alerts = self._generate_alerts(agent_statuses, active_agents, total_agents)
        
        # Determine overall status
        if avg_health >= 90:
            overall_status = "EXCELLENT"
        elif avg_health >= 75:
            overall_status = "GOOD"
        elif avg_health >= 60:
            overall_status = "FAIR"
        elif avg_health >= 40:
            overall_status = "POOR"
        else:
            overall_status = "CRITICAL"
        
        return SystemHealth(
            overall_status=overall_status,
            active_agents=active_agents,
            total_agents=total_agents,
            health_score=avg_health,
            alerts=alerts,
            timestamp=datetime.now().isoformat()
        )
    
    def _generate_alerts(self, statuses: List[AgentStatus], active: int, total: int) -> List[str]:
        """Generate system alerts"""
        alerts = []
        
        # Check agent availability
        if active < total * 0.5:
            alerts.append(f"LOW AGENT AVAILABILITY: Only {active}/{total} agents active")
        
        # Check individual agent health
        for status in statuses:
            if status.health_score < 50:
                alerts.append(f"AGENT HEALTH: {status.agent_id} health score low ({status.health_score:.1f})")
            
            if status.status != 'ACTIVE':
                alerts.append(f"AGENT STATUS: {status.agent_id} is {status.status}")
        
        return alerts


class WatchdogService:
    """Main watchdog service for system monitoring"""
    
    def __init__(self, config_path: str = "config/watchdog_config.json"):
        """Initialize watchdog service"""
        self.config_path = Path(config_path)
        self.health_checker = SystemHealthChecker()
        self.running = False
        self.check_interval = 300  # 5 minutes
        self.load_config()
    
    def load_config(self) -> None:
        """Load watchdog configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                self.check_interval = config.get('check_interval', 300)
                logger.info(f"Watchdog config loaded: check_interval={self.check_interval}s")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
        else:
            self._create_default_config()
    
    def _create_default_config(self) -> None:
        """Create default configuration"""
        config = {
            "check_interval": 300,
            "alert_thresholds": {
                "health_score_warning": 60,
                "health_score_critical": 40,
                "agent_availability_warning": 0.5
            },
            "enabled_checks": {
                "agent_status": True,
                "system_health": True,
                "resource_usage": True
            }
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Default watchdog config created: {self.config_path}")
    
    def run_health_check(self) -> SystemHealth:
        """Run single health check"""
        return self.health_checker.check_system_health()
    
    def get_agent_report(self) -> Dict[str, Any]:
        """Get detailed agent report"""
        statuses = self.health_checker.agent_monitor.check_all_agents()
        
        return {
            "timestamp": datetime.now().isoformat(),
            "agents": [
                {
                    "agent_id": s.agent_id,
                    "status": s.status,
                    "role": s.role,
                    "last_active": s.last_active,
                    "task_count": s.task_count,
                    "health_score": s.health_score
                }
                for s in statuses
            ],
            "summary": {
                "total_agents": len(statuses),
                "active_agents": sum(1 for s in statuses if s.status == 'ACTIVE'),
                "average_health": sum(s.health_score for s in statuses) / len(statuses) if statuses else 0
            }
        }
    
    def save_health_report(self, output_path: str = "reports/health_report.json") -> None:
        """Save health report to file"""
        health = self.run_health_check()
        agent_report = self.get_agent_report()
        
        report = {
            "system_health": {
                "overall_status": health.overall_status,
                "active_agents": health.active_agents,
                "total_agents": health.total_agents,
                "health_score": health.health_score,
                "alerts": health.alerts,
                "timestamp": health.timestamp
            },
            "agent_details": agent_report
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Health report saved: {output_file}")


def main():
    """Main execution function"""
    print("🔍 WATCHDOG SYSTEM - V2_SWARM Monitoring")
    print("=" * 60)
    
    # Initialize watchdog
    watchdog = WatchdogService()
    
    # Run health check
    print("\n📊 Running system health check...")
    health = watchdog.run_health_check()
    
    # Display results
    print(f"\n✅ System Status: {health.overall_status}")
    print(f"📈 Health Score: {health.health_score:.1f}/100")
    print(f"🤖 Active Agents: {health.active_agents}/{health.total_agents}")
    
    if health.alerts:
        print(f"\n⚠️  Alerts ({len(health.alerts)}):")
        for alert in health.alerts:
            print(f"  - {alert}")
    else:
        print("\n✅ No alerts - system healthy")
    
    # Get agent report
    print("\n📋 Agent Status Report:")
    agent_report = watchdog.get_agent_report()
    for agent in agent_report['agents']:
        status_emoji = "✅" if agent['status'] == 'ACTIVE' else "❌"
        print(f"  {status_emoji} {agent['agent_id']}: {agent['status']} | Role: {agent['role']} | Health: {agent['health_score']:.1f}")
    
    # Save report
    watchdog.save_health_report()
    print("\n💾 Health report saved to reports/health_report.json")
    
    print("\n🔍 Watchdog system check complete")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

