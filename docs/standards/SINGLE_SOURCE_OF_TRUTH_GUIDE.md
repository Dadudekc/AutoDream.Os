# 🔗 Single Source of Truth Guide
**V2 Compliance Tracking Standards**

## 📋 **Overview**

This guide establishes the **Single Source of Truth (SSOT)** approach for maintaining the V2 Compliance Progress Tracker. This approach ensures data consistency, eliminates duplication, and provides a reliable foundation for compliance tracking.

## 🎯 **Core Principles**

### **1. Single Master File**
- **Root Tracker**: `V2_COMPLIANCE_PROGRESS_TRACKER.md` is the **ONLY** source of truth
- **Docs Copy**: `docs/reports/V2_COMPLIANCE_PROGRESS_TRACKER.md` is an **automated copy**
- **Never edit the docs version manually** - it will be overwritten

### **2. Automated Synchronization**
- The validation script automatically keeps both files in sync
- Changes should only be made to the root tracker file
- The docs version is automatically updated to match

### **3. Data Integrity**
- All compliance data comes from actual repository analysis
- No manual data entry without validation
- Real-time file counting and violation detection

## 📁 **File Structure**

```
Agent_Cellphone_V2_Repository/
├── V2_COMPLIANCE_PROGRESS_TRACKER.md          # 🎯 MASTER FILE (edit here)
├── docs/reports/
│   └── V2_COMPLIANCE_PROGRESS_TRACKER.md     # 📋 AUTO-SYNCED COPY
└── scripts/utilities/
    └── validate_compliance_tracker.py         # 🔧 VALIDATION SCRIPT
```

## 🚀 **Usage Workflow**

### **For Updates:**
1. **Edit ONLY** `V2_COMPLIANCE_PROGRESS_TRACKER.md`
2. **Run validation** to sync changes: `python scripts/utilities/validate_compliance_tracker.py`
3. **Verify** both files are identical

### **For Validation:**
1. **Run validation script** to check consistency
2. **Review output** for any issues
3. **Fix issues** in the root file if needed
4. **Re-run validation** to confirm fixes

## 🔧 **Validation Script**

### **Features:**
- **File Analysis**: Counts lines in all Python files
- **Violation Detection**: Categorizes files by size violations
- **Consistency Check**: Ensures tracker files are identical
- **Auto-Sync**: Updates docs version to match root
- **Report Generation**: Creates detailed compliance reports

### **Usage:**
```bash
# Run from repository root
python scripts/utilities/validate_compliance_tracker.py

# Or specify custom repo path
python scripts/utilities/validate_compliance_tracker.py /path/to/repo
```

### **Output:**
- **Console**: Real-time validation progress
- **JSON Report**: `data/compliance_validation_results.json`
- **Exit Codes**: 
  - `0`: Success, consistent
  - `1`: Error (critical issues)
  - `2`: Warning (minor issues)

## 📊 **Data Sources**

### **Repository Analysis:**
- **Python Files**: Automatically discovered and analyzed
- **Line Counts**: Real-time calculation
- **Violation Categories**: Based on V2 standards (300, 500, 800 line thresholds)

### **Contract Management:**
- **Contract Numbers**: Sequential assignment
- **Agent Recommendations**: Based on specializations
- **Timeline Tracking**: 3-week completion targets

## 🚨 **Common Issues & Solutions**

### **Issue: Tracker Files Out of Sync**
**Solution**: Run validation script - it will auto-sync

### **Issue: Git Merge Conflicts**
**Solution**: 
1. Resolve conflicts in root tracker
2. Run validation script to sync docs version

### **Issue: Duplicate Contract Entries**
**Solution**: 
1. Remove duplicates from root tracker
2. Run validation script to sync

### **Issue: Inaccurate File Counts**
**Solution**: 
1. Run validation script to get real counts
2. Update root tracker with accurate data
3. Re-run validation to confirm

## 📝 **Editing Guidelines**

### **What to Edit:**
- ✅ Contract completion status
- ✅ Agent assignments
- ✅ Progress percentages
- ✅ Timeline updates
- ✅ New contract details

### **What NOT to Edit:**
- ❌ The docs version (auto-synced)
- ❌ File counts (auto-calculated)
- ❌ Violation categories (auto-detected)
- ❌ Contract numbers (auto-assigned)

## 🔄 **Maintenance Schedule**

### **Daily:**
- Run validation script
- Check for any consistency issues
- Update contract progress

### **Weekly:**
- Review compliance percentages
- Update timeline targets
- Validate agent assignments

### **Monthly:**
- Full compliance audit
- Update standards if needed
- Review validation script

## 📚 **Related Documentation**

- [V2 Coding Standards](V2_CODING_STANDARDS.md)
- [Contract Management Guide](../reports/CONTRACT_MANAGEMENT_GUIDE.md)
- [Agent Assignment Protocol](../reports/AGENT_ASSIGNMENT_PROTOCOL.md)

## 🤝 **Support & Questions**

### **For Technical Issues:**
- Run validation script first
- Check console output for errors
- Review generated JSON report

### **For Process Questions:**
- Review this guide
- Check related documentation
- Contact Agent-4 (Quality Assurance)

---

## 🎯 **Quick Reference**

| Action | File to Edit | Command to Run |
|--------|--------------|----------------|
| Update Progress | Root Tracker | `python scripts/utilities/validate_compliance_tracker.py` |
| Check Status | Either | `python scripts/utilities/validate_compliance_tracker.py` |
| Fix Issues | Root Tracker | `python scripts/utilities/validate_compliance_tracker.py` |
| Generate Report | Either | `python scripts/utilities/validate_compliance_tracker.py` |

**Remember: Root Tracker = Master, Docs Version = Auto-Synced Copy**

