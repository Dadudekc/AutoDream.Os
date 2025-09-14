"""
Compression Strategy
===================

Data compression optimization strategies.
"""

import gzip
import zlib
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class CompressionConfig:
    """Configuration for compression strategy."""
    algorithm: str = "gzip"
    level: int = 6
    threshold: int = 1024  # Only compress if data is larger than this


class CompressionStrategy(ABC):
    """Abstract base class for compression strategies."""
    
    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        """Compress data."""
        pass
    
    @abstractmethod
    def decompress(self, compressed_data: bytes) -> bytes:
        """Decompress data."""
        pass


class GzipCompression(CompressionStrategy):
    """Gzip compression strategy."""
    
    def __init__(self, level: int = 6):
        """Initialize gzip compression."""
        self.level = level
    
    def compress(self, data: bytes) -> bytes:
        """Compress data using gzip."""
        return gzip.compress(data, compresslevel=self.level)
    
    def decompress(self, compressed_data: bytes) -> bytes:
        """Decompress gzip data."""
        return gzip.decompress(compressed_data)


class ZlibCompression(CompressionStrategy):
    """Zlib compression strategy."""
    
    def __init__(self, level: int = 6):
        """Initialize zlib compression."""
        self.level = level
    
    def compress(self, data: bytes) -> bytes:
        """Compress data using zlib."""
        return zlib.compress(data, level=self.level)
    
    def decompress(self, compressed_data: bytes) -> bytes:
        """Decompress zlib data."""
        return zlib.decompress(compressed_data)


class CompressionStrategyFactory:
    """Factory for creating compression strategies."""
    
    @staticmethod
    def create_strategy(config: CompressionConfig) -> CompressionStrategy:
        """Create compression strategy based on config."""
        if config.algorithm == "gzip":
            return GzipCompression(config.level)
        elif config.algorithm == "zlib":
            return ZlibCompression(config.level)
        else:
            raise ValueError(f"Unsupported compression algorithm: {config.algorithm}")

