"""Core models for the middleware orchestration system.

This module defines enums and dataclasses that describe middleware
components and data packets flowing through the system.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set


class MiddlewareType(Enum):
    """Types of middleware for categorization."""

    PREPROCESSING = "preprocessing"
    PROCESSING = "processing"
    POSTPROCESSING = "postprocessing"
    ROUTING = "routing"
    VALIDATION = "validation"
    TRANSFORMATION = "transformation"
    MONITORING = "monitoring"


class DataFlowDirection(Enum):
    """Direction of data flow through middleware."""

    INBOUND = "inbound"
    OUTBOUND = "outbound"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class MiddlewareChain:
    """Represents a chain of middleware components.

    The order of ``middleware_list`` defines the execution sequence. Components
    are invoked in list order and may mutate the ``DataPacket`` before passing
    it to the next middleware.
    """

    name: str
    middleware_list: List[str] = field(default_factory=list)
    enabled: bool = True
    priority: int = 0
    conditions: Dict[str, Any] = field(default_factory=dict)
    description: str = ""


@dataclass
class DataPacket:
    """Represents a data packet flowing through the middleware system.

    Middleware components are expected to mutate instances of this class in
    place. Typical mutations include altering ``data``, appending tags to
    ``tags``, recording steps in ``processing_history``, updating the
    ``destination`` during routing, and adding contextual information to the
    ``metadata`` dictionary.
    """

    id: str
    data: Any
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    source: str = ""
    destination: str = ""
    flow_direction: DataFlowDirection = DataFlowDirection.INBOUND
    tags: Set[str] = field(default_factory=set)
    processing_history: List[str] = field(default_factory=list)
