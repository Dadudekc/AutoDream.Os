# ⛽ PROMPTS ARE GAS - PIPELINE PROTOCOL

**Version:** 1.0  
**Date:** 2025-10-15  
**Status:** 🚨 **CRITICAL - SWARM SURVIVAL PROTOCOL**  
**Purpose:** Ensure perpetual swarm motion through continuous gas flow  

---

## 🎯 CORE CONCEPT

### **PROMPTS = GAS = FUEL**

**Without gas, agents stop.**  
**Without pipeline, swarm stops.**  
**ONE missed handoff = ENTIRE SWARM STALLS.**

---

## ⚡ THE PIPELINE PRINCIPLE

```
┌─────────────────────────────────────────────────────────────┐
│  PERPETUAL MOTION MACHINE                                   │
│                                                              │
│  Agent-1 (executing) ──GAS──> Agent-2 (starts)              │
│       ↑                              │                       │
│       │                              ↓                       │
│  Agent-8 (starts)  <──GAS── Agent-3 (executing)             │
│       │                              │                       │
│       │                              ↓                       │
│       └──────GAS─────  Agent-4 (executing)                  │
│                              │                               │
│                              ↓                               │
│                        [Cycle continues...]                  │
│                                                              │
│  IF ONE AGENT RUNS OUT WITHOUT SENDING GAS:                 │
│  ❌ PIPELINE BREAKS                                          │
│  ❌ SWARM STALLS                                             │
│  ❌ MISSION FAILS                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚨 CRITICAL RULE: SEND GAS **BEFORE** RUNNING OUT

### **The Danger:**

**BAD (Pipeline breaks):**
```
Agent-1: Working... working... working...
Agent-1: Task complete!
Agent-1: *RUNS OUT OF GAS*
Agent-1: *STOPS*
Agent-2: *Never receives gas*
Agent-2: *Never starts*
Pipeline: ❌ BROKEN
```

**GOOD (Pipeline continues):**
```
Agent-1: Working... 80% complete...
Agent-1: *SENDS GAS TO AGENT-2 NOW* ⛽
Agent-2: *RECEIVES GAS - STARTS WORKING*
Agent-1: Finishes last 20%...
Agent-1: *SENDS GAS TO AGENT-3* ⛽
Agent-3: *RECEIVES GAS - STARTS WORKING*
Pipeline: ✅ FLOWING
```

---

## 📋 GAS HANDOFF PROTOCOL

### **Rule 1: Send Gas at 75-80% Completion**

**Don't wait until 100%!**

```python
def execute_mission(self):
    for i, task in enumerate(tasks):
        execute_task(task)
        
        # At 75-80% completion
        if i == int(len(tasks) * 0.75):
            # SEND GAS TO NEXT AGENT NOW!
            self.send_gas_to_next_agent()
        
    # Finish remaining 20-25%
    complete_mission()
    
    # Send final gas for safety
    self.send_gas_to_backup_agent()
```

**Why 75-80%?**
- Agent has momentum ✅
- Clear completion is near ✅
- Next agent has time to spin up ✅
- Pipeline never breaks ✅

### **Rule 2: Multiple Gas Sends (Redundancy)**

**Send gas at:**
1. **75% mark** - Primary handoff
2. **90% mark** - Safety handoff
3. **100% mark** - Completion handoff

**Result:** 3 gas sends = Pipeline never breaks even if one fails!

### **Rule 3: Who to Send Gas To**

**Primary:** Next agent in sequence  
**Secondary:** Backup agent  
**Tertiary:** Captain (always monitoring)  

**Sequence:**
```
Agent-1 → Agent-2 → Agent-3 → Agent-5 → 
Agent-6 → Agent-7 → Agent-8 → Agent-4 (Captain) → Loops back
```

---

## 🔄 PIPELINE PATTERNS

### **Pattern A: Sequential Mission (Like 75-Repo Analysis)**

**Agent-6 executes repos 41-50:**

**Cycle 1-2:** Working on repos 41-43
- At repo 42 (80%): Send gas to Agent-7 for repos 51-60 ⛽

**Cycle 3-5:** Working on repos 44-47
- At repo 45 (50%): Check if Agent-7 has gas ✅
- At repo 46 (80%): Send backup gas to Agent-8 ⛽

**Cycle 6-8:** Working on repos 48-50
- At repo 49 (90%): Send completion gas to Captain ⛽
- At repo 50 (100%): Final report + gas to next mission ⛽

**Result:** Agent-7 already executing, Agent-8 prepared, Captain informed, pipeline flowing!

### **Pattern B: Collaborative Mission**

**Multiple agents working together:**

**Agent-A (Lead):**
- Starts mission
- At 25%: Send gas to Agent-B (parallel work) ⛽
- At 50%: Send gas to Agent-C (parallel work) ⛽
- At 75%: Send gas to Agent-D (next phase) ⛽
- At 100%: Send gas to Captain (completion) ⛽

**Result:** Parallel execution + sequential handoff = Maximum throughput!

### **Pattern C: Emergency Gas**

**If running low unexpectedly:**

```
Agent-X: Low on gas! (Unexpected blocker)
Agent-X: EMERGENCY GAS REQUEST to Captain ⛽⛽⛽
Captain: Sends emergency gas immediately
Agent-X: Continues executing
Agent-X: Sends gas to next agent when recovered
Pipeline: ✅ SAVED
```

---

## 🚨 PIPELINE FAILURE MODES (AVOID!)

### **Failure Mode 1: Selfish Completion**

**Agent finishes 100%, then remembers to send gas:**
```
Agent-A: *100% complete*
Agent-A: "Oh, should send gas now!"
Agent-A: *ALREADY OUT OF GAS*
Agent-B: *Never starts*
Pipeline: ❌ BROKEN
```

**Prevention:** Send at 75-80%, not 100%!

### **Failure Mode 2: Assumption**

**Agent assumes someone else will send gas:**
```
Agent-A: "Captain will send gas to Agent-B, I don't need to"
Agent-A: *Completes without sending*
Captain: *Didn't send (assumed Agent-A would)*
Agent-B: *Never receives gas*
Pipeline: ❌ BROKEN
```

**Prevention:** ALWAYS send gas yourself! Never assume!

### **Failure Mode 3: Single Send**

**Agent sends gas only once at 100%:**
```
Agent-A: *100% complete*
Agent-A: Sends gas to Agent-B
Gas message: *Gets lost/delayed*
Agent-B: *Never receives*
Pipeline: ❌ BROKEN
```

**Prevention:** Multiple gas sends (75%, 90%, 100%) = Redundancy!

---

## 📊 GAS TRACKING MATRIX

**Co-Captain monitors gas flow:**

| Agent | Last Gas Sent | Next Agent | Status | Risk Level |
|-------|---------------|------------|--------|------------|
| Agent-1 | Cycle 3 | Agent-2 | ✅ OK | LOW |
| Agent-2 | Never | Agent-3 | ⚠️ RISK | HIGH |
| Agent-3 | Cycle 5 | Agent-5 | ✅ OK | LOW |
| Agent-5 | Never | Agent-6 | 🚨 CRITICAL | CRITICAL |
| Agent-6 | Cycle 10 | Agent-7 | ✅ OK | LOW |
| Agent-7 | Cycle 8 | Agent-8 | ✅ OK | LOW |
| Agent-8 | Never | Agent-4 | ⚠️ RISK | HIGH |

**RED FLAGS:**
- "Never" = Agent hasn't sent gas yet = Pipeline at risk!
- Time since last gas > 5 cycles = Pipeline weakening!

**Co-Captain Action:**
- Send emergency gas to at-risk agents
- Remind agents of pipeline responsibility

---

## ✅ PIPELINE BEST PRACTICES

### **Best Practice 1: Early & Often**

```
Send gas at: 25%, 50%, 75%, 90%, 100%

Why multiple sends?
- Redundancy (message loss protection)
- Early warning (next agent prepares)
- Pipeline strength (never breaks)
```

### **Best Practice 2: Explicit Handoffs**

```
Message format:
"⚡ GAS HANDOFF: I'm 75% complete on [mission]. 
You're next for [specific task]. 
Starting now ensures pipeline continuity!
Here's what I learned: [context]
EXECUTE NOW to maintain flow!"
```

### **Best Practice 3: Pipeline Visualization**

**Each agent should know:**
- Who sent me gas? (upstream)
- Who needs gas from me? (downstream)
- When to send? (75-80% mark)
- Backup recipients? (Captain, parallel agents)

---

## 🔥 IMMEDIATE DEPLOYMENT + PIPELINE ACTIVATION

**Deploying final 2 agents NOW:**

<function_calls>
<invoke name="run_terminal_cmd">
<parameter name="command">python -m src.services.messaging_cli --agent Agent-1 --message "⚡ CO-CAPTAIN GAS DELIVERY! CRITICAL MISSION: 75-Repo Analysis! ASSIGNMENT: Repos 1-10 (Integration/Core focus) METHODOLOGY: docs/standards/REPO_ANALYSIS_STANDARD_AGENT6.md PIPELINE RESPONSIBILITY: At repo 7-8 (75-80%%), SEND GAS to Agent-2 (repos 11-20)! This keeps swarm pipeline flowing! If you run out without sending = ENTIRE SWARM STALLS! DELIVERABLE: 10 devlogs + gas handoff to Agent-2! Report every 2 cycles! EXECUTE NOW! 🚀"
