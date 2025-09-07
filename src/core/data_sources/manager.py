#!/usr/bin/env python3
"""
Data Source Manager - Core consolidation logic
=============================================

Manages the consolidation of data sources into a unified system.
"""

import json
import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from .types import DataSourceType, DataType, DataPriority
from .models import DataSource, DataRecord, DataSourceMapping, DataConsolidationReport


class UnifiedDataSourceManager:
    """Manages unified data source consolidation"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "data_sources_config.json"
        self.sources: Dict[str, DataSource] = {}
        self.mappings: List[DataSourceMapping] = []
        self.logger = logging.getLogger(__name__)
        
    def add_source(self, source: DataSource) -> bool:
        """Add a new data source"""
        try:
            if source.id in self.sources:
                self.logger.warning(f"Source {source.id} already exists")
                return False
                
            self.sources[source.id] = source
            self.logger.info(f"Added source: {source.name} ({source.id})")
            return True
        except Exception as e:
            self.logger.error(f"Error adding source: {e}")
            return False
    
    def remove_source(self, source_id: str) -> bool:
        """Remove a data source"""
        try:
            if source_id not in self.sources:
                return False
                
            del self.sources[source_id]
            self.logger.info(f"Removed source: {source_id}")
            return True
        except Exception as e:
            self.logger.error(f"Error removing source: {e}")
            return False
    
    def get_source(self, source_id: str) -> Optional[DataSource]:
        """Get a data source by ID"""
        return self.sources.get(source_id)
    
    def list_sources(self, source_type: Optional[DataSourceType] = None) -> List[DataSource]:
        """List all sources, optionally filtered by type"""
        if source_type is None:
            return list(self.sources.values())
        return [s for s in self.sources.values() if s.type == source_type]
    
    def consolidate_sources(self, target_source: DataSource, 
                          sources_to_consolidate: List[str]) -> bool:
        """Consolidate multiple sources into one"""
        try:
            # Create mapping for each source being consolidated
            for source_id in sources_to_consolidate:
                if source_id in self.sources:
                    mapping = DataSourceMapping(
                        old_source=source_id,
                        new_source=target_source.id,
                        migration_path=f"{source_id} -> {target_source.id}",
                        status="migrating"
                    )
                    self.mappings.append(mapping)
                    
                    # Mark old source for removal
                    self.sources[source_id].enabled = False
                    
            self.logger.info(f"Consolidated {len(sources_to_consolidate)} sources into {target_source.id}")
            return True
        except Exception as e:
            self.logger.error(f"Error consolidating sources: {e}")
            return False
    
    def generate_report(self) -> DataConsolidationReport:
        """Generate consolidation report"""
        total = len(self.sources)
        consolidated = len([s for s in self.sources.values() if not s.enabled])
        remaining = total - consolidated
        progress = (consolidated / total * 100) if total > 0 else 0
        
        return DataConsolidationReport(
            total_sources=total,
            consolidated_sources=consolidated,
            remaining_sources=remaining,
            migration_progress=progress
        )
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config = {
                "sources": {k: self._source_to_dict(v) for k, v in self.sources.items()},
                "mappings": [self._mapping_to_dict(m) for m in self.mappings],
                "last_updated": datetime.now().isoformat()
            }
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
                
            return True
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            return False
    
    def _source_to_dict(self, source: DataSource) -> Dict[str, Any]:
        """Convert DataSource to dictionary"""
        return {
            "id": source.id,
            "name": source.name,
            "type": source.type.value,
            "data_type": source.data_type.value,
            "location": source.location,
            "priority": source.priority.value,
            "enabled": source.enabled,
            "last_updated": source.last_updated,
            "metadata": source.metadata,
            "validation_rules": source.validation_rules,
            "access_patterns": source.access_patterns,
            "original_service": source.original_service,
            "migration_status": source.migration_status
        }
    
    def _mapping_to_dict(self, mapping: DataSourceMapping) -> Dict[str, Any]:
        """Convert DataSourceMapping to dictionary"""
        return {
            "old_source": mapping.old_source,
            "new_source": mapping.new_source,
            "migration_path": mapping.migration_path,
            "status": mapping.status,
            "created_at": mapping.created_at.isoformat(),
            "completed_at": mapping.completed_at.isoformat() if mapping.completed_at else None
        }
