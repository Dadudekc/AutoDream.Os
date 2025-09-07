from src.web.frontend import ui_interactions, assertion_helpers


def test_assert_component_props():
    component = ui_interactions.create_mock_component("Button")
    assertion_helpers.assert_component_props(
        component,
        {
            "id": "test-id",
            "className": "test-class",
            "data-testid": "test-component",
        },
    )


def test_assert_route_config():
    route = ui_interactions.create_mock_route("/test")
    assertion_helpers.assert_route_config(route, "/test", "TestComponent")


def test_assert_navigation_state():
    state = ui_interactions.create_mock_navigation_state()
    assertion_helpers.assert_navigation_state(state, "/test")
