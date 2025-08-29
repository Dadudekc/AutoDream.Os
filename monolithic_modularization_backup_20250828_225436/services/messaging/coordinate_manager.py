#!/usr/bin/env python3
"""
Coordinate Manager - Agent Cellphone V2
======================================

Manages agent coordinates and validation.
Single responsibility: Coordinate management only.
Follows V2 standards: OOP, SRP, clean production-grade code.

Author: V2 SWARM CAPTAIN
License: MIT
"""

import json
import logging

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from dataclasses import dataclass

from .interfaces import ICoordinateManager

logger = logging.getLogger(__name__)


@dataclass
class CoordinateData:
    """Data structure for agent coordinates"""
    agent_id: str
    mode: str
    input_box: Tuple[int, int]
    starter_location: Tuple[int, int]


@dataclass
class AgentCoordinates:
    """Agent coordinate data structure"""
    agent_id: str
    starter_location: Tuple[int, int]
    input_box: Tuple[int, int]
    mode: str


class CoordinateManager(ICoordinateManager):
    """
    Coordinate Manager - Single responsibility: Manage agent coordinates
    
    This class only handles:
    - Loading coordinate files
    - Retrieving agent coordinates
    - Validating coordinate data
    - Coordinate mapping and calibration
    """
    
    def __init__(self, coordinates_file: str = "config/agents/coordinates.json"):
        """Initialize the coordinate manager with primary config location"""
        self.coordinates_file = Path(coordinates_file)
        # Fallback to runtime location if primary doesn't exist
        if not self.coordinates_file.exists():
            fallback_file = Path("runtime/agent_comms/cursor_agent_coords.json")
            if fallback_file.exists():
                self.coordinates_file = fallback_file
                logger.info(f"Using fallback coordinate file: {fallback_file}")
        
        self.coordinates = self._load_coordinates()
        logger.info("Coordinate Manager initialized")
    
    def _load_coordinates(self) -> Dict[str, Any]:
        """Load agent coordinates from configuration file"""
        try:
            if self.coordinates_file.exists():
                with open(self.coordinates_file, 'r') as f:
                    coords = json.load(f)
                    logger.info(f"Coordinates loaded: {len(coords)} agent configurations")
                    return coords
            else:
                logger.error(f"Coordinate file not found: {self.coordinates_file}")
                return {}
        except Exception as e:
            logger.error(f"Error loading coordinates: {e}")
            return {}
    
    def get_agent_coordinates(self, agent_id: str, mode: str = "8-agent") -> Optional[AgentCoordinates]:
        """Get coordinates for a specific agent"""
        try:
            if mode in self.coordinates and agent_id in self.coordinates[mode]:
                agent_coords = self.coordinates[mode][agent_id]
                
                starter_x = agent_coords["starter_location_box"]["x"]
                starter_y = agent_coords["starter_location_box"]["y"]
                input_x = agent_coords["input_box"]["x"]
                input_y = agent_coords["input_box"]["y"]
                
                return AgentCoordinates(
                    agent_id=agent_id,
                    starter_location=(starter_x, starter_y),
                    input_box=(input_x, input_y),
                    mode=mode
                )
            else:
                logger.warning(f"Coordinates not found for {agent_id} in {mode} mode")
                return None
        except Exception as e:
            logger.error(f"Error getting coordinates for {agent_id}: {e}")
            return None
    
    def validate_coordinates(self) -> Dict[str, Any]:
        """Validate all loaded coordinates"""
        validation_results = {
            "total_modes": len(self.coordinates),
            "total_agents": 0,
            "valid_coordinates": 0,
            "missing_coordinates": 0,
            "errors": []
        }
        
        for mode, agents in self.coordinates.items():
            for agent_id, coords in agents.items():
                validation_results["total_agents"] += 1
                
                try:
                    required_fields = ["starter_location_box", "input_box"]
                    if all(field in coords for field in required_fields):
                        validation_results["valid_coordinates"] += 1
                    else:
                        validation_results["missing_coordinates"] += 1
                        validation_results["errors"].append(f"Missing fields for {agent_id} in {mode}")
                except Exception as e:
                    validation_results["errors"].append(f"Error validating {agent_id} in {mode}: {e}")
        
        return validation_results
    
    def get_available_modes(self) -> list:
        """Get list of available coordinate modes"""
        return list(self.coordinates.keys())
    
    def get_agents_in_mode(self, mode: str) -> list:
        """Get list of agents available in a specific mode"""
        return list(self.coordinates.get(mode, {}).keys())
    
    def map_coordinates(self, mode: str = "8-agent") -> Dict[str, Any]:
        """
        Map and display coordinate information for debugging and calibration
        
        Returns detailed coordinate mapping for all agents in a mode
        """
        logger.info(f"🗺️  Mapping coordinates for mode: {mode}")
        
        mapping_result = {
            "mode": mode,
            "agents": {},
            "summary": {
                "total_agents": 0,
                "valid_agents": 0,
                "invalid_agents": 0
            }
        }
        
        if mode not in self.coordinates:
            logger.warning(f"Mode '{mode}' not found in coordinates")
            return mapping_result
        
        for agent_id, agent_data in self.coordinates[mode].items():
            mapping_result["summary"]["total_agents"] += 1
            
            try:
                # Extract coordinates
                input_box = agent_data.get("input_box", {})
                starter_box = agent_data.get("starter_location_box", {})
                
                input_coords = (input_box.get("x"), input_box.get("y"))
                starter_coords = (starter_box.get("x"), starter_box.get("y"))
                
                # Validate coordinates
                valid_input = all(coord is not None for coord in input_coords)
                valid_starter = all(coord is not None for coord in starter_coords)
                
                agent_mapping = {
                    "input_box": {
                        "coordinates": input_coords,
                        "raw": input_box,
                        "valid": valid_input
                    },
                    "starter_location": {
                        "coordinates": starter_coords,
                        "raw": starter_box,
                        "valid": valid_starter
                    },
                    "overall_valid": valid_input and valid_starter
                }
                
                mapping_result["agents"][agent_id] = agent_mapping
                
                if agent_mapping["overall_valid"]:
                    mapping_result["summary"]["valid_agents"] += 1
                    logger.info(f"✅ {agent_id}: Input({input_coords[0]}, {input_coords[1]}) Starter({starter_coords[0]}, {starter_coords[1]})")
                else:
                    mapping_result["summary"]["invalid_agents"] += 1
                    logger.warning(f"❌ {agent_id}: Invalid coordinates")
                    
            except Exception as e:
                mapping_result["summary"]["invalid_agents"] += 1
                logger.error(f"❌ {agent_id}: Error mapping coordinates: {e}")
                
        logger.info(f"📊 Coordinate mapping complete: {mapping_result['summary']['valid_agents']}/{mapping_result['summary']['total_agents']} valid agents")
        return mapping_result
    
    def calibrate_coordinates(self, agent_id: str, input_coords: Tuple[int, int], starter_coords: Tuple[int, int], mode: str = "8-agent") -> bool:
        """
        Calibrate/update coordinates for a specific agent
        
        This method updates coordinates and saves them back to the file
        """
        logger.info(f"🔧 Calibrating coordinates for {agent_id} in mode {mode}")
        
        try:
            # Ensure mode exists
            if mode not in self.coordinates:
                self.coordinates[mode] = {}
            
            # Ensure agent exists
            if agent_id not in self.coordinates[mode]:
                self.coordinates[mode][agent_id] = {}
            
            # Update coordinates
            self.coordinates[mode][agent_id]["input_box"] = {
                "x": input_coords[0],
                "y": input_coords[1]
            }
            self.coordinates[mode][agent_id]["starter_location_box"] = {
                "x": starter_coords[0],
                "y": starter_coords[1]
            }
            
            # Save back to file
            with open(self.coordinates_file, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            
            logger.info(f"✅ Coordinates calibrated for {agent_id}: Input({input_coords[0]}, {input_coords[1]}) Starter({starter_coords[0]}, {starter_coords[1]})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to calibrate coordinates for {agent_id}: {e}")
            return False
    
    def consolidate_coordinate_files(self) -> Dict[str, Any]:
        """
        Consolidate multiple coordinate files into the primary config location
        
        This method finds and merges coordinate data from multiple sources
        """
        logger.info("🔄 Consolidating coordinate files...")
        
        consolidation_result = {
            "primary_file": str(self.coordinates_file),
            "sources_found": [],
            "sources_merged": [],
            "conflicts": [],
            "final_coordinates": {}
        }
        
        # List of possible coordinate file locations
        possible_sources = [
            Path("config/agents/coordinates.json"),
            Path("runtime/agent_comms/cursor_agent_coords.json"),
            Path("src/services/cursor_agent_coords.json"),
            Path("cursor_agent_coords.json")
        ]
        
        # Find existing coordinate files
        existing_sources = [source for source in possible_sources if source.exists()]
        consolidation_result["sources_found"] = [str(source) for source in existing_sources]
        
        logger.info(f"📁 Found {len(existing_sources)} coordinate files")
        
        # Load and merge coordinates from all sources
        merged_coordinates = {}
        
        for source in existing_sources:
            try:
                with open(source, 'r') as f:
                    source_coords = json.load(f)
                
                consolidation_result["sources_merged"].append(str(source))
                logger.info(f"📥 Loading coordinates from: {source}")
                
                # Merge coordinates
                for mode, agents in source_coords.items():
                    if mode not in merged_coordinates:
                        merged_coordinates[mode] = {}
                    
                    for agent_id, agent_data in agents.items():
                        if agent_id in merged_coordinates[mode]:
                            # Check for conflicts
                            existing_data = merged_coordinates[mode][agent_id]
                            if existing_data != agent_data:
                                conflict_info = {
                                    "agent": agent_id,
                                    "mode": mode,
                                    "source1": "previous",
                                    "source2": str(source),
                                    "data1": existing_data,
                                    "data2": agent_data
                                }
                                consolidation_result["conflicts"].append(conflict_info)
                                logger.warning(f"⚠️  Coordinate conflict for {agent_id} in {mode}")
                        
                        # Use the latest source (override previous)
                        merged_coordinates[mode][agent_id] = agent_data
                        
            except Exception as e:
                logger.error(f"❌ Failed to load coordinates from {source}: {e}")
        
        # Save consolidated coordinates to primary location
        try:
            # Ensure config directory exists
            self.coordinates_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.coordinates_file, 'w') as f:
                json.dump(merged_coordinates, f, indent=2)
            
            self.coordinates = merged_coordinates
            consolidation_result["final_coordinates"] = merged_coordinates
            
            logger.info(f"✅ Consolidated coordinates saved to: {self.coordinates_file}")
            logger.info(f"📊 Final result: {len(merged_coordinates)} modes with {sum(len(agents) for agents in merged_coordinates.values())} total agent configurations")
            
        except Exception as e:
            logger.error(f"❌ Failed to save consolidated coordinates: {e}")
            
        return consolidation_result
    
    def set_agent_coordinates(self, agent_id: str, mode: str, coordinate_data: CoordinateData) -> bool:
        """Set coordinates for a specific agent in a specific mode"""
        try:
            if mode not in self.coordinates:
                self.coordinates[mode] = {}
            
            # Convert CoordinateData to the expected format
            self.coordinates[mode][agent_id] = {
                "input_box": {
                    "x": coordinate_data.input_box[0],
                    "y": coordinate_data.input_box[1]
                },
                "starter_location_box": {
                    "x": coordinate_data.starter_location[0],
                    "y": coordinate_data.starter_location[1]
                }
            }
            
            # Save to file
            self._save_coordinates()
            return True
            
        except Exception as e:
            logger.error(f"❌ Error setting coordinates for {agent_id} in {mode} mode: {e}")
            return False
    
    def _save_coordinates(self) -> None:
        """Save coordinates to file"""
        try:
            # Ensure config directory exists
            self.coordinates_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.coordinates_file, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            
            logger.info(f"✅ Coordinates saved to: {self.coordinates_file}")
            
        except Exception as e:
            logger.error(f"❌ Failed to save coordinates: {e}")
            raise
