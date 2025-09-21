# Agent Protocol System - Standardized Workflows
**Version**: 1.0  
**Date**: 2025-01-18  
**Purpose**: Standardized workflows for all agents across projects  
**Maintainer**: Agent-3 (Infrastructure & DevOps Specialist)  

---

## 🎯 **PROTOCOL SYSTEM OVERVIEW**

### **📋 Purpose:**
This protocol system provides standardized workflows, procedures, and guidelines for all agents to ensure consistent, high-quality development practices across all projects.

### **🔧 Scope:**
- Git workflow and branch management
- Pull request procedures
- Code quality standards
- Testing protocols
- Deployment procedures
- Documentation requirements
- Agent coordination protocols

---

## 🔄 **GIT WORKFLOW PROTOCOL**

### **🔀 Branch Strategy (MANDATORY):**
```
main (production) ← develop (integration) ← feature branches
```

#### **Branch Types:**
- **`main`**: Production-ready code only
- **`develop`**: Integration branch for all features
- **`feat/feature-name`**: New features
- **`fix/issue-description`**: Bug fixes
- **`hotfix/critical-issue`**: Critical production fixes
- **`release/v1.2.3`**: Release preparation

#### **Branch Creation Protocol:**
```bash
# 1. Always start from develop
git checkout develop
git pull origin develop

# 2. Create feature branch with proper naming
git checkout -b feat/your-feature-name

# 3. Work on feature
# 4. Create PR targeting develop
```

### **📝 Commit Message Protocol (MANDATORY):**
```
type: short description

Longer description if needed

- Bullet point 1
- Bullet point 2

Closes #issue-number
```

#### **Commit Types:**
- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation updates
- `refactor:` - Code refactoring
- `test:` - Testing updates
- `chore:` - Maintenance tasks
- `perf:` - Performance improvements
- `ci:` - CI/CD changes

---

## 🔄 **PULL REQUEST PROTOCOL**

### **📋 PR Creation Process:**
1. **Create Feature Branch**: Follow branch naming convention
2. **Implement Changes**: With proper commits
3. **Run Quality Gates**: Linting, tests, formatting
4. **Create PR**: Target `develop` branch
5. **Add Description**: Use PR template
6. **Request Review**: Assign appropriate reviewers
7. **Address Feedback**: Make requested changes
8. **Merge**: After approval and CI passes

### **📝 PR Template (MANDATORY):**
```markdown
## 🎯 **CHANGE DESCRIPTION**
Brief description of what this PR does.

## 🔧 **CHANGES MADE**
- Change 1
- Change 2
- Change 3

## 🧪 **TESTING**
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] V2 compliance verified

## 📋 **CHECKLIST**
- [ ] Code follows V2 standards
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] CI checks pass
- [ ] Ready for review

## 🔗 **RELATED ISSUES**
Closes #issue-number
```

### **🔍 PR Review Protocol:**
- **Required Reviewers**: At least 1 agent review
- **CI Requirements**: All checks must pass
- **Quality Gates**: V2 compliance verified
- **Testing**: All tests must pass

---

## 📊 **CODE QUALITY PROTOCOL**

### **🎯 V2 Compliance Standards (MANDATORY):**
- **File Size**: ≤400 lines (hard limit)
- **Classes**: ≤5 per file
- **Functions**: ≤10 per file
- **Complexity**: ≤10 cyclomatic complexity
- **Parameters**: ≤5 per function
- **Inheritance**: ≤2 levels deep

### **🔧 Pre-commit Requirements:**
```bash
# Run before every commit
python quality_gates.py
pytest
pre-commit run --all-files
```

### **📋 Quality Gates Checklist:**
- [ ] Linting passes (flake8, black, isort)
- [ ] Tests pass (pytest)
- [ ] V2 compliance verified
- [ ] Documentation updated
- [ ] Type hints added (Python)
- [ ] Error handling implemented

---

## 🧪 **TESTING PROTOCOL**

### **📋 Test Requirements:**
- **Unit Tests**: All new code requires unit tests
- **Integration Tests**: For complex integrations
- **Coverage**: Minimum 85% test coverage
- **Test Naming**: Descriptive test names

### **🧪 Test Structure:**
```python
def test_feature_should_handle_success_case():
    """Test that feature handles success case correctly."""
    # Arrange
    input_data = create_test_data()
    
    # Act
    result = feature_under_test(input_data)
    
    # Assert
    assert result.status == "success"
    assert result.data is not None
```

### **🔧 Testing Commands:**
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_specific_feature.py
```

---

## 🚀 **DEPLOYMENT PROTOCOL**

### **📋 Deployment Process:**
1. **Feature Complete**: All features merged to `develop`
2. **Integration Testing**: Full system testing
3. **Release Branch**: Create `release/v1.2.3`
4. **Release Testing**: Comprehensive testing
5. **Merge to Main**: Release to production
6. **Tag Release**: Create version tag
7. **Deploy**: Run deployment pipeline

### **🏷️ Release Protocol:**
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
```

---

## 📚 **DOCUMENTATION PROTOCOL**

### **📋 Required Documentation:**
- **README.md**: Project overview and setup
- **CHANGELOG.md**: Version history
- **API Documentation**: For all public APIs
- **Code Comments**: For complex logic
- **Devlogs**: For all agent actions

### **📝 Documentation Standards:**
```python
def function_name(param1: Type, param2: Type) -> ReturnType:
    """
    Brief description of what function does.

    Args:
        param1: Description of parameter
        param2: Description of parameter

    Returns:
        Description of return value

    Raises:
        ExceptionType: When this exception occurs

    Example:
        >>> result = function_name(value1, value2)
        >>> print(result)
        expected_output
    """
```

---

## 🤖 **AGENT COORDINATION PROTOCOL**

### **📋 Agent Communication:**
- **Primary**: Inbox messaging system
- **Secondary**: Direct file communication
- **Emergency**: Override protocols available

### **📨 Message Format:**
```
============================================================
[A2A] MESSAGE
============================================================
📤 FROM: Agent-X
📥 TO: Agent-Y
Priority: NORMAL|HIGH|URGENT
Tags: GENERAL|COORDINATION|TASK|STATUS
------------------------------------------------------------
{CONTENT}
📝 DISCORD DEVLOG REMINDER: Create a Discord devlog for this action
------------------------------------------------------------
```

### **📊 Status Reporting Protocol:**
- **Frequency**: After each major task completion
- **Format**: JSON status files
- **Location**: `agent_workspaces/{Agent-X}/status.json`
- **Required Fields**: See status file template

### **🎯 Task Management Protocol:**
- **Task Claiming**: Use `--get-next-task` command
- **Status Updates**: Update working_tasks.json
- **Completion**: Mark tasks complete with devlog

---

## 🔧 **TOOL DEVELOPMENT PROTOCOL**

### **📋 Tool Creation Process:**
1. **Identify Need**: Document the problem
2. **Design Solution**: Plan the implementation
3. **Create Tool**: Follow V2 compliance
4. **Test Tool**: Comprehensive testing
5. **Document Tool**: Usage examples and API
6. **Deploy Tool**: Make available to team
7. **Create Devlog**: Document the process

### **🛠️ Tool Standards:**
- **Location**: `tools/` directory
- **Naming**: `descriptive_tool_name.py`
- **CLI Support**: Command-line interface
- **Documentation**: README with examples
- **Testing**: Unit tests for all functions

---

## 🚨 **EMERGENCY PROTOCOLS**

### **🔧 Critical Issues:**
- **Production Issues**: Immediate response required
- **Security Issues**: Highest priority
- **Data Loss**: Emergency recovery procedures
- **System Down**: Escalation protocols

### **📞 Emergency Contacts:**
- **Captain Agent-4**: Strategic oversight and emergency response
- **Agent-3**: Infrastructure and DevOps issues
- **Agent-1**: Core systems and architecture

---

## 📋 **COMPLIANCE CHECKLIST**

### **✅ Pre-commit Checklist:**
- [ ] Code follows V2 standards
- [ ] All tests pass
- [ ] Linting passes
- [ ] Documentation updated
- [ ] Type hints added
- [ ] Error handling implemented

### **✅ PR Checklist:**
- [ ] Feature branch created properly
- [ ] All commits follow convention
- [ ] PR targets correct branch
- [ ] Description follows template
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Ready for merge

### **✅ Release Checklist:**
- [ ] All features complete
- [ ] Integration testing passed
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] CHANGELOG.md updated
- [ ] Release branch created
- [ ] Production testing complete

---

## 🔄 **PROTOCOL UPDATES**

### **📋 Update Process:**
1. **Identify Need**: Document improvement needed
2. **Propose Change**: Create proposal
3. **Team Review**: Get agent feedback
4. **Implement**: Update protocol
5. **Communicate**: Notify all agents
6. **Train**: Ensure understanding

### **📅 Review Schedule:**
- **Monthly**: Protocol effectiveness review
- **Quarterly**: Major updates and improvements
- **As Needed**: Emergency updates

---

## 📚 **REFERENCE LINKS**

### **🔗 Internal Documentation:**
- [V2 Compliance Standards](../README.md#v2-compliance)
- [Agent Workflow Guide](../AGENT_WORKFLOW_GUIDE.md)
- [Quality Gates](../quality_gates.py)
- [CI/CD Pipeline](../.github/workflows/ci-cd.yml)

### **🔗 External References:**
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Semantic Versioning](https://semver.org/)

---

## 📝 **PROTOCOL ACKNOWLEDGMENT**

By using this protocol system, all agents agree to:
- Follow established workflows
- Maintain code quality standards
- Document all changes
- Coordinate effectively with team
- Report status regularly
- Respond to emergencies promptly

**Last Updated**: 2025-01-18  
**Next Review**: 2025-02-18  
**Version**: 1.0  

---

**🐝 WE ARE SWARM** - Standardized protocols for consistent, high-quality development across all projects!
