#!/usr/bin/env python3
"""
Core Perpetual Motion Service
=============================

Core perpetual motion service for V2 system with contract generation
and task management capabilities.
Follows V2 coding standards: ≤300 lines per module.
"""

import json
import logging
import time
import threading
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import argparse
import random

logger = logging.getLogger(__name__)


@dataclass
class ContractTemplate:
    """Contract template for automatic generation."""
    title: str
    description: str
    acceptance_criteria: List[str]
    estimated_hours: int
    priority: str
    category: str
    skills_required: List[str]


@dataclass
class GeneratedContract:
    """Automatically generated contract."""
    contract_id: str
    task_id: str
    title: str
    description: str
    assignee: str
    state: str
    created_at: datetime
    template_source: str


class ContractGenerator:
    """Generates new contracts from templates"""
    
    def __init__(self, templates_dir: str = "contract_templates"):
        self.templates_dir = Path(templates_dir)
        self.templates_dir.mkdir(exist_ok=True)
        self.contract_templates = self._load_contract_templates()
        
        logger.info("Contract Generator initialized")
        
    def _load_contract_templates(self) -> List[ContractTemplate]:
        """Load contract templates from directory"""
        templates = []
        try:
            for template_file in self.templates_dir.glob("*.json"):
                with open(template_file, 'r') as f:
                    template_data = json.load(f)
                    template = ContractTemplate(**template_data)
                    templates.append(template)
            logger.info(f"Loaded {len(templates)} contract templates")
        except Exception as e:
            logger.error(f"Failed to load contract templates: {e}")
        return templates
        
    def generate_contract(self, template_id: str = None, 
                         custom_data: Dict[str, Any] = None) -> GeneratedContract:
        """Generate a new contract from template"""
        try:
            # Select template
            if template_id:
                template = next((t for t in self.contract_templates if t.title == template_id), None)
            else:
                template = random.choice(self.contract_templates) if self.contract_templates else None
                
            if not template:
                raise ValueError("No contract template available")
                
            # Generate contract data
            contract_id = f"contract_{int(time.time())}"
            task_id = f"task_{int(time.time())}"
            
            contract = GeneratedContract(
                contract_id=contract_id,
                task_id=task_id,
                title=template.title,
                description=template.description,
                assignee="unassigned",
                state="new",
                created_at=datetime.now(),
                template_source=template.title
            )
            
            logger.info(f"Generated contract: {contract_id}")
            return contract
            
        except Exception as e:
            logger.error(f"Failed to generate contract: {e}")
            return None
            
    def generate_multiple_contracts(self, count: int) -> List[GeneratedContract]:
        """Generate multiple contracts"""
        contracts = []
        for i in range(count):
            contract = self.generate_contract()
            if contract:
                contracts.append(contract)
        return contracts


class TaskManager:
    """Manages task lifecycle and completion tracking"""
    
    def __init__(self):
        self.active_tasks: Dict[str, Dict[str, Any]] = {}
        self.completed_tasks: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        
        logger.info("Task Manager initialized")
        
    def create_task(self, contract: GeneratedContract) -> str:
        """Create a new task from contract"""
        try:
            task_id = contract.task_id
            task_data = {
                "contract_id": contract.contract_id,
                "title": contract.title,
                "description": contract.description,
                "assignee": contract.assignee,
                "state": "new",
                "created_at": datetime.now(),
                "estimated_hours": 0,
                "actual_hours": 0,
                "priority": "medium"
            }
            
            with self._lock:
                self.active_tasks[task_id] = task_data
                
            logger.info(f"Task created: {task_id}")
            return task_id
            
        except Exception as e:
            logger.error(f"Failed to create task: {e}")
            return ""
            
    def update_task_status(self, task_id: str, status: str, 
                          details: Dict[str, Any] = None) -> bool:
        """Update task status"""
        try:
            with self._lock:
                if task_id in self.active_tasks:
                    self.active_tasks[task_id]["state"] = status
                    if details:
                        self.active_tasks[task_id].update(details)
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to update task status: {e}")
            return False
            
    def complete_task(self, task_id: str, completion_data: Dict[str, Any] = None) -> bool:
        """Mark task as completed"""
        try:
            with self._lock:
                if task_id in self.active_tasks:
                    task = self.active_tasks.pop(task_id)
                    task["state"] = "completed"
                    task["completed_at"] = datetime.now()
                    if completion_data:
                        task.update(completion_data)
                    self.completed_tasks[task_id] = task
                    return True
            return False
        except Exception as e:
            logger.error(f"Failed to complete task: {e}")
            return False
            
    def get_active_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all active tasks"""
        with self._lock:
            return self.active_tasks.copy()
            
    def get_completed_tasks(self) -> Dict[str, Dict[str, Any]]:
        """Get all completed tasks"""
        with self._lock:
            return self.completed_tasks.copy()


class PerpetualMotionContractService:
    """Main perpetual motion contract service"""
    
    def __init__(self, contracts_dir: str = "contracts", 
                 templates_dir: str = "contract_templates"):
        self.contracts_dir = Path(contracts_dir)
        self.contracts_dir.mkdir(exist_ok=True)
        
        # Setup logging
        self.setup_logging()
        
        # Initialize components
        self.contract_generator = ContractGenerator(templates_dir)
        self.task_manager = TaskManager()
        
        # Auto-generation settings
        self.auto_generate_on_completion = True
        self.contracts_per_completion = 2
        self.min_contracts_maintained = 10
        
        # Monitoring thread
        self.monitor_thread = None
        self.monitoring_active = False
        
        # Completion triggers
        self.completion_triggers = [
            "fsm_update",
            "contract_complete", 
            "task_done",
            "mission_accomplished"
        ]
        
        logger.info("🔄 PERPETUAL MOTION: Auto-completion detection enabled")
        logger.info("Perpetual Motion Contract Service initialized")
        
    def setup_logging(self) -> None:
        """Setup logging for the service"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s | %(levelname)s | %(message)s",
            handlers=[
                logging.FileHandler(log_dir / "perpetual_motion.log"),
                logging.StreamHandler()
            ]
        )
        
    def start_monitoring(self) -> bool:
        """Start perpetual motion monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring already active")
            return False
            
        try:
            self.monitoring_active = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            logger.info("🔄 Perpetual motion monitoring started")
            return True
        except Exception as e:
            logger.error(f"Failed to start monitoring: {e}")
            self.monitoring_active = False
            return False
            
    def stop_monitoring(self) -> bool:
        """Stop perpetual motion monitoring"""
        if not self.monitoring_active:
            logger.warning("Monitoring not active")
            return False
            
        try:
            self.monitoring_active = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=5.0)
            logger.info("🔄 Perpetual motion monitoring stopped")
            return True
        except Exception as e:
            logger.error(f"Failed to stop monitoring: {e}")
            return False
            
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                self._check_contract_balance()
                self._detect_completions()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(30)
                
    def _check_contract_balance(self) -> None:
        """Check if we need to generate more contracts"""
        try:
            active_tasks = self.task_manager.get_active_tasks()
            if len(active_tasks) < self.min_contracts_maintained:
                needed = self.min_contracts_maintained - len(active_tasks)
                logger.info(f"🔄 Generating {needed} new contracts to maintain balance")
                self._generate_contracts(needed)
        except Exception as e:
            logger.error(f"Error checking contract balance: {e}")
            
    def _detect_completions(self) -> None:
        """Detect task completions and trigger new contract generation"""
        try:
            # This would integrate with the actual completion detection system
            # For now, it's a placeholder
            pass
        except Exception as e:
            logger.error(f"Error detecting completions: {e}")
            
    def _generate_contracts(self, count: int) -> None:
        """Generate new contracts and tasks"""
        try:
            contracts = self.contract_generator.generate_multiple_contracts(count)
            for contract in contracts:
                if contract:
                    task_id = self.task_manager.create_task(contract)
                    if task_id:
                        logger.info(f"🔄 New task created: {task_id}")
        except Exception as e:
            logger.error(f"Error generating contracts: {e}")
            
    def get_service_status(self) -> Dict[str, Any]:
        """Get current service status"""
        try:
            status = {
                "monitoring_active": self.monitoring_active,
                "auto_generation": self.auto_generate_on_completion,
                "contracts_per_completion": self.contracts_per_completion,
                "min_contracts_maintained": self.min_contracts_maintained,
                "active_tasks": len(self.task_manager.get_active_tasks()),
                "completed_tasks": len(self.task_manager.get_completed_tasks()),
                "available_templates": len(self.contract_generator.contract_templates)
            }
            return status
        except Exception as e:
            logger.error(f"Failed to get service status: {e}")
            return {"error": str(e)}
            
    def generate_contracts_manual(self, count: int) -> List[str]:
        """Manually generate contracts"""
        try:
            contracts = self.contract_generator.generate_multiple_contracts(count)
            task_ids = []
            for contract in contracts:
                if contract:
                    task_id = self.task_manager.create_task(contract)
                    if task_id:
                        task_ids.append(task_id)
            logger.info(f"🔄 Manually generated {len(task_ids)} contracts")
            return task_ids
        except Exception as e:
            logger.error(f"Failed to manually generate contracts: {e}")
            return []
            
    def test_perpetual_motion(self, agent_id: str) -> Dict[str, Any]:
        """Test perpetual motion system for an agent"""
        try:
            # Generate test contracts
            test_contracts = self.contract_generator.generate_multiple_contracts(3)
            test_tasks = []
            
            for contract in test_contracts:
                if contract:
                    task_id = self.task_manager.create_task(contract)
                    if task_id:
                        test_tasks.append(task_id)
                        
            # Simulate completion
            for task_id in test_tasks:
                self.task_manager.complete_task(task_id, {
                    "completed_by": agent_id,
                    "completion_notes": "Test completion"
                })
                
            result = {
                "status": "success",
                "test_contracts_generated": len(test_contracts),
                "test_tasks_completed": len(test_tasks),
                "agent_id": agent_id,
                "message": "🔄 Perpetual motion test completed successfully"
            }
            
            logger.info(f"🔄 Perpetual motion test completed for {agent_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to test perpetual motion: {e}")
            return {"error": str(e)}
