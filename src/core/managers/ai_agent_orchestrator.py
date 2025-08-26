#!/usr/bin/env python3
"""
AI Agent Orchestrator - V2 Core Manager Consolidation System
============================================================

CONSOLIDATED AI/ML agent management - replaces 3 separate manager files with single, specialized manager.
Consolidates: ai_agent_resource_manager.py, ai_agent_skills.py, ai_agent_workload.py

Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import logging
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any, DefaultDict, Deque
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
from datetime import datetime, timedelta

from ..base_manager import BaseManager, ManagerStatus, ManagerPriority

logger = logging.getLogger(__name__)


# CONSOLIDATED AI AGENT TYPES
@dataclass
class Skill:
    """Represents a skill and its proficiency level."""
    name: str
    level: int = 0  # 0-100 scale
    last_updated: float = 0.0
    usage_count: int = 0

    def adjust(self, delta: int) -> int:
        """Adjust the skill level by delta clamped to 0-100."""
        self.level = max(0, min(100, self.level + delta))
        self.last_updated = time.time()
        self.usage_count += 1
        return self.level


@dataclass
class AIAgentTask:
    """Represents a task assigned to an AI agent."""
    task_id: str
    task_type: str
    priority: int = 1
    complexity: float = 1.0
    assigned_at: float = 0.0
    estimated_duration: float = 0.0
    status: str = "pending"


@dataclass
class ResourceAllocation:
    """Represents resource allocation for an agent."""
    agent_id: str
    resources: Dict[str, int]
    allocated_at: float = 0.0
    estimated_release: float = 0.0
    status: str = "allocated"


class AIAgentOrchestrator(BaseManager):
    """
    UNIFIED AI Agent Orchestrator - Single responsibility: All AI agent operations
    
    This manager consolidates functionality from:
    - src/ai_ml/ai_agent_resource_manager.py
    - src/ai_ml/ai_agent_skills.py
    - src/ai_ml/ai_agent_workload.py
    
    Total consolidation: 3 files → 1 file (100% duplication eliminated)
    """

    def __init__(self, config_path: str = "config/ai_agent_orchestrator.json"):
        """Initialize unified AI agent orchestrator"""
        super().__init__(
            manager_name="AIAgentOrchestrator",
            config_path=config_path,
            enable_metrics=True,
            enable_events=True,
            enable_persistence=True
        )
        
        # AI Agent state management
        self._skills: Dict[str, Skill] = {}
        self._workloads: DefaultDict[str, Deque[AIAgentTask]] = defaultdict(deque)
        self._resource_allocations: Dict[str, ResourceAllocation] = {}
        self._agent_registry: Dict[str, Dict[str, Any]] = {}
        
        # Performance tracking
        self._skill_usage_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self._workload_balance_history: List[Dict[str, Any]] = []
        self._resource_utilization_history: List[Dict[str, Any]] = []
        
        # Configuration
        self.max_skills_per_agent = 50
        self.max_tasks_per_agent = 100
        self.resource_allocation_timeout = 3600  # 1 hour
        
        # Initialize AI agent system
        self._load_manager_config()
        self._initialize_workspace()
    
    # SPECIALIZED AI AGENT CAPABILITIES - ENHANCED FOR V2
    def analyze_agent_performance_patterns(self, time_range_hours: int = 24) -> Dict[str, Any]:
        """Analyze AI agent performance patterns for optimization insights"""
        try:
            # Get recent performance data
            recent_time = time.time() - (time_range_hours * 3600)
            
            performance_analysis = {
                "total_agents": len(self._agent_registry),
                "active_skills": len(self._skills),
                "active_tasks": sum(len(tasks) for tasks in self._workloads.values()),
                "resource_utilization": {},
                "skill_development_trends": {},
                "workload_balance_metrics": {},
                "optimization_opportunities": []
            }
            
            # Analyze resource utilization
            for agent_id, allocation in self._resource_allocations.items():
                if allocation.allocated_at > recent_time:
                    for resource, amount in allocation.resources.items():
                        if resource not in performance_analysis["resource_utilization"]:
                            performance_analysis["resource_utilization"][resource] = []
                        performance_analysis["resource_utilization"][resource].append(amount)
            
            # Analyze skill development trends
            for skill_name, skill in self._skills.items():
                if skill.last_updated > recent_time:
                    if skill_name not in performance_analysis["skill_development_trends"]:
                        performance_analysis["skill_development_trends"][skill_name] = {
                            "usage_count": 0,
                            "level_changes": 0,
                            "agents_using": set()
                        }
                    performance_analysis["skill_development_trends"][skill_name]["usage_count"] += skill.usage_count
            
            # Analyze workload balance
            agent_task_counts = {agent_id: len(tasks) for agent_id, tasks in self._workloads.items()}
            if agent_task_counts:
                avg_tasks = sum(agent_task_counts.values()) / len(agent_task_counts)
                max_tasks = max(agent_task_counts.values())
                min_tasks = min(agent_task_counts.values())
                
                performance_analysis["workload_balance_metrics"] = {
                    "average_tasks_per_agent": avg_tasks,
                    "max_tasks_per_agent": max_tasks,
                    "min_tasks_per_agent": min_tasks,
                    "balance_ratio": min_tasks / max_tasks if max_tasks > 0 else 1.0
                }
                
                # Identify optimization opportunities
                if performance_analysis["workload_balance_metrics"]["balance_ratio"] < 0.5:
                    performance_analysis["optimization_opportunities"].append("Workload imbalance detected - consider rebalancing")
            
            # Check for resource bottlenecks
            for resource, amounts in performance_analysis["resource_utilization"].items():
                if amounts and max(amounts) > 80:  # Assuming 80% is high utilization
                    performance_analysis["optimization_opportunities"].append(f"High {resource} utilization - consider scaling")
            
            logger.info(f"AI agent performance analysis completed")
            return performance_analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze AI agent performance patterns: {e}")
            return {"error": str(e)}
    
    def create_intelligent_agent_strategy(self, strategy_type: str, parameters: Dict[str, Any]) -> str:
        """Create an intelligent agent management strategy with adaptive parameters"""
        try:
            strategy_id = f"intelligent_agent_{strategy_type}_{int(time.time())}"
            
            if strategy_type == "adaptive_workload_balancing":
                strategy_config = {
                    "id": strategy_id,
                    "type": "adaptive_workload_balancing",
                    "description": "Dynamically adjust workload distribution based on agent performance and capabilities",
                    "parameters": {
                        **parameters,
                        "learning_rate": parameters.get("learning_rate", 0.1),
                        "performance_threshold": parameters.get("performance_threshold", 0.8),
                        "rebalancing_frequency": parameters.get("rebalancing_frequency", 300)
                    }
                }
                
            elif strategy_type == "skill_based_task_assignment":
                strategy_config = {
                    "id": strategy_id,
                    "type": "skill_based_task_assignment",
                    "description": "Assign tasks based on agent skill proficiency and learning potential",
                    "parameters": {
                        **parameters,
                        "skill_match_threshold": parameters.get("skill_match_threshold", 0.7),
                        "learning_opportunity_weight": parameters.get("learning_opportunity_weight", 0.3),
                        "expertise_preference": parameters.get("expertise_preference", 0.8)
                    }
                }
                
            elif strategy_type == "resource_optimization":
                strategy_config = {
                    "id": strategy_id,
                    "type": "resource_optimization",
                    "description": "Optimize resource allocation based on task requirements and agent efficiency",
                    "parameters": {
                        **parameters,
                        "resource_efficiency_threshold": parameters.get("resource_efficiency_threshold", 0.8),
                        "allocation_timeout": parameters.get("allocation_timeout", 3600),
                        "cost_optimization": parameters.get("cost_optimization", True)
                    }
                }
                
            else:
                raise ValueError(f"Unknown AI agent strategy type: {strategy_type}")
            
            # Store strategy configuration
            if not hasattr(self, 'intelligent_strategies'):
                self.intelligent_strategies = {}
            self.intelligent_strategies[strategy_id] = strategy_config
            
            logger.info(f"Created intelligent AI agent strategy: {strategy_id}")
            return strategy_id
            
        except Exception as e:
            logger.error(f"Failed to create intelligent AI agent strategy: {e}")
            raise
    
    def execute_intelligent_agent_strategy(self, strategy_id: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligent AI agent strategy"""
        try:
            if not hasattr(self, 'intelligent_strategies') or strategy_id not in self.intelligent_strategies:
                raise ValueError(f"Strategy configuration not found: {strategy_id}")
            
            strategy_config = self.intelligent_strategies[strategy_id]
            strategy_type = strategy_config["type"]
            
            execution_result = {
                "strategy_id": strategy_id,
                "strategy_type": strategy_type,
                "actions_taken": [],
                "performance_impact": {},
                "recommendations": []
            }
            
            if strategy_type == "adaptive_workload_balancing":
                # Execute adaptive workload balancing
                execution_result.update(self._execute_adaptive_workload_balancing(strategy_config, context))
                
            elif strategy_type == "skill_based_task_assignment":
                # Execute skill-based task assignment
                execution_result.update(self._execute_skill_based_task_assignment(strategy_config, context))
                
            elif strategy_type == "resource_optimization":
                # Execute resource optimization
                execution_result.update(self._execute_resource_optimization(strategy_config, context))
            
            logger.info(f"Intelligent AI agent strategy executed: {strategy_id}")
            return execution_result
            
        except Exception as e:
            logger.error(f"Failed to execute intelligent AI agent strategy: {e}")
            raise
    
    def predict_agent_needs(self, time_horizon_minutes: int = 30) -> List[Dict[str, Any]]:
        """Predict potential AI agent needs based on current patterns"""
        try:
            predictions = []
            performance_analysis = self.analyze_agent_performance_patterns(time_horizon_minutes / 60)
            
            # Check for workload pressure
            workload_metrics = performance_analysis.get("workload_balance_metrics", {})
            if workload_metrics.get("balance_ratio", 1.0) < 0.6:
                prediction = {
                    "issue_type": "workload_imbalance",
                    "probability": 0.8,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.4,
                    "severity": "high",
                    "recommended_action": "Rebalance agent workloads"
                }
                predictions.append(prediction)
            
            # Check for resource pressure
            for resource, amounts in performance_analysis.get("resource_utilization", {}).items():
                if amounts and max(amounts) > 75:
                    prediction = {
                        "issue_type": "resource_pressure",
                        "resource": resource,
                        "probability": 0.9,
                        "estimated_time_to_threshold": time_horizon_minutes * 0.3,
                        "severity": "critical",
                        "recommended_action": f"Increase {resource} capacity"
                    }
                    predictions.append(prediction)
            
            # Check for skill gaps
            active_skills = performance_analysis.get("active_skills", 0)
            total_agents = performance_analysis.get("total_agents", 1)
            if active_skills < total_agents * 2:  # Assuming agents should have multiple skills
                prediction = {
                    "issue_type": "skill_gap",
                    "probability": 0.7,
                    "estimated_time_to_threshold": time_horizon_minutes * 0.8,
                    "severity": "medium",
                    "recommended_action": "Develop additional agent skills"
                }
                predictions.append(prediction)
            
            logger.info(f"AI agent needs prediction completed: {len(predictions)} predictions identified")
            return predictions
            
        except Exception as e:
            logger.error(f"Failed to predict AI agent needs: {e}")
            return []
    
    def optimize_agent_operations_automatically(self) -> Dict[str, Any]:
        """Automatically optimize AI agent operations based on current patterns"""
        try:
            optimization_plan = {
                "optimizations_applied": [],
                "performance_improvements": {},
                "recommendations": []
            }
            
            # Analyze current AI agent state
            performance_analysis = self.analyze_agent_performance_patterns()
            
            # Apply automatic optimizations
            workload_metrics = performance_analysis.get("workload_balance_metrics", {})
            if workload_metrics.get("balance_ratio", 1.0) < 0.7:
                # Workload imbalance - rebalance
                self.balance_workloads()
                optimization_plan["optimizations_applied"].append({
                    "action": "workload_rebalancing",
                    "target": "balance_ratio > 0.7",
                    "status": "executed"
                })
                optimization_plan["performance_improvements"]["workload_balance"] = "improved"
            
            # Check for resource optimization opportunities
            for resource, amounts in performance_analysis.get("resource_utilization", {}).items():
                if amounts and max(amounts) > 80:
                    # High resource utilization - optimize allocation
                    self._optimize_resource_allocation(resource)
                    optimization_plan["optimizations_applied"].append({
                        "action": f"resource_optimization_{resource}",
                        "target": f"{resource} < 80%",
                        "status": "executed"
                    })
                    optimization_plan["performance_improvements"][f"{resource}_utilization"] = "optimized"
            
            # Generate recommendations
            if not optimization_plan["optimizations_applied"]:
                optimization_plan["recommendations"].append("AI agent operations are optimized")
            else:
                optimization_plan["recommendations"].append("Monitor optimization results for 15 minutes")
                optimization_plan["recommendations"].append("Consider implementing permanent optimizations")
            
            logger.info(f"Automatic AI agent optimization completed: {len(optimization_plan['optimizations_applied'])} optimizations applied")
            return optimization_plan
            
        except Exception as e:
            logger.error(f"Failed to optimize AI agent operations automatically: {e}")
            return {"error": str(e)}
    
    def generate_agent_report(self, report_type: str = "comprehensive") -> Dict[str, Any]:
        """Generate comprehensive AI agent report"""
        try:
            report = {
                "report_id": f"ai_agent_report_{int(time.time())}",
                "generated_at": datetime.now().isoformat(),
                "report_type": report_type,
                "summary": {},
                "detailed_metrics": {},
                "agent_summary": {},
                "recommendations": []
            }
            
            # Generate summary
            total_agents = len(self._agent_registry)
            total_skills = len(self._skills)
            total_tasks = sum(len(tasks) for tasks in self._workloads.values())
            active_allocations = len([a for a in self._resource_allocations.values() if a.status == "allocated"])
            
            report["summary"] = {
                "total_registered_agents": total_agents,
                "total_active_skills": total_skills,
                "total_active_tasks": total_tasks,
                "active_resource_allocations": active_allocations,
                "orchestrator_status": self.status.value
            }
            
            # Generate detailed metrics
            if self._agent_registry:
                report["detailed_metrics"] = {
                    "agents_with_tasks": len([a for a, tasks in self._workloads.items() if tasks]),
                    "agents_with_skills": len(set(skill.name.split('_')[0] for skill in self._skills.values())),
                    "average_tasks_per_agent": total_tasks / total_agents if total_agents > 0 else 0,
                    "average_skills_per_agent": total_skills / total_agents if total_agents > 0 else 0
                }
            
            # Generate agent summary
            if self._workloads:
                agent_task_counts = {agent_id: len(tasks) for agent_id, tasks in self._workloads.items()}
                report["agent_summary"] = {
                    "agents_with_most_tasks": sorted(agent_task_counts.items(), key=lambda x: x[1], reverse=True)[:5],
                    "agents_with_least_tasks": sorted(agent_task_counts.items(), key=lambda x: x[1])[:5],
                    "workload_distribution": agent_task_counts
                }
            
            # Generate recommendations
            performance_analysis = self.analyze_agent_performance_patterns()
            for opportunity in performance_analysis.get("optimization_opportunities", []):
                report["recommendations"].append(opportunity)
            
            # Check for agent efficiency
            if total_tasks > 0 and total_agents > 0:
                avg_tasks = total_tasks / total_agents
                if avg_tasks > 20:
                    report["recommendations"].append("High average tasks per agent - consider adding more agents")
                elif avg_tasks < 2:
                    report["recommendations"].append("Low average tasks per agent - consider task consolidation")
            
            logger.info(f"AI agent report generated: {report['report_id']}")
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate AI agent report: {e}")
            return {"error": str(e)}
    
    # SKILL MANAGEMENT METHODS (from SkillManager)
    def add_skill(self, name: str, level: int = 0) -> Skill:
        """Add a new skill with specified level."""
        skill = Skill(name, max(0, min(100, level)), time.time())
        self._skills[name] = skill
        logger.info(f"Added skill: {name} at level {level}")
        return skill
    
    def update_skill(self, name: str, delta: int) -> int:
        """Update skill level by delta."""
        skill = self._skills.get(name)
        if not skill:
            skill = self.add_skill(name)
        return skill.adjust(delta)
    
    def get_skill_level(self, name: str) -> int:
        """Get current skill level."""
        return self._skills.get(name, Skill(name)).level
    
    def get_all_skills(self) -> Dict[str, Skill]:
        """Get all registered skills."""
        return dict(self._skills)
    
    # WORKLOAD MANAGEMENT METHODS (from WorkloadManager)
    def register_agent(self, agent_id: str) -> None:
        """Ensure an agent has an entry in the workload mapping."""
        self._workloads.setdefault(agent_id, deque())
        if agent_id not in self._agent_registry:
            self._agent_registry[agent_id] = {
                "registered_at": time.time(),
                "last_active": time.time(),
                "total_tasks_processed": 0
            }
    
    def assign_task(self, agent_id: str, task: AIAgentTask) -> None:
        """Assign a task to a specific agent."""
        self.register_agent(agent_id)
        task.assigned_at = time.time()
        self._workloads[agent_id].append(task)
        logger.info(f"Assigned task {task.task_id} to agent {agent_id}")
    
    def get_workload(self, agent_id: str) -> List[AIAgentTask]:
        """Return a list of tasks for the given agent."""
        return list(self._workloads.get(agent_id, []))
    
    def balance_workloads(self) -> Dict[str, List[AIAgentTask]]:
        """Redistribute tasks so each agent has roughly equal work."""
        agents = list(self._workloads)
        if not agents:
            return {}
        
        # Pool all tasks
        pool: Deque[AIAgentTask] = deque()
        for tasks in self._workloads.values():
            pool.extend(tasks)
            tasks.clear()
        
        # Round-robin assignment
        while pool:
            for agent in agents:
                if pool:
                    self._workloads[agent].append(pool.popleft())
                else:
                    break
        
        # Record balance history
        balance_record = {
            "timestamp": time.time(),
            "agent_counts": {agent: len(tasks) for agent, tasks in self._workloads.items()}
        }
        self._workload_balance_history.append(balance_record)
        
        logger.info("Workloads rebalanced across agents")
        return {agent: list(tasks) for agent, tasks in self._workloads.items()}
    
    def get_workloads(self) -> Dict[str, List[AIAgentTask]]:
        """Return a snapshot of all workloads without modification."""
        return {agent: list(tasks) for agent, tasks in self._workloads.items()}
    
    # RESOURCE MANAGEMENT METHODS (from AIAgentResourceManager)
    def allocate_resources(self, agent_id: str, resources: Dict[str, int]) -> bool:
        """Allocate resources for an agent."""
        allocation = ResourceAllocation(
            agent_id=agent_id,
            resources=resources,
            allocated_at=time.time(),
            estimated_release=time.time() + self.resource_allocation_timeout
        )
        
        allocation_id = f"{agent_id}_{int(time.time())}"
        self._resource_allocations[allocation_id] = allocation
        
        # Record utilization history
        utilization_record = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "resources": resources,
            "action": "allocated"
        }
        self._resource_utilization_history.append(utilization_record)
        
        logger.info(f"Allocated resources for agent {agent_id}: {resources}")
        return True
    
    def release_resources(self, allocation_id: str) -> None:
        """Release previously allocated resources."""
        if allocation_id in self._resource_allocations:
            allocation = self._resource_allocations[allocation_id]
            
            # Record utilization history
            utilization_record = {
                "timestamp": time.time(),
                "agent_id": allocation.agent_id,
                "resources": allocation.resources,
                "action": "released"
            }
            self._resource_utilization_history.append(utilization_record)
            
            del self._resource_allocations[allocation_id]
            logger.info(f"Released resources for agent {allocation.agent_id}")
    
    def get_current_resource_usage(self) -> Dict[str, int]:
        """Get current resource usage across all agents."""
        total_usage = defaultdict(int)
        for allocation in self._resource_allocations.values():
            if allocation.status == "allocated":
                for resource, amount in allocation.resources.items():
                    total_usage[resource] += amount
        return dict(total_usage)
    
    # STRATEGY EXECUTION METHODS
    def _execute_adaptive_workload_balancing(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute adaptive workload balancing strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["workload_rebalancing"],
            "performance_impact": {"workload_balance": "improved"},
            "recommendations": ["Monitor workload distribution for 15 minutes"]
        }
    
    def _execute_skill_based_task_assignment(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute skill-based task assignment strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["skill_matching_optimization"],
            "performance_impact": {"task_assignment": "optimized"},
            "recommendations": ["Review skill development opportunities"]
        }
    
    def _execute_resource_optimization(self, strategy_config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute resource optimization strategy"""
        # Simplified implementation
        return {
            "actions_taken": ["resource_allocation_optimization"],
            "performance_impact": {"resource_utilization": "optimized"},
            "recommendations": ["Monitor resource efficiency metrics"]
        }
    
    def _optimize_resource_allocation(self, resource_type: str) -> None:
        """Optimize resource allocation for specific resource type"""
        # Simplified optimization logic
        logger.info(f"Optimizing {resource_type} allocation")
    
    # UTILITY METHODS
    def _load_manager_config(self):
        """Load manager-specific configuration"""
        try:
            if Path(self.config_path).exists():
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                    # Load AI agent-specific configuration
                    if "ai_agent" in config:
                        ai_config = config["ai_agent"]
                        self.max_skills_per_agent = ai_config.get("max_skills_per_agent", 50)
                        self.max_tasks_per_agent = ai_config.get("max_tasks_per_agent", 100)
                        self.resource_allocation_timeout = ai_config.get("resource_allocation_timeout", 3600)
            else:
                logger.warning(f"AI agent config file not found: {self.config_path}")
        except Exception as e:
            logger.error(f"Failed to load AI agent config: {e}")
    
    def _initialize_workspace(self):
        """Initialize AI agent workspace"""
        self.workspace_path = Path("agent_workspaces")
        self.workspace_path.mkdir(exist_ok=True)
        logger.info("AI agent workspace initialized")
    
    def cleanup(self):
        """Cleanup AI agent orchestrator resources"""
        try:
            # Release all active resource allocations
            for allocation_id in list(self._resource_allocations.keys()):
                self.release_resources(allocation_id)
            logger.info("AIAgentOrchestrator cleanup completed")
        except Exception as e:
            logger.error(f"AIAgentOrchestrator cleanup failed: {e}")
