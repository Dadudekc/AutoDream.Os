# DUP-008: Data Processing Migration Guide

**For Future Agents:** How to migrate existing code to use unified processors

---

## 🎯 **MIGRATION PATHS:**

### **1. Migrate process_batch() Calls:**

**Old Code:**
```python
# From various files
async def process_batch(items, batch_size=100):
    # Custom implementation
    pass
```

**New Code:**
```python
from src.core.data_processing import UnifiedBatchProcessor

processor = UnifiedBatchProcessor(batch_size=100)
result = await processor.process_batch(items, processor_func=my_func)
```

### **2. Migrate process_data() Calls:**

**Old Code:**
```python
async def process_data(data, transformer=None):
    # Custom implementation
    pass
```

**New Code:**
```python
from src.core.data_processing import UnifiedDataProcessor

processor = UnifiedDataProcessor([transformer1, transformer2])
result = await processor.process_data(data)
```

### **3. Migrate process_results() Calls:**

**Old Code:**
```python
def process_results(results, context=None):
    # Custom implementation
    pass
```

**New Code:**
```python
from src.core.data_processing import UnifiedResultsProcessor

processor = UnifiedResultsProcessor(validators=[validator1])
result = processor.process_results(results, context, result_type="validation")
```

---

## ✅ **BACKWARD COMPATIBILITY:**

**Convenience functions available:**
```python
from src.core.data_processing import process_batch, process_data, process_results

# These work like the old functions for easy migration
result = await process_batch(items, processor_func)
result = await process_data(data, transformer)
result = process_results(results, context)
```

---

**Agent-1 - Migration Guide Complete!** 🐝

