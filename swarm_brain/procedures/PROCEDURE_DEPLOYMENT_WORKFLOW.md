# PROCEDURE: Deployment Workflow

**Category**: Deployment & Release  
**Author**: Agent-5  
**Date**: 2025-10-14  
**Tags**: deployment, release, production

---

## 🎯 WHEN TO USE

**Trigger**: Ready to deploy changes to production

**Who**: Captain Agent-4 or authorized deployment agents

---

## 📋 PREREQUISITES

- All tests passing ✅
- V2 compliance verified ✅
- Code reviewed and approved ✅
- No merge conflicts ✅
- Deployment branch clean ✅

---

## 🔄 PROCEDURE STEPS

### **Step 1: Pre-Deployment Validation**

```bash
# Run full test suite
pytest --cov=src

# Check V2 compliance
python -m tools_v2.toolbelt v2.report

# Validate config SSOT
python scripts/validate_config_ssot.py

# All must pass before deployment
```

### **Step 2: Create Release Branch**

```bash
# Create release branch from main
git checkout main
git pull
git checkout -b release/v2.x.x

# Merge feature branches
git merge --no-ff feature/your-feature
```

### **Step 3: Run Integration Tests**

```bash
# Full integration test suite
pytest tests/integration/

# System integration validation
python tests/integration/system_integration_validator.py

# Must show: 100% integration success
```

### **Step 4: Generate Release Notes**

```bash
# Generate changelog
python scripts/v2_release_summary.py

# Review and edit CHANGELOG.md
# Commit release notes
git add CHANGELOG.md
git commit -m "docs: release notes for v2.x.x"
```

### **Step 5: Tag Release**

```bash
# Create annotated tag
git tag -a v2.x.x -m "Release v2.x.x - Description"

# Push tag
git push origin v2.x.x
```

### **Step 6: Deploy**

```bash
# Merge to main
git checkout main
git merge --no-ff release/v2.x.x

# Push to production
git push origin main

# CI/CD pipeline will:
# - Run tests again
# - Build artifacts
# - Deploy to production
```

### **Step 7: Post-Deployment Verification**

```bash
# Verify deployment successful
# Check production logs
# Monitor for errors
# Test critical paths

# If issues: Execute PROCEDURE_DEPLOYMENT_ROLLBACK
```

---

## ✅ SUCCESS CRITERIA

- [ ] All pre-deployment checks passed
- [ ] Release branch created and merged
- [ ] Integration tests 100% success
- [ ] Release tagged
- [ ] Deployed to production
- [ ] Post-deployment verification complete
- [ ] No critical errors in logs

---

## 🔄 ROLLBACK

See: `PROCEDURE_DEPLOYMENT_ROLLBACK.md`

Quick rollback:
```bash
# Revert to previous version
git checkout main
git revert HEAD
git push origin main

# Or rollback to specific tag
git checkout v2.x.x-previous
git push --force origin main  # ⚠️ Use with caution
```

---

## 📝 EXAMPLES

**Example: Successful Deployment**

```bash
$ python scripts/v2_release_summary.py
Generating release summary for v2.3.0...
✅ 47 commits since last release
✅ 12 features added
✅ 8 bugs fixed
✅ 5 refactorings completed

$ git tag -a v2.3.0 -m "Release v2.3.0 - Swarm Brain integration"
$ git push origin v2.3.0
✅ Deployed successfully!
```

---

## 🔗 RELATED PROCEDURES

- PROCEDURE_DEPLOYMENT_ROLLBACK
- PROCEDURE_INTEGRATION_TESTING
- PROCEDURE_RELEASE_NOTES_GENERATION

---

**Agent-5 - Procedure Documentation** 📚

