#!/usr/bin/env python3
"""
FSM Types - V2 Modular Architecture
===================================

Type definitions and configuration structures for the FSM system.
Follows V2 standards: OOP design, SRP, no strict LOC limits.

Author: Agent-4 (Captain)
Task: TASK 4I - FSM System Modularization
License: MIT
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional, List


@dataclass
class FSMConfig:
    """FSM system configuration."""
    
    # Core system settings
    max_concurrent_workflows: int = 10
    default_timeout: float = 300.0
    enable_logging: bool = True
    
    # Task management settings
    max_tasks_per_agent: int = 10
    task_timeout_hours: int = 24
    auto_cleanup_completed: bool = True
    
    # Communication settings
    enable_discord_bridge: bool = True
    
    # Retry policy
    retry_policy: Dict[str, Any] = None
    
    # Monitoring settings
    monitoring: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.retry_policy is None:
            self.retry_policy = {
                "max_retries": 3,
                "retry_delay": 5.0,
                "exponential_backoff": True
            }
        
        if self.monitoring is None:
            self.monitoring = {
                "enabled": True,
                "interval": 1.0,
                "metrics_collection": True
            }


@dataclass
class FSMStrategy:
    """FSM strategy configuration."""
    
    id: str
    type: str
    description: str
    parameters: Dict[str, Any]
    
    # Strategy-specific configurations
    performance_threshold: float = 0.8
    workload_balance: bool = True
    skill_matching: bool = True
    pattern_analysis: bool = True
    condition_optimization: bool = True
    transition_validation: bool = True
    message_routing: bool = True
    event_prioritization: bool = True
    bridge_optimization: bool = True


class FSMStrategyTypes:
    """FSM strategy type definitions."""
    
    ADAPTIVE_TASK_ASSIGNMENT = "adaptive_task_assignment"
    INTELLIGENT_STATE_TRANSITION = "intelligent_state_transition"
    COMMUNICATION_OPTIMIZATION = "communication_optimization"
    
    @classmethod
    def get_all_types(cls) -> List[str]:
        """Get all available strategy types."""
        return [
            cls.ADAPTIVE_TASK_ASSIGNMENT,
            cls.INTELLIGENT_STATE_TRANSITION,
            cls.COMMUNICATION_OPTIMIZATION
        ]


class FSMConstants:
    """FSM system constants."""
    
    # Default timeouts
    DEFAULT_TIMEOUT = 30.0
    DEFAULT_RETRY_COUNT = 3
    DEFAULT_PING_INTERVAL = 30
    DEFAULT_PING_TIMEOUT = 10
    
    # Task limits
    MAX_TASKS_PER_AGENT = 10
    TASK_RETENTION_HOURS = 24
    
    # Workflow limits
    MAX_CONCURRENT_WORKFLOWS = 10
    MAX_WORKFLOW_QUEUE_SIZE = 100
    
    # Performance thresholds
    HIGH_ERROR_THRESHOLD = 10
    LOAD_BALANCE_THRESHOLD = 100
    SUCCESS_RATE_THRESHOLD = 0.95
    
    # Monitoring intervals
    DEFAULT_MONITORING_INTERVAL = 1.0
    DEFAULT_CLEANUP_INTERVAL = 3600.0  # 1 hour

