"""
PersistentMemory - Native Dream.OS persistent memory system
V2 Compliant: ≤400 lines, ≤3 enums, ≤5 classes, ≤10 functions
"""

import os
import time
import json
import gzip
from typing import Dict, Optional, Any
from dataclasses import dataclass
from enum import Enum


class MemoryStatus(Enum):
    """Simple memory status enum"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"


class StorageType(Enum):
    """Simple storage type enum"""
    JSON = "json"
    BINARY = "binary"
    COMPRESSED = "compressed"


@dataclass
class MemoryConfig:
    """Simple memory configuration"""
    max_size: int = 1024 * 1024  # 1MB
    compression_enabled: bool = True
    encryption_enabled: bool = False
    cache_size: int = 100


class PersistentMemory:
    """Native Dream.OS persistent memory system"""
    
    def __init__(self, storage_path: str, config: MemoryConfig):
        self.storage_path = storage_path
        self.config = config
        self.memory_cache: Dict[str, Dict] = {}
        self.read_count = 0
        self.write_count = 0
        self.delete_count = 0
        self.last_access = None
        self.status = MemoryStatus.ACTIVE
        os.makedirs(storage_path, exist_ok=True)
    
    def store_memory(self, key: str, data: Any) -> bool:
        """Store data in persistent memory"""
        try:
            if not self._validate_key(key, data):
                return False
            
            storage_data = self._data_operations(data)
            self._cache_operations(key, storage_data)
            self.write_count += 1
            self.last_access = time.time()
            return True
        except Exception:
            self.status = MemoryStatus.ERROR
            return False
    
    def retrieve_memory(self, key: str) -> Optional[Any]:
        """Retrieve data from persistent memory"""
        try:
            if not self._validate_key(key):
                return None
            
            cached_data = self._cache_operations(key)
            if cached_data is not None:
                self.read_count += 1
                self.last_access = time.time()
                return self._data_operations(storage_data=cached_data)
            
            disk_data = self._disk_operations(key)
            if disk_data is not None:
                self._cache_operations(key, disk_data)
                self.read_count += 1
                self.last_access = time.time()
                return self._data_operations(storage_data=disk_data)
            
            return None
        except Exception:
            self.status = MemoryStatus.ERROR
            return None
    
    def delete_memory(self, key: str) -> bool:
        """Delete data from persistent memory"""
        try:
            if not self._validate_key(key):
                return False
            
            if key in self.memory_cache:
                del self.memory_cache[key]
            
            file_path = self._get_file_path(key)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            self.delete_count += 1
            self.last_access = time.time()
            return True
        except Exception:
            self.status = MemoryStatus.ERROR
            return False
    
    def get_memory_info(self) -> Dict[str, Any]:
        """Get memory system information"""
        return {
            'status': self.status.value,
            'cache_size': len(self.memory_cache),
            'total_reads': self.read_count,
            'total_writes': self.write_count,
            'total_deletes': self.delete_count,
            'last_access': self.last_access
        }
    
    def _validate_key(self, key: str, data: Any = None) -> bool:
        """Validate memory key and optionally data"""
        if not key or len(key) == 0 or len(key) > 255:
            return False
        if data is not None:
            data_size = len(str(data).encode('utf-8'))
            return data_size <= self.config.max_size
        return True
    
    def _data_operations(self, data: Any = None, storage_data: Dict = None) -> Any:
        """Prepare data for storage or restore from storage"""
        if data is not None:
            # Prepare for storage
            storage_data = {
                'data': data,
                'timestamp': time.time(),
                'size': len(str(data).encode('utf-8')),
                'compressed': False
            }
            
            if self.config.compression_enabled and storage_data['size'] > 1024:
                compressed_data = gzip.compress(str(data).encode('utf-8'))
                storage_data['data'] = compressed_data
                storage_data['compressed'] = True
            
            return storage_data
        else:
            # Restore from storage
            data = storage_data['data']
            if storage_data.get('compressed', False):
                data = gzip.decompress(data).decode('utf-8')
            return data
    
    def _cache_operations(self, key: str, data: Dict = None) -> Optional[Dict]:
        """Cache operations: store or retrieve"""
        if data is not None:
            # Store in cache
            if len(self.memory_cache) >= self.config.cache_size:
                oldest_key = min(self.memory_cache.keys(), 
                               key=lambda k: self.memory_cache[k]['timestamp'])
                del self.memory_cache[oldest_key]
            self.memory_cache[key] = data
            self._disk_operations(key, data)
            return None
        else:
            # Get from cache
            return self.memory_cache.get(key)
    
    def _disk_operations(self, key: str, data: Dict = None) -> Optional[Dict]:
        """Store to disk or load from disk"""
        file_path = self._get_file_path(key)
        if data is not None:
            # Store to disk
            with open(file_path, 'wb') as f:
                json.dump(data, f)
            return None
        else:
            # Load from disk
            if not os.path.exists(file_path):
                return None
            try:
                with open(file_path, 'rb') as f:
                    return json.load(f)
            except Exception:
                return None
    
    def _get_file_path(self, key: str) -> str:
        """Get file path for key"""
        safe_key = key.replace('/', '_').replace('\\', '_')
        return os.path.join(self.storage_path, f"{safe_key}.mem")


# Example usage:
# config = MemoryConfig(max_size=512*1024, compression_enabled=True, cache_size=50)
# memory = PersistentMemory("/tmp/memory", config)
# memory.store_memory("test_key", "Hello World")
# data = memory.retrieve_memory("test_key")