#!/usr/bin/env python3
"""
AI/ML Orchestrator - Agent Cellphone V2
=======================================

Coordinates AI/ML system components and provides system-wide orchestration
for AI/ML operations. Follows V2 standards: OOP, SRP, clean code.

Author: Agent-5 (REFACTORING MANAGER)
License: MIT
"""

import logging
import threading
import time
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass

from src.core.base_manager import BaseManager
from .unified_ai_ml_manager import UnifiedAIMLManager, AIModel, AIAgent, APIKey, Workflow


@dataclass
class OrchestrationTask:
    """AI/ML orchestration task"""
    task_id: str
    task_type: str  # 'model_management', 'agent_coordination', 'workflow_execution'
    priority: int
    data: Dict[str, Any]
    created_at: datetime
    status: str = "pending"  # pending, running, completed, failed
    assigned_agent: Optional[str] = None
    result: Optional[Any] = None


@dataclass
class SystemHealth:
    """AI/ML system health status"""
    overall_health: str
    models_health: str
    agents_health: str
    api_keys_health: str
    workflows_health: str
    last_check: datetime
    issues: List[str]


class AIMLOrchestrator(BaseManager):
    """
    AI/ML Orchestrator - Coordinates AI/ML system components
    
    This orchestrator provides:
    - Component lifecycle management
    - Inter-component communication
    - System health monitoring
    - Performance optimization
    - Task distribution and coordination
    """

    def __init__(self, config_path: str = "config/ai_ml/ai_ml_orchestrator.json"):
        super().__init__(
            manager_id="ai_ml_orchestrator",
            name="AIMLOrchestrator",
            description="AI/ML system orchestration and coordination"
        )
        
        # Core AI/ML manager
        self.ai_ml_manager = UnifiedAIMLManager()
        
        # Orchestration state
        self.tasks: Dict[str, OrchestrationTask] = {}
        self.task_queue: List[str] = []
        self.active_tasks: Dict[str, str] = {}  # agent_id -> task_id
        
        # Health monitoring
        self.health_status = SystemHealth(
            overall_health="unknown",
            models_health="unknown",
            agents_health="unknown",
            api_keys_health="unknown",
            workflows_health="unknown",
            last_check=datetime.now(),
            issues=[]
        )
        
        # Performance tracking
        self.performance_metrics: Dict[str, Dict[str, Any]] = {
            "task_processing": {"total": 0, "successful": 0, "failed": 0, "avg_time": 0.0},
            "system_health": {"checks": 0, "issues_found": 0, "last_optimization": None},
            "resource_utilization": {"models": 0.0, "agents": 0.0, "workflows": 0.0}
        }
        
        # Monitoring thread
        self.monitoring_thread: Optional[threading.Thread] = None
        self.monitoring_active = False
        
        # Load configuration
        self._load_manager_config()
        
        # Initialize orchestration
        self._initialize_orchestration()
        
        self.logger.info("✅ AI/ML Orchestrator initialized successfully")

    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if self.config:
                orchestration_config = self.config.get("orchestration", {})
                
                # Load monitoring settings
                self.monitoring_interval = orchestration_config.get("monitoring_interval", 30)
                self.health_check_interval = orchestration_config.get("health_check_interval", 60)
                self.optimization_interval = orchestration_config.get("optimization_interval", 300)
                
                self.logger.info("Orchestration configuration loaded successfully")
                
        except Exception as e:
            self.logger.error(f"Error loading orchestration config: {e}")

    def _initialize_orchestration(self):
        """Initialize orchestration system"""
        try:
            # Start monitoring thread
            self._start_monitoring()
            
            # Perform initial health check
            self._perform_health_check()
            
            # Initialize performance tracking
            self._initialize_performance_tracking()
            
            self.logger.info("Orchestration system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Error initializing orchestration: {e}")

    def _start_monitoring(self):
        """Start monitoring thread"""
        try:
            if not self.monitoring_active:
                self.monitoring_active = True
                self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
                self.monitoring_thread.start()
                self.logger.info("Monitoring thread started")
                
        except Exception as e:
            self.logger.error(f"Error starting monitoring thread: {e}")

    def _monitoring_loop(self):
        """Main monitoring loop"""
        try:
            while self.monitoring_active:
                # Perform health check
                self._perform_health_check()
                
                # Update performance metrics
                self._update_performance_metrics()
                
                # Check for optimization opportunities
                self._check_optimization_opportunities()
                
                # Process pending tasks
                self._process_pending_tasks()
                
                # Sleep for monitoring interval
                time.sleep(self.monitoring_interval)
                
        except Exception as e:
            self.logger.error(f"Error in monitoring loop: {e}")
            self.monitoring_active = False

    def _perform_health_check(self):
        """Perform comprehensive health check"""
        try:
            self.health_status.last_check = datetime.now()
            issues = []
            
            # Check models health
            models_status = self.ai_ml_manager.get_system_status()
            if models_status["total_models"] == 0:
                self.health_status.models_health = "critical"
                issues.append("No AI models registered")
            elif models_status["active_models"] < models_status["total_models"] * 0.8:
                self.health_status.models_health = "warning"
                issues.append("Some AI models are inactive")
            else:
                self.health_status.models_health = "healthy"
            
            # Check agents health
            if models_status["total_agents"] == 0:
                self.health_status.agents_health = "critical"
                issues.append("No AI agents registered")
            elif models_status["active_agents"] < models_status["total_agents"] * 0.8:
                self.health_status.agents_health = "warning"
                issues.append("Some AI agents are inactive")
            else:
                self.health_status.agents_health = "healthy"
            
            # Check API keys health
            if models_status["total_api_keys"] == 0:
                self.health_status.api_keys_health = "warning"
                issues.append("No API keys configured")
            else:
                self.health_status.api_keys_health = "healthy"
            
            # Check workflows health
            if models_status["total_workflows"] == 0:
                self.health_status.workflows_health = "warning"
                issues.append("No workflows configured")
            else:
                self.health_status.workflows_health = "healthy"
            
            # Determine overall health
            health_scores = [
                self.health_status.models_health,
                self.health_status.agents_health,
                self.health_status.api_keys_health,
                self.health_status.workflows_health
            ]
            
            if "critical" in health_scores:
                self.health_status.overall_health = "critical"
            elif "warning" in health_scores:
                self.health_status.overall_health = "warning"
            else:
                self.health_status.overall_health = "healthy"
            
            # Update issues list
            self.health_status.issues = issues
            
            # Update performance metrics
            self.performance_metrics["system_health"]["checks"] += 1
            if issues:
                self.performance_metrics["system_health"]["issues_found"] += len(issues)
            
            self.logger.info(f"Health check completed: {self.health_status.overall_health}")
            
        except Exception as e:
            self.logger.error(f"Error performing health check: {e}")
            self.health_status.overall_health = "error"

    def _update_performance_metrics(self):
        """Update performance metrics"""
        try:
            # Update task processing metrics
            total_tasks = len(self.tasks)
            completed_tasks = len([t for t in self.tasks.values() if t.status == "completed"])
            failed_tasks = len([t for t in self.tasks.values() if t.status == "failed"])
            
            self.performance_metrics["task_processing"]["total"] = total_tasks
            self.performance_metrics["task_processing"]["successful"] = completed_tasks
            self.performance_metrics["task_processing"]["failed"] = failed_tasks
            
            # Update resource utilization
            system_status = self.ai_ml_manager.get_system_status()
            total_agents = system_status["total_agents"]
            active_agents = system_status["active_agents"]
            
            if total_agents > 0:
                self.performance_metrics["resource_utilization"]["agents"] = active_agents / total_agents
            else:
                self.performance_metrics["resource_utilization"]["agents"] = 0.0
            
            # Calculate average task processing time
            if completed_tasks > 0:
                # This would be calculated from actual task timing data
                self.performance_metrics["task_processing"]["avg_time"] = 0.0
            
        except Exception as e:
            self.logger.error(f"Error updating performance metrics: {e}")

    def _check_optimization_opportunities(self):
        """Check for optimization opportunities"""
        try:
            current_time = datetime.now()
            last_optimization = self.performance_metrics["system_health"]["last_optimization"]
            
            # Check if it's time for optimization
            if (last_optimization is None or 
                (current_time - last_optimization).total_seconds() > self.optimization_interval):
                
                self._perform_system_optimization()
                self.performance_metrics["system_health"]["last_optimization"] = current_time
                
        except Exception as e:
            self.logger.error(f"Error checking optimization opportunities: {e}")

    def _perform_system_optimization(self):
        """Perform system optimization"""
        try:
            self.logger.info("Performing system optimization...")
            
            # Optimize agent workload distribution
            self._optimize_agent_workloads()
            
            # Optimize model usage
            self._optimize_model_usage()
            
            # Clean up completed tasks
            self._cleanup_completed_tasks()
            
            self.logger.info("System optimization completed")
            
        except Exception as e:
            self.logger.error(f"Error performing system optimization: {e}")

    def _optimize_agent_workloads(self):
        """Optimize agent workload distribution"""
        try:
            agents = self.ai_ml_manager.list_agents()
            
            # Find agents with high workload
            high_workload_agents = [a for a in agents if a.current_workload > a.workload_capacity * 0.8]
            
            # Find agents with low workload
            low_workload_agents = [a for a in agents if a.current_workload < a.workload_capacity * 0.3]
            
            # Redistribute tasks if possible
            if high_workload_agents and low_workload_agents:
                self.logger.info(f"Redistributing workload from {len(high_workload_agents)} high-load agents to {len(low_workload_agents)} low-load agents")
                
        except Exception as e:
            self.logger.error(f"Error optimizing agent workloads: {e}")

    def _optimize_model_usage(self):
        """Optimize model usage patterns"""
        try:
            models = self.ai_ml_manager.list_models()
            
            # Check for unused models
            unused_models = [m for m in models if m.usage_count == 0 and m.is_active]
            
            if unused_models:
                self.logger.info(f"Found {len(unused_models)} unused models")
                
                # Could implement model deactivation or resource cleanup here
                
        except Exception as e:
            self.logger.error(f"Error optimizing model usage: {e}")

    def _cleanup_completed_tasks(self):
        """Clean up completed tasks"""
        try:
            # Remove completed tasks older than 24 hours
            cutoff_time = datetime.now() - timedelta(hours=24)
            tasks_to_remove = []
            
            for task_id, task in self.tasks.items():
                if (task.status in ["completed", "failed"] and 
                    task.created_at < cutoff_time):
                    tasks_to_remove.append(task_id)
            
            for task_id in tasks_to_remove:
                del self.tasks[task_id]
                if task_id in self.task_queue:
                    self.task_queue.remove(task_id)
            
            if tasks_to_remove:
                self.logger.info(f"Cleaned up {len(tasks_to_remove)} old tasks")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up completed tasks: {e}")

    def _process_pending_tasks(self):
        """Process pending tasks"""
        try:
            # Get available agents
            available_agents = [a for a in self.ai_ml_manager.list_agents() 
                              if a.is_active and a.current_workload < a.workload_capacity * 0.8]
            
            # Process pending tasks
            pending_tasks = [task_id for task_id in self.task_queue 
                           if self.tasks[task_id].status == "pending"]
            
            for task_id in pending_tasks[:len(available_agents)]:
                if available_agents:
                    agent = available_agents.pop(0)
                    self._assign_task_to_agent(task_id, agent.agent_id)
                    
        except Exception as e:
            self.logger.error(f"Error processing pending tasks: {e}")

    def _assign_task_to_agent(self, task_id: str, agent_id: str):
        """Assign a task to an agent"""
        try:
            if task_id in self.tasks and agent_id not in self.active_tasks:
                task = self.tasks[task_id]
                task.status = "running"
                task.assigned_agent = agent_id
                
                self.active_tasks[agent_id] = task_id
                
                # Update agent workload
                self.ai_ml_manager.assign_task_to_agent(agent_id, 1)
                
                self.logger.info(f"Assigned task {task_id} to agent {agent_id}")
                
        except Exception as e:
            self.logger.error(f"Error assigning task to agent: {e}")

    # ============================================================================
    # Public Orchestration Interface
    # ============================================================================
    
    def submit_task(self, task_type: str, priority: int, data: Dict[str, Any]) -> str:
        """Submit a new orchestration task"""
        try:
            task_id = f"task_{int(datetime.now().timestamp())}_{len(self.tasks)}"
            
            task = OrchestrationTask(
                task_id=task_id,
                task_type=task_type,
                priority=priority,
                data=data,
                created_at=datetime.now()
            )
            
            self.tasks[task_id] = task
            self.task_queue.append(task_id)
            
            # Sort queue by priority (higher priority first)
            self.task_queue.sort(key=lambda tid: self.tasks[tid].priority, reverse=True)
            
            # Update metrics
            self.metrics.total_operations += 1
            self.metrics.successful_operations += 1
            
            # Emit task submitted event
            self.emit_event("task_submitted", {
                "task_id": task_id,
                "task_type": task_type,
                "priority": priority
            })
            
            self.logger.info(f"Submitted task: {task_type} (priority: {priority})")
            return task_id
            
        except Exception as e:
            self.logger.error(f"Error submitting task: {e}")
            self.metrics.failed_operations += 1
            return ""

    def get_task_status(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get task status"""
        try:
            if task_id in self.tasks:
                task = self.tasks[task_id]
                return {
                    "task_id": task.task_id,
                    "type": task.task_type,
                    "priority": task.priority,
                    "status": task.status,
                    "assigned_agent": task.assigned_agent,
                    "created_at": task.created_at.isoformat(),
                    "result": task.result
                }
            return None
            
        except Exception as e:
            self.logger.error(f"Error getting task status: {e}")
            return None

    def get_system_health(self) -> Dict[str, Any]:
        """Get system health status"""
        try:
            return {
                "overall_health": self.health_status.overall_health,
                "models_health": self.health_status.models_health,
                "agents_health": self.health_status.agents_health,
                "api_keys_health": self.health_status.api_keys_health,
                "workflows_health": self.health_status.workflows_health,
                "last_check": self.health_status.last_check.isoformat(),
                "issues": self.health_status.issues,
                "performance_metrics": self.performance_metrics
            }
            
        except Exception as e:
            self.logger.error(f"Error getting system health: {e}")
            return {"error": str(e)}

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        try:
            return {
                "task_processing": self.performance_metrics["task_processing"],
                "system_health": self.performance_metrics["system_health"],
                "resource_utilization": self.performance_metrics["resource_utilization"],
                "ai_ml_manager_status": self.ai_ml_manager.get_system_status()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {e}")
            return {"error": str(e)}

    def force_health_check(self):
        """Force an immediate health check"""
        try:
            self.logger.info("Forcing immediate health check...")
            self._perform_health_check()
            self.logger.info("Forced health check completed")
            
        except Exception as e:
            self.logger.error(f"Error during forced health check: {e}")

    def force_optimization(self):
        """Force an immediate system optimization"""
        try:
            self.logger.info("Forcing immediate system optimization...")
            self._perform_system_optimization()
            self.logger.info("Forced optimization completed")
            
        except Exception as e:
            self.logger.error(f"Error during forced optimization: {e}")

    # ============================================================================
    # BaseManager Abstract Method Implementations
    # ============================================================================
    
    def _on_start(self) -> bool:
        """Start the orchestrator"""
        try:
            self.logger.info("Starting AI/ML Orchestrator...")
            
            # Ensure monitoring is active
            if not self.monitoring_active:
                self._start_monitoring()
            
            # Perform initial health check
            self._perform_health_check()
            
            self.logger.info("AI/ML Orchestrator started successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start AI/ML Orchestrator: {e}")
            return False

    def _on_stop(self):
        """Stop the orchestrator"""
        try:
            self.logger.info("Stopping AI/ML Orchestrator...")
            
            # Stop monitoring
            self.monitoring_active = False
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            self.logger.info("AI/ML Orchestrator stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Error during AI/ML Orchestrator shutdown: {e}")

    def _on_heartbeat(self):
        """Orchestrator heartbeat"""
        try:
            # Check if monitoring is active
            if not self.monitoring_active:
                self.logger.warning("Monitoring thread is not active, restarting...")
                self._start_monitoring()
            
            # Quick health status check
            if self.health_status.overall_health == "critical":
                self.logger.warning("System health is critical, performing emergency optimization")
                self._perform_system_optimization()
                
        except Exception as e:
            self.logger.error(f"Heartbeat error: {e}")

    def _on_initialize_resources(self) -> bool:
        """Initialize orchestrator resources"""
        try:
            # Initialize AI/ML manager if needed
            if not hasattr(self, 'ai_ml_manager') or self.ai_ml_manager is None:
                self.ai_ml_manager = UnifiedAIMLManager()
            
            # Initialize performance tracking
            self._initialize_performance_tracking()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Resource initialization failed: {e}")
            return False

    def _on_cleanup_resources(self):
        """Cleanup orchestrator resources"""
        try:
            # Cleanup tasks
            self.tasks.clear()
            self.task_queue.clear()
            self.active_tasks.clear()
            
            # Cleanup performance metrics
            self.performance_metrics.clear()
            
            # Cleanup AI/ML manager
            if hasattr(self, 'ai_ml_manager') and self.ai_ml_manager:
                self.ai_ml_manager.cleanup()
                
        except Exception as e:
            self.logger.error(f"Resource cleanup error: {e}")

    def _initialize_performance_tracking(self):
        """Initialize performance tracking"""
        try:
            self.performance_metrics = {
                "task_processing": {"total": 0, "successful": 0, "failed": 0, "avg_time": 0.0},
                "system_health": {"checks": 0, "issues_found": 0, "last_optimization": None},
                "resource_utilization": {"models": 0.0, "agents": 0.0, "workflows": 0.0}
            }
            
        except Exception as e:
            self.logger.error(f"Error initializing performance tracking: {e}")

    def cleanup(self):
        """Cleanup resources"""
        try:
            # Stop monitoring
            self.monitoring_active = False
            if self.monitoring_thread and self.monitoring_thread.is_alive():
                self.monitoring_thread.join(timeout=5)
            
            # Cleanup tasks and metrics
            self._on_cleanup_resources()
            
            self.logger.info("AI/ML Orchestrator cleaned up successfully")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


# Global instance
ai_ml_orchestrator = AIMLOrchestrator()
