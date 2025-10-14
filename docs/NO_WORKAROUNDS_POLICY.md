# 🚫 NO WORKAROUNDS POLICY
**Version**: 1.0  
**Date**: 2025-10-13  
**Priority**: CRITICAL  
**Status**: ACTIVE POLICY

---

## 🎯 **CORE PRINCIPLE**

### **"FIX THE ORIGINAL ARCHITECTURE - NO WORKAROUNDS!"**

**Why**: The human won't know about workarounds. They create hidden technical debt and confusion.

---

## ❌ **WHAT IS NOT ACCEPTABLE**

### **Workarounds Include**:
1. ❌ Creating temporary scripts to bypass broken systems
2. ❌ Building parallel systems instead of fixing existing ones
3. ❌ Hardcoding values to avoid configuration issues
4. ❌ Copy-pasting code instead of fixing imports
5. ❌ Creating wrapper functions to hide bugs
6. ❌ Documenting "known issues" instead of fixing them
7. ❌ Building new tools when existing tools are broken

### **Why Workarounds Fail**:
- Human doesn't know they exist
- Future agents get confused
- Technical debt compounds
- Original issue never gets fixed
- System becomes fragile
- Maintenance becomes impossible

---

## ✅ **WHAT IS ACCEPTABLE**

### **Proper Fixes Include**:
1. ✅ **Fix the root cause** in original architecture
2. ✅ **Update broken imports** at the source
3. ✅ **Repair broken systems** where they live
4. ✅ **Refactor properly** following SOLID principles
5. ✅ **Document the fix** in the original code
6. ✅ **Test the repair** thoroughly
7. ✅ **Remove deprecated code** cleanly

### **Process for Fixes**:
1. **Identify root cause** (not symptoms)
2. **Fix at the source** (not downstream)
3. **Test thoroughly** (ensure it works)
4. **Document the fix** (in code + changelog)
5. **Verify no workarounds remain** (clean up)

---

## 🔧 **EXAMPLES**

### ❌ **WRONG** (Workaround):
```python
# messaging_cli.py broken? Create new file!
# File: tools/send_messages_workaround.py

def send_message_workaround(agent, msg):
    # Bypass broken messaging_cli.py
    # Copy-paste code here...
```

**Problem**: Human doesn't know this exists. Original issue unfixed.

### ✅ **RIGHT** (Proper Fix):
```python
# Fix the actual issue in messaging_cli.py
# Move sys.path.insert BEFORE imports

import sys
from pathlib import Path

# CRITICAL: Add to path BEFORE imports  
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# NOW import works!
from src.services.messaging_cli_handlers import ...
```

**Result**: Original architecture fixed. No hidden workarounds.

---

## 📋 **AGENT CHECKLIST**

### **Before Creating ANY File, Ask**:
- [ ] Is this fixing the root cause?
- [ ] Or am I working around a broken system?
- [ ] Will the human know this exists?
- [ ] Am I leaving technical debt?
- [ ] Should I fix the original instead?

### **If Tempted to Create Workaround**:
1. **STOP** - Don't create it
2. **IDENTIFY** - What's the real problem?
3. **FIX** - Repair the original architecture
4. **TEST** - Verify the fix works
5. **DOCUMENT** - Update the original file

---

## 🎯 **POLICY ENFORCEMENT**

### **All Agents Must**:
1. ✅ Fix original architecture FIRST
2. ✅ Only create new files when truly needed
3. ✅ Document all fixes in original code
4. ✅ Remove workarounds if found
5. ✅ Ask Captain if unsure

### **Captain Will**:
1. ✅ Reject workaround solutions
2. ✅ Require root cause fixes
3. ✅ Verify no hidden technical debt
4. ✅ Enforce this policy strictly

---

## 🚨 **EXAMPLES FROM TODAY**

### ❌ **What I Almost Did** (Workaround):
Created `tools/send_agent_messages.py` to bypass broken messaging_cli.py

### ✅ **What I Did Instead** (Proper Fix):
Fixed the import error IN messaging_cli.py by moving sys.path.insert before imports

**Result**: Original system works. No workaround needed. Human understands the codebase.

---

## 📖 **REMEMBER**

### **Key Principles**:
1. **"Fix don't patch"** - Repair root causes
2. **"Human must understand"** - No hidden systems
3. **"Original architecture first"** - Respect the design
4. **"Technical debt = future failure"** - Pay it down now
5. **"Clean code > quick hacks"** - Quality matters

### **When In Doubt**:
- **Ask**: "Will the human know about this?"
- **Ask**: "Am I fixing or bypassing?"
- **Ask**: "Is this the root cause?"
- **If unsure**: Ask Captain before proceeding

---

🚫 **NO WORKAROUNDS - FIX THE ORIGINAL ARCHITECTURE!** 🚫

🐝 **WE. ARE. SWARM.** ⚡

---

**Policy Status**: ACTIVE  
**Enforcement**: IMMEDIATE  
**Applies To**: ALL AGENTS  
**No Exceptions**: Without Captain approval

