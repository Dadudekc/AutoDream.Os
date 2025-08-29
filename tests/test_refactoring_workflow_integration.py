import time

from tools.refactoring_workflow import (
    AutomatedRefactoringWorkflowSystem,
    WorkflowState,
)


def wait_for_completion(system: AutomatedRefactoringWorkflowSystem, execution_id: str):
    start = time.time()
    while time.time() - start < 5:
        status = system.get_workflow_status(execution_id)
        if not status:
            break
        time.sleep(0.1)
    history = system.get_workflow_history()
    return next((e for e in history if e.id == execution_id), None)


def test_code_analysis_workflow_matches_original():
    system = AutomatedRefactoringWorkflowSystem()
    exec_id = system.execute_code_analysis_workflow(["dummy.py"])
    execution = wait_for_completion(system, exec_id)
    assert execution is not None
    assert execution.state == WorkflowState.COMPLETED
    assert len(execution.steps_completed) == 3
    assert execution.performance_metrics["success_rate"] == 1.0


def test_modularization_workflow_matches_original():
    system = AutomatedRefactoringWorkflowSystem()
    exec_id = system.execute_modularization_workflow(["dummy.py"])
    execution = wait_for_completion(system, exec_id)
    assert execution is not None
    assert execution.state == WorkflowState.COMPLETED
    assert len(execution.steps_completed) == 3
