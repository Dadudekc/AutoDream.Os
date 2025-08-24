from datetime import datetime
from src.services.financial.api_persistence import PersistenceManager
from src.services.financial.models import AgentRegistration, CrossAgentRequest


def test_save_and_load_roundtrip(tmp_path):
    agents = {}
    requests = []
    metrics = {}

    pm = PersistenceManager(
        tmp_path / "agents.json",
        tmp_path / "requests.json",
        tmp_path / "perf.json",
    )

    agent = AgentRegistration(
        agent_id="A1",
        agent_name="Agent 1",
        agent_type="TEST",
        required_services=["portfolio_management"],
        registration_time=datetime.now(),
        last_heartbeat=datetime.now(),
        status="ACTIVE",
    )
    agents["A1"] = agent
    req = CrossAgentRequest(
        request_id="R1",
        source_agent="A1",
        target_service="portfolio_management",
        request_type="get_portfolio",
        request_data={},
        timestamp=datetime.now(),
        priority="MEDIUM",
        status="PENDING",
    )
    requests.append(req)
    metrics["A1"] = {"total_requests": 1}

    pm.save(agents, requests, metrics)

    loaded_agents: dict = {}
    loaded_requests: list = []
    loaded_metrics: dict = {}
    pm.load(loaded_agents, loaded_requests, loaded_metrics)

    assert "A1" in loaded_agents
    assert loaded_agents["A1"].agent_name == "Agent 1"
    assert loaded_requests[0].request_id == "R1"
    assert loaded_metrics["A1"]["total_requests"] == 1
