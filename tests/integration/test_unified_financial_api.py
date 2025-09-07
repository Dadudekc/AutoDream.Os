import pytest

from src.services.financial.unified_financial_api import UnifiedFinancialAPI


@pytest.fixture
def api():
    return UnifiedFinancialAPI()


def _register(api: UnifiedFinancialAPI):
    assert api.register_agent(
        agent_id="AGENT", 
        agent_name="Agent", 
        agent_type="TEST", 
        required_services=["portfolio_management"],
        api_token="token",
    )


def test_successful_service_request(api):
    _register(api)
    request_id = api.request_service(
        source_agent="AGENT",
        target_service="portfolio_management",
        request_type="get_portfolio",
        request_data={},
        api_token="token",
    )
    response = api.execute_service_request(request_id)
    assert response.status == "SUCCESS"


def test_authentication_failure(api):
    _register(api)
    with pytest.raises(PermissionError):
        api.request_service(
            source_agent="AGENT",
            target_service="portfolio_management",
            request_type="get_portfolio",
            request_data={},
            api_token="wrong",
        )


def test_error_handling(api):
    _register(api)
    request_id = api.request_service(
        source_agent="AGENT",
        target_service="portfolio_management",
        request_type="unknown",
        request_data={},
        api_token="token",
    )
    response = api.execute_service_request(request_id)
    assert response.status == "ERROR"
    assert response.error_message
