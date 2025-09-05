# V2 Compliance - JavaScript LOC Enforcement

## 🚀 Overview

This project enforces **V2 Compliance Standards** for JavaScript/TypeScript files through automated LOC (Lines of Code) limits and code quality checks.

## 📏 V2 COMPLIANCE STANDARDS - UPDATED 2025-01-27

### 🎯 **CORE PHILOSOPHY: CLEAN, TESTED, CLASS-BASED, REUSABLE, SCALABLE CODE**

**The real goal of V2 compliance is ensuring:**
- ✅ **Clean Code**: Readable, maintainable, and well-structured  
- ✅ **Tested Code**: Comprehensive unit tests with >85% coverage
- ✅ **Class-Based**: Object-oriented design for complex domain logic
- ✅ **Reusable**: Modular components with clear interfaces
- ✅ **Scalable**: Architecture that supports growth and performance

### 📏 **FILE SIZE THRESHOLDS (Updated Strategy)**

#### **Strategic V2 Compliance Levels**
- 🚨 **CRITICAL VIOLATION**: >500 lines (immediate refactoring required)
- ⚠️ **MAJOR VIOLATION**: 400-500 lines (strategic refactoring target)  
- 📋 **MINOR VIOLATION**: 300-400 lines (acceptable with justification)
- ✅ **COMPLIANT**: <300 lines (ideal target)

**Rationale**: Focus development resources on eliminating truly problematic files (>400 lines) while maintaining code quality. Strategic efficiency over micro-optimization.

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

### ESLint Rules Summary (Updated)
- `max-lines`: 400 lines per file (strategic threshold, 300 ideal)
- `max-lines-per-function`: 30 lines per function
- `complexity`: Maximum 10
- `max-params`: Maximum 4 parameters
- `max-depth`: Maximum 4 nesting levels

### Code Quality Focus Areas
- **Clean Architecture**: Modular design with clear separation of concerns
- **Test Coverage**: Minimum 85% coverage for all production code
- **Type Safety**: Full TypeScript strict mode compliance
- **Error Handling**: Comprehensive exception handling and logging
- **Performance**: Optimized for scalability and high-frequency operations

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

### File Too Large (>400 lines - Strategic Threshold)
**Solution**: Refactor into modular components with orchestrator pattern
```javascript
// ❌ Bad: One monolithic file
// src/services/user-service.js (450 lines)

// ✅ Good: Modular architecture with orchestrator
// src/services/user/user-models.js (120 lines) - Data models & types
// src/services/user/user-repository.js (180 lines) - Data access layer
// src/services/user/user-validation.js (150 lines) - Business logic
// src/services/user/user-orchestrator.js (200 lines) - Coordination layer
// src/services/user/index.js (50 lines) - Public interface
```

### Files 300-400 Lines (Minor Violations)
**Acceptable with justification** - Focus on code quality over line count:
- Clean, well-structured code with clear responsibilities
- Comprehensive test coverage (>85%)
- Clear class-based design with dependency injection
- Proper error handling and logging

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

## 🎯 V2 Compliance Checklist (Updated)

### 🚨 **CRITICAL PRIORITIES**
- [ ] No files over 500 lines (immediate refactoring required)
- [ ] Strategic refactoring of files 400-500 lines
- [ ] All tests pass with >85% coverage
- [ ] ESLint passes with zero errors

### ✅ **QUALITY STANDARDS**
- [ ] Clean, class-based architecture with dependency injection
- [ ] Comprehensive error handling and logging
- [ ] Full type safety (TypeScript strict mode)
- [ ] Modular design with clear component boundaries
- [ ] All functions under 30 lines
- [ ] Complexity score under 10
- [ ] No more than 4 parameters per function
- [ ] Maximum 4 levels of nesting

### 📋 **ACCEPTABLE WITH JUSTIFICATION**
- [ ] Files 300-400 lines (minor violations, monitor and improve)
- [ ] Legacy code with migration plan to modular architecture

## 📞 Support

For questions about V2 compliance:
1. Run `npm run v2:audit` to check current status
2. Check ESLint output for specific violations
3. Review the examples above for refactoring patterns
4. Contact the Swarm coordination team for complex cases

---

**Remember**: V2 Compliance isn't just about LOC limits—it's about creating maintainable, testable, and scalable code that supports the Swarm's 8x efficiency goals! ⚡

