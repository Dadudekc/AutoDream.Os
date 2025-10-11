#!/usr/bin/env python3
"""
Coordinate Loader - Advanced Coordinate Management System
======================================================

Advanced coordinate loading and management system for Dream.OS integration.
Provides coordinate validation, transformation, and management capabilities.

V2 Compliance: < 400 lines, single responsibility
Author: Agent-1 (Backend & API Specialist)
License: MIT
"""

import json
import logging
import math
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class CoordinateSystem(Enum):
    """Coordinate system enumeration."""
    CARTESIAN = "cartesian"
    POLAR = "polar"
    SPHERICAL = "spherical"
    CYLINDRICAL = "cylindrical"


class CoordinateType(Enum):
    """Coordinate type enumeration."""
    POSITION = "position"
    ROTATION = "rotation"
    SCALE = "scale"
    TRANSFORM = "transform"


@dataclass
class Coordinate:
    """Coordinate data structure."""
    x: float
    y: float
    z: float = 0.0
    system: CoordinateSystem = CoordinateSystem.CARTESIAN
    coord_type: CoordinateType = CoordinateType.POSITION
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CoordinateTransform:
    """Coordinate transformation data structure."""
    source_system: CoordinateSystem
    target_system: CoordinateSystem
    transform_matrix: List[List[float]]
    translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)


class CoordinateValidator:
    """Coordinate validation system."""
    
    def __init__(self):
        self.validation_rules: Dict[str, Any] = {}
        self.bounds: Dict[str, Tuple[float, float]] = {}
        logger.info("CoordinateValidator initialized")
    
    def set_validation_rules(self, rules: Dict[str, Any]) -> bool:
        """Set validation rules for coordinates."""
        try:
            self.validation_rules = rules
            logger.info("Validation rules set")
            return True
        except Exception as e:
            logger.error(f"Failed to set validation rules: {e}")
            return False
    
    def set_bounds(self, bounds: Dict[str, Tuple[float, float]]) -> bool:
        """Set coordinate bounds for validation."""
        try:
            self.bounds = bounds
            logger.info("Coordinate bounds set")
            return True
        except Exception as e:
            logger.error(f"Failed to set bounds: {e}")
            return False
    
    def validate_coordinate(self, coord: Coordinate) -> Tuple[bool, List[str]]:
        """Validate coordinate against rules and bounds."""
        errors = []
        
        try:
            # Check bounds
            if "x" in self.bounds:
                min_x, max_x = self.bounds["x"]
                if not (min_x <= coord.x <= max_x):
                    errors.append(f"X coordinate {coord.x} out of bounds [{min_x}, {max_x}]")
            
            if "y" in self.bounds:
                min_y, max_y = self.bounds["y"]
                if not (min_y <= coord.y <= max_y):
                    errors.append(f"Y coordinate {coord.y} out of bounds [{min_y}, {max_y}]")
            
            if "z" in self.bounds:
                min_z, max_z = self.bounds["z"]
                if not (min_z <= coord.z <= max_z):
                    errors.append(f"Z coordinate {coord.z} out of bounds [{min_z}, {max_z}]")
            
            # Check validation rules
            if "max_distance" in self.validation_rules:
                max_dist = self.validation_rules["max_distance"]
                distance = math.sqrt(coord.x**2 + coord.y**2 + coord.z**2)
                if distance > max_dist:
                    errors.append(f"Distance {distance} exceeds maximum {max_dist}")
            
            if "min_distance" in self.validation_rules:
                min_dist = self.validation_rules["min_distance"]
                distance = math.sqrt(coord.x**2 + coord.y**2 + coord.z**2)
                if distance < min_dist:
                    errors.append(f"Distance {distance} below minimum {min_dist}")
            
            is_valid = len(errors) == 0
            logger.info(f"Coordinate validation: {'PASS' if is_valid else 'FAIL'}")
            return is_valid, errors
            
        except Exception as e:
            logger.error(f"Error validating coordinate: {e}")
            return False, [f"Validation error: {e}"]


class CoordinateTransformer:
    """Coordinate transformation system."""
    
    def __init__(self):
        self.transforms: Dict[str, CoordinateTransform] = {}
        logger.info("CoordinateTransformer initialized")
    
    def add_transform(self, name: str, transform: CoordinateTransform) -> bool:
        """Add coordinate transformation."""
        try:
            self.transforms[name] = transform
            logger.info(f"Added transform: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add transform {name}: {e}")
            return False
    
    def transform_coordinate(self, coord: Coordinate, transform_name: str) -> Optional[Coordinate]:
        """Transform coordinate using specified transformation."""
        try:
            if transform_name not in self.transforms:
                logger.warning(f"Transform {transform_name} not found")
                return None
            
            transform = self.transforms[transform_name]
            
            # Apply transformation based on source and target systems
            if transform.source_system == CoordinateSystem.CARTESIAN and transform.target_system == CoordinateSystem.POLAR:
                return self._cartesian_to_polar(coord, transform)
            elif transform.source_system == CoordinateSystem.POLAR and transform.target_system == CoordinateSystem.CARTESIAN:
                return self._polar_to_cartesian(coord, transform)
            elif transform.source_system == CoordinateSystem.CARTESIAN and transform.target_system == CoordinateSystem.SPHERICAL:
                return self._cartesian_to_spherical(coord, transform)
            elif transform.source_system == CoordinateSystem.SPHERICAL and transform.target_system == CoordinateSystem.CARTESIAN:
                return self._spherical_to_cartesian(coord, transform)
            else:
                logger.warning(f"Unsupported transformation: {transform.source_system} -> {transform.target_system}")
                return None
                
        except Exception as e:
            logger.error(f"Error transforming coordinate: {e}")
            return None
    
    def _cartesian_to_polar(self, coord: Coordinate, transform: CoordinateTransform) -> Coordinate:
        """Convert Cartesian to polar coordinates."""
        r = math.sqrt(coord.x**2 + coord.y**2)
        theta = math.atan2(coord.y, coord.x)
        return Coordinate(r, theta, coord.z, CoordinateSystem.POLAR, coord.coord_type, coord.timestamp, coord.metadata)
    
    def _polar_to_cartesian(self, coord: Coordinate, transform: CoordinateTransform) -> Coordinate:
        """Convert polar to Cartesian coordinates."""
        x = coord.x * math.cos(coord.y)
        y = coord.x * math.sin(coord.y)
        return Coordinate(x, y, coord.z, CoordinateSystem.CARTESIAN, coord.coord_type, coord.timestamp, coord.metadata)
    
    def _cartesian_to_spherical(self, coord: Coordinate, transform: CoordinateTransform) -> Coordinate:
        """Convert Cartesian to spherical coordinates."""
        r = math.sqrt(coord.x**2 + coord.y**2 + coord.z**2)
        theta = math.atan2(coord.y, coord.x)
        phi = math.acos(coord.z / r) if r > 0 else 0
        return Coordinate(r, theta, phi, CoordinateSystem.SPHERICAL, coord.coord_type, coord.timestamp, coord.metadata)
    
    def _spherical_to_cartesian(self, coord: Coordinate, transform: CoordinateTransform) -> Coordinate:
        """Convert spherical to Cartesian coordinates."""
        x = coord.x * math.sin(coord.z) * math.cos(coord.y)
        y = coord.x * math.sin(coord.z) * math.sin(coord.y)
        z = coord.x * math.cos(coord.z)
        return Coordinate(x, y, z, CoordinateSystem.CARTESIAN, coord.coord_type, coord.timestamp, coord.metadata)


class CoordinateStorage:
    """Coordinate storage and retrieval system."""
    
    def __init__(self, storage_path: str = "data/coordinates.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.coordinates: Dict[str, Coordinate] = {}
        self._load_coordinates()
        logger.info("CoordinateStorage initialized")
    
    def _load_coordinates(self) -> None:
        """Load coordinates from storage."""
        try:
            if self.storage_path.exists():
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for coord_id, coord_data in data.items():
                        coord = Coordinate(
                            x=coord_data['x'],
                            y=coord_data['y'],
                            z=coord_data.get('z', 0.0),
                            system=CoordinateSystem(coord_data.get('system', 'cartesian')),
                            coord_type=CoordinateType(coord_data.get('coord_type', 'position')),
                            timestamp=datetime.fromisoformat(coord_data['timestamp']),
                            metadata=coord_data.get('metadata', {})
                        )
                        self.coordinates[coord_id] = coord
                logger.info(f"Loaded {len(self.coordinates)} coordinates from storage")
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
    
    def save_coordinates(self) -> bool:
        """Save coordinates to storage."""
        try:
            data = {}
            for coord_id, coord in self.coordinates.items():
                data[coord_id] = {
                    'x': coord.x,
                    'y': coord.y,
                    'z': coord.z,
                    'system': coord.system.value,
                    'coord_type': coord.coord_type.value,
                    'timestamp': coord.timestamp.isoformat(),
                    'metadata': coord.metadata
                }
            
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.coordinates)} coordinates to storage")
            return True
        except Exception as e:
            logger.error(f"Error saving coordinates: {e}")
            return False
    
    def store_coordinate(self, coord_id: str, coord: Coordinate) -> bool:
        """Store coordinate with ID."""
        try:
            self.coordinates[coord_id] = coord
            self.save_coordinates()
            logger.info(f"Stored coordinate {coord_id}")
            return True
        except Exception as e:
            logger.error(f"Error storing coordinate {coord_id}: {e}")
            return False
    
    def get_coordinate(self, coord_id: str) -> Optional[Coordinate]:
        """Get coordinate by ID."""
        return self.coordinates.get(coord_id)
    
    def list_coordinates(self, coord_type: Optional[CoordinateType] = None) -> List[Coordinate]:
        """List coordinates with optional filtering."""
        coords = list(self.coordinates.values())
        if coord_type:
            coords = [c for c in coords if c.coord_type == coord_type]
        return coords


class CoordinateLoader:
    """Main CoordinateLoader class."""
    
    def __init__(self, storage_path: str = "data/coordinates.json"):
        self.validator = CoordinateValidator()
        self.transformer = CoordinateTransformer()
        self.storage = CoordinateStorage(storage_path)
        logger.info("CoordinateLoader initialized")
    
    def load_coordinate(self, coord_id: str) -> Optional[Coordinate]:
        """Load coordinate by ID."""
        try:
            coord = self.storage.get_coordinate(coord_id)
            if coord:
                logger.info(f"Loaded coordinate {coord_id}")
            else:
                logger.warning(f"Coordinate {coord_id} not found")
            return coord
        except Exception as e:
            logger.error(f"Error loading coordinate {coord_id}: {e}")
            return None
    
    def save_coordinate(self, coord_id: str, coord: Coordinate) -> bool:
        """Save coordinate with validation."""
        try:
            # Validate coordinate
            is_valid, errors = self.validator.validate_coordinate(coord)
            if not is_valid:
                logger.warning(f"Coordinate validation failed: {errors}")
                return False
            
            # Store coordinate
            success = self.storage.store_coordinate(coord_id, coord)
            if success:
                logger.info(f"Saved coordinate {coord_id}")
            return success
        except Exception as e:
            logger.error(f"Error saving coordinate {coord_id}: {e}")
            return False
    
    def transform_coordinate(self, coord: Coordinate, transform_name: str) -> Optional[Coordinate]:
        """Transform coordinate using specified transformation."""
        return self.transformer.transform_coordinate(coord, transform_name)
    
    def set_validation_rules(self, rules: Dict[str, Any]) -> bool:
        """Set validation rules."""
        return self.validator.set_validation_rules(rules)
    
    def set_coordinate_bounds(self, bounds: Dict[str, Tuple[float, float]]) -> bool:
        """Set coordinate bounds."""
        return self.validator.set_bounds(bounds)
    
    def add_transform(self, name: str, transform: CoordinateTransform) -> bool:
        """Add coordinate transformation."""
        return self.transformer.add_transform(name, transform)
    
    def get_coordinate_stats(self) -> Dict[str, Any]:
        """Get coordinate statistics."""
        coords = self.storage.list_coordinates()
        return {
            "total_coordinates": len(coords),
            "coordinate_types": {
                coord_type.value: len([c for c in coords if c.coord_type == coord_type])
                for coord_type in CoordinateType
            },
            "coordinate_systems": {
                system.value: len([c for c in coords if c.system == system])
                for system in CoordinateSystem
            }
        }


def main():
    """Main function for testing."""
    loader = CoordinateLoader()
    
    # Test coordinate creation
    coord = Coordinate(1.0, 2.0, 3.0, CoordinateSystem.CARTESIAN, CoordinateType.POSITION)
    print(f"Created coordinate: {coord}")
    
    # Test coordinate saving
    success = loader.save_coordinate("test_coord_1", coord)
    print(f"Coordinate saving: {'Success' if success else 'Failed'}")
    
    # Test coordinate loading
    loaded_coord = loader.load_coordinate("test_coord_1")
    print(f"Coordinate loading: {'Success' if loaded_coord else 'Failed'}")
    
    # Test coordinate stats
    stats = loader.get_coordinate_stats()
    print(f"Coordinate stats: {stats}")


if __name__ == "__main__":
    main()
