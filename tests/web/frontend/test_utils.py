from src.web.frontend import utils


def test_create_mock_component_util():
    component = utils.create_mock_component("SampleComponent")
    assert component.type == "SampleComponent"
    assert component.props["id"] == "test-id"


def test_create_mock_route_util():
    route = utils.create_mock_route("/sample")
    assert route.path == "/sample"
    assert route.component == "TestComponent"


def test_create_mock_navigation_state_util():
    state = utils.create_mock_navigation_state()
    assert state.current_route == "/test"
    assert state.previous_route == "/"
