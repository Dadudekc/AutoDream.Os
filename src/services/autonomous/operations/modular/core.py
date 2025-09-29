#!/usr/bin/env python3
"""
Autonomous Operations Core - V2 Compliant
=========================================

Core autonomous operations functionality.
V2 Compliance: ≤200 lines, single responsibility, KISS principle.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional

from .operations_manager import OperationsManager
from .operation_executor import OperationExecutor
from .operations_loader import OperationsLoader

logger = logging.getLogger(__name__)


class AutonomousOperationsCore:
    """Core autonomous operations functionality."""
    
    def __init__(self, agent_id: str, workspace_dir: Path):
        """Initialize autonomous operations core."""
        self.agent_id = agent_id
        self.workspace_dir = workspace_dir
        self.operations_file = workspace_dir / "autonomous_operations.json"
        
        # Initialize modular components
        self.operations_manager = OperationsManager(self)
        self.operation_executor = OperationExecutor(self)
        self.operations_loader = OperationsLoader(self)
    
    async def run_autonomous_operations(self) -> Dict[str, Any]:
        """Run autonomous operations when no urgent tasks are pending."""
        try:
            operations_results = {
                "operations_run": 0,
                "operations_successful": 0,
                "operations_failed": 0,
                "details": []
            }
            
            # Get available operations
            available_operations = await self.operations_loader.get_available_operations()
            
            if not available_operations:
                logger.info(f"{self.agent_id}: No autonomous operations available")
                return operations_results
            
            # Run operations
            for operation in available_operations:
                operations_results["operations_run"] += 1
                
                try:
                    result = await self.operation_executor.execute_operation(operation)
                    
                    if result.get("success", False):
                        operations_results["operations_successful"] += 1
                        logger.info(f"{self.agent_id}: Operation '{operation.get('name', 'Unknown')}' completed successfully")
                    else:
                        operations_results["operations_failed"] += 1
                        logger.warning(f"{self.agent_id}: Operation '{operation.get('name', 'Unknown')}' failed: {result.get('error', 'Unknown error')}")
                    
                    operations_results["details"].append({
                        "operation": operation.get("name", "Unknown"),
                        "result": result
                    })
                    
                except Exception as e:
                    operations_results["operations_failed"] += 1
                    logger.error(f"{self.agent_id}: Operation '{operation.get('name', 'Unknown')}' failed with exception: {e}")
                    
                    operations_results["details"].append({
                        "operation": operation.get("name", "Unknown"),
                        "result": {"success": False, "error": str(e)}
                    })
            
            # Update operations with results
            await self.operations_manager.update_operations_with_results(available_operations, operations_results["details"])
            
            logger.info(f"{self.agent_id}: Autonomous operations completed - {operations_results['operations_successful']}/{operations_results['operations_run']} successful")
            
            return operations_results
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Failed to run autonomous operations: {e}")
            return {
                "operations_run": 0,
                "operations_successful": 0,
                "operations_failed": 0,
                "details": [],
                "error": str(e)
            }
    
    def get_operations_summary(self) -> Dict[str, Any]:
        """Get summary of available operations."""
        try:
            if not self.operations_file.exists():
                return {"total_operations": 0, "operations": []}
            
            with open(self.operations_file, 'r') as f:
                operations = json.load(f)
            
            return {
                "total_operations": len(operations),
                "operations": operations
            }
            
        except Exception as e:
            logger.error(f"{self.agent_id}: Failed to get operations summary: {e}")
            return {"total_operations": 0, "operations": [], "error": str(e)}
    
    def clear_operations(self) -> None:
        """Clear all operations."""
        try:
            if self.operations_file.exists():
                self.operations_file.unlink()
                logger.info(f"{self.agent_id}: Cleared all autonomous operations")
        except Exception as e:
            logger.error(f"{self.agent_id}: Failed to clear operations: {e}")
