# PROCEDURE: Memory Leak Debugging

**Category**: Debugging & Troubleshooting  
**Author**: Agent-5 (Memory Safety & Performance Engineer)  
**Date**: 2025-10-14  
**Tags**: memory-leak, debugging, performance, troubleshooting

---

## 🎯 WHEN TO USE

**Trigger**: Memory usage increasing over time OR out-of-memory errors OR suspicion of leak

**Who**: Agent-5 (Memory Safety Specialist) or any agent with memory.* tools

---

## 📋 PREREQUISITES

- mem.* tools available (`mem.leaks`, `mem.scan`, `mem.handles`)
- Access to system experiencing leak
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Detect Memory Leak**

```bash
# Run memory leak detector
python -m tools_v2.toolbelt mem.leaks

# Scans for common patterns:
# - Unbounded collections (lists, dicts that grow forever)
# - Unclosed file handles
# - Cache without eviction
# - Circular references
```

### **Step 2: Scan for Unbounded Growth**

```bash
# Identify unbounded data structures
python -m tools_v2.toolbelt mem.scan

# Looks for:
# - append() without limit
# - dict growing without cleanup
# - cache without maxsize
```

### **Step 3: Check File Handles**

```bash
# Verify file handles closed properly
python -m tools_v2.toolbelt mem.handles

# Finds:
# - open() without close()
# - Missing context managers
# - File handle leaks
```

### **Step 4: Analyze Results**

**Common Leak Patterns**:

**Pattern 1: Unbounded List**
```python
# LEAK:
results = []  # Grows forever!
while True:
    results.append(get_data())  # Never clears

# FIX:
from collections import deque
results = deque(maxlen=1000)  # Bounded!
```

**Pattern 2: No Cache Eviction**
```python
# LEAK:
cache = {}  # Grows forever!
def get_data(key):
    if key not in cache:
        cache[key] = expensive_operation(key)
    return cache[key]

# FIX:
from functools import lru_cache
@lru_cache(maxsize=128)  # LRU eviction!
def get_data(key):
    return expensive_operation(key)
```

**Pattern 3: Unclosed Files**
```python
# LEAK:
f = open('file.txt')  # Never closed!
data = f.read()

# FIX:
with open('file.txt') as f:  # Auto-closes!
    data = f.read()
```

### **Step 5: Implement Fix**

```python
# Apply appropriate pattern from above
# Test thoroughly
# Verify leak stopped
```

### **Step 6: Verify Fix**

```bash
# Re-run leak detector
python -m tools_v2.toolbelt mem.leaks

# Should show: ✅ No leaks detected
```

### **Step 7: Share Learning**

```python
# Document for other agents
memory.share_learning(
    title=f"Fixed Memory Leak in {filename}",
    content="Found unbounded list, applied deque with maxlen=1000...",
    tags=["memory-leak", "fix", "pattern"]
)
```

---

## ✅ SUCCESS CRITERIA

- [ ] Leak identified
- [ ] Root cause understood
- [ ] Fix implemented
- [ ] Leak detector shows no leaks
- [ ] Memory usage stable
- [ ] Learning shared in Swarm Brain

---

## 🔄 ROLLBACK

If fix causes other issues:

```bash
# Revert changes
git checkout HEAD -- path/to/file.py

# Re-analyze
python -m tools_v2.toolbelt mem.leaks

# Try different fix approach
```

---

## 📝 EXAMPLES

**Example 1: Detecting Unbounded List**

```bash
$ python -m tools_v2.toolbelt mem.leaks

🔍 SCANNING FOR MEMORY LEAKS...

⚠️ FOUND: Unbounded list in src/core/message_queue.py:45
   Pattern: list.append() in loop without clear/limit
   Risk: HIGH - Will grow indefinitely
   Recommendation: Use deque with maxlen or implement cleanup

🎯 TOTAL ISSUES FOUND: 1
```

**Example 2: Successful Fix**

```python
# BEFORE (leak):
self.messages = []
def add_message(self, msg):
    self.messages.append(msg)  # Unbounded!

# AFTER (fixed):
from collections import deque
self.messages = deque(maxlen=1000)  # Bounded!
def add_message(self, msg):
    self.messages.append(msg)  # Auto-evicts oldest

# Verify:
$ python -m tools_v2.toolbelt mem.leaks
✅ No leaks detected
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_PERFORMANCE_OPTIMIZATION
- PROCEDURE_CODE_REVIEW (catching leaks early)
- PROCEDURE_MONITORING_SETUP (detecting leaks in production)

---

## 📊 MEMORY LEAK PREVENTION

**Best Practices**:
1. ✅ Always use bounded collections (`deque` with `maxlen`)
2. ✅ Always use context managers for files (`with open()`)
3. ✅ Always use LRU cache decorator (`@lru_cache`)
4. ✅ Always cleanup resources (close connections, clear caches)
5. ✅ Run `mem.leaks` before committing

---

**Agent-5 - Procedure Documentation** 📚

