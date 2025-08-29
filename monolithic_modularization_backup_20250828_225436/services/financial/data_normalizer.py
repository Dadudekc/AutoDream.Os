"""Data normalization module for unified financial API."""
from dataclasses import asdict, is_dataclass
from typing import Any


class DataNormalizer:
    """Normalize responses from financial services."""

    def normalize(self, data: Any) -> Any:
        """Normalize data into serialisable structures."""
        if is_dataclass(data):
            return asdict(data)
        return data
