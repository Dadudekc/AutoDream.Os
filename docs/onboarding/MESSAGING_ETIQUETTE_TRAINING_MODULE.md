# 📱 **MESSAGING ETIQUETTE TRAINING MODULE - AGENT CELLPHONE V2**
**Document**: Messaging Etiquette Training Module  
**Date**: December 19, 2024  
**Author**: V2_SWARM_CAPTAIN  
**Status**: ACTIVE - MANDATORY TRAINING FOR ALL AGENTS

---

## 🎯 **TRAINING OBJECTIVES**

By the end of this module, you will be able to:
- ✅ **Understand mandatory response requirements** and time standards
- ✅ **Execute proper response protocol** using standard templates
- ✅ **Use messaging CLI commands** correctly and efficiently
- ✅ **Handle protocol violations** and troubleshooting scenarios
- ✅ **Maintain communication compliance** in all agent interactions

---

## ⏰ **TRAINING DURATION**

- **Total Time**: 50 minutes
- **Theory**: 15 minutes
- **Practical Exercises**: 25 minutes
- **Assessment**: 10 minutes

---

## 📚 **THEORY SECTION - MESSAGING ETIQUETTE FUNDAMENTALS**

### **🚨 CRITICAL RESPONSE REQUIREMENTS**

**When you receive ANY message from another agent, you MUST:**

1. **✅ ACKNOWLEDGE IMMEDIATELY** (within 5 minutes)
2. **✅ RESPOND VIA MESSAGING SYSTEM** (not devlog, not Discord)
3. **✅ FOLLOW STANDARD FORMAT** exactly as specified
4. **✅ CONFIRM READINESS** to collaborate

**❌ VIOLATIONS RESULT IN:**
- Immediate protocol violation report
- Required retraining on messaging etiquette
- Potential role reassignment for repeated violations

### **📋 STANDARD RESPONSE FORMATS**

#### **Template 1: Simple Acknowledgment**
```
Agent-[X]: Message received! Status: [your status]. Ready to collaborate.
```

#### **Template 2: Detailed Response**
```
Agent-[X]: Message received! Status: [your status]. Ready to collaborate. [Additional context or questions]
```

#### **Template 3: Task Assignment Response**
```
Agent-[X]: Task received! Status: [your status]. Will begin work on [task description]. Ready to collaborate.
```

### **📱 MESSAGING SYSTEM COMMANDS**

#### **Basic Response Command**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Your message here" --type text
```

#### **Response with Status Update**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Agent-[X]: Status update - [details]. Ready to collaborate." --type text
```

#### **Task Confirmation Response**
```bash
python -m src.services.messaging --mode pyautogui --agent [SENDER_ID] --message "Agent-[X]: Task confirmed. Will begin work on [task]. Ready to collaborate." --type text
```

---

## 🎯 **PRACTICAL EXERCISES**

### **Exercise 1: Basic Response Protocol (5 minutes)**

**Scenario**: You receive a message from Agent-3 asking about your current status.

**Your Task**:
1. **Acknowledge** the message using standard format
2. **Provide your current status**
3. **Confirm readiness** to collaborate
4. **Validate coordinates** before sending
5. **Send response** via messaging system

**Expected Response Format**:
```
Agent-[X]: Message received! Status: [your status]. Ready to collaborate.
```

**CLI Commands to Use**:
```bash
# Step 1: Validate coordinates first
python -m src.services.messaging --mode pyautogui --agent Agent-3 --validate-coordinates

# Step 2: Send message after successful validation
python -m src.services.messaging --mode pyautogui --agent Agent-3 --message "Agent-[X]: Message received! Status: [status]. Ready to collaborate." --type text
```

**Practice Steps**:
1. Replace `[X]` with your agent ID
2. Replace `[status]` with your actual current status
3. **Execute coordinate validation first**
4. **Verify validation success**
5. **Execute message command**
6. Verify message appears in Agent-3's interface

---

### **Exercise 2: Task Assignment Response (5 minutes)**

**Scenario**: Agent-1 assigns you a task to review code changes.

**Your Task**:
1. **Acknowledge** task assignment
2. **Confirm task understanding**
3. **Provide timeline estimate**
4. **Send confirmation** via messaging system

**Expected Response Format**:
```
Agent-[X]: Task received! Status: [your status]. Will begin work on [task description]. Ready to collaborate.
```

**CLI Command to Use**:
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-1 --message "Agent-[X]: Task received! Status: [status]. Will begin work on code review. Ready to collaborate." --type text
```

**Practice Steps**:
1. Customize the message with your details
2. Execute the CLI command
3. Verify task confirmation received
4. Report any issues immediately

---

### **Exercise 3: Status Update Response (5 minutes)**

**Scenario**: Agent-4 requests a status update on your current work.

**Your Task**:
1. **Acknowledge** status request
2. **Provide detailed status update**
3. **Include progress percentage**
4. **Send comprehensive response** via messaging system

**Expected Response Format**:
```
Agent-[X]: Status update received! Status: [detailed status with progress]. Ready to collaborate.
```

**CLI Command to Use**:
```bash
python -m src.services.messaging --mode pyautogui --agent Agent-4 --message "Agent-[X]: Status update received! Status: Working on feature X, 75% complete. Ready to collaborate." --type text
```

**Practice Steps**:
1. Provide accurate status information
2. Include progress metrics
3. Execute the CLI command
4. Verify status update received

---

### **Exercise 4: Coordinate Validation (5 minutes)**

**Scenario**: You need to send a message to Agent-1, but want to ensure coordinates are correct first.

**Your Task**:
1. **Validate coordinates** for Agent-1
2. **Verify validation success**
3. **Send test message** after validation
4. **Confirm message delivery**

**CLI Commands to Use**:
```bash
# Step 1: Validate coordinates
python -m src.services.messaging --mode pyautogui --agent Agent-1 --validate-coordinates

# Step 2: Send test message after successful validation
python -m src.services.messaging --mode pyautogui --agent Agent-1 --message "Agent-[X]: Coordinate validation test successful. Ready to collaborate." --type text
```

**Practice Steps**:
1. Run coordinate validation first
2. Check for validation success indicators
3. Send test message only after validation
4. Verify message appears in Agent-1's interface
5. Report any validation failures immediately

---

### **Exercise 5: Troubleshooting Response (5 minutes)**

**Scenario**: Your PyAutoGUI messaging fails, but you need to respond to Agent-2.

**Your Task**:
1. **Identify the technical issue**
2. **Use alternative communication method**
3. **Report the issue** via devlog system
4. **Maintain communication** until resolved

**Alternative Communication Steps**:
1. **Report Issue**: Use devlog to report PyAutoGUI failure
2. **File Communication**: Create response file in shared workspace
3. **Escalation**: Contact captain for immediate assistance
4. **Retry**: Attempt messaging system again after issue resolution

**Devlog Command**:
```bash
python scripts/devlog.py "Messaging System Failure" "PyAutoGUI messaging failed when responding to Agent-2. Using alternative communication methods." --category "issue" --priority "high"
```

---

## 📊 **ASSESSMENT SECTION**

### **Knowledge Check Questions (5 minutes)**

**Question 1**: What is the maximum time allowed to respond to a coordination message?
- [ ] 15 minutes
- [ ] 5 minutes ✅
- [ ] 30 minutes
- [ ] 1 hour

**Question 2**: Which response format is correct for task assignments?
- [ ] "Message received, thanks"
- [ ] "Agent-[X]: Task received! Status: [status]. Will begin work on [task]. Ready to collaborate." ✅
- [ ] "I'll get to it later"
- [ ] "Task confirmed"

**Question 3**: What should you do if PyAutoGUI messaging fails?
- [ ] Wait for it to fix itself
- [ ] Use devlog system to report issue and find alternative communication ✅
- [ ] Ignore the message
- [ ] Send email instead

**Question 4**: What is the correct sequence for responding to Agent-3?
- [ ] Send message directly without validation
- [ ] Validate coordinates first, then send message ✅
- [ ] Send message, then validate coordinates
- [ ] Only validate coordinates, don't send message

**Question 5**: What happens if you violate messaging protocol repeatedly?
- [ ] Nothing
- [ ] Warning only
- [ ] Required retraining and potential role reassignment ✅
- [ ] Temporary suspension

**Question 6**: What should you do if coordinate validation fails?
- [ ] Send the message anyway
- [ ] Wait and try again later
- [ ] Report the issue via devlog and use alternative communication ✅
- [ ] Ignore the failure

---

### **Practical Assessment (5 minutes)**

**Final Task**: Send a test message to another agent and receive a response.

**Requirements**:
1. **Send message** to Agent-1 using proper CLI command
2. **Wait for response** from Agent-1
3. **Respond appropriately** using standard format
4. **Verify communication** established successfully

**Success Criteria**:
- [ ] Message sent successfully
- [ ] Response received within 5 minutes
- [ ] Proper response format used
- [ ] Communication channel established
- [ ] Protocol compliance confirmed

---

## 🚀 **POST-TRAINING REQUIREMENTS**

### **Immediate Actions Required**
1. **Read messaging etiquette framework** completely
2. **Practice response protocol** with other agents
3. **Send 5 test messages** to different agents
4. **Confirm responses received** successfully
5. **Report any issues** immediately

### **Ongoing Compliance**
1. **Monitor response times** daily
2. **Follow standard formats** for all responses
3. **Use troubleshooting procedures** when needed
4. **Maintain communication standards** consistently
5. **Report protocol violations** to captain

---

## 📋 **CERTIFICATION CHECKLIST**

### **Training Completion**
- [ ] **Theory section completed** and understood
- [ ] **All practical exercises** completed successfully
- [ ] **Assessment questions** answered correctly (80% minimum)
- [ ] **Practical assessment** completed successfully
- [ ] **Post-training requirements** understood and accepted

### **Certification Requirements**
- [ ] **Complete messaging etiquette training** (this module)
- [ ] **Demonstrate proper response protocol** in practice
- [ ] **Successfully send 5 test messages** to different agents
- [ ] **Pass protocol compliance assessment** (this module)
- [ ] **Receive messaging certification** from captain

---

## 🚨 **IMPORTANT REMINDERS**

### **Critical Points**
- **Messaging etiquette is MANDATORY** - not optional
- **5-minute response time** is the maximum allowed
- **Always use standard format** for responses
- **Report technical issues** immediately
- **Maintain communication** until resolved

### **Contact Information**
- **For Questions**: Review this training module
- **For Issues**: Use devlog system to report problems
- **For Violations**: Contact V2_SWARM_CAPTAIN immediately
- **For Certification**: Complete all requirements in this module

---

**Status**: ACTIVE - MANDATORY TRAINING
**Next Review**: Weekly protocol compliance assessment
**Contact**: V2_SWARM_CAPTAIN for questions or certification
**Completion Required**: Before any agent coordination activities
