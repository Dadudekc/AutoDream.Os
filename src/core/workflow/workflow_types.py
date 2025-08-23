#!/usr/bin/env python3
"""
Workflow Types Module - V2 Core Workflow System
===============================================

Contains all workflow type definitions, enums, and data structures.
Follows V2 coding standards: ≤100 LOC, single responsibility, clean OOP design.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime

# ============================================================================
# WORKFLOW ENUMS - Single Responsibility: Define workflow types and states
# ============================================================================

class WorkflowType(Enum):
    """Advanced workflow types for V2 system"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    LOOP = "loop"
    EVENT_DRIVEN = "event_driven"
    ADAPTIVE = "adaptive"
    # V2 specific types
    INITIALIZATION = "initialization"
    TRAINING = "training"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPABILITY_GRANT = "capability_grant"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    COMPLETION = "completion"


class WorkflowPriority(Enum):
    """Workflow priority levels"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"
    EMERGENCY = "emergency"


class OptimizationStrategy(Enum):
    """Workflow optimization strategies"""
    PERFORMANCE = "performance"
    RESOURCE_EFFICIENCY = "resource_efficiency"
    COST_OPTIMIZATION = "cost_optimization"
    LATENCY_REDUCTION = "latency_reduction"
    THROUGHPUT_MAXIMIZATION = "throughput_maximization"


# ============================================================================
# WORKFLOW DATA STRUCTURES - Single Responsibility: Define workflow components
# ============================================================================

@dataclass
class WorkflowStep:
    """Advanced workflow step definition"""
    step_id: str
    name: str
    step_type: str
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    required_capabilities: List[str] = field(default_factory=list)
    estimated_duration: float = 0.0
    timeout: float = 300.0
    retry_policy: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    # V2 specific fields
    agent_target: str = ""
    prompt_template: str = ""
    expected_response_type: str = "text"
    completion_criteria: Dict[str, Any] = field(default_factory=dict)

    def is_ready(self, completed_steps: set) -> bool:
        """Check if step dependencies are satisfied"""
        return all(dep in completed_steps for dep in self.dependencies)


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""
    execution_id: str
    workflow_id: str
    status: str
    current_step: str
    completed_steps: List[str]
    failed_steps: List[str]
    start_time: str
    estimated_completion: str
    actual_completion: Optional[str]
    performance_metrics: Dict[str, float]
    optimization_history: List[Dict[str, Any]]
    agent_id: Optional[str] = None
    step_results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkflowOptimization:
    """Workflow optimization result"""
    optimization_id: str
    workflow_id: str
    strategy: OptimizationStrategy
    before_metrics: Dict[str, float]
    after_metrics: Dict[str, float]
    improvement_percentage: float
    optimization_timestamp: str
    applied_changes: List[str]


@dataclass
class V2Workflow:
    """V2 workflow definition"""
    workflow_id: str
    name: str
    description: str
    steps: List[WorkflowStep]
    created_at: str
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AIResponse:
    """Captured AI response from V2 system"""
    agent: str
    text: str
    timestamp: float
    message_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# CLI INTERFACE - Single Responsibility: Command-line testing
# ============================================================================

def run_smoke_test():
    """Run basic functionality test for workflow types"""
    try:
        # Test enum creation
        assert WorkflowType.SEQUENTIAL == "sequential"
        assert WorkflowPriority.HIGH == "high"
        assert OptimizationStrategy.PERFORMANCE == "performance"
        
        # Test data class creation
        step = WorkflowStep(
            step_id="test",
            name="Test Step",
            step_type="test",
            description="Test description"
        )
        assert step.step_id == "test"
        assert step.is_ready(set())
        
        # Test workflow creation
        workflow = V2Workflow(
            workflow_id="test_workflow",
            name="Test Workflow",
            description="Test workflow",
            steps=[step],
            created_at="2024-01-01",
            status="active"
        )
        assert workflow.workflow_id == "test_workflow"
        assert len(workflow.steps) == 1
        
        print("✅ WorkflowTypes smoke test passed!")
        return True
        
    except Exception as e:
        print(f"❌ WorkflowTypes smoke test failed: {e}")
        return False


if __name__ == "__main__":
    run_smoke_test()
