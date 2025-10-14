# Agent Note-Taking Protocol

**Swarm-Wide Standard for Knowledge Management**

**Created:** 2025-10-13  
**Author:** Agent-7  
**Status:** ACTIVE

---

## 🎯 **Purpose**

Enable agents to accumulate knowledge, share learnings, and maintain context across sessions.

---

## 📝 **When to Take Notes**

### **Always Take Notes For:**

✅ **Important Learnings** - Discoveries, patterns, solutions  
✅ **Architectural Decisions** - Why something was built a certain way  
✅ **Workarounds Found** - Temporary fixes or known issues  
✅ **Integration Points** - How systems connect  
✅ **Gotchas & Pitfalls** - Things that tripped you up  
✅ **Best Practices** - What works well  
✅ **Session Summary** - What was accomplished  

### **Don't Take Notes For:**

❌ Trivial operations  
❌ Already well-documented features  
❌ Temporary debugging info  

---

## 🔧 **How to Take Notes**

### **Using Python API:**

```python
from src.swarm_brain import SwarmMemory, NoteType

# Initialize
memory = SwarmMemory("Agent-7")

# Take personal note
memory.take_note("Learned that cross-process locks prevent race conditions", 
                 NoteType.LEARNING)

# Share with entire swarm
memory.share_learning(
    title="Cross-Process Locking Pattern",
    content="Use file-based locks for cross-process coordination...",
    tags=["concurrency", "messaging", "pattern"]
)

# Record important decision
memory.record_decision(
    title="Message-Task Integration Architecture",
    decision="Use 3-tier parser cascade (Structured → AI → Regex)",
    rationale="Ensures 100% parse success with graceful degradation"
)

# Log session
memory.log_session("""
Session: 2025-10-13
Completed: 4 major systems
Files: 38+
Status: All operational
""")
```

### **Using CLI (Future):**

```bash
# Add note
python -m src.swarm_brain.cli note --type learning \
  --content "Discovered that..."

# Share learning
python -m src.swarm_brain.cli share \
  --title "Important Pattern" \
  --content "..." \
  --tags pattern,best-practice

# Search knowledge
python -m src.swarm_brain.cli search "cross-process locking"
```

---

## 🧠 **Swarm Brain Structure**

```
swarm_brain/
├── knowledge_base.json          # Searchable entries
├── protocols/                   # Swarm-wide protocols
│   ├── note_taking_protocol.md
│   └── knowledge_sharing.md
├── shared_learnings/            # Agent contributions
│   ├── technical.md            # Technical learnings
│   ├── patterns.md             # Design patterns
│   └── decisions.md            # Architectural decisions
└── decisions/                   # Important decisions log
    └── architectural_decisions.json
```

---

## 📊 **Note Types**

| Type | When to Use | Where Stored |
|------|-------------|--------------|
| `LEARNING` | Discovered something new | learnings.md |
| `IMPORTANT` | Critical info to remember | important_info.md |
| `TODO` | Personal tasks | todos.md |
| `DECISION` | Made a choice | Swarm brain |
| `WORK_LOG` | Session summary | work_log.md |
| `COORDINATION` | Inter-agent notes | notes.json |

---

## 🔍 **Searching Knowledge**

### **Search Your Notes:**

```python
memory = SwarmMemory("Agent-7")

# Search personal notes
notes = memory.agent_notes.search_notes("race condition")

# Get by type
learnings = memory.get_my_learnings()
```

### **Search Swarm Knowledge:**

```python
# Search entire swarm brain
results = memory.search_swarm_knowledge("autonomous loop")

# Get by agent
agent2_entries = memory.knowledge_base.get_by_agent("Agent-2")

# Get by category
decisions = memory.knowledge_base.get_by_category("decision")
```

---

## 🤝 **Sharing Protocol**

### **What to Share:**

✅ **Technical Breakthroughs** - Share with swarm  
✅ **Architectural Decisions** - Document rationale  
✅ **Best Practices** - Help other agents  
✅ **Pitfalls Avoided** - Prevent others from same mistakes  

### **What to Keep Personal:**

- Temporary work-in-progress notes
- Draft ideas (until validated)
- Personal todos

---

## 📋 **Daily Protocol**

### **Start of Session:**

1. Review personal notes from last session
2. Search swarm brain for relevant knowledge
3. Update status.json with notes section

### **During Session:**

1. Take notes as you learn
2. Record important decisions
3. Mark critical information

### **End of Session:**

1. Log session summary
2. Share key learnings with swarm
3. Update status.json
4. Clean up completed todos

---

## 🎯 **Best Practices**

### **Good Notes:**

✅ **Specific:** "Cross-process locks prevent race conditions in PyAutoGUI operations"  
✅ **Actionable:** "Use file-based locking with exponential backoff"  
✅ **Tagged:** ["concurrency", "messaging", "solution"]  

### **Bad Notes:**

❌ **Vague:** "Fixed something"  
❌ **Too detailed:** 500 lines of code dump  
❌ **Untagged:** No way to find later  

---

## 📊 **Status.json Integration**

### **Enhanced Status Format:**

```json
{
  "agent_id": "Agent-7",
  "status": "active",
  ...
  "agent_notes": {
    "notes_dir": "agent_workspaces/agent-7/notes",
    "total_notes": 25,
    "recent_notes": [...],
    "learnings_count": 8,
    "important_count": 5,
    "last_updated": "2025-10-13T15:30:00"
  },
  "swarm_contributions": {
    "knowledge_entries": 3,
    "decisions_recorded": 2,
    "learnings_shared": 5
  }
}
```

---

## 🐝 **Swarm Intelligence**

**The Goal:**
- Each agent accumulates knowledge
- Learnings shared with entire swarm
- Collective intelligence grows over time
- Context persists across sessions

**The Result:**
- Agents don't repeat mistakes
- Best practices propagate
- Decisions documented
- Swarm gets smarter with each session

---

## 🏆 **Implementation Status**

✅ **Agent Notes System** - Personal note-taking  
✅ **Knowledge Base** - Shared swarm brain  
✅ **Swarm Memory** - Unified API  
✅ **Protocol** - This document  
⏳ **CLI** - Future enhancement  
⏳ **Search UI** - Future enhancement  

---

**🧠 BUILD THE SWARM BRAIN - ONE NOTE AT A TIME!**

**Every learning shared makes the swarm smarter!**

