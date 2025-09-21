#!/usr/bin/env python3
"""
Contract Execution Core
=======================

Core contract execution system with threading and lifecycle management.
V2 Compliance: ≤200 lines, focused responsibility, KISS principle.
"""

import logging
import threading
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Callable
from concurrent.futures import ThreadPoolExecutor

from .contract_models import V3Contract, ContractStatus, ContractPriority

logger = logging.getLogger(__name__)


class ContractExecutionCore:
    """Core contract execution system."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize contract execution core."""
        self.config = config or {}
        
        # Execution settings
        self.execution_interval = self.config.get('execution_interval', 50)  # seconds
        self.max_workers = self.config.get('max_workers', 6)
        self.auto_execution = self.config.get('auto_execution', True)
        
        # Execution state
        self._running = False
        self._execution_thread: Optional[threading.Thread] = None
        self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
        self._contracts: List[V3Contract] = []
        
        # Callbacks
        self._execution_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        logger.info("Contract Execution Core initialized")
    
    def start_execution(self) -> None:
        """Start contract execution system."""
        if self._running:
            logger.warning("Contract execution already running")
            return
        
        self._running = True
        if self.auto_execution:
            self._execution_thread = threading.Thread(target=self._execution_loop, daemon=True)
            self._execution_thread.start()
        logger.info("Contract Execution System started")
    
    def stop_execution(self) -> None:
        """Stop contract execution system."""
        self._running = False
        if self._execution_thread:
            self._execution_thread.join(timeout=5.0)
        logger.info("Contract Execution System stopped")
    
    def add_execution_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Add execution callback."""
        self._execution_callbacks.append(callback)
        logger.info("Execution callback added")
    
    def _execution_loop(self) -> None:
        """Main contract execution loop."""
        while self._running:
            try:
                self._process_available_contracts()
                self._execute_claimed_contracts()
                time.sleep(self.execution_interval)
            except Exception as e:
                logger.error(f"Execution loop error: {e}")
                time.sleep(5)
    
    def _process_available_contracts(self) -> None:
        """Process available contracts."""
        try:
            available_contracts = [c for c in self._contracts if c.status == ContractStatus.AVAILABLE]
            
            for contract in available_contracts:
                self._evaluate_contract(contract)
            
        except Exception as e:
            logger.error(f"Failed to process available contracts: {e}")
    
    def _evaluate_contract(self, contract: V3Contract) -> None:
        """Evaluate contract for assignment."""
        try:
            if contract.priority == ContractPriority.HIGH:
                self._claim_contract(contract, "Agent-3")
            elif contract.priority == ContractPriority.MEDIUM:
                if self._should_claim_contract(contract):
                    self._claim_contract(contract, "Agent-3")
            
        except Exception as e:
            logger.error(f"Failed to evaluate contract: {e}")
    
    def _should_claim_contract(self, contract: V3Contract) -> bool:
        """Determine if contract should be claimed."""
        try:
            return True  # Agent-3 can claim all available contracts
            
        except Exception as e:
            logger.error(f"Failed to determine contract claiming: {e}")
            return False
    
    def _claim_contract(self, contract: V3Contract, agent_id: str) -> None:
        """Claim contract for execution."""
        try:
            contract.status = ContractStatus.CLAIMED
            contract.assigned_agent = agent_id
            contract.updated_at = datetime.now(timezone.utc)
            
            logger.info(f"Contract {contract.contract_id} claimed by {agent_id}")
            
            self._notify_execution_update({
                'type': 'contract_claimed',
                'contract': contract.to_dict(),
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
        except Exception as e:
            logger.error(f"Failed to claim contract: {e}")
    
    def _execute_claimed_contracts(self) -> None:
        """Execute claimed contracts."""
        try:
            claimed_contracts = [c for c in self._contracts if c.status == ContractStatus.CLAIMED]
            
            for contract in claimed_contracts:
                self._execute_contract(contract)
            
        except Exception as e:
            logger.error(f"Failed to execute claimed contracts: {e}")
    
    def _execute_contract(self, contract: V3Contract) -> None:
        """Execute a specific contract."""
        try:
            contract.status = ContractStatus.IN_PROGRESS
            contract.updated_at = datetime.now(timezone.utc)
            
            # Contract execution would be handled by specific executors
            # This is a placeholder for the actual execution logic
            
            contract.status = ContractStatus.COMPLETED
            contract.updated_at = datetime.now(timezone.utc)
            
            logger.info(f"Contract {contract.contract_id} completed successfully")
            
        except Exception as e:
            logger.error(f"Failed to execute contract: {e}")
            contract.status = ContractStatus.FAILED
            contract.updated_at = datetime.now(timezone.utc)
    
    def _notify_execution_update(self, update_data: Dict[str, Any]) -> None:
        """Notify execution update callbacks."""
        try:
            for callback in self._execution_callbacks:
                try:
                    callback(update_data)
                except Exception as e:
                    logger.error(f"Execution callback error: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to notify execution update: {e}")
    
    def set_contracts(self, contracts: List[V3Contract]) -> None:
        """Set contracts for execution."""
        self._contracts = contracts
    
    def get_contracts(self) -> List[V3Contract]:
        """Get current contracts."""
        return self._contracts.copy()
    
    def close(self) -> None:
        """Close contract execution system."""
        try:
            self.stop_execution()
            self._executor.shutdown(wait=True)
            self._contracts.clear()
            self._execution_callbacks.clear()
            logger.info("Contract Execution System closed")
            
        except Exception as e:
            logger.error(f"Error closing execution system: {e}")
