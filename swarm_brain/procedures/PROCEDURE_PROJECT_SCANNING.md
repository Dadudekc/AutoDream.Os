# PROCEDURE: Project Scanning & Analysis

**Category**: Analysis & Discovery  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: analysis, scanning, discovery, project-analysis

---

## 🎯 WHEN TO USE

**Trigger**: Beginning new work OR need to find opportunities OR periodic health check

**Who**: Any agent, especially at start of new cycle

---

## 📋 PREREQUISITES

- Project scanner installed
- Write access to analysis output directories
- Python environment active

---

## 🔄 PROCEDURE STEPS

### **Step 1: Run Project Scanner**

```bash
python tools/run_project_scan.py
```

**What it does**:
- Scans all Python files
- Analyzes V2 compliance
- Identifies consolidation opportunities
- Generates comprehensive reports

### **Step 2: Review Analysis Outputs**

**Main files created**:
1. `project_analysis.json` - Complete project analysis
2. `test_analysis.json` - Test coverage data
3. `chatgpt_project_context.json` - LLM-formatted context
4. `analysis_chunks/` - Modular analysis reports

### **Step 3: Identify Opportunities**

```bash
# Review analysis
cat project_analysis.json | python -m json.tool | grep -A 5 "violations"

# Or use BI tools
python -m tools_v2.toolbelt analysis.scan
```

**Look for**:
- V2 violations (high-value fixes)
- Duplicate code (consolidation opportunities)
- Missing tests (quality improvements)
- Architecture issues (refactoring targets)

### **Step 4: Claim High-Value Work**

```bash
# Calculate ROI for tasks
python -m tools_v2.toolbelt captain.calc_points \
  --file path/to/file.py \
  --current-lines 500 \
  --target-lines 300

# Shows: Points, ROI, effort estimate
```

### **Step 5: Update Status & Begin**

```bash
# Update your status.json
echo '{"current_mission": "Fixing X violations in file.py"}' >> agent_workspaces/Agent-X/status.json

# Begin work
# [Execute your fix]
```

---

## ✅ SUCCESS CRITERIA

- [ ] project_analysis.json generated
- [ ] No errors in scanning process
- [ ] Analysis chunks created
- [ ] Opportunities identified
- [ ] High-value work claimed

---

## 🔄 ROLLBACK

If scan fails or produces bad data:

```bash
# Clean analysis outputs
rm project_analysis.json test_analysis.json chatgpt_project_context.json
rm -rf analysis_chunks/

# Re-run scanner
python tools/run_project_scan.py
```

---

## 📝 EXAMPLES

**Example 1: Successful Scan**

```bash
$ python tools/run_project_scan.py

🔍 SCANNING PROJECT...
📊 Analyzing 1,700+ files...
✅ Python files: 543 analyzed
✅ Tests: 127 test files found
✅ Coverage: 82% average

📄 OUTPUTS CREATED:
✅ project_analysis.json (2.4MB)
✅ test_analysis.json (450KB)
✅ chatgpt_project_context.json (1.1MB)
✅ analysis_chunks/ (17 files)

🎯 SCAN COMPLETE! Review project_analysis.json for opportunities.
```

**Example 2: Finding High-ROI Opportunities**

```bash
# Review violations
$ cat project_analysis.json | grep -C 3 "CRITICAL"

"violations": [
  {
    "file": "tools/autonomous_task_engine.py",
    "severity": "CRITICAL",
    "lines": 797,
    "target": 300,
    "estimated_points": 500,
    "roi": 16.67
  }
]

# This is HIGH ROI work! Claim it!
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_V2_COMPLIANCE_CHECK (checking compliance)
- PROCEDURE_TASK_CLAIMING (autonomous task claiming)
- PROCEDURE_ROI_CALCULATION (calculating task ROI)

---

## 📊 SCAN METRICS

**Files Analyzed**: 1,700+  
**Analysis Time**: ~2-3 minutes  
**Output Size**: ~4MB total  
**Frequency**: Daily or per-cycle recommended

---

**Agent-5 - Procedure Documentation** 📚

