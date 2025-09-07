#!/usr/bin/env python3
"""
Contract Manager - Agent Cellphone V2
====================================

Manages contract operations and task assignments.

Author: Agent-7 (Web Development Specialist)
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

from .storage import ContractStorage
from .models import Contract

logger = logging.getLogger(__name__)


class ContractManager:
    """Manages contract operations and task assignments."""
    
    def __init__(self):
        """Initialize contract manager."""
        self.storage = ContractStorage()
        self.logger = logger
        
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system contract status."""
        try:
            contracts = self.storage.get_all_contracts()
            
            status = {
                "total_contracts": len(contracts),
                "active_contracts": len([c for c in contracts if c.get('status') == 'active']),
                "completed_contracts": len([c for c in contracts if c.get('status') == 'completed']),
                "pending_contracts": len([c for c in contracts if c.get('status') == 'pending']),
                "last_updated": datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def get_agent_status(self, agent_id: str) -> Dict[str, Any]:
        """Get contract status for specific agent."""
        try:
            agent_contracts = self.storage.get_agent_contracts(agent_id)
            
            status = {
                "agent_id": agent_id,
                "total_contracts": len(agent_contracts),
                "active_contracts": len([c for c in agent_contracts if c.get('status') == 'active']),
                "completed_contracts": len([c for c in agent_contracts if c.get('status') == 'completed']),
                "contracts": agent_contracts,
                "last_updated": datetime.now().isoformat()
            }
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting agent status for {agent_id}: {e}")
            return {"error": str(e), "agent_id": agent_id}
    
    def get_next_task(self, agent_id: str) -> Dict[str, Any]:
        """Get next available task for agent."""
        try:
            # Get available tasks
            all_contracts = self.storage.get_all_contracts()
            available_tasks = [c for c in all_contracts if c.get('status') == 'pending']
            
            if not available_tasks:
                return {
                    "agent_id": agent_id,
                    "task": None,
                    "message": "No available tasks",
                    "status": "no_tasks"
                }
            
            # Assign first available task
            task = available_tasks[0]
            task['assigned_to'] = agent_id
            task['status'] = 'active'
            task['assigned_at'] = datetime.now().isoformat()
            
            # Save updated task
            self.storage.save_contract(task)
            
            return {
                "agent_id": agent_id,
                "task": task,
                "status": "assigned"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting next task for {agent_id}: {e}")
            return {"error": str(e), "agent_id": agent_id}
    
    def add_task_to_contract(self, contract_id: str, task: Dict[str, Any]) -> bool:
        """Add a task to an existing contract."""
        try:
            contract = self.storage.get_contract(contract_id)
            if not contract:
                return False
                
            if 'tasks' not in contract:
                contract['tasks'] = []
                
            contract['tasks'].append(task)
            contract['last_updated'] = datetime.now().isoformat()
            
            return self.storage.save_contract(contract)
            
        except Exception as e:
            self.logger.error(f"Error adding task to contract {contract_id}: {e}")
            return False
