#!/usr/bin/env python3
"""
Coordinate Validation Engine
============================

Coordinate validation engine for the unified validation system.
Handles coordinate validation for PyAutoGUI operations.
V2 COMPLIANT: Focused coordinate validation under 300 lines.

@version 1.0.0 - V2 COMPLIANCE MODULAR COORDINATE VALIDATION
@license MIT
"""

import logging
from typing import List, Tuple, Optional, Dict, Any

from .models.validation_models import (
    ValidationSeverity, ValidationResult, ValidationType
)


class CoordinateValidationEngine:
    """Coordinate validation engine for PyAutoGUI operations"""
    
    def __init__(self):
        """Initialize coordinate validation engine"""
        self.logger = logging.getLogger(__name__)
        # Coordinate validation patterns
        self.coordinate_patterns = {
            "valid_range": (-10000, 10000),
            "min_coords": 2,
            "max_coords": 2
        }
    
    def validate_coordinates(self, coords: Tuple[int, int], recipient: str = None) -> List[ValidationResult]:
        """
        Validate coordinates for PyAutoGUI operations.
        
        Args:
            coords: Tuple of (x, y) coordinates
            recipient: Optional recipient for context
            
        Returns:
            List of validation issues
        """
        issues = []
        
        try:
            if not coords:
                issues.append(create_validation_issue(
                    message="Coordinates are required",
                    severity=ValidationSeverity.ERROR,
                    field="coords"
                ))
                return issues
            
            if not isinstance(coords, (tuple, list)) or len(coords) != 2:
                issues.append(create_validation_issue(
                    message="Coordinates must be a tuple/list of (x, y)",
                    severity=ValidationSeverity.ERROR,
                    field="coords",
                    value=coords
                ))
                return issues
            
            x, y = coords
            
            # Validate x coordinate
            if not isinstance(x, (int, float)):
                issues.append(create_validation_issue(
                    message="X coordinate must be a number",
                    severity=ValidationSeverity.ERROR,
                    field="x",
                    value=x
                ))
            else:
                x_range = self.pattern.constraints["x_range"]
                if not (x_range[0] <= x <= x_range[1]):
                    issues.append(create_validation_issue(
                        message=f"X coordinate {x} is outside valid range {x_range}",
                        severity=ValidationSeverity.WARNING,
                        field="x",
                        value=x,
                        suggestion=f"Consider adjusting to range {x_range[0]}-{x_range[1]}"
                    ))
            
            # Validate y coordinate
            if not isinstance(y, (int, float)):
                issues.append(create_validation_issue(
                    message="Y coordinate must be a number",
                    severity=ValidationSeverity.ERROR,
                    field="y",
                    value=y
                ))
            else:
                y_range = self.pattern.constraints["y_range"]
                if not (y_range[0] <= y <= y_range[1]):
                    issues.append(create_validation_issue(
                        message=f"Y coordinate {y} is outside valid range {y_range}",
                        severity=ValidationSeverity.WARNING,
                        field="y",
                        value=y,
                        suggestion=f"Consider adjusting to range {y_range[0]}-{y_range[1]}"
                    ))
            
            # Additional validation for specific recipients
            if recipient:
                issues.extend(self._validate_recipient_specific_coords(coords, recipient))
            
            # Log validation results
            if issues:
                self.logger.warning(f"Coordinate validation failed: {len(issues)} issues")
            else:
                self.logger.debug("Coordinate validation passed")
                
        except Exception as e:
            issues.append(create_validation_issue(
                message=f"Coordinate validation error: {e}",
                severity=ValidationSeverity.CRITICAL,
                field="coords",
                value=coords
            ))
        
        return issues
    
    def _validate_recipient_specific_coords(self, coords: Tuple[int, int], recipient: str) -> List[ValidationResult]:
        """Validate coordinates for specific recipients."""
        issues = []
        x, y = coords
        
        # Agent-specific coordinate validation
        if recipient and recipient.startswith("Agent-"):
            # Check if coordinates are in agent-specific areas
            agent_areas = {
                "Agent-1": (100, 200, 100, 200),
                "Agent-2": (300, 400, 100, 200),
                "Agent-3": (500, 600, 100, 200),
                "Agent-4": (700, 800, 100, 200),
                "Agent-5": (100, 200, 300, 400),
                "Agent-6": (300, 400, 300, 400),
                "Agent-7": (500, 600, 300, 400),
                "Agent-8": (700, 800, 300, 400)
            }
            
            if recipient in agent_areas:
                min_x, max_x, min_y, max_y = agent_areas[recipient]
                if not (min_x <= x <= max_x and min_y <= y <= max_y):
                    issues.append(create_validation_issue(
                        message=f"Coordinates ({x}, {y}) are outside {recipient} area",
                        severity=ValidationSeverity.WARNING,
                        field="coords",
                        value=coords,
                        suggestion=f"Consider using coordinates within {recipient} area: ({min_x}-{max_x}, {min_y}-{max_y})"
                    ))
        
        return issues
    
    def validate_coordinate_list(self, coord_list: List[Tuple[int, int]], 
                               recipient: str = None) -> List[ValidationResult]:
        """Validate a list of coordinates."""
        issues = []
        
        if not coord_list:
            issues.append(create_validation_issue(
                message="Coordinate list is empty",
                severity=ValidationSeverity.WARNING,
                field="coord_list"
            ))
            return issues
        
        for i, coords in enumerate(coord_list):
            coord_issues = self.validate_coordinates(coords, recipient)
            for issue in coord_issues:
                # Update field to include index
                issue.field = f"coord_list[{i}].{issue.field}" if issue.field else f"coord_list[{i}]"
            issues.extend(coord_issues)
        
        return issues
    
    def validate_coordinate_bounds(self, coords: Tuple[int, int], 
                                 bounds: Tuple[int, int, int, int]) -> List[ValidationResult]:
        """Validate coordinates against custom bounds (min_x, max_x, min_y, max_y)."""
        issues = []
        
        if not coords or len(coords) != 2:
            issues.append(create_validation_issue(
                message="Invalid coordinates format",
                severity=ValidationSeverity.ERROR,
                field="coords"
            ))
            return issues
        
        if len(bounds) != 4:
            issues.append(create_validation_issue(
                message="Bounds must be (min_x, max_x, min_y, max_y)",
                severity=ValidationSeverity.ERROR,
                field="bounds"
            ))
            return issues
        
        x, y = coords
        min_x, max_x, min_y, max_y = bounds
        
        if not (min_x <= x <= max_x):
            issues.append(create_validation_issue(
                message=f"X coordinate {x} is outside bounds [{min_x}, {max_x}]",
                severity=ValidationSeverity.WARNING,
                field="x",
                value=x
            ))
        
        if not (min_y <= y <= max_y):
            issues.append(create_validation_issue(
                message=f"Y coordinate {y} is outside bounds [{min_y}, {max_y}]",
                severity=ValidationSeverity.WARNING,
                field="y",
                value=y
            ))
        
        return issues
    
    def get_coordinate_validation_result(self, coords: Tuple[int, int], 
                                       recipient: str = None) -> ValidationResult:
        """Get comprehensive validation result for coordinates."""
        issues = self.validate_coordinates(coords, recipient)
        is_valid = len(issues) == 0 or not any(issue.severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL] for issue in issues)
        
        return create_validation_result(
            is_valid=is_valid,
            issues=issues,
            validated_data=coords,
            validation_type="coordinate"
        )
    
    def suggest_coordinate_corrections(self, coords: Tuple[int, int]) -> Tuple[int, int]:
        """Suggest corrected coordinates within valid bounds."""
        if not coords or len(coords) != 2:
            return (0, 0)
        
        x, y = coords
        x_range = self.pattern.constraints["x_range"]
        y_range = self.pattern.constraints["y_range"]
        
        # Clamp coordinates to valid ranges
        corrected_x = max(x_range[0], min(x, x_range[1]))
        corrected_y = max(y_range[0], min(y, y_range[1]))
        
        return (corrected_x, corrected_y)


# Factory function for dependency injection
def create_coordinate_validation_engine() -> CoordinateValidationEngine:
    """Factory function to create coordinate validation engine"""
    return CoordinateValidationEngine()


# Export for DI
__all__ = ['CoordinateValidationEngine', 'create_coordinate_validation_engine']
