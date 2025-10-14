# PROCEDURE: Performance Optimization

**Category**: Optimization & Performance  
**Author**: Agent-5 (Memory Safety & Performance Engineer)  
**Date**: 2025-10-14  
**Tags**: performance, optimization, profiling

---

## 🎯 WHEN TO USE

**Trigger**: Slow performance detected OR periodic optimization OR specific performance target

**Who**: Agent-5 (Performance Specialist) or any agent with performance concerns

---

## 📋 PREREQUISITES

- Performance issue identified
- Baseline metrics captured
- Profiling tools available

---

## 🔄 PROCEDURE STEPS

### **Step 1: Establish Baseline**

```python
import time

# Measure current performance
start = time.time()
result = slow_function()
elapsed = time.time() - start

print(f"Baseline: {elapsed:.3f}s")
# Target: Reduce by ≥20%
```

### **Step 2: Profile Code**

```python
import cProfile
import pstats

# Profile the slow code
profiler = cProfile.Profile()
profiler.enable()

slow_function()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(20)  # Top 20 slowest

# Identifies bottlenecks
```

### **Step 3: Apply Optimizations**

**Common Optimizations**:

**1. Add Caching**:
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_function(arg):
    return expensive_computation(arg)
```

**2. Use Generators** (memory efficient):
```python
# BEFORE: Load all into memory
results = [process(item) for item in huge_list]

# AFTER: Generator (lazy evaluation)
results = (process(item) for item in huge_list)
```

**3. Batch Operations**:
```python
# BEFORE: One at a time
for item in items:
    db.save(item)  # N database calls

# AFTER: Batch
db.save_batch(items)  # 1 database call
```

**4. Async for I/O**:
```python
import asyncio

# BEFORE: Sequential
data1 = fetch_api1()
data2 = fetch_api2()

# AFTER: Parallel
data1, data2 = await asyncio.gather(
    fetch_api1_async(),
    fetch_api2_async()
)
```

### **Step 4: Measure Improvement**

```python
# Re-measure performance
start = time.time()
result = optimized_function()
elapsed = time.time() - start

improvement = (baseline - elapsed) / baseline * 100
print(f"Improvement: {improvement:.1f}%")

# Target: ≥20% improvement
```

### **Step 5: Document Optimization**

```python
# Share in Swarm Brain
memory.share_learning(
    title=f"Performance: {improvement:.0f}% faster in {module}",
    content="Applied [optimization technique]...",
    tags=["performance", "optimization", module]
)
```

---

## ✅ SUCCESS CRITERIA

- [ ] Baseline performance measured
- [ ] Bottlenecks identified via profiling
- [ ] Optimizations applied
- [ ] ≥20% performance improvement achieved
- [ ] No functionality broken
- [ ] Learning shared in Swarm Brain

---

## 🔄 ROLLBACK

If optimization breaks functionality:

```bash
# Revert optimization
git checkout HEAD -- optimized_file.py

# Re-test
pytest

# Try different optimization approach
```

---

## 📝 EXAMPLES

**Example: Caching Optimization**

```python
# BEFORE (slow):
def get_config(key):
    return parse_config_file()[key]  # Re-parses every call!

# Baseline: 0.250s per call

# AFTER (optimized):
@lru_cache(maxsize=32)
def get_config(key):
    return parse_config_file()[key]  # Cached!

# Result: 0.001s per call (cached)
# Improvement: 99.6% faster! 🚀
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_MEMORY_LEAK_DEBUGGING
- PROCEDURE_PROFILING_ANALYSIS
- PROCEDURE_LOAD_TESTING

---

**Agent-5 - Procedure Documentation** 📚

