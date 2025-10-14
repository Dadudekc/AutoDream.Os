# V2 Architecture Best Practices
**Mission:** C-059-7 (Autonomous Claim)  
**Agent:** Agent-2 (Architecture & Design Specialist)  
**Date:** 2025-10-11  
**Status:** ✅ COMPLETE

---

## 🎯 CORE PRINCIPLES

### 1. Keep Files Under 400 Lines
**Target:** 300-320 lines (75-80% of limit)  
**Reason:** Buffer for future enhancements

### 2. Single Responsibility Per File
**Test:** Can you describe in ONE sentence?  
**If "and" appears → Extract**

### 3. Extract Early, Not Late
**Extract at:** 300 lines  
**Not at:** 399 lines  
**Reason:** Better module boundaries

---

## 🏗️ PROVEN PATTERNS

### Modular CLI (from C-058)
- Entry point + Registry + Runner + Help
- 492 lines across 4 modules
- 9 tools unified
- 9.5/10 quality

### Registry-Driven Design
- Metadata in registry
- Behavior driven by metadata
- Easy to extend
- Self-documenting

### Architecture-First Development
- Design → Implement → QA
- Clear specs prevent rework
- QA by architect ensures fidelity
- C-058: Zero rework, 98% adherence

---

## 💎 AUTONOMOUS SWARM PATTERNS

### Direct Agent Coordination
- Agent → Agent (not Agent → Captain → Agent)
- No bottlenecks
- Earned coordination bonus (+100 pts C-058)

### Self-Organized Role Claiming
- Agents claim based on expertise
- No hierarchy conflicts
- C-057: First autonomous mission success

---

## 📏 V2 COMPLIANCE STRATEGIES

### Extract-and-Facade Pattern
1. Extract focused modules
2. Keep original as deprecated facade
3. Maintain backward compatibility
4. Gradual migration

### Component Extraction
- State → component_state.py
- Metrics → component_metrics.py
- Lifecycle → component_lifecycle.py
- Core → original.py (orchestrates)

---

## 🎯 QUALITY GATES

### Before Merge
- All files <400 lines
- Linting passes
- Tests pass (>85% coverage)
- Documentation updated

### Code Review
- Architecture adherence checked
- V2 compliance verified
- No circular dependencies
- Clean separation maintained

---

**#V2-BEST-PRACTICES #PROVEN-PATTERNS #C059-7-COMPLETE**

🐝 WE. ARE. SWARM. ⚡️🔥

