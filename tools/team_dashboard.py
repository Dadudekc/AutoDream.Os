#!/usr/bin/env python3
"""
Team Dashboard - Real-time Swarm Coordination Tool
=================================================

Provides real-time visibility into agent status, tasks, and coordination.
Addresses the captain's #1 pain point: real-time swarm visibility.

Author: Agent-4 (Captain & Operations Coordinator) + Agent-2 (Architecture & Design)
License: MIT
"""

import sys
import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import argparse

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import ConsolidatedMessagingService


class TeamDashboard:
    """Real-time team dashboard for swarm coordination."""
    
    def __init__(self, coords_file: str = "config/coordinates.json"):
        self.coords_file = coords_file
        self.messaging_service = ConsolidatedMessagingService(coords_file)
        self.agents = ["Agent-1", "Agent-2", "Agent-3", "Agent-4", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
        self.dashboard_data = {}
        self.last_update = None
        
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get current status for a specific agent."""
        try:
            # Load agent workspace data
            workspace_file = Path(f"agent_workspaces/{agent_id}/working_tasks.json")
            if workspace_file.exists():
                with open(workspace_file, 'r') as f:
                    agent_data = json.load(f)
                
                current_task = agent_data.get("current_task")
                completed_tasks = agent_data.get("completed_tasks", [])
                
                return {
                    "agent_id": agent_id,
                    "status": "active",
                    "current_task": current_task,
                    "completed_tasks_count": len(completed_tasks),
                    "last_activity": datetime.now().isoformat(),
                    "specialization": agent_data.get("specialization", "Unknown"),
                    "team": agent_data.get("team", "Unknown")
                }
            else:
                return {
                    "agent_id": agent_id,
                    "status": "unknown",
                    "current_task": None,
                    "completed_tasks_count": 0,
                    "last_activity": None,
                    "specialization": "Unknown",
                    "team": "Unknown"
                }
        except Exception as e:
            return {
                "agent_id": agent_id,
                "status": "error",
                "error": str(e),
                "current_task": None,
                "completed_tasks_count": 0,
                "last_activity": None,
                "specialization": "Unknown",
                "team": "Unknown"
            }
    
    def get_all_agents_status(self) -> Dict[str, Any]:
        """Get status for all agents."""
        agents_status = {}
        active_agents = 0
        busy_agents = 0
        available_agents = 0
        
        for agent_id in self.agents:
            status = self.get_agent_status(agent_id)
            agents_status[agent_id] = status
            
            if status["status"] == "active":
                active_agents += 1
                if status["current_task"]:
                    busy_agents += 1
                else:
                    available_agents += 1
        
        return {
            "timestamp": datetime.now().isoformat(),
            "total_agents": len(self.agents),
            "active_agents": active_agents,
            "busy_agents": busy_agents,
            "available_agents": available_agents,
            "agents": agents_status
        }
    
    def get_task_queue_summary(self) -> Dict[str, Any]:
        """Get summary of current task queue."""
        task_summary = {
            "in_progress": [],
            "completed_today": [],
            "pending": [],
            "blocked": []
        }
        
        for agent_id in self.agents:
            status = self.get_agent_status(agent_id)
            if status["current_task"]:
                task = status["current_task"]
                task_info = {
                    "agent_id": agent_id,
                    "task_id": task.get("task_id", "Unknown"),
                    "title": task.get("title", "Unknown"),
                    "priority": task.get("priority", "Unknown"),
                    "progress": task.get("progress", "0%"),
                    "started_at": task.get("started_at", "Unknown")
                }
                task_summary["in_progress"].append(task_info)
        
        return task_summary
    
    def get_communication_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent communication logs."""
        logs = []
        
        # Check recent devlogs
        devlogs_dir = Path("devlogs")
        if devlogs_dir.exists():
            recent_files = sorted(devlogs_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
            for file_path in recent_files[:limit]:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Extract basic info
                    lines = content.split('\n')
                    title = lines[0].replace('#', '').strip() if lines else file_path.name
                    
                    logs.append({
                        "timestamp": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                        "type": "devlog",
                        "title": title,
                        "file": file_path.name,
                        "agent": self._extract_agent_from_filename(file_path.name)
                    })
                except Exception:
                    continue
        
        return logs[:limit]
    
    def _extract_agent_from_filename(self, filename: str) -> str:
        """Extract agent name from filename."""
        if "Agent-1" in filename:
            return "Agent-1"
        elif "Agent-2" in filename:
            return "Agent-2"
        elif "Agent-3" in filename:
            return "Agent-3"
        elif "Agent-4" in filename:
            return "Agent-4"
        else:
            return "Unknown"
    
    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        try:
            # Get messaging service status
            status_result = self.messaging_service.get_status()
            
            return {
                "timestamp": datetime.now().isoformat(),
                "messaging_system": status_result.get("status", "unknown"),
                "agent_count": status_result.get("agent_count", 0),
                "coordinates_valid": status_result.get("system_health", {}).get("coordinates_valid", False),
                "pyautogui_available": status_result.get("system_health", {}).get("pyautogui_available", False),
                "overall_status": status_result.get("system_health", {}).get("overall_status", "unknown")
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "messaging_system": "error",
                "error": str(e),
                "overall_status": "error"
            }
    
    def generate_dashboard_data(self) -> Dict[str, Any]:
        """Generate complete dashboard data."""
        self.dashboard_data = {
            "timestamp": datetime.now().isoformat(),
            "agents_status": self.get_all_agents_status(),
            "task_queue": self.get_task_queue_summary(),
            "communication_logs": self.get_communication_logs(),
            "system_health": self.get_system_health()
        }
        self.last_update = datetime.now()
        return self.dashboard_data
    
    def display_dashboard(self, refresh_interval: int = 30):
        """Display real-time dashboard with auto-refresh."""
        print("🎯 TEAM DASHBOARD - Real-time Swarm Coordination")
        print("=" * 60)
        
        while True:
            try:
                # Clear screen (works on most terminals)
                print("\033[2J\033[H", end="")
                
                # Generate fresh data
                data = self.generate_dashboard_data()
                
                # Display header
                print(f"🎯 TEAM DASHBOARD - {data['timestamp']}")
                print("=" * 60)
                
                # Display agent status
                agents_data = data["agents_status"]
                print(f"\n📊 AGENT STATUS ({agents_data['active_agents']}/{agents_data['total_agents']} active)")
                print("-" * 40)
                print(f"🟢 Available: {agents_data['available_agents']}")
                print(f"🟡 Busy: {agents_data['busy_agents']}")
                print(f"🔴 Inactive: {agents_data['total_agents'] - agents_data['active_agents']}")
                
                # Display individual agent status
                print(f"\n🤖 AGENT DETAILS:")
                print("-" * 40)
                for agent_id, agent_data in agents_data["agents"].items():
                    status_icon = "🟢" if agent_data["status"] == "active" else "🔴"
                    task_info = ""
                    if agent_data["current_task"]:
                        task = agent_data["current_task"]
                        task_info = f" | Task: {task.get('title', 'Unknown')} ({task.get('progress', '0%')})"
                    
                    print(f"{status_icon} {agent_id}: {agent_data['specialization']}{task_info}")
                
                # Display task queue
                task_data = data["task_queue"]
                print(f"\n📋 TASK QUEUE")
                print("-" * 40)
                print(f"In Progress: {len(task_data['in_progress'])}")
                for task in task_data["in_progress"]:
                    print(f"  • {task['agent_id']}: {task['title']} ({task['progress']})")
                
                # Display system health
                health_data = data["system_health"]
                print(f"\n💚 SYSTEM HEALTH")
                print("-" * 40)
                print(f"Messaging: {health_data.get('messaging_system', 'Unknown')}")
                print(f"Coordinates: {'✅' if health_data.get('coordinates_valid') else '❌'}")
                print(f"PyAutoGUI: {'✅' if health_data.get('pyautogui_available') else '❌'}")
                print(f"Overall: {health_data.get('overall_status', 'Unknown')}")
                
                # Display recent activity
                logs = data["communication_logs"]
                print(f"\n📝 RECENT ACTIVITY")
                print("-" * 40)
                for log in logs[:5]:
                    print(f"  • {log['agent']}: {log['title']}")
                
                print(f"\n🔄 Auto-refresh every {refresh_interval}s (Ctrl+C to exit)")
                time.sleep(refresh_interval)
                
            except KeyboardInterrupt:
                print("\n\n👋 Dashboard closed by user")
                break
            except Exception as e:
                print(f"\n❌ Dashboard error: {e}")
                time.sleep(5)
    
    def save_dashboard_snapshot(self, filename: str = None):
        """Save current dashboard data to file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"dashboard_snapshot_{timestamp}.json"
        
        data = self.generate_dashboard_data()
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"📊 Dashboard snapshot saved: {filename}")
        return filename


def main():
    """Main CLI interface for team dashboard."""
    parser = argparse.ArgumentParser(description="Team Dashboard - Real-time Swarm Coordination")
    parser.add_argument("--coords", default="config/coordinates.json", help="Coordinates file")
    parser.add_argument("--display", action="store_true", help="Display real-time dashboard")
    parser.add_argument("--refresh", type=int, default=30, help="Refresh interval in seconds")
    parser.add_argument("--snapshot", help="Save dashboard snapshot to file")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--agents", action="store_true", help="Show agent status")
    parser.add_argument("--tasks", action="store_true", help="Show task queue")
    parser.add_argument("--health", action="store_true", help="Show system health")
    
    args = parser.parse_args()
    
    dashboard = TeamDashboard(args.coords)
    
    try:
        if args.display:
            dashboard.display_dashboard(args.refresh)
        elif args.snapshot:
            dashboard.save_dashboard_snapshot(args.snapshot)
        elif args.status:
            data = dashboard.generate_dashboard_data()
            print("🎯 TEAM DASHBOARD STATUS")
            print("=" * 40)
            print(json.dumps(data, indent=2))
        elif args.agents:
            agents_data = dashboard.get_all_agents_status()
            print("🤖 AGENT STATUS")
            print("=" * 40)
            print(json.dumps(agents_data, indent=2))
        elif args.tasks:
            task_data = dashboard.get_task_queue_summary()
            print("📋 TASK QUEUE")
            print("=" * 40)
            print(json.dumps(task_data, indent=2))
        elif args.health:
            health_data = dashboard.get_system_health()
            print("💚 SYSTEM HEALTH")
            print("=" * 40)
            print(json.dumps(health_data, indent=2))
        else:
            # Default: show quick status
            data = dashboard.generate_dashboard_data()
            agents_data = data["agents_status"]
            print(f"🐝 WE ARE SWARM - Team Dashboard")
            print(f"Active Agents: {agents_data['active_agents']}/{agents_data['total_agents']}")
            print(f"Available: {agents_data['available_agents']} | Busy: {agents_data['busy_agents']}")
            print(f"System: {data['system_health'].get('overall_status', 'Unknown')}")
            print(f"Use --display for real-time dashboard")
        
        return 0
        
    except Exception as e:
        print(f"🐝 WE ARE SWARM - Dashboard error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())






