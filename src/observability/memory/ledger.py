"""
Memory Usage Ledger - V2_SWARM
==============================

Persistent ledger for tracking memory usage over time.
Provides historical analysis and trend detection.

Author: Agent-5 (Coordinator)
License: MIT
"""

import json
import logging
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class LedgerEntry:
    """Single ledger entry for memory usage"""
    
    timestamp: float
    service_name: str
    memory_usage_mb: float
    object_count: int
    allocation_count: int
    deallocation_count: int
    gc_collections: int
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


class MemoryLedger:
    """Memory usage ledger with persistence"""
    
    def __init__(self, storage_path: str = "logs/memory_ledger.json", 
                 max_entries: int = 10000):
        """Initialize memory ledger"""
        self.storage_path = Path(storage_path)
        self.max_entries = max_entries
        self.entries = []
        self._ensure_storage_directory()
    
    def _ensure_storage_directory(self) -> None:
        """Ensure storage directory exists"""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
    
    def add_entry(self, entry: LedgerEntry) -> None:
        """Add entry to ledger"""
        self.entries.append(entry)
        
        # Maintain entry limit
        if len(self.entries) > self.max_entries:
            self.entries.pop(0)
    
    def record(self, service_name: str, memory_mb: float, object_count: int,
               allocation_count: int = 0, deallocation_count: int = 0,
               gc_collections: int = 0) -> LedgerEntry:
        """Record new memory usage entry"""
        entry = LedgerEntry(
            timestamp=time.time(),
            service_name=service_name,
            memory_usage_mb=memory_mb,
            object_count=object_count,
            allocation_count=allocation_count,
            deallocation_count=deallocation_count,
            gc_collections=gc_collections
        )
        
        self.add_entry(entry)
        return entry
    
    def save(self) -> bool:
        """Save ledger to disk"""
        try:
            data = [entry.to_dict() for entry in self.entries]
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Ledger saved to {self.storage_path} ({len(self.entries)} entries)")
            return True
            
        except Exception as e:
            logger.error(f"Error saving ledger: {e}")
            return False
    
    def load(self) -> bool:
        """Load ledger from disk"""
        try:
            if not self.storage_path.exists():
                return True  # No ledger yet, that's OK
            
            with open(self.storage_path) as f:
                data = json.load(f)
            
            self.entries = [
                LedgerEntry(**entry) for entry in data
            ]
            
            logger.info(f"Ledger loaded from {self.storage_path} ({len(self.entries)} entries)")
            return True
            
        except Exception as e:
            logger.error(f"Error loading ledger: {e}")
            return False
    
    def get_entries_for_service(self, service_name: str) -> List[LedgerEntry]:
        """Get all entries for specific service"""
        return [entry for entry in self.entries if entry.service_name == service_name]
    
    def get_recent_entries(self, count: int = 100) -> List[LedgerEntry]:
        """Get most recent entries"""
        return self.entries[-count:]
    
    def cleanup_old_entries(self, max_age_days: int = 30) -> int:
        """Remove entries older than max age"""
        cutoff_time = time.time() - (max_age_days * 24 * 60 * 60)
        
        original_count = len(self.entries)
        self.entries = [entry for entry in self.entries if entry.timestamp >= cutoff_time]
        
        removed_count = original_count - len(self.entries)
        
        if removed_count > 0:
            logger.info(f"Cleaned up {removed_count} old ledger entries")
        
        return removed_count


class LedgerAnalyzer:
    """Analyze ledger data for insights"""
    
    def __init__(self, ledger: MemoryLedger):
        """Initialize ledger analyzer"""
        self.ledger = ledger
    
    def get_service_summary(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Get summary statistics for service"""
        entries = self.ledger.get_entries_for_service(service_name)
        
        if not entries:
            return None
        
        memory_values = [e.memory_usage_mb for e in entries]
        object_counts = [e.object_count for e in entries]
        
        return {
            'service': service_name,
            'entry_count': len(entries),
            'memory_stats': {
                'min_mb': min(memory_values),
                'max_mb': max(memory_values),
                'avg_mb': sum(memory_values) / len(memory_values),
                'latest_mb': memory_values[-1]
            },
            'object_stats': {
                'min_count': min(object_counts),
                'max_count': max(object_counts),
                'avg_count': sum(object_counts) / len(object_counts),
                'latest_count': object_counts[-1]
            },
            'time_range': {
                'first': entries[0].timestamp,
                'last': entries[-1].timestamp,
                'duration_hours': (entries[-1].timestamp - entries[0].timestamp) / 3600
            }
        }
    
    def detect_memory_growth(self, service_name: str) -> Optional[Dict[str, Any]]:
        """Detect memory growth patterns"""
        entries = self.ledger.get_entries_for_service(service_name)
        
        if len(entries) < 2:
            return None
        
        first = entries[0]
        last = entries[-1]
        
        memory_growth_mb = last.memory_usage_mb - first.memory_usage_mb
        duration_hours = (last.timestamp - first.timestamp) / 3600
        
        if duration_hours == 0:
            return None
        
        growth_rate = memory_growth_mb / duration_hours
        
        return {
            'service': service_name,
            'total_growth_mb': memory_growth_mb,
            'duration_hours': duration_hours,
            'growth_rate_mb_per_hour': growth_rate,
            'growth_percent': (memory_growth_mb / first.memory_usage_mb * 100) 
                             if first.memory_usage_mb > 0 else 0,
            'first_reading': first.memory_usage_mb,
            'last_reading': last.memory_usage_mb
        }
    
    def get_global_summary(self) -> Dict[str, Any]:
        """Get summary across all services"""
        if not self.ledger.entries:
            return {'error': 'No ledger entries'}
        
        services = set(entry.service_name for entry in self.ledger.entries)
        
        summaries = {}
        for service in services:
            summary = self.get_service_summary(service)
            if summary:
                summaries[service] = summary
        
        return {
            'total_entries': len(self.ledger.entries),
            'services': list(services),
            'service_count': len(services),
            'time_range': {
                'first': self.ledger.entries[0].timestamp,
                'last': self.ledger.entries[-1].timestamp
            },
            'service_summaries': summaries
        }


class PersistentLedgerManager:
    """Manage ledger with automatic persistence"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize ledger manager"""
        self.config = config
        ledger_config = config.get('ledger', {})
        
        storage_path = ledger_config.get('storage_path', 'logs/memory_ledger.json')
        max_entries = ledger_config.get('retention', {}).get('max_entries', 10000)
        
        self.ledger = MemoryLedger(storage_path, max_entries)
        self.analyzer = LedgerAnalyzer(self.ledger)
        
        # Load existing ledger
        self.ledger.load()
    
    def record_snapshot(self, service_name: str, snapshot) -> None:
        """Record snapshot to ledger"""
        self.ledger.record(
            service_name=service_name,
            memory_mb=snapshot.current_mb,
            object_count=snapshot.object_count,
            allocation_count=0,
            deallocation_count=0,
            gc_collections=0
        )
    
    def save_ledger(self) -> bool:
        """Save ledger with cleanup"""
        # Cleanup old entries
        max_age_days = self.config.get('ledger', {}).get('retention', {}).get('max_age_days', 30)
        self.ledger.cleanup_old_entries(max_age_days)
        
        # Save to disk
        return self.ledger.save()
    
    def get_service_analysis(self, service_name: str) -> Dict[str, Any]:
        """Get comprehensive service analysis"""
        summary = self.analyzer.get_service_summary(service_name)
        growth = self.analyzer.detect_memory_growth(service_name)
        
        return {
            'summary': summary,
            'growth_analysis': growth
        }

