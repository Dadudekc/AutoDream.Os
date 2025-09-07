#!/usr/bin/env python3
"""
Data Source Types - Core enums and constants
============================================

Defines all data source types, data types, and priority levels
for the unified data source consolidation system.
"""

from enum import Enum


class DataSourceType(Enum):
    """Unified data source types"""
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
    """Unified data types"""
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
    OPTIONS = "insider_trading"
    INSIDER_TRADING = "insider_trading"


class DataPriority(Enum):
    """Data priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5


class DataAccessPattern(Enum):
    """Data access patterns"""
    READ_ONLY = "read_only"
    WRITE_ONLY = "write_only"
    READ_WRITE = "read_write"
    BATCH = "batch"
    STREAMING = "streaming"
    CACHED = "cached"


class DataValidationLevel(Enum):
    """Data validation levels"""
    NONE = "none"
    BASIC = "basic"
    STRICT = "strict"
    CUSTOM = "custom"
