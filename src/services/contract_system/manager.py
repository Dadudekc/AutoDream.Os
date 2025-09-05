"""
Contract System Manager - KISS Simplified
=========================================

Simplified main business logic for contract system operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined contract management.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
Original: Agent-4 - Strategic Oversight & Emergency Intervention Manager
License: MIT
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import Contract, Task, TaskType, PriorityLevel, TaskStatus
from .storage import ContractStorage


class ContractManager:
    """Simplified contract system operations manager."""
    
    def __init__(self, storage: Optional[ContractStorage] = None):
        """Initialize contract manager - simplified."""
        self.storage = storage or ContractStorage()
    
    def create_contract(self, title: str, description: str, agent_id: str, 
                       tasks: List[Dict[str, Any]] = None) -> str:
        """Create new contract for agent - simplified."""
        try:
            contract_id = f"contract_{agent_id}_{uuid.uuid4().hex[:8]}"
            contract = Contract(
                contract_id=contract_id,
                title=title,
                description=description,
                agent_id=agent_id
            )
            
            # Add tasks if provided
            if tasks:
                for task_data in tasks:
                    task = self._create_task_from_data(task_data, contract_id)
                    contract.add_task(task)
            
            # Save contract
            if self.storage.save_contract(contract):
                return contract_id
            return None
        except Exception as e:
            print(f"Error creating contract: {e}")
            return None
    
    def _create_task_from_data(self, task_data: Dict[str, Any], contract_id: str) -> Task:
        """Create task from data - simplified."""
        try:
            return Task(
                task_id=f"task_{uuid.uuid4().hex[:8]}",
                contract_id=contract_id,
                title=task_data.get("title", "Untitled Task"),
                description=task_data.get("description", ""),
                task_type=TaskType(task_data.get("type", "general")),
                priority=PriorityLevel(task_data.get("priority", "normal")),
                status=TaskStatus.PENDING
            )
        except Exception as e:
            print(f"Error creating task from data: {e}")
            return None
    
    def get_contract(self, contract_id: str) -> Optional[Contract]:
        """Get contract by ID - simplified."""
        try:
            return self.storage.get_contract(contract_id)
        except Exception as e:
            print(f"Error getting contract: {e}")
            return None
    
    def get_agent_contracts(self, agent_id: str) -> List[Contract]:
        """Get contracts for agent - simplified."""
        try:
            return self.storage.get_agent_contracts(agent_id)
        except Exception as e:
            print(f"Error getting agent contracts: {e}")
            return []
    
    def assign_task(self, contract_id: str, task_id: str, agent_id: str) -> bool:
        """Assign task to agent - simplified."""
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                return False
            
            task = contract.get_task(task_id)
            if not task:
                return False
            
            task.assigned_agent = agent_id
            task.status = TaskStatus.ASSIGNED
            task.assigned_at = datetime.now()
            
            return self.storage.save_contract(contract)
        except Exception as e:
            print(f"Error assigning task: {e}")
            return False
    
    def complete_task(self, contract_id: str, task_id: str, result: Dict[str, Any]) -> bool:
        """Complete task - simplified."""
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                return False
            
            task = contract.get_task(task_id)
            if not task:
                return False
            
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now()
            task.result = result
            
            return self.storage.save_contract(contract)
        except Exception as e:
            print(f"Error completing task: {e}")
            return False
    
    def get_next_task(self, agent_id: str) -> Optional[Task]:
        """Get next available task for agent - simplified."""
        try:
            contracts = self.get_agent_contracts(agent_id)
            for contract in contracts:
                for task in contract.tasks:
                    if task.status == TaskStatus.PENDING:
                        return task
            return None
        except Exception as e:
            print(f"Error getting next task: {e}")
            return None
    
    def get_task_status(self, contract_id: str, task_id: str) -> Optional[TaskStatus]:
        """Get task status - simplified."""
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                return None
            
            task = contract.get_task(task_id)
            if not task:
                return None
            
            return task.status
        except Exception as e:
            print(f"Error getting task status: {e}")
            return None
    
    def update_task_priority(self, contract_id: str, task_id: str, priority: PriorityLevel) -> bool:
        """Update task priority - simplified."""
        try:
            contract = self.get_contract(contract_id)
            if not contract:
                return False
            
            task = contract.get_task(task_id)
            if not task:
                return False
            
            task.priority = priority
            return self.storage.save_contract(contract)
        except Exception as e:
            print(f"Error updating task priority: {e}")
            return False
    
    def get_contract_stats(self, agent_id: str) -> Dict[str, Any]:
        """Get contract statistics - simplified."""
        try:
            contracts = self.get_agent_contracts(agent_id)
            total_tasks = 0
            completed_tasks = 0
            pending_tasks = 0
            
            for contract in contracts:
                for task in contract.tasks:
                    total_tasks += 1
                    if task.status == TaskStatus.COMPLETED:
                        completed_tasks += 1
                    elif task.status == TaskStatus.PENDING:
                        pending_tasks += 1
            
            return {
                "agent_id": agent_id,
                "total_contracts": len(contracts),
                "total_tasks": total_tasks,
                "completed_tasks": completed_tasks,
                "pending_tasks": pending_tasks,
                "completion_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
            }
        except Exception as e:
            print(f"Error getting contract stats: {e}")
            return {}
    
    def delete_contract(self, contract_id: str) -> bool:
        """Delete contract - simplified."""
        try:
            return self.storage.delete_contract(contract_id)
        except Exception as e:
            print(f"Error deleting contract: {e}")
            return False
    
    def get_all_contracts(self) -> List[Contract]:
        """Get all contracts - simplified."""
        try:
            return self.storage.get_all_contracts()
        except Exception as e:
            print(f"Error getting all contracts: {e}")
            return []
    
    def search_contracts(self, query: str) -> List[Contract]:
        """Search contracts - simplified."""
        try:
            all_contracts = self.get_all_contracts()
            results = []
            query_lower = query.lower()
            
            for contract in all_contracts:
                if (query_lower in contract.title.lower() or 
                    query_lower in contract.description.lower()):
                    results.append(contract)
            
            return results
        except Exception as e:
            print(f"Error searching contracts: {e}")
            return []
    
    def get_manager_status(self) -> Dict[str, Any]:
        """Get manager status - simplified."""
        try:
            all_contracts = self.get_all_contracts()
            return {
                "total_contracts": len(all_contracts),
                "storage_available": self.storage is not None,
                "last_updated": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Error getting manager status: {e}")
            return {}


    def create_default_tasks(self) -> None:
        """Create default tasks for all agents."""
        try:
            # Agent-1: Integration & Core Systems
            self._create_agent_tasks("Agent-1", [
                {
                    "title": "V2 Compliance Refactoring",
                    "description": "Refactor large files to meet V2 compliance standards",
                    "task_type": "v2_compliance",
                    "priority": "high"
                },
                {
                    "title": "Core System Integration",
                    "description": "Integrate core systems with messaging and vector database",
                    "task_type": "feature_development",
                    "priority": "medium"
                }
            ])
            
            # Agent-2: Architecture & Design
            self._create_agent_tasks("Agent-2", [
                {
                    "title": "Architecture Optimization",
                    "description": "Optimize system architecture for better performance",
                    "task_type": "optimization",
                    "priority": "high"
                },
                {
                    "title": "Design Pattern Implementation",
                    "description": "Implement design patterns for better code organization",
                    "task_type": "refactoring",
                    "priority": "medium"
                }
            ])
            
            # Agent-3: Infrastructure & DevOps
            self._create_agent_tasks("Agent-3", [
                {
                    "title": "Infrastructure Monitoring",
                    "description": "Set up comprehensive infrastructure monitoring",
                    "task_type": "feature_development",
                    "priority": "high"
                },
                {
                    "title": "DevOps Pipeline Optimization",
                    "description": "Optimize CI/CD pipeline for better efficiency",
                    "task_type": "optimization",
                    "priority": "medium"
                }
            ])
            
            # Agent-4: Strategic Oversight (Captain)
            self._create_agent_tasks("Agent-4", [
                {
                    "title": "Strategic Oversight",
                    "description": "Provide strategic oversight and emergency intervention",
                    "task_type": "coordination",
                    "priority": "critical"
                },
                {
                    "title": "Agent Coordination",
                    "description": "Coordinate agent activities and task assignments",
                    "task_type": "coordination",
                    "priority": "high"
                }
            ])
            
            # Agent-5: Business Intelligence
            self._create_agent_tasks("Agent-5", [
                {
                    "title": "Analytics System Development",
                    "description": "Develop comprehensive analytics system",
                    "task_type": "feature_development",
                    "priority": "high"
                },
                {
                    "title": "Data Processing Optimization",
                    "description": "Optimize data processing pipelines",
                    "task_type": "optimization",
                    "priority": "medium"
                }
            ])
            
            # Agent-6: Coordination & Communication
            self._create_agent_tasks("Agent-6", [
                {
                    "title": "Communication System Enhancement",
                    "description": "Enhance inter-agent communication systems",
                    "task_type": "feature_development",
                    "priority": "high"
                },
                {
                    "title": "Coordination Protocol Development",
                    "description": "Develop coordination protocols for agent collaboration",
                    "task_type": "feature_development",
                    "priority": "medium"
                }
            ])
            
            # Agent-7: Web Development
            self._create_agent_tasks("Agent-7", [
                {
                    "title": "Web Interface Development",
                    "description": "Develop web interface for agent management",
                    "task_type": "feature_development",
                    "priority": "high"
                },
                {
                    "title": "Frontend Performance Optimization",
                    "description": "Optimize frontend performance and user experience",
                    "task_type": "optimization",
                    "priority": "medium"
                }
            ])
            
            # Agent-8: SSOT & System Integration
            self._create_agent_tasks("Agent-8", [
                {
                    "title": "System Integration Testing",
                    "description": "Comprehensive system integration testing",
                    "task_type": "testing",
                    "priority": "high"
                },
                {
                    "title": "SSOT Implementation",
                    "description": "Implement Single Source of Truth across systems",
                    "task_type": "feature_development",
                    "priority": "critical"
                }
            ])
            
        except Exception as e:
            print(f"❌ Error creating default tasks: {e}")
    
    def _create_agent_tasks(self, agent_id: str, task_data_list: List[Dict[str, Any]]) -> None:
        """Create tasks for specific agent."""
        try:
            contract_id = self.create_contract(
                title=f"{agent_id} Default Contract",
                description=f"Default contract for {agent_id}",
                agent_id=agent_id
            )
            
            if contract_id:
                for task_data in task_data_list:
                    self.add_task_to_contract(contract_id, task_data)
        except Exception as e:
            print(f"❌ Error creating agent tasks for {agent_id}: {e}")
    
    def _create_task_from_data(self, task_data: Dict[str, Any], contract_id: str) -> Task:
        """Create task from data dictionary."""
        task_id = f"task_{contract_id}_{uuid.uuid4().hex[:8]}"
        
        return Task(
            task_id=task_id,
            title=task_data.get("title", "Untitled Task"),
            description=task_data.get("description", ""),
            task_type=TaskType(task_data.get("task_type", "maintenance")),
            priority=PriorityLevel(task_data.get("priority", "medium")),
            status=TaskStatus.PENDING,
            estimated_duration=task_data.get("estimated_duration", "1 cycle")
        )


# Global instance for backward compatibility
_global_contract_manager: Optional[ContractManager] = None

def get_contract_manager(storage: Optional[ContractStorage] = None) -> ContractManager:
    """Returns a global instance of the ContractManager."""
    global _global_contract_manager
    if _global_contract_manager is None:
        _global_contract_manager = ContractManager(storage)
    return _global_contract_manager