# V2 Compliance - JavaScript LOC Enforcement

## 🚀 Overview

This project enforces **V2 Compliance Standards** for JavaScript/TypeScript files through automated LOC (Lines of Code) limits and code quality checks.

## 📏 LOC Limits (V2 Standards)

### Per File
- **Maximum**: 300 lines (hard limit)
- **Warning**: 250 lines
- **Rationale**: Files over 300 lines become hard to maintain and review

### Per Function
- **Maximum**: 30 lines (hard limit)
- **Warning**: 25 lines
- **Rationale**: Functions over 30 lines are complex and hard to test

### Per Class/Module
- **Maximum**: 500 lines
- **Rationale**: Large modules violate single responsibility principle

## 🛠️ Usage

### Quick Start
```bash
# Install dependencies
npm install

# Run basic linting
npm run lint

# Auto-fix issues
npm run lint:fix

# Strict V2 compliance check
npm run lint:v2

# Check LOC for largest files
npm run loc:check

# Complete V2 audit
npm run v2:audit
```

### CI/CD Integration
```bash
# In your CI pipeline
npm run ci  # Fails if any V2 compliance issues
```

### Pre-commit Hooks
```bash
# Automatic V2 compliance check before commits
npm run pre-commit
```

## 📊 Monitoring

### LOC Distribution Check
```bash
npm run loc:check
```
Shows the 20 largest files by line count:
```
   450 src/services/messaging-core.js
   380 src/utils/validation-utils.js
   320 src/services/agent-coordinator.js
   ...
```

### ESLint Reports
- **Errors**: Must be fixed immediately
- **Warnings**: Should be addressed soon
- **Suggestions**: Nice to have improvements

## 🔧 Configuration

### ESLint Rules Summary
- `max-lines`: 300 lines per file
- `max-lines-per-function`: 30 lines per function
- `complexity`: Maximum 10
- `max-params`: Maximum 4 parameters
- `max-depth`: Maximum 4 nesting levels

### File Type Overrides
- **Test files**: No LOC limits (flexibility for comprehensive tests)
- **Config files**: Relaxed limits (webpack.config.js, etc.)
- **Utility modules**: 400 lines max (but functions still 20 lines)

## 📈 Benefits

### Code Quality
- ✅ **Better Maintainability**: Smaller files are easier to understand
- ✅ **Faster Reviews**: Code reviews are quicker with smaller chunks
- ✅ **Easier Testing**: Small functions are easier to unit test
- ✅ **Reduced Bugs**: Complex code has fewer edge cases

### Team Productivity
- ✅ **Faster Onboarding**: New developers understand code faster
- ✅ **Parallel Development**: Smaller modules reduce merge conflicts
- ✅ **Easier Refactoring**: Isolated code is easier to change
- ✅ **Better Documentation**: Clear boundaries make docs simpler

## 🚨 Common Issues & Solutions

### File Too Large (>300 lines)
**Solution**: Split into smaller modules
```javascript
// ❌ Bad: One large file
// src/services/user-service.js (450 lines)

// ✅ Good: Multiple focused modules
// src/services/user/user-repository.js (120 lines)
// src/services/user/user-validation.js (80 lines)
// src/services/user/user-controller.js (150 lines)
// src/services/user/index.js (50 lines)
```

### Function Too Long (>30 lines)
**Solution**: Extract helper functions
```javascript
// ❌ Bad: One long function
function processUserData(user) {
  // 45 lines of mixed logic
}

// ✅ Good: Multiple focused functions
function validateUserData(user) {
  // 10 lines: validation logic
}

function transformUserData(user) {
  // 8 lines: transformation logic
}

function processUserData(user) {
  // 12 lines: orchestration
  validateUserData(user);
  const transformed = transformUserData(user);
  return saveUser(transformed);
}
```

## 🎯 V2 Compliance Checklist

- [ ] All JavaScript files under 300 lines
- [ ] All functions under 30 lines
- [ ] Complexity score under 10
- [ ] No more than 4 parameters per function
- [ ] Maximum 4 levels of nesting
- [ ] ESLint passes with zero errors
- [ ] All tests pass
- [ ] Code coverage >85%

## 📞 Support

For questions about V2 compliance:
1. Run `npm run v2:audit` to check current status
2. Check ESLint output for specific violations
3. Review the examples above for refactoring patterns
4. Contact the Swarm coordination team for complex cases

---

**Remember**: V2 Compliance isn't just about LOC limits—it's about creating maintainable, testable, and scalable code that supports the Swarm's 8x efficiency goals! ⚡

