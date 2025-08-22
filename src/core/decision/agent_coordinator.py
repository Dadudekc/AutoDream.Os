#!/usr/bin/env python3
"""
Agent Coordinator - Agent Cellphone V2 Decision System
=====================================================

Implements agent coordination and capability management for the autonomous decision engine.
Follows V2 coding standards: ≤300 LOC, OOP design, SRP.

**Responsibilities:**
- Agent capability management
- Agent coordination protocols
- Resource allocation
- Task assignment coordination

**Author:** Agent-1
**Created:** Current Sprint
**Status:** ACTIVE - V2 STANDARDS COMPLIANT
"""

import json
import time
import threading
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import asdict
from datetime import datetime

from .decision_types import AgentCapability, DecisionType, DecisionContext
from ..persistent_data_storage import PersistentDataStorage


class AgentCoordinator:
    """
    Coordinates agent activities and manages agent capabilities
    
    Responsibilities:
    - Manage agent capability information
    - Coordinate agent task assignments
    - Handle resource allocation
    - Facilitate agent communication
    """
    
    def __init__(self, storage: PersistentDataStorage):
        self.storage = storage
        self.agent_capabilities: Dict[str, AgentCapability] = {}
        self.agent_tasks: Dict[str, List[str]] = {}
        self.agent_status: Dict[str, str] = {}
        self.coordination_lock = threading.Lock()
        
    def register_agent(self, agent_id: str, capability: AgentCapability) -> bool:
        """Register a new agent with the system"""
        try:
            with self.coordination_lock:
                self.agent_capabilities[agent_id] = capability
                self.agent_tasks[agent_id] = []
                self.agent_status[agent_id] = "available"
                
                # Store agent registration
                self.storage.store_data(
                    f"agent_registration_{agent_id}",
                    asdict(capability),
                    "autonomous/agents",
                    DataIntegrityLevel.BASIC
                )
            return True
        except Exception as e:
            print(f"Error registering agent {agent_id}: {e}")
            return False
    
    def update_agent_capability(self, agent_id: str, capability: AgentCapability) -> bool:
        """Update agent capability information"""
        try:
            with self.coordination_lock:
                self.agent_capabilities[agent_id] = capability
                
                # Store updated capability
                self.storage.store_data(
                    f"agent_capability_{agent_id}",
                    asdict(capability),
                    "autonomous/agents",
                    DataIntegrityLevel.BASIC
                )
            return True
        except Exception as e:
            print(f"Error updating agent capability: {e}")
            return False
    
    def assign_task(self, agent_id: str, task_id: str) -> bool:
        """Assign a task to a specific agent"""
        try:
            with self.coordination_lock:
                if agent_id not in self.agent_tasks:
                    return False
                
                self.agent_tasks[agent_id].append(task_id)
                self.agent_status[agent_id] = "busy"
                
                # Store task assignment
                self.storage.store_data(
                    f"task_assignment_{task_id}",
                    {
                        "agent_id": agent_id,
                        "task_id": task_id,
                        "timestamp": datetime.now().isoformat(),
                        "status": "assigned"
                    },
                    "autonomous/tasks",
                    DataIntegrityLevel.BASIC
                )
            return True
        except Exception as e:
            print(f"Error assigning task {task_id} to agent {agent_id}: {e}")
            return False
    
    def complete_task(self, agent_id: str, task_id: str) -> bool:
        """Mark a task as completed by an agent"""
        try:
            with self.coordination_lock:
                if agent_id in self.agent_tasks and task_id in self.agent_tasks[agent_id]:
                    self.agent_tasks[agent_id].remove(task_id)
                    
                    # Update agent status if no more tasks
                    if not self.agent_tasks[agent_id]:
                        self.agent_status[agent_id] = "available"
                    
                    # Store task completion
                    self.storage.store_data(
                        f"task_completion_{task_id}",
                        {
                            "agent_id": agent_id,
                            "task_id": task_id,
                            "timestamp": datetime.now().isoformat(),
                            "status": "completed"
                        },
                        "autonomous/tasks",
                        DataIntegrityLevel.BASIC
                    )
                    return True
            return False
        except Exception as e:
            print(f"Error completing task {task_id} for agent {agent_id}: {e}")
            return False
    
    def get_agent_status(self, agent_id: str) -> Optional[Dict[str, Any]]:
        """Get current status of a specific agent"""
        try:
            with self.coordination_lock:
                if agent_id not in self.agent_capabilities:
                    return None
                
                capability = self.agent_capabilities[agent_id]
                tasks = self.agent_tasks.get(agent_id, [])
                status = self.agent_status.get(agent_id, "unknown")
                
                return {
                    "agent_id": agent_id,
                    "status": status,
                    "current_tasks": len(tasks),
                    "skills": capability.skills,
                    "experience_level": capability.experience_level,
                    "specialization": capability.specialization,
                    "availability": capability.availability
                }
        except Exception as e:
            print(f"Error getting agent status for {agent_id}: {e}")
            return None
    
    def get_available_agents(self, required_skills: List[str] = None) -> List[str]:
        """Get list of available agents, optionally filtered by skills"""
        try:
            with self.coordination_lock:
                available = []
                
                for agent_id, capability in self.agent_capabilities.items():
                    if not capability.availability:
                        continue
                    
                    if self.agent_status.get(agent_id) != "available":
                        continue
                    
                    if required_skills:
                        # Check if agent has required skills
                        if not any(skill in capability.skills for skill in required_skills):
                            continue
                    
                    available.append(agent_id)
                
                return available
        except Exception as e:
            print(f"Error getting available agents: {e}")
            return []
    
    def get_coordination_status(self) -> Dict[str, Any]:
        """Get overall coordination system status"""
        with self.coordination_lock:
            total_agents = len(self.agent_capabilities)
            available_agents = len([aid for aid, status in self.agent_status.items() if status == "available"])
            busy_agents = total_agents - available_agents
            total_tasks = sum(len(tasks) for tasks in self.agent_tasks.values())
            
            return {
                "total_agents": total_agents,
                "available_agents": available_agents,
                "busy_agents": busy_agents,
                "total_tasks": total_tasks,
                "agent_statuses": dict(self.agent_status),
                "task_distribution": {aid: len(tasks) for aid, tasks in self.agent_tasks.items()}
            }
    
    def run_smoke_test(self) -> bool:
        """Run basic functionality test"""
        try:
            # Test agent registration
            test_capability = AgentCapability(
                agent_id="test_agent",
                skills=["testing", "coordination"],
                experience_level=0.8,
                performance_history=[0.7, 0.8, 0.9],
                learning_rate=0.1,
                specialization="testing",
                availability=True
            )
            
            success = self.register_agent("test_agent", test_capability)
            if not success:
                return False
            
            # Test task assignment
            success = self.assign_task("test_agent", "test_task_1")
            if not success:
                return False
            
            # Test status retrieval
            status = self.get_agent_status("test_agent")
            if not status:
                return False
            
            # Test task completion
            success = self.complete_task("test_agent", "test_task_1")
            if not success:
                return False
            
            # Test coordination status
            coord_status = self.get_coordination_status()
            if not coord_status:
                return False
            
            return True
            
        except Exception as e:
            print(f"Agent coordinator smoke test failed: {e}")
            return False
