import pytest

from services.messaging_cli_coordinate_management.validators import parse_coord_string


def test_parse_coord_string_valid():
    agent_id, x, y = parse_coord_string("Agent-1,10,20")
    assert agent_id == "Agent-1"
    assert (x, y) == (10, 20)


def test_parse_coord_string_invalid_format():
    with pytest.raises(ValueError):
        parse_coord_string("invalid")


def test_parse_coord_string_non_integer():
    with pytest.raises(ValueError):
        parse_coord_string("Agent-1,x,20")
