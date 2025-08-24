"""Smoke tests for the setup workflow modules."""

from scripts.setup import (
    backend_api,
    cli,
    dependency_install,
    env_config,
    frontend_tooling,
    testing_setup,
)


def test_env_config_smoke():
    result = env_config.setup_environment()
    assert result["status"] == "environment configured"


def test_dependency_install_smoke():
    result = dependency_install.install_dependencies()
    assert result["status"] == "dependencies installed"


def test_frontend_tooling_smoke():
    result = frontend_tooling.setup_frontend()
    assert result["status"] == "frontend tooling ready"


def test_backend_api_smoke():
    result = backend_api.setup_backend()
    assert result["status"] == "backend APIs configured"


def test_testing_setup_smoke():
    result = testing_setup.setup_testing()
    assert result["status"] == "testing setup complete"


def test_cli_runs_all_steps():
    results = cli.main([])
    statuses = [r["status"] for r in results]
    assert "environment configured" in statuses
    assert "dependencies installed" in statuses
    assert "frontend tooling ready" in statuses
    assert "backend APIs configured" in statuses
    assert "testing setup complete" in statuses
    assert len(results) == 5
