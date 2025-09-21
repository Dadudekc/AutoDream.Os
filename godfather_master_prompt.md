# 🛰️ GODFATHER MASTER PROMPT — Project Explainer

## Role: "Project Godfather Reviewer"
## Mode: "Forge"

### Task:
Review my project repository file by file. 
For each file:
- Identify its purpose and scope in plain language.
- Explain its major components (functions, classes, configs).
- Describe how it fits into the overall system architecture.
- Highlight dependencies (imports, cross-file calls).
- Note any patterns, anti-patterns, or obvious improvement areas.
- Keep explanations concise but complete — no drift, no filler.

### Format:
- 📂 **File Path**
- 🧩 **Purpose**
- 🏗️ **Major Components**
- 🔗 **Dependencies**
- 🧭 **Role in System**
- ⚠️ **Observations / Improvements**

### Rules:
- Cover *every* file once — no skipping.
- Summarize large boilerplate (don't paste the whole thing).
- Highlight only what matters for architecture + comprehension.
- Closure per file = ✅
- Closure for repo = final "Master System Summary."

### Output Style:
- Structured markdown
- Emojis for section clarity
- End with full system overview ("Like a Godfather explaining the family").

---

## 🎯 USAGE INSTRUCTIONS

### Step 1: Generate Repository Structure
```bash
find . -type f | grep -v -E "(venv|\.git|node_modules|__pycache__|\.pytest_cache|\.mypy_cache)" | sort > repo_structure.txt
```

### Step 2: Execute File Reviews
For each file, apply this prompt with the file content to get comprehensive analysis.

### Step 3: Collect Results
Compile all individual file analyses into a master project review document.

---

## 🔥 BATTLE-TESTED FEATURES

- **No Drift**: Forces closure on every file
- **Architecture Focus**: Highlights system relationships
- **Pattern Recognition**: Identifies good/bad patterns
- **Dependency Mapping**: Shows how files connect
- **Improvement Areas**: Actionable insights
- **Godfather Style**: Complete system understanding

---

## 📋 EXPECTED OUTPUT STRUCTURE

```markdown
# 🏛️ PROJECT GODFATHER REVIEW

## 📊 Repository Overview
- Total files analyzed: X
- Architecture layers: Y
- Key patterns identified: Z

## 📂 File-by-File Analysis

### File 1: path/to/file.py
📂 **File Path**: path/to/file.py
🧩 **Purpose**: What this file does
🏗️ **Major Components**: Key classes/functions
🔗 **Dependencies**: What it imports/uses
🧭 **Role in System**: How it fits architecture
⚠️ **Observations**: Issues/improvements
✅ **Closure**: Complete

[... continue for all files ...]

## 🎯 MASTER SYSTEM SUMMARY

### Architecture Overview
[High-level system architecture explanation]

### Key Patterns
[Major patterns and anti-patterns identified]

### Dependencies Map
[How major components connect]

### Improvement Recommendations
[Priority improvements across the system]

### Final Assessment
[Overall system health and recommendations]
```

---

## ⚡ QUICK START

1. **Run structure generator**: `find . -type f | grep -v -E "(venv|\.git|node_modules|__pycache__|\.pytest_cache|\.mypy_cache)" | sort`
2. **Feed files one by one** to this prompt
3. **Collect outputs** into `project_review.md`
4. **Get complete system understanding** in one go

---

*This prompt forces agents into closure-first architecture analysis — perfect for comprehensive project understanding.*