#!/usr/bin/env python3
"""
Enhanced Enter-Press Coordinate Calibration (V1 Copied)
======================================================
Calibrate 5-agent coordinates by pressing Enter when ready
instead of using countdown timers. Includes backup restoration
and enhanced coordinate validation.
"""

import json
import time
import sys
from pathlib import Path
from typing import Dict, Tuple, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = True
except ImportError:
    print("❌ PyAutoGUI not installed. Install with: pip install pyautogui")
    sys.exit(1)

class EnhancedEnterPressCalibrator:
    """Enhanced coordinate calibration using Enter key with backup restoration"""
    
    def __init__(self):
        self.coord_file = Path("../runtime/agent_comms/cursor_agent_coords.json")
        self.backup_file = Path("../runtime/agent_comms/cursor_agent_coords_backup.json")
        self.current_coords = {}
        self.new_coords = {}
        self.min_distance = 50  # Minimum distance between agent coordinates
        
        # Load current coordinates
        self.load_current_coordinates()
    
    def load_current_coordinates(self):
        """Load current coordinate configuration"""
        try:
            if self.coord_file.exists():
                with open(self.coord_file, 'r') as f:
                    self.current_coords = json.load(f)
                print("✅ Current coordinates loaded")
            else:
                print("❌ Coordinate file not found")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Error loading coordinates: {e}")
            sys.exit(1)
    
    def backup_current_coordinates(self):
        """Create backup of current coordinates"""
        try:
            import shutil
            shutil.copy2(self.coord_file, self.backup_file)
            print(f"✅ Current coordinates backed up to {self.backup_file}")
        except Exception as e:
            print(f"⚠️ Warning: Could not create backup: {e}")
    
    def restore_backup_coordinates(self):
        """Restore coordinates from backup"""
        try:
            if not self.backup_file.exists():
                print("❌ No backup file found to restore from")
                return False
            
            # Load backup coordinates
            with open(self.backup_file, 'r') as f:
                backup_coords = json.load(f)
            
            # Create new backup of current state before restoring
            current_backup = Path("../runtime/agent_comms/cursor_agent_coords_current_backup.json")
            import shutil
            shutil.copy2(self.coord_file, current_backup)
            print(f"✅ Current coordinates backed up to {current_backup}")
            
            # Restore from backup
            self.current_coords["5-agent"] = backup_coords["5-agent"]
            
            # Save restored coordinates
            with open(self.coord_file, 'w') as f:
                json.dump(self.current_coords, f, indent=2)
            
            print("✅ Backup coordinates restored successfully!")
            print(f"📁 Restored to: {self.coord_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error restoring backup: {e}")
            return False
    
    def show_coordinate_comparison(self):
        """Show comparison between current and backup coordinates"""
        try:
            if not self.backup_file.exists():
                print("❌ No backup file found for comparison")
                return
            
            with open(self.backup_file, 'r') as f:
                backup_coords = json.load(f)
            
            print("\n📊 COORDINATE COMPARISON (Current vs Backup)")
            print("=" * 70)
            
            if "5-agent" not in self.current_coords or "5-agent" not in backup_coords:
                print("❌ Cannot compare - missing 5-agent configuration")
                return
            
            current_5agent = self.current_coords["5-agent"]
            backup_5agent = backup_coords["5-agent"]
            
            for agent_name in backup_5agent.keys():
                print(f"\n🤖 {agent_name}:")
                
                # Current coordinates
                if agent_name in current_5agent:
                    current = current_5agent[agent_name]
                    print(f"   Current Starter: ({current.get('starter_location_box', {}).get('x', 'N/A')}, {current.get('starter_location_box', {}).get('y', 'N/A')})")
                    print(f"   Current Resume Input:  ({current.get('resume_input_box', {}).get('x', 'N/A')}, {current.get('resume_input_box', {}).get('y', 'N/A')})")
                else:
                    print("   Current: Not configured")
                
                # Backup coordinates
                backup = backup_5agent[agent_name]
                print(f"   Backup Starter: ({backup.get('starter_location_box', {}).get('x', 'N/A')}, {backup.get('starter_location_box', {}).get('y', 'N/A')})")
                print(f"   Backup Resume Input:  ({backup.get('resume_input_box', {}).get('x', 'N/A')}, {backup.get('resume_input_box', {}).get('y', 'N/A')})")
                
        except Exception as e:
            print(f"❌ Error showing coordinate comparison: {e}")
    
    def get_agent_layout(self) -> Dict[str, str]:
        """Get 5-agent layout description with better positioning guidance"""
        return {
            "Agent-1": "Top Left (upper left quadrant)",
            "Agent-2": "Top Right (upper right quadrant)", 
            "Agent-3": "Bottom Left (lower left quadrant)",
            "Agent-4": "Bottom Right (lower right quadrant)",
            "Agent-5": "Center/Right (middle area)"
        }
    
    def calculate_distance(self, coord1: Dict, coord2: Dict) -> float:
        """Calculate distance between two coordinates"""
        dx = coord1['x'] - coord2['x']
        dy = coord1['y'] - coord2['y']
        return (dx**2 + dy**2)**0.5
    
    def validate_coordinate_separation(self, new_coord: Dict, agent_name: str) -> bool:
        """Validate that new coordinate is sufficiently separated from others"""
        for existing_agent, existing_coords in self.new_coords.items():
            if existing_agent == agent_name:
                continue
            
            # Check starter location separation
            if 'starter_location_box' in existing_coords:
                distance = self.calculate_distance(new_coord['starter_location_box'], 
                                                existing_coords['starter_location_box'])
                if distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} starter location too close to {existing_agent}")
                    print(f"   Distance: {distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
            
            # Check resume input box separation
            if 'resume_input_box' in existing_coords:
                distance = self.calculate_distance(new_coord['resume_input_box'], 
                                                existing_coords['resume_input_box'])
                if distance < self.min_distance:
                    print(f"⚠️  Warning: {agent_name} resume input box too close to {existing_agent}")
                    print(f"   Distance: {distance:.1f} pixels (minimum: {self.min_distance})")
                    return False
        
        return True
    
    def calibrate_agent_coordinates(self, agent_name: str, position: str):
        """Calibrate coordinates for a specific agent using Enter key"""
        print(f"\n🎯 Calibrating {agent_name} ({position})")
        print("=" * 60)
        print(f"📱 Position: {position}")
        print("💡 Make sure this is a DIFFERENT area from other agents!")
        print("=" * 60)
        
        # Calibrate starter location
        print(f"📍 Position your mouse where {agent_name} should click to start a new chat")
        print("   (This should be in the TOP area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   Take your time to position it exactly where you want...")
        print("   When ready, press ENTER to capture the coordinates")
        
        input("   Press ENTER when mouse is positioned for starter location...")
        
        starter_x, starter_y = pyautogui.position()
        print(f"✅ Starter location captured: ({starter_x}, {starter_y})")
        
        # Calibrate resume input box
        print(f"\n⌨️  Position your mouse where {agent_name} should type messages")
        print("   (This should be in the BOTTOM area of this agent's chat window)")
        print("   ⚠️  IMPORTANT: Make sure this is NOT the same area as other agents!")
        print("   Take your time to position it exactly where you want...")
        print("   When ready, press ENTER to capture the coordinates")
        
        input("   Press ENTER when mouse is positioned for resume input box...")
        
        input_x, input_y = pyautogui.position()
        print(f"✅ Resume input box captured: ({input_x}, {input_y})")
        
        # Store coordinates
        agent_coords = {
            "starter_location_box": {"x": starter_x, "y": starter_y},
            "resume_input_box": {"x": input_x, "y": input_y}
        }
        
        # Validate separation
        if self.validate_coordinate_separation(agent_coords, agent_name):
            self.new_coords[agent_name] = agent_coords
            print(f"✅ {agent_name} coordinates calibrated and validated!")
        else:
            print(f"⚠️  {agent_name} coordinates may be too close to other agents")
            print("   Consider recalibrating this agent with more separation")
            
            # Ask if user wants to continue or recalibrate
            response = input("Continue anyway? (y/N): ").strip().lower()
            if response == 'y':
                self.new_coords[agent_name] = agent_coords
                print(f"✅ {agent_name} coordinates saved (with warning)")
            else:
                print(f"🔄 Recalibrating {agent_name}...")
                return self.calibrate_agent_coordinates(agent_name, position)
    
    def run_calibration(self):
        """Run the Enter-press calibration process"""
        print("🚀 ENHANCED ENTER-PRESS 5-AGENT COORDINATE CALIBRATION")
        print("=" * 70)
        print("This will recalibrate coordinates for all 5 agents")
        print("⚠️  CRITICAL: Each agent must have DISTINCT coordinates!")
        print("💡 You can take your time and press ENTER when ready")
        print("Make sure your Cursor is in 5-agent mode and visible")
        print("=" * 70)
        
        # Show current layout
        layout = self.get_agent_layout()
        print("\n📱 5-Agent Layout Guide:")
        for agent, position in layout.items():
            print(f"   {agent}: {position}")
        
        print(f"\n📏 Minimum separation between agents: {self.min_distance} pixels")
        print("💡 This ensures agents don't interfere with each other")
        
        # Backup current coordinates
        self.backup_current_coordinates()
        
        # Confirm before starting
        print(f"\n⚠️  This will update coordinates in: {self.coord_file}")
        response = input("Continue with Enter-press calibration? (y/N): ").strip().lower()
        if response != 'y':
            print("❌ Calibration cancelled")
            return
        
        print("\n🎯 Starting Enter-press calibration process...")
        print("Position your mouse over DISTINCT locations for each agent")
        print("Press ENTER when ready to capture each coordinate")
        print("Use Ctrl+C to cancel at any time")
        
        try:
            # Calibrate each agent
            for agent_name, position in layout.items():
                self.calibrate_agent_coordinates(agent_name, position)
                
                # Show current progress
                print(f"\n📊 Progress: {len(self.new_coords)}/5 agents calibrated")
                
                # Small break between agents
                if agent_name != "Agent-5":
                    print("\n⏳ Moving to next agent...")
                    print("💡 Remember: Each agent needs DISTINCT coordinates!")
                    input("Press ENTER when ready for next agent...")
            
            # Save new coordinates
            self.save_new_coordinates()
            
            # Show coordinate summary
            self.show_coordinate_summary()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Calibration interrupted by user")
            print("No changes were saved")
            return
        except Exception as e:
            print(f"\n❌ Calibration error: {e}")
            return
    
    def save_new_coordinates(self):
        """Save new coordinates to file"""
        try:
            # Update 5-agent section with new coordinates
            self.current_coords["5-agent"] = self.new_coords
            
            # Save to file
            with open(self.coord_file, 'w') as f:
                json.dump(self.current_coords, f, indent=2)
            
            print(f"\n✅ New coordinates saved to {self.coord_file}")
            
        except Exception as e:
            print(f"❌ Error saving coordinates: {e}")
            sys.exit(1)
    
    def show_coordinate_summary(self):
        """Show detailed coordinate summary with separation analysis"""
        print("\n📊 COORDINATE CALIBRATION SUMMARY")
        print("=" * 70)
        
        # Show all coordinates
        for agent_name in self.new_coords.keys():
            coords = self.new_coords[agent_name]
            print(f"\n🤖 {agent_name}:")
            print(f"   📍 Starter: ({coords['starter_location_box']['x']}, {coords['starter_location_box']['y']})")
            print(f"   ⌨️  Resume Input:  ({coords['resume_input_box']['x']}, {coords['resume_input_box']['y']})")
        
        # Analyze separation
        print(f"\n🔍 COORDINATE SEPARATION ANALYSIS:")
        print(f"   Minimum required separation: {self.min_distance} pixels")
        
        all_good = True
        for i, agent1 in enumerate(self.new_coords.keys()):
            for j, agent2 in enumerate(self.new_coords.keys()):
                if i >= j:
                    continue
                
                coords1 = self.new_coords[agent1]
                coords2 = self.new_coords[agent2]
                
                # Check starter locations
                starter_distance = self.calculate_distance(
                    coords1['starter_location_box'], 
                    coords2['starter_location_box']
                )
                
                # Check resume input boxes
                input_distance = self.calculate_distance(
                    coords1['resume_input_box'], 
                    coords2['resume_input_box']
                )
                
                if starter_distance < self.min_distance:
                    print(f"   ⚠️  {agent1} ↔ {agent2} starters: {starter_distance:.1f}px")
                    all_good = False
                else:
                    print(f"   ✅ {agent1} ↔ {agent2} starters: {starter_distance:.1f}px")
                
                if input_distance < self.min_distance:
                    print(f"   ⚠️  {agent1} ↔ {agent2} resume inputs: {input_distance:.1f}px")
                    all_good = False
                else:
                    print(f"   ✅ {agent1} ↔ {agent2} resume inputs: {input_distance:.1f}px")
        
        print("\n" + "=" * 70)
        if all_good:
            print("🎉 ALL COORDINATES PROPERLY SEPARATED!")
            print("✅ Your 5-agent mode is ready for reliable communication")
        else:
            print("⚠️  SOME COORDINATES MAY BE TOO CLOSE")
            print("💡 Consider recalibrating agents with insufficient separation")
        
        print("\n📋 Next steps:")
        print("1. Test coordinates: python test_calibrated_coordinates.py")
        print("2. If issues persist, run calibration again")
        print("3. Restore backup if needed: python restore_coordinate_backup.py")
    
    def show_main_menu(self):
        """Show main menu with all available options"""
        while True:
            print("\n" + "=" * 70)
            print("🎯 ENHANCED COORDINATE CALIBRATION SYSTEM")
            print("=" * 70)
            print("1. 🚀 Run Full 5-Agent Calibration")
            print("2. 📊 Show Current vs Backup Comparison")
            print("3. 🔄 Restore from Backup")
            print("4. 📋 Show Current Coordinates")
            print("5. 🚪 Exit")
            print("=" * 70)
            
            choice = input("Select an option (1-5): ").strip()
            
            if choice == "1":
                self.run_calibration()
            elif choice == "2":
                self.show_coordinate_comparison()
            elif choice == "3":
                if self.restore_backup_coordinates():
                    print("✅ Backup restored successfully!")
                else:
                    print("❌ Failed to restore backup")
            elif choice == "4":
                self.show_current_coordinates()
            elif choice == "5":
                print("👋 Exiting coordinate calibration system")
                break
            else:
                print("❌ Invalid choice. Please select 1-5.")
    
    def show_current_coordinates(self):
        """Show current coordinate configuration"""
        print("\n📋 CURRENT COORDINATE CONFIGURATION")
        print("=" * 60)
        
        if "5-agent" not in self.current_coords:
            print("❌ No 5-agent configuration found")
            return
        
        for agent_name, coords in self.current_coords["5-agent"].items():
            print(f"\n🤖 {agent_name}:")
            print(f"   📍 Starter: ({coords['starter_location_box']['x']}, {coords['starter_location_box']['y']})")
            print(f"   ⌨️  Resume Input:  ({coords['resume_input_box']['x']}, {coords['resume_input_box']['y']})")

def main():
    """Main calibration function"""
    try:
        calibrator = EnhancedEnterPressCalibrator()
        
        # Check if command line argument is provided
        if len(sys.argv) > 1 and sys.argv[1] == "--menu":
            calibrator.show_main_menu()
        else:
            # Default behavior: run calibration directly
            calibrator.run_calibration()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Calibration cancelled")
        return 1
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
