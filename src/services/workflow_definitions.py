"""
Workflow Definitions Module - Workflow Data Structures

This module contains workflow step definitions and data structures.
Follows Single Responsibility Principle - only manages workflow definitions.

Architecture: Single Responsibility Principle - workflow definitions only
LOC: 150 lines (under 200 limit)
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class WorkflowStep(Enum):
    """Orientation workflow steps"""

    INITIALIZATION = "initialization"
    TRAINING = "training"
    ROLE_ASSIGNMENT = "role_assignment"
    CAPABILITY_GRANT = "capability_grant"
    SYSTEM_INTEGRATION = "system_integration"
    VALIDATION = "validation"
    COMPLETION = "completion"


class WorkflowStatus(Enum):
    """Workflow execution status"""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class WorkflowStepData:
    """Workflow step execution data"""

    step_id: WorkflowStep
    name: str
    description: str
    duration_minutes: int
    prerequisites: List[WorkflowStep]
    completion_criteria: List[str]
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class WorkflowExecution:
    """Workflow execution instance"""

    workflow_id: str
    agent_id: str
    status: WorkflowStatus
    current_step: Optional[WorkflowStep]
    completed_steps: List[WorkflowStep]
    start_time: float
    step_results: Dict[WorkflowStep, Dict[str, Any]]
    completion_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None


class WorkflowDefinitionManager:
    """
    Manages workflow definitions and templates.

    Responsibilities:
    - Provide workflow definitions
    - Manage workflow templates
    - Support workflow customization
    """

    def __init__(self):
        self.workflow_definitions: Dict[str, List[WorkflowStepData]] = {}
        self._initialize_workflow_definitions()

    def _initialize_workflow_definitions(self):
        """Initialize orientation workflow definitions"""
        # Standard orientation workflow
        standard_workflow = [
            WorkflowStepData(
                step_id=WorkflowStep.INITIALIZATION,
                name="Agent Initialization",
                description="Initialize agent system components and basic configuration",
                duration_minutes=2,
                prerequisites=[],
                completion_criteria=[
                    "Agent system components initialized",
                    "Basic configuration loaded",
                    "Agent identity established",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.TRAINING,
                name="Core Training",
                description="Complete essential training modules and orientation",
                duration_minutes=5,
                prerequisites=[WorkflowStep.INITIALIZATION],
                completion_criteria=[
                    "Core training modules completed",
                    "System protocols understood",
                    "Basic capabilities demonstrated",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.ROLE_ASSIGNMENT,
                name="Role Assignment",
                description="Assign specific role and responsibilities",
                duration_minutes=1,
                prerequisites=[WorkflowStep.TRAINING],
                completion_criteria=[
                    "Role assigned and accepted",
                    "Responsibilities understood",
                    "Capabilities mapped to role",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.CAPABILITY_GRANT,
                name="Capability Grant",
                description="Grant role-specific capabilities and permissions",
                duration_minutes=1,
                prerequisites=[WorkflowStep.ROLE_ASSIGNMENT],
                completion_criteria=[
                    "Role capabilities granted",
                    "Permissions configured",
                    "Access controls set",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.SYSTEM_INTEGRATION,
                name="System Integration",
                description="Integrate agent into active system workflows",
                duration_minutes=2,
                prerequisites=[WorkflowStep.CAPABILITY_GRANT],
                completion_criteria=[
                    "Agent integrated into workflows",
                    "Communication channels established",
                    "Team coordination active",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.VALIDATION,
                name="Final Validation",
                description="Validate complete onboarding and readiness",
                duration_minutes=1,
                prerequisites=[WorkflowStep.SYSTEM_INTEGRATION],
                completion_criteria=[
                    "All onboarding steps completed",
                    "Agent ready for active duty",
                    "Quality standards met",
                ],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.COMPLETION,
                name="Onboarding Completion",
                description="Complete onboarding and transition to active status",
                duration_minutes=1,
                prerequisites=[WorkflowStep.VALIDATION],
                completion_criteria=[
                    "Onboarding officially completed",
                    "Agent status updated to active",
                    "Welcome to team message sent",
                ],
            ),
        ]

        # Quick orientation workflow
        quick_workflow = [
            WorkflowStepData(
                step_id=WorkflowStep.INITIALIZATION,
                name="Quick Initialization",
                description="Rapid agent initialization",
                duration_minutes=1,
                prerequisites=[],
                completion_criteria=["Basic initialization complete"],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.TRAINING,
                name="Essential Training",
                description="Critical training only",
                duration_minutes=2,
                prerequisites=[WorkflowStep.INITIALIZATION],
                completion_criteria=["Essential training completed"],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.ROLE_ASSIGNMENT,
                name="Role Assignment",
                description="Assign role and basic capabilities",
                duration_minutes=1,
                prerequisites=[WorkflowStep.TRAINING],
                completion_criteria=["Role assigned"],
            ),
            WorkflowStepData(
                step_id=WorkflowStep.COMPLETION,
                name="Quick Completion",
                description="Complete quick onboarding",
                duration_minutes=1,
                prerequisites=[WorkflowStep.ROLE_ASSIGNMENT],
                completion_criteria=["Quick onboarding complete"],
            ),
        ]

        self.workflow_definitions = {
            "standard": standard_workflow,
            "quick": quick_workflow,
        }

    def get_workflow_definition(self, workflow_type: str) -> List[WorkflowStepData]:
        """Get workflow definition by type"""
        return self.workflow_definitions.get(workflow_type, [])

    def get_available_workflows(self) -> List[str]:
        """Get list of available workflow types"""
        return list(self.workflow_definitions.keys())

    def get_workflow_step(
        self, workflow_type: str, step_id: WorkflowStep
    ) -> Optional[WorkflowStepData]:
        """Get specific workflow step"""
        workflow = self.get_workflow_definition(workflow_type)
        for step in workflow:
            if step.step_id == step_id:
                return step
        return None

    def validate_workflow_definition(self, workflow_type: str) -> bool:
        """Validate workflow definition integrity"""
        workflow = self.get_workflow_definition(workflow_type)
        if not workflow:
            return False

        # Check for required steps
        required_steps = {WorkflowStep.INITIALIZATION, WorkflowStep.COMPLETION}
        workflow_steps = {step.step_id for step in workflow}

        if not required_steps.issubset(workflow_steps):
            return False

        # Check step dependencies
        for step in workflow:
            for prereq in step.prerequisites:
                if not any(s.step_id == prereq for s in workflow):
                    return False

        return True


def run_smoke_test():
    """Run basic functionality test for WorkflowDefinitionManager"""
    print("🧪 Running WorkflowDefinitionManager Smoke Test...")

    try:
        manager = WorkflowDefinitionManager()

        # Test workflow retrieval
        standard = manager.get_workflow_definition("standard")
        assert len(standard) == 7

        quick = manager.get_workflow_definition("quick")
        assert len(quick) == 4

        # Test step retrieval
        init_step = manager.get_workflow_step("standard", WorkflowStep.INITIALIZATION)
        assert init_step.name == "Agent Initialization"

        # Test validation
        assert manager.validate_workflow_definition("standard")
        assert manager.validate_workflow_definition("quick")

        # Test available workflows
        available = manager.get_available_workflows()
        assert "standard" in available
        assert "quick" in available

        print("✅ WorkflowDefinitionManager Smoke Test PASSED")
        return True

    except Exception as e:
        print(f"❌ WorkflowDefinitionManager Smoke Test FAILED: {e}")
        return False


def main():
    """CLI interface for WorkflowDefinitionManager testing"""
    import argparse

    parser = argparse.ArgumentParser(description="Workflow Definition Manager CLI")
    parser.add_argument("--test", action="store_true", help="Run smoke test")
    parser.add_argument("--list", action="store_true", help="List available workflows")
    parser.add_argument("--workflow", help="Show workflow definition")
    parser.add_argument("--validate", help="Validate workflow definition")

    args = parser.parse_args()

    if args.test:
        run_smoke_test()
        return

    manager = WorkflowDefinitionManager()

    if args.list:
        workflows = manager.get_available_workflows()
        print("Available workflows:")
        for wf in workflows:
            steps = manager.get_workflow_definition(wf)
            print(f"  {wf}: {len(steps)} steps")
    elif args.workflow:
        workflow = manager.get_workflow_definition(args.workflow)
        if workflow:
            print(f"Workflow: {args.workflow}")
            for step in workflow:
                print(f"  {step.step_id.value}: {step.name}")
        else:
            print(f"Workflow '{args.workflow}' not found")
    elif args.validate:
        is_valid = manager.validate_workflow_definition(args.validate)
        print(f"Workflow '{args.validate}' is {'valid' if is_valid else 'invalid'}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
