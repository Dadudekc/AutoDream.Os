"""Set coordinates via simple commands or files."""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any, Dict, List

from ..messaging_cli_utils import MessagingCLIUtils
from .coordinate_repository import CoordinateRepository


class CoordinateSetter:
    """High level coordinate setting utilities."""

    def __init__(
        self,
        repository: CoordinateRepository,
        utils: MessagingCLIUtils,
    ) -> None:
        self.repository = repository
        self.utils = utils

    def set_onboarding_coordinates(self, coord_string: str) -> Dict[str, Any]:
        parts = coord_string.split(",")
        if len(parts) != 3:
            return {"error": "Invalid format. Use: agent_id,x,y"}
        agent_id, x_str, y_str = parts
        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            return {"error": "Coordinates must be integers"}
        return self.repository.update_onboarding_coordinates(agent_id, [x, y])

    def set_chat_coordinates(self, coord_string: str) -> Dict[str, Any]:
        parts = coord_string.split(",")
        if len(parts) != 3:
            return {"error": "Invalid format. Use: agent_id,x,y"}
        agent_id, x_str, y_str = parts
        try:
            x, y = int(x_str), int(y_str)
        except ValueError:
            return {"error": "Coordinates must be integers"}
        return self.repository.update_chat_coordinates(agent_id, [x, y])

    def update_coordinates_from_file(self, file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"error": f"File {file_path} not found"}
        new_coords = self.utils.read_json(file_path)
        if not new_coords or "agents" not in new_coords:
            return {"error": "Invalid coordinates file"}
        if self.utils.write_json(self.repository.file_path, new_coords):
            new_coords["last_updated"] = datetime.now().isoformat()
            return {
                "success": True,
                "message": f"Updated coordinates from {file_path}",
                "agents_updated": len(new_coords.get("agents", {})),
            }
        return {"error": "Failed to save coordinates"}
