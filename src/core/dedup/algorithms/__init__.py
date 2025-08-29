"""Algorithm implementations for deduplication."""
from .detector import DuplicationDetector
from .parser import CodeParser

__all__ = ["DuplicationDetector", "CodeParser"]
