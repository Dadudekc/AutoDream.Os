"""Unit tests for agent vector integration initialization."""

from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2] / "src"))

from services.agent_vector_integration_core import (  # noqa: E402
    AgentVectorIntegrationCore,
)
from services.agent_vector_integration_operations import (  # noqa: E402
    AgentVectorIntegrationOperations,
)


def test_core_initialization() -> None:
    core = AgentVectorIntegrationCore(agent_id="Agent-9")
    assert core.config["collection_name"] == "agent_Agent-9"
    assert core.vector_integration["status"] == "initialized"


def test_operations_initialization() -> None:
    ops = AgentVectorIntegrationOperations(agent_id="Agent-9")
    assert ops.config["collection_name"] == "agent_Agent-9"
