#!/usr/bin/env python3
"""
Swarm Coordination Dashboard CLI
================================

Command-line interface for the Swarm Coordination Dashboard.
Provides easy access to dashboard functionality and web interface.

Author: Agent-2 (Architecture & Design Specialist) + Agent-4 (Captain)
License: MIT
"""

import sys
import argparse
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.services.dashboard import SwarmCoordinationDashboard, DashboardWebServer

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="Swarm Coordination Dashboard CLI")
    parser.add_argument("--config", default="config/coordinates.json", 
                       help="Path to coordinates configuration file")
    parser.add_argument("--host", default="localhost", 
                       help="Host for web interface")
    parser.add_argument("--port", type=int, default=8080, 
                       help="Port for web interface")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Start web interface
    start_parser = subparsers.add_parser("start", help="Start web interface")
    start_parser.add_argument("--daemon", action="store_true", 
                             help="Run in background")
    
    # Show status
    status_parser = subparsers.add_parser("status", help="Show dashboard status")
    status_parser.add_argument("--format", choices=["json", "table"], 
                              default="table", help="Output format")
    
    # Show agents
    agents_parser = subparsers.add_parser("agents", help="Show agent status")
    agents_parser.add_argument("--agent", help="Show specific agent")
    agents_parser.add_argument("--format", choices=["json", "table"], 
                              default="table", help="Output format")
    
    # Show tasks
    tasks_parser = subparsers.add_parser("tasks", help="Show task status")
    tasks_parser.add_argument("--task", help="Show specific task")
    tasks_parser.add_argument("--format", choices=["json", "table"], 
                             default="table", help="Output format")
    
    # Show alerts
    alerts_parser = subparsers.add_parser("alerts", help="Show alerts")
    alerts_parser.add_argument("--acknowledge", help="Acknowledge alert by ID")
    alerts_parser.add_argument("--format", choices=["json", "table"], 
                              default="table", help="Output format")
    
    # Add alert
    add_alert_parser = subparsers.add_parser("add-alert", help="Add new alert")
    add_alert_parser.add_argument("--type", required=True, 
                                 choices=["info", "warning", "error"], 
                                 help="Alert type")
    add_alert_parser.add_argument("--message", required=True, 
                                 help="Alert message")
    add_alert_parser.add_argument("--agent", help="Associated agent ID")
    
    # Update agent
    update_agent_parser = subparsers.add_parser("update-agent", help="Update agent status")
    update_agent_parser.add_argument("--agent", required=True, 
                                    help="Agent ID")
    update_agent_parser.add_argument("--status", required=True,
                                    choices=["active", "idle", "working", "stalled", "error", "offline"],
                                    help="New status")
    update_agent_parser.add_argument("--task", help="Current task")
    update_agent_parser.add_argument("--score", type=float, help="Performance score")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Initialize dashboard
    dashboard = SwarmCoordinationDashboard(args.config)
    dashboard.initialize()
    
    if args.command == "start":
        start_web_interface(dashboard, args.host, args.port, args.daemon)
    elif args.command == "status":
        show_status(dashboard, args.format)
    elif args.command == "agents":
        show_agents(dashboard, args.agent, args.format)
    elif args.command == "tasks":
        show_tasks(dashboard, args.task, args.format)
    elif args.command == "alerts":
        show_alerts(dashboard, args.acknowledge, args.format)
    elif args.command == "add-alert":
        add_alert(dashboard, args.type, args.message, args.agent)
    elif args.command == "update-agent":
        update_agent(dashboard, args.agent, args.status, args.task, args.score)

def start_web_interface(dashboard, host, port, daemon):
    """Start the web interface"""
    server = DashboardWebServer(dashboard, host, port)
    server.start()
    
    if daemon:
        print(f"🚀 Dashboard running in background at http://{host}:{port}")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()
    else:
        print(f"🚀 Dashboard started at http://{host}:{port}")
        print("Press Ctrl+C to stop")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            server.stop()

def show_status(dashboard, format):
    """Show dashboard status"""
    data = dashboard.get_dashboard_data()
    
    if format == "json":
        print(json.dumps(data, indent=2))
    else:
        summary = data["summary"]
        print("🐝 Swarm Coordination Dashboard Status")
        print("=" * 40)
        print(f"Active Agents: {summary['active_agents']}/{summary['total_agents']}")
        print(f"Completed Tasks: {summary['completed_tasks']}/{summary['total_tasks']}")
        print(f"Completion Rate: {summary['completion_rate']:.1f}%")
        print(f"Pending Alerts: {summary['pending_alerts']}")
        print(f"Last Update: {summary['last_update']}")

def show_agents(dashboard, agent_id, format):
    """Show agent status"""
    if agent_id:
        agent = dashboard.get_agent_status(agent_id)
        if not agent:
            print(f"Agent {agent_id} not found")
            return
        
        if format == "json":
            data = {
                "agent_id": agent.agent_id,
                "status": agent.status.value,
                "current_task": agent.current_task,
                "last_activity": agent.last_activity.isoformat(),
                "performance_score": agent.performance_score,
                "message_count": agent.message_count,
                "error_count": agent.error_count
            }
            print(json.dumps(data, indent=2))
        else:
            print(f"🤖 Agent {agent.agent_id}")
            print("=" * 20)
            print(f"Status: {agent.status.value.upper()}")
            print(f"Current Task: {agent.current_task or 'None'}")
            print(f"Last Activity: {agent.last_activity}")
            print(f"Performance Score: {agent.performance_score}%")
            print(f"Message Count: {agent.message_count}")
            print(f"Error Count: {agent.error_count}")
    else:
        agents = dashboard.get_all_agent_status()
        
        if format == "json":
            data = {
                agent_id: {
                    "agent_id": agent.agent_id,
                    "status": agent.status.value,
                    "current_task": agent.current_task,
                    "performance_score": agent.performance_score
                }
                for agent_id, agent in agents.items()
            }
            print(json.dumps(data, indent=2))
        else:
            print("🤖 Agent Status")
            print("=" * 20)
            for agent_id, agent in agents.items():
                print(f"{agent_id}: {agent.status.value.upper()} - {agent.current_task or 'No task'} ({agent.performance_score}%)")

def show_tasks(dashboard, task_id, format):
    """Show task status"""
    if task_id:
        task = dashboard.get_task_status(task_id)
        if not task:
            print(f"Task {task_id} not found")
            return
        
        if format == "json":
            data = {
                "task_id": task.task_id,
                "title": task.title,
                "status": task.status.value,
                "assigned_agent": task.assigned_agent,
                "priority": task.priority,
                "progress": task.progress,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
            print(json.dumps(data, indent=2))
        else:
            print(f"📋 Task {task.task_id}")
            print("=" * 20)
            print(f"Title: {task.title}")
            print(f"Status: {task.status.value.upper()}")
            print(f"Assigned Agent: {task.assigned_agent}")
            print(f"Priority: {task.priority}")
            print(f"Progress: {task.progress}%")
            print(f"Created: {task.created_at}")
            print(f"Updated: {task.updated_at}")
    else:
        tasks = dashboard.get_all_task_status()
        
        if format == "json":
            data = {
                task_id: {
                    "task_id": task.task_id,
                    "title": task.title,
                    "status": task.status.value,
                    "assigned_agent": task.assigned_agent,
                    "progress": task.progress
                }
                for task_id, task in tasks.items()
            }
            print(json.dumps(data, indent=2))
        else:
            print("📋 Task Status")
            print("=" * 20)
            for task_id, task in tasks.items():
                print(f"{task_id}: {task.title} - {task.status.value.upper()} ({task.progress}%) - {task.assigned_agent}")

def show_alerts(dashboard, acknowledge_id, format):
    """Show alerts"""
    if acknowledge_id:
        dashboard.acknowledge_alert(acknowledge_id)
        print(f"✅ Alert {acknowledge_id} acknowledged")
        return
    
    alerts = dashboard.get_alerts()
    
    if format == "json":
        print(json.dumps(alerts, indent=2))
    else:
        if not alerts:
            print("🚨 No active alerts")
        else:
            print("🚨 Active Alerts")
            print("=" * 20)
            for alert in alerts:
                status = "✅" if alert["acknowledged"] else "⚠️"
                print(f"{status} {alert['type'].upper()}: {alert['message']}")
                print(f"   Agent: {alert.get('agent_id', 'N/A')} | Time: {alert['timestamp']}")
                print()

def add_alert(dashboard, alert_type, message, agent_id):
    """Add new alert"""
    dashboard.add_alert(alert_type, message, agent_id)
    print(f"✅ Alert added: {alert_type.upper()} - {message}")

def update_agent(dashboard, agent_id, status, current_task, performance_score):
    """Update agent status"""
    from src.services.dashboard import AgentStatus
    agent_status = AgentStatus(status)
    dashboard.update_agent_status(agent_id, agent_status, current_task, performance_score)
    print(f"✅ Agent {agent_id} updated: {status.upper()}")

if __name__ == "__main__":
    main()


