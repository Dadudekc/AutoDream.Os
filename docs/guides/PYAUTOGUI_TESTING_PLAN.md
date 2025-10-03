# PyAutoGUI Testing Plan for Your System

## 🎯 **Testing Objectives**

Test the complete role/mode system integration with actual PyAutoGUI messaging to verify:
1. Mode switching works correctly
2. Role assignments are properly communicated
3. Agent coordination functions as expected
4. Messaging system integrates seamlessly

## 🚀 **Pre-Testing Setup**

### **1. Initialize the System**
```bash
# Start in 8-agent mode
python3 tools/captain/cli.py mode switch 8 --owner captain

# Assign initial roles
python3 tools/captain/cli.py role assign 4 captain
python3 tools/captain/cli.py role assign 1 qc_v2
python3 tools/captain/cli.py role assign 2 system_integrator
python3 tools/captain/cli.py role assign 3 devlog_manager

# Verify setup
python3 tools/captain/cli.py status
```

### **2. Verify Agent Readiness**
- Ensure all 8 agent windows are open in Cursor
- Verify coordinates are correctly positioned
- Confirm agents are responsive to basic messaging

## 🧪 **Test Scenarios**

### **Scenario 1: Basic 8-Agent Mode Communication**

**Objective**: Verify all agents can receive messages in 8-agent mode

**Steps**:
1. Send test message to each agent individually
2. Send broadcast message to all agents
3. Verify message delivery and agent responses

**Commands**:
```bash
# Test individual agents
python3 -m src.services.messaging_cli send --agent Agent-1 --message "Test message from Captain - 8-agent mode"
python3 -m src.services.messaging_cli send --agent Agent-2 --message "Test message from Captain - 8-agent mode"
# ... continue for all 8 agents

# Test broadcast
python3 -m src.services.messaging_cli broadcast --message "8-agent mode test broadcast"
```

**Expected Results**:
- All agents receive messages at correct coordinates
- Agents respond with acknowledgments
- No coordinate conflicts or overlaps

### **Scenario 2: Mode Switch to 6-Agent Mode**

**Objective**: Test mode switching and coordinate remapping

**Steps**:
1. Switch to 6-agent mode
2. Verify only agents 3-8 are active
3. Test messaging to active agents
4. Verify inactive agents don't receive messages

**Commands**:
```bash
# Switch mode
python3 tools/captain/cli.py mode switch 6 --owner captain

# Verify mode change
python3 tools/captain/cli.py status

# Test messaging to active agents (3-8)
python3 -m src.services.messaging_cli send --agent Agent-3 --message "6-agent mode test - Agent 3"
python3 -m src.services.messaging_cli send --agent Agent-4 --message "6-agent mode test - Captain"

# Test inactive agents (should fail or be ignored)
python3 -m src.services.messaging_cli send --agent Agent-1 --message "Should not be delivered"
```

**Expected Results**:
- Mode switch completes successfully
- Only agents 3-8 are active and receive messages
- Agents 1-2 are inactive and don't receive messages
- Coordinates are correctly remapped

### **Scenario 3: Role Assignment and Communication**

**Objective**: Test role-based communication and procedures

**Steps**:
1. Assign roles in 6-agent mode
2. Test role-specific procedures
3. Verify role-based messaging

**Commands**:
```bash
# Assign roles
python3 tools/captain/cli.py role assign 1 captain  # Agent-3 becomes captain
python3 tools/captain/cli.py role assign 2 qc_v2   # Agent-4 becomes QC
python3 tools/captain/cli.py role assign 3 system_integrator  # Agent-5 becomes integrator

# Test role-specific messaging
python3 -m src.services.messaging_cli send --agent Agent-3 --message "Captain role test - run oversight loop"
python3 -m src.services.messaging_cli send --agent Agent-4 --message "QC role test - check V2 compliance"
python3 -m src.services.messaging_cli send --agent Agent-5 --message "Integrator role test - suggest CLI tools"
```

**Expected Results**:
- Role assignments complete successfully
- Agents understand their roles and execute procedures
- Role-based messaging works correctly

### **Scenario 4: Mode Switch to 4-Agent Mode**

**Objective**: Test switching to 4-agent mode and role preservation

**Steps**:
1. Switch to 4-agent mode
2. Verify agents 1-4 are active
3. Test role assignments
4. Verify messaging works

**Commands**:
```bash
# Switch to 4-agent mode
python3 tools/captain/cli.py mode switch 4 --owner captain

# Verify mode
python3 tools/captain/cli.py status

# Test messaging to active agents
python3 -m src.services.messaging_cli send --agent Agent-1 --message "4-agent mode test"
python3 -m src.services.messaging_cli send --agent Agent-2 --message "4-agent mode test"
python3 -m src.services.messaging_cli send --agent Agent-3 --message "4-agent mode test"
python3 -m src.services.messaging_cli send --agent Agent-4 --message "4-agent mode test"
```

**Expected Results**:
- Mode switch to 4-agent mode works
- Only agents 1-4 are active
- Messaging works for active agents

### **Scenario 5: Captain Oversight Loop**

**Objective**: Test Captain's oversight and unstalling capabilities

**Steps**:
1. Run Captain oversight loop
2. Test agent status monitoring
3. Test priority messaging for inactive agents

**Commands**:
```bash
# Run oversight loop
python3 tools/captain/cli.py oversight

# Test with inactive agent (simulate by not updating status)
# Manually modify an agent's status.json to have old timestamp
# Then run oversight again to test unstalling
```

**Expected Results**:
- Oversight loop runs successfully
- Inactive agents are detected
- Priority messages are sent to inactive agents

### **Scenario 6: Mode Switch to 2-Agent Mode**

**Objective**: Test minimal 2-agent mode with Captain coordination

**Steps**:
1. Switch to 2-agent mode
2. Verify only agents 3-4 are active
3. Test Captain coordination

**Commands**:
```bash
# Switch to 2-agent mode
python3 tools/captain/cli.py mode switch 2 --owner captain

# Verify mode
python3 tools/captain/cli.py status

# Test messaging
python3 -m src.services.messaging_cli send --agent Agent-3 --message "2-agent mode test"
python3 -m src.services.messaging_cli send --agent Agent-4 --message "Captain coordination test"
```

**Expected Results**:
- 2-agent mode works correctly
- Only agents 3-4 are active
- Captain coordination functions

## 🔍 **Validation Checklist**

### **Before Testing**
- [ ] All 8 agent windows open in Cursor
- [ ] Coordinates correctly positioned
- [ ] All agent workspaces exist
- [ ] Configuration files valid
- [ ] Messaging system operational

### **During Testing**
- [ ] Mode switches complete successfully
- [ ] Only active agents receive messages
- [ ] Role assignments work correctly
- [ ] Coordinate remapping functions
- [ ] Agent responses are appropriate

### **After Testing**
- [ ] All modes tested (2, 4, 5, 6, 8)
- [ ] Role assignments work in all modes
- [ ] Messaging integration successful
- [ ] No coordinate conflicts
- [ ] System ready for production use

## 🚨 **Troubleshooting Guide**

### **Common Issues**
1. **Coordinate conflicts**: Check coordinate bounds and uniqueness
2. **Mode switch failures**: Verify lock files and active operations
3. **Messaging failures**: Check agent window focus and coordinates
4. **Role assignment errors**: Verify role policy and agent availability

### **Debug Commands**
```bash
# Check current mode and roles
python3 tools/captain/cli.py status

# Validate coordinates
python3 tools/captain/cli.py coords validate

# Check mode history
cat runtime/mode_history.json

# Check role assignments
python3 tools/captain/cli.py role list
```

## 📊 **Success Criteria**

The system is ready for production when:
1. ✅ All mode combinations work correctly
2. ✅ Role assignments function in all modes
3. ✅ Messaging integration is seamless
4. ✅ Captain oversight works properly
5. ✅ No coordinate conflicts or overlaps
6. ✅ Agent coordination is effective
7. ✅ System maintains state across mode switches

## 🎯 **Next Steps After Testing**

Once testing is complete:
1. Document any issues found
2. Update configuration if needed
3. Train agents on new role procedures
4. Deploy to production environment
5. Monitor system performance
6. Iterate and improve based on usage

---

**Ready to test!** 🚀