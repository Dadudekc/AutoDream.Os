from src.web.frontend import ui_interactions


def test_create_mock_component():
    component = ui_interactions.create_mock_component("TestButton")
    assert component.type == "TestButton"
    assert component.props["id"] == "test-id"


def test_create_mock_route():
    route = ui_interactions.create_mock_route("/example")
    assert route.path == "/example"
    assert route.component == "TestComponent"


def test_create_mock_navigation_state():
    state = ui_interactions.create_mock_navigation_state()
    assert state.current_route == "/test"
    assert state.previous_route == "/"
