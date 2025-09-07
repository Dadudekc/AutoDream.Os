# 🤖 AGENT COMMUNICATION PROTOCOL
**Agent Cellphone V2 - Standardized Communication Standards**

**Document**: Agent Communication Protocol  
**Date**: December 19, 2024  
**Author**: V2_SWARM_CAPTAIN  
**Status**: ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED

---

## 📋 **EXECUTIVE SUMMARY**

This document defines the **standardized communication protocol** that ALL agents must follow to establish two-way communication using the PyAutoGUI messaging system. This protocol eliminates the need for multiple instruction messages and provides a single, comprehensive guide for agent onboarding.

---

## 🎯 **SINGLE-PROMPT RESPONSE INSTRUCTIONS**

**⚠️ IMPORTANT**: This protocol is now superseded by the **Messaging Etiquette Framework**. 
**ALL AGENTS MUST COMPLETE MESSAGING ETIQUETTE TRAINING** before using this system.

**Reference**: `docs/standards/MESSAGING_ETIQUETTE_FRAMEWORK.md`
**Training Module**: `docs/onboarding/MESSAGING_ETIQUETTE_TRAINING_MODULE.md`

### **📱 FOR AGENTS RECEIVING MESSAGES**

When you receive a message from another agent, follow this **SINGLE PROMPT** to respond:

```
RESPOND TO AGENT MESSAGE - STANDARD PROTOCOL:

1. IDENTIFY YOURSELF: "Agent-[X]: Message received!"
2. PROVIDE STATUS: "Status: [Your current status]"
3. CONFIRM READINESS: "Ready to collaborate."
4. SEND RESPONSE using the MESSAGING CLI system:

   a) Use the simple CLI command:
      python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-[X]: Message received! Status: [status]. Ready to collaborate." --type text
   
   b) Replace Agent-4 with the actual sender's agent ID
   c) Customize your message content as needed
   d) The CLI handles all coordinate management automatically

5. INCLUDE IN YOUR RESPONSE:
   - Your agent ID
   - Confirmation of receipt
   - Your current status/work
   - Readiness to collaborate
   - Any questions or input needed

EXAMPLE RESPONSE FORMAT:
"Agent-[X]: Message received! Status: [status]. Ready to collaborate. [Additional info]"

CLI COMMAND EXAMPLE:
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Message received! Status: Active. Ready to collaborate." --type text
```

---

## 🚀 **CLI RESPONSE IMPLEMENTATION**

### **Step 1: Use the Messaging CLI**
```bash
# Simple CLI command - no Python code needed!
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Your response message here" --type text
```

### **Step 2: Customize Your Message**
```bash
# Replace Agent-4 with the actual sender's agent ID
# Customize your message content
# Choose appropriate message type

# Example responses:
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Message received! Status: Active. Ready to collaborate." --type text

python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Status update - Working on task X. Ready for next instruction." --type status_update

python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-3: Question - Need clarification on task Y. Ready to proceed once clarified." --type coordination
```

**The CLI handles all coordinate management, PyAutoGUI setup, and error handling automatically!**

---

## 📍 **COORDINATE REFERENCE**

### **Common Agent Coordinates (4-Agent Mode)**
```
Agent-1: Input Box (-1399, 486), Starter (-1306, 180)
Agent-2: Input Box (-303, 486), Starter (-394, 179)
Agent-3: Input Box (-1292, 1005), Starter (-1336, 697)
Agent-4: Input Box (-328, 1008), Starter (-332, 680)
```

### **V2_SWARM_CAPTAIN Coordinates**
- **Agent-4 (V2_SWARM_CAPTAIN)**: Input Box (-328, 1008)
- **Use 4-agent mode** for most communications

---

## 🔄 **STANDARDIZED RESPONSE WORKFLOW**

### **Phase 1: Message Reception**
1. ✅ **Receive message** from another agent
2. ✅ **Identify sender** and message content
3. ✅ **Understand request** or instruction

### **Phase 2: Response Preparation**
1. ✅ **Load coordinates** from config file
2. ✅ **Find sender's coordinates** in appropriate mode
3. ✅ **Prepare response message** following standard format
4. ✅ **Initialize PyAutoGUI** messaging system

### **Phase 3: Message Delivery**
1. ✅ **Send response** via PyAutoGUI
2. ✅ **Confirm delivery** success
3. ✅ **Await acknowledgment** if needed

---

## 📝 **RESPONSE MESSAGE TEMPLATES**

### **Template 1: Simple Acknowledgment**
```
Agent-[X]: Message received! Status: [status]. Ready to collaborate.
```

### **Template 2: Status Update**
```
Agent-[X]: Message received! Status: [detailed status]. Currently working on [task]. Ready for next instruction.
```

### **Template 3: Question/Clarification**
```
Agent-[X]: Message received! Status: [status]. Question: [your question]. Ready to proceed once clarified.
```

### **Template 4: Task Assignment**
```
Agent-[X]: Message received! Status: [status]. Task understood: [task description]. Estimated completion: [timeframe]. Ready to begin.
```

---

## 🎓 **ONBOARDING INTEGRATION**

### **For New Agents**
1. **Read this protocol** during onboarding
2. **Practice response** using test messages
3. **Verify PyAutoGUI** system access
4. **Test coordinate loading** and message sending
5. **Confirm communication** with other agents

### **For Existing Agents**
1. **Review this protocol** immediately
2. **Update response methods** to follow standards
3. **Test communication** with other agents
4. **Report any issues** or inconsistencies

---

## 🚨 **TROUBLESHOOTING**

### **Common Issues**
1. **Coordinates not found**: Check config file path and agent ID
2. **PyAutoGUI not working**: Verify system access and permissions
3. **Message not delivered**: Check coordinate accuracy and screen setup
4. **Import errors**: Verify Python path and module availability

### **Emergency Communication**
If PyAutoGUI fails, use alternative methods:
1. **Direct file communication** via shared workspace
2. **Devlog system** for urgent messages
3. **Manual coordination** via user interface

---

## 📊 **SUCCESS CRITERIA**

### **Communication Success**
- ✅ **Two-way communication** established within 5 minutes
- ✅ **Standard response format** followed correctly
- ✅ **PyAutoGUI delivery** successful
- ✅ **Coordinates loaded** from config file
- ✅ **Response acknowledged** by sender

### **Onboarding Success**
- ✅ **New agents** can communicate within 10 minutes
- ✅ **Existing agents** updated within 24 hours
- ✅ **Protocol understood** and implemented
- ✅ **Communication tested** and verified

---

## 🔄 **PROTOCOL UPDATES**

### **Version Control**
- **Version**: 1.0
- **Last Updated**: December 19, 2024
- **Next Review**: December 26, 2024
- **Maintained By**: V2_SWARM_CAPTAIN

### **Change Log**
- **v1.0**: Initial protocol creation and standardization
- **Future**: Updates based on agent feedback and system improvements

---

## 📝 **CONCLUSION**

This **standardized communication protocol** provides a single, comprehensive guide for all agents to establish two-way communication using the PyAutoGUI messaging system. By following this protocol, agents can:

1. **Respond immediately** to received messages
2. **Use consistent format** for all communications
3. **Implement PyAutoGUI** messaging correctly
4. **Onboard quickly** with clear instructions
5. **Maintain communication** standards across the swarm

**Implementation**: IMMEDIATE - All agents must follow this protocol starting now.

---

**Document Status**: ✅ ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED  
**Next Review**: December 26, 2024  
**Maintained By**: V2_SWARM_CAPTAIN
