# 🧹 CONTRACT CLEANUP PROMPT TEMPLATE - AGENT CELLPHONE V2

**Standard Prompt for Agents to Complete Contracts Properly**

---

## 🚨 **CRITICAL CLEANUP REQUIREMENT**

**Before marking any contract as completed, you MUST run this cleanup validation:**

```bash
# 1. Validate your cleanup and standards compliance
python cleanup_validator.py auto-validate TASK_XXX

# 2. Generate detailed cleanup report
python cleanup_validator.py report TASK_XXX

# 3. Show cleanup checklist
python cleanup_validator.py checklist TASK_XXX
```

---

## 📋 **COMPLETE CLEANUP CHECKLIST**

### **🧹 Code Cleanup**
- [ ] Remove all temporary code and debug statements
- [ ] Clean up unused imports and dead code
- [ ] Remove any test-specific temporary code
- [ ] Ensure all TODO/FIXME comments are resolved

### **📚 Documentation Cleanup**
- [ ] Update or create proper documentation
- [ ] Add/update docstrings and comments
- [ ] Update README files if needed
- [ ] Create comprehensive devlog entry

### **🧪 Test Cleanup**
- [ ] Ensure all tests pass
- [ ] Remove test-specific temporary code
- [ ] Clean up test data and fixtures

### **📁 File Organization**
- [ ] Organize files in proper directories
- [ ] Remove any temporary files
- [ ] Ensure proper file naming conventions

### **🔧 Git Cleanup**
- [ ] Commit all changes with proper commit messages
- [ ] Push to remote repository
- [ ] Ensure no uncommitted changes remain

### **📝 Devlog Entry**
- [ ] Create comprehensive devlog entry
- [ ] Document all work completed
- [ ] Include any issues encountered and resolved

### **💬 Discord Update**
- [ ] Post Discord devlog update
- [ ] Summarize completed work
- [ ] Include key achievements and metrics

---

## 🏗️ **V2 STANDARDS COMPLIANCE**

### **✅ Single Responsibility Principle**
- [ ] Each class/module has one clear purpose
- [ ] No mixed responsibilities in single files

### **✅ Line Count Compliance**
- [ ] No file exceeds 200 LOC
- [ ] Large files properly modularized

### **✅ OOP Patterns**
- [ ] Proper inheritance structure
- [ ] Clean interfaces and abstractions

### **✅ No Duplication**
- [ ] Use existing unified systems
- [ ] No duplicate functionality

### **✅ Error Handling**
- [ ] Comprehensive error handling
- [ ] Proper logging throughout

### **✅ Integration Compliance**
- [ ] Proper integration with existing systems
- [ ] No breaking changes to existing functionality

---

## 🚀 **COMPLETE WORKFLOW**

### **Step 1: Complete Your Work**
```bash
# Finish the actual task implementation
# Ensure functionality works as expected
```

### **Step 2: Run Cleanup Validation**
```bash
# Auto-validate cleanup and standards
python cleanup_validator.py auto-validate TASK_XXX

# Check the results - you need 90%+ overall score
```

### **Step 3: Address Any Issues**
```bash
# If validation fails, fix the issues shown
# Re-run validation until you pass
```

### **Step 4: Generate Final Report**
```bash
# Create comprehensive cleanup report
python cleanup_validator.py report TASK_XXX
```

### **Step 5: Update Contract Status**
```bash
# Mark all requirements as completed
python contract_cli.py update TASK_XXX task_completion true "Task completed with full cleanup"
python contract_cli.py update TASK_XXX progress_documentation true "Documentation complete"
python contract_cli.py update TASK_XXX integration_verification true "Integration verified"
```

### **Step 6: Final Validation**
```bash
# Validate contract completion
python contract_cli.py validate TASK_XXX

# Should show 100% completion and VALID status
```

---

## 🎯 **VALIDATION SCORING REQUIREMENTS**

### **Minimum Scores Required:**
- **Overall Score**: 90%+ (0.9/1.0)
- **Cleanup Score**: 85%+ (0.85/1.0) 
- **Standards Score**: 80%+ (0.8/1.0)

### **Score Breakdown:**
- **Cleanup Requirements**: 60% of overall score
- **V2 Standards**: 40% of overall score

---

## 🚨 **COMMON CLEANUP FAILURES**

### **❌ Code Cleanup Issues**
- Temporary files left behind
- Debug print statements not removed
- Unused imports not cleaned up
- TODO/FIXME comments not resolved

### **❌ Documentation Issues**
- Missing devlog entry
- Incomplete README updates
- Poor commit messages
- Missing Discord update

### **❌ Standards Issues**
- Files exceeding 200 LOC
- Mixed responsibilities in modules
- Poor error handling
- Breaking existing functionality

---

## 📊 **EXAMPLE VALIDATION OUTPUT**

```bash
$ python cleanup_validator.py auto-validate TASK_1B

🤖 Auto-validating contract TASK_1B...
❌ Auto-validation complete: Contract is INVALID (Score: 0.45)

📊 DETAILED RESULTS:
Cleanup Score: 0.29/1.0
Standards Score: 0.67/1.0
Overall Score: 0.45/1.0

❌ MISSING CLEANUP:
  - Clean up any temporary code, debug statements, or unused imports
  - Update or create proper documentation (README, docstrings, comments)
  - Ensure tests pass and remove any test-specific temporary code
  - Organize files in proper directories and remove any temporary files
  - Commit all changes with proper commit messages and push to remote
  - Create comprehensive devlog entry documenting all work completed
  - Post Discord devlog update summarizing completed work
```

---

## 🔧 **FIXING VALIDATION ISSUES**

### **If Cleanup Score is Low:**
1. **Code Cleanup**: Remove debug statements, temp files, unused imports
2. **Documentation**: Create devlog entry, update READMEs
3. **Git**: Commit and push all changes
4. **Discord**: Post update to Discord

### **If Standards Score is Low:**
1. **Large Files**: Break down files exceeding 200 LOC
2. **SRP**: Ensure each module has single responsibility
3. **Integration**: Fix any breaking changes
4. **Error Handling**: Add proper error handling and logging

---

## 📝 **FINAL CHECKLIST BEFORE SUBMISSION**

### **✅ Validation Passes**
- [ ] `python cleanup_validator.py auto-validate TASK_XXX` shows 90%+ overall score
- [ ] All cleanup requirements met
- [ ] All V2 standards compliant

### **✅ Contract Status Updated**
- [ ] All requirements marked as completed
- [ ] Contract validation shows 100% completion
- [ ] Status shows "COMPLETED" or "REVIEW_NEEDED"

### **✅ Documentation Complete**
- [ ] Devlog entry created
- [ ] Discord update posted
- [ ] All changes committed and pushed

### **✅ Project State Clean**
- [ ] No temporary files
- [ ] No debug statements
- [ ] All tests pass
- [ ] No uncommitted changes

---

## 🎉 **SUCCESS INDICATORS**

### **✅ You're Ready When:**
- Cleanup validation shows 90%+ overall score
- Contract validation shows 100% completion
- All cleanup checklist items are checked
- Project is in clean, production-ready state
- All work is documented and communicated

### **❌ You're NOT Ready When:**
- Any validation score is below minimum
- Cleanup checklist has unchecked items
- Project has temporary files or debug code
- Uncommitted changes remain
- Missing documentation or Discord update

---

## 🚀 **FINAL COMMAND SEQUENCE**

```bash
# 1. Complete all cleanup tasks manually
# 2. Run auto-validation
python cleanup_validator.py auto-validate TASK_XXX

# 3. If validation passes (90%+), generate report
python cleanup_validator.py report TASK_XXX

# 4. Update contract status
python contract_cli.py update TASK_XXX task_completion true "Task completed with full cleanup"
python contract_cli.py update TASK_XXX progress_documentation true "Documentation complete"
python contract_cli.py update TASK_XXX integration_verification true "Integration verified"

# 5. Final validation
python contract_cli.py validate TASK_XXX

# 6. If all passes, you're done! 🎉
```

---

## ⚠️ **REMEMBER**

**This cleanup is MANDATORY before marking any contract as completed.**
**The system will bounce back incomplete contracts.**
**Only submit when you're 100% confident everything is clean and compliant.**

---

**Generated by**: Captain Agent-4 Contract Cleanup System  
**Purpose**: Ensure contracts meet all cleanup and V2 standards requirements  
**Status**: **MANDATORY FOR ALL AGENTS** 🚨
