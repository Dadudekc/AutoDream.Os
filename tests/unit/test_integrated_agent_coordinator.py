import pytest

from src.services.integrated_agent_coordinator import IntegratedAgentCoordinator
from src.services.agent_registry import AgentRegistry
from src.services.task_assigner import TaskAssigner
from src.core.communication import CommunicationManager


def test_agent_lifecycle():
    coord = IntegratedAgentCoordinator()
    coord.register_agent("agent1", {"role": "tester"})
    assert "agent1" in coord.agent_ids()

    coord.assign_task("agent1", "do stuff")
    coord.send_message("agent1", "hello")

    assert coord.get_agent_tasks("agent1") == ["do stuff"]
    assert coord.get_agent_messages("agent1") == ["hello"]

    coord.deregister_agent("agent1")
    assert "agent1" not in coord.agent_ids()


def test_coordination_flow_with_custom_components():
    registry = AgentRegistry()
    tasks = TaskAssigner()
    comms = CommunicationManager()
    coord = IntegratedAgentCoordinator(registry, tasks, comms)

    coord.register_agent("a1")
    coord.register_agent("a2")

    coord.assign_task("a1", "task1")
    coord.assign_task("a2", "task2")
    coord.send_message("a1", "msg1")
    coord.send_message("a2", "msg2")

    assert tasks.get_tasks("a1") == ["task1"]
    assert tasks.get_tasks("a2") == ["task2"]
    assert comms.get_messages("a1") == ["msg1"]
    assert comms.get_messages("a2") == ["msg2"]
