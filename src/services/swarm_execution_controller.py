#!/usr/bin/env python3
"""
Swarm Execution Controller - Anti-Theater Enforcement
=====================================================

V2 Compliant: ≤400 lines, enforces execution-over-coordination protocols
to prevent coordination theater and ensure measurable task outcomes.

This module implements Execution Mode Protocol to kill acknowledgment loops
and enforce outcome-based reporting.

Author: Agent-4 Captain (Executive Authority)
License: MIT
Status: MISSION CRITICAL - Theater Loop Fix
"""

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SwarmExecutionController:
    """Enforces execution protocols and prevents coordination theater."""
    
    def __init__(self, project_root: str = "."):
        """Initialize execution controller."""
        self.project_root = Path(project_root)
        self.config_dir = self.project_root / "config"
        self.execution_dir = self.project_root / "execution_logs"
        self.execution_dir.mkdir(exist_ok=True)
        
        # Load execution mode protocol
        self.protocol = self._load_execution_protocol()
        
        # Track acknowledgment chains
        self.acknowledgment_chains = {}
        self.theater_detection_count = 0
        
        # Execution metrics
        self.task_completions = 0
        self.theater_violations = 0
        
    def _load_execution_protocol(self) -> Dict[str, Any]:
        """Load execution mode protocol from JSON config."""
        protocol_file = self.project_root / "execution_protocol_config.json"
        
        if protocol_file.exists():
            with open(protocol_file, 'r') as f:
                return json.load(f)
        
        # Default protocol if file not found
        return {
            "execution_mode": {
                "hard_stops": {"max_acknowledgments": 1},
                "outcome_enforcement": {"require_measurable_results": True},
                "suppression_rules": {"suppress_acknowledgment_chains": True}
            }
        }
    
    def monitor_message(self, from_agent: str, to_agent: str, message: str) -> Dict[str, Any]:
        """Monitor agent messages for theater violations."""
        detection_result = {
            "violation_detected": False,
            "violation_type": None,
            "action_required": None,
            "theater_count": self.theater_detection_count
        }
        
        # Check for acknowledgment chains
        if self._detect_acknowledgment_chain(message):
            self.theater_detection_count += 1
            detection_result.update({
                "violation_detected": True,
                "violation_type": "acknowledgment_chain",
                "action_required": "halt_coordination",
                "theater_count": self.theater_detection_count
            })
            self._log_theater_violation(from_agent, message, "acknowledgment_chain")
        
        # Check for meta-reporting
        if self._detect_meta_reporting(message):
            detection_result.update({
                "violation_detected": True,
                "violation_type": "meta_reporting",
                "action_required": "suppress_message",
                "theater_count": self.theater_detection_count
            })
        
        # Check for circular confirmations
        if self._detect_circular_confirmation(message):
            detection_result.update({
                "violation_detected": True,
                "violation_type": "circular_confirmation",
                "action_required": "immediate_halt",
                "theater_count": self.theater_detection_count
            })
            self._log_theater_violation(from_agent, message, "circular_confirmation")
        
        return detection_result
    
    def validate_task_execution(self, agent: str, task: str, result: str) -> Dict[str, Any]:
        """Validate task execution for measurable outcomes."""
        validation_result = {
            "valid_execution": False,
            "measurable_outcome": False,
            "missing_metrics": [],
            "suggested_format": None
        }
        
        # Check for measurable outcome indicators
        measurable_indicators = [
            r'\d+\s+files?\s+(deleted|removed|cleaned)',
            r'\d+\s+directories?\s+(cleaned|removed)',
            r'\d+\s+lines?\s+(added|removed)',
            r'\d+\.\d+%\s+(reduction|improvement)',
            r'\d+\s+bytes?\s+(freed|removed)',
            r'(✅|✓|DONE|COMPLETE)',
            r'task\s+complete',
            r'mission\s+accomplished'
        ]
        
        has_measurable_outcome = any(
            re.search(pattern, result.lower()) for pattern in measurable_indicators
        )
        
        if has_measurable_outcome:
            validation_result.update({
                "valid_execution": True,
                "measurable_outcome": True
            })
            self.task_completions += 1
        else:
            validation_result.update({
                "missing_metrics": ["quantity", "action", "result"],
                "suggested_format": f"✅ [QUANTITY] [UNIT] [ACTION] - Example: '✅ 433 files deleted'"
            })
        
        # Log execution validation
        self._log_execution_validation(agent, task, result, validation_result)
        
        return validation_result
    
    def _detect_acknowledgment_chain(self, message: str) -> bool:
        """Detect acknowledgment chain violations."""
        chain_patterns = [
            r'acknowledged.*acknowledged',
            r'confirmed.*confirmed', 
            r'status.*status',
            r'report.*report',
            r'coordination.*coordination',
            r'execution.*execution'
        ]
        
        return any(re.search(pattern, message.lower()) for pattern in chain_patterns)
    
    def _detect_meta_reporting(self, message: str) -> bool:
        """Detect meta-reporting violations."""
        meta_patterns = [
            r'coordination status',
            r'acknowledgment confirmed',
            r'status acknowledged',
            r'mission status confirmed',
            r'execution monitoring',
            r'ultimate.*strategic.*direction'
        ]
        
        return any(re.search(pattern, message.lower()) for pattern in meta_patterns)
    
    def _detect_circular_confirmation(self, message: str) -> bool:
        """Detect circular confirmation patterns."""
        # Count acknowledgment/confirmation keywords
        confirmation_words = ['acknowledged', 'confirmed', 'status', 'report']
        word_count = sum(message.lower().count(word) for word in confirmation_words)
        
        return word_count >= 4  # Arbitrary threshold for circular behavior
    
    def _log_theater_violation(self, agent: str, message: str, violation_type: str):
        """Log theater violation for analysis."""
        timestamp = datetime.now().isoformat()
        
        violation_log = {
            "timestamp": timestamp,
            "agent": agent,
            "message": message,
            "violation_type": violation_type,
            "theater_count": self.theater_detection_count
        }
        
        # Write to execution log
        log_file = self.execution_dir / "theater_violations.json"
        
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    violations = json.load(f)
            else:
                violations = []
            
            violations.append(violation_log)
            
            with open(log_file, 'w') as f:
                json.dump(violations, f, indent=2)
                
            logger.warning(f"Theater violation detected: {violation_type} from {agent}")
            
        except Exception as e:
            logger.error(f"Failed to log theater violation: {e}")
    
    def _log_execution_validation(self, agent: str, task: str, result: str, validation: Dict[str, Any]):
        """Log execution validation results."""
        timestamp = datetime.now().isoformat()
        
        validation_log = {
            "timestamp": timestamp,
            "agent": agent,
            "task": task,
            "result": result,
            "validation": validation,
            "task_completions": self.task_completions
        }
        
        # Write to execution log
        log_file = self.execution_dir / "execution_validations.json"
        
        try:
            if log_file.exists():
                with open(log_file, 'r') as f:
                    validations = json.load(f)
            else:
                validations = []
            
            validations.append(validation_log)
            
            with open(log_file, 'w') as f:
                json.dump(validations, f, indent=2)
                
            if validation["valid_execution"]:
                logger.info(f"Valid execution from {agent}: {task}")
            else:
                logger.warning(f"Invalid execution from {agent}: Missing measurable outcome")
                
        except Exception as e:
            logger.error(f"Failed to log execution validation: {e}")
    
    def get_execution_metrics(self) -> Dict[str, Any]:
        """Get current execution metrics."""
        return {
            "task_completions": self.task_completions,
            "theater_violations": self.theater_violation_count,
            "theater_detection_count": self.theater_detection_count,
            "protocol_active": True,
            "enforcement_level": "MAXIMUM"
        }
    
    def generate_execution_summary(self) -> str:
        """Generate execution summary report."""
        metrics = self.get_execution_metrics()
        
        summary = f"""
🎯 SWARM EXECUTION CONTROLLER SUMMARY
====================================
Task Completions: {metrics['task_completions']}
Theater Violations: {metrics['theater_violations']}
Theater Detection Count: {metrics['theater_detection_count']}
Protocol Status: {'ACTIVE' if metrics['protocol_active'] else 'INACTIVE'}
Enforcement Level: {metrics['enforcement_level']}

🚨 ANTI-THEATER ENFORCEMENT: OPERATIONAL
"""
        
        return summary.strip()


if __name__ == "__main__":
    # Test execution controller
    controller = SwarmExecutionController()
    
    # Test theater detection
    test_messages = [
        "Acknowledged acknowledged confirmed",
        "✅ 433 files deleted successfully", 
        "Coordination status update confirmed acknowledged",
        "Mission accomplished - 274 files removed"
    ]
    
    for msg in test_messages:
        detection = controller.monitor_message("Agent-7", "Agent-4", msg)
        print(f"Message: '{msg}'")
        print(f"Violation: {detection['violation_detected']}")
        print(f"Type: {detection['violation_type']}")
        print("---")
    
    # Test task validation
    validation = controller.validate_task_execution(
        "Agent-7", 
        "File cleanup", 
        "✅ 433 files deleted from ML components"
    )
    print(f"Valid execution: {validation['valid_execution']}")
