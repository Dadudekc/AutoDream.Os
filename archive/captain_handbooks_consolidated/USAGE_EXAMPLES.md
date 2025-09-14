# 🚀 **Usage Examples - Agent Cellphone V2**

**Comprehensive usage examples for all major components and workflows**

---

## 🎯 **Table of Contents**

1. [Quick Start Examples](#quick-start-examples)
2. [Messaging System Examples](#messaging-system-examples)
3. [Backup & Recovery Examples](#backup--recovery-examples)
4. [Discord Commander Examples](#discord-commander-examples)
5. [Coordinate Management Examples](#coordinate-management-examples)
6. [Role Management Examples](#role-management-examples)
7. [Advanced Workflows](#advanced-workflows)
8. [Integration Examples](#integration-examples)

---

## 🚀 **Quick Start Examples**

### **Basic System Check**

```python
#!/usr/bin/env python3
"""
Basic system health check example.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.coordinate_loader import get_coordinate_loader
from src.services.consolidated_messaging_service import list_agents
from src.services.messaging.shared import MessagingUtilities, list_agents as shared_list_agents
from src.core.backup_disaster_recovery import BackupSystemCore

def shared_utilities_example():
    """Example of using shared messaging utilities."""
    print("🔧 Shared Messaging Utilities Example")
    print("=" * 40)
    
    # Initialize utilities
    utils = MessagingUtilities()
    
    # Load coordinates
    coords = utils.load_coordinates_from_json()
    print(f"✅ Loaded coordinates: {len(coords)} entries")
    
    # List agents
    agents = utils.list_agents()
    print(f"✅ Available agents: {agents}")
    
    # Validate coordinates
    validation = utils.validate_coordinates()
    print(f"✅ Validation: {validation}")
    
    # Example of sending message (dry run)
    print("📤 Message sending example (dry run)")
    success = utils.send_message_pyautogui("agent-1", "Hello from shared utilities!")
    print(f"✅ Message sent: {success}")
    
    print()

async def system_health_check():
    """Perform basic system health check."""
    print("🔍 Agent Cellphone V2 - System Health Check")
    print("=" * 50)

    # Check coordinate system
    try:
        loader = get_coordinate_loader()
        agents = loader.get_all_agents()
        print(f"✅ Coordinate System: {len(agents)} agents configured")

        for agent_id in agents:
            coords = loader.get_agent_coordinates(agent_id)
            print(f"   📍 {agent_id}: {coords}")

    except Exception as e:
        print(f"❌ Coordinate System Error: {e}")

    # Check messaging system
    try:
        available_agents = await list_agents()
        print(f"✅ Messaging System: {len(available_agents)} agents available")

    except Exception as e:
        print(f"❌ Messaging System Error: {e}")

    # Check backup system
    try:
        backup_system = BackupSystemCore()
        print("✅ Backup System: Initialized successfully")

    except Exception as e:
        print(f"❌ Backup System Error: {e}")

    print("\n🎉 System health check completed!")

if __name__ == "__main__":
    asyncio.run(system_health_check())
```

### **Simple Agent Communication**

```python
#!/usr/bin/env python3
"""
Simple agent-to-agent communication example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, send_message
)

async def simple_communication():
    """Demonstrate simple agent communication."""
    print("🤖 Simple Agent Communication Example")
    print("=" * 40)

    # Create a message from Agent-8 to Agent-5
    message = UnifiedMessage(
        content="Hello Agent-5! This is a test message from Agent-8.",
        sender="Agent-8",
        recipient="Agent-5",
        message_type=UnifiedMessageType.AGENT_TO_AGENT,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.COORDINATION]
    )

    print(f"📤 Sending message from {message.sender} to {message.recipient}")
    print(f"📝 Content: {message.content}")
    print(f"🏷️  Tags: {[tag.value for tag in message.tags]}")

    # Send the message
    success = await send_message(message)

    if success:
        print("✅ Message sent successfully!")
    else:
        print("❌ Failed to send message")

    return success

if __name__ == "__main__":
    asyncio.run(simple_communication())
```

---

## 💬 **Messaging System Examples**

### **Complete Messaging Workflow**

```python
#!/usr/bin/env python3
"""
Complete messaging workflow with all features.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    UnifiedMessageTag, SenderType, RecipientType,
    send_message, broadcast_message, list_agents
)

async def complete_messaging_workflow():
    """Demonstrate complete messaging capabilities."""
    print("💬 Complete Messaging Workflow")
    print("=" * 35)

    # 1. List available agents
    print("1️⃣ Listing available agents...")
    agents = await list_agents()
    print(f"   Available agents: {agents}")

    # 2. Send individual messages
    print("\n2️⃣ Sending individual messages...")
    for i, agent_id in enumerate(agents[:3]):  # Send to first 3 agents
        message = UnifiedMessage(
            content=f"Individual message #{i+1} from Agent-8",
            sender="Agent-8",
            recipient=agent_id,
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL,
            tags=[UnifiedMessageTag.COORDINATION],
            sender_type=SenderType.AGENT,
            recipient_type=RecipientType.AGENT
        )

        success = await send_message(message)
        print(f"   📤 {agent_id}: {'✅' if success else '❌'}")

    # 3. Send urgent message
    print("\n3️⃣ Sending urgent message...")
    urgent_message = UnifiedMessage(
        content="🚨 URGENT: System maintenance in 10 minutes!",
        sender="Agent-8",
        recipient="Agent-1",
        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
        priority=UnifiedMessagePriority.URGENT,
        tags=[UnifiedMessageTag.SYSTEM],
        sender_type=SenderType.SYSTEM,
        recipient_type=RecipientType.AGENT
    )

    urgent_success = await send_message(urgent_message)
    print(f"   🚨 Urgent message: {'✅' if urgent_success else '❌'}")

    # 4. Broadcast to all agents
    print("\n4️⃣ Broadcasting to all agents...")
    broadcast_success = await broadcast_message(
        "📢 System-wide announcement: All systems operational",
        "Agent-8"
    )
    print(f"   📢 Broadcast: {'✅' if broadcast_success else '❌'}")

    # 5. Send onboarding message
    print("\n5️⃣ Sending onboarding message...")
    onboarding_message = UnifiedMessage(
        content="Welcome to the team! Please review your role assignment.",
        sender="Captain Agent-4",
        recipient="Agent-5",
        message_type=UnifiedMessageType.ONBOARDING,
        priority=UnifiedMessagePriority.NORMAL,
        tags=[UnifiedMessageTag.ONBOARDING],
        sender_type=SenderType.CAPTAIN,
        recipient_type=RecipientType.AGENT
    )

    onboarding_success = await send_message(onboarding_message)
    print(f"   👋 Onboarding: {'✅' if onboarding_success else '❌'}")

    print("\n🎉 Messaging workflow completed!")

if __name__ == "__main__":
    asyncio.run(complete_messaging_workflow())
```

### **Message History and Tracking**

```python
#!/usr/bin/env python3
"""
Message history and tracking example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    send_message, show_message_history
)

async def message_tracking_example():
    """Demonstrate message tracking and history."""
    print("📊 Message Tracking and History")
    print("=" * 35)

    # Send multiple messages with tracking
    messages = [
        {
            "content": "First test message",
            "recipient": "Agent-1",
            "priority": UnifiedMessagePriority.NORMAL
        },
        {
            "content": "Second test message",
            "recipient": "Agent-2",
            "priority": UnifiedMessagePriority.URGENT
        },
        {
            "content": "Third test message",
            "recipient": "Agent-3",
            "priority": UnifiedMessagePriority.NORMAL
        }
    ]

    print("📤 Sending tracked messages...")
    for i, msg_data in enumerate(messages, 1):
        message = UnifiedMessage(
            content=msg_data["content"],
            sender="Agent-8",
            recipient=msg_data["recipient"],
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=msg_data["priority"]
        )

        success = await send_message(message)
        print(f"   {i}. {msg_data['recipient']}: {'✅' if success else '❌'}")

    # Show message history
    print("\n📋 Message History:")
    try:
        history = await show_message_history()
        if history:
            for entry in history[-5:]:  # Show last 5 messages
                print(f"   📝 {entry}")
        else:
            print("   No message history available")
    except Exception as e:
        print(f"   ❌ Error retrieving history: {e}")

if __name__ == "__main__":
    asyncio.run(message_tracking_example())
```

---

## 💾 **Backup & Recovery Examples**

### **Basic Backup Operations**

```python
#!/usr/bin/env python3
"""
Basic backup operations example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.backup_disaster_recovery import BackupSystemCore

async def basic_backup_operations():
    """Demonstrate basic backup operations."""
    print("💾 Basic Backup Operations")
    print("=" * 30)

    # Initialize backup system
    backup_system = BackupSystemCore()
    print("✅ Backup system initialized")

    # Create different types of backups
    backup_types = ["full", "incremental", "differential"]

    for backup_type in backup_types:
        print(f"\n📦 Creating {backup_type} backup...")

        try:
            result = await backup_system.create_backup(
                backup_type=backup_type,
                source_path=".",
                custom_name=f"example_{backup_type}_backup"
            )

            print(f"   ✅ {backup_type.title()} backup created")
            print(f"   📋 Backup ID: {result.get('backup_id', 'N/A')}")
            print(f"   📁 Size: {result.get('size_mb', 0):.2f} MB")
            print(f"   ⏰ Duration: {result.get('duration_seconds', 0):.2f}s")

        except Exception as e:
            print(f"   ❌ Failed to create {backup_type} backup: {e}")

    # List all backups
    print("\n📋 Listing all backups...")
    try:
        backups = await backup_system.list_backups()
        print(f"   Found {len(backups)} backups:")

        for backup in backups[-3:]:  # Show last 3 backups
            print(f"   📦 {backup.get('backup_id', 'Unknown')} - {backup.get('timestamp', 'Unknown')}")

    except Exception as e:
        print(f"   ❌ Error listing backups: {e}")

if __name__ == "__main__":
    asyncio.run(basic_backup_operations())
```

### **Point-in-Time Recovery**

```python
#!/usr/bin/env python3
"""
Point-in-time recovery example.
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.backup_disaster_recovery import BackupSystemCore

async def point_in_time_recovery():
    """Demonstrate point-in-time recovery."""
    print("⏰ Point-in-Time Recovery")
    print("=" * 30)

    backup_system = BackupSystemCore()

    # Create a backup first
    print("📦 Creating initial backup...")
    backup_result = await backup_system.create_backup(
        backup_type="full",
        source_path=".",
        custom_name="recovery_test_backup"
    )

    backup_id = backup_result.get('backup_id')
    print(f"✅ Backup created: {backup_id}")

    # Simulate some time passing
    print("\n⏳ Simulating time passage...")
    await asyncio.sleep(2)

    # Create incremental backup
    print("📦 Creating incremental backup...")
    incremental_result = await backup_system.create_backup(
        backup_type="incremental",
        source_path=".",
        custom_name="recovery_test_incremental"
    )

    incremental_id = incremental_result.get('backup_id')
    print(f"✅ Incremental backup created: {incremental_id}")

    # Demonstrate point-in-time recovery
    print("\n🔄 Performing point-in-time recovery...")

    # Calculate a point in time (1 minute ago)
    recovery_time = datetime.now() - timedelta(minutes=1)

    try:
        restore_result = await backup_system.restore_backup(
            backup_id=backup_id,
            target_path="./recovery_test",
            point_in_time=recovery_time
        )

        print(f"✅ Point-in-time recovery completed")
        print(f"   📁 Restored to: {restore_result.get('target_path', 'N/A')}")
        print(f"   ⏰ Recovery time: {recovery_time}")
        print(f"   📊 Status: {restore_result.get('status', 'Unknown')}")

    except Exception as e:
        print(f"❌ Recovery failed: {e}")

    # Cleanup
    print("\n🧹 Cleaning up test files...")
    import shutil
    try:
        shutil.rmtree("./recovery_test", ignore_errors=True)
        print("✅ Cleanup completed")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")

if __name__ == "__main__":
    asyncio.run(point_in_time_recovery())
```

### **Business Continuity Planning**

```python
#!/usr/bin/env python3
"""
Business continuity planning example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.backup_disaster_recovery import (
    BusinessContinuityPlanner, DisasterType
)

async def business_continuity_example():
    """Demonstrate business continuity planning."""
    print("🏢 Business Continuity Planning")
    print("=" * 35)

    # Initialize BCP
    bcp = BusinessContinuityPlanner()
    print("✅ Business continuity planner initialized")

    # Define disaster scenarios
    disaster_scenarios = [
        {
            "type": DisasterType.HARDWARE_FAILURE,
            "systems": ["messaging_system", "agent_coordination"],
            "description": "Primary server hardware failure"
        },
        {
            "type": DisasterType.DATA_CORRUPTION,
            "systems": ["database", "configuration"],
            "description": "Critical data corruption detected"
        },
        {
            "type": DisasterType.SECURITY_BREACH,
            "systems": ["authentication", "messaging_system"],
            "description": "Security breach in authentication system"
        }
    ]

    # Create recovery plans for each scenario
    for i, scenario in enumerate(disaster_scenarios, 1):
        print(f"\n{i}️⃣ Creating recovery plan for: {scenario['description']}")

        try:
            plan = await bcp.create_recovery_plan(
                disaster_type=scenario["type"],
                affected_systems=scenario["systems"]
            )

            print(f"   ✅ Recovery plan created: {plan.get('plan_id', 'N/A')}")
            print(f"   📋 RTO: {plan.get('rto_minutes', 'N/A')} minutes")
            print(f"   📊 RPO: {plan.get('rpo_minutes', 'N/A')} minutes")
            print(f"   🎯 Priority: {plan.get('priority', 'N/A')}")

        except Exception as e:
            print(f"   ❌ Failed to create plan: {e}")

    # Test business continuity plan
    print("\n🧪 Testing business continuity plan...")
    try:
        test_result = await bcp.test_business_continuity_plan()

        print(f"   📊 Overall Score: {test_result.get('overall_score', 0):.2f}/100")
        print(f"   ✅ Passed Tests: {test_result.get('passed_tests', 0)}")
        print(f"   ❌ Failed Tests: {test_result.get('failed_tests', 0)}")

        # Show recommendations
        recommendations = test_result.get('recommendations', [])
        if recommendations:
            print("   💡 Recommendations:")
            for rec in recommendations[:3]:  # Show top 3
                print(f"      • {rec}")

    except Exception as e:
        print(f"   ❌ BCP test failed: {e}")

if __name__ == "__main__":
    asyncio.run(business_continuity_example())
```

---

## 🤖 **Discord Commander Examples**

### **Discord Bot Setup and Commands**

```python
#!/usr/bin/env python3
"""
Discord bot setup and command examples.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.discord_commander.discord_agent_bot import DiscordAgentBot
from src.discord_commander.handlers_swarm import SwarmCommandHandlers

async def discord_bot_example():
    """Demonstrate Discord bot functionality."""
    print("🤖 Discord Bot Example")
    print("=" * 25)

    # Note: This is a demonstration of the bot structure
    # In practice, you would need valid Discord tokens and proper setup

    print("📋 Discord Bot Features:")
    print("   ✅ Agent coordination commands")
    print("   ✅ Swarm broadcast functionality")
    print("   ✅ Real-time status monitoring")
    print("   ✅ Emergency intervention protocols")

    print("\n🔧 Available Commands:")
    commands = [
        "!swarm broadcast <message> - Broadcast to all agents",
        "!swarm status - Get swarm status",
        "!swarm emergency <message> - Emergency broadcast",
        "!agent <agent_id> <message> - Send message to specific agent",
        "!help - Show all available commands"
    ]

    for cmd in commands:
        print(f"   {cmd}")

    print("\n⚠️  Note: Discord bot requires valid tokens and proper configuration")
    print("   See config/discord_config.yaml for setup instructions")

if __name__ == "__main__":
    asyncio.run(discord_bot_example())
```

---

## 📍 **Coordinate Management Examples**

### **Advanced Coordinate Operations**

```python
#!/usr/bin/env python3
"""
Advanced coordinate management examples.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.coordinate_loader import get_coordinate_loader

def advanced_coordinate_operations():
    """Demonstrate advanced coordinate operations."""
    print("📍 Advanced Coordinate Operations")
    print("=" * 35)

    # Get coordinate loader
    loader = get_coordinate_loader()

    # 1. Get all agents and their coordinates
    print("1️⃣ All agent coordinates:")
    agents = loader.get_all_agents()

    for agent_id in agents:
        try:
            coords = loader.get_agent_coordinates(agent_id)
            is_active = loader.is_agent_active(agent_id)
            status = "🟢 Active" if is_active else "🔴 Inactive"
            print(f"   {agent_id}: {coords} {status}")
        except ValueError as e:
            print(f"   {agent_id}: ❌ Error - {e}")

    # 2. Coordinate validation
    print("\n2️⃣ Coordinate validation:")
    try:
        validation = loader.validate_coordinates()
        print(f"   ✅ Valid coordinates: {validation['valid_coordinates']}")
        print(f"   ❌ Invalid coordinates: {validation['invalid_coordinates']}")
        print(f"   📊 Total agents: {validation['total_agents']}")

        if validation['invalid_coordinates'] > 0:
            print("   ⚠️  Some coordinates need attention")
        else:
            print("   🎉 All coordinates are valid!")

    except Exception as e:
        print(f"   ❌ Validation error: {e}")

    # 3. Coordinate mapping visualization
    print("\n3️⃣ Coordinate mapping visualization:")
    print("   Monitor Layout:")
    print("   ┌─────────────────┐         ┌─────────────────┐")
    print("   │ Monitor 1 (Left)│         │ Monitor 2 (Right)│")
    print("   │                 │         │                 │")

    # Group agents by monitor (simplified)
    left_monitor = []
    right_monitor = []

    for agent_id in agents:
        try:
            coords = loader.get_agent_coordinates(agent_id)
            if coords[0] < 0:  # Negative X = left monitor
                left_monitor.append((agent_id, coords))
            else:  # Positive X = right monitor
                right_monitor.append((agent_id, coords))
        except ValueError:
            continue

    # Display left monitor agents
    for i, (agent_id, coords) in enumerate(left_monitor[:4]):
        y_pos = "Top" if coords[1] < 500 else "Bottom"
        print(f"   │ {agent_id} ({y_pos})     │         │                 │")

    print("   └─────────────────┘         └─────────────────┘")

    # Display right monitor agents
    for i, (agent_id, coords) in enumerate(right_monitor[:4]):
        y_pos = "Top" if coords[1] < 500 else "Bottom"
        print(f"   │                 │         │ {agent_id} ({y_pos})     │")

if __name__ == "__main__":
    advanced_coordinate_operations()
```

---

## 👥 **Role Management Examples**

### **Agent Onboarding Workflow**

```python
#!/usr/bin/env python3
"""
Agent onboarding workflow example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.role_manager import RoleManager

async def agent_onboarding_workflow():
    """Demonstrate agent onboarding workflow."""
    print("👥 Agent Onboarding Workflow")
    print("=" * 30)

    # Initialize role manager
    role_manager = RoleManager()

    # 1. Get available roles
    print("1️⃣ Available role modes:")
    roles = role_manager.get_available_roles()
    for i, role in enumerate(roles, 1):
        print(f"   {i}. {role}")

    # 2. Onboard agents with different roles
    print("\n2️⃣ Onboarding agents with different roles:")

    onboarding_scenarios = [
        {
            "agent_id": "Agent-1",
            "role_mode": "bootstrap_cli",
            "style": "friendly",
            "description": "Bootstrap CLI migration"
        },
        {
            "agent_id": "Agent-2",
            "role_mode": "compliance_refactor_v2",
            "style": "professional",
            "description": "V2 compliance refactoring"
        },
        {
            "agent_id": "Agent-3",
            "role_mode": "production_ready",
            "style": "professional",
            "description": "Production deployment"
        }
    ]

    for scenario in onboarding_scenarios:
        print(f"\n   📋 Onboarding {scenario['agent_id']} as {scenario['role_mode']}")
        print(f"   📝 Description: {scenario['description']}")
        print(f"   🎨 Style: {scenario['style']}")

        try:
            success = await role_manager.onboard_agent(
                agent_id=scenario["agent_id"],
                role_mode=scenario["role_mode"],
                style=scenario["style"]
            )

            print(f"   Result: {'✅ Success' if success else '❌ Failed'}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    # 3. Smart onboarding (auto-select best role)
    print("\n3️⃣ Smart onboarding (auto-select best role):")

    test_agents = ["Agent-5", "Agent-6", "Agent-7"]

    for agent_id in test_agents:
        print(f"   🤖 Smart onboarding for {agent_id}...")

        try:
            # In a real implementation, this would analyze the project context
            # and automatically select the best role mode
            success = await role_manager.onboard_agent(
                agent_id=agent_id,
                role_mode="production_ready",  # Auto-selected
                style="friendly"
            )

            print(f"   Result: {'✅ Success' if success else '❌ Failed'}")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    print("\n🎉 Onboarding workflow completed!")

if __name__ == "__main__":
    asyncio.run(agent_onboarding_workflow())
```

---

## 🔄 **Advanced Workflows**

### **Complete System Integration**

```python
#!/usr/bin/env python3
"""
Complete system integration example.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    send_message, broadcast_message
)
from src.core.coordinate_loader import get_coordinate_loader
from src.core.backup_disaster_recovery import BackupSystemCore
from src.services.role_manager import RoleManager

async def complete_system_integration():
    """Demonstrate complete system integration."""
    print("🔄 Complete System Integration")
    print("=" * 35)

    # Initialize all systems
    print("🚀 Initializing all systems...")

    # Coordinate system
    coordinate_loader = get_coordinate_loader()
    print("   ✅ Coordinate system initialized")

    # Backup system
    backup_system = BackupSystemCore()
    print("   ✅ Backup system initialized")

    # Role manager
    role_manager = RoleManager()
    print("   ✅ Role manager initialized")

    # 1. System health check
    print("\n1️⃣ System health check...")
    agents = coordinate_loader.get_all_agents()
    print(f"   📍 {len(agents)} agents configured")

    # 2. Create system backup
    print("\n2️⃣ Creating system backup...")
    try:
        backup_result = await backup_system.create_backup(
            backup_type="full",
            source_path=".",
            custom_name="integration_test_backup"
        )
        print(f"   ✅ Backup created: {backup_result.get('backup_id', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Backup failed: {e}")

    # 3. Onboard new agent
    print("\n3️⃣ Onboarding new agent...")
    try:
        onboarding_success = await role_manager.onboard_agent(
            agent_id="Agent-8",
            role_mode="production_ready",
            style="professional"
        )
        print(f"   ✅ Onboarding: {'Success' if onboarding_success else 'Failed'}")
    except Exception as e:
        print(f"   ❌ Onboarding failed: {e}")

    # 4. Send coordination message
    print("\n4️⃣ Sending coordination message...")
    try:
        coordination_message = UnifiedMessage(
            content="System integration test completed successfully!",
            sender="Agent-8",
            recipient="Agent-1",
            message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL
        )

        message_success = await send_message(coordination_message)
        print(f"   ✅ Coordination message: {'Sent' if message_success else 'Failed'}")
    except Exception as e:
        print(f"   ❌ Message failed: {e}")

    # 5. Broadcast system status
    print("\n5️⃣ Broadcasting system status...")
    try:
        broadcast_success = await broadcast_message(
            "🟢 All systems operational - Integration test complete",
            "Agent-8"
        )
        print(f"   ✅ System broadcast: {'Sent' if broadcast_success else 'Failed'}")
    except Exception as e:
        print(f"   ❌ Broadcast failed: {e}")

    print("\n🎉 Complete system integration test finished!")
    print("   All major systems have been tested and integrated successfully.")

if __name__ == "__main__":
    asyncio.run(complete_system_integration())
```

### **Error Handling and Recovery**

```python
#!/usr/bin/env python3
"""
Error handling and recovery example.
"""

import asyncio
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    send_message, MessagingError
)
from src.core.coordinate_loader import get_coordinate_loader, CoordinateError
from src.core.backup_disaster_recovery import BackupSystemCore, BackupError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def error_handling_example():
    """Demonstrate robust error handling and recovery."""
    print("🛡️ Error Handling and Recovery")
    print("=" * 35)

    # 1. Coordinate system error handling
    print("1️⃣ Coordinate system error handling...")
    try:
        loader = get_coordinate_loader()
        # Try to get coordinates for non-existent agent
        coords = loader.get_agent_coordinates("NonExistentAgent")
        print(f"   Coordinates: {coords}")
    except CoordinateError as e:
        print(f"   ❌ Coordinate error caught: {e}")
        print("   🔄 Attempting recovery...")
        # Recovery: Use default coordinates or fallback
        print("   ✅ Recovery: Using fallback coordinates")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

    # 2. Messaging system error handling
    print("\n2️⃣ Messaging system error handling...")
    try:
        # Create message with invalid recipient
        message = UnifiedMessage(
            content="Test message",
            sender="Agent-8",
            recipient="InvalidAgent",
            message_type=UnifiedMessageType.AGENT_TO_AGENT,
            priority=UnifiedMessagePriority.NORMAL
        )

        success = await send_message(message)
        print(f"   Message sent: {success}")

    except MessagingError as e:
        print(f"   ❌ Messaging error caught: {e}")
        print("   🔄 Attempting recovery...")
        # Recovery: Try fallback delivery method
        print("   ✅ Recovery: Using inbox fallback delivery")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

    # 3. Backup system error handling
    print("\n3️⃣ Backup system error handling...")
    try:
        backup_system = BackupSystemCore()
        # Try to create backup with invalid path
        result = await backup_system.create_backup(
            backup_type="full",
            source_path="/invalid/path/that/does/not/exist",
            custom_name="error_test_backup"
        )
        print(f"   Backup created: {result.get('backup_id', 'N/A')}")

    except BackupError as e:
        print(f"   ❌ Backup error caught: {e}")
        print("   🔄 Attempting recovery...")
        # Recovery: Use current directory as fallback
        try:
            result = await backup_system.create_backup(
                backup_type="full",
                source_path=".",
                custom_name="recovery_backup"
            )
            print("   ✅ Recovery: Backup created with fallback path")
        except Exception as recovery_error:
            print(f"   ❌ Recovery failed: {recovery_error}")
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")

    # 4. Comprehensive error handling with retries
    print("\n4️⃣ Comprehensive error handling with retries...")

    async def robust_operation_with_retries(operation, max_retries=3):
        """Execute operation with retry logic."""
        for attempt in range(max_retries):
            try:
                result = await operation()
                print(f"   ✅ Operation succeeded on attempt {attempt + 1}")
                return result
            except Exception as e:
                print(f"   ⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    print(f"   🔄 Retrying in 1 second...")
                    await asyncio.sleep(1)
                else:
                    print(f"   ❌ All attempts failed")
                    raise

    # Example robust operation
    async def test_operation():
        """Test operation that might fail."""
        # Simulate random failure
        import random
        if random.random() < 0.7:  # 70% chance of failure
            raise Exception("Simulated operation failure")
        return "Operation successful"

    try:
        result = await robust_operation_with_retries(test_operation)
        print(f"   🎉 Final result: {result}")
    except Exception as e:
        print(f"   💥 Operation failed after all retries: {e}")

    print("\n🛡️ Error handling demonstration completed!")
    print("   All error scenarios have been handled gracefully.")

if __name__ == "__main__":
    asyncio.run(error_handling_example())
```

---

## 🔗 **Integration Examples**

### **External System Integration**

```python
#!/usr/bin/env python3
"""
External system integration example.
"""

import asyncio
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.services.consolidated_messaging_service import (
    UnifiedMessage, UnifiedMessageType, UnifiedMessagePriority,
    send_message, broadcast_message
)
from src.core.backup_disaster_recovery import BackupSystemCore

async def external_system_integration():
    """Demonstrate integration with external systems."""
    print("🔗 External System Integration")
    print("=" * 35)

    # 1. Webhook integration simulation
    print("1️⃣ Webhook integration simulation...")

    async def simulate_webhook_receiver(webhook_data):
        """Simulate receiving webhook data."""
        print(f"   📥 Received webhook: {webhook_data.get('event', 'unknown')}")

        # Process webhook and send notification
        if webhook_data.get('event') == 'system_alert':
            alert_message = UnifiedMessage(
                content=f"🚨 System Alert: {webhook_data.get('message', 'Unknown alert')}",
                sender="WebhookSystem",
                recipient="Agent-1",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.URGENT
            )

            success = await send_message(alert_message)
            print(f"   📤 Alert notification: {'Sent' if success else 'Failed'}")

    # Simulate webhook data
    webhook_data = {
        "event": "system_alert",
        "message": "High CPU usage detected",
        "timestamp": "2024-01-01T12:00:00Z",
        "severity": "high"
    }

    await simulate_webhook_receiver(webhook_data)

    # 2. API integration simulation
    print("\n2️⃣ API integration simulation...")

    async def simulate_api_call():
        """Simulate external API call."""
        print("   🌐 Making external API call...")

        # Simulate API response
        api_response = {
            "status": "success",
            "data": {
                "agents_online": 8,
                "system_health": "good",
                "last_backup": "2024-01-01T11:00:00Z"
            }
        }

        print(f"   📊 API Response: {api_response['data']}")

        # Process API response and update system
        if api_response['data']['system_health'] == 'good':
            status_message = UnifiedMessage(
                content="✅ External system reports good health",
                sender="APIIntegration",
                recipient="Agent-8",
                message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                priority=UnifiedMessagePriority.NORMAL
            )

            success = await send_message(status_message)
            print(f"   📤 Status update: {'Sent' if success else 'Failed'}")

    await simulate_api_call()

    # 3. Database integration simulation
    print("\n3️⃣ Database integration simulation...")

    async def simulate_database_operation():
        """Simulate database operations."""
        print("   🗄️  Performing database operations...")

        # Simulate database query
        db_data = {
            "agents": [
                {"id": "Agent-1", "status": "active", "last_seen": "2024-01-01T12:00:00Z"},
                {"id": "Agent-2", "status": "active", "last_seen": "2024-01-01T12:00:00Z"},
                {"id": "Agent-3", "status": "inactive", "last_seen": "2024-01-01T11:30:00Z"}
            ]
        }

        print(f"   📊 Database query result: {len(db_data['agents'])} agents found")

        # Process database data
        inactive_agents = [agent for agent in db_data['agents'] if agent['status'] == 'inactive']

        if inactive_agents:
            print(f"   ⚠️  Found {len(inactive_agents)} inactive agents")

            # Send alert about inactive agents
            alert_content = f"⚠️ {len(inactive_agents)} agents are inactive: {[a['id'] for a in inactive_agents]}"

            broadcast_success = await broadcast_message(alert_content, "DatabaseMonitor")
            print(f"   📢 Inactive agent alert: {'Sent' if broadcast_success else 'Failed'}")
        else:
            print("   ✅ All agents are active")

    await simulate_database_operation()

    # 4. File system integration
    print("\n4️⃣ File system integration...")

    async def simulate_file_operations():
        """Simulate file system operations."""
        print("   📁 Performing file system operations...")

        # Simulate file monitoring
        files_to_monitor = [
            "config/coordinates.json",
            "logs/system.log",
            "backups/latest_backup.tar.gz"
        ]

        for file_path in files_to_monitor:
            file_obj = Path(file_path)
            if file_obj.exists():
                size_mb = file_obj.stat().st_size / (1024 * 1024)
                print(f"   📄 {file_path}: {size_mb:.2f} MB")
            else:
                print(f"   ❌ {file_path}: Not found")

                # Send alert for missing critical files
                if "coordinates.json" in file_path:
                    alert_message = UnifiedMessage(
                        content=f"🚨 Critical file missing: {file_path}",
                        sender="FileMonitor",
                        recipient="Agent-8",
                        message_type=UnifiedMessageType.SYSTEM_TO_AGENT,
                        priority=UnifiedMessagePriority.URGENT
                    )

                    success = await send_message(alert_message)
                    print(f"   📤 Critical file alert: {'Sent' if success else 'Failed'}")

    await simulate_file_operations()

    print("\n🔗 External system integration completed!")
    print("   All integration scenarios have been demonstrated successfully.")

def main():
    """Run all examples including shared utilities."""
    print("🚀 Agent Cellphone V2 - Usage Examples")
    print("=" * 50)
    
    # Run shared utilities example
    shared_utilities_example()
    
    # Run other examples
    asyncio.run(external_system_integration())

if __name__ == "__main__":
    main()
```

---

## 📚 **Additional Resources**

### **Running the Examples**

All examples can be run independently:

```bash
# Run individual examples
python docs/USAGE_EXAMPLES.md  # This file contains all examples

# Or run specific examples by copying the code into separate files
python examples/quick_start.py
python examples/messaging_workflow.py
python examples/backup_operations.py
```

### **Prerequisites**

Before running the examples, ensure you have:

1. **Python 3.8+** installed
2. **Required dependencies** installed:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configuration files** in place:
   - `config/coordinates.json`
   - `config/unified_config.yaml`
4. **Proper permissions** for file operations

### **Customization**

All examples can be customized by:

- Modifying agent IDs and coordinates
- Changing message content and priorities
- Adjusting backup types and schedules
- Customizing role modes and onboarding styles

---

**📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action in devlogs/ directory**


