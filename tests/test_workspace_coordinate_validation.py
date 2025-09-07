from scripts.validate_workspace_coords import validate_workspaces


def test_workspace_coordinates_consistency() -> None:
    assert validate_workspaces()

