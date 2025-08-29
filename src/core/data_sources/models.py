from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class DataSourceType(Enum):
    """Unified data source types."""
    DATABASE = "database"
    FILE = "file"
    API = "api"
    MEMORY = "memory"
    CACHE = "cache"
    EXTERNAL = "external"
    MOCK = "mock"
    STREAM = "stream"
    FINANCIAL = "financial"
    SENTIMENT = "sentiment"
    MARKET = "market"
    CONFIGURATION = "configuration"
    SYSTEM = "system"


class DataType(Enum):
    """Unified data types."""
    CONFIGURATION = "configuration"
    PERFORMANCE = "performance"
    USER = "user"
    SYSTEM = "system"
    BUSINESS = "business"
    ANALYTICS = "analytics"
    LOGS = "logs"
    METRICS = "metrics"
    FINANCIAL = "financial"
    MARKET = "market"
    SENTIMENT = "sentiment"
    OPTIONS = "options"
    INSIDER_TRADING = "insider_trading"


class DataPriority(Enum):
    """Data priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


@dataclass
class DataSource:
    """Unified data source definition."""
    id: str
    name: str
    type: DataSourceType
    data_type: DataType
    location: str
    priority: DataPriority = DataPriority.NORMAL
    enabled: bool = True
    last_updated: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_rules: Dict[str, Any] = field(default_factory=dict)
    access_patterns: List[str] = field(default_factory=list)
    original_service: str = ""
    migration_status: str = "pending"


@dataclass
class DataRecord:
    """Unified data record structure."""
    id: str
    data_type: DataType
    source_id: str
    data: Any
    timestamp: str
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_status: str = "pending"
    last_accessed: str = ""
