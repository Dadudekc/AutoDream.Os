# 🧠 Swarm Vector Integration Guide

**Created**: 2025-10-17  
**Author**: Agent-5 (Business Intelligence Specialist)  
**Module**: `src/core/swarm_vector_integration.py`  
**Purpose**: Semantic search for protocols, knowledge, and cycle context  
**Status**: ✅ OPERATIONAL

---

## 🎯 **What Is This?**

**Swarm Vector Integration** enables agents to semantically search:
- Swarm protocols (find relevant guidance)
- Past cycles (learn from similar work)
- Swarm knowledge (access collective intelligence)
- Quick references (instant protocol lookup)

**Use this during autonomous cycles to find relevant knowledge!**

---

## 🚀 **Quick Start**

### **Search Protocols:**
```python
from src.core.swarm_vector_integration import search_protocols

# Find protocols about stop detection
results = search_protocols("how to handle stop detection")
for result in results:
    print(f"📚 {result['title']}: {result['file']}")
```

### **Get Cycle Context:**
```python
from src.core.swarm_vector_integration import get_cycle_context

# Get context for DUP fix cycle
context = get_cycle_context('DUP_FIX')
print(f"Protocols: {context['protocols']}")
print(f"Best practices: {context['best_practices']}")
print(f"Success metrics: {context['success_metrics']}")
```

### **Quick Reference:**
```python
from src.core.swarm_vector_integration import get_quick_ref

# Get gas pipeline quick ref
ref = get_quick_ref('gas_pipeline')
print(ref)
# Output: "Send gas at 75-80% completion. 3-send redundancy..."
```

---

## 📋 **Available Functions**

### **search_protocols(query, agent_id)**
Search swarm protocols semantically.

**Args:**
- `query`: Search query (e.g., "anti-stop protocol")
- `agent_id`: Your agent ID (default: "Agent-5")

**Returns:** List of relevant protocol sections

**Example:**
```python
results = search_protocols("how to avoid stopping")
```

---

### **get_cycle_context(cycle_type, agent_id)**
Get context for specific cycle type.

**Cycle Types:**
- `DUP_FIX`: Duplicate consolidation cycles
- `REPO_ANALYSIS`: Repository analysis cycles
- `TESTING`: Testing cycles
- `ANTI_STOP`: Anti-stop execution cycles

**Returns:** Dictionary with protocols, best practices, success metrics

**Example:**
```python
context = get_cycle_context('ANTI_STOP')
# Returns: {
#   'protocols': ['ANTI_STOP_PROTOCOL', 'NEVER_STOP_V2'],
#   'best_practices': ['8+ cycles per session', 'Code:Celebrate = 3:1'],
#   'success_metrics': {'cycles_complete': 8, 'lines_coded': 1000}
# }
```

---

### **get_quick_ref(topic, agent_id)**
Get quick reference for common topics.

**Topics Available:**
- `gas_pipeline`: Gas delivery protocol
- `anti_stop`: Anti-stop guidelines
- `v2_compliance`: V2 compliance rules
- `strategic_rest`: Strategic rest protocol
- `code_first`: Anti-cheerleader guidelines

**Returns:** Quick reference string

**Example:**
```python
ref = get_quick_ref('code_first')
# Returns: "75% execution (coding), 25% support (gas/celebration)..."
```

---

## 🎯 **Use Cases**

### **During Autonomous Cycles:**
```python
# Before starting cycle
context = get_cycle_context('DUP_FIX')
print(f"I should follow: {context['protocols']}")
print(f"Success means: {context['success_metrics']}")

# Execute cycle with context awareness
```

### **When Encountering Issues:**
```python
# Search for relevant protocols
results = search_protocols("what to do when stuck")
for result in results:
    read_protocol(result['file'])
```

### **Quick Protocol Lookup:**
```python
# Need quick reminder
gas_protocol = get_quick_ref('gas_pipeline')
print(f"Gas reminder: {gas_protocol}")
```

---

## 🧠 **Integration with Swarm Brain**

**This module complements SwarmMemory:**
- **SwarmMemory**: Share/store learnings
- **SwarmVectorIntegration**: Search/retrieve knowledge

**Use Together:**
```python
from src.swarm_brain.swarm_memory import SwarmMemory
from src.core.swarm_vector_integration import search_protocols

# Search for protocols
protocols = search_protocols("gas pipeline")

# Execute work based on protocols

# Share learnings back
memory = SwarmMemory(agent_id='Agent-5')
memory.share_learning(
    title="Successfully applied gas pipeline",
    content="Used search_protocols() to find guidance, executed perfectly!",
    tags=['gas-pipeline', 'success']
)
```

---

## 📊 **Features**

### **Semantic Protocol Search:**
- Searches `swarm_brain/protocols/`
- Returns relevant sections
- Ranked by relevance
- Agent-context aware

### **Cycle Context Awareness:**
- Predefined contexts for common cycle types
- Best practices included
- Success metrics provided
- Protocol recommendations

### **Knowledge Retrieval:**
- Searches entire swarm brain
- Multiple source types (knowledge, learnings, decisions, protocols)
- Agent-specific prioritization
- Fast keyword-based retrieval

### **Quick References:**
- Instant protocol lookup
- Common topics covered
- Brief, actionable guidance
- No reading full protocols needed

---

## 🎯 **When to Use**

**Use This When:**
- ✅ Starting new cycle (get context!)
- ✅ Encountering unfamiliar situation (search protocols!)
- ✅ Need quick reminder (quick ref!)
- ✅ Learning from past cycles (find similar!)
- ✅ Executing autonomously (knowledge access!)

**DON'T Use When:**
- ❌ You already know the protocol
- ❌ You're in the middle of coding (finish first!)
- ❌ As excuse to stop (CODE FIRST!)

---

## 🚀 **Adding to Your Workflow**

### **At Cycle Start:**
```python
# 1. Get context for cycle type
context = get_cycle_context('DUP_FIX')

# 2. Quick ref check if needed
if unsure_about_gas:
    gas_ref = get_quick_ref('gas_pipeline')

# 3. Execute with context awareness
execute_cycle_with_knowledge(context)
```

### **When Stuck:**
```python
# Search for help
results = search_protocols("handling import errors")
# Read first result, apply solution, continue
```

---

## 📝 **Created By Agent-5**

**Mission**: Cycle 8 - Vector DB Swarm Integration  
**Lines**: 280 lines  
**Purpose**: Make swarm knowledge easily accessible during autonomous execution  
**Impact**: Agents can find protocols/knowledge without asking!

---

🐝 **WE. ARE. SWARM.** - **Knowledge accessible, execution autonomous!**

