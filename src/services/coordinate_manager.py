#!/usr/bin/env python3
"""
Coordinate Manager - Advanced Coordinate Management Utilities
==========================================================

Advanced coordinate management utilities for Dream.OS integration.
Provides coordinate operations, calculations, and management capabilities.

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


class CoordinateOperation(Enum):
    """Coordinate operation enumeration."""
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"
    DISTANCE = "distance"
    NORMALIZE = "normalize"


class CoordinateFilter(Enum):
    """Coordinate filter enumeration."""
    BY_TYPE = "by_type"
    BY_SYSTEM = "by_system"
    BY_RANGE = "by_range"
    BY_TIMESTAMP = "by_timestamp"


@dataclass
class CoordinateRange:
    """Coordinate range data structure."""
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    min_z: float = 0.0
    max_z: float = 0.0
    name: str = "default"


@dataclass
class CoordinateBatch:
    """Coordinate batch data structure."""
    coordinates: List[Tuple[str, Any]]  # (coord_id, coordinate)
    operation: CoordinateOperation
    parameters: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class CoordinateCalculator:
    """Coordinate calculation utilities."""
    
    def __init__(self):
        self.calculation_cache: Dict[str, float] = {}
        logger.info("CoordinateCalculator initialized")
    
    def calculate_distance(self, coord1: Any, coord2: Any) -> float:
        """Calculate distance between two coordinates."""
        try:
            dx = coord2.x - coord1.x
            dy = coord2.y - coord1.y
            dz = coord2.z - coord1.z
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # Cache calculation
            cache_key = f"distance_{id(coord1)}_{id(coord2)}"
            self.calculation_cache[cache_key] = distance
            
            logger.info(f"Calculated distance: {distance}")
            return distance
        except Exception as e:
            logger.error(f"Error calculating distance: {e}")
            return 0.0
    
    def calculate_angle(self, coord1: Any, coord2: Any, coord3: Any) -> float:
        """Calculate angle between three coordinates."""
        try:
            # Vector from coord1 to coord2
            v1_x = coord2.x - coord1.x
            v1_y = coord2.y - coord1.y
            v1_z = coord2.z - coord1.z
            
            # Vector from coord1 to coord3
            v2_x = coord3.x - coord1.x
            v2_y = coord3.y - coord1.y
            v2_z = coord3.z - coord1.z
            
            # Dot product
            dot_product = v1_x * v2_x + v1_y * v2_y + v1_z * v2_z
            
            # Magnitudes
            mag1 = math.sqrt(v1_x**2 + v1_y**2 + v1_z**2)
            mag2 = math.sqrt(v2_x**2 + v2_y**2 + v2_z**2)
            
            if mag1 == 0 or mag2 == 0:
                return 0.0
            
            # Angle in radians
            cos_angle = dot_product / (mag1 * mag2)
            cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to valid range
            angle = math.acos(cos_angle)
            
            logger.info(f"Calculated angle: {math.degrees(angle)} degrees")
            return angle
        except Exception as e:
            logger.error(f"Error calculating angle: {e}")
            return 0.0
    
    def normalize_coordinate(self, coord: Any) -> Any:
        """Normalize coordinate to unit length."""
        try:
            magnitude = math.sqrt(coord.x**2 + coord.y**2 + coord.z**2)
            if magnitude == 0:
                return coord
            
            normalized = type(coord)(
                x=coord.x / magnitude,
                y=coord.y / magnitude,
                z=coord.z / magnitude,
                system=coord.system,
                coord_type=coord.coord_type,
                timestamp=coord.timestamp,
                metadata=coord.metadata
            )
            
            logger.info("Normalized coordinate")
            return normalized
        except Exception as e:
            logger.error(f"Error normalizing coordinate: {e}")
            return coord
    
    def interpolate_coordinates(self, coord1: Any, coord2: Any, t: float) -> Any:
        """Interpolate between two coordinates."""
        try:
            if t < 0 or t > 1:
                logger.warning(f"Interpolation parameter t={t} out of range [0,1]")
                t = max(0.0, min(1.0, t))
            
            interpolated = type(coord1)(
                x=coord1.x + t * (coord2.x - coord1.x),
                y=coord1.y + t * (coord2.y - coord1.y),
                z=coord1.z + t * (coord2.z - coord1.z),
                system=coord1.system,
                coord_type=coord1.coord_type,
                timestamp=datetime.now(timezone.utc),
                metadata=coord1.metadata
            )
            
            logger.info(f"Interpolated coordinate with t={t}")
            return interpolated
        except Exception as e:
            logger.error(f"Error interpolating coordinates: {e}")
            return coord1


class CoordinateFilter:
    """Coordinate filtering system."""
    
    def __init__(self):
        self.filters: Dict[str, Any] = {}
        logger.info("CoordinateFilter initialized")
    
    def add_filter(self, name: str, filter_type: CoordinateFilter, parameters: Dict[str, Any]) -> bool:
        """Add coordinate filter."""
        try:
            self.filters[name] = {
                'type': filter_type,
                'parameters': parameters
            }
            logger.info(f"Added filter: {name}")
            return True
        except Exception as e:
            logger.error(f"Failed to add filter {name}: {e}")
            return False
    
    def apply_filters(self, coordinates: List[Any]) -> List[Any]:
        """Apply all filters to coordinates."""
        try:
            filtered_coords = coordinates.copy()
            
            for filter_name, filter_data in self.filters.items():
                filter_type = filter_data['type']
                parameters = filter_data['parameters']
                
                if filter_type == CoordinateFilter.BY_TYPE:
                    target_type = parameters.get('type')
                    if target_type:
                        filtered_coords = [c for c in filtered_coords if c.coord_type.value == target_type]
                
                elif filter_type == CoordinateFilter.BY_SYSTEM:
                    target_system = parameters.get('system')
                    if target_system:
                        filtered_coords = [c for c in filtered_coords if c.system.value == target_system]
                
                elif filter_type == CoordinateFilter.BY_RANGE:
                    coord_range = parameters.get('range')
                    if coord_range:
                        filtered_coords = [c for c in filtered_coords if self._is_in_range(c, coord_range)]
                
                elif filter_type == CoordinateFilter.BY_TIMESTAMP:
                    start_time = parameters.get('start_time')
                    end_time = parameters.get('end_time')
                    if start_time and end_time:
                        filtered_coords = [c for c in filtered_coords if start_time <= c.timestamp <= end_time]
            
            logger.info(f"Applied filters: {len(filtered_coords)}/{len(coordinates)} coordinates remain")
            return filtered_coords
        except Exception as e:
            logger.error(f"Error applying filters: {e}")
            return coordinates
    
    def _is_in_range(self, coord: Any, coord_range: CoordinateRange) -> bool:
        """Check if coordinate is within range."""
        return (coord_range.min_x <= coord.x <= coord_range.max_x and
                coord_range.min_y <= coord.y <= coord_range.max_y and
                coord_range.min_z <= coord.z <= coord_range.max_z)


class CoordinateBatchProcessor:
    """Coordinate batch processing system."""
    
    def __init__(self):
        self.batch_queue: List[CoordinateBatch] = []
        self.processing_stats: Dict[str, int] = {
            'processed_batches': 0,
            'total_coordinates': 0,
            'successful_operations': 0,
            'failed_operations': 0
        }
        logger.info("CoordinateBatchProcessor initialized")
    
    def add_batch(self, batch: CoordinateBatch) -> bool:
        """Add batch to processing queue."""
        try:
            self.batch_queue.append(batch)
            logger.info(f"Added batch with {len(batch.coordinates)} coordinates")
            return True
        except Exception as e:
            logger.error(f"Failed to add batch: {e}")
            return False
    
    def process_batch(self, batch: CoordinateBatch) -> Dict[str, Any]:
        """Process coordinate batch."""
        try:
            results = {
                'batch_id': id(batch),
                'operation': batch.operation.value,
                'coordinates_processed': len(batch.coordinates),
                'results': [],
                'success': True,
                'errors': []
            }
            
            for coord_id, coord in batch.coordinates:
                try:
                    if batch.operation == CoordinateOperation.ADD:
                        result = self._add_coordinates(coord, batch.parameters)
                    elif batch.operation == CoordinateOperation.SUBTRACT:
                        result = self._subtract_coordinates(coord, batch.parameters)
                    elif batch.operation == CoordinateOperation.MULTIPLY:
                        result = self._multiply_coordinates(coord, batch.parameters)
                    elif batch.operation == CoordinateOperation.DIVIDE:
                        result = self._divide_coordinates(coord, batch.parameters)
                    elif batch.operation == CoordinateOperation.DISTANCE:
                        result = self._calculate_distance(coord, batch.parameters)
                    elif batch.operation == CoordinateOperation.NORMALIZE:
                        result = self._normalize_coordinate(coord)
                    else:
                        result = coord
                    
                    results['results'].append({
                        'coord_id': coord_id,
                        'result': result,
                        'success': True
                    })
                    self.processing_stats['successful_operations'] += 1
                    
                except Exception as e:
                    results['results'].append({
                        'coord_id': coord_id,
                        'result': None,
                        'success': False,
                        'error': str(e)
                    })
                    results['errors'].append(f"Error processing {coord_id}: {e}")
                    self.processing_stats['failed_operations'] += 1
            
            self.processing_stats['processed_batches'] += 1
            self.processing_stats['total_coordinates'] += len(batch.coordinates)
            
            logger.info(f"Processed batch: {len(batch.coordinates)} coordinates")
            return results
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            return {'success': False, 'error': str(e)}
    
    def _add_coordinates(self, coord: Any, parameters: Dict[str, Any]) -> Any:
        """Add coordinates."""
        add_x = parameters.get('x', 0.0)
        add_y = parameters.get('y', 0.0)
        add_z = parameters.get('z', 0.0)
        
        return type(coord)(
            x=coord.x + add_x,
            y=coord.y + add_y,
            z=coord.z + add_z,
            system=coord.system,
            coord_type=coord.coord_type,
            timestamp=coord.timestamp,
            metadata=coord.metadata
        )
    
    def _subtract_coordinates(self, coord: Any, parameters: Dict[str, Any]) -> Any:
        """Subtract coordinates."""
        sub_x = parameters.get('x', 0.0)
        sub_y = parameters.get('y', 0.0)
        sub_z = parameters.get('z', 0.0)
        
        return type(coord)(
            x=coord.x - sub_x,
            y=coord.y - sub_y,
            z=coord.z - sub_z,
            system=coord.system,
            coord_type=coord.coord_type,
            timestamp=coord.timestamp,
            metadata=coord.metadata
        )
    
    def _multiply_coordinates(self, coord: Any, parameters: Dict[str, Any]) -> Any:
        """Multiply coordinates."""
        mult_x = parameters.get('x', 1.0)
        mult_y = parameters.get('y', 1.0)
        mult_z = parameters.get('z', 1.0)
        
        return type(coord)(
            x=coord.x * mult_x,
            y=coord.y * mult_y,
            z=coord.z * mult_z,
            system=coord.system,
            coord_type=coord.coord_type,
            timestamp=coord.timestamp,
            metadata=coord.metadata
        )
    
    def _divide_coordinates(self, coord: Any, parameters: Dict[str, Any]) -> Any:
        """Divide coordinates."""
        div_x = parameters.get('x', 1.0)
        div_y = parameters.get('y', 1.0)
        div_z = parameters.get('z', 1.0)
        
        # Avoid division by zero
        div_x = div_x if div_x != 0 else 1.0
        div_y = div_y if div_y != 0 else 1.0
        div_z = div_z if div_z != 0 else 1.0
        
        return type(coord)(
            x=coord.x / div_x,
            y=coord.y / div_y,
            z=coord.z / div_z,
            system=coord.system,
            coord_type=coord.coord_type,
            timestamp=coord.timestamp,
            metadata=coord.metadata
        )
    
    def _calculate_distance(self, coord: Any, parameters: Dict[str, Any]) -> float:
        """Calculate distance."""
        target_x = parameters.get('target_x', 0.0)
        target_y = parameters.get('target_y', 0.0)
        target_z = parameters.get('target_z', 0.0)
        
        dx = target_x - coord.x
        dy = target_y - coord.y
        dz = target_z - coord.z
        
        return math.sqrt(dx**2 + dy**2 + dz**2)
    
    def _normalize_coordinate(self, coord: Any) -> Any:
        """Normalize coordinate."""
        magnitude = math.sqrt(coord.x**2 + coord.y**2 + coord.z**2)
        if magnitude == 0:
            return coord
        
        return type(coord)(
            x=coord.x / magnitude,
            y=coord.y / magnitude,
            z=coord.z / magnitude,
            system=coord.system,
            coord_type=coord.coord_type,
            timestamp=coord.timestamp,
            metadata=coord.metadata
        )
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics."""
        return self.processing_stats.copy()


def main():
    """Main function for testing."""
    calculator = CoordinateCalculator()
    filter_system = CoordinateFilter()
    batch_processor = CoordinateBatchProcessor()
    
    print("Coordinate Manager utilities initialized")
    print(f"Processing stats: {batch_processor.get_processing_stats()}")


if __name__ == "__main__":
    main()
