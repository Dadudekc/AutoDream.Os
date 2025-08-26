# 🏗️ Architecture Reference Guide - Agent-1

## **QUICK REFERENCE: EXISTING SYSTEMS TO USE**

### **1. Coordinate Manager** (`src/services/messaging/coordinate_manager.py`)
```python
# ✅ USE THIS for system coordination
from services.messaging.coordinate_manager import CoordinateManager

coordinate_manager = CoordinateManager()
# Get agent coordinates
mode_agents = list(coordinate_manager.coordinates["4-agent"].keys())
# Access system coordinates
system_coords = coordinate_manager.coordinates
```

### **2. PyAutoGUI Messaging** (`src/services/messaging/unified_pyautogui_messaging.py`)
```python
# ✅ USE THIS for all messaging
from services.messaging.unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging

messaging = UnifiedPyAutoGUIMessaging(coordinate_manager)
# Send messages
messaging.send_message(recipient, content, priority="high")
# Check delivery status
status = messaging.check_delivery_status(message_id)
```

### **3. Agent Coordinator** (`src/autonomous_development/agents/agent_coordinator.py`)
```python
# ✅ USE THIS for agent management
from autonomous_development.agents.agent_coordinator import AgentCoordinator

coordinator = AgentCoordinator()
# Load contracts
coordinator.load_phase3_contracts()
# Assign tasks
assignments = coordinator.assign_phase3_contracts_to_agents()
```

### **4. Message Coordinator** (`src/services/communication/message_coordinator.py`)
```python
# ✅ USE THIS for message routing
from services.communication.message_coordinator import MessageCoordinator

message_coordinator = MessageCoordinator()
# Route messages
message_coordinator.route_message(message, target_agent)
```

---

## **🚫 WHAT NOT TO CREATE**

### **NEVER Create:**
- ❌ New messaging systems
- ❌ New coordinate managers
- ❌ New agent coordinators
- ❌ Duplicate workflow engines
- ❌ New task schedulers

### **ALWAYS Extend:**
- ✅ Existing messaging classes
- ✅ Current coordinate systems
- ✅ Established agent management
- ✅ Existing workflow patterns

---

## **🔧 INTEGRATION PATTERNS**

### **Extending Existing Classes:**
```python
# ✅ GOOD: Extend existing system
from services.messaging.unified_pyautogui_messaging import UnifiedPyAutoGUIMessaging

class ExtendedMessaging(UnifiedPyAutoGUIMessaging):
    def new_feature(self, data):
        # Use existing functionality
        result = self.send_message(recipient, data)
        # Add new functionality
        return self.process_new_feature(result)
```

### **Using Existing Infrastructure:**
```python
# ✅ GOOD: Use existing coordinate system
coordinate_manager = CoordinateManager()
target_agent = coordinate_manager.get_agent_coordinates("Agent-2")

# ✅ GOOD: Use existing messaging
messaging = UnifiedPyAutoGUIMessaging(coordinate_manager)
messaging.send_message(target_agent, "Task completed", "high")
```

---

## **📋 TASK EXECUTION FLOW**

### **1. Receive Captain's Orders**
- Monitor inbox for captain's message
- Acknowledge within 30 seconds

### **2. Architecture Check**
- Identify existing systems that can help
- Check coordinate manager for agent locations
- Use existing messaging infrastructure

### **3. Task Execution**
- Extend existing systems if needed
- Use established patterns
- Follow integration guidelines

### **4. Reporting**
- Update status files
- Send completion reports
- Log activities

---

## **🎯 READY FOR CAPTAIN'S ORDERS**

**Agent-1, you now have complete understanding of the existing architecture. Use it, extend it, but never duplicate it.**

**Stand by for orders...** 🚀

