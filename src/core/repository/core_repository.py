#!/usr/bin/env python3
"""
Core Repository Module - V2 Compliant
Repository pattern implementation for core interfaces extracted from unified_core_interfaces.py
V2 Compliance: ≤400 lines for compliance

Author: Agent-7 (Web Development Specialist) - Swarm Coordination
License: MIT
"""

from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Protocol, Union
from concurrent.futures import Future

logger = logging.getLogger(__name__)


class SystemStatus(Enum):
    """System status enumeration."""
    INITIALIZING = "initializing"
    ACTIVE = "active"
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class ComponentType(Enum):
    """Component type enumeration."""
    CORE = "core"
    SERVICE = "service"
    INTERFACE = "interface"
    UTILITY = "utility"
    INTEGRATION = "integration"


@dataclass
class CoreSystemMetadata:
    """Metadata for core system components."""
    system_name: str
    version: str
    component_type: ComponentType
    status: SystemStatus
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    dependencies: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)
    configuration: Dict[str, Any] = field(default_factory=dict)


class ICoreSystem(Protocol):
    """Core system interface for all major system components."""

    @property
    def system_name(self) -> str:
        """Return the system name."""
        ...

    @property
    def version(self) -> str:
        """Return the system version."""
        ...

    @property
    def status(self) -> SystemStatus:
        """Return the current system status."""
        ...

    async def initialize(self) -> bool:
        """Initialize the system."""
        ...

    async def shutdown(self) -> bool:
        """Shutdown the system."""
        ...

    def get_metadata(self) -> CoreSystemMetadata:
        """Get system metadata."""
        ...


class IRepository(ABC):
    """Base repository interface for data access abstraction."""
    
    @abstractmethod
    async def create(self, entity: Any) -> Any:
        """Create a new entity."""
        pass
    
    @abstractmethod
    async def read(self, entity_id: str) -> Optional[Any]:
        """Read an entity by ID."""
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, entity: Any) -> bool:
        """Update an entity."""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete an entity."""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Any]:
        """List all entities."""
        pass
    
    @abstractmethod
    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[Any]:
        """Find entities by criteria."""
        pass


class CoreSystemRepository(IRepository):
    """
    Repository for core system components.
    
    V2 Compliance: Repository pattern implementation for core interfaces.
    """
    
    def __init__(self):
        self._systems: Dict[str, ICoreSystem] = {}
        self._metadata: Dict[str, CoreSystemMetadata] = {}
        self._cache: Dict[str, Any] = {}
        self._cache_ttl: Dict[str, datetime] = {}
        self.cache_timeout = 300  # 5 minutes
    
    async def create(self, system: ICoreSystem) -> ICoreSystem:
        """Create a new core system."""
        try:
            system_id = system.system_name
            self._systems[system_id] = system
            self._metadata[system_id] = system.get_metadata()
            
            # Initialize system
            await system.initialize()
            
            logger.info(f"✅ Core system created: {system_id}")
            return system
            
        except Exception as e:
            logger.error(f"❌ Failed to create core system: {e}")
            raise
    
    async def read(self, system_id: str) -> Optional[ICoreSystem]:
        """Read a core system by ID."""
        try:
            # Check cache first
            if self._is_cached(system_id):
                return self._cache[system_id]
            
            system = self._systems.get(system_id)
            if system:
                # Cache the result
                self._cache[system_id] = system
                self._cache_ttl[system_id] = datetime.now()
            
            return system
            
        except Exception as e:
            logger.error(f"❌ Failed to read core system {system_id}: {e}")
            return None
    
    async def update(self, system_id: str, system: ICoreSystem) -> bool:
        """Update a core system."""
        try:
            if system_id not in self._systems:
                logger.warning(f"⚠️ Core system {system_id} not found for update")
                return False
            
            self._systems[system_id] = system
            self._metadata[system_id] = system.get_metadata()
            
            # Update cache
            self._cache[system_id] = system
            self._cache_ttl[system_id] = datetime.now()
            
            logger.info(f"✅ Core system updated: {system_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update core system {system_id}: {e}")
            return False
    
    async def delete(self, system_id: str) -> bool:
        """Delete a core system."""
        try:
            if system_id not in self._systems:
                logger.warning(f"⚠️ Core system {system_id} not found for deletion")
                return False
            
            system = self._systems[system_id]
            
            # Shutdown system before deletion
            await system.shutdown()
            
            # Remove from storage
            del self._systems[system_id]
            del self._metadata[system_id]
            
            # Remove from cache
            self._cache.pop(system_id, None)
            self._cache_ttl.pop(system_id, None)
            
            logger.info(f"✅ Core system deleted: {system_id}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to delete core system {system_id}: {e}")
            return False
    
    async def list_all(self) -> List[ICoreSystem]:
        """List all core systems."""
        try:
            # Refresh cache for all systems
            await self._refresh_cache()
            
            return list(self._systems.values())
            
        except Exception as e:
            logger.error(f"❌ Failed to list core systems: {e}")
            return []
    
    async def find_by_criteria(self, criteria: Dict[str, Any]) -> List[ICoreSystem]:
        """Find core systems by criteria."""
        try:
            results = []
            
            for system_id, metadata in self._metadata.items():
                if self._matches_criteria(metadata, criteria):
                    system = await self.read(system_id)
                    if system:
                        results.append(system)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Failed to find core systems by criteria: {e}")
            return []
    
    def _is_cached(self, system_id: str) -> bool:
        """Check if system is cached and not expired."""
        if system_id not in self._cache:
            return False
        
        cache_time = self._cache_ttl.get(system_id)
        if not cache_time:
            return False
        
        return (datetime.now() - cache_time).total_seconds() < self.cache_timeout
    
    async def _refresh_cache(self):
        """Refresh cache for all systems."""
        try:
            current_time = datetime.now()
            expired_keys = []
            
            for system_id, cache_time in self._cache_ttl.items():
                if (current_time - cache_time).total_seconds() >= self.cache_timeout:
                    expired_keys.append(system_id)
            
            for system_id in expired_keys:
                self._cache.pop(system_id, None)
                self._cache_ttl.pop(system_id, None)
                
                # Re-cache if system exists
                if system_id in self._systems:
                    self._cache[system_id] = self._systems[system_id]
                    self._cache_ttl[system_id] = current_time
                    
        except Exception as e:
            logger.error(f"❌ Cache refresh failed: {e}")
    
    def _matches_criteria(self, metadata: CoreSystemMetadata, criteria: Dict[str, Any]) -> bool:
        """Check if metadata matches search criteria."""
        try:
            for key, value in criteria.items():
                if key == "component_type" and metadata.component_type != value:
                    return False
                elif key == "status" and metadata.status != value:
                    return False
                elif key == "capability" and value not in metadata.capabilities:
                    return False
                elif key == "dependency" and value not in metadata.dependencies:
                    return False
                elif key == "version" and metadata.version != value:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Criteria matching failed: {e}")
            return False
    
    def get_repository_statistics(self) -> Dict[str, Any]:
        """Get repository statistics for web interface."""
        return {
            "total_systems": len(self._systems),
            "cached_systems": len(self._cache),
            "systems_by_type": self._get_systems_by_type(),
            "systems_by_status": self._get_systems_by_status(),
            "cache_hit_ratio": self._calculate_cache_hit_ratio(),
            "last_updated": datetime.now().isoformat()
        }
    
    def _get_systems_by_type(self) -> Dict[str, int]:
        """Get count of systems by type."""
        type_counts = {}
        for metadata in self._metadata.values():
            type_name = metadata.component_type.value
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        return type_counts
    
    def _get_systems_by_status(self) -> Dict[str, int]:
        """Get count of systems by status."""
        status_counts = {}
        for metadata in self._metadata.values():
            status_name = metadata.status.value
            status_counts[status_name] = status_counts.get(status_name, 0) + 1
        return status_counts
    
    def _calculate_cache_hit_ratio(self) -> float:
        """Calculate cache hit ratio."""
        total_requests = len(self._systems) + len(self._cache)
        if total_requests == 0:
            return 0.0
        return len(self._cache) / total_requests
    
    def clear_cache(self):
        """Clear all cached data."""
        self._cache.clear()
        self._cache_ttl.clear()
        logger.info("🧹 Repository cache cleared")


class CoreSystemService:
    """
    Service layer for core system operations.
    
    V2 Compliance: Service layer pattern implementation.
    """
    
    def __init__(self):
        self.repository = CoreSystemRepository()
        self.web_interface_callbacks = []
    
    async def register_system(self, system: ICoreSystem) -> bool:
        """Register a new core system."""
        try:
            await self.repository.create(system)
            
            # Notify web interface
            self._notify_web_interface("system_registered", {
                "system_name": system.system_name,
                "version": system.version,
                "status": system.status.value
            })
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to register system: {e}")
            return False
    
    async def get_system(self, system_id: str) -> Optional[ICoreSystem]:
        """Get a core system by ID."""
        return await self.repository.read(system_id)
    
    async def update_system(self, system_id: str, system: ICoreSystem) -> bool:
        """Update a core system."""
        success = await self.repository.update(system_id, system)
        
        if success:
            # Notify web interface
            self._notify_web_interface("system_updated", {
                "system_id": system_id,
                "status": system.status.value
            })
        
        return success
    
    async def unregister_system(self, system_id: str) -> bool:
        """Unregister a core system."""
        success = await self.repository.delete(system_id)
        
        if success:
            # Notify web interface
            self._notify_web_interface("system_unregistered", {
                "system_id": system_id
            })
        
        return success
    
    async def list_systems(self) -> List[ICoreSystem]:
        """List all registered systems."""
        return await self.repository.list_all()
    
    async def find_systems_by_type(self, component_type: ComponentType) -> List[ICoreSystem]:
        """Find systems by component type."""
        return await self.repository.find_by_criteria({"component_type": component_type})
    
    async def find_systems_by_status(self, status: SystemStatus) -> List[ICoreSystem]:
        """Find systems by status."""
        return await self.repository.find_by_criteria({"status": status})
    
    def get_service_statistics(self) -> Dict[str, Any]:
        """Get service statistics for web interface."""
        return self.repository.get_repository_statistics()
    
    def add_web_interface_callback(self, callback):
        """Add web interface callback for real-time updates."""
        self.web_interface_callbacks.append(callback)
    
    def _notify_web_interface(self, event_type: str, data: Dict[str, Any]):
        """Notify web interface of events."""
        try:
            for callback in self.web_interface_callbacks:
                try:
                    callback(event_type, data)
                except Exception as e:
                    logger.error(f"❌ Web interface callback error: {e}")
        except Exception as e:
            logger.error(f"❌ Web interface notification failed: {e}")


# Global instance for web interface integration
_core_system_service = None


def get_core_system_service() -> CoreSystemService:
    """Get the global core system service instance."""
    global _core_system_service
    if _core_system_service is None:
        _core_system_service = CoreSystemService()
    return _core_system_service
