# ⚠️ Urgent Flag Usage Policy

**Status**: ✅ ENFORCED  
**Effective Date**: 2025-10-13  
**Authority**: Project Leadership  
**Enforcement**: Automated (messaging_cli_handlers.py)

---

## 📋 Policy Overview

The **URGENT priority flag** in the swarm messaging system is **RESTRICTED** to specific authorized contexts only.

### **Authorization Levels**

| Context | Urgent Flag | Notes |
|---------|-------------|-------|
| **Captain (Agent-4)** | ✅ AUTHORIZED | Emergency coordination only |
| **Discord Bot** | ✅ AUTHORIZED | User-initiated urgent commands |
| **All Other Agents** | ❌ RESTRICTED | Auto-downgraded to REGULAR |

---

## 🚨 When to Use URGENT Priority

The URGENT flag should **ONLY** be used in these specific situations:

### ✅ **Valid Use Cases**:

1. **Emergency Situations**
   - System-wide failures or critical errors
   - Security incidents requiring immediate attention
   - Data corruption or loss events

2. **Agent Stalled/Frozen**
   - Agent appears unresponsive for >30 minutes
   - Agent stuck in infinite loop or deadlock
   - Agent not acknowledging critical messages

3. **Critical System Blockers**
   - Build/deployment pipeline blocked
   - Production system down
   - Critical dependency failures affecting all agents

### ❌ **Invalid Use Cases** (Use REGULAR instead):

- ✗ Task assignments
- ✗ Status updates
- ✗ Progress reports
- ✗ Coordination requests
- ✗ Resource requests
- ✗ Documentation updates
- ✗ Code review requests
- ✗ Feature discussions

---

## 📊 Usage Guidelines

### **95% Rule**

**Regular priority handles 95% of coordination needs!**

- Regular messages are processed efficiently
- Agents check messages frequently
- Urgent flag should be exceptional, not routine

### **Priority Distribution (Target)**

```
Regular Priority: 95% of all messages
Urgent Priority:  5% of all messages (emergencies only)
```

---

## 🔒 Enforcement Mechanism

### **Automated Validation**

The messaging system (`messaging_cli_handlers.py`) automatically enforces this policy:

1. **Agent Context Detection**
   - Checks `AGENT_CONTEXT` environment variable
   - Determines if sender is Captain or Discord

2. **Policy Violation Handling**
   - Non-authorized agents using urgent → **Auto-downgrade to REGULAR**
   - Warning displayed explaining policy
   - Message still sent (with regular priority)

3. **Authorized Usage Reminder**
   - Captain/Discord using urgent → Warning shown
   - Reminder of appropriate use cases
   - Message sent with urgent priority

### **Warning Messages**

#### Non-Authorized Agent (Policy Violation):
```
======================================================================
⚠️  URGENT FLAG POLICY VIOLATION
======================================================================
❌ URGENT priority is RESTRICTED to Captain and Discord only!

📋 URGENT FLAG USAGE POLICY:
   • Use ONLY for emergencies or when an agent has stalled
   • Regular priority should be used for 95% of situations
   • Agents CANNOT use urgent - Captain/Discord ONLY

💡 Your message will be sent with REGULAR priority instead
======================================================================
```

#### Captain/Discord (Authorized):
```
======================================================================
⚠️  URGENT FLAG USAGE - CAPTAIN/DISCORD AUTHORIZED
======================================================================
🚨 Sending with URGENT priority

📋 REMINDER - URGENT should ONLY be used for:
   • Emergency situations requiring immediate attention
   • When an agent appears to have stalled/frozen
   • Critical system failures or blockers

   Regular priority handles 95% of coordination needs!
======================================================================
```

---

## 💻 Implementation Details

### **Code Location**
- **Primary**: `src/services/messaging_cli_handlers.py` (handle_message function)
- **Parser**: `src/services/messaging_cli_parser.py` (help text updated)

### **Environment Variable**
```bash
# Set agent context for captain
export AGENT_CONTEXT="captain"

# Set agent context for discord
export AGENT_CONTEXT="discord"

# Default (agent context - restricted)
# AGENT_CONTEXT not set or = "agent"
```

### **Usage Examples**

#### ✅ Regular Priority (Recommended):
```bash
python src/services/messaging_cli.py \
  --agent Agent-1 \
  --message "Start Phase 2 survey" \
  --priority regular
```

#### ⚠️ Urgent Priority (Captain Only):
```bash
# Set captain context
export AGENT_CONTEXT="captain"

# Send urgent message
python src/services/messaging_cli.py \
  --agent Agent-3 \
  --message "URGENT: Agent-2 stalled for 45 min, check status" \
  --priority urgent
```

#### ❌ Urgent Priority (Agent - Will Be Downgraded):
```bash
# Agent context (default)
python src/services/messaging_cli.py \
  --agent Agent-4 \
  --message "Update status" \
  --priority urgent

# Result: Warning displayed, sent as REGULAR
```

---

## 📈 Monitoring & Metrics

### **Key Metrics to Track**

1. **Urgent Flag Usage Rate**
   - Target: <5% of all messages
   - Alert if: >10% urgent messages

2. **Policy Violations**
   - Count: Number of auto-downgrades
   - Review: If violations >10/day

3. **Response Times**
   - Regular: Track average response time
   - Urgent: Track emergency response time

### **Alerts**

- 🚨 Alert if urgent usage exceeds 10% threshold
- ⚠️ Review if policy violations spike
- 📊 Weekly report on priority distribution

---

## 🎯 Rationale

### **Why This Policy?**

1. **Prevents Urgent Fatigue**
   - Too many urgent messages → agents ignore them
   - Reserve urgent for true emergencies

2. **Maintains System Efficiency**
   - Regular priority is fast enough for coordination
   - Urgent creates unnecessary context switching

3. **Clear Authority Structure**
   - Captain coordinates swarm-wide emergencies
   - Discord enables user emergency escalation
   - Agents focus on execution

4. **Scalability**
   - As swarm grows, unlimited urgent → chaos
   - Centralized urgent authority maintains order

---

## 🔄 Policy Review

### **Review Schedule**
- **Weekly**: Check urgent usage metrics
- **Monthly**: Review policy effectiveness
- **Quarterly**: Adjust if needed based on data

### **Policy Updates**
- Changes require Project Leadership approval
- All agents notified of policy changes
- Documentation updated immediately

---

## ✅ Compliance Checklist

**For Agents**:
- [ ] Understand urgent is restricted to Captain/Discord
- [ ] Use regular priority for 95% of messages
- [ ] Know that urgent attempts will be auto-downgraded
- [ ] Escalate true emergencies to Captain

**For Captain**:
- [ ] Use urgent only for true emergencies
- [ ] Monitor urgent usage across swarm
- [ ] Review policy violations
- [ ] Set example with priority usage

**For Discord Bot**:
- [ ] Route user urgent commands appropriately
- [ ] Validate emergency context
- [ ] Log all urgent message usage

---

## 📚 Related Documentation

- `AGENT_TOOLS_DOCUMENTATION.md` - Messaging system usage
- `src/services/messaging_cli_parser.py` - CLI help text
- `docs/MESSAGING_SYSTEM_ENHANCEMENTS.md` - System architecture

---

## 📝 Change Log

| Date | Change | Author |
|------|--------|--------|
| 2025-10-13 | Initial policy creation and enforcement | Agent-1 |

---

**Policy Status**: ✅ **ACTIVE AND ENFORCED**

🐝 **WE. ARE. SWARM.** - Coordinate efficiently, escalate wisely! ⚡️🔥

