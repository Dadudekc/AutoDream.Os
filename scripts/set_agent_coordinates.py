from ..core.unified_entry_point_system import main
#!/usr/bin/env python3
"""
Agent Coordinate Management Script
=================================

Interactive script to set, update, and manage agent coordinates for PyAutoGUI messaging.
Supports both chat_input_coordinates and onboarding_input_coords.

Author: Agent-4 - Strategic Oversight & Emergency Intervention Manager
"""

import time

# Add src to path for imports
sys.path.insert(0, str(get_unified_utility().Path(__file__).parent.parent / "src"))

try:
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False

class AgentCoordinateManager:
    """Manages agent coordinates for PyAutoGUI messaging system."""
    
    def __init__(self, coords_file: str = "cursor_agent_coords.json"):
        self.coords_file = coords_file
        self.coords_data = self.load_coordinates()
        
    def load_coordinates(self) -> Dict:
        """Load existing coordinates from file."""
        if get_unified_utility().path.exists(self.coords_file):
            try:
                with open(self.coords_file, "r") as f:
                    return read_json(f)
            except Exception as e:
                get_logger(__name__).info(f"❌ Error loading coordinates: {e}")
                return self.get_default_structure()
        else:
            get_logger(__name__).info(f"📝 Creating new coordinate file: {self.coords_file}")
            return self.get_default_structure()
    
    def get_default_structure(self) -> Dict:
        """Get default coordinate structure."""
        return {
            "description": "Agent coordinate configuration - Single Source of Truth for all agent coordinates",
            "version": "2.0.0",
            "last_updated": datetime.now().isoformat() + "Z",
            "coordinate_system": {
                "origin": "top-left",
                "unit": "pixels",
                "max_resolution": "3840x2160",
                "note": "Coordinates are screen-relative (0,0 = top-left corner) - FIXED COORDINATES (must not change)"
            },
            "agents": {
                "Agent-1": {
                    "chat_input_coordinates": [-1269, 481],
                    "onboarding_input_coords": [-1269, 481],
                    "description": "Integration & Core Systems Specialist",
                    "active": True
                },
                "Agent-2": {
                    "chat_input_coordinates": [-308, 480],
                    "onboarding_input_coords": [-308, 480],
                    "description": "Architecture & Design Specialist",
                    "active": True
                },
                "Agent-3": {
                    "chat_input_coordinates": [-1269, 1001],
                    "onboarding_input_coords": [-1269, 1001],
                    "description": "Infrastructure & DevOps Specialist",
                    "active": True
                },
                "Agent-4": {
                    "chat_input_coordinates": [-308, 1000],
                    "onboarding_input_coords": [-308, 1000],
                    "description": "Quality Assurance Specialist (CAPTAIN)",
                    "active": True
                },
                "Agent-5": {
                    "chat_input_coordinates": [652, 421],
                    "onboarding_input_coords": [652, 421],
                    "description": "Business Intelligence Specialist",
                    "active": True
                },
                "Agent-6": {
                    "chat_input_coordinates": [1612, 419],
                    "onboarding_input_coords": [1612, 419],
                    "description": "Coordination & Communication Specialist",
                    "active": True
                },
                "Agent-7": {
                    "chat_input_coordinates": [653, 940],
                    "onboarding_input_coords": [653, 940],
                    "description": "Web Development Specialist",
                    "active": True
                },
                "Agent-8": {
                    "chat_input_coordinates": [1611, 941],
                    "onboarding_input_coords": [1611, 941],
                    "description": "SSOT & System Integration Specialist",
                    "active": True
                }
            },
            "fallback_behavior": {
                "on_coordinate_failure": "fallback_to_inbox",
                "inbox_delivery": True,
                "notification_on_fallback": True
            },
            "validation_rules": {
                "min_x": -2000,
                "min_y": 0,
                "max_x": 2000,
                "max_y": 1200,
                "require_positive": False,
                "note": "Allow negative coordinates for multi-monitor setups"
            }
        }
    
    def save_coordinates(self) -> bool:
        """Save coordinates to file."""
        try:
            self.coords_data["last_updated"] = datetime.now().isoformat() + "Z"
            with open(self.coords_file, "w") as f:
                write_json(self.coords_data, f, indent=2)
            get_logger(__name__).info(f"✅ Coordinates saved to {self.coords_file}")
            return True
        except Exception as e:
            get_logger(__name__).info(f"❌ Error saving coordinates: {e}")
            return False
    
    def show_coordinates(self):
        """Display current coordinates."""
        get_logger(__name__).info("🎯 Current Agent Coordinates")
        get_logger(__name__).info("=" * 50)
        
        for agent_id, agent_data in self.coords_data["agents"].items():
            chat_coords = agent_data["chat_input_coordinates"]
            onboarding_coords = agent_data["onboarding_input_coords"]
            description = agent_data["description"]
            active = "🟢" if agent_data["active"] else "🔴"
            
            get_logger(__name__).info(f"{active} {agent_id}: {description}")
            get_logger(__name__).info(f"   Chat Input: {chat_coords}")
            get_logger(__name__).info(f"   Onboarding: {onboarding_coords}")
            get_logger(__name__).info()
    
    def set_agent_coordinates(self, agent_id: str, chat_coords: Tuple[int, int], 
                            onboarding_coords: Optional[Tuple[int, int]] = None) -> bool:
        """Set coordinates for a specific agent."""
        if agent_id not in self.coords_data["agents"]:
            get_logger(__name__).info(f"❌ Agent {agent_id} not found")
            return False
        
        # Validate coordinates
        if not self.validate_coordinates(chat_coords):
            get_logger(__name__).info(f"❌ Invalid chat coordinates: {chat_coords}")
            return False
        
        if onboarding_coords and not self.validate_coordinates(onboarding_coords):
            get_logger(__name__).info(f"❌ Invalid onboarding coordinates: {onboarding_coords}")
            return False
        
        # Update coordinates
        self.coords_data["agents"][agent_id]["chat_input_coordinates"] = list(chat_coords)
        if onboarding_coords:
            self.coords_data["agents"][agent_id]["onboarding_input_coords"] = list(onboarding_coords)
        else:
            # Default onboarding coords to chat coords if not specified
            self.coords_data["agents"][agent_id]["onboarding_input_coords"] = list(chat_coords)
        
        get_logger(__name__).info(f"✅ Updated coordinates for {agent_id}")
        get_logger(__name__).info(f"   Chat Input: {chat_coords}")
        get_logger(__name__).info(f"   Onboarding: {onboarding_coords or chat_coords}")
        return True
    
    def validate_coordinates(self, coords: Tuple[int, int]) -> bool:
        """Validate coordinate values."""
        x, y = coords
        rules = self.coords_data["validation_rules"]
        
        if not (rules["min_x"] <= x <= rules["max_x"]):
            return False
        if not (rules["min_y"] <= y <= rules["max_y"]):
            return False
        
        return True
    
    def interactive_setup(self):
        """Interactive coordinate setup."""
        get_logger(__name__).info("🎯 Interactive Agent Coordinate Setup")
        get_logger(__name__).info("=" * 50)
        get_logger(__name__).info("This will help you set coordinates for each agent.")
        get_logger(__name__).info("You can use a tool like 'Mouse Position' to get exact coordinates.")
        get_logger(__name__).info()
        
        for agent_id in self.coords_data["agents"].keys():
            get_logger(__name__).info(f"Setting coordinates for {agent_id}...")
            
            # Get chat input coordinates
            while True:
                try:
                    chat_input = input(f"Enter chat input coordinates for {agent_id} (x,y): ").strip()
                    if not get_unified_validator().validate_required(chat_input):
                        get_logger(__name__).info("Using existing coordinates...")
                        break
                    
                    x, y = map(int, chat_input.split(","))
                    chat_coords = (x, y)
                    
                    if self.validate_coordinates(chat_coords):
                        break
                    else:
                        get_logger(__name__).info("❌ Invalid coordinates. Please try again.")
                except ValueError:
                    get_logger(__name__).info("❌ Invalid format. Use x,y (e.g., -1269,481)")
            
            # Get onboarding coordinates
            while True:
                try:
                    onboarding_input = input(f"Enter onboarding coordinates for {agent_id} (x,y) [Enter to use chat coords]: ").strip()
                    if not get_unified_validator().validate_required(onboarding_input):
                        onboarding_coords = None
                        break
                    
                    x, y = map(int, onboarding_input.split(","))
                    onboarding_coords = (x, y)
                    
                    if self.validate_coordinates(onboarding_coords):
                        break
                    else:
                        get_logger(__name__).info("❌ Invalid coordinates. Please try again.")
                except ValueError:
                    get_logger(__name__).info("❌ Invalid format. Use x,y (e.g., -1269,481)")
            
            # Update coordinates
            if chat_input:
                self.set_agent_coordinates(agent_id, chat_coords, onboarding_coords)
            
            get_logger(__name__).info()
        
        # Save changes
        if input("Save changes? (y/N): ").lower() == 'y':
            self.save_coordinates()
        else:
            get_logger(__name__).info("Changes not saved.")
    
    def get_current_cursor_position(self) -> Tuple[int, int]:
        """Get current cursor position."""
        if not get_unified_validator().validate_required(PYAUTOGUI_AVAILABLE):
            get_logger(__name__).info("❌ PyAutoGUI not available. Install with: pip install pyautogui")
            return (0, 0)
        
        try:
            return pyautogui.position()
        except Exception as e:
            get_logger(__name__).info(f"❌ Error getting cursor position: {e}")
            return (0, 0)
    
    def capture_coordinate_interactive(self, agent_id: str, coord_type: str = "chat") -> Optional[Tuple[int, int]]:
        """Capture coordinate by hovering cursor and pressing Enter."""
        if not get_unified_validator().validate_required(PYAUTOGUI_AVAILABLE):
            get_logger(__name__).info("❌ PyAutoGUI not available for coordinate capture")
            return None
        
        if not get_unified_validator().validate_required(KEYBOARD_AVAILABLE):
            get_logger(__name__).info("❌ Keyboard module not available. Install with: pip install keyboard")
            return None
        
        get_logger(__name__).info(f"\n🎯 Capturing {coord_type} coordinates for {agent_id}")
        get_logger(__name__).info(f"📝 {self.coords_data['agents'][agent_id]['description']}")
        get_logger(__name__).info("\n📍 INSTRUCTIONS:")
        get_logger(__name__).info(f"1. Hover your cursor over the agent's {coord_type} input field")
        get_logger(__name__).info("2. Press ENTER to capture the coordinates")
        get_logger(__name__).info("3. Press ESC to skip this coordinate")
        get_logger(__name__).info("4. Press Q to quit the tool")
        get_logger(__name__).info("\n⏳ Waiting for input...")
        
        while True:
            try:
                # Get current cursor position for display
                x, y = self.get_current_cursor_position()
                get_logger(__name__).info(f"\r📍 Current cursor: [{x}, {y}] - Press ENTER to capture, ESC to skip, Q to quit", end="", flush=True)
                
                # Check for key presses
                if keyboard.is_pressed('enter'):
                    time.sleep(0.1)  # Debounce
                    final_x, final_y = self.get_current_cursor_position()
                    get_logger(__name__).info(f"\n✅ Captured {coord_type} coordinates for {agent_id}: [{final_x}, {final_y}]")
                    return (final_x, final_y)
                
                elif keyboard.is_pressed('esc'):
                    time.sleep(0.1)  # Debounce
                    get_logger(__name__).info(f"\n⏭️  Skipped {coord_type} coordinates for {agent_id}")
                    return None
                
                elif keyboard.is_pressed('q'):
                    time.sleep(0.1)  # Debounce
                    get_logger(__name__).info(f"\n🛑 Quitting coordinate capture")
                    return "quit"
                
                time.sleep(0.05)  # Small delay to prevent high CPU usage
                
            except KeyboardInterrupt:
                get_logger(__name__).info(f"\n🛑 Interrupted by user")
                return "quit"
    
    def capture_all_coordinates_interactive(self):
        """Interactive coordinate capture for all agents."""
        if not PYAUTOGUI_AVAILABLE or not KEYBOARD_AVAILABLE:
            get_logger(__name__).info("❌ Required dependencies not available:")
            if not get_unified_validator().validate_required(PYAUTOGUI_AVAILABLE):
                get_logger(__name__).info("   - PyAutoGUI: pip install pyautogui")
            if not get_unified_validator().validate_required(KEYBOARD_AVAILABLE):
                get_logger(__name__).info("   - Keyboard: pip install keyboard")
            return
        
        get_logger(__name__).info("🚀 Interactive Coordinate Capture Tool")
        get_logger(__name__).info("=" * 50)
        get_logger(__name__).info("This tool will help you capture coordinates for all agents.")
        get_logger(__name__).info("Make sure your agent chat windows are visible and positioned correctly.")
        get_logger(__name__).info("\nPress Ctrl+C at any time to quit.")
        
        captured_count = 0
        skipped_count = 0
        
        # PHASE 1: Capture all chat coordinates first
        get_logger(__name__).info("\n" + "="*60)
        get_logger(__name__).info("🎯 PHASE 1: CAPTURING CHAT INPUT COORDINATES")
        get_logger(__name__).info("="*60)
        get_logger(__name__).info("We'll capture chat input coordinates for all agents first.")
        get_logger(__name__).info("These are the coordinates used for regular messaging.")
        
        for agent_id in self.coords_data["agents"].keys():
            get_logger(__name__).info(f"\n{'='*20} {agent_id} {'='*20}")
            
            # Check if agent already has chat coordinates
            existing_chat = self.coords_data["agents"][agent_id].get("chat_input_coordinates")
            
            if existing_chat:
                get_logger(__name__).info(f"📍 {agent_id} already has chat coordinates: {existing_chat}")
                response = input("Do you want to update chat coordinates? (y/n): ").lower().strip()
                if response == 'y':
                    result = self.capture_coordinate_interactive(agent_id, "chat")
                    if result == "quit":
                        get_logger(__name__).info("\n🛑 Chat coordinate capture cancelled by user")
                        return
                    elif result is not None:
                        self.coords_data["agents"][agent_id]["chat_input_coordinates"] = list(result)
                        captured_count += 1
                else:
                    skipped_count += 1
            else:
                result = self.capture_coordinate_interactive(agent_id, "chat")
                if result == "quit":
                    get_logger(__name__).info("\n🛑 Chat coordinate capture cancelled by user")
                    return
                elif result is not None:
                    self.coords_data["agents"][agent_id]["chat_input_coordinates"] = list(result)
                    captured_count += 1
                else:
                    skipped_count += 1
        
        # PHASE 2: Capture all onboarding coordinates
        get_logger(__name__).info("\n" + "="*60)
        get_logger(__name__).info("🎯 PHASE 2: CAPTURING ONBOARDING INPUT COORDINATES")
        get_logger(__name__).info("="*60)
        get_logger(__name__).info("Now we'll capture onboarding input coordinates for all agents.")
        get_logger(__name__).info("These are the coordinates used for the hard onboarding process.")
        get_logger(__name__).info("You can use the same coordinates as chat, or set different ones.")
        
        for agent_id in self.coords_data["agents"].keys():
            get_logger(__name__).info(f"\n{'='*20} {agent_id} {'='*20}")
            
            # Get the chat coordinates we just captured
            chat_coords = self.coords_data["agents"][agent_id].get("chat_input_coordinates")
            existing_onboarding = self.coords_data["agents"][agent_id].get("onboarding_input_coords")
            
            get_logger(__name__).info(f"📍 Chat coordinates: {chat_coords}")
            if existing_onboarding:
                get_logger(__name__).info(f"📍 Current onboarding coordinates: {existing_onboarding}")
            
            # Ask if they want different onboarding coordinates
            response = input("Do you want different onboarding coordinates? (y/n): ").lower().strip()
            if response == 'y':
                result = self.capture_coordinate_interactive(agent_id, "onboarding")
                if result == "quit":
                    get_logger(__name__).info("\n🛑 Onboarding coordinate capture cancelled by user")
                    break
                elif result is not None:
                    self.coords_data["agents"][agent_id]["onboarding_input_coords"] = list(result)
                else:
                    # Use chat coordinates for onboarding
                    self.coords_data["agents"][agent_id]["onboarding_input_coords"] = chat_coords
            else:
                # Use chat coordinates for onboarding
                self.coords_data["agents"][agent_id]["onboarding_input_coords"] = chat_coords
                get_logger(__name__).info(f"✅ Using chat coordinates for onboarding: {chat_coords}")
        
        # Save coordinates
        if captured_count > 0:
            self.save_coordinates()
            get_logger(__name__).info(f"\n🎉 Coordinate capture completed!")
            get_logger(__name__).info(f"✅ Captured: {captured_count} chat coordinates")
            get_logger(__name__).info(f"⏭️  Skipped: {skipped_count} chat coordinates")
            get_logger(__name__).info(f"📋 All agents now have both chat and onboarding coordinates configured")
        else:
            get_logger(__name__).info(f"\n📝 No coordinates were captured")
    
    def bulk_update_from_file(self, file_path: str):
        """Bulk update coordinates from a CSV or JSON file."""
        get_logger(__name__).info(f"📁 Loading coordinates from {file_path}")
        # Implementation for bulk updates from file
        pass



if __name__ == "__main__":
    main()
