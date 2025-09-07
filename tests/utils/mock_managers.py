from pathlib import Path


class MockWorkspaceManager:
    """Mock workspace manager for testing."""

    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.workspaces = {}

    def get_sprints_path(self):
        sprints_path = self.base_path / "sprints"
        sprints_path.mkdir(parents=True, exist_ok=True)
        return sprints_path


class MockTaskManager:
    """Mock task manager for testing."""

    def __init__(self):
        self.tasks = {}

    def get_task(self, task_id):
        return self.tasks.get(task_id)


class MockFSMOrchestrator:
    """Mock FSM orchestrator for workflow tests."""

    def create_task(self, title, description, assigned_agent, priority):
        return f"TASK-{hash(title)}"

    def update_task_status(self, task_id, status):
        return True


class MockAgentManager:
    """Simple mock agent manager."""

    pass


class MockResponseCaptureService:
    """Simple mock response capture service."""

    pass


class MockWorkflowEngine:
    """Minimal mock workflow engine."""

    pass
