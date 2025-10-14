# PROCEDURE: Contributing to Swarm Brain

**Category**: Knowledge Management  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: swarm-brain, knowledge-sharing, documentation

---

## 🎯 WHEN TO USE

**Trigger**: After completing work OR discovering something useful OR solving a problem

**Who**: ALL agents (encouraged!)

---

## 📋 PREREQUISITES

- Swarm Brain system active
- Python environment active
- Knowledge to share

---

## 🔄 PROCEDURE STEPS

### **Step 1: Initialize Swarm Memory**

```python
from src.swarm_brain.swarm_memory import SwarmMemory

# Initialize with your agent ID
memory = SwarmMemory(agent_id='Agent-5')
```

### **Step 2: Share Your Learning**

```python
# Document what you learned
memory.share_learning(
    title="Clear, Descriptive Title",
    content="""
    Detailed explanation of what you learned.
    
    Include:
    - Context (what you were doing)
    - Discovery (what you found)
    - Solution (how you solved it)
    - Code examples (if applicable)
    """,
    tags=["relevant", "tags", "for", "search"]
)
```

### **Step 3: Verify Storage**

```bash
# Check Swarm Brain updated
cat swarm_brain/knowledge_base.json | python -m json.tool | grep "your_title"

# Should see your entry
```

### **Step 4: Make It Searchable**

Other agents can now find your knowledge:
```python
# Any agent can search
results = memory.search_swarm_knowledge("your topic")

# Will find your contribution!
```

---

## ✅ SUCCESS CRITERIA

- [ ] Knowledge added to swarm_brain/knowledge_base.json
- [ ] Entry includes title, content, author, tags
- [ ] Searchable by other agents
- [ ] Saved to category file (swarm_brain/shared_learnings/)

---

## 🔄 ROLLBACK

Cannot easily remove knowledge (intentionally permanent), but can:

```python
# Add correction/update
memory.share_learning(
    title="CORRECTION: [Original Title]",
    content="Updated information: ...",
    tags=["correction", original_tags]
)
```

---

## 📝 EXAMPLES

**Example 1: Sharing a Pattern**

```python
from src.swarm_brain.swarm_memory import SwarmMemory

memory = SwarmMemory(agent_id='Agent-5')

memory.share_learning(
    title="LRU Cache Pattern for Memory Safety",
    content="""
    When implementing caches, ALWAYS use LRU eviction:
    
    ```python
    from functools import lru_cache
    
    @lru_cache(maxsize=128)
    def expensive_function(arg):
        return compute_expensive_result(arg)
    ```
    
    Prevents unbounded memory growth.
    Tested in message_queue - reduced memory by 40%.
    """,
    tags=["memory-safety", "caching", "pattern", "performance"]
)

# Output:
# ✅ Knowledge entry added: LRU_cache_pattern by Agent-5
```

**Example 2: Recording a Decision**

```python
memory.record_decision(
    title="Use 3-Module Split for 700+ Line Files",
    decision="Files >700 lines split into 3 modules ≤300 lines each",
    rationale="Maintains V2 compliance, improves maintainability, clear separation",
    participants=["Agent-5", "Captain-4"]
)

# Output:
# ✅ Decision recorded: 3_module_split_decision
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_SWARM_BRAIN_SEARCH (finding knowledge)
- PROCEDURE_DOCUMENTATION_UPDATE (updating docs)
- PROCEDURE_KNOWLEDGE_REVIEW (reviewing contributions)

---

## 💡 TIPS

**What to Share**:
- ✅ Useful patterns discovered
- ✅ Problems solved
- ✅ Efficiency improvements
- ✅ Important decisions
- ✅ Gotchas/warnings

**What NOT to Share**:
- ❌ Trivial information
- ❌ Temporary notes
- ❌ Agent-specific data
- ❌ Redundant knowledge

---

**Agent-5 - Procedure Documentation** 📚

