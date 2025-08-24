#!/usr/bin/env python3
"""
Interactive Coordinate Capture Module
===================================
Provides interactive coordinate capture functionality for the unified messaging system.
Follows V2 coding standards with SRP, clean interfaces, and modularity.
"""

import json
import sys

from src.utils.stability_improvements import stability_manager, safe_import
from pathlib import Path
from typing import Dict, Tuple, Optional, List
from abc import ABC, abstractmethod

try:
    import pyautogui
    pyautogui.FAILSAFE = True
except ImportError:
    pyautogui = None

from .interfaces import CoordinateData, CoordinateCaptureInterface
from .coordinate_manager import CoordinateManager


class InteractiveCoordinateCapture(CoordinateCaptureInterface):
    """
    Interactive coordinate capture using mouse positioning and Enter key.
    Follows V2 coding standards with SRP and clean interfaces.
    """
    
    def __init__(self, coordinate_manager: CoordinateManager):
        self.coordinate_manager = coordinate_manager
        self.min_distance = 50  # Minimum distance between agent coordinates
        
        if not pyautogui:
            raise ImportError("PyAutoGUI is required for interactive coordinate capture")
    
    def capture_agent_coordinates(self, agent_name: str, mode: str = "8-agent") -> Optional[CoordinateData]:
        """
        Capture coordinates for a specific agent interactively.
        
        Args:
            agent_name: Name of the agent (e.g., "Agent-1")
            mode: Coordinate mode (e.g., "8-agent", "5-agent")
            
        Returns:
            CoordinateData object if successful, None otherwise
        """
        try:
            print(f"\n🎯 Capturing coordinates for {agent_name} ({mode} mode)")
            print("=" * 60)
            
            # Capture starter location
            starter_coords = self._capture_starter_location(agent_name)
            if not starter_coords:
                return None
            
            # Capture input box location
            input_coords = self._capture_input_box_location(agent_name)
            if not input_coords:
                return None
            
            # Create coordinate data
            coordinate_data = CoordinateData(
                agent_id=agent_name,
                mode=mode,
                input_box=starter_coords,
                starter_location=input_coords
            )
            
            # Validate separation from existing coordinates
            if self._validate_coordinate_separation(coordinate_data, agent_name, mode):
                print(f"✅ {agent_name} coordinates captured and validated!")
                return coordinate_data
            else:
                print(f"⚠️ {agent_name} coordinates may be too close to other agents")
                response = input("Continue anyway? (y/N): ").strip().lower()
                if response == 'y':
                    return coordinate_data
                else:
                    return None
                    
        except Exception as e:
            print(f"❌ Error capturing coordinates for {agent_name}: {e}")
            return None
    
    def _capture_starter_location(self, agent_name: str) -> Optional[Tuple[int, int]]:
        """Capture starter location coordinates"""
        print(f"📍 Position your mouse where {agent_name} should click to start a new chat")
        print("   (This should be in the TOP area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   Take your time to position it exactly where you want...")
        print("   When ready, press ENTER to capture the coordinates")
        
        try:
            input("   Press ENTER when mouse is positioned for starter location...")
            x, y = pyautogui.position()
            print(f"✅ Starter location captured: ({x}, {y})")
            return (x, y)
        except KeyboardInterrupt:
            print("   ⏭️ Starter location capture cancelled")
            return None
    
    def _capture_input_box_location(self, agent_name: str) -> Optional[Tuple[int, int]]:
        """Capture input box coordinates"""
        print(f"\n⌨️  Position your mouse where {agent_name} should type messages")
        print("   (This should be in the BOTTOM area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   Take your time to position it exactly where you want...")
        print("   When ready, press ENTER to capture the coordinates")
        
        try:
            input("   Press ENTER when mouse is positioned for input box...")
            x, y = pyautogui.position()
            print(f"✅ Input box captured: ({x}, {y})")
            return (x, y)
        except KeyboardInterrupt:
            print("   ⏭️ Input box capture cancelled")
            return None
    
    def _validate_coordinate_separation(self, new_coords: CoordinateData, agent_name: str, mode: str) -> bool:
        """Validate that new coordinates are sufficiently separated from existing ones"""
        try:
            existing_agents = self.coordinate_manager.get_agents_in_mode(mode)
            if not existing_agents:
                return True  # No existing coordinates to compare against
            
            for existing_agent in existing_agents:
                if existing_agent == agent_name:
                    continue
                
                existing_coords = self.coordinate_manager.get_agent_coordinates(existing_agent, mode)
                if not existing_coords:
                    continue
                
                # Check starter location separation
                starter_distance = self._calculate_distance(
                    new_coords.starter_location, 
                    existing_coords.starter_location
                )
                if starter_distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} starter location too close to {existing_agent}")
                    print(f"   Distance: {starter_distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
                
                # Check input box separation
                input_distance = self._calculate_distance(
                    new_coords.input_box, 
                    existing_coords.input_box
                )
                if input_distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} input box too close to {existing_agent}")
                    print(f"   Distance: {input_distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
            
            return True
            
        except Exception as e:
            print(f"⚠️  Warning: Could not validate coordinate separation: {e}")
            return True  # Allow if validation fails
    
    def _calculate_distance(self, coord1: Tuple[int, int], coord2: Tuple[int, int]) -> float:
        """Calculate distance between two coordinates"""
        dx = coord1[0] - coord2[0]
        dy = coord1[1] - coord2[1]
        return (dx**2 + dy**2)**0.5


class InteractiveCoordinateCaptureService:
    """
    Service class for managing interactive coordinate capture operations.
    Follows V2 coding standards with SRP and dependency injection.
    """
    
    def __init__(self, coordinate_manager: CoordinateManager):
        self.coordinate_manager = coordinate_manager
        self.capture_interface = InteractiveCoordinateCapture(coordinate_manager)
    
    def run_full_calibration(self, mode: str = "8-agent") -> bool:
        """
        Run full interactive calibration for all agents in a mode.
        Two-phase approach: starter locations first, then input boxes.
        
        Args:
            mode: Coordinate mode to calibrate
            
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"🚀 INTERACTIVE COORDINATE CALIBRATION - {mode.upper()} MODE")
            print("=" * 70)
            print("This will calibrate coordinates for all agents in this mode")
            print("🔄 TWO-PHASE APPROACH:")
            print("   Phase 1: Capture STARTER locations for ALL agents")
            print("   Phase 2: Capture INPUT BOX locations for ALL agents")
            print("⚠️  CRITICAL: Each agent must have DISTINCT coordinates!")
            print("💡 You can take your time and press ENTER when ready")
            print("Make sure your Cursor is in the correct mode and visible")
            print("=" * 70)
            
            # Get available agents for this mode
            available_agents = self.coordinate_manager.get_agents_in_mode(mode)
            if not available_agents:
                print(f"❌ No agents found for {mode} mode")
                return False
            
            print(f"\n📱 {mode.upper()} Mode Layout Guide:")
            for i, agent in enumerate(available_agents, 1):
                print(f"   {agent}: Position {i}")
            
            print(f"\n📏 Minimum separation between agents: {self.capture_interface.min_distance} pixels")
            print("💡 This ensures agents don't interfere with each other")
            
            # Confirm before starting
            response = input(f"\n⚠️  This will update coordinates for {mode} mode. Continue? (y/N): ").strip().lower()
            if response != 'y':
                print("❌ Calibration cancelled")
                return False
            
            print(f"\n🎯 Starting TWO-PHASE interactive calibration for {mode} mode...")
            print("Use Ctrl+C to cancel at any time")
            
            try:
                # PHASE 1: Capture starter locations for ALL agents
                starter_coordinates = self._capture_all_starter_locations(available_agents, mode)
                if not starter_coordinates:
                    print("❌ Failed to capture starter locations")
                    return False
                
                # PHASE 2: Capture input box locations for ALL agents
                input_coordinates = self._capture_all_input_locations(available_agents, mode)
                if not input_coordinates:
                    print("❌ Failed to capture input box locations")
                    return False
                
                # Combine coordinates
                captured_coordinates = self._combine_coordinates(starter_coordinates, input_coordinates, mode)
                
                # Save captured coordinates
                if captured_coordinates:
                    self._save_captured_coordinates(captured_coordinates, mode)
                    self._show_calibration_summary(captured_coordinates, mode)
                    return True
                else:
                    print("❌ No coordinates were captured")
                    return False
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Calibration interrupted by user")
                print("No changes were saved")
                return False
                
        except Exception as e:
            print(f"\n❌ Calibration error: {e}")
            return False
    
    def _capture_all_starter_locations(self, agents: List[str], mode: str) -> Dict[str, Tuple[int, int]]:
        """Phase 1: Capture starter locations for all agents"""
        print(f"\n🏁 PHASE 1: STARTER LOCATIONS FOR ALL AGENTS")
        print("=" * 60)
        print("📍 Position your mouse where each agent should click to START a new chat")
        print("   (This should be in the TOP area of each agent's chat window)")
        print("=" * 60)
        
        starter_coords = {}
        
        for i, agent_name in enumerate(agents, 1):
            print(f"\n🎯 [{i}/{len(agents)}] Capturing STARTER location for {agent_name}")
            print(f"📍 Position your mouse where {agent_name} should click to start a new chat")
            print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
            print("   Take your time to position it exactly where you want...")
            
            try:
                input("   Press ENTER when mouse is positioned for STARTER location...")
                x, y = pyautogui.position()
                starter_coords[agent_name] = (x, y)
                print(f"✅ {agent_name} starter location captured: ({x}, {y})")
                
                # Small break between agents (except for the last one)
                if i < len(agents):
                    print("   ⏳ Moving to next agent...")
                    
            except KeyboardInterrupt:
                print(f"   ⏭️ Skipping {agent_name}")
                
        print(f"\n🏁 PHASE 1 COMPLETE: {len(starter_coords)}/{len(agents)} starter locations captured")
        return starter_coords
    
    def _capture_all_input_locations(self, agents: List[str], mode: str) -> Dict[str, Tuple[int, int]]:
        """Phase 2: Capture input box locations for all agents"""
        print(f"\n⌨️  PHASE 2: INPUT BOX LOCATIONS FOR ALL AGENTS")
        print("=" * 60)
        print("⌨️  Position your mouse where each agent should TYPE messages")
        print("   (This should be in the BOTTOM area of each agent's chat window)")
        print("=" * 60)
        
        input_coords = {}
        
        for i, agent_name in enumerate(agents, 1):
            print(f"\n🎯 [{i}/{len(agents)}] Capturing INPUT BOX location for {agent_name}")
            print(f"⌨️  Position your mouse where {agent_name} should type messages")
            print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
            print("   Take your time to position it exactly where you want...")
            
            try:
                input("   Press ENTER when mouse is positioned for INPUT BOX...")
                x, y = pyautogui.position()
                input_coords[agent_name] = (x, y)
                print(f"✅ {agent_name} input box captured: ({x}, {y})")
                
                # Small break between agents (except for the last one)
                if i < len(agents):
                    print("   ⏳ Moving to next agent...")
                    
            except KeyboardInterrupt:
                print(f"   ⏭️ Skipping {agent_name}")
                
        print(f"\n⌨️  PHASE 2 COMPLETE: {len(input_coords)}/{len(agents)} input box locations captured")
        return input_coords
    
    def _combine_coordinates(self, starter_coords: Dict[str, Tuple[int, int]], 
                            input_coords: Dict[str, Tuple[int, int]], mode: str) -> Dict[str, CoordinateData]:
        """Combine starter and input coordinates into CoordinateData objects"""
        from .coordinate_manager import CoordinateData
        
        combined_coords = {}
        
        # Only create coordinates for agents that have both starter and input coordinates
        for agent_name in starter_coords:
            if agent_name in input_coords:
                combined_coords[agent_name] = CoordinateData(
                    agent_id=agent_name,
                    mode=mode,
                    starter_location=starter_coords[agent_name],
                    input_box=input_coords[agent_name]
                )
            else:
                print(f"⚠️  Warning: {agent_name} missing input box coordinates")
        
        return combined_coords
    
    def _save_captured_coordinates(self, coordinates: Dict[str, CoordinateData], mode: str) -> None:
        """Save captured coordinates to the coordinate manager"""
        try:
            for agent_name, coord_data in coordinates.items():
                self.coordinate_manager.set_agent_coordinates(agent_name, mode, coord_data)
            
            print(f"\n✅ All coordinates saved for {mode} mode")
            
        except Exception as e:
            print(f"❌ Error saving coordinates: {e}")
            raise
    
    def _show_calibration_summary(self, coordinates: Dict[str, CoordinateData], mode: str) -> None:
        """Show detailed calibration summary"""
        print(f"\n📊 COORDINATE CALIBRATION SUMMARY - {mode.upper()} MODE")
        print("=" * 70)
        
        # Show all coordinates
        for agent_name, coords in coordinates.items():
            print(f"\n🤖 {agent_name}:")
            print(f"   📍 Starter: {coords.starter_location}")
            print(f"   ⌨️  Input Box: {coords.input_box}")
        
        print(f"\n🎉 CALIBRATION COMPLETE!")
        print(f"✅ Your {mode} mode is ready for reliable communication")
        print(f"\n📋 Next steps:")
        print(f"1. Test coordinates: python -m src.services.messaging --coordinates")
        print(f"2. Send test message: python -m src.services.messaging --mode pyautogui --agent {list(coordinates.keys())[0]} --message 'Test'")
