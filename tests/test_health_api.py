import importlib


def test_health_and_health_threshold_same_api():
    health = importlib.import_module("core.health")
    health_threshold = importlib.import_module("core.health_threshold")

    assert set(health.__all__) == set(health_threshold.__all__)
    for name in health.__all__:
        assert getattr(health, name) is getattr(health_threshold, name)
