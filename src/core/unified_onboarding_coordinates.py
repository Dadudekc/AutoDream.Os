#!/usr/bin/env python3
"""
Unified Onboarding Coordinates - Consolidated coordinate management
================================================================

Consolidates get_onboarding_coordinates functions from multiple files.
V2 compliant: ≤400 lines, focused responsibility
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class UnifiedOnboardingCoordinates:
    """Unified onboarding coordinates management."""
    
    def __init__(self, coord_path: str = "config/coordinates.json"):
        """Initialize unified onboarding coordinates."""
        self.coord_path = Path(coord_path)
        self.coordinates: Dict[str, Dict[str, int]] = {}
        self._load_coordinates()
        
        logger.info("Unified onboarding coordinates initialized")
    
    def _load_coordinates(self) -> None:
        """Load coordinates from configuration file."""
        try:
            if self.coord_path.exists():
                with open(self.coord_path, 'r') as f:
                    self.coordinates = json.load(f)
                logger.info(f"Loaded coordinates for {len(self.coordinates)} agents")
            else:
                logger.warning(f"Coordinates file not found: {self.coord_path}")
        except Exception as e:
            logger.error(f"Failed to load coordinates: {e}")
            self.coordinates = {}
    
    def get_onboarding_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get onboarding coordinates for a specific agent."""
        try:
            if agent_id not in self.coordinates:
                logger.warning(f"No coordinates found for agent: {agent_id}")
                return None
            
            agent_coords = self.coordinates[agent_id]
            
            # Check for input coordinates first, then fallback to chat coordinates
            if 'input_x' in agent_coords and 'input_y' in agent_coords:
                coords = (agent_coords['input_x'], agent_coords['input_y'])
                logger.debug(f"Using input coordinates for {agent_id}: {coords}")
                return coords
            elif 'chat_x' in agent_coords and 'chat_y' in agent_coords:
                coords = (agent_coords['chat_x'], agent_coords['chat_y'])
                logger.debug(f"Using chat coordinates for {agent_id}: {coords}")
                return coords
            else:
                logger.warning(f"Incomplete coordinates for {agent_id}: {agent_coords}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get onboarding coordinates for {agent_id}: {e}")
            return None
    
    def get_chat_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get chat coordinates for a specific agent."""
        try:
            if agent_id not in self.coordinates:
                logger.warning(f"No coordinates found for agent: {agent_id}")
                return None
            
            agent_coords = self.coordinates[agent_id]
            
            if 'chat_x' in agent_coords and 'chat_y' in agent_coords:
                coords = (agent_coords['chat_x'], agent_coords['chat_y'])
                logger.debug(f"Using chat coordinates for {agent_id}: {coords}")
                return coords
            else:
                logger.warning(f"No chat coordinates for {agent_id}: {agent_coords}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get chat coordinates for {agent_id}: {e}")
            return None
    
    def get_input_coordinates(self, agent_id: str) -> Optional[Tuple[int, int]]:
        """Get input coordinates for a specific agent."""
        try:
            if agent_id not in self.coordinates:
                logger.warning(f"No coordinates found for agent: {agent_id}")
                return None
            
            agent_coords = self.coordinates[agent_id]
            
            if 'input_x' in agent_coords and 'input_y' in agent_coords:
                coords = (agent_coords['input_x'], agent_coords['input_y'])
                logger.debug(f"Using input coordinates for {agent_id}: {coords}")
                return coords
            else:
                logger.warning(f"No input coordinates for {agent_id}: {agent_coords}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get input coordinates for {agent_id}: {e}")
            return None
    
    def set_coordinates(self, agent_id: str, coord_type: str, x: int, y: int) -> bool:
        """Set coordinates for a specific agent."""
        try:
            if agent_id not in self.coordinates:
                self.coordinates[agent_id] = {}
            
            self.coordinates[agent_id][f"{coord_type}_x"] = x
            self.coordinates[agent_id][f"{coord_type}_y"] = y
            
            # Save to file
            self._save_coordinates()
            
            logger.info(f"Set {coord_type} coordinates for {agent_id}: ({x}, {y})")
            return True
            
        except Exception as e:
            logger.error(f"Failed to set coordinates for {agent_id}: {e}")
            return False
    
    def _save_coordinates(self) -> None:
        """Save coordinates to configuration file."""
        try:
            self.coord_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.coord_path, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            logger.debug("Coordinates saved to file")
        except Exception as e:
            logger.error(f"Failed to save coordinates: {e}")
    
    def get_all_agents(self) -> List[str]:
        """Get list of all agent IDs with coordinates."""
        return list(self.coordinates.keys())
    
    def get_agent_coordinates(self, agent_id: str) -> Optional[Dict[str, int]]:
        """Get all coordinates for a specific agent."""
        return self.coordinates.get(agent_id)
    
    def validate_coordinates(self) -> Dict[str, List[str]]:
        """Validate all coordinates and return issues."""
        issues = {}
        
        for agent_id, coords in self.coordinates.items():
            agent_issues = []
            
            # Check for required coordinate types
            required_types = ['chat', 'input']
            for coord_type in required_types:
                if f"{coord_type}_x" not in coords or f"{coord_type}_y" not in coords:
                    agent_issues.append(f"Missing {coord_type} coordinates")
                else:
                    x, y = coords[f"{coord_type}_x"], coords[f"{coord_type}_y"]
                    if not isinstance(x, int) or not isinstance(y, int):
                        agent_issues.append(f"Invalid {coord_type} coordinate types")
                    elif x < 0 or y < 0:
                        agent_issues.append(f"Negative {coord_type} coordinates")
            
            if agent_issues:
                issues[agent_id] = agent_issues
        
        return issues
    
    def get_coordinate_summary(self) -> Dict[str, Any]:
        """Get summary of all coordinates."""
        summary = {
            'total_agents': len(self.coordinates),
            'agents_with_complete_coords': 0,
            'coordinate_types': set(),
            'validation_issues': self.validate_coordinates()
        }
        
        for agent_id, coords in self.coordinates.items():
            # Count coordinate types
            for key in coords.keys():
                if key.endswith('_x') or key.endswith('_y'):
                    coord_type = key[:-2]
                    summary['coordinate_types'].add(coord_type)
            
            # Check if agent has complete coordinates
            has_chat = 'chat_x' in coords and 'chat_y' in coords
            has_input = 'input_x' in coords and 'input_y' in coords
            
            if has_chat and has_input:
                summary['agents_with_complete_coords'] += 1
        
        summary['coordinate_types'] = list(summary['coordinate_types'])
        return summary
    
    def backup_coordinates(self, backup_path: str = None) -> bool:
        """Create backup of coordinates."""
        try:
            if backup_path is None:
                backup_path = f"{self.coord_path}.backup"
            
            backup_file = Path(backup_path)
            with open(backup_file, 'w') as f:
                json.dump(self.coordinates, f, indent=2)
            
            logger.info(f"Coordinates backed up to: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to backup coordinates: {e}")
            return False
    
    def restore_coordinates(self, backup_path: str) -> bool:
        """Restore coordinates from backup."""
        try:
            backup_file = Path(backup_path)
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            with open(backup_file, 'r') as f:
                self.coordinates = json.load(f)
            
            # Save to main file
            self._save_coordinates()
            
            logger.info(f"Coordinates restored from: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore coordinates: {e}")
            return False


# Global instance for easy access
_unified_coordinates = None


def get_unified_onboarding_coordinates() -> UnifiedOnboardingCoordinates:
    """Get global unified onboarding coordinates instance."""
    global _unified_coordinates
    if _unified_coordinates is None:
        _unified_coordinates = UnifiedOnboardingCoordinates()
    return _unified_coordinates


def get_onboarding_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Convenience function to get onboarding coordinates."""
    return get_unified_onboarding_coordinates().get_onboarding_coordinates(agent_id)


def get_chat_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Convenience function to get chat coordinates."""
    return get_unified_onboarding_coordinates().get_chat_coordinates(agent_id)


def get_input_coordinates(agent_id: str) -> Optional[Tuple[int, int]]:
    """Convenience function to get input coordinates."""
    return get_unified_onboarding_coordinates().get_input_coordinates(agent_id)


if __name__ == "__main__":
    # Test the unified coordinates system
    coords = get_unified_onboarding_coordinates()
    
    print("=== Unified Onboarding Coordinates Test ===")
    print(f"Total agents: {len(coords.get_all_agents())}")
    print(f"Summary: {coords.get_coordinate_summary()}")
    
    # Test getting coordinates for each agent
    for agent_id in coords.get_all_agents():
        onboarding_coords = coords.get_onboarding_coordinates(agent_id)
        chat_coords = coords.get_chat_coordinates(agent_id)
        input_coords = coords.get_input_coordinates(agent_id)
        
        print(f"\n{agent_id}:")
        print(f"  Onboarding: {onboarding_coords}")
        print(f"  Chat: {chat_coords}")
        print(f"  Input: {input_coords}")
