#!/usr/bin/env python3
"""
Autonomous Loop Validator - Autonomous Loop Validation System
===========================================================

Validation system for autonomous loop integration and continuous autonomy behavior.
Part of the autonomous loop integration implementation.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

from .autonomous_loop_integration import AutonomousLoopIntegration
from .continuous_autonomy_behavior import ContinuousAutonomyBehavior

logger = logging.getLogger(__name__)


class AutonomousLoopValidator:
    """Validator for autonomous loop integration and continuous autonomy behavior."""
    
    def __init__(self, agent_id: str = "Agent-2") -> None:
        """Initialize autonomous loop validator."""
        self.agent_id = agent_id
        self.autonomous_loop = AutonomousLoopIntegration(agent_id)
        self.continuous_autonomy = ContinuousAutonomyBehavior(agent_id)
        
        # Validation results
        self.validation_results: Dict[str, Any] = {}
        self.validation_timestamp = None
        
        logger.info(f"Autonomous loop validator initialized for {agent_id}")
    
    def validate_integration(self) -> Dict[str, Any]:
        """Validate autonomous loop integration."""
        validation_start = datetime.now()
        results = {
            "integration_valid": False,
            "components_valid": {},
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        try:
            # 1. Validate autonomous loop integration
            integration_valid = self._validate_autonomous_loop_component()
            results["components_valid"]["autonomous_loop"] = integration_valid
            
            # 2. Validate continuous autonomy behavior
            behavior_valid = self._validate_continuous_autonomy_component()
            results["components_valid"]["continuous_autonomy"] = behavior_valid
            
            # 3. Validate file system integration
            filesystem_valid = self._validate_filesystem_integration()
            results["components_valid"]["filesystem"] = filesystem_valid
            
            # 4. Validate task management integration
            task_mgmt_valid = self._validate_task_management_integration()
            results["components_valid"]["task_management"] = task_mgmt_valid
            
            # 5. Validate message processing integration
            message_valid = self._validate_message_processing_integration()
            results["components_valid"]["message_processing"] = message_valid
            
            # Overall validation result
            results["integration_valid"] = all(results["components_valid"].values())
            
            # Generate recommendations
            if not results["integration_valid"]:
                results["recommendations"].append("Fix failed component validations")
            
            validation_end = datetime.now()
            results["validation_duration"] = (validation_end - validation_start).total_seconds()
            
            logger.info(f"Integration validation completed: {results['integration_valid']}")
            return results
            
        except Exception as e:
            logger.error(f"Integration validation failed: {e}")
            results["errors"].append(str(e))
            return results
    
    def _validate_autonomous_loop_component(self) -> bool:
        """Validate autonomous loop integration component."""
        try:
            # Test basic functionality
            tasks = self.autonomous_loop.get_available_tasks()
            pending = self.autonomous_loop.get_pending_tasks()
            current = self.autonomous_loop.get_current_task()
            
            # Test cycle execution
            cycle_results = self.autonomous_loop.autonomous_loop_cycle()
            
            logger.info("Autonomous loop component validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Autonomous loop component validation failed: {e}")
            return False
    
    def _validate_continuous_autonomy_component(self) -> bool:
        """Validate continuous autonomy behavior component."""
        try:
            # Test status retrieval
            status = self.continuous_autonomy.get_status()
            
            # Test configuration methods
            self.continuous_autonomy.set_cycle_interval(30)
            self.continuous_autonomy.set_max_idle_cycles(3)
            
            logger.info("Continuous autonomy component validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Continuous autonomy component validation failed: {e}")
            return False
    
    def _validate_filesystem_integration(self) -> bool:
        """Validate file system integration."""
        try:
            # Test workspace paths
            workspace_path = self.autonomous_loop.workspace_path
            inbox_path = self.autonomous_loop.inbox_path
            processed_path = self.autonomous_loop.processed_path
            
            # Verify paths exist
            if not workspace_path.exists():
                return False
            if not inbox_path.exists():
                return False
            if not processed_path.exists():
                return False
            
            # Test file operations
            working_tasks_path = self.autonomous_loop.working_tasks_path
            future_tasks_path = self.autonomous_loop.future_tasks_path
            
            # Verify task files exist
            if not working_tasks_path.exists():
                return False
            if not future_tasks_path.exists():
                return False
            
            logger.info("File system integration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"File system integration validation failed: {e}")
            return False
    
    def _validate_task_management_integration(self) -> bool:
        """Validate task management integration."""
        try:
            # Test task loading
            working_tasks = self.autonomous_loop._load_working_tasks()
            future_tasks = self.autonomous_loop._load_future_tasks()
            
            # Verify task structure
            if "current_task" not in working_tasks:
                return False
            if "completed_tasks" not in working_tasks:
                return False
            if "available_tasks" not in working_tasks:
                return False
            
            if "pending_tasks" not in future_tasks:
                return False
            if "completed_future_tasks" not in future_tasks:
                return False
            
            logger.info("Task management integration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Task management integration validation failed: {e}")
            return False
    
    def _validate_message_processing_integration(self) -> bool:
        """Validate message processing integration."""
        try:
            # Test mailbox checking
            messages = self.autonomous_loop.check_mailbox()
            
            # Verify message processing (without actually processing)
            # This tests the method exists and can be called
            if not hasattr(self.autonomous_loop, 'process_message'):
                return False
            if not hasattr(self.autonomous_loop, 'process_all_messages'):
                return False
            
            logger.info("Message processing integration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Message processing integration validation failed: {e}")
            return False
    
    def validate_behavior(self) -> Dict[str, Any]:
        """Validate continuous autonomy behavior."""
        validation_start = datetime.now()
        results = {
            "behavior_valid": False,
            "test_results": {},
            "errors": [],
            "warnings": [],
            "recommendations": []
        }
        
        try:
            # 1. Test behavior start/stop
            start_result = self._test_behavior_start_stop()
            results["test_results"]["start_stop"] = start_result
            
            # 2. Test cycle execution
            cycle_result = self._test_cycle_execution()
            results["test_results"]["cycle_execution"] = cycle_result
            
            # 3. Test status reporting
            status_result = self._test_status_reporting()
            results["test_results"]["status_reporting"] = status_result
            
            # 4. Test callback integration
            callback_result = self._test_callback_integration()
            results["test_results"]["callback_integration"] = callback_result
            
            # Overall validation result
            results["behavior_valid"] = all(results["test_results"].values())
            
            validation_end = datetime.now()
            results["validation_duration"] = (validation_end - validation_start).total_seconds()
            
            logger.info(f"Behavior validation completed: {results['behavior_valid']}")
            return results
            
        except Exception as e:
            logger.error(f"Behavior validation failed: {e}")
            results["errors"].append(str(e))
            return results
    
    def _test_behavior_start_stop(self) -> bool:
        """Test behavior start and stop functionality."""
        try:
            # Test start
            start_success = self.continuous_autonomy.start()
            if not start_success:
                return False
            
            # Verify running status
            status = self.continuous_autonomy.get_status()
            if not status.get("is_running"):
                return False
            
            # Test stop
            stop_success = self.continuous_autonomy.stop()
            if not stop_success:
                return False
            
            # Verify stopped status
            status = self.continuous_autonomy.get_status()
            if status.get("is_running"):
                return False
            
            logger.info("Behavior start/stop test passed")
            return True
            
        except Exception as e:
            logger.error(f"Behavior start/stop test failed: {e}")
            return False
    
    def _test_cycle_execution(self) -> bool:
        """Test cycle execution functionality."""
        try:
            # Execute a single cycle
            cycle_results = self.autonomous_loop.autonomous_loop_cycle()
            
            # Verify cycle results structure
            required_fields = ["messages_processed", "messages_failed", "current_task"]
            for field in required_fields:
                if field not in cycle_results:
                    return False
            
            logger.info("Cycle execution test passed")
            return True
            
        except Exception as e:
            logger.error(f"Cycle execution test failed: {e}")
            return False
    
    def _test_status_reporting(self) -> bool:
        """Test status reporting functionality."""
        try:
            # Get status
            status = self.continuous_autonomy.get_status()
            
            # Verify status structure
            required_fields = ["is_running", "cycle_interval", "max_idle_cycles", "idle_cycle_count"]
            for field in required_fields:
                if field not in status:
                    return False
            
            logger.info("Status reporting test passed")
            return True
            
        except Exception as e:
            logger.error(f"Status reporting test failed: {e}")
            return False
    
    def _test_callback_integration(self) -> bool:
        """Test callback integration functionality."""
        try:
            # Test callback setting
            test_callback = lambda x: True
            
            self.continuous_autonomy.set_message_processor(test_callback)
            self.continuous_autonomy.set_task_processor(test_callback)
            self.continuous_autonomy.set_status_reporter(test_callback)
            self.continuous_autonomy.set_blocker_resolver(test_callback)
            
            logger.info("Callback integration test passed")
            return True
            
        except Exception as e:
            logger.error(f"Callback integration test failed: {e}")
            return False
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run full validation of autonomous loop integration."""
        validation_start = datetime.now()
        results = {
            "overall_valid": False,
            "integration_validation": {},
            "behavior_validation": {},
            "total_validation_time": 0,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # Run integration validation
            results["integration_validation"] = self.validate_integration()
            
            # Run behavior validation
            results["behavior_validation"] = self.validate_behavior()
            
            # Overall validation result
            results["overall_valid"] = (
                results["integration_validation"].get("integration_valid", False) and
                results["behavior_validation"].get("behavior_valid", False)
            )
            
            validation_end = datetime.now()
            results["total_validation_time"] = (validation_end - validation_start).total_seconds()
            
            # Store results
            self.validation_results = results
            self.validation_timestamp = validation_end
            
            logger.info(f"Full validation completed: {results['overall_valid']}")
            return results
            
        except Exception as e:
            logger.error(f"Full validation failed: {e}")
            results["error"] = str(e)
            return results
    
    def get_validation_report(self) -> Dict[str, Any]:
        """Get comprehensive validation report."""
        return {
            "agent_id": self.agent_id,
            "validation_results": self.validation_results,
            "validation_timestamp": self.validation_timestamp,
            "validator_status": "operational"
        }
