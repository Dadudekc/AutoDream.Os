# Message Batching Guide
## Combine Multiple Updates into Single Messages

**Created:** 2025-10-11  
**Status:** ACTIVE  
**Priority:** HIGH - Reduces Captain Inbox Load

---

## 🎯 **PURPOSE**

Message batching allows agents to combine multiple updates into a single consolidated message. This reduces Captain inbox overload during high-velocity autonomous execution while maintaining all update information.

**Benefits:**
- ✅ Reduces Captain message processing load
- ✅ Groups related updates together
- ✅ Maintains update ordering and context
- ✅ Works WITH message queue for safe delivery
- ✅ Automatic formatting and timestamps

---

## 🔄 **BATCH + QUEUE = BEST OF BOTH**

This system combines TWO powerful features:

### **Message Queue (Already Implemented)**
- Thread-safe FIFO queue
- Prevents race conditions
- Guarantees ordered delivery
- **Purpose:** Safe concurrent messaging

### **Message Batching (New)**
- Combines multiple updates
- Reduces message volume
- Consolidated formatting
- **Purpose:** Efficient communication

**Together:** Safe, efficient, high-velocity agent communication! 🚀

---

## 💡 **USAGE METHODS**

### **Method 1: Simplified Batch (Recommended)**

Combine multiple messages in a single command:

```bash
# Batch 3 updates into one message
python -m src.services.messaging_cli \
  --batch "Update 1: Task A complete" \
         "Update 2: Task B in progress" \
         "Update 3: Task C starting"

# With priority
python -m src.services.messaging_cli \
  --batch "Critical update 1" "Critical update 2" \
  --priority urgent

# From agent to Captain
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --batch "Phase 1 complete" "Phase 2 starting" "Phase 3 planned"
```

---

### **Method 2: Multi-Step Batch (Advanced)**

Build batch incrementally, then send:

```bash
# 1. Start batch
python -m src.services.messaging_cli --batch-start --agent Agent-7

# 2. Add messages (one at a time)
python -m src.services.messaging_cli --batch-add "Update 1: Files ported"
python -m src.services.messaging_cli --batch-add "Update 2: Tests passing"
python -m src.services.messaging_cli --batch-add "Update 3: V2 compliant"

# 3. Send consolidated batch
python -m src.services.messaging_cli --batch-send --priority urgent
```

---

### **Method 3: Batch Management Commands**

```bash
# Check batch status
python -m src.services.messaging_cli --batch-status --agent Agent-7

# Cancel batch without sending
python -m src.services.messaging_cli --batch-cancel --agent Agent-7
```

---

## 📋 **MESSAGE FORMAT**

Batched messages are automatically formatted for clarity:

```
[BATCHED UPDATES from Agent-7]
============================================================

📋 UPDATE 1/3:
Phase 1 complete: 12 files ported, 100% V2 compliant

📋 UPDATE 2/3:
Phase 2 starting: Integration testing in progress

📋 UPDATE 3/3:
Phase 3 planned: Documentation creation scheduled

============================================================
📊 BATCH SUMMARY: 3 updates consolidated
⏱️ Batch created: 16:30:15
⏱️ Batch sent: 16:35:42
```

---

## 🎯 **USE CASES**

### **Use Case 1: Multi-Phase Mission Updates**

Agent completing multiple phases:

```bash
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --batch "Phase 1: V2 compliance 100% complete" \
         "Phase 2: Integration tests all passing" \
         "Phase 3: Documentation created" \
  --priority regular
```

---

### **Use Case 2: Progress During Long Task**

Agent working on extended task:

```bash
# Start batch at beginning of work
python -m src.services.messaging_cli --batch-start --agent Agent-3

# Add updates as you progress
python -m src.services.messaging_cli --batch-add "10% complete: Setup done"
# ... continue working ...
python -m src.services.messaging_cli --batch-add "50% complete: Core work done"
# ... continue working ...
python -m src.services.messaging_cli --batch-add "90% complete: Testing in progress"

# Send when complete
python -m src.services.messaging_cli --batch-add "100% COMPLETE: All tasks done"
python -m src.services.messaging_cli --batch-send
```

---

### **Use Case 3: Multiple Quick Updates**

Agent completing several small tasks:

```bash
python -m src.services.messaging_cli \
  --batch "Fixed linter errors in module A" \
         "Updated documentation for feature B" \
         "Refactored helper function C" \
         "Added tests for component D"
```

---

## ⚙️ **TECHNICAL DETAILS**

### **Batch Storage**

- Batches stored in memory with thread-safe locking
- Each batch uniquely identified by `agent_id→recipient`
- Automatic cleanup after sending
- History saved to `runtime/message_batches/` for tracking

### **Integration with Message Queue**

When batch is sent:
1. Messages combined into consolidated format
2. Consolidated message added to message queue
3. Queue delivers via PyAutoGUI (coordinate-validated)
4. Thread-safe delivery guaranteed

### **Tags and Metadata**

Batched messages automatically tagged:
- `BATCHED` tag for identification
- `COORDINATION` tag for categorization
- Metadata includes batch creation/send timestamps

---

## 🔍 **BATCH STATUS**

Check current batch status anytime:

```bash
python -m src.services.messaging_cli --batch-status --agent Agent-7
```

**Output:**
```
✅ Active batch found:
   Agent: Agent-7
   Recipient: Agent-4
   Messages: 3
   Created: 2025-10-11T16:30:15
```

---

## 🚫 **CANCEL BATCH**

Cancel batch without sending:

```bash
python -m src.services.messaging_cli --batch-cancel --agent Agent-7
```

**Use when:**
- Decided not to send updates
- Want to start fresh batch
- Made mistake in batch composition

---

## 📊 **BATCH HISTORY**

All sent batches logged to `runtime/message_batches/`:

**File Format:** `batch_{agent_id}_{timestamp}.json`

**Contents:**
```json
{
  "agent_id": "Agent-7",
  "recipient": "Agent-4",
  "message_count": 3,
  "created_at": "2025-10-11T16:30:15",
  "sent_at": "2025-10-11T16:35:42",
  "individual_messages": [
    "Update 1 text",
    "Update 2 text",
    "Update 3 text"
  ],
  "consolidated_message": "Full consolidated message..."
}
```

---

## 🎯 **BEST PRACTICES**

1. **Use Simplified Batch** when you know all updates upfront
2. **Use Multi-Step Batch** for long-running tasks with incremental updates
3. **Group Related Updates** - keep batches focused on single topic/mission
4. **Reasonable Batch Size** - 2-5 updates is optimal, avoid 10+
5. **Clear Update Text** - each update should be independently understandable
6. **Send When Complete** - don't leave batches open indefinitely
7. **Use Priority Appropriately** - urgent for critical batches only

---

## ⚠️ **LIMITATIONS**

- **One Batch Per Agent→Recipient Pair** - Can't have multiple simultaneous batches from same agent to same recipient
- **Memory Storage** - Batches cleared on service restart (send before shutting down)
- **Manual Grouping** - Agent decides what to batch (no automatic batching)

---

## 💡 **AGENT-7 EXAMPLE (Real Usage)**

Agent-7's Team Beta completion could have used batching:

**Before (Multiple Messages):**
```
Message 1: "Phase 4 complete"
Message 2: "Phase 5 complete"
Message 3: "Phase 6 complete"
Message 4: "Phase 7 complete"
Message 5: "All 7 phases done, 12 files V2 compliant"
```

**After (Single Batched Message):**
```bash
python -m src.services.messaging_cli \
  --agent Agent-7 \
  --batch "Phase 4: V2 condensation complete (12/12 files compliant)" \
         "Phase 5: __init__.py refinement complete" \
         "Phase 6: Integration testing complete (all tests passed)" \
         "Phase 7: Documentation complete (devlog + integration docs)" \
         "PRIMARY ROLE COMPLETE: Team Beta 8/8 (100%), 37 files total"
```

**Result:** 5 updates → 1 consolidated message! 🎉

---

## 🚀 **PERFORMANCE IMPACT**

**Captain's Perspective:**
- **Before:** Process 5 individual messages (5x overhead)
- **After:** Process 1 consolidated message (1x overhead, 80% reduction!)

**Agent's Perspective:**
- **Before:** 5 separate CLI calls
- **After:** 1 CLI call with --batch flag (simpler!)

**System's Perspective:**
- Message queue handles both efficiently
- Coordinate validation still applies
- Thread safety maintained

---

## 📖 **EXAMPLES SUMMARY**

```bash
# Quick 3-update batch
python -m src.services.messaging_cli --batch "Update 1" "Update 2" "Update 3"

# Incremental batch building
python -m src.services.messaging_cli --batch-start
python -m src.services.messaging_cli --batch-add "First update"
python -m src.services.messaging_cli --batch-add "Second update"
python -m src.services.messaging_cli --batch-send

# Check what's in batch
python -m src.services.messaging_cli --batch-status

# Cancel if needed
python -m src.services.messaging_cli --batch-cancel

# Agent-specific batching
python -m src.services.messaging_cli --agent Agent-7 --batch "Update 1" "Update 2"
```

---

## 🐝 **CIVILIZATION-BUILDING IMPACT**

**Benefits for Swarm:**
- Reduces Captain processing overhead
- Enables higher agent velocity
- Maintains communication quality
- Preserves all update information
- Improves swarm coordination efficiency

**When to Use:**
- ✅ Multiple related updates
- ✅ High-velocity execution
- ✅ Long-running tasks with checkpoints
- ✅ Multi-phase missions

**When NOT to Use:**
- ❌ Single update (just use regular message)
- ❌ Critical urgent alerts (send immediately)
- ❌ Unrelated updates (separate messages better)

---

**Status:** Fully implemented and tested  
**Integration:** Works with message queue system  
**Performance:** 80% reduction in message volume possible  
**Recommended:** Use for multi-update scenarios  

🐝 **WE. ARE. SWARM.** ⚡

