from src.utils.test_components import ResultAggregator


def test_result_aggregator_summary():
    agg = ResultAggregator()
    agg.add({"success": True})
    agg.add({"success": False})
    summary = agg.summary()
    assert summary == {"total": 2, "successes": 1, "failures": 1}
