from __future__ import annotations

import pytest

from src.services.financial.unified_financial_api import (
    UnifiedFinancialAPI,
)
from src.services.financial.api_authentication import APIAuthenticator
from src.services.financial.api_error_handler import APIErrorHandler
from src.services.financial.api_data_aggregator import DataAggregator


class DummyAuthenticator(APIAuthenticator):
    def __init__(self):
        self.calls: list[tuple[str, str]] = []

    def authorize(self, source_agent, target_service, registered_agents):
        self.calls.append((source_agent, target_service))
        return super().authorize(source_agent, target_service, registered_agents)


class DummyRouter:
    def __init__(self, should_fail: bool = False):
        self.called = False
        self.should_fail = should_fail

    def route(self, target_service, request_type, request_data):
        self.called = True
        if self.should_fail:
            raise RuntimeError("router failure")
        return {"routed": True}


class DummyAggregator(DataAggregator):
    def __init__(self):
        self.called = False

    def aggregate_system_health(self, registered_agents, performance_metrics):
        self.called = True
        return super().aggregate_system_health(registered_agents, performance_metrics)


class DummyErrorHandler(APIErrorHandler):
    def __init__(self):
        self.called = False

    def handle(self, request_id, error, request, performance_metrics, response_cls):
        self.called = True
        return super().handle(request_id, error, request, performance_metrics, response_cls)


def _setup_api(should_fail=False):
    auth = DummyAuthenticator()
    router = DummyRouter(should_fail=should_fail)
    aggregator = DummyAggregator()
    err = DummyErrorHandler()
    api = UnifiedFinancialAPI(
        authenticator=auth,
        router=router,
        aggregator=aggregator,
        error_handler=err,
    )
    return api, auth, router, aggregator, err


def test_facade_coordinates_components_success():
    api, auth, router, aggregator, err = _setup_api()

    api.register_agent(
        agent_id="A1",
        agent_name="Agent 1",
        agent_type="TEST",
        required_services=["portfolio_management"],
    )

    req_id = api.request_service(
        "A1", "portfolio_management", "get_portfolio", {}
    )
    resp = api.execute_service_request(req_id)

    assert resp.status == "SUCCESS"
    assert auth.calls == [("A1", "portfolio_management")]
    assert router.called
    assert not err.called

    api.get_system_health_metrics()
    assert aggregator.called


def test_error_handler_invoked_on_failure():
    api, auth, router, aggregator, err = _setup_api(should_fail=True)

    api.register_agent(
        agent_id="A1",
        agent_name="Agent 1",
        agent_type="TEST",
        required_services=["portfolio_management"],
    )

    req_id = api.request_service(
        "A1", "portfolio_management", "get_portfolio", {}
    )
    resp = api.execute_service_request(req_id)

    assert resp.status == "ERROR"
    assert err.called
    assert router.called
