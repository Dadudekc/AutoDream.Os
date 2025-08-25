"""Simple network protocol helpers."""

class NetworkProtocol:
    """Handles encoding and decoding of data."""

    def __init__(self, version: str = "1.0") -> None:
        self.version = version

    def encode(self, data: str) -> bytes:
        """Encode a string into bytes."""
        return data.encode("utf-8")

    def decode(self, payload: bytes) -> str:
        """Decode bytes back into a string."""
        return payload.decode("utf-8")
