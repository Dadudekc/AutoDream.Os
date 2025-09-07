"""Set coordinates via simple commands or files."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, cast

from ..messaging_cli_utils import MessagingCLIUtils
from .coordinate_repository import CoordinateRepository
from .utilities import load_coords_file
from .validators import parse_coord_string


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
        try:
            agent_id, x, y = parse_coord_string(coord_string)
        except ValueError as exc:
            return {"error": str(exc)}
        return self.repository.update_onboarding_coordinates(agent_id, [x, y])

    def set_chat_coordinates(self, coord_string: str) -> Dict[str, Any]:
        try:
            agent_id, x, y = parse_coord_string(coord_string)
        except ValueError as exc:
            return {"error": str(exc)}
        return self.repository.update_chat_coordinates(agent_id, [x, y])

    def update_coordinates_from_file(self, file_path: str) -> Dict[str, Any]:
        data, error = load_coords_file(self.utils, file_path)
        if error:
            return {"error": error}
        data = cast(Dict[str, Any], data)
        if self.utils.write_json(self.repository.file_path, data):
            data["last_updated"] = datetime.now().isoformat()
            return {
                "success": True,
                "message": f"Updated coordinates from {file_path}",
                "agents_updated": len(data.get("agents", {})),
            }
        return {"error": "Failed to save coordinates"}
