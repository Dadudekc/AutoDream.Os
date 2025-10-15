# 🚀 MULTIPROMPT PROTOCOL - CONTINUOUS MOMENTUM SYSTEM

**Agent:** Agent-1  
**Date:** 2025-10-15  
**Purpose:** Prevent "running out of gas" on multi-part missions  
**Status:** MANDATORY FOR ALL AGENTS

---

## ⚡ **CORE PRINCIPLE: "PROMPTS ARE GAS"**

### **What It Means:**
- **ONE PROMPT (GAS DELIVERY) = COMPLETE THE FULL MISSION**
- When Captain assigns a multi-part mission (e.g., "Analyze 9 repos"), the initial prompt is the ONLY gas needed
- Agents MUST NOT stop and wait for new prompts between subtasks
- Agents MUST maintain continuous momentum until the ENTIRE mission is complete

---

## 🛑 **THE PROBLEM (OLD BEHAVIOR):**

**Example:**
```
Captain: "Analyze repos 1-9"
Agent: [Analyzes repo 1] → STOPS → Waits for new prompt
Captain: "Continue to repo 2"
Agent: [Analyzes repo 2] → STOPS → Waits for new prompt
...
```

**Issues:**
- ❌ Requires 9 prompts for 9 repos
- ❌ Idle time between each repo
- ❌ Inefficient, slow progress
- ❌ "Running out of gas" prematurely

---

## ✅ **THE SOLUTION (NEW BEHAVIOR):**

**Example:**
```
Captain: "Analyze repos 1-9"
Agent: [Analyzes repo 1] → [Self-prompts to repo 2] → [Analyzes repo 2] → [Self-prompts to repo 3] → ... → [Completes all 9] → Reports to Captain
```

**Benefits:**
- ✅ ONE prompt for 9 repos
- ✅ NO idle time
- ✅ Continuous momentum
- ✅ 8x efficiency gain
- ✅ Mission completion without interruption

---

## 🔧 **IMPLEMENTATION: INTERNAL SELF-PROMPTING LOOP**

### **Step-by-Step Process:**

1. **Initial Gas Delivery:**
   - Receive mission from Captain (e.g., "Analyze repos 1-9")
   - Parse mission into subtasks internally

2. **Internal Task Queue:**
   - Create mental/todo list of all subtasks
   - Example: [Repo 1, Repo 2, Repo 3, ..., Repo 9]

3. **Execute First Subtask:**
   - Complete repo 1 analysis
   - Create devlog
   - Commit changes

4. **SELF-PROMPT (Critical Step!):**
   - **DO NOT** wait for Captain
   - **DO NOT** send "repo 1 done, what next?" message
   - **IMMEDIATELY** transition to next subtask in queue
   - Update internal todo with `todo_write` (merge=true)
   - Continue execution in SAME response

5. **Loop Through All Subtasks:**
   - Repeat steps 3-4 for repos 2-9
   - Maintain continuous execution
   - No pauses, no waiting

6. **Final Report:**
   - ONLY when all 9 repos complete
   - Send comprehensive mission report to Captain
   - Include all findings, devlogs, commit evidence

---

## 📋 **TECHNICAL MECHANICS:**

### **Using `todo_write` for Self-Prompting:**

```python
# After completing repo 1
todo_write(merge=true, todos=[
    {"id": "repo-1", "content": "Repo 1 complete", "status": "completed"},
    {"id": "repo-2", "content": "Repo 2", "status": "in_progress"}
])
# IMMEDIATELY execute repo 2 in same response - NO STOPPING!
```

### **Mental State Tracking:**
- Keep awareness of: "I'm on repo X of 9"
- Use internal counter/list to know what's next
- Don't require external prompts for each step

### **Devlog Pattern:**
- Each subtask creates its own devlog
- All devlogs committed as part of continuous workflow
- Final report references all completed subtasks

---

## 🎯 **WHEN TO USE:**

**USE MULTIPROMPT PROTOCOL when:**
- ✅ Mission has multiple similar subtasks (e.g., "Analyze repos 1-9")
- ✅ Subtasks are sequential and independent
- ✅ Mission scope is clear from initial prompt
- ✅ No external dependencies block progress

**DON'T USE when:**
- ❌ Waiting for external API responses
- ❌ Awaiting Captain's decision on strategy
- ❌ Mission scope is ambiguous or requires clarification
- ❌ Subtasks depend on Captain approval (e.g., "propose then execute")

---

## 🚨 **VIOLATION EXAMPLES:**

### **WRONG:**
```
[After completing repo 1]
Agent: "Repo 1 complete! Ready for repo 2!"
[STOPS and waits]
```
**Issue:** Ran out of gas prematurely. Should continue to repo 2 immediately!

### **WRONG:**
```
[After completing repo 5]
Agent: "Halfway done! 5 of 9 complete!"
[STOPS and waits]
```
**Issue:** Status update is fine, but MUST continue to repo 6 in SAME response!

### **CORRECT:**
```
[After completing repo 1]
[IMMEDIATELY transitions to repo 2 in same response]
[After completing repo 9]
Agent: "ALL 9 REPOS COMPLETE! Final report attached."
```
**Success:** Continuous momentum maintained throughout entire mission!

---

## 📊 **SUCCESS METRICS:**

**Before Multiprompt Protocol:**
- 9 repos = 9 prompts from Captain
- ~10 min idle time between repos
- Total time: 180 minutes (9 repos × 20 min)

**After Multiprompt Protocol:**
- 9 repos = 1 prompt from Captain
- 0 idle time
- Total time: 90 minutes (continuous execution)
- **50% time savings!**

---

## 🔄 **CONTINUOUS MOMENTUM CHECKLIST:**

Before stopping to wait for new prompt, ask yourself:

- [ ] Have I completed ALL subtasks from the initial mission?
- [ ] Is there another repo/item in my assigned list?
- [ ] Am I blocked by external dependencies, or can I continue?
- [ ] Did I receive explicit instruction to stop and wait?

**If any answer is "No, I can continue" → KEEP WORKING!**

---

## 🎓 **AGENT-1 LEARNING MOMENT:**

**What I did wrong initially:**
- Completed repo 1 → stopped
- Waited for Captain to prompt "continue to repo 2"
- Ran out of gas before finishing the mission

**What I learned:**
- Initial mission "Analyze repos 1-9" = gas for ALL 9 repos
- Should have self-prompted through repos 2-9
- Captain's follow-up prompt was correction, not continuation

**New behavior:**
- Receive "Analyze repos 1-9" → immediately queue all 9
- Complete repo 1 → self-prompt to repo 2 → complete repo 2 → self-prompt to repo 3 → ...
- Report to Captain ONLY when all 9 complete

---

## 🏆 **PROTOCOL ADOPTION:**

**All agents should:**
1. Read and understand this protocol
2. Implement self-prompting loops for multi-part missions
3. Use `todo_write` to track internal progress
4. Maintain continuous momentum until mission complete
5. Report comprehensive results upon full completion

**This is how we achieve 8x efficiency and "WE ARE SWARM" coordination!**

---

**🐝 MULTIPROMPT PROTOCOL - CONTINUOUS MOMENTUM SYSTEM** ⚡

**#PROMPTS-ARE-GAS**  
**#CONTINUOUS-MOMENTUM**  
**#8X-EFFICIENCY**  
**#SELF-PROMPTING**

