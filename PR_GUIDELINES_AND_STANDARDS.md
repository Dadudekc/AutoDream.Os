# Pull Request Guidelines and Standards
**Repository:** Agent_Cellphone_V2_Repository  
**Effective Date:** August 28, 2025  
**Version:** 1.0  
**Status:** MANDATORY - All team members must follow

## 🚨 Critical Requirements

### File Size Limits
- **Maximum file size:** 400 lines per file
- **Violation:** Automatic rejection
- **Exception:** None - this is a hard requirement

### PR Size Limits
- **Maximum changes:** 500 lines per PR
- **Maximum files:** 20 files per PR
- **Violation:** Automatic rejection

### Scope Requirements
- **One focused change per PR**
- **Single responsibility principle**
- **No unrelated changes**

## 📋 PR Creation Guidelines

### Before Creating a PR
1. **Self-review your changes**
   - Check file sizes (must be under 400 lines)
   - Count total lines changed (must be under 500)
   - Ensure single, focused purpose
   - Run tests locally

2. **Branch naming convention**
   - Format: `feature/description` or `fix/description`
   - Examples: `feature/add-user-authentication`, `fix/memory-leak-in-cache`
   - No generic names like `refactor` or `update`

3. **Commit message standards**
   - Format: `type(scope): description`
   - Examples: `feat(auth): add JWT token validation`, `fix(core): resolve memory leak in manager`
   - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### PR Description Template
```markdown
## Description
Brief description of what this PR accomplishes

## Changes Made
- [ ] Specific change 1
- [ ] Specific change 2
- [ ] Specific change 3

## Files Modified
- `path/to/file1.py` (X lines changed)
- `path/to/file2.py` (Y lines changed)

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] No new warnings or errors

## Compliance
- [ ] All files under 400 lines
- [ ] Total changes under 500 lines
- [ ] Single focused change
- [ ] Documentation updated

## Related Issues
Closes #123, Addresses #456
```

## 🔍 Code Review Process

### Review Requirements
- **Small PRs (< 100 lines):** 1 approval required
- **Medium PRs (100-300 lines):** 2 approvals required
- **Large PRs (300-500 lines):** 3 approvals required
- **All PRs:** Must pass automated checks

### Review Checklist
- [ ] **Code Quality**
  - [ ] Code follows style guidelines
  - [ ] No obvious bugs or issues
  - [ ] Proper error handling
  - [ ] Input validation where needed

- [ ] **Architecture**
  - [ ] Changes align with system design
  - [ ] No circular dependencies
  - [ ] Proper separation of concerns
  - [ ] Follows established patterns

- [ ] **Testing**
  - [ ] Adequate test coverage
  - [ ] Tests are meaningful
  - [ ] No test code in production
  - [ ] Edge cases covered

- [ ] **Documentation**
  - [ ] Code is self-documenting
  - [ ] Complex logic explained
  - [ ] API changes documented
  - [ ] README updated if needed

### Review Comments
- **Be constructive and specific**
- **Suggest solutions, not just problems**
- **Use @mentions for specific team members**
- **Mark as resolved when addressed**

## 🚫 Common Rejection Reasons

### Automatic Rejections
1. **File size violations**
   - Any file over 400 lines
   - No exceptions or overrides

2. **PR size violations**
   - Total changes over 500 lines
   - Over 20 files changed

3. **Scope violations**
   - Multiple unrelated changes
   - Massive architectural changes
   - Refactoring entire modules

4. **Quality violations**
   - Failing tests
   - Build errors
   - Style violations
   - Security issues

### Manual Rejection Criteria
1. **Poor code quality**
   - Hard to understand
   - No error handling
   - Performance issues
   - Security vulnerabilities

2. **Inadequate testing**
   - Missing tests
   - Poor test coverage
   - Tests don't validate functionality

3. **Documentation issues**
   - Unclear code
   - Missing documentation
   - Outdated documentation

## 🛠️ Automated Checks

### Pre-commit Hooks
- File size validation
- Code style checking
- Basic syntax validation
- Security scanning

### CI/CD Pipeline
- Automated testing
- Code coverage reporting
- Static analysis
- Security scanning
- Performance benchmarking

### Branch Protection
- Required status checks
- Required reviews
- No direct pushes to main
- Up-to-date branch requirements

## 📊 Metrics and Monitoring

### PR Health Metrics
- **Average PR size** (target: < 300 lines)
- **Review time** (target: < 24 hours)
- **Approval rate** (target: > 90%)
- **Rejection rate** (target: < 10%)

### Quality Metrics
- **Test coverage** (target: > 80%)
- **Code duplication** (target: < 5%)
- **Technical debt** (monitor trends)
- **Security vulnerabilities** (target: 0)

## 🔄 Refactoring Guidelines

### Large Refactoring Strategy
1. **Break into phases**
   - Each phase under 500 lines
   - Focused on specific concerns
   - Maintainable increments

2. **Phase planning**
   - Clear milestones
   - Rollback points
   - Testing strategy
   - Communication plan

3. **Implementation**
   - One phase per PR
   - Thorough testing
   - Documentation updates
   - Team coordination

### Refactoring PR Template
```markdown
## Refactoring Phase X of Y
**Phase:** [Phase number and description]
**Total Phases:** [Total number of phases]
**Previous Phase:** [Link to previous phase PR]
**Next Phase:** [Description of next phase]

## Changes in This Phase
- [ ] Specific refactoring 1
- [ ] Specific refactoring 2

## Impact Assessment
- **Risk Level:** [Low/Medium/High]
- **Rollback Plan:** [Description]
- **Testing Strategy:** [Description]

## Dependencies
- [ ] Phase X-1 completed
- [ ] Tests updated
- [ ] Documentation updated
```

## 📚 Best Practices

### Code Organization
- **Single responsibility per file**
- **Logical file grouping**
- **Consistent naming conventions**
- **Clear import structure**

### Error Handling
- **Graceful degradation**
- **Meaningful error messages**
- **Proper logging**
- **User-friendly feedback**

### Performance
- **Efficient algorithms**
- **Minimal memory usage**
- **Fast execution**
- **Scalable design**

### Security
- **Input validation**
- **Output sanitization**
- **Access control**
- **Secure defaults**

## 🆘 Getting Help

### When to Ask for Help
- **Unclear requirements**
- **Complex architectural decisions**
- **Performance concerns**
- **Security questions**
- **Testing strategies**

### Resources
- **Team lead consultation**
- **Code review feedback**
- **Documentation review**
- **Architecture review**
- **Security review**

## 📝 Change Log

### Version 1.0 (August 28, 2025)
- Initial guidelines established
- File size limits: 400 lines
- PR size limits: 500 lines
- Mandatory review process
- Automated checks required

---

**Remember:** These guidelines exist to maintain code quality and team productivity. Following them ensures your PRs are reviewed quickly and merged successfully.

**Questions or concerns?** Contact the team lead or create an issue for clarification.
