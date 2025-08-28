import pytest

from src.core.agent_manager import AgentManager
from src.core.assignment_engine import ContractManager
from src.core.config_manager import ConfigManager
from src.core.contract_models import ContractPriority
from src.core.optimization import (
    AssignmentOptimizer,
    AssignmentMetrics,
    CapabilityScoringStrategy,
)


def test_scoring_strategy():
    scoring = CapabilityScoringStrategy()
    contract_required = ["python", "ml"]
    agent_info = {"capabilities": ["python"]}
    score = scoring.score(
        contract=type("C", (), {"required_capabilities": contract_required})(),
        agent_info=agent_info,
    )
    assert score == pytest.approx(0.5)


def test_assignment_optimizer_selects_best_agent():
    optimizer = AssignmentOptimizer()
    contract = type("C", (), {"required_capabilities": ["python"]})()
    agents = {
        "a1": {"capabilities": ["python"]},
        "a2": {"capabilities": ["rust"]},
    }
    chosen, score = optimizer.choose_agent(contract, agents)
    assert chosen == "a1"
    assert score == pytest.approx(1.0)


def test_contract_manager_integration():
    agent_manager = AgentManager()
    agent_manager.register_agent("agent-1", ["python"])
    config = ConfigManager()
    metrics = AssignmentMetrics()
    optimizer = AssignmentOptimizer()
    manager = ContractManager(agent_manager, config, optimizer, metrics)
    contract_id = manager.create_contract(
        title="Test",
        description="desc",
        priority=ContractPriority.NORMAL,
        required_capabilities=["python"],
    )
    assert manager.assign_contract(contract_id)
    summary = manager.get_contract_summary()
    assert summary["active_contracts"] == 1
    assert metrics.average_score() == pytest.approx(1.0)
