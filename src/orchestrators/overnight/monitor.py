"""
Progress Monitor - V2 Compliant
===============================

Progress monitoring and health tracking for overnight operations.
Provides agent activity monitoring, stall detection, and status reporting.

V2 Compliance: ≤400 lines, SOLID principles, comprehensive error handling.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import time
from typing import Dict, List, Optional, Any
import logging

# V2 Integration imports
try:
    from ...core.unified_config import get_unified_config
    from ...core.unified_logging_system import get_logger
except ImportError as e:
    logging.warning(f"V2 integration imports failed: {e}")
    # Fallback implementations
    def get_unified_config():
        return type('MockConfig', (), {'get_env': lambda x, y=None: y})()
    
    def get_logger(name):
        return logging.getLogger(name)


class ProgressMonitor:
    """
    Progress monitoring for overnight operations.
    
    Provides:
    - Agent activity tracking
    - Stall detection
    - Health status monitoring
    - Performance metrics
    - Status reporting
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize progress monitor.
        
        Args:
            config: Configuration dictionary (uses config/orchestration.yml if None)
        """
        self.config = config or {}
        self.logger = get_logger(__name__)
        
        # V2 Integration
        self.unified_config = get_unified_config()
        
        # Monitoring settings
        monitoring_config = self.config.get('overnight', {}).get('monitoring', {})
        self.check_interval = monitoring_config.get('check_interval', 60)  # seconds
        self.stall_timeout = monitoring_config.get('stall_timeout', 300)  # seconds
        self.health_checks = monitoring_config.get('health_checks', True)
        self.performance_tracking = monitoring_config.get('performance_tracking', True)
        
        # State
        self.is_monitoring = False
        self.start_time = 0
        self.current_cycle = 0
        self.cycle_start_times = {}
        self.agent_activity = {}  # Agent ID -> last activity timestamp
        self.agent_tasks = {}  # Agent ID -> current task
        self.performance_metrics = {
            'cycles_completed': 0,
            'total_tasks': 0,
            'completed_tasks': 0,
            'failed_tasks': 0,
            'average_cycle_time': 0,
            'average_task_time': 0,
        }
        self.health_status = {
            'healthy': True,
            'issues': [],
            'last_check': 0,
        }
        
        self.logger.info("Progress Monitor initialized")

    def start_monitoring(self) -> None:
        """Start progress monitoring."""
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.start_time = time.time()
        
        # Initialize agent activity tracking
        current_time = time.time()
        for i in range(1, 9):
            agent_id = f"Agent-{i}"
            self.agent_activity[agent_id] = current_time
            self.agent_tasks[agent_id] = None
        
        self.logger.info("Progress monitoring started")

    def stop_monitoring(self) -> None:
        """Stop progress monitoring."""
        if not self.is_monitoring:
            return
        
        self.is_monitoring = False
        self.logger.info("Progress monitoring stopped")

    def update_cycle(self, cycle_number: int, cycle_start_time: float) -> None:
        """Update cycle information."""
        self.current_cycle = cycle_number
        self.cycle_start_times[cycle_number] = cycle_start_time
        
        # Update performance metrics
        if cycle_number > 1:
            # Calculate average cycle time
            cycle_times = []
            for i in range(1, cycle_number):
                if i in self.cycle_start_times and i + 1 in self.cycle_start_times:
                    cycle_time = self.cycle_start_times[i + 1] - self.cycle_start_times[i]
                    cycle_times.append(cycle_time)
            
            if cycle_times:
                self.performance_metrics['average_cycle_time'] = sum(cycle_times) / len(cycle_times)
        
        self.performance_metrics['cycles_completed'] = cycle_number
        self.logger.info(f"Cycle {cycle_number} updated")

    def update_tasks(self, tasks: List[Dict[str, Any]]) -> None:
        """Update task information."""
        current_time = time.time()
        
        for task in tasks:
            agent_id = task.get('agent_id')
            task_id = task.get('id')
            
            if agent_id:
                # Update agent activity
                self.agent_activity[agent_id] = current_time
                self.agent_tasks[agent_id] = task_id
        
        # Update performance metrics
        self.performance_metrics['total_tasks'] += len(tasks)
        
        self.logger.debug(f"Updated {len(tasks)} tasks")

    def mark_task_completed(self, task_id: str, agent_id: str, duration: float) -> None:
        """Mark a task as completed."""
        self.performance_metrics['completed_tasks'] += 1
        
        # Update average task time
        total_completed = self.performance_metrics['completed_tasks']
        current_avg = self.performance_metrics['average_task_time']
        self.performance_metrics['average_task_time'] = (
            (current_avg * (total_completed - 1) + duration) / total_completed
        )
        
        # Clear agent task
        if agent_id in self.agent_tasks:
            self.agent_tasks[agent_id] = None
        
        self.logger.info(f"Task completed: {task_id} by {agent_id} in {duration:.1f}s")

    def mark_task_failed(self, task_id: str, agent_id: str, error: str) -> None:
        """Mark a task as failed."""
        self.performance_metrics['failed_tasks'] += 1
        
        # Clear agent task
        if agent_id in self.agent_tasks:
            self.agent_tasks[agent_id] = None
        
        self.logger.error(f"Task failed: {task_id} by {agent_id} - {error}")

    async def get_stalled_agents(self) -> List[str]:
        """Get list of agents that appear to be stalled."""
        stalled_agents = []
        current_time = time.time()
        
        for agent_id, last_activity in self.agent_activity.items():
            if current_time - last_activity > self.stall_timeout:
                stalled_agents.append(agent_id)
        
        if stalled_agents:
            self.logger.warning(f"Detected stalled agents: {stalled_agents}")
        
        return stalled_agents

    async def get_health_status(self) -> Dict[str, Any]:
        """Get current system health status."""
        current_time = time.time()
        
        # Check agent activity
        stalled_agents = await self.get_stalled_agents()
        
        # Check task completion rate
        total_tasks = self.performance_metrics['total_tasks']
        completed_tasks = self.performance_metrics['completed_tasks']
        failed_tasks = self.performance_metrics['failed_tasks']
        
        completion_rate = 0
        if total_tasks > 0:
            completion_rate = completed_tasks / total_tasks
        
        failure_rate = 0
        if total_tasks > 0:
            failure_rate = failed_tasks / total_tasks
        
        # Determine health status
        health_issues = []
        healthy = True
        
        if stalled_agents:
            health_issues.append(f"Stalled agents: {stalled_agents}")
            healthy = False
        
        if failure_rate > 0.3:  # More than 30% failure rate
            health_issues.append(f"High failure rate: {failure_rate:.1%}")
            healthy = False
        
        if completion_rate < 0.5:  # Less than 50% completion rate
            health_issues.append(f"Low completion rate: {completion_rate:.1%}")
            healthy = False
        
        # Update health status
        self.health_status = {
            'healthy': healthy,
            'issues': health_issues,
            'last_check': current_time,
            'completion_rate': completion_rate,
            'failure_rate': failure_rate,
            'stalled_agents': stalled_agents,
        }
        
        return self.health_status

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        current_time = time.time()
        uptime = current_time - self.start_time if self.start_time > 0 else 0
        
        # Calculate rates
        cycles_per_hour = 0
        tasks_per_hour = 0
        
        if uptime > 0:
            cycles_per_hour = (self.current_cycle * 3600) / uptime
            tasks_per_hour = (self.performance_metrics['total_tasks'] * 3600) / uptime
        
        return {
            **self.performance_metrics,
            'uptime_seconds': uptime,
            'uptime_hours': uptime / 3600,
            'cycles_per_hour': cycles_per_hour,
            'tasks_per_hour': tasks_per_hour,
            'current_cycle': self.current_cycle,
            'active_agents': len([a for a, task in self.agent_tasks.items() if task is not None]),
        }

    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        current_time = time.time()
        agent_status = {}
        
        for agent_id in self.agent_activity:
            last_activity = self.agent_activity[agent_id]
            current_task = self.agent_tasks[agent_id]
            
            # Determine agent status
            time_since_activity = current_time - last_activity
            
            if time_since_activity > self.stall_timeout:
                status = 'stalled'
            elif current_task:
                status = 'busy'
            else:
                status = 'idle'
            
            agent_status[agent_id] = {
                'status': status,
                'last_activity': last_activity,
                'time_since_activity': time_since_activity,
                'current_task': current_task,
            }
        
        return agent_status

    def generate_status_report(self) -> Dict[str, Any]:
        """Generate comprehensive status report."""
        current_time = time.time()
        
        return {
            'timestamp': current_time,
            'monitoring_active': self.is_monitoring,
            'uptime_seconds': current_time - self.start_time if self.start_time > 0 else 0,
            'current_cycle': self.current_cycle,
            'performance_metrics': self.get_performance_metrics(),
            'health_status': self.health_status,
            'agent_status': self.get_agent_status(),
            'configuration': {
                'check_interval': self.check_interval,
                'stall_timeout': self.stall_timeout,
                'health_checks': self.health_checks,
                'performance_tracking': self.performance_tracking,
            }
        }

    def get_monitor_info(self) -> Dict[str, Any]:
        """Get information about monitor capabilities."""
        return {
            "monitoring_active": self.is_monitoring,
            "check_interval": self.check_interval,
            "stall_timeout": self.stall_timeout,
            "health_checks": self.health_checks,
            "performance_tracking": self.performance_tracking,
            "start_time": self.start_time,
            "current_cycle": self.current_cycle,
            "tracked_agents": len(self.agent_activity),
        }
