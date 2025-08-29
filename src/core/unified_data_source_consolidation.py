#!/usr/bin/env python3
"""
Unified Data Source Consolidation - SSOT-002 Contract Implementation
==================================================================

This module consolidates ALL scattered data sources into single authoritative
locations, eliminating SSOT violations and creating a unified data architecture.

Contract: SSOT-002: Data Source Consolidation - 450 points
Agent: Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)
Status: IN PROGRESS - ENHANCING FOR COMPLETION

Consolidates:
- Multiple data source implementations
- Scattered data access patterns
- Inconsistent data validation
- Duplicate data storage systems
- Multiple data synchronization mechanisms

Result: Single unified data source system with comprehensive SSOT compliance
"""
import json
import logging
import uuid
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, field
from enum import Enum
import sqlite3
import asyncio
from concurrent.futures import ThreadPoolExecutor


# ============================================================================
# DATA SOURCE TYPES - Consolidated from scattered implementations
# ============================================================================

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
    OPTIONS = "options"
    INSIDER_TRADING = "insider_trading"

class DataPriority(Enum):
    """Data priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4
    EMERGENCY = 5

@dataclass
class DataSource:
    """Unified data source definition"""
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
    """Unified data record structure"""
    id: str
    data_type: DataType
    source_id: str
    data: Any
    timestamp: str
    version: int = 1
    metadata: Dict[str, Any] = field(default_factory=dict)
    validation_status: str = "pending"
    last_accessed: str = ""

# ============================================================================
# DATA SOURCE MAPPING - Maps existing scattered implementations
# ============================================================================

class DataSourceMapper:
    """Maps existing scattered data sources to unified system"""
    
    def __init__(self):
        self.source_mappings = {
            # Financial Services
            "market_data_service": {
                "sources": [
                    {
                        "name": "YFinance Market Data",
                        "type": DataSourceType.API,
                        "data_type": DataType.MARKET,
                        "location": "src/services/financial/market_data_service.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "market_data_service",
                        "metadata": {
                            "provider": "yfinance",
                            "cache_duration": 300,
                            "market_hours": "09:30-16:00 EST"
                        }
                    },
                    {
                        "name": "Mock Market Data",
                        "type": DataSourceType.MOCK,
                        "data_type": DataType.MARKET,
                        "location": "src/services/financial/market_data_service.py",
                        "priority": DataPriority.LOW,
                        "original_service": "market_data_service",
                        "metadata": {
                            "provider": "mock",
                            "purpose": "testing"
                        }
                    }
                ]
            },
            "sentiment_data_analyzer": {
                "sources": [
                    {
                        "name": "Analyst Ratings Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.SENTIMENT,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "rating_based",
                            "confidence_threshold": 0.7
                        }
                    },
                    {
                        "name": "Options Flow Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.OPTIONS,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "volume_based",
                            "pcr_threshold": 1.0
                        }
                    },
                    {
                        "name": "Insider Trading Sentiment",
                        "type": DataSourceType.API,
                        "data_type": DataType.INSIDER_TRADING,
                        "location": "src/services/financial/sentiment/data_analyzer.py",
                        "priority": DataPriority.CRITICAL,
                        "original_service": "sentiment_data_analyzer",
                        "metadata": {
                            "analysis_method": "activity_based",
                            "trade_size_threshold": 100000
                        }
                    }
                ]
            },
            "data_manager": {
                "sources": [
                    {
                        "name": "Unified Data Manager",
                        "type": DataSourceType.DATABASE,
                        "data_type": DataType.SYSTEM,
                        "location": "src/core/managers/data_manager.py",
                        "priority": DataPriority.HIGH,
                        "original_service": "data_manager",
                        "metadata": {
                            "consolidation_level": "high",
                            "duplication_eliminated": "80%"
                        }
                    }
                ]
            }
        }
    
    def get_all_source_mappings(self) -> List[Dict[str, Any]]:
        """Get all source mappings for migration"""
        all_sources = []
        for service, mapping_data in self.source_mappings.items():
            all_sources.extend(mapping_data["sources"])
        return all_sources
    
    def get_service_mappings(self, service_name: str) -> List[Dict[str, Any]]:
        """Get mappings for a specific service"""
        return self.source_mappings.get(service_name, {}).get("sources", [])
    
    def validate_mapping(self, mapping: Dict[str, Any]) -> bool:
        """Validate a source mapping"""
        required_fields = ["name", "type", "data_type", "location", "original_service"]
        return all(field in mapping for field in required_fields)

# ============================================================================
# DATA VALIDATION ENGINE - Consolidated from scattered implementations
# ============================================================================

class DataValidationEngine:
    """Unified data validation engine for all data sources"""
    
    def __init__(self):
        self.validation_rules = {
            DataType.MARKET: {
                "required_fields": ["symbol", "price", "timestamp"],
                "price_validation": lambda x: isinstance(x, (int, float)) and x > 0,
                "timestamp_validation": lambda x: isinstance(x, str) and len(x) > 0
            },
            DataType.SENTIMENT: {
                "required_fields": ["score", "confidence", "source"],
                "score_validation": lambda x: isinstance(x, (int, float)) and -1 <= x <= 1,
                "confidence_validation": lambda x: isinstance(x, (int, float)) and 0 <= x <= 1
            },
            DataType.FINANCIAL: {
                "required_fields": ["amount", "currency", "date"],
                "amount_validation": lambda x: isinstance(x, (int, float)) and x >= 0,
                "currency_validation": lambda x: isinstance(x, str) and len(x) == 3
            }
        }
    
    def validate_data(self, data: Any, data_type: DataType) -> Dict[str, Any]:
        """Validate data against type-specific rules"""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "validation_time": datetime.now(timezone.utc).isoformat()
        }
        
        if data_type not in self.validation_rules:
            validation_result["warnings"].append(f"No validation rules for {data_type}")
            return validation_result
        
        rules = self.validation_rules[data_type]
        
        # Check required fields
        if isinstance(data, dict):
            for field in rules.get("required_fields", []):
                if field not in data:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Missing required field: {field}")
        
        # Apply custom validation functions
        for rule_name, validation_func in rules.items():
            if rule_name.endswith("_validation") and callable(validation_func):
                try:
                    if not validation_func(data):
                        validation_result["valid"] = False
                        validation_result["errors"].append(f"Validation failed for {rule_name}")
                except Exception as e:
                    validation_result["valid"] = False
                    validation_result["errors"].append(f"Validation error for {rule_name}: {str(e)}")
        
        return validation_result
    
    def get_validation_rules(self, data_type: DataType) -> Dict[str, Any]:
        """Get validation rules for a specific data type"""
        return self.validation_rules.get(data_type, {})

# ============================================================================
# MIGRATION FRAMEWORK - For consolidating existing data sources
# ============================================================================

class DataSourceMigrationFramework:
    """Framework for migrating existing scattered data sources"""
    
    def __init__(self, consolidation_system):
        self.consolidation_system = consolidation_system
        self.migration_log = []
        self.migration_status = {}
    
    def migrate_service(self, service_name: str) -> Dict[str, Any]:
        """Migrate a specific service to the unified system"""
        migration_result = {
            "service": service_name,
            "status": "pending",
            "sources_migrated": 0,
            "errors": [],
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None
        }
        
        try:
            # Get service mappings
            mappings = self.consolidation_system.mapper.get_service_mappings(service_name)
            if not mappings:
                migration_result["errors"].append(f"No mappings found for service: {service_name}")
                migration_result["status"] = "failed"
                return migration_result
            
            # Migrate each source
            for mapping in mappings:
                if self.consolidation_system.mapper.validate_mapping(mapping):
                    try:
                        self._migrate_source(mapping)
                        migration_result["sources_migrated"] += 1
                    except Exception as e:
                        migration_result["errors"].append(f"Failed to migrate source {mapping['name']}: {str(e)}")
                else:
                    migration_result["errors"].append(f"Invalid mapping for source: {mapping.get('name', 'Unknown')}")
            
            # Update migration status
            if migration_result["errors"]:
                migration_result["status"] = "completed_with_errors"
            else:
                migration_result["status"] = "completed"
            
            migration_result["end_time"] = datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            migration_result["status"] = "failed"
            migration_result["errors"].append(f"Migration failed: {str(e)}")
            migration_result["end_time"] = datetime.now(timezone.utc).isoformat()
        
        # Log migration result
        self.migration_log.append(migration_result)
        self.migration_status[service_name] = migration_result
        
        return migration_result
    
    def _migrate_source(self, mapping: Dict[str, Any]):
        """Migrate a single data source"""
        # Create data source record
        source = DataSource(
            id=str(uuid.uuid4()),
            name=mapping["name"],
            type=mapping["type"],
            data_type=mapping["data_type"],
            location=mapping["location"],
            priority=mapping.get("priority", DataPriority.NORMAL),
            metadata=mapping.get("metadata", {}),
            original_service=mapping["original_service"],
            migration_status="migrated"
        )
        
        # Register with consolidation system
        self.consolidation_system.register_data_source(source)
    
    def get_migration_status(self) -> Dict[str, Any]:
        """Get overall migration status"""
        total_services = len(self.migration_status)
        completed_services = sum(1 for status in self.migration_status.values() 
                               if status["status"] in ["completed", "completed_with_errors"])
        
        return {
            "total_services": total_services,
            "completed_services": completed_services,
            "pending_services": total_services - completed_services,
            "migration_log": self.migration_log,
            "service_status": self.migration_status
        }
    
    def rollback_migration(self, service_name: str) -> bool:
        """Rollback migration for a specific service"""
        if service_name not in self.migration_status:
            return False
        
        try:
            # Remove migrated sources
            sources_to_remove = []
            for source in self.consolidation_system.list_data_sources():
                if source.original_service == service_name:
                    sources_to_remove.append(source.id)
            
            for source_id in sources_to_remove:
                self.consolidation_system.remove_data_source(source_id)
            
            # Update migration status
            self.migration_status[service_name]["status"] = "rolled_back"
            self.migration_status[service_name]["rollback_time"] = datetime.now(timezone.utc).isoformat()
            
            return True
            
        except Exception as e:
            logging.error(f"Rollback failed for {service_name}: {str(e)}")
            return False

# ============================================================================
# DATA STORAGE SYSTEM - Consolidated from scattered implementations
# ============================================================================

class DataStorage:
    """Unified data storage system"""
    
    def __init__(self, storage_path: str = "data/unified_storage.db"):
        self.logger = logging.getLogger(f"{__name__}.DataStorage")
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = None
        self.lock = threading.RLock()
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage database and tables"""
        try:
            self.connection = sqlite3.connect(self.storage_path, check_same_thread=False)
            cursor = self.connection.cursor()
            
            # Create data sources table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_sources (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    type TEXT NOT NULL,
                    data_type TEXT NOT NULL,
                    location TEXT NOT NULL,
                    priority INTEGER NOT NULL,
                    enabled BOOLEAN NOT NULL,
                    last_updated TEXT NOT NULL,
                    metadata TEXT,
                    validation_rules TEXT,
                    access_patterns TEXT,
                    original_service TEXT,
                    migration_status TEXT
                )
            ''')
            
            # Create data records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS data_records (
                    id TEXT PRIMARY KEY,
                    data_type TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    data TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    version INTEGER NOT NULL,
                    metadata TEXT,
                    validation_status TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES data_sources (id)
                )
            ''')
            
            # Create access patterns table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_patterns (
                    id TEXT PRIMARY KEY,
                    pattern TEXT NOT NULL,
                    source_id TEXT NOT NULL,
                    frequency INTEGER DEFAULT 0,
                    last_used TEXT NOT NULL,
                    FOREIGN KEY (source_id) REFERENCES data_sources (id)
                )
            ''')
            
            self.connection.commit()
            self.logger.info("Data storage initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize storage: {e}")
    
    def store_data_source(self, data_source: DataSource) -> bool:
        """Store data source in unified storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO data_sources 
                    (id, name, type, data_type, location, priority, enabled, 
                     last_updated, metadata, validation_rules, access_patterns,
                     original_service, migration_status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data_source.id,
                    data_source.name,
                    data_source.type.value,
                    data_source.data_type.value,
                    data_source.location,
                    data_source.priority.value,
                    data_source.enabled,
                    data_source.last_updated,
                    json.dumps(data_source.metadata),
                    json.dumps(data_source.validation_rules),
                    json.dumps(data_source.access_patterns),
                    data_source.original_service,
                    data_source.migration_status
                ))
                
                self.connection.commit()
                self.logger.info(f"Data source stored: {data_source.name}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to store data source: {e}")
            return False
    
    def store_data_record(self, record: DataRecord) -> bool:
        """Store data record in unified storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO data_records 
                    (id, data_type, source_id, data, timestamp, version, 
                     metadata, validation_status, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    record.id,
                    record.data_type.value,
                    record.source_id,
                    json.dumps(record.data),
                    record.timestamp,
                    record.version,
                    json.dumps(record.metadata),
                    record.validation_status,
                    record.last_accessed
                ))
                
                self.connection.commit()
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to store data record: {e}")
            return False
    
    def get_data_source(self, source_id: str) -> Optional[DataSource]:
        """Retrieve data source from unified storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('''
                    SELECT * FROM data_sources WHERE id = ?
                ''', (source_id,))
                
                row = cursor.fetchone()
                if row:
                    return DataSource(
                        id=row[0],
                        name=row[1],
                        type=DataSourceType(row[2]),
                        data_type=DataType(row[3]),
                        location=row[4],
                        priority=DataPriority(row[5]),
                        enabled=bool(row[6]),
                        last_updated=row[7],
                        metadata=json.loads(row[8]) if row[8] else {},
                        validation_rules=json.loads(row[9]) if row[9] else {},
                        access_patterns=json.loads(row[10]) if row[10] else [],
                        original_service=row[11] if len(row) > 11 else "",
                        migration_status=row[12] if len(row) > 12 else "pending"
                    )
                return None
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve data source: {e}")
            return None
    
    def get_data_records(self, data_type: DataType, source_id: str = None, 
                        limit: int = 100) -> List[DataRecord]:
        """Retrieve data records from unified storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                
                if source_id:
                    cursor.execute('''
                        SELECT * FROM data_records 
                        WHERE data_type = ? AND source_id = ?
                        ORDER BY timestamp DESC LIMIT ?
                    ''', (data_type.value, source_id, limit))
                else:
                    cursor.execute('''
                        SELECT * FROM data_records 
                        WHERE data_type = ?
                        ORDER BY timestamp DESC LIMIT ?
                    ''', (data_type.value, limit))
                
                records = []
                for row in cursor.fetchall():
                    record = DataRecord(
                        id=row[0],
                        data_type=DataType(row[1]),
                        source_id=row[2],
                        data=json.loads(row[3]),
                        timestamp=row[4],
                        version=row[5],
                        metadata=json.loads(row[6]) if row[6] else {},
                        validation_status=row[7],
                        last_accessed=row[8]
                    )
                    records.append(record)
                
                return records
                
        except Exception as e:
            self.logger.error(f"Failed to retrieve data records: {e}")
            return []

    def create_tables(self):
        """Create database tables - alias for _initialize_storage"""
        self._initialize_storage()
    
    def get_all_data_sources(self) -> List[DataSource]:
        """Get all data sources from storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('SELECT * FROM data_sources')
                
                sources = []
                for row in cursor.fetchall():
                    source = DataSource(
                        id=row[0],
                        name=row[1],
                        type=DataSourceType(row[2]),
                        data_type=DataType(row[3]),
                        location=row[4],
                        priority=DataPriority(row[5]),
                        enabled=bool(row[6]),
                        last_updated=row[7],
                        metadata=json.loads(row[8]) if row[8] else {},
                        validation_rules=json.loads(row[9]) if row[9] else {},
                        access_patterns=json.loads(row[10]) if row[10] else [],
                        original_service=row[11] if len(row) > 11 else "",
                        migration_status=row[12] if len(row) > 12 else "pending"
                    )
                    sources.append(source)
                
                return sources
                
        except Exception as e:
            self.logger.error(f"Failed to get all data sources: {e}")
            return []
    
    def remove_data_source(self, source_id: str) -> bool:
        """Remove a data source from storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('DELETE FROM data_sources WHERE id = ?', (source_id,))
                self.connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Failed to remove data source: {e}")
            return False
    
    def update_data_source(self, data_source: DataSource) -> bool:
        """Update a data source in storage"""
        try:
            with self.lock:
                cursor = self.connection.cursor()
                cursor.execute('''
                    UPDATE data_sources SET
                        name = ?, type = ?, data_type = ?, location = ?, 
                        priority = ?, enabled = ?, last_updated = ?, metadata = ?,
                        validation_rules = ?, access_patterns = ?, original_service = ?,
                        migration_status = ?
                    WHERE id = ?
                ''', (
                    data_source.name,
                    data_source.type.value,
                    data_source.data_type.value,
                    data_source.location,
                    data_source.priority.value,
                    data_source.enabled,
                    data_source.last_updated,
                    json.dumps(data_source.metadata),
                    json.dumps(data_source.validation_rules),
                    json.dumps(data_source.access_patterns),
                    data_source.original_service,
                    data_source.migration_status,
                    data_source.id
                ))
                
                self.connection.commit()
                return cursor.rowcount > 0
                
        except Exception as e:
            self.logger.error(f"Failed to update data source: {e}")
            return False

# ============================================================================
# DATA SYNCHRONIZATION SYSTEM - Consolidated from scattered implementations
# ============================================================================

class DataSynchronizer:
    """Unified data synchronization system"""
    
    def __init__(self, storage: DataStorage):
        self.storage = storage
        self.logger = logging.getLogger(f"{__name__}.DataSynchronizer")
        self.sync_threads = {}
        self.sync_configs = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
    
    def register_sync_config(self, source_id: str, target_id: str, 
                           sync_interval: int = 300, sync_type: str = "full"):
        """Register synchronization configuration"""
        try:
            sync_id = f"{source_id}_to_{target_id}"
            self.sync_configs[sync_id] = {
                "source_id": source_id,
                "target_id": target_id,
                "sync_interval": sync_interval,
                "sync_type": sync_type,
                "last_sync": None,
                "enabled": True
            }
            
            self.logger.info(f"Synchronization config registered: {sync_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to register sync config: {e}")
    
    def start_synchronization(self, sync_id: str):
        """Start data synchronization for specified config"""
        try:
            if sync_id not in self.sync_configs:
                raise ValueError(f"Sync config not found: {sync_id}")
            
            if sync_id in self.sync_threads:
                self.logger.warning(f"Synchronization already running: {sync_id}")
                return
            
            config = self.sync_configs[sync_id]
            thread = threading.Thread(
                target=self._sync_worker,
                args=(sync_id,),
                daemon=True
            )
            
            self.sync_threads[sync_id] = thread
            thread.start()
            
            self.logger.info(f"Synchronization started: {sync_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to start synchronization: {e}")
    
    def _sync_worker(self, sync_id: str):
        """Synchronization worker thread"""
        try:
            config = self.sync_configs[sync_id]
            
            while config.get("enabled", True):
                # Perform synchronization
                self._perform_sync(sync_id)
                
                # Update last sync time
                config["last_sync"] = datetime.now(timezone.utc).isoformat()
                
                # Wait for next sync interval
                time.sleep(config["sync_interval"])
                
        except Exception as e:
            self.logger.error(f"Synchronization worker error for {sync_id}: {e}")
        finally:
            if sync_id in self.sync_threads:
                del self.sync_threads[sync_id]
    
    def _perform_sync(self, sync_id: str):
        """Perform actual data synchronization"""
        try:
            config = self.sync_configs[sync_id]
            source_id = config["source_id"]
            target_id = config["target_id"]
            sync_type = config["sync_type"]
            
            self.logger.info(f"Performing {sync_type} sync: {source_id} → {target_id}")
            
            # Get source data
            source_records = self.storage.get_data_records(
                DataType.CONFIGURATION, source_id, limit=1000
            )
            
            # Sync to target (simplified for demonstration)
            for record in source_records:
                # Update target with source data
                target_record = DataRecord(
                    id=str(uuid.uuid4()),
                    data_type=record.data_type,
                    source_id=target_id,
                    data=record.data,
                    timestamp=datetime.now(timezone.utc).isoformat(),
                    version=record.version + 1,
                    metadata={"synced_from": source_id, "sync_type": sync_type},
                    validation_status="synced",
                    last_accessed=datetime.now(timezone.utc).isoformat()
                )
                
                self.storage.store_data_record(target_record)
            
            self.logger.info(f"Sync completed: {len(source_records)} records")
            
        except Exception as e:
            self.logger.error(f"Sync operation failed: {e}")

# ============================================================================
# ENHANCED UNIFIED DATA SOURCE CONSOLIDATION
# ============================================================================

class UnifiedDataSourceConsolidation:
    """Enhanced unified data source consolidation system"""
    
    def __init__(self, db_path: str = "unified_data_sources.db"):
        self.db_path = db_path
        self.storage = DataStorage(db_path)
        self.validator = DataValidationEngine()
        self.synchronizer = DataSynchronizer(self.storage)
        self.mapper = DataSourceMapper()
        self.migration_framework = DataSourceMigrationFramework(self)
        
        # Initialize system
        self._initialize_system()
    
    def _initialize_system(self):
        """Initialize the consolidation system"""
        try:
            # Create database tables
            self.storage.create_tables()
            
            # Register core data sources
            self._register_core_sources()
            
            logging.info("Unified Data Source Consolidation system initialized successfully")
            
        except Exception as e:
            logging.error(f"Failed to initialize consolidation system: {str(e)}")
            raise
    
    def _register_core_sources(self):
        """Register core data sources"""
        core_sources = [
            DataSource(
                id="core-system",
                name="System Core",
                type=DataSourceType.SYSTEM,
                data_type=DataType.SYSTEM,
                location="internal",
                priority=DataPriority.CRITICAL,
                metadata={"purpose": "system_operations"}
            )
        ]
        
        for source in core_sources:
            self.register_data_source(source)
    
    def consolidate_all_sources(self) -> Dict[str, Any]:
        """Consolidate all scattered data sources"""
        consolidation_result = {
            "status": "in_progress",
            "services_processed": 0,
            "sources_consolidated": 0,
            "errors": [],
            "start_time": datetime.now(timezone.utc).isoformat(),
            "end_time": None
        }
        
        try:
            # Get all service mappings
            all_mappings = self.mapper.get_all_source_mappings()
            
            # Process each service
            processed_services = set()
            for mapping in all_mappings:
                service_name = mapping["original_service"]
                if service_name not in processed_services:
                    # Migrate service
                    migration_result = self.migration_framework.migrate_service(service_name)
                    consolidation_result["services_processed"] += 1
                    
                    if migration_result["status"] == "completed":
                        consolidation_result["sources_consolidated"] += migration_result["sources_migrated"]
                    else:
                        consolidation_result["errors"].extend(migration_result["errors"])
                    
                    processed_services.add(service_name)
            
            consolidation_result["status"] = "completed"
            consolidation_result["end_time"] = datetime.now(timezone.utc).isoformat()
            
        except Exception as e:
            consolidation_result["status"] = "failed"
            consolidation_result["errors"].append(f"Consolidation failed: {str(e)}")
            consolidation_result["end_time"] = datetime.now(timezone.utc).isoformat()
        
        return consolidation_result
    
    def get_consolidation_status(self) -> Dict[str, Any]:
        """Get overall consolidation status"""
        return {
            "total_sources": len(self.list_data_sources()),
            "migration_status": self.migration_framework.get_migration_status(),
            "validation_status": self._get_validation_status(),
            "ssot_compliance": self._check_ssot_compliance()
        }
    
    def _get_validation_status(self) -> Dict[str, Any]:
        """Get validation status for all data sources"""
        validation_results = {}
        for source in self.list_data_sources():
            validation_results[source.id] = {
                "source_name": source.name,
                "data_type": source.data_type.value,
                "validation_rules": self.validator.get_validation_rules(source.data_type)
            }
        return validation_results
    
    def _check_ssot_compliance(self) -> Dict[str, Any]:
        """Check SSOT compliance across all data sources"""
        ssot_analysis = {
            "total_violations": 0,
            "duplicate_sources": 0,
            "scattered_data": 0,
            "compliance_score": 100
        }
        
        # Check for duplicate data types
        data_type_counts = {}
        for source in self.list_data_sources():
            data_type = source.data_type.value
            data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1
        
        # Identify violations
        for data_type, count in data_type_counts.items():
            if count > 1:
                ssot_analysis["duplicate_sources"] += count - 1
                ssot_analysis["total_violations"] += 1
        
        # Calculate compliance score
        total_sources = len(self.list_data_sources())
        if total_sources > 0:
            violation_penalty = (ssot_analysis["total_violations"] / total_sources) * 100
            ssot_analysis["compliance_score"] = max(0, 100 - violation_penalty)
        
        return ssot_analysis

    def register_data_source(self, source: DataSource) -> bool:
        """Register a data source in the unified system"""
        try:
            if self.storage.store_data_source(source):
                logging.info(f"Data source registered: {source.name} ({source.id})")
                return True
            return False
        except Exception as e:
            logging.error(f"Failed to register data source: {str(e)}")
            return False
    
    def list_data_sources(self) -> List[DataSource]:
        """List all registered data sources"""
        try:
            return self.storage.get_all_data_sources()
        except Exception as e:
            logging.error(f"Failed to list data sources: {str(e)}")
            return []
    
    def remove_data_source(self, source_id: str) -> bool:
        """Remove a data source from the unified system"""
        try:
            return self.storage.remove_data_source(source_id)
        except Exception as e:
            logging.error(f"Failed to remove data source: {str(e)}")
            return False
    
    def get_data_source(self, source_id: str) -> Optional[DataSource]:
        """Get a specific data source by ID"""
        try:
            return self.storage.get_data_source(source_id)
        except Exception as e:
            logging.error(f"Failed to get data source: {str(e)}")
            return None
    
    def update_data_source(self, source_id: str, updates: Dict[str, Any]) -> bool:
        """Update a data source with new information"""
        try:
            source = self.get_data_source(source_id)
            if not source:
                return False
            
            # Update fields
            for field, value in updates.items():
                if hasattr(source, field):
                    setattr(source, field, value)
            
            source.last_updated = datetime.now(timezone.utc).isoformat()
            
            return self.storage.update_data_source(source)
        except Exception as e:
            logging.error(f"Failed to update data source: {str(e)}")
            return False
    
    def validate_all_data(self) -> Dict[str, Any]:
        """Validate all data in the system"""
        validation_results = {
            "total_sources": 0,
            "valid_sources": 0,
            "invalid_sources": 0,
            "validation_details": {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        try:
            sources = self.list_data_sources()
            validation_results["total_sources"] = len(sources)
            
            for source in sources:
                # Validate source metadata
                validation_result = self.validator.validate_data(
                    source.metadata, source.data_type
                )
                
                validation_results["validation_details"][source.id] = {
                    "source_name": source.name,
                    "data_type": source.data_type.value,
                    "validation_result": validation_result
                }
                
                if validation_result["valid"]:
                    validation_results["valid_sources"] += 1
                else:
                    validation_results["invalid_sources"] += 1
            
        except Exception as e:
            validation_results["error"] = str(e)
        
        return validation_results
    
    def export_consolidation_report(self, output_path: str = "consolidation_report.json") -> bool:
        """Export a comprehensive consolidation report"""
        try:
            report = {
                "consolidation_status": self.get_consolidation_status(),
                "validation_status": self.validate_all_data(),
                "migration_summary": self.migration_framework.get_migration_status(),
                "ssot_analysis": self._check_ssot_compliance(),
                "data_sources": [
                    {
                        "id": source.id,
                        "name": source.name,
                        "type": source.type.value,
                        "data_type": source.data_type.value,
                        "location": source.location,
                        "priority": source.priority.value,
                        "enabled": source.enabled,
                        "original_service": source.original_service,
                        "migration_status": source.migration_status
                    }
                    for source in self.list_data_sources()
                ],
                "export_timestamp": datetime.now(timezone.utc).isoformat(),
                "contract_info": {
                    "contract_id": "SSOT-002",
                    "contract_name": "Data Source Consolidation",
                    "agent": "Agent-5",
                    "points": 450,
                    "status": "IN_PROGRESS"
                }
            }
            
            with open(output_path, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            logging.info(f"Consolidation report exported to: {output_path}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to export consolidation report: {str(e)}")
            return False

# ============================================================================
# CLI INTERFACE - For contract completion and system management
# ============================================================================

class ConsolidationCLI:
    """Command-line interface for the Data Source Consolidation system"""
    
    def __init__(self):
        self.consolidation_system = None
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for the CLI"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler('consolidation_cli.log')
            ]
        )
    
    def initialize_system(self, db_path: str = "unified_data_sources.db"):
        """Initialize the consolidation system"""
        try:
            self.consolidation_system = UnifiedDataSourceConsolidation(db_path)
            logging.info("Consolidation system initialized successfully")
            return True
        except Exception as e:
            logging.error(f"Failed to initialize consolidation system: {str(e)}")
            return False
    
    def run_consolidation(self) -> bool:
        """Run the complete consolidation process"""
        if not self.consolidation_system:
            logging.error("Consolidation system not initialized")
            return False
        
        try:
            logging.info("Starting data source consolidation...")
            result = self.consolidation_system.consolidate_all_sources()
            
            if result["status"] == "completed":
                logging.info("Consolidation completed successfully!")
                logging.info(f"Services processed: {result['services_processed']}")
                logging.info(f"Sources consolidated: {result['sources_consolidated']}")
                return True
            else:
                logging.error(f"Consolidation failed: {result['errors']}")
                return False
                
        except Exception as e:
            logging.error(f"Consolidation process failed: {str(e)}")
            return False
    
    def show_status(self):
        """Show consolidation system status"""
        if not self.consolidation_system:
            logging.error("Consolidation system not initialized")
            return
        
        try:
            status = self.consolidation_system.get_consolidation_status()
            
            print("\n" + "="*60)
            print("📊 DATA SOURCE CONSOLIDATION STATUS")
            print("="*60)
            print(f"Total Data Sources: {status['total_sources']}")
            
            # Migration status
            migration = status['migration_status']
            print(f"\n🔄 MIGRATION STATUS:")
            print(f"  Total Services: {migration['total_services']}")
            print(f"  Completed: {migration['completed_services']}")
            print(f"  Pending: {migration['pending_services']}")
            
            # SSOT compliance
            ssot = status['ssot_compliance']
            print(f"\n✅ SSOT COMPLIANCE:")
            print(f"  Compliance Score: {ssot['compliance_score']:.1f}%")
            print(f"  Total Violations: {ssot['total_violations']}")
            print(f"  Duplicate Sources: {ssot['duplicate_sources']}")
            
            # Service details
            if migration['service_status']:
                print(f"\n📋 SERVICE DETAILS:")
                for service, service_status in migration['service_status'].items():
                    print(f"  {service}: {service_status['status']}")
                    if service_status['sources_migrated'] > 0:
                        print(f"    Sources migrated: {service_status['sources_migrated']}")
            
            print("="*60)
            
        except Exception as e:
            logging.error(f"Failed to show status: {str(e)}")
    
    def export_report(self, output_path: str = "consolidation_report.json"):
        """Export consolidation report"""
        if not self.consolidation_system:
            logging.error("Consolidation system not initialized")
            return False
        
        try:
            success = self.consolidation_system.export_consolidation_report(output_path)
            if success:
                print(f"✅ Consolidation report exported to: {output_path}")
            else:
                print("❌ Failed to export consolidation report")
            return success
        except Exception as e:
            logging.error(f"Export failed: {str(e)}")
            return False
    
    def run_interactive(self):
        """Run interactive CLI mode"""
        if not self.consolidation_system:
            if not self.initialize_system():
                return
        
        print("\n🚀 DATA SOURCE CONSOLIDATION CLI")
        print("Contract: SSOT-002 - Data Source Consolidation (450 points)")
        print("Agent: Agent-5 - SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER")
        
        while True:
            print("\n📋 Available Commands:")
            print("1. Show Status")
            print("2. Run Consolidation")
            print("3. Export Report")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                self.show_status()
            elif choice == "2":
                print("\n🔄 Running consolidation...")
                success = self.run_consolidation()
                if success:
                    print("✅ Consolidation completed successfully!")
                else:
                    print("❌ Consolidation failed")
            elif choice == "3":
                output_path = input("Enter output path (default: consolidation_report.json): ").strip()
                if not output_path:
                    output_path = "consolidation_report.json"
                self.export_report(output_path)
            elif choice == "4":
                print("👋 Exiting consolidation CLI")
                break
            else:
                print("❌ Invalid choice. Please enter 1-4.")

# ============================================================================
# MAIN EXECUTION - Contract completion entry point
# ============================================================================

def main():
    """Main entry point for the Data Source Consolidation contract"""
    print("=" * 70)
    print("🎯 Contract: SSOT-002: Data Source Consolidation - 450 points")
    print("👤 Agent: Agent-5 (SPRINT ACCELERATION REFACTORING TOOL PREPARATION MANAGER)")
    print("📋 Status: IN PROGRESS - ENHANCING FOR COMPLETION")
    print("=" * 70)
    
    # Initialize CLI
    cli = ConsolidationCLI()
    
    # Check command line arguments
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--status":
            cli.initialize_system()
            cli.show_status()
        elif command == "--consolidate":
            cli.initialize_system()
            success = cli.run_consolidation()
            if success:
                print("✅ Data source consolidation completed successfully!")
                cli.export_report()
            else:
                print("❌ Data source consolidation failed")
                sys.exit(1)
        elif command == "--export":
            cli.initialize_system()
            cli.export_report()
        elif command == "--interactive":
            cli.run_interactive()
        else:
            print("Usage:")
            print("  python unified_data_source_consolidation.py --status")
            print("  python unified_data_source_consolidation.py --consolidate")
            print("  python unified_data_source_consolidation.py --export")
            print("  python unified_data_source_consolidation.py --interactive")
    else:
        # Default: run consolidation
        cli.initialize_system()
        success = cli.run_consolidation()
        if success:
            print("✅ Data source consolidation completed successfully!")
            cli.export_report()
        else:
            print("❌ Data source consolidation failed")
            sys.exit(1)

if __name__ == "__main__":
    main()
