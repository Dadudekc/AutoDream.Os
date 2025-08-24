"""Unit tests for frontend testing utilities."""
import pytest  # noqa: F401

pytest_plugins = ["src.web.frontend.testing.fixtures"]

from src.web.frontend.testing import fixtures as frontend_fixtures  # noqa: F401


def test_create_mock_component(ui_utils, assertion_helpers):
    component = ui_utils.create_mock_component("Button")
    assertion_helpers.assert_component_props(
        component, {"data-testid": "test-component"}
    )
    assert component.type == "Button"


def test_route_and_navigation_helpers(ui_utils, assertion_helpers):
    route = ui_utils.create_mock_route("/test")
    assertion_helpers.assert_route_config(route, "/test", "TestComponent")

    state = ui_utils.create_mock_navigation_state()
    assertion_helpers.assert_navigation_state(state, "/test")
