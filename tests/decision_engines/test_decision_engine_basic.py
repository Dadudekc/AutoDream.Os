def test_decision_engine_positive(decision_engine):
    assert decision_engine.decide(1) == "positive"


def test_decision_engine_non_positive(decision_engine):
    assert decision_engine.decide(-1) == "non-positive"
