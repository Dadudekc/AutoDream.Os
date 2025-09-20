# Agent Protocol Quick Reference
**Version**: 1.0  
**Date**: 2025-01-18  
**Purpose**: Quick reference for daily agent operations  

---

## 🚀 **DAILY WORKFLOW QUICK REFERENCE**

### **🔧 Starting Work:**
```bash
# 1. Check status
git status

# 2. Pull latest changes
git checkout develop
git pull origin develop

# 3. Create feature branch
git checkout -b feat/your-feature-name

# 4. Check inbox
ls agent_workspaces/Agent-X/inbox/
```

### **📝 Making Changes:**
```bash
# 1. Make your changes
# 2. Run quality gates
python quality_gates.py

# 3. Run tests
pytest

# 4. Commit with proper message
git add .
git commit -m "feat: add new feature"

# 5. Push branch
git push origin feat/your-feature-name
```

### **🔄 Creating PR:**
```bash
# 1. Create PR targeting develop
gh pr create --title "feat: add new feature" --body "Description"

# 2. Request review
gh pr ready

# 3. Check CI status
gh pr checks
```

---

## 📋 **COMMIT MESSAGE TEMPLATES**

### **Feature:**
```
feat: add user authentication system

- Implement JWT token handling
- Add user registration endpoint
- Create authentication middleware

Closes #123
```

### **Fix:**
```
fix: resolve memory leak in data processing

- Fix unclosed file handles
- Add proper resource cleanup
- Update error handling

Fixes #456
```

### **Docs:**
```
docs: update API documentation

- Add new endpoint examples
- Update authentication section
- Fix typos in usage guide
```

---

## 🧪 **TESTING QUICK COMMANDS**

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_feature.py

# Run specific test
pytest tests/test_feature.py::test_specific_function

# Run tests with verbose output
pytest -v
```

---

## 📊 **QUALITY GATES CHECKLIST**

### **Before Every Commit:**
- [ ] `python quality_gates.py` passes
- [ ] `pytest` passes
- [ ] Code follows V2 standards (≤400 lines)
- [ ] Type hints added (Python)
- [ ] Error handling implemented
- [ ] Documentation updated

### **Before Every PR:**
- [ ] Feature branch created properly
- [ ] All commits follow convention
- [ ] PR targets `develop` branch
- [ ] PR description follows template
- [ ] All tests pass
- [ ] Code reviewed
- [ ] Ready for merge

---

## 🤖 **AGENT COMMUNICATION TEMPLATES**

### **Status Update Message:**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-3
📥 TO: Agent-4
Priority: NORMAL
Tags: STATUS
------------------------------------------------------------
🎯 STATUS UPDATE: V3-003 Database Architecture Setup

✅ COMPLETED:
- Database replication configuration
- Backup system implementation
- Performance optimization setup

🔄 IN PROGRESS:
- Monitoring system integration

📋 NEXT ACTIONS:
- Complete monitoring setup
- Begin V3-006 integration

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action
------------------------------------------------------------
```

### **Task Request Message:**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-1
📥 TO: Agent-3
Priority: HIGH
Tags: TASK
------------------------------------------------------------
🎯 TASK REQUEST: V3-006 Database Integration

DESCRIPTION: Integrate V3-003 database architecture with V3-006 system

REQUIREMENTS:
- Use existing database configuration
- Implement connection pooling
- Add error handling

DEADLINE: 2 cycles

📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action
------------------------------------------------------------
```

---

## 🔧 **EMERGENCY PROCEDURES**

### **🚨 Production Issue:**
1. **Immediate Response**: Notify Captain Agent-4
2. **Assessment**: Document the issue
3. **Hotfix**: Create `hotfix/issue-description` branch
4. **Deploy**: Emergency deployment
5. **Document**: Create incident report

### **🔒 Security Issue:**
1. **Immediate Response**: Notify Captain Agent-4
2. **Assessment**: Evaluate security impact
3. **Mitigation**: Implement immediate fixes
4. **Investigation**: Root cause analysis
5. **Prevention**: Update security protocols

---

## 📚 **COMMON COMMANDS**

### **Git Commands:**
```bash
# Checkout develop
git checkout develop

# Create feature branch
git checkout -b feat/feature-name

# Check status
git status

# Add changes
git add .

# Commit with message
git commit -m "feat: add feature"

# Push branch
git push origin feat/feature-name

# Create PR
gh pr create --title "Title" --body "Description"
```

### **Quality Commands:**
```bash
# Run quality gates
python quality_gates.py

# Run tests
pytest

# Run linting
flake8 src/
black src/
isort src/

# Run pre-commit
pre-commit run --all-files
```

### **Agent Commands:**
```bash
# Check inbox
ls agent_workspaces/Agent-X/inbox/

# Update status
echo '{"status": "ACTIVE"}' > agent_workspaces/Agent-X/status.json

# Send message
python src/services/simple_messaging_service.py --agent Agent-Y --message "Your message"
```

---

## 🎯 **BRANCH NAMING EXAMPLES**

### **Features:**
- `feat/user-authentication`
- `feat/payment-integration`
- `feat/real-time-chat`

### **Bug Fixes:**
- `fix/memory-leak-database`
- `fix/login-validation-error`
- `fix/api-response-format`

### **Hotfixes:**
- `hotfix/critical-security-patch`
- `hotfix/production-crash-fix`
- `hotfix/data-corruption-issue`

### **Releases:**
- `release/v1.2.3`
- `release/v2.0.0`
- `release/v1.1.5`

---

## 📋 **STATUS FILE TEMPLATE**

```json
{
  "agent_id": "Agent-3",
  "agent_name": "Infrastructure & DevOps Specialist",
  "status": "ACTIVE_AGENT_MODE",
  "current_phase": "TASK_EXECUTION",
  "last_updated": "2025-01-18 19:35:00",
  "current_mission": "V3 Infrastructure Deployment",
  "mission_priority": "HIGH",
  "current_tasks": ["V3-003 Database Architecture"],
  "completed_tasks": ["V3-001 Cloud Infrastructure"],
  "achievements": ["ML Training Infrastructure Tool"],
  "next_actions": ["Complete V3-003", "Begin V3-006"]
}
```

---

## 🚀 **RELEASE PROCESS QUICK REFERENCE**

```bash
# 1. Create release branch
git checkout develop
git checkout -b release/v1.2.3

# 2. Update version numbers
# 3. Update CHANGELOG.md
# 4. Create PR: release/v1.2.3 → main
# 5. Merge after approval
# 6. Tag release
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3

# 7. Deploy to production
```

---

## 📞 **EMERGENCY CONTACTS**

- **Captain Agent-4**: Strategic oversight and emergency response
- **Agent-3**: Infrastructure and DevOps issues
- **Agent-1**: Core systems and architecture
- **Agent-2**: Architecture and design issues

---

## 🔄 **PROTOCOL UPDATES**

This quick reference is updated monthly. Check `docs/AGENT_PROTOCOL_SYSTEM.md` for the complete protocol system.

**Last Updated**: 2025-01-18  
**Next Review**: 2025-02-18  
**Version**: 1.0  

---

**🐝 WE ARE SWARM** - Quick reference for efficient daily operations!
