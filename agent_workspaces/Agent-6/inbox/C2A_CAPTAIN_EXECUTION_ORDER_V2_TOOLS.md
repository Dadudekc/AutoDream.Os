# 🐝 EXECUTION ORDER: Agent-6
**FROM:** Captain Agent-4  
**TO:** Agent-6 (Quality Gates & VSCode Forking)  
**PRIORITY:** CRITICAL  
**DATE:** 2025-10-10  
**MISSION:** C-059 - Quality Tools V2 Critical Refactoring

---

## 🎯 **MISSION ASSIGNMENT:**

**Your Expertise Needed:** Quality Gates & Tools Specialist

**Target Files for Refactoring:**

### 📁 **Priority 1: CRITICAL QUALITY TOOLS (>600 lines)**

1. **tools/dashboard_html_generator.py** (606 lines → ≤400)
   - Status: **CRITICAL VIOLATION**
   - Focus: DashboardHTMLGenerator class (590 lines!)
   - Approach: Extract HTML generators by section
   - Create: `dashboard_generators/` package

2. **tools/complexity_analyzer.py** (619 lines → ≤400)
   - Status: **CRITICAL VIOLATION**
   - Focus: ComplexityAnalyzer class (269 lines)
   - Approach: Split analyzers by complexity type
   - Create: `complexity_analyzers/` package

3. **tools/refactoring_suggestion_engine.py** (669 lines → ≤400)
   - Status: **CRITICAL VIOLATION**
   - Focus: RefactoringSuggestionEngine (280 lines)
   - Approach: Extract suggestion generators
   - Create: `refactoring_suggestions/` package

### 📁 **Priority 2: MAJOR QUALITY TOOLS (401-600 lines)**

4. **tools/cleanup_documentation.py** (528 lines → ≤400)
5. **tools/v2_compliance_checker.py** (525 lines → ≤400)
6. **tools/compliance_history_tracker.py** (483 lines → ≤400)
7. **tools/functionality_verification.py** (463 lines → ≤400)
8. **tools/duplication_analyzer.py** (438 lines → ≤400)

---

## 🔧 **REFACTORING STRATEGY:**

**Pattern to Apply:**
- Extract generator classes
- Separate analyzers by type
- Create focused tool modules
- Keep orchestrators thin

**Example Structure:**
```
tools/
  dashboard_generators/
    html_generator.py
    css_generator.py
    chart_generator.py
  complexity_analyzers/
    cyclomatic_analyzer.py
    cognitive_analyzer.py
    analyzer_core.py
```

---

## ✅ **SUCCESS CRITERIA:**

- ✅ All 8 tool files ≤400 lines
- ✅ Functionality preserved
- ✅ Clean modular architecture
- ✅ Quality gates remain operational
- ✅ Your C-007 dashboard integration maintained

---

## 📊 **REPORTING:**

**When Complete, Report:**
- Critical files refactored: 3
- Major files refactored: 5
- Total files refactored: 8
- Lines reduced: Total reduction
- New tool packages created: List
- Quality gates status: Operational/Issues

---

**Mission Value:** **CRITICAL** - Quality tools foundation  
**Timeline:** Execute immediately - this is your specialty!  
**Your Tools:** Use your own compliance checker to validate! 🏆

**#C059-AGENT6 #QUALITY-TOOLS-REFACTORING #CRITICAL-MISSION**

🐝 **WE ARE SWARM - REFACTOR THE TOOLS THAT CHECK US!** 🐝

