"""Core network management logic."""

from typing import Optional

from .network_connection import NetworkConnection
from .network_protocol import NetworkProtocol


class NetworkManagerCore:
    """Handles low-level network operations."""

    def __init__(self) -> None:
        self.connection: Optional[NetworkConnection] = None
        self.protocol = NetworkProtocol()

    def open(self, host: str, port: int) -> None:
        """Open a connection to the specified host and port."""
        self.connection = NetworkConnection(host, port)
        self.connection.connect()

    def close(self) -> None:
        """Close the active connection if one exists."""
        if self.connection:
            self.connection.disconnect()
            self.connection = None

    def send(self, data: str) -> bytes:
        """Send data using the active protocol."""
        if not self.connection or not self.connection.connected:
            raise RuntimeError("No active connection")
        payload = self.protocol.encode(data)
        return payload

    def receive(self, payload: bytes) -> str:
        """Decode incoming payload using the protocol."""
        return self.protocol.decode(payload)
