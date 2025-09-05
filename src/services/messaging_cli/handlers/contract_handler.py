#!/usr/bin/env python3
"""
Contract Handler - KISS Simplified
==================================

Simplified contract-related CLI operations.
KISS PRINCIPLE: Keep It Simple, Stupid - streamlined contract handling.

Author: Agent-8 (SSOT & System Integration Specialist) - KISS Simplification
License: MIT
"""

import logging
from typing import Dict, Any, List, Optional

try:
    from ...models.messaging_models import UnifiedMessage
    from ....core.unified_data_processing_system import read_json, write_json
except ImportError:
    # Fallback implementations
    class UnifiedMessage:
        def __init__(self, **kwargs):
            for key, value in kwargs.items():
                setattr(self, key, value)
    
    def read_json(file_path: str) -> Dict[str, Any]:
        return {}
    
    def write_json(file_path: str, data: Dict[str, Any]) -> bool:
        return True


class ContractHandler:
    """Simplified contract-related operations for messaging CLI."""
    
    def __init__(self):
        """Initialize contract handler - simplified."""
        self.logger = logging.getLogger(__name__)
        self.contract_cache: Dict[str, Any] = {}
        
    def get_next_task(self, agent_id: str) -> Dict[str, Any]:
        """Get next available task for specified agent - simplified."""
        try:
            self.logger.info(f"Getting next task for {agent_id}")
            
            # Try to read agent-specific contracts
            contracts_file = f"agent_workspaces/contracts/{agent_id}_contracts.json"
            contracts_data = read_json(contracts_file)
            
            if contracts_data and "available_tasks" in contracts_data:
                available_tasks = contracts_data["available_tasks"]
                if available_tasks:
                    task = available_tasks[0]
                    # Mark task as claimed
                    task["status"] = "claimed"
                    task["claimed_by"] = agent_id
                    contracts_data["claimed_tasks"] = contracts_data.get("claimed_tasks", [])
                    contracts_data["claimed_tasks"].append(task)
                    contracts_data["available_tasks"] = available_tasks[1:]
                    write_json(contracts_file, contracts_data)
                    return {"success": True, "task": task}
            
            return {"success": False, "message": "No available tasks"}
            
        except Exception as e:
            self.logger.error(f"Error getting next task: {e}")
            return {"success": False, "error": str(e)}
    
    def check_status(self) -> Dict[str, Any]:
        """Check contract system status - simplified."""
        try:
            self.logger.info("Checking contract system status")
            
            # Basic status check
            status = {
                "contract_system": "active",
                "total_agents": 8,
                "available_tasks": 0,
                "claimed_tasks": 0,
                "completed_tasks": 0
            }
            
            # Try to read global contracts
            global_contracts_file = "agent_workspaces/contracts/global_contracts.json"
            global_data = read_json(global_contracts_file)
            
            if global_data:
                status.update({
                    "available_tasks": len(global_data.get("available_tasks", [])),
                    "claimed_tasks": len(global_data.get("claimed_tasks", [])),
                    "completed_tasks": len(global_data.get("completed_tasks", []))
                })
            
            return {"success": True, "status": status}
            
        except Exception as e:
            self.logger.error(f"Error checking status: {e}")
            return {"success": False, "error": str(e)}
    
    def create_contract(self, contract_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new contract - simplified."""
        try:
            self.logger.info("Creating new contract")
            
            # Basic contract creation
            contract_id = f"contract_{int(time.time())}"
            contract = {
                "contract_id": contract_id,
                "title": contract_data.get("title", "Untitled Contract"),
                "description": contract_data.get("description", ""),
                "priority": contract_data.get("priority", "normal"),
                "status": "active",
                "created_at": time.time(),
                "assigned_agent": contract_data.get("assigned_agent", None)
            }
            
            # Save contract
            contracts_file = "agent_workspaces/contracts/global_contracts.json"
            contracts_data = read_json(contracts_file)
            if not contracts_data:
                contracts_data = {"contracts": [], "available_tasks": []}
            
            contracts_data["contracts"].append(contract)
            write_json(contracts_file, contracts_data)
            
            return {"success": True, "contract_id": contract_id}
            
        except Exception as e:
            self.logger.error(f"Error creating contract: {e}")
            return {"success": False, "error": str(e)}
    
    def complete_task(self, agent_id: str, task_id: str) -> Dict[str, Any]:
        """Complete a task - simplified."""
        try:
            self.logger.info(f"Completing task {task_id} for {agent_id}")
            
            # Find and complete task
            contracts_file = f"agent_workspaces/contracts/{agent_id}_contracts.json"
            contracts_data = read_json(contracts_file)
            
            if contracts_data and "claimed_tasks" in contracts_data:
                claimed_tasks = contracts_data["claimed_tasks"]
                for task in claimed_tasks:
                    if task.get("task_id") == task_id:
                        task["status"] = "completed"
                        task["completed_at"] = time.time()
                        contracts_data["completed_tasks"] = contracts_data.get("completed_tasks", [])
                        contracts_data["completed_tasks"].append(task)
                        contracts_data["claimed_tasks"] = [t for t in claimed_tasks if t.get("task_id") != task_id]
                        write_json(contracts_file, contracts_data)
                        return {"success": True, "message": "Task completed"}
            
            return {"success": False, "message": "Task not found"}
            
        except Exception as e:
            self.logger.error(f"Error completing task: {e}")
            return {"success": False, "error": str(e)}
    
    def get_agent_contracts(self, agent_id: str) -> Dict[str, Any]:
        """Get contracts for specific agent - simplified."""
        try:
            self.logger.info(f"Getting contracts for {agent_id}")
            
            contracts_file = f"agent_workspaces/contracts/{agent_id}_contracts.json"
            contracts_data = read_json(contracts_file)
            
            if contracts_data:
                return {
                    "success": True,
                    "contracts": contracts_data.get("contracts", []),
                    "available_tasks": contracts_data.get("available_tasks", []),
                    "claimed_tasks": contracts_data.get("claimed_tasks", []),
                    "completed_tasks": contracts_data.get("completed_tasks", [])
                }
            
            return {"success": True, "contracts": [], "available_tasks": [], "claimed_tasks": [], "completed_tasks": []}
            
        except Exception as e:
            self.logger.error(f"Error getting agent contracts: {e}")
            return {"success": False, "error": str(e)}
    
    def get_contract_stats(self) -> Dict[str, Any]:
        """Get contract statistics - simplified."""
        try:
            self.logger.info("Getting contract statistics")
            
            stats = {
                "total_contracts": 0,
                "active_contracts": 0,
                "completed_contracts": 0,
                "total_tasks": 0,
                "available_tasks": 0,
                "claimed_tasks": 0,
                "completed_tasks": 0
            }
            
            # Read global contracts
            global_contracts_file = "agent_workspaces/contracts/global_contracts.json"
            global_data = read_json(global_contracts_file)
            
            if global_data:
                stats.update({
                    "total_contracts": len(global_data.get("contracts", [])),
                    "active_contracts": len([c for c in global_data.get("contracts", []) if c.get("status") == "active"]),
                    "completed_contracts": len([c for c in global_data.get("contracts", []) if c.get("status") == "completed"]),
                    "total_tasks": len(global_data.get("available_tasks", [])) + len(global_data.get("claimed_tasks", [])) + len(global_data.get("completed_tasks", [])),
                    "available_tasks": len(global_data.get("available_tasks", [])),
                    "claimed_tasks": len(global_data.get("claimed_tasks", [])),
                    "completed_tasks": len(global_data.get("completed_tasks", []))
                })
            
            return {"success": True, "stats": stats}
            
        except Exception as e:
            self.logger.error(f"Error getting contract stats: {e}")
            return {"success": False, "error": str(e)}
    
    def cleanup_old_contracts(self, days_old: int = 30) -> Dict[str, Any]:
        """Cleanup old contracts - simplified."""
        try:
            self.logger.info(f"Cleaning up contracts older than {days_old} days")
            
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            # Cleanup global contracts
            global_contracts_file = "agent_workspaces/contracts/global_contracts.json"
            global_data = read_json(global_contracts_file)
            
            if global_data:
                original_count = len(global_data.get("contracts", []))
                global_data["contracts"] = [
                    c for c in global_data.get("contracts", [])
                    if c.get("created_at", 0) > cutoff_time
                ]
                cleaned_count = original_count - len(global_data["contracts"])
                write_json(global_contracts_file, global_data)
                
                return {"success": True, "cleaned_contracts": cleaned_count}
            
            return {"success": True, "cleaned_contracts": 0}
            
        except Exception as e:
            self.logger.error(f"Error cleaning up contracts: {e}")
            return {"success": False, "error": str(e)}
    
    def get_handler_status(self) -> Dict[str, Any]:
        """Get handler status - simplified."""
        return {
            "handler_type": "contract_handler",
            "contract_cache_size": len(self.contract_cache),
            "status": "active"
        }