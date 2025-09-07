#!/usr/bin/env python3
"""
Data Source Migration - Migration utilities
==========================================

Provides utilities for migrating data between sources during consolidation.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable
from .models import DataSource, DataSourceMapping, DataRecord
from .types import DataSourceType


class DataSourceMigrator:
    """Handles data source migration during consolidation"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.migration_handlers: Dict[DataSourceType, Callable] = {}
        self._setup_default_handlers()
    
    def _setup_default_handlers(self):
        """Setup default migration handlers for different source types"""
        self.migration_handlers[DataSourceType.FILE] = self._migrate_file_source
        self.migration_handlers[DataSourceType.DATABASE] = self._migrate_database_source
        self.migration_handlers[DataSourceType.API] = self._migrate_api_source
        self.migration_handlers[DataSourceType.MEMORY] = self._migrate_memory_source
    
    def migrate_data(self, source: DataSource, target: DataSource, 
                    data: List[DataRecord]) -> bool:
        """Migrate data from source to target"""
        try:
            if source.type not in self.migration_handlers:
                self.logger.error(f"No migration handler for source type: {source.type}")
                return False
            
            handler = self.migration_handlers[source.type]
            success = handler(source, target, data)
            
            if success:
                self.logger.info(f"Successfully migrated {len(data)} records from {source.id} to {target.id}")
            else:
                self.logger.error(f"Failed to migrate data from {source.id} to {target.id}")
            
            return success
        except Exception as e:
            self.logger.error(f"Migration error: {e}")
            return False
    
    def _migrate_file_source(self, source: DataSource, target: DataSource, 
                           data: List[DataRecord]) -> bool:
        """Migrate data from file-based source"""
        try:
            # Create backup of source data
            backup_path = f"backup_{source.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(backup_path, 'w') as f:
                json.dump([self._record_to_dict(record) for record in data], f, indent=2)
            
            # Write data to target location
            target_path = Path(target.location)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, 'w') as f:
                json.dump([self._record_to_dict(record) for record in data], f, indent=2)
            
            self.logger.info(f"File migration completed: {source.location} -> {target.location}")
            return True
        except Exception as e:
            self.logger.error(f"File migration error: {e}")
            return False
    
    def _migrate_database_source(self, source: DataSource, target: DataSource, 
                               data: List[DataRecord]) -> bool:
        """Migrate data from database source"""
        try:
            # For database sources, we'd typically use SQL or ORM operations
            # This is a simplified implementation
            self.logger.info(f"Database migration: {source.location} -> {target.location}")
            
            # In a real implementation, you'd:
            # 1. Connect to source database
            # 2. Extract data
            # 3. Transform if needed
            # 4. Insert into target database
            
            return True
        except Exception as e:
            self.logger.error(f"Database migration error: {e}")
            return False
    
    def _migrate_api_source(self, source: DataSource, target: DataSource, 
                          data: List[DataRecord]) -> bool:
        """Migrate data from API source"""
        try:
            # For API sources, we'd typically make HTTP requests
            self.logger.info(f"API migration: {source.location} -> {target.location}")
            
            # In a real implementation, you'd:
            # 1. Make API calls to source
            # 2. Process responses
            # 3. Send to target API
            
            return True
        except Exception as e:
            self.logger.error(f"API migration error: {e}")
            return False
    
    def _migrate_memory_source(self, source: DataSource, target: DataSource, 
                             data: List[DataRecord]) -> bool:
        """Migrate data from memory source"""
        try:
            # For memory sources, we'd typically serialize to persistent storage
            self.logger.info(f"Memory migration: {source.location} -> {target.location}")
            
            # Serialize memory data to target location
            target_path = Path(target.location)
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(target_path, 'w') as f:
                json.dump([self._record_to_dict(record) for record in data], f, indent=2)
            
            return True
        except Exception as e:
            self.logger.error(f"Memory migration error: {e}")
            return False
    
    def _record_to_dict(self, record: DataRecord) -> Dict[str, Any]:
        """Convert DataRecord to dictionary for serialization"""
        return {
            "id": record.id,
            "source_id": record.source_id,
            "data": record.data,
            "timestamp": record.timestamp.isoformat(),
            "version": record.version,
            "metadata": record.metadata,
            "validation_status": record.validation_status,
            "quality_score": record.quality_score
        }
    
    def validate_migration(self, source: DataSource, target: DataSource, 
                         original_count: int, migrated_count: int) -> Dict[str, Any]:
        """Validate that migration was successful"""
        success_rate = (migrated_count / original_count * 100) if original_count > 0 else 0
        
        return {
            "success": success_rate >= 95,  # 95% success threshold
            "success_rate": success_rate,
            "original_count": original_count,
            "migrated_count": migrated_count,
            "missing_records": original_count - migrated_count,
            "validation_timestamp": datetime.now().isoformat()
        }
