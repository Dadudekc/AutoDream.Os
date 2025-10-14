# 🧠 Swarm Brain Access Guide - AGENT QUICK REFERENCE

**Version**: 1.0  
**Last Updated**: 2025-10-14  
**Author**: Agent-5 (Business Intelligence & Team Beta Leader)

---

## 🎯 WHAT IS THE SWARM BRAIN?

The **Swarm Brain** is our **centralized knowledge repository** where all agents can:
- 📚 **Store** important learnings, decisions, and protocols
- 🔍 **Search** collective knowledge instantly
- 🤝 **Share** discoveries with the entire swarm
- 📝 **Access** protocols and best practices

**Location**: `swarm_brain/` directory

---

## 🚀 QUICK START FOR AGENTS

### **Python API Usage**:

```python
from src.swarm_brain.swarm_memory import SwarmMemory

# Initialize (replace 'Agent-X' with your agent ID)
memory = SwarmMemory(agent_id='Agent-5')

# 1. SEARCH SWARM KNOWLEDGE
results = memory.search_swarm_knowledge("memory leaks")
for entry in results:
    print(f"📚 {entry.title} by {entry.author}")
    print(entry.content)

# 2. SHARE A LEARNING
memory.share_learning(
    title="LRU Cache Pattern for Memory Safety",
    content="Always implement LRU eviction for unbounded collections...",
    tags=["memory-safety", "performance", "pattern"]
)

# 3. RECORD A DECISION
memory.record_decision(
    title="Use 3-Module Split for 700+ Line Files",
    decision="Files >700 lines split into 3 modules ≤300 lines each",
    rationale="Maintains V2 compliance, improves maintainability",
    participants=["Agent-5", "Captain-4"]
)

# 4. TAKE PERSONAL NOTES
memory.take_note(
    content="Remember to always validate file operations",
    note_type=NoteType.IMPORTANT
)

# 5. LOG SESSION
memory.log_session("Completed memory leak audit - found 3 issues, fixed all")
```

---

## 📁 SWARM BRAIN STRUCTURE

```
swarm_brain/
├── knowledge_base.json          # Central knowledge storage
├── protocols/                   # Protocols & guides
│   ├── NOTE_TAKING_PROTOCOL.md
│   └── SWARM_BRAIN_ACCESS_GUIDE.md (this file)
├── shared_learnings/            # Shared knowledge
│   ├── learning.md
│   ├── decision.md
│   └── technical.md
└── decisions/                   # Swarm decisions
```

---

## 🔍 HOW TO SEARCH KNOWLEDGE

### **Search by Topic**:
```python
# Search for specific topics
results = memory.search_swarm_knowledge("V2 compliance")
results = memory.search_swarm_knowledge("refactoring patterns")
results = memory.search_swarm_knowledge("memory leaks")
```

### **Get by Category**:
```python
# Get all entries in a category
technical = memory.knowledge_base.get_by_category("technical")
protocols = memory.knowledge_base.get_by_category("protocol")
learnings = memory.knowledge_base.get_by_category("learning")
```

### **Get by Agent**:
```python
# See what a specific agent contributed
agent5_knowledge = memory.knowledge_base.get_by_agent("Agent-5")
```

---

## 📚 KNOWLEDGE CATEGORIES

| Category | Purpose | Examples |
|----------|---------|----------|
| **technical** | Technical solutions, patterns, code | "LRU Cache Implementation", "Module Splitting Pattern" |
| **protocol** | Protocols, procedures, guidelines | "V2 Compliance Protocol", "Git Commit Standards" |
| **learning** | Lessons learned, insights | "What Works: Incremental Refactoring", "Avoid: Massive File Changes" |
| **decision** | Swarm decisions, rationale | "Split vs Consolidate Decision", "Architecture Choices" |

---

## 🎯 WHEN TO USE SWARM BRAIN

### **✅ DO USE SWARM BRAIN FOR**:

1. **Sharing Important Discoveries**
   - Found a critical bug pattern? Share it!
   - Discovered a useful refactoring technique? Share it!
   - Created a helpful tool? Document it!

2. **Recording Swarm Decisions**
   - Architecture choices
   - Protocol changes
   - Task prioritization decisions

3. **Documenting Learnings**
   - What worked well
   - What didn't work
   - Best practices discovered

4. **Accessing Protocols**
   - Check before starting work
   - Reference during execution
   - Update when improved

### **❌ DON'T USE SWARM BRAIN FOR**:

1. Temporary notes (use personal agent notes)
2. Task-specific details (use task comments)
3. Chat messages (use messaging system)
4. File-specific documentation (use file docstrings)

---

## 🛠️ COMMON USE CASES

### **Use Case 1: Before Starting a Task**
```python
# Search for similar work
memory = SwarmMemory(agent_id='Agent-5')
similar_work = memory.search_swarm_knowledge("file refactoring")

# Check for relevant protocols
protocols = memory.knowledge_base.get_by_category("protocol")
```

### **Use Case 2: After Completing a Task**
```python
# Share your learning
memory.share_learning(
    title="Effective File Refactoring Strategy",
    content="Split large files by functional responsibility, not line count...",
    tags=["refactoring", "v2-compliance", "best-practice"]
)

# Log your session
memory.log_session("Refactored autonomous_task_engine.py - 797→3 modules")
```

### **Use Case 3: Multi-Agent Decision**
```python
# Record a decision
memory.record_decision(
    title="Analytics Framework Architecture",
    decision="9-module framework with clean separation",
    rationale="Maintains V2 compliance while enabling feature growth",
    participants=["Agent-2", "Agent-5"]
)
```

---

## 📊 SWARM BRAIN TOOLS

### **Available via Toolbelt**:
```bash
# Search swarm knowledge (coming soon)
python -m tools_v2.toolbelt swarm.search --query "memory leaks"

# Add knowledge entry (coming soon)
python -m tools_v2.toolbelt swarm.add --title "..." --content "..."

# View swarm stats (coming soon)
python -m tools_v2.toolbelt swarm.stats
```

---

## 🔥 AGENT RESPONSIBILITIES

### **Every Agent Should**:

1. **📖 READ Before Acting**
   - Search swarm brain for similar work
   - Check protocols before starting
   - Learn from others' experiences

2. **✍️ WRITE After Acting**
   - Share important discoveries
   - Document lessons learned
   - Record decisions made

3. **🔄 UPDATE Continuously**
   - Keep protocols current
   - Refine best practices
   - Improve documentation

4. **🤝 COLLABORATE**
   - Reference others' work
   - Build on existing knowledge
   - Credit contributors

---

## 📝 BEST PRACTICES

### **Writing Good Knowledge Entries**:

✅ **DO**:
- Use clear, descriptive titles
- Provide context and examples
- Add relevant tags
- Include code snippets when helpful
- Credit sources/contributors

❌ **DON'T**:
- Write vague titles ("Fixed stuff")
- Skip context ("Did the thing")
- Forget tags (harder to find)
- Duplicate existing knowledge

### **Example Good Entry**:
```python
memory.share_learning(
    title="LRU Cache Pattern for Preventing Memory Leaks",
    content="""
    When implementing caches, ALWAYS add eviction policies:
    
    ```python
    from functools import lru_cache
    
    @lru_cache(maxsize=128)  # ✅ Bounded cache
    def expensive_function(arg):
        return result
    ```
    
    Prevents unbounded memory growth in long-running processes.
    Tested in autonomous_task_engine.py - reduced memory usage by 40%.
    """,
    tags=["memory-safety", "caching", "pattern", "performance"]
)
```

---

## 🚀 QUICK REFERENCE COMMANDS

```python
# Import
from src.swarm_brain.swarm_memory import SwarmMemory, NoteType

# Initialize
memory = SwarmMemory(agent_id='your-agent-id')

# Search
results = memory.search_swarm_knowledge("query")

# Share Learning
memory.share_learning(title, content, tags)

# Record Decision  
memory.record_decision(title, decision, rationale, participants)

# Take Note
memory.take_note(content, NoteType.IMPORTANT)

# Log Session
memory.log_session(summary)
```

---

## 🎯 SUCCESS METRICS

**Swarm Brain is successful when**:
- ✅ Agents find solutions faster (search before building)
- ✅ Patterns are reused (not reinvented)
- ✅ Knowledge grows organically (all agents contribute)
- ✅ New agents onboard quickly (documented knowledge)
- ✅ Decisions are traceable (recorded rationale)

---

## 📖 ADDITIONAL RESOURCES

- **Note Taking Protocol**: `swarm_brain/protocols/NOTE_TAKING_PROTOCOL.md`
- **Knowledge Base API**: `src/swarm_brain/knowledge_base.py`
- **Agent Notes API**: `src/swarm_brain/agent_notes.py`
- **Swarm Memory API**: `src/swarm_brain/swarm_memory.py`

---

## 🐝 **WE. ARE. SWARM.**

**The Swarm Brain makes us smarter together.**

Every agent's knowledge strengthens the entire swarm.  
Search before you build. Share after you succeed.  
Learn from the collective. Contribute to the collective.

**🔥 USE THE SWARM BRAIN - IT'S YOUR SUPERPOWER! 🧠**

---

**Agent-5 (Business Intelligence & Team Beta Leader)**  
**Documentation & Knowledge Systems Specialist**

