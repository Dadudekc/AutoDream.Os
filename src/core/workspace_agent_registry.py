# src/core/agent_registry.py
from __future__ import annotations

import json
import os


class AgentRegistry:
    def __init__(self, root: str = "agent_workspaces") -> None:
        self.root = root
        os.makedirs(self.root, exist_ok=True)

    def list_agents(self) -> list[str]:
        if not os.path.isdir(self.root):
            return []
        return sorted(
            [
                d
                for d in os.listdir(self.root)
                if d.startswith("Agent-") and os.path.isdir(os.path.join(self.root, d))
            ]
        )

    def _status_path(self, agent_id: str) -> str:
        return os.path.join(self.root, agent_id, "status.json")

    def _onboard_path(self, agent_id: str) -> str:
        return os.path.join(self.root, agent_id, "onboarding.json")

    # --- Mutations ---
    def reset_statuses(self, agents: list[str]) -> None:
        for a in agents:
            p = self._status_path(a)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"state": "RESET", "updated": True}, f)

    def clear_onboarding_flags(self, agents: list[str]) -> None:
        for a in agents:
            p = self._onboard_path(a)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as f:
                json.dump({"onboarded": False, "hard_onboarding": True}, f)

    def force_onboard(self, agent_id: str, timeout: int = 30) -> None:
        """Send aggressive onboarding messages via your existing messaging bus.

        Here we simulate by marking onboarded=True. Replace with real bus call.
        """
        p = self._onboard_path(agent_id)
        data = {"onboarded": True, "hard_onboarding": True, "timeout": timeout}
        with open(p, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def verify_onboarded(self, agent_id: str) -> bool:
        p = self._onboard_path(agent_id)
        if not os.path.exists(p):
            return False
        try:
            data = json.load(open(p, encoding="utf-8"))
            return bool(data.get("onboarded") is True)
        except Exception:
            return False

    def synchronize(self) -> None:
        """Force a global sync across agents.

        Stub for now; integrate your real sync.
        """
        # e.g., touch a sync marker file
        with open(os.path.join(self.root, "_sync.ok"), "w", encoding="utf-8") as f:
            f.write("ok")

    # NEW: persist last onboarding message for programmatic path
    def save_last_onboarding_message(self, agent_id: str, message: str) -> None:
        agent_dir = os.path.join(self.root, agent_id)
        os.makedirs(agent_dir, exist_ok=True)
        p = os.path.join(agent_dir, "last_onboarding_message.txt")
        with open(p, "w", encoding="utf-8") as f:
            f.write(message)

    def get_onboarding_coords(self, agent_id: str) -> tuple[int, int]:
        """Get onboarding coordinates for an agent.

        Uses SSOT coordinate loader for consistency across the system.

        Args:
            agent_id: Agent identifier

        Returns:
            Tuple of (x, y) coordinates
        """
        try:
            from .coordinate_loader import get_coordinate_loader

            loader = get_coordinate_loader()
            return loader.get_onboarding_coordinates(agent_id)
        except Exception:
            return (0, 0)
