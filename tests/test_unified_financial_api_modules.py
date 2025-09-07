"""Tests for refactored unified financial API modules."""
from dataclasses import dataclass

from src.services.financial.data_aggregator import DataAggregator
from src.services.financial.data_normalizer import DataNormalizer
from src.services.financial.request_handler import RequestHandler
from src.services.financial.response_formatter import ResponseFormatter
from src.services.financial.unified_financial_api import UnifiedFinancialAPI


@dataclass
class DummyData:
    value: int


def test_aggregator_returns_payload():
    aggregator = DataAggregator()
    result = aggregator.aggregate("svc", "op", {"a": 1})
    assert result == {"service": "svc", "type": "op", "payload": {"a": 1}}


def test_normalizer_converts_dataclass():
    normalizer = DataNormalizer()
    assert normalizer.normalize(DummyData(5)) == {"value": 5}


def test_response_formatter_creates_response():
    formatter = ResponseFormatter()
    resp = formatter.format("id", {"x": 1}, 0.0)
    assert resp.request_id == "id"
    assert resp.response_data == {"x": 1}
    assert resp.status == "SUCCESS"


def test_request_handler_flow():
    handler = RequestHandler(DataAggregator(), DataNormalizer(), ResponseFormatter())
    rid = handler.create_request("agent", "svc", "op", {"a": 2})
    resp = handler.execute_request(rid)
    assert resp.request_id == rid
    assert resp.response_data["payload"]["a"] == 2
    assert resp.status == "SUCCESS"


def test_unified_api_handles_request():
    api = UnifiedFinancialAPI()
    resp = api.handle_request("agent", "svc", "op", {"a": 3})
    assert resp.response_data["payload"]["a"] == 3
    assert resp.status == "SUCCESS"
