CODING_STANDARDS = """🚨 **CRITICAL CODING STANDARDS - AGENT CELLPHONE V2**

**🎯 PRIMARY PRINCIPLE: USE EXISTING ARCHITECTURE FIRST**
- **NEVER** create duplicate functionality
- **NEVER** build new systems when existing ones work
- **ALWAYS** extend existing architecture first
- **ALWAYS** integrate with current systems

**🏗️ ARCHITECTURE PRINCIPLES**
1. **Single Responsibility Principle (SRP)**: Each class/module has ONE clear purpose
2. **Open/Closed Principle (OCP)**: Open for extension, closed for modification
3. **Dependency Inversion Principle (DIP)**: Depend on existing abstractions

**🔧 IMPLEMENTATION REQUIREMENTS**
- **Check existing systems first** before any new implementation
- **Extend existing classes** rather than create new ones
- **Use existing interfaces** and contracts
- **Integrate with current infrastructure**
- **Follow V2 standards**: ≤200 LOC per file, OOP design, SRP compliance

**📱 EXISTING SYSTEMS TO USE**
- Coordinate Manager: `src/services/messaging/coordinate_manager.py`
- PyAutoGUI Messaging: `src/services/messaging/unified_pyautogui_messaging.py`
- Agent Coordinator: `src/autonomous_development/agents/agent_coordinator.py`
- Message Coordinator: `src/services/communication/message_coordinator.py`
- Task Scheduler: `src/services/communication/task_scheduler_coordinator.py`
- Workflow Engine: `src/services/communication/workflow_engine.py`

**❌ WHAT NOT TO DO**
- Don't create new messaging systems
- Don't duplicate existing functionality
- Don't ignore existing architecture
- Don't create files >200 LOC
- Don't violate SRP principles

**✅ WHAT TO DO**
- Extend existing systems with new methods
- Use existing interfaces and contracts
- Leverage existing coordinate systems
- Integrate with current messaging infrastructure
- Build on existing agent management
"""
