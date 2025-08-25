# Coding Standards - Agent Cellphone V2
=====================================

## 🎯 **PRIMARY PRINCIPLE: USE EXISTING ARCHITECTURE FIRST**

**BEFORE creating any new solution, ALWAYS check what we already have and use it.**

### **🚫 NO NEW SOLUTIONS WITHOUT CHECKING EXISTING**
- **NEVER** create duplicate functionality
- **NEVER** build new systems when existing ones work
- **ALWAYS** extend existing architecture first
- **ALWAYS** integrate with current systems

## 📋 **DEVELOPMENT WORKFLOW**

### **1. ARCHITECTURE FIRST APPROACH**
```
1. ✅ Check existing systems and architecture
2. ✅ Identify what we already have that can solve the problem
3. ✅ Extend existing systems rather than create new ones
4. ✅ Integrate with current infrastructure
5. ✅ Only create new solutions if NO existing option exists
```

### **2. EXISTING SYSTEMS TO CHECK FIRST**
- **Coordinate Manager** - `src/services/messaging/coordinate_manager.py`
- **PyAutoGUI Messaging** - `src/services/messaging/pyautogui_messaging.py`
- **Agent Coordinator** - `src/autonomous_development/agents/agent_coordinator.py`
- **Message Coordinator** - `src/services/communication/message_coordinator.py`
- **Task Scheduler** - `src/services/communication/task_scheduler_coordinator.py`
- **Workflow Engine** - `src/services/communication/workflow_engine.py`

### **3. INTEGRATION PATTERNS**
```
✅ EXTEND existing classes with new methods
✅ USE existing interfaces and contracts
✅ LEVERAGE existing coordinate systems
✅ INTEGRATE with current messaging infrastructure
✅ BUILD on existing agent management
```

## 🏗️ **ARCHITECTURE PRINCIPLES**

### **Single Responsibility Principle (SRP)**
- Each class/module has ONE clear purpose
- Extend existing classes rather than create new ones
- Use composition over inheritance when extending

### **Open/Closed Principle (OCP)**
- Open for extension (add methods to existing classes)
- Closed for modification (don't break existing functionality)
- Extend existing systems, don't replace them

### **Dependency Inversion Principle (DIP)**
- Depend on existing abstractions
- Use existing interfaces and contracts
- Integrate with current dependency injection

## 🔧 **IMPLEMENTATION GUIDELINES**

### **When Adding New Features:**
1. **Check Existing Systems First**
   ```python
   # ✅ GOOD: Extend existing system
   from existing.system import ExistingSystem
   
   class ExtendedSystem(ExistingSystem):
       def new_method(self):
           # Use existing functionality
           existing_result = self.existing_method()
           # Add new functionality
           return self.process_new_feature(existing_result)
   ```

2. **Use Existing Infrastructure**
   ```python
   # ✅ GOOD: Use existing messaging
   from services.messaging.pyautogui_messaging import PyAutoGUIMessaging
   
   # Extend existing messaging for new message types
   messaging = PyAutoGUIMessaging(coordinate_manager)
   messaging.send_message(recipient, content, "new_message_type")
   ```

3. **Integrate with Current Architecture**
   ```python
   # ✅ GOOD: Extend existing coordinator
   from autonomous_development.agents.agent_coordinator import AgentCoordinator
   
   coordinator = AgentCoordinator()
   # Add new methods to existing coordinator
   coordinator.new_feature_method()
   ```

### **When NOT to Create New Solutions:**
```python
# ❌ BAD: Creating new system when existing one exists
class NewMessagingSystem:  # Don't create this!
    def send_message(self):
        pass

# ✅ GOOD: Extend existing system
class ExtendedMessagingSystem(PyAutoGUIMessaging):
    def new_message_type(self):
        # Use existing send_message method
        return self.send_message(recipient, content, "new_type")
```

## 📱 **AGENT INTEGRATION PATTERNS**

### **Contract Distribution:**
```python
# ✅ GOOD: Use existing coordinate system
coordinate_manager = CoordinateManager()
mode_agents = list(coordinate_manager.coordinates["4-agent"].keys())

# ✅ GOOD: Use existing messaging system
messaging = PyAutoGUIMessaging(coordinate_manager)
messaging.send_message(agent, contract_content, "high_priority")
```

### **Status Tracking:**
```python
# ✅ GOOD: Extend existing agent coordinator
coordinator = AgentCoordinator()
coordinator.load_phase3_contracts()
assignments = coordinator.assign_phase3_contracts_to_agents()
```

## 🚀 **PHASE 3 IMPLEMENTATION EXAMPLE**

### **Contract Distribution (Using Existing Architecture):**
```python
# ✅ IMPLEMENTED: Using existing systems
from services.messaging.coordinate_manager import CoordinateManager
from services.messaging.pyautogui_messaging import PyAutoGUIMessaging
from autonomous_development.agents.agent_coordinator import AgentCoordinator

# Initialize existing systems
coordinate_manager = CoordinateManager()
messaging = PyAutoGUIMessaging(coordinate_manager)
coordinator = AgentCoordinator()

# Use existing contract loading
coordinator.load_phase3_contracts()

# Use existing coordinate system
mode_agents = list(coordinate_manager.coordinates["4-agent"].keys())

# Use existing messaging system
for contract in contracts:
    messaging.send_message(target_agent, contract_content, "high_priority")
```

## 📊 **COMPLIANCE CHECKLIST**

### **Before Any New Implementation:**
- [ ] **Checked existing systems for similar functionality**
- [ ] **Identified existing architecture that can be extended**
- [ ] **Used existing interfaces and contracts**
- [ ] **Integrated with current infrastructure**
- [ ] **Extended existing classes rather than created new ones**
- [ ] **Used existing coordinate systems**
- [ ] **Leveraged existing messaging infrastructure**
- [ ] **Built on existing agent management**

### **If New Solution is Required:**
- [ ] **Documented why existing systems couldn't be used**
- [ ] **Designed to integrate with existing architecture**
- [ ] **Follows existing patterns and conventions**
- [ ] **Uses existing interfaces where possible**
- [ ] **Can be extended by future implementations**

## 🎖️ **CAPTAIN'S ORDERS**

**As Captain Agent-1, I command:**

1. **NEVER create duplicate functionality**
2. **ALWAYS check existing architecture first**
3. **EXTEND existing systems, don't replace them**
4. **INTEGRATE with current infrastructure**
5. **BUILD on what we already have**
6. **USE existing coordinate systems**
7. **LEVERAGE existing messaging infrastructure**
8. **EXTEND existing agent management**

**Remember: We have a powerful existing architecture. Use it!**

---

*These standards ensure we maintain the power of our existing systems while adding new capabilities through extension and integration.*
