import json
from services.messaging_cli_coordinate_management import MessagingCLICoordinateManagement


def test_update_and_get_coords(tmp_path):
    coords_file = tmp_path / "coords.json"
    coords_file.write_text(
        json.dumps({"agents": {"Agent-1": {"onboarding_input_coords": [0, 0], "chat_input_coordinates": [0, 0]}}})
    )
    mgr = MessagingCLICoordinateManagement(coords_file=str(coords_file))
    result = mgr.update_agent_coordinates("Agent-1", [1, 2], [3, 4])
    assert result["success"]
    assert mgr.get_chat_input_xy("Agent-1") == (3, 4)
    assert mgr.get_onboarding_input_xy("Agent-1") == (1, 2)
