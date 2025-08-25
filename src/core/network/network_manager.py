"""Orchestrator for network operations."""

from .network_manager_core import NetworkManagerCore


class NetworkManager:
    """High-level interface coordinating network components."""

    def __init__(self) -> None:
        self.core = NetworkManagerCore()

    def connect(self, host: str, port: int) -> None:
        """Establish a new network connection."""
        self.core.open(host, port)

    def disconnect(self) -> None:
        """Close the current network connection."""
        self.core.close()

    def send(self, data: str) -> bytes:
        """Send data over the active connection."""
        return self.core.send(data)

    def receive(self, payload: bytes) -> str:
        """Receive data from the active connection."""
        return self.core.receive(payload)
