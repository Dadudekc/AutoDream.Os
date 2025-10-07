"""
Overnight Runner Tests - V2 Compliant
=====================================

Comprehensive test suite for the Overnight Autonomous Runner.
Maintains 100% test pass rate and V2 compliance standards.

Author: Agent-1 - Autonomous Operations Specialist
License: MIT
"""

import pytest
from src.orchestrators.overnight.orchestrator import OvernightOrchestrator
from src.orchestrators.overnight.scheduler import TaskScheduler, Task
from src.orchestrators.overnight.monitor import ProgressMonitor
from src.orchestrators.overnight.recovery import RecoverySystem


class TestOvernightOrchestrator:
    """Test overnight orchestrator."""

    def test_orchestrator_initialization(self):
        """Test orchestrator initialization."""
        orchestrator = OvernightOrchestrator()

        assert orchestrator.enabled
        assert orchestrator.cycle_interval == 10
        assert orchestrator.max_cycles == 60
        assert not orchestrator.is_running

    def test_orchestrator_status(self):
        """Test orchestrator status retrieval."""
        orchestrator = OvernightOrchestrator()
        status = orchestrator.get_orchestrator_status()

        assert "enabled" in status
        assert "is_running" in status
        assert "current_cycle" in status
        assert "max_cycles" in status


class TestTaskScheduler:
    """Test task scheduler."""

    def test_scheduler_initialization(self):
        """Test scheduler initialization."""
        scheduler = TaskScheduler()

        assert scheduler.strategy == "cycle_based"
        assert scheduler.priority_queue
        assert scheduler.load_balancing

    def test_add_task(self):
        """Test adding tasks."""
        scheduler = TaskScheduler()

        success = scheduler.add_task(
            task_id="test_task",
            task_type="monitoring",
            agent_id="Agent-1",
            data={"key": "value"},
        )

        assert success
        assert "test_task" in scheduler.task_registry

    def test_task_priority_ordering(self):
        """Test task priority ordering."""
        task1 = Task(id="task1", type="monitoring", priority=5, agent_id="Agent-1")
        task2 = Task(id="task2", type="system_health", priority=1, agent_id="Agent-2")

        # Lower priority number should come first
        assert task2 < task1

    def test_scheduler_status(self):
        """Test scheduler status retrieval."""
        scheduler = TaskScheduler()
        status = scheduler.get_scheduler_status()

        assert "strategy" in status
        assert "priority_queue" in status
        assert "queue_size" in status
        assert "completed_tasks" in status


class TestProgressMonitor:
    """Test progress monitor."""

    def test_monitor_initialization(self):
        """Test monitor initialization."""
        monitor = ProgressMonitor()

        assert monitor.check_interval == 60
        assert monitor.stall_timeout == 300
        assert not monitor.is_monitoring

    def test_start_stop_monitoring(self):
        """Test starting and stopping monitoring."""
        monitor = ProgressMonitor()

        monitor.start_monitoring()
        assert monitor.is_monitoring

        monitor.stop_monitoring()
        assert not monitor.is_monitoring

    def test_monitor_status(self):
        """Test monitor information retrieval."""
        monitor = ProgressMonitor()
        info = monitor.get_monitor_info()

        assert "monitoring_active" in info
        assert "check_interval" in info
        assert "stall_timeout" in info

    def test_performance_metrics(self):
        """Test performance metrics calculation."""
        monitor = ProgressMonitor()
        monitor.start_monitoring()

        metrics = monitor.get_performance_metrics()

        assert "cycles_completed" in metrics
        assert "total_tasks" in metrics
        assert "uptime_seconds" in metrics


class TestRecoverySystem:
    """Test recovery system."""

    def test_recovery_initialization(self):
        """Test recovery system initialization."""
        recovery = RecoverySystem()

        assert recovery.max_retries == 3
        assert recovery.escalation_threshold == 5
        assert recovery.auto_recovery

    def test_recovery_status(self):
        """Test recovery status retrieval."""
        recovery = RecoverySystem()
        status = recovery.get_recovery_status()

        assert "max_retries" in status
        assert "escalation_threshold" in status
        assert "auto_recovery" in status
        assert "failure_history_count" in status

