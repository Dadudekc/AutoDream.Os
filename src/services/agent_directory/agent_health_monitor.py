#!/usr/bin/env python3
"""
Agent Health Monitor - V2 Compliant
===================================

Monitors agent health and status for V2_SWARM system.
Provides health checks, status monitoring, and alerting.

Author: Agent-4 (Captain)
License: MIT
"""

import json
import logging
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

logger = logging.getLogger(__name__)


@dataclass
class HealthCheck:
    """Health check result."""
    
    agent_id: str
    status: str
    last_seen: str
    workspace_exists: bool
    status_file_exists: bool
    status_file_valid: bool
    last_update_age: int  # minutes
    health_score: float  # 0.0 to 1.0


class AgentHealthMonitor:
    """Monitors agent health and status."""
    
    def __init__(self, workspace_root: str = "agent_workspaces"):
        """Initialize agent health monitor."""
        self.workspace_root = Path(workspace_root)
        self.health_threshold_minutes = 60  # Alert if no update in 60 minutes
        self.critical_threshold_minutes = 180  # Critical if no update in 3 hours
        
        logger.info("Agent Health Monitor initialized")
    
    def check_agent_health(self, agent_id: str) -> HealthCheck:
        """Check agent health status."""
        try:
            workspace_dir = self.workspace_root / agent_id
            
            # Check workspace existence
            workspace_exists = workspace_dir.exists()
            
            # Check status file
            status_file = workspace_dir / "status.json"
            status_file_exists = status_file.exists()
            status_file_valid = False
            last_update_age = 999999  # Default to very old
            
            if status_file_exists:
                try:
                    with open(status_file) as f:
                        status_data = json.load(f)
                    
                    # Check if status file is valid
                    if isinstance(status_data, dict) and ("last_update" in status_data or "last_updated" in status_data):
                        status_file_valid = True
                        
                        # Calculate age of last update
                        last_update_str = status_data.get("last_update", status_data.get("last_updated", ""))
                        if last_update_str:
                            try:
                                last_update_time = datetime.fromisoformat(last_update_str)
                                current_time = datetime.now()
                                
                                # Handle timezone-aware vs naive datetimes
                                if last_update_time.tzinfo is not None and current_time.tzinfo is None:
                                    current_time = current_time.replace(tzinfo=last_update_time.tzinfo)
                                elif last_update_time.tzinfo is None and current_time.tzinfo is not None:
                                    last_update_time = last_update_time.replace(tzinfo=current_time.tzinfo)
                                
                                age_delta = current_time - last_update_time
                                last_update_age = int(age_delta.total_seconds() / 60)
                            except (ValueError, TypeError):
                                last_update_age = 999999
                
                except (json.JSONDecodeError, IOError):
                    status_file_valid = False
            
            # Determine health status
            if not workspace_exists:
                status = "missing_workspace"
                health_score = 0.0
            elif not status_file_exists:
                status = "missing_status"
                health_score = 0.1
            elif not status_file_valid:
                status = "invalid_status"
                health_score = 0.2
            elif last_update_age > self.critical_threshold_minutes:
                status = "critical"
                health_score = 0.3
            elif last_update_age > self.health_threshold_minutes:
                status = "warning"
                health_score = 0.6
            else:
                status = "healthy"
                health_score = 1.0
            
            return HealthCheck(
                agent_id=agent_id,
                status=status,
                last_seen=datetime.now().isoformat(),
                workspace_exists=workspace_exists,
                status_file_exists=status_file_exists,
                status_file_valid=status_file_valid,
                last_update_age=last_update_age,
                health_score=health_score
            )
            
        except Exception as e:
            logger.error(f"Error checking health for {agent_id}: {e}")
            return HealthCheck(
                agent_id=agent_id,
                status="error",
                last_seen=datetime.now().isoformat(),
                workspace_exists=False,
                status_file_exists=False,
                status_file_valid=False,
                last_update_age=999999,
                health_score=0.0
            )
    
    def monitor_all_agents(self) -> Dict[str, HealthCheck]:
        """Monitor all agents."""
        health_results = {}
        
        if not self.workspace_root.exists():
            logger.warning(f"Workspace root not found: {self.workspace_root}")
            return health_results
        
        # Discover all agents
        for agent_dir in self.workspace_root.iterdir():
            if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                agent_id = agent_dir.name
                health_results[agent_id] = self.check_agent_health(agent_id)
        
        logger.info(f"Monitored {len(health_results)} agents")
        return health_results
    
    def alert_unhealthy_agents(self) -> List[str]:
        """Alert on unhealthy agents."""
        unhealthy_agents = []
        health_results = self.monitor_all_agents()
        
        for agent_id, health in health_results.items():
            if health.status in ["critical", "warning", "missing_workspace", "missing_status", "invalid_status"]:
                unhealthy_agents.append(agent_id)
                logger.warning(f"Unhealthy agent detected: {agent_id} - {health.status}")
        
        return unhealthy_agents
    
    def get_health_summary(self) -> Dict[str, Any]:
        """Get health summary for all agents."""
        health_results = self.monitor_all_agents()
        
        if not health_results:
            return {
                "total_agents": 0,
                "healthy_agents": 0,
                "warning_agents": 0,
                "critical_agents": 0,
                "error_agents": 0,
                "average_health_score": 0.0,
                "last_check": datetime.now().isoformat()
            }
        
        # Count agents by status
        status_counts = {
            "healthy": 0,
            "warning": 0,
            "critical": 0,
            "missing_workspace": 0,
            "missing_status": 0,
            "invalid_status": 0,
            "error": 0
        }
        
        total_health_score = 0.0
        
        for health in health_results.values():
            status_counts[health.status] = status_counts.get(health.status, 0) + 1
            total_health_score += health.health_score
        
        average_health_score = total_health_score / len(health_results)
        
        return {
            "total_agents": len(health_results),
            "healthy_agents": status_counts["healthy"],
            "warning_agents": status_counts["warning"],
            "critical_agents": status_counts["critical"],
            "error_agents": status_counts["missing_workspace"] + status_counts["missing_status"] + status_counts["invalid_status"] + status_counts["error"],
            "average_health_score": round(average_health_score, 2),
            "last_check": datetime.now().isoformat(),
            "status_breakdown": status_counts
        }
    
    def get_agent_health_history(self, agent_id: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get agent health history (simulated for now)."""
        # This would typically read from a health history database
        # For now, return current health status
        current_health = self.check_agent_health(agent_id)
        
        return [{
            "timestamp": current_health.last_seen,
            "status": current_health.status,
            "health_score": current_health.health_score,
            "last_update_age": current_health.last_update_age
        }]
    
    def generate_health_report(self) -> str:
        """Generate a comprehensive health report."""
        summary = self.get_health_summary()
        unhealthy_agents = self.alert_unhealthy_agents()
        
        report = f"""
# 🏥 AGENT HEALTH REPORT

**Generated**: {summary['last_check']}
**Total Agents**: {summary['total_agents']}

## 📊 Health Summary
- **Healthy**: {summary['healthy_agents']} agents
- **Warning**: {summary['warning_agents']} agents  
- **Critical**: {summary['critical_agents']} agents
- **Errors**: {summary['error_agents']} agents
- **Average Health Score**: {summary['average_health_score']}/1.0

## 🚨 Unhealthy Agents
"""
        
        if unhealthy_agents:
            for agent_id in unhealthy_agents:
                health = self.check_agent_health(agent_id)
                report += f"- **{agent_id}**: {health.status} (last update: {health.last_update_age} minutes ago)\n"
        else:
            report += "✅ All agents are healthy!\n"
        
        report += f"""
## 📈 Status Breakdown
"""
        for status, count in summary['status_breakdown'].items():
            if count > 0:
                report += f"- **{status.replace('_', ' ').title()}**: {count} agents\n"
        
        return report


def main():
    """CLI interface for agent health monitor."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Health Monitor CLI")
    parser.add_argument("--check", help="Check health for specific agent")
    parser.add_argument("--monitor", action="store_true", help="Monitor all agents")
    parser.add_argument("--alerts", action="store_true", help="Show unhealthy agents")
    parser.add_argument("--summary", action="store_true", help="Show health summary")
    parser.add_argument("--report", action="store_true", help="Generate health report")
    parser.add_argument("--history", nargs=2, metavar=("AGENT", "HOURS"), 
                       help="Get health history for agent")
    
    args = parser.parse_args()
    
    monitor = AgentHealthMonitor()
    
    if args.check:
        health = monitor.check_agent_health(args.check)
        print(f"Health Check for {args.check}:")
        print(f"  Status: {health.status}")
        print(f"  Health Score: {health.health_score}")
        print(f"  Last Update Age: {health.last_update_age} minutes")
        print(f"  Workspace Exists: {health.workspace_exists}")
        print(f"  Status File Valid: {health.status_file_valid}")
    
    elif args.monitor:
        results = monitor.monitor_all_agents()
        print("Agent Health Monitor Results:")
        for agent_id, health in results.items():
            status_icon = "🟢" if health.status == "healthy" else "🟡" if health.status == "warning" else "🔴"
            print(f"  {status_icon} {agent_id}: {health.status} (score: {health.health_score})")
    
    elif args.alerts:
        unhealthy = monitor.alert_unhealthy_agents()
        if unhealthy:
            print("🚨 Unhealthy Agents:")
            for agent in unhealthy:
                print(f"  - {agent}")
        else:
            print("✅ All agents are healthy!")
    
    elif args.summary:
        summary = monitor.get_health_summary()
        print("Health Summary:")
        print(json.dumps(summary, indent=2))
    
    elif args.report:
        report = monitor.generate_health_report()
        print(report)
    
    elif args.history:
        agent_id, hours = args.history
        history = monitor.get_agent_health_history(agent_id, int(hours))
        print(f"Health History for {agent_id} (last {hours} hours):")
        print(json.dumps(history, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
