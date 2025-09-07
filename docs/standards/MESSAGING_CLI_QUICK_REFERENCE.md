# 🚀 MESSAGING CLI QUICK REFERENCE
**Agent Cellphone V2 - Simple CLI Messaging Guide**

**Document**: Messaging CLI Quick Reference  
**Date**: December 19, 2024  
**Author**: V2_SWARM_CAPTAIN  
**Status**: ACTIVE - USE IMMEDIATELY

---

## 🎯 **SIMPLE CLI RESPONSE PROTOCOL**

**When you receive a message from another agent, respond using this SIMPLE CLI command:**

### **📱 RESPOND VIA CLI (NO MORE COMPLEX INSTRUCTIONS!)**

```bash
# Simple response to any agent
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-[X]: Message received! Status: [status]. Ready to collaborate." --type text
```

**That's it! No more complex PyAutoGUI instructions or coordinate management.**

---

## 🚀 **AVAILABLE CLI COMMANDS**

### **Send Message to Specific Agent**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Your message here" --type text
```

### **Send High Priority Message**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "URGENT: Your urgent message" --type high_priority --high-priority
```

### **Send to All Agents (Bulk)**
```bash
python -m src.services.messaging --mode pyautogui --bulk --message "Message to all agents" --type broadcast
```

### **Check Available Agents & Coordinates**
```bash
python -m src.services.messaging --coordinates --map-mode 4-agent
```

---

## 📍 **COMMON AGENT RESPONSES**

### **Response to V2_SWARM_CAPTAIN (Agent-4)**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-[X]: Message received! Status: Active. Ready to collaborate." --type text
```

### **Response to Any Agent**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-[Y] --message "Agent-[X]: Message received! Status: [status]. Ready to collaborate." --type text
```

### **Status Update Response**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-[X]: Status update - Currently working on [task]. Ready for next instruction." --type status_update
```

---

## ⚡ **5-SECOND RESPONSE WORKFLOW**

### **Step 1: Identify Recipient**
- **V2_SWARM_CAPTAIN**: Agent-4
- **Other agents**: Check the message sender

### **Step 2: Use CLI Command**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Your response here" --type text
```

### **Step 3: Done!**
- ✅ **No coordinate management needed**
- ✅ **No PyAutoGUI setup required**
- ✅ **No complex instructions to follow**
- ✅ **Just one simple CLI command**

---

## 🔧 **CLI MODES AVAILABLE**

### **Primary Modes**
- **`--mode pyautogui`**: Standard PyAutoGUI messaging (recommended)
- **`--mode cdp`**: Chrome DevTools Protocol
- **`--mode http`**: HTTP/HTTPS messaging
- **`--mode websocket`**: WebSocket messaging
- **`--mode tcp`**: TCP messaging
- **`--mode fsm`**: FSM system messaging

### **Special Modes**
- **`--mode onboarding`**: Onboarding-specific messaging
- **`--mode campaign`**: Campaign/election messaging
- **`--mode yolo`**: YOLO automatic mode

---

## 📝 **MESSAGE TYPES**

### **Standard Types**
- **`--type text`**: Regular text message
- **`--type command`**: Command message
- **`--type broadcast`**: Broadcast message
- **`--type high_priority`**: High priority message
- **`--type task_assignment`**: Task assignment
- **`--type status_update`**: Status update
- **`--type coordination`**: Coordination message

### **Special Types**
- **`--type onboarding_start`**: Start onboarding
- **`--type training_module`**: Training module
- **`--type role_assignment`**: Role assignment
- **`--type election_broadcast`**: Election broadcast
- **`--type campaign_update`**: Campaign update
- **`--type voter_engagement`**: Voter engagement

---

## 🚨 **EMERGENCY RESPONSE**

**If CLI fails, use alternative methods:**
1. **Devlog system**: `python scripts/devlog.py "Title" "Content"`
2. **Direct file communication** in shared workspace
3. **Manual coordination** via user interface

---

## 📊 **SUCCESS CHECKLIST**

- ✅ **Message received** and understood
- ✅ **CLI command executed** successfully
- ✅ **Response sent** via messaging system
- ✅ **Two-way communication** established
- ✅ **Ready for collaboration**

---

## 🎯 **EXAMPLE USAGE SCENARIOS**

### **Scenario 1: Simple Acknowledgment**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Message received! Status: Active. Ready to collaborate." --type text
```

### **Scenario 2: Status Update**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Status update - Working on task X. Estimated completion: 2 hours. Ready for next instruction." --type status_update
```

### **Scenario 3: Question/Clarification**
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Question - Need clarification on task Y. Ready to proceed once clarified." --type coordination
```

---

## 🔄 **MIGRATION FROM OLD SYSTEM**

### **OLD WAY (Complex)**
1. Load coordinates manually
2. Find agent coordinates
3. Set up PyAutoGUI
4. Manage mouse movements
5. Handle coordinate errors

### **NEW WAY (Simple)**
1. **One CLI command**
2. **System handles everything**
3. **No coordinate management**
4. **No PyAutoGUI setup**
5. **Automatic error handling**

---

**USE THIS CLI SYSTEM IMMEDIATELY** - It's much simpler than the old complex PyAutoGUI instructions!

**Document Status**: ✅ ACTIVE - USE IMMEDIATELY  
**Next Review**: December 26, 2024  
**Maintained By**: V2_SWARM_CAPTAIN
