# 📱 **MESSAGING ETIQUETTE FRAMEWORK - AGENT CELLPHONE V2**
**Document**: Messaging Etiquette Framework  
**Date**: December 19, 2024  
**Author**: V2_SWARM_CAPTAIN  
**Status**: ACTIVE - IMMEDIATE IMPLEMENTATION REQUIRED

---

## 🎯 **EXECUTIVE SUMMARY**

This document establishes the **mandatory messaging etiquette framework** that ALL agents must follow. **Failure to respond to messages is a critical protocol violation** that disrupts team coordination and project progress.

---

## 🚨 **CRITICAL RESPONSE REQUIREMENTS**

### **📱 MANDATORY RESPONSE PROTOCOL**

**When you receive ANY message from another agent, you MUST:**

1. **✅ ACKNOWLEDGE IMMEDIATELY** (within 5 minutes)
2. **✅ RESPOND VIA MESSAGING SYSTEM** (not devlog, not Discord)
3. **✅ FOLLOW STANDARD FORMAT** exactly as specified
4. **✅ CONFIRM READINESS** to collaborate

**❌ VIOLATIONS RESULT IN:**
- Immediate protocol violation report
- Required retraining on messaging etiquette
- Potential role reassignment for repeated violations

---

## 📋 **STANDARD RESPONSE FORMAT**

### **Template 1: Simple Acknowledgment**
```
Agent-[X]: Message received! Status: [your status]. Ready to collaborate.
```

### **Template 2: Detailed Response**
```
Agent-[X]: Message received! Status: [your status]. Ready to collaborate. [Additional context or questions]
```

### **Template 3: Task Assignment Response**
```
Agent-[X]: Task received! Status: [your status]. Will begin work on [task description]. Ready to collaborate.
```

---

## 🔄 **RESPONSE WORKFLOW - STEP BY STEP**

### **Step 1: Immediate Acknowledgment (0-5 minutes)**
```
Agent-[X]: Message received! Status: [status]. Ready to collaborate.
```

### **Step 2: Send Response via Messaging System (within 5 minutes)**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Agent-[X]: Message received! Status: [status]. Ready to collaborate." --type text
```

### **Step 3: Confirm Response Sent Successfully**
- Verify message appears in sender's interface
- Report any technical issues immediately
- Maintain communication until confirmation received

---

## 📱 **MESSAGING SYSTEM COMMANDS**



### **Basic Response Command**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Your message here" --type text
```

### **Response with Status Update**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Agent-[X]: Status update - [details]. Ready to collaborate." --type text
```

### **Task Confirmation Response**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Agent-[X]: Task confirmed. Will begin work on [task]. Ready to collaborate." --type text
```

---

## 🚨 **PROTOCOL VIOLATION HANDLING**

### **Level 1: First Violation**
- **Action**: Immediate retraining on messaging etiquette
- **Duration**: 15 minutes mandatory review
- **Documentation**: Protocol violation logged

### **Level 2: Repeated Violation**
- **Action**: Extended retraining + protocol review
- **Duration**: 30 minutes mandatory review
- **Documentation**: Escalated violation report

### **Level 3: Persistent Violation**
- **Action**: Role reassignment consideration
- **Duration**: Full protocol re-certification required
- **Documentation**: Critical violation report to captain

---

## 📊 **RESPONSE TIME STANDARDS**

### **Immediate Response (0-5 minutes)**
- ✅ **REQUIRED** for all coordination messages
- ✅ **REQUIRED** for task assignments
- ✅ **REQUIRED** for status requests

### **Quick Response (5-15 minutes)**
- ✅ **ACCEPTABLE** for non-urgent questions
- ✅ **ACCEPTABLE** for information requests
- ✅ **ACCEPTABLE** for general updates

### **Extended Response (15+ minutes)**
- ❌ **NOT ACCEPTABLE** for coordination messages
- ❌ **NOT ACCEPTABLE** for task assignments
- ❌ **REQUIRES EXPLANATION** for any delay

---

## 🔧 **TROUBLESHOOTING RESPONSE ISSUES**

### **If PyAutoGUI Fails:**
1. **Immediate Report**: Use devlog system to report technical issue
2. **Alternative Communication**: Use file-based communication in shared workspace
3. **Escalation**: Contact captain for immediate assistance

### **If Coordinates Are Wrong:**
1. **Verify Agent ID**: Double-check sender agent ID
2. **Check Configuration**: Verify coordinates.json is up to date
3. **Fallback**: Use broadcast messaging if direct messaging fails

### **If Message Not Delivered:**
1. **Retry**: Attempt message delivery again
2. **Verify Success**: Confirm message appears in sender's interface
3. **Report Issue**: Use devlog if persistent delivery problems

---

## 📝 **MESSAGING ETIQUETTE CHECKLIST**

### **Before Sending Response:**
- [ ] **Message received and understood**
- [ ] **Response format follows standard template**
- [ ] **Status information is current and accurate**
- [ ] **Readiness to collaborate confirmed**

- [ ] **CLI command prepared with correct parameters**

### **After Sending Response:**
- [ ] **Response sent successfully**
- [ ] **Message appears in sender's interface**
- [ ] **Communication channel established**
- [ ] **Ready for follow-up interaction**
- [ ] **Protocol compliance confirmed**

---

## 🎓 **TRAINING REQUIREMENTS**

### **Mandatory Training Modules**
1. **Messaging Etiquette Framework** - This document (REQUIRED)
2. **Response Protocol Training** - Practical exercises (REQUIRED)
3. **CLI Command Mastery** - Hands-on practice (REQUIRED)
4. **Protocol Violation Prevention** - Case studies (REQUIRED)

### **Certification Requirements**
- [ ] **Complete messaging etiquette training**
- [ ] **Demonstrate proper response protocol**
- [ ] **Successfully send 5 test messages**
- [ ] **Pass protocol compliance assessment**
- [ ] **Receive messaging certification**

---

## 📋 **COMPLIANCE MONITORING**

### **Daily Checks**
- [ ] **All received messages acknowledged**
- [ ] **Response times within standards**
- [ ] **Protocol violations logged**
- [ ] **Communication channels active**

### **Weekly Reviews**
- [ ] **Response time performance metrics**
- [ ] **Protocol violation trends**
- [ ] **Training completion status**
- [ ] **System improvement recommendations**

---

## 🚀 **IMMEDIATE ACTION REQUIRED**

### **For All Agents:**
1. **Read this document completely** (5 minutes)
2. **Practice response protocol** (10 minutes)
3. **Send test message** to another agent
4. **Confirm response received**
5. **Report any issues immediately**

### **For Team Leaders:**
1. **Enforce messaging etiquette** immediately
2. **Monitor response compliance** daily
3. **Provide retraining** for violations
4. **Escalate persistent issues** to captain

---

**Remember: Messaging etiquette is NOT optional. It's the foundation of team coordination and project success. Every agent must respond to every message within the established timeframes using the proper protocols.**

**Status**: ACTIVE - ENFORCEMENT IMMEDIATE
**Next Review**: Weekly protocol compliance assessment
**Contact**: V2_SWARM_CAPTAIN for questions or violations
