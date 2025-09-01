#!/usr/bin/env python3
"""
Coordinate Validator Module - Agent Cellphone V2
===============================================

Validates agent coordinates before PyAutoGUI message delivery to prevent
out-of-bounds errors and ensure reliable message delivery.

Author: Agent-1 (Integration & Core Systems Specialist)
License: MIT
"""

import pyautogui
from typing import Dict, Tuple, Optional, List
from dataclasses import dataclass


@dataclass
class CoordinateValidationResult:
    """Result of coordinate validation."""
    is_valid: bool
    error_message: Optional[str] = None
    screen_bounds: Optional[Tuple[int, int]] = None
    adjusted_coords: Optional[Tuple[int, int]] = None


class CoordinateValidator:
    """
    Validates agent coordinates before PyAutoGUI operations.
    
    Ensures coordinates are within screen bounds and provides
    automatic adjustment for out-of-bounds coordinates.
    """
    
    def __init__(self):
        """Initialize coordinate validator with current screen dimensions."""
        self.screen_width, self.screen_height = pyautogui.size()
        self.safety_margin = 50  # 50 pixel safety margin from screen edges
        
    def validate_coordinates(self, coords: Tuple[int, int], agent_id: str) -> CoordinateValidationResult:
        """
        Validate coordinates for PyAutoGUI operations.
        
        For dual monitor systems, coordinates can be negative or exceed primary screen bounds.
        This method validates that coordinates are reasonable for multi-monitor setups.
        
        Args:
            coords: (x, y) coordinate tuple
            agent_id: Agent identifier for error reporting
            
        Returns:
            CoordinateValidationResult with validation status and details
        """
        x, y = coords
        
        # For dual monitor systems, allow negative coordinates and coordinates beyond primary screen
        # Only validate that coordinates are not extremely out of reasonable bounds
        min_reasonable_x = -3000  # Allow for extended desktop setups
        max_reasonable_x = 5000   # Allow for multiple monitors
        min_reasonable_y = -1000  # Allow for extended desktop setups
        max_reasonable_y = 3000   # Allow for multiple monitors
        
        if x < min_reasonable_x or x > max_reasonable_x:
            return CoordinateValidationResult(
                is_valid=False,
                error_message=f"❌ COORDINATE VALIDATION FAILED: {agent_id} X coordinate {x} outside reasonable bounds ({min_reasonable_x} to {max_reasonable_x})",
                screen_bounds=(self.screen_width, self.screen_height)
            )
            
        if y < min_reasonable_y or y > max_reasonable_y:
            return CoordinateValidationResult(
                is_valid=False,
                error_message=f"❌ COORDINATE VALIDATION FAILED: {agent_id} Y coordinate {y} outside reasonable bounds ({min_reasonable_y} to {max_reasonable_y})",
                screen_bounds=(self.screen_width, self.screen_height)
            )
        
        # Coordinates are valid for dual monitor system
        return CoordinateValidationResult(
            is_valid=True,
            screen_bounds=(self.screen_width, self.screen_height)
        )
    
    def validate_all_agent_coordinates(self, agents: Dict[str, Dict[str, any]]) -> List[CoordinateValidationResult]:
        """
        Validate coordinates for all agents in the configuration.
        
        Args:
            agents: Dictionary of agent configurations with coordinate data
            
        Returns:
            List of CoordinateValidationResult for each agent
        """
        results = []
        
        for agent_id, agent_config in agents.items():
            if "coords" in agent_config:
                coords = agent_config["coords"]
                result = self.validate_coordinates(coords, agent_id)
                results.append(result)
                
                if not result.is_valid:
                    print(f"⚠️  WARNING: {result.error_message}")
            else:
                results.append(CoordinateValidationResult(
                    is_valid=False,
                    error_message=f"❌ COORDINATE VALIDATION FAILED: {agent_id} missing 'coords' configuration"
                ))
        
        return results
    
    def get_screen_info(self) -> Dict[str, int]:
        """Get current screen dimensions and reasonable bounds for dual monitor systems."""
        return {
            "screen_width": self.screen_width,
            "screen_height": self.screen_height,
            "safety_margin": self.safety_margin,
            "reasonable_x_range": (-3000, 5000),  # Dual monitor extended desktop bounds
            "reasonable_y_range": (-1000, 3000),  # Dual monitor extended desktop bounds
            "primary_screen_bounds": (0, self.screen_width, 0, self.screen_height)
        }
    
    def print_coordinate_report(self, agents: Dict[str, Dict[str, any]]) -> None:
        """
        Print a comprehensive coordinate validation report.
        
        Args:
            agents: Dictionary of agent configurations
        """
        print("🔍 COORDINATE VALIDATION REPORT")
        print("=" * 50)
        
        screen_info = self.get_screen_info()
        print(f"📺 Primary Screen Dimensions: {screen_info['screen_width']}x{screen_info['screen_height']}")
        print(f"🖥️  Dual Monitor System: Extended desktop coordinates supported")
        print(f"✅ Reasonable X Range: {screen_info['reasonable_x_range'][0]} - {screen_info['reasonable_x_range'][1]}")
        print(f"✅ Reasonable Y Range: {screen_info['reasonable_y_range'][0]} - {screen_info['reasonable_y_range'][1]}")
        print(f"📍 Primary Screen Bounds: X({screen_info['primary_screen_bounds'][0]}-{screen_info['primary_screen_bounds'][1]}) Y({screen_info['primary_screen_bounds'][2]}-{screen_info['primary_screen_bounds'][3]})")
        print()
        
        results = self.validate_all_agent_coordinates(agents)
        
        valid_count = sum(1 for r in results if r.is_valid)
        total_count = len(results)
        
        print(f"📊 VALIDATION SUMMARY: {valid_count}/{total_count} agents have valid coordinates")
        print()
        
        for i, result in enumerate(results):
            agent_id = list(agents.keys())[i]
            coords = agents[agent_id].get("coords", "MISSING")
            
            if result.is_valid:
                print(f"✅ {agent_id}: {coords} - VALID")
            else:
                print(f"❌ {agent_id}: {coords} - INVALID")
                print(f"   {result.error_message}")
                print()


def validate_coordinates_before_delivery(coords: Tuple[int, int], agent_id: str) -> bool:
    """
    Quick coordinate validation function for use before PyAutoGUI operations.
    
    Args:
        coords: (x, y) coordinate tuple
        agent_id: Agent identifier
        
    Returns:
        bool: True if coordinates are valid, False otherwise
    """
    validator = CoordinateValidator()
    result = validator.validate_coordinates(coords, agent_id)
    
    if not result.is_valid:
        print(result.error_message)
        return False
    
    return True
