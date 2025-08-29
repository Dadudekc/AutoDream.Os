from __future__ import annotations

from typing import Optional


class HandshakeNegotiator:
    """Perform handshake negotiation between agents."""

    def __init__(self, auth_manager, protocol_version: str, logger):
        self._auth_manager = auth_manager
        self._protocol_version = protocol_version
        self._logger = logger

    def negotiate(self, peer_id: str, token: str, version: str) -> bool:
        """Validate the provided token and protocol version."""
        if version != self._protocol_version:
            self._logger.warning(
                f"Protocol mismatch: expected {self._protocol_version}, got {version}"
            )
            return False

        agent_id = self._auth_manager.validate_agent_token(token)
        if agent_id != peer_id:
            self._logger.warning("Authentication failed during handshake")
            return False

        self._logger.info(f"Handshake successful with {peer_id}")
        return True
