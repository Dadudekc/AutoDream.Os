"""File-based coordinate repository for messaging CLI."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from ..messaging_cli_utils import MessagingCLIUtils


@dataclass
class CoordinateRepository:
    """Read and write agent coordinates from a JSON file."""

    utils: MessagingCLIUtils
    file_path: str = "cursor_agent_coords.json"

    def _load_coords(self) -> Optional[Dict[str, any]]:
        return self.utils.read_json(self.file_path)

    def _save_coords(self, data: Dict[str, any]) -> bool:
        data["last_updated"] = datetime.now().isoformat()
        return self.utils.write_json(self.file_path, data)

    # ------------------------------------------------------------------
    # Update functions
    # ------------------------------------------------------------------
    def update_agent_coordinates(
        self, agent_id: str, onboarding: List[int], chat: List[int]
    ) -> Dict[str, any]:
        data = self._load_coords()
        if not data or agent_id not in data.get("agents", {}):
            return {"error": f"Agent {agent_id} not found"}
        agent = data["agents"][agent_id]
        agent["onboarding_input_coords"] = onboarding
        agent["chat_input_coordinates"] = chat
        if self._save_coords(data):
            return {
                "success": True,
                "agent_id": agent_id,
                "onboarding_coords": onboarding,
                "chat_coords": chat,
            }
        return {"error": "Failed to save coordinates"}

    def update_all_agents_coordinates(
        self, onboarding: List[int], chat: List[int]
    ) -> Dict[str, any]:
        data = self._load_coords()
        if not data:
            return {"error": "Could not load coordinates file"}
        agents = data.get("agents", {})
        for agent in agents.values():
            agent["onboarding_input_coords"] = onboarding
            agent["chat_input_coordinates"] = chat
        if self._save_coords(data):
            return {
                "success": True,
                "agents_updated": len(agents),
                "onboarding_coords": onboarding,
                "chat_coords": chat,
            }
        return {"error": "Failed to save coordinates"}

    def update_onboarding_coordinates(
        self, agent_id: str, onboarding: List[int]
    ) -> Dict[str, any]:
        data = self._load_coords()
        if not data or agent_id not in data.get("agents", {}):
            return {"error": f"Agent {agent_id} not found"}
        data["agents"][agent_id]["onboarding_input_coords"] = onboarding
        if self._save_coords(data):
            return {"success": True, "agent_id": agent_id, "onboarding_coords": onboarding}
        return {"error": "Failed to save coordinates"}

    def update_chat_coordinates(
        self, agent_id: str, chat: List[int]
    ) -> Dict[str, any]:
        data = self._load_coords()
        if not data or agent_id not in data.get("agents", {}):
            return {"error": f"Agent {agent_id} not found"}
        data["agents"][agent_id]["chat_input_coordinates"] = chat
        if self._save_coords(data):
            return {"success": True, "agent_id": agent_id, "chat_coords": chat}
        return {"error": "Failed to save coordinates"}

    def update_all_onboarding_coordinates(self, onboarding: List[int]) -> Dict[str, any]:
        data = self._load_coords()
        if not data:
            return {"error": "Could not load coordinates file"}
        for agent in data.get("agents", {}).values():
            agent["onboarding_input_coords"] = onboarding
        if self._save_coords(data):
            return {
                "success": True,
                "agents_updated": len(data.get("agents", {})),
                "onboarding_coords": onboarding,
            }
        return {"error": "Failed to save coordinates"}

    def update_all_chat_coordinates(self, chat: List[int]) -> Dict[str, any]:
        data = self._load_coords()
        if not data:
            return {"error": "Could not load coordinates file"}
        for agent in data.get("agents", {}).values():
            agent["chat_input_coordinates"] = chat
        if self._save_coords(data):
            return {
                "success": True,
                "agents_updated": len(data.get("agents", {})),
                "chat_coords": chat,
            }
        return {"error": "Failed to save coordinates"}

    # ------------------------------------------------------------------
    # Query functions
    # ------------------------------------------------------------------
    def get_chat_input_xy(self, agent_id: str) -> Tuple[int, int]:
        data = self._load_coords()
        coords = data and data.get("agents", {}).get(agent_id, {}).get(
            "chat_input_coordinates", [0, 0]
        )
        return tuple(coords) if coords else (0, 0)

    def get_onboarding_input_xy(self, agent_id: str) -> Tuple[int, int]:
        data = self._load_coords()
        coords = data and data.get("agents", {}).get(agent_id, {}).get(
            "onboarding_input_coords", [0, 0]
        )
        return tuple(coords) if coords else (0, 0)
