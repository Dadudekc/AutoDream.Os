import os
import sys
import json

sys.path.append(os.path.abspath("."))

from src.agent_registry import COORDINATES  # noqa: E402
from src.services.handlers.utility_handler import UtilityHandler  # noqa: E402
from src.services.messaging_handlers_engine import (  # noqa: E402
    MessagingHandlersEngine,
)


def test_utility_handler_coordinates():
    handler = UtilityHandler()
    assert handler.get_coordinates() == COORDINATES


def test_messaging_engine_coordinates():
    engine = MessagingHandlersEngine()
    for agent_id, data in COORDINATES.items():
        coord = engine.get_agent_coordinates(agent_id)
        assert coord is not None
        assert coord.x == data["x"]
        assert coord.y == data["y"]
        assert coord.description == data.get("description", "")


def test_registry_matches_ssot():
    with open("cursor_agent_coords.json", "r", encoding="utf-8") as f:
        ssot = json.load(f)["agents"]
    for agent_id, info in ssot.items():
        chat = info.get("chat_input_coordinates", [0, 0])
        assert COORDINATES[agent_id]["x"] == chat[0]
        assert COORDINATES[agent_id]["y"] == chat[1]
