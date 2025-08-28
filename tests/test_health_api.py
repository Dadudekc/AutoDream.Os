import importlib


def test_health_exports_health_base_api():
    health = importlib.import_module("core.health")
    health_base = importlib.import_module("core.health_base")

    assert set(health.__all__) == set(health_base.__all__)
    for name in health.__all__:
        assert getattr(health, name) is getattr(health_base, name)
