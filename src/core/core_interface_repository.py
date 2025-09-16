#!/usr/bin/env python3
"""
Core Interface Repository - Repository Pattern Implementation
===========================================================

Repository pattern implementation for core system interfaces.
Provides data access abstraction and interface management.

Author: Agent-2 (Architecture & Design Specialist)
License: MIT
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Protocol

logger = logging.getLogger(__name__)


class IInterfaceRepository(Protocol):
    """Repository interface for core system interfaces."""
    
    def get_interface(self, interface_id: str) -> Optional[Any]:
        """Get an interface by ID."""
        ...
    
    def save_interface(self, interface_id: str, interface: Any) -> bool:
        """Save an interface."""
        ...
    
    def delete_interface(self, interface_id: str) -> bool:
        """Delete an interface."""
        ...
    
    def list_interfaces(self) -> List[str]:
        """List all interface IDs."""
        ...


class InMemoryInterfaceRepository:
    """In-memory implementation of interface repository."""
    
    def __init__(self) -> None:
        self._interfaces: Dict[str, Any] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}
    
    def get_interface(self, interface_id: str) -> Optional[Any]:
        """Get an interface by ID."""
        interface = self._interfaces.get(interface_id)
        if interface:
            logger.debug(f"Retrieved interface: {interface_id}")
        else:
            logger.warning(f"Interface not found: {interface_id}")
        return interface
    
    def save_interface(self, interface_id: str, interface: Any) -> bool:
        """Save an interface."""
        try:
            self._interfaces[interface_id] = interface
            self._metadata[interface_id] = {
                "created_at": "2025-09-14T22:00:00",
                "updated_at": "2025-09-14T22:00:00"
            }
            logger.debug(f"Saved interface: {interface_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save interface {interface_id}: {e}")
            return False
    
    def delete_interface(self, interface_id: str) -> bool:
        """Delete an interface."""
        if interface_id in self._interfaces:
            del self._interfaces[interface_id]
            if interface_id in self._metadata:
                del self._metadata[interface_id]
            logger.debug(f"Deleted interface: {interface_id}")
            return True
        else:
            logger.warning(f"Interface not found for deletion: {interface_id}")
            return False
    
    def list_interfaces(self) -> List[str]:
        """List all interface IDs."""
        interface_ids = list(self._interfaces.keys())
        logger.debug(f"Listed {len(interface_ids)} interfaces")
        return interface_ids
    
    def get_metadata(self, interface_id: str) -> Optional[Dict[str, Any]]:
        """Get metadata for an interface."""
        return self._metadata.get(interface_id)


class FileBasedInterfaceRepository:
    """File-based implementation of interface repository."""
    
    def __init__(self, storage_path: Path) -> None:
        self._storage_path = storage_path
        self._storage_path.mkdir(parents=True, exist_ok=True)
        self._cache: Dict[str, Any] = {}
    
    def get_interface(self, interface_id: str) -> Optional[Any]:
        """Get an interface by ID from file or cache."""
        if interface_id in self._cache:
            return self._cache[interface_id]
        
        file_path = self._storage_path / f"{interface_id}.json"
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self._cache[interface_id] = data
                    logger.debug(f"Loaded interface from file: {interface_id}")
                    return data
            except Exception as e:
                logger.error(f"Failed to load interface {interface_id}: {e}")
        else:
            logger.warning(f"Interface file not found: {interface_id}")
        
        return None
    
    def save_interface(self, interface_id: str, interface: Any) -> bool:
        """Save an interface to file."""
        try:
            file_path = self._storage_path / f"{interface_id}.json"
            with open(file_path, 'w') as f:
                json.dump(interface, f, indent=2)
            
            self._cache[interface_id] = interface
            logger.debug(f"Saved interface to file: {interface_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save interface {interface_id}: {e}")
            return False
    
    def delete_interface(self, interface_id: str) -> bool:
        """Delete an interface file."""
        file_path = self._storage_path / f"{interface_id}.json"
        try:
            if file_path.exists():
                file_path.unlink()
                if interface_id in self._cache:
                    del self._cache[interface_id]
                logger.debug(f"Deleted interface file: {interface_id}")
                return True
            else:
                logger.warning(f"Interface file not found: {interface_id}")
                return False
        except Exception as e:
            logger.error(f"Failed to delete interface {interface_id}: {e}")
            return False
    
    def list_interfaces(self) -> List[str]:
        """List all interface files."""
        interface_files = [f.stem for f in self._storage_path.glob("*.json")]
        logger.debug(f"Listed {len(interface_files)} interface files")
        return interface_files





