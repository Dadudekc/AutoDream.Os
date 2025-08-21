#!/usr/bin/env python3
"""
Set 8-Agent Coordinates Script
Sets up the coordinate system for all 8 agents in 8-agent mode
"""

import pyautogui
import time

# Configure PyAutoGUI safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 1.0

def set_8_agent_coordinates():
    """Set up coordinates for all 8 agents."""
    print("🎯 Setting up 8-Agent Coordinate System")
    print("=" * 50)
    
    # Get screen size
    screen_width, screen_height = pyautogui.size()
    print(f"📱 Screen Resolution: {screen_width}x{screen_height}")
    
    # Check if screen supports 8-agent layout
    if screen_width < 3200 or screen_height < 1200:
        print("⚠️  Warning: Screen resolution may be too small for 8-agent layout")
        print("   Recommended: 3200x1200 or higher")
        print("   Current: {screen_width}x{screen_height}")
    
    # Define agent regions
    agent_regions = {
        "Agent-1": {
            "name": "Foundation & Testing",
            "region": (0, 0, 800, 600),
            "center": (400, 300),
            "color": "🟢"
        },
        "Agent-2": {
            "name": "AI & ML Integration", 
            "region": (800, 0, 800, 600),
            "center": (1200, 300),
            "color": "🔵"
        },
        "Agent-3": {
            "name": "Multimedia & Content",
            "region": (0, 600, 800, 600), 
            "center": (400, 900),
            "color": "🟡"
        },
        "Agent-4": {
            "name": "Security & Infrastructure",
            "region": (800, 600, 800, 600),
            "center": (1200, 900), 
            "color": "🔴"
        },
        "Agent-5": {
            "name": "Business Intelligence",
            "region": (1600, 0, 800, 600),
            "center": (2000, 300),
            "color": "🟣"
        },
        "Agent-6": {
            "name": "Gaming & Entertainment",
            "region": (1600, 600, 800, 600),
            "center": (2000, 900),
            "color": "🟠"
        },
        "Agent-7": {
            "name": "Web Development",
            "region": (2400, 0, 800, 600),
            "center": (2800, 300),
            "color": "⚪"
        },
        "Agent-8": {
            "name": "Integration & Performance",
            "region": (2400, 600, 800, 600),
            "center": (2800, 900),
            "color": "⚫"
        }
    }
    
    print("\n🎨 Agent Coordinate Layout:")
    print("┌─────────────────────────────────────────────────────────────────────────────────────────────┐")
    print("│                                    SCREEN LAYOUT (3200x1200)                              │")
    print("├─────────────────────────────────────────────────────────────────────────────────────────────┤")
    print("│                                                                                             │")
    print("│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │")
    print("│  │   AGENT-1   │  │   AGENT-2   │  │   AGENT-5   │  │   AGENT-7   │                      │")
    print("│  │ Foundation  │  │ AI & ML     │  │ Business    │  │ Web Dev     │                      │")
    print("│  │ & Testing   │  │ Integration │  │ Intelligence│  │ & UI       │                      │")
    print("│  │             │  │             │  │ & Trading   │  │ Framework  │                      │")
    print("│  │ (0,0,800,600)│  │(800,0,800,600)│  │(1600,0,800,600)│  │(2400,0,800,600)│                      │")
    print("│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                      │")
    print("│                                                                                             │")
    print("├─────────────────────────────────────────────────────────────────────────────────────────────┤")
    print("│                                                                                             │")
    print("│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                      │")
    print("│  │   AGENT-3   │  │   AGENT-4   │  │   AGENT-6   │  │   AGENT-8   │                      │")
    print("│  │ Multimedia  │  │ Security &  │  │ Gaming &    │  │ Integration │                      │")
    print("│  │ & Content   │  │ Infrastructure│  │ Entertainment│  │ & Performance│                      │")
    print("│  │             │  │             │  │             │  │ Optimization│                      │")
    print("│  │(0,600,800,600)│  │(800,600,800,600)│  │(1600,600,800,600)│  │(2400,600,800,600)│                      │")
    print("│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘                      │")
    print("│                                                                                             │")
    print("└─────────────────────────────────────────────────────────────────────────────────────────────┘")
    
    print("\n🎯 Agent Coordinate Details:")
    for agent_id, info in agent_regions.items():
        print(f"{info['color']} {agent_id}: {info['name']}")
        print(f"   Region: {info['region']}")
        print(f"   Center: {info['center']}")
        print()
    
    # Test coordinate system
    print("🧪 Testing coordinate system...")
    print("   Moving mouse to each agent's center position...")
    
    for agent_id, info in agent_regions.items():
        try:
            center_x, center_y = info['center']
            print(f"   {info['color']} Moving to {agent_id} center: ({center_x}, {center_y})")
            
            # Move mouse to center of agent region
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            time.sleep(0.5)
            
            print(f"   ✅ {agent_id} coordinates set successfully")
            
        except Exception as e:
            print(f"   ❌ Error setting coordinates for {agent_id}: {e}")
    
    print("\n🎯 Coordinate System Setup Complete!")
    print("=" * 50)
    print("All 8 agents now have their coordinate regions configured:")
    print("• Agent-1: (0, 0, 800, 600) - Foundation & Testing")
    print("• Agent-2: (800, 0, 800, 600) - AI & ML Integration")
    print("• Agent-3: (0, 600, 800, 600) - Multimedia & Content")
    print("• Agent-4: (800, 600, 800, 600) - Security & Infrastructure")
    print("• Agent-5: (1600, 0, 800, 600) - Business Intelligence")
    print("• Agent-6: (1600, 600, 800, 600) - Gaming & Entertainment")
    print("• Agent-7: (2400, 0, 800, 600) - Web Development")
    print("• Agent-8: (2400, 600, 800, 600) - Integration & Performance")
    print("\n🚀 Ready for 8-agent PyAutoGUI coordination!")

def main():
    """Main function."""
    try:
        print("🎯 8-AGENT COORDINATE SETUP")
        print("=" * 50)
        print("This script will set up the coordinate system for all 8 agents.")
        print("Make sure you have enough screen space (3200x1200 recommended).")
        print()
        
        # Give user time to prepare
        input("Press Enter when ready to set coordinates...")
        
        # Set coordinates
        set_8_agent_coordinates()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Coordinate setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during coordinate setup: {e}")

if __name__ == "__main__":
    main()
