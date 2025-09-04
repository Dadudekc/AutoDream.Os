#!/usr/bin/env python3
"""
Initialization Workflow Definitions
==================================

Provides initialization workflows for the unified workflow system.
Follows V2 standards: single source of truth, modular definitions.

Author: Agent-3 (Workflow Unification)
License: MIT
"""



# Single source of truth for initialization workflows
WORKFLOWS: Dict[str, WorkflowDefinition] = {
    "agent_onboarding": WorkflowDefinition(
        workflow_id="agent_onboarding",
        workflow_type=WorkflowType.INITIALIZATION,
        name="Agent Onboarding",
        description="Standard agent onboarding workflow",
        steps=[
            create_workflow_step(
                step_id="init",
                name="Initialization",
                step_type="initialization",
                description="Initialize agent system",
                dependencies=[],
                estimated_duration=30.0,
            ),
            create_workflow_step(
                step_id="training",
                name="Training",
                step_type="training",
                description="Conduct agent training",
                dependencies=["init"],
                estimated_duration=300.0,
            ),
            create_workflow_step(
                step_id="role_assignment",
                name="Role Assignment",
                step_type="role_assignment",
                description="Assign agent role",
                dependencies=["training"],
                estimated_duration=60.0,
            ),
            create_workflow_step(
                step_id="completion",
                name="Completion",
                step_type="completion",
                description="Complete onboarding",
                dependencies=["role_assignment"],
                estimated_duration=30.0,
            ),
        ],
    )
}


def get_workflows() -> Dict[str, WorkflowDefinition]:
    """Return initialization workflows."""
    return WORKFLOWS
