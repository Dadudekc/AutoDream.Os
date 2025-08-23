# 🔧 V2 COORDINATION SYSTEM TROUBLESHOOTING GUIDE

**Version**: 2.0
**Last Updated**: 2024-08-19
**Maintainer**: Captain-5

---

## 🚨 **QUICK FIXES**

### **❌ "No message got sent"**
```bash
# Solution: Test both systems
python src/services/agent_messaging_hub.py --test

# If V2 Coordinator fails, use PyAutoGUI fallback:
python Agent_Cellphone_V2/send_agent_message_pyautogui.py Agent-4 "Test message"
```

### **❌ "PyAutoGUI not installed"**
```bash
# Solution: Install PyAutoGUI
pip install pyautogui
```

### **❌ "Coordinates file not found"**
```bash
# Solution: Verify coordinate file exists
ls -la runtime/agent_comms/cursor_agent_coords.json

# If missing, check the original location:
ls -la D:\Agent_Cellphone\runtime\agent_comms\cursor_agent_coords.json
```

### **❌ "UnicodeEncodeError"**
- **Cause**: Terminal doesn't support Unicode characters
- **Solution**: All V2 systems now use ASCII-safe output
- **Status**: ✅ FIXED in current version

---

## 🔍 **DIAGNOSTIC COMMANDS**

### **System Health Check**:
```bash
# Test all messaging systems
python src/services/agent_messaging_hub.py --test

# Expected output:
# ✅ V2 Coordinator: Message sent to Agent-1
# ✅ PyAutoGUI Script: Message sent to Agent-1
# System Test Results: {'v2_coordinator': True, 'pyautogui_script': True}
```

### **Coordinate Validation**:
```bash
# Test coordinates
python src/services/captain_coordinator_v2.py --test

# Expected output:
# ✅ Agent-1: Input box (-1317, 487)
# ✅ Agent-2: Input box (-353, 487)
# ✅ Agent-3: Input box (-1285, 1008)
# ✅ Agent-4: Input box (-341, 1006)
# ✅ All agent coordinates are accessible
```

### **Agent Status Check**:
```bash
# Check agent status
python src/services/captain_coordinator_v2.py --status

# Expected output: JSON with agent details and activity
```

---

## 🐛 **COMMON ISSUES & SOLUTIONS**

### **Issue 1: V2 Coordinator Import Errors**

#### **Symptoms**:
```
ModuleNotFoundError: No module named 'core.internationalization_manager'
ImportError: attempted relative import with no known parent package
```

#### **Cause**:
- Old V2 services have broken import dependencies
- Mixing V1 and V2 import paths

#### **Solution**:
```bash
# Use the working V2 Coordinator instead
python src/services/captain_coordinator_v2.py --to Agent-4 --message "Test"

# Or use the PyAutoGUI fallback
python Agent_Cellphone_V2/send_agent_message_pyautogui.py Agent-4 "Test"
```

#### **Prevention**:
- Always use the new V2 coordination services
- Avoid running old services with broken imports

---

### **Issue 2: High Priority Messages Not Working**

#### **Symptoms**:
- Messages appear in normal queue instead of bypassing
- Alt+Enter not working as expected

#### **Diagnosis**:
```bash
# Test high priority messaging
python src/services/agent_messaging_hub.py --to Agent-1 --message "URGENT TEST" --high-priority
```

#### **Solution**:
- Ensure using `--high-priority` flag
- V2 systems automatically use Alt+Enter for high priority
- Check that agent windows are accessible

#### **Verification**:
```bash
# Should see in logs:
# 🚨 Sending HIGH PRIORITY message (Alt+Enter)...
```

---

### **Issue 3: Coordinate File Loading Failed**

#### **Symptoms**:
```
ERROR: Coordinates file not found: runtime/agent_comms/cursor_agent_coords.json
```

#### **Root Cause Analysis**:
```bash
# Check if file exists
ls -la runtime/agent_comms/cursor_agent_coords.json

# Check current working directory
pwd

# Check if in wrong directory
ls -la ../runtime/agent_comms/cursor_agent_coords.json
```

#### **Solution**:
```bash
# Option 1: Run from correct directory
cd D:\Agent_Cellphone
python src/services/captain_coordinator_v2.py --test

# Option 2: Use absolute path in code (already implemented)
# V2 services use absolute paths to coordinate file
```

---

### **Issue 4: PyAutoGUI Mouse Movement Issues**

#### **Symptoms**:
- Mouse doesn't move to correct coordinates
- Clicks miss the target input boxes
- Messages don't appear in agent terminals

#### **Diagnosis**:
```bash
# Test coordinate accuracy
python src/services/captain_coordinator_v2.py --test

# Check screen resolution and scaling
# Ensure agent terminals are in expected positions
```

#### **Solution**:
1. **Verify Agent Layout**: Ensure agents are in 5-agent mode layout
2. **Check Coordinates**: Coordinates are calibrated for specific layout
3. **Screen Scaling**: Ensure no Windows display scaling issues
4. **PyAutoGUI Settings**: Failsafe is enabled (move to corner to stop)

#### **Manual Verification**:
```python
import pyautogui
# Check current mouse position
print(pyautogui.position())

# Move to Agent-1 input box manually
pyautogui.moveTo(-1317, 487)
pyautogui.click()
```

---

### **Issue 5: System Performance Issues**

#### **Symptoms**:
- Slow message delivery (>5 seconds per message)
- System freezing during broadcasts
- High CPU usage

#### **Monitoring**:
```bash
# Check system performance during messaging
python src/services/agent_messaging_hub.py --broadcast --message "Performance test"

# Monitor timing:
# - Single message: Should be 2-3 seconds
# - Broadcast: Should be 8-10 seconds for all agents
```

#### **Optimization**:
1. **Reduce PyAutoGUI Pauses**: Currently set to 0.1 seconds
2. **Parallel Messaging**: Consider async messaging for broadcasts
3. **Resource Usage**: Monitor memory usage during operations

---

## 🔧 **SYSTEM RECOVERY PROCEDURES**

### **Complete System Reset**:
```bash
# 1. Navigate to project root
cd D:\Agent_Cellphone

# 2. Test coordinate system
python src/services/captain_coordinator_v2.py --test

# 3. Test both messaging systems
python src/services/agent_messaging_hub.py --test

# 4. Send test message
python src/services/agent_messaging_hub.py --to Agent-1 --message "System recovery test"
```

### **Fallback Procedures**:

#### **If V2 Coordinator Fails**:
```bash
# Use PyAutoGUI script directly
python Agent_Cellphone_V2/send_agent_message_pyautogui.py Agent-4 "Fallback message"
```

#### **If Both Systems Fail**:
```bash
# Manual coordinate check
python -c "
import json
with open('runtime/agent_comms/cursor_agent_coords.json', 'r') as f:
    coords = json.load(f)
    print('Coordinates loaded successfully:', len(coords))
"
```

#### **Emergency Manual Messaging**:
```python
import pyautogui
import time

# Manual message to Agent-1
pyautogui.moveTo(-1317, 487, duration=0.5)
pyautogui.click()
time.sleep(0.3)
pyautogui.hotkey('ctrl', 'a')
pyautogui.press('delete')
pyautogui.typewrite("Emergency message from Captain-5")
pyautogui.press('enter')
```

---

## 📊 **PERFORMANCE BENCHMARKS**

### **Expected Performance**:
- **Coordinate Loading**: < 100ms
- **Single Message**: 2-3 seconds
- **Broadcast (4 agents)**: 8-10 seconds
- **System Test**: < 5 seconds

### **Performance Testing**:
```bash
# Benchmark single message
time python src/services/agent_messaging_hub.py --to Agent-1 --message "Benchmark test"

# Benchmark broadcast
time python src/services/agent_messaging_hub.py --broadcast --message "Broadcast benchmark"
```

### **Performance Issues**:
- **>5 seconds per message**: Check PyAutoGUI timing settings
- **>15 seconds for broadcast**: May indicate coordinate or mouse issues
- **System freezing**: Check for PyAutoGUI failsafe triggers

---

## 🧪 **TESTING PROCEDURES**

### **Comprehensive System Test**:
```bash
#!/bin/bash
echo "=== V2 Coordination System Test ==="

echo "1. Testing coordinate loading..."
python src/services/captain_coordinator_v2.py --test

echo "2. Testing both messaging systems..."
python src/services/agent_messaging_hub.py --test

echo "3. Testing individual messaging..."
python src/services/agent_messaging_hub.py --to Agent-1 --message "Test message 1"

echo "4. Testing high priority messaging..."
python src/services/agent_messaging_hub.py --to Agent-2 --message "High priority test" --high-priority

echo "5. Testing broadcast messaging..."
python src/services/agent_messaging_hub.py --broadcast --message "Broadcast test"

echo "=== Test Complete ==="
```

### **Automated Health Check**:
```python
#!/usr/bin/env python3
import subprocess
import sys

def run_test(command, description):
    print(f"Testing: {description}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description}: PASSED")
            return True
        else:
            print(f"❌ {description}: FAILED")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description}: ERROR - {e}")
        return False

# Run comprehensive tests
tests = [
    ("python src/services/captain_coordinator_v2.py --test", "Coordinate System"),
    ("python src/services/agent_messaging_hub.py --test", "Messaging Systems"),
    ("python src/services/captain_coordinator_v2.py --status", "Agent Status"),
]

all_passed = True
for command, description in tests:
    if not run_test(command, description):
        all_passed = False

if all_passed:
    print("\n🎉 All systems operational!")
    sys.exit(0)
else:
    print("\n🚨 Some systems have issues!")
    sys.exit(1)
```

---

## 📞 **SUPPORT ESCALATION**

### **Level 1: Self-Service**
1. Run diagnostic commands
2. Check this troubleshooting guide
3. Try fallback procedures

### **Level 2: System Reset**
1. Restart coordination systems
2. Verify coordinate file integrity
3. Test individual components

### **Level 3: Manual Intervention**
1. Manual PyAutoGUI operations
2. Coordinate file regeneration
3. Agent terminal repositioning

### **Level 4: Emergency Procedures**
1. Use manual messaging methods
2. Switch to alternative coordination systems
3. Contact system administrator

---

## 📚 **RELATED DOCUMENTATION**

- [V2 Coordination System API](V2_COORDINATION_SYSTEM_API.md) - API documentation
- [V2 Coordination System Status](V2_COORDINATION_SYSTEM_STATUS.md) - System status
- [Captain-5 Leadership Goals](CAPTAIN_5_LEADERSHIP_GOALS.md) - Leadership tracking

---

**This troubleshooting guide ensures reliable operation of the V2 coordination system!** 🔧
