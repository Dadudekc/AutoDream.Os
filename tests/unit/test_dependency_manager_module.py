from src.testing.dependency_manager import DependencyManager


def test_dependency_manager_checks_modules():
    dm = DependencyManager()
    assert dm.check_dependency("json")
    assert not dm.check_dependency("definitely_missing_module")
