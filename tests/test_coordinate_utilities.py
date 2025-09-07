import json

from services.messaging_cli_coordinate_management.utilities import load_coords_file
from services.messaging_cli_utils import MessagingCLIUtils


def test_load_coords_file_valid(tmp_path):
    utils = MessagingCLIUtils()
    file_path = tmp_path / "coords.json"
    data = {"agents": {"A": {}}}
    file_path.write_text(json.dumps(data))
    loaded, error = load_coords_file(utils, str(file_path))
    assert error is None
    assert loaded == data


def test_load_coords_file_missing(tmp_path):
    utils = MessagingCLIUtils()
    loaded, error = load_coords_file(utils, str(tmp_path / "missing.json"))
    assert loaded is None
    assert "not found" in error.lower()


def test_load_coords_file_invalid(tmp_path):
    utils = MessagingCLIUtils()
    file_path = tmp_path / "bad.json"
    file_path.write_text(json.dumps({"no_agents": {}}))
    loaded, error = load_coords_file(utils, str(file_path))
    assert loaded is None
    assert error == "Invalid coordinates file"
