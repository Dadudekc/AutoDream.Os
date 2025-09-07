from typing import Dict


class AuthenticationService:
    """Simple token-based authentication for agents."""

    def __init__(self) -> None:
        self._tokens: Dict[str, str] = {}

    def register_agent(self, agent_id: str, token: str) -> None:
        self._tokens[agent_id] = token

    def authenticate(self, agent_id: str, token: str) -> bool:
        stored = self._tokens.get(agent_id)
        return stored is not None and stored == token
