"""Network connection utilities."""

from dataclasses import dataclass


@dataclass
class NetworkConnection:
    """Represents a basic network connection."""

    host: str
    port: int
    connected: bool = False

    def connect(self) -> None:
        """Mark the connection as active."""
        self.connected = True

    def disconnect(self) -> None:
        """Mark the connection as inactive."""
        self.connected = False
