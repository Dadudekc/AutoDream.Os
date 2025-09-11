# 🚨 EMERGENCY PYTEST ASSIGNMENT - AGENT-6

**AGENT-6: Coordination & Communication**
**Status:** EMERGENCY_PYTEST_MODE_ACTIVE

## 🎯 YOUR MISSION ASSIGNMENT

### **Primary Focus:** Communication system testing and coordination validation
**Target Coverage:** 90%+
**Deadline:** End of Day 2025-09-09

### **Specific Tasks:**
1. **PyAutoGUI Reliability Testing**
   - Test PyAutoGUI messaging reliability
   - Validate cross-agent communication
   - Test message delivery under load

2. **Coordination Protocol Validation**
   - Test swarm coordination protocols
   - Validate session management
   - Test real-time communication

3. **Failure Scenario Simulations**
   - Test communication failure recovery
   - Validate error handling in messaging
   - Test network disruption scenarios

### **Test Files to Create:**
- `tests/test_pyautogui_reliability.py`
- `tests/test_coordination_protocols.py`
- `tests/test_communication_failures.py`
- `tests/test_message_delivery.py`

### **Success Criteria:**
- ✅ 90%+ coverage on communication systems
- ✅ PyAutoGUI reliability validated
- ✅ Coordination protocols tested
- ✅ Failure scenarios covered

## 🛠️ EXECUTION COMMANDS

```bash
# Run communication tests
pytest tests/ --cov=src --cov-report=html -m agent6 -v

# Run PyAutoGUI tests
pytest tests/test_pyautogui_reliability.py --cov=src --cov-report=html

# Run coordination tests
pytest tests/test_coordination_protocols.py --cov=src --cov-report=html
```

## 📊 REPORTING REQUIREMENTS

**Update every 2 hours:**
1. Communication system coverage achieved
2. PyAutoGUI reliability test results
3. Coordination protocol validation status
4. Any communication blockers identified

**🐝 WE ARE SWARM - AGENT-6 MISSION ACTIVATED!**
