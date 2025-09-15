# 🎯 V2 JavaScript Compliance Rules

## **📏 FILE SIZE LIMITS**
### **Maximum Line Counts**:
- **Main Application Files**: 300 lines maximum
- **Component Files**: 200 lines maximum  
- **Utility/Helper Files**: 150 lines maximum
- **Configuration Files**: 100 lines maximum
- **Test Files**: 250 lines maximum

### **Enforcement**:
- Files exceeding limits MUST be refactored into modular components
- Use ES6 modules for proper separation of concerns
- Implement dependency injection for shared utilities

## **🏗️ ARCHITECTURE PRINCIPLES**
### **Modular Design**:
- **Single Responsibility**: Each file should have one clear purpose
- **Dependency Injection**: Pass dependencies as parameters, don't import everything
- **Composition over Inheritance**: Use composition patterns for complex functionality
- **Interface Segregation**: Create focused, specific interfaces

### **Module Organization**:
```
src/web/static/js/
├── core/           # Core application logic (300 line limit)
├── components/     # UI components (200 line limit)
├── services/       # Business logic services (200 line limit)
├── utils/          # Utility functions (150 line limit)
├── config/         # Configuration files (100 line limit)
└── tests/          # Test files (250 line limit)
```

## **📦 MODULE SYSTEM REQUIREMENTS**
### **ES6 Modules**:
- Use `import`/`export` statements exclusively
- No global variables or window object pollution
- Explicit dependency declarations
- Tree-shaking compatible exports

### **Import/Export Standards**:
```javascript
// ✅ GOOD: Named exports with clear naming
export { DashboardManager, initializeDashboard };
export const CONFIG = { /* ... */ };

// ✅ GOOD: Default export for main class
export default class DashboardOrchestrator { /* ... */ }

// ❌ BAD: Global variables
window.DashboardManager = class { /* ... */ };
```

## **🎨 COMPONENT ARCHITECTURE**
### **Component Structure**:
```javascript
/**
 * ComponentName - Brief description
 * @author Agent-X
 * @version X.X.X
 * @description Detailed component description
 */
export class ComponentName {
    constructor(options = {}) {
        // Initialize with dependency injection
        this.dependencies = options.dependencies || {};
        this.config = { ...this.defaultConfig, ...options.config };
    }

    async initialize() {
        // Component initialization
    }

    destroy() {
        // Cleanup and memory management
    }
}

// Factory function for dependency injection
export function createComponentName(dependencies, config) {
    return new ComponentName({ dependencies, config });
}
```

### **Component Size Limits**:
- **UI Components**: 200 lines maximum
- **Service Components**: 200 lines maximum
- **Utility Components**: 150 lines maximum

## **🔄 DEPENDENCY MANAGEMENT**
### **Dependency Injection Pattern**:
```javascript
// ✅ GOOD: Dependency injection
class DashboardManager {
    constructor({ dataService, uiService, configService }) {
        this.dataService = dataService;
        this.uiService = uiService;
        this.configService = configService;
    }
}

// ❌ BAD: Direct imports creating tight coupling
import { DataService } from './data-service.js';
import { UIService } from './ui-service.js';
```

### **Circular Dependency Prevention**:
- Use dependency injection to break circular imports
- Create shared interfaces/contracts
- Implement event-driven communication between modules

## **📊 PERFORMANCE REQUIREMENTS**
### **Bundle Size Limits**:
- **Main Bundle**: < 500KB gzipped
- **Component Bundles**: < 100KB gzipped
- **Utility Bundles**: < 50KB gzipped

### **Loading Performance**:
- Implement lazy loading for non-critical components
- Use dynamic imports for code splitting
- Minimize initial bundle size

### **Runtime Performance**:
- Avoid blocking operations in main thread
- Use Web Workers for heavy computations
- Implement proper memory management

## **🧪 TESTING REQUIREMENTS**
### **Test Coverage**:
- **Minimum Coverage**: 85%
- **Critical Paths**: 100% coverage required
- **Component Tests**: All public methods tested

### **Test Structure**:
```javascript
/**
 * ComponentName.test.js
 * @description Tests for ComponentName
 */
import { ComponentName, createComponentName } from './component-name.js';

describe('ComponentName', () => {
    let component;
    let mockDependencies;

    beforeEach(() => {
        mockDependencies = {
            dataService: createMockDataService(),
            uiService: createMockUIService()
        };
        component = createComponentName(mockDependencies);
    });

    afterEach(() => {
        component?.destroy();
    });

    describe('initialization', () => {
        it('should initialize successfully with valid dependencies', async () => {
            await expect(component.initialize()).resolves.not.toThrow();
        });
    });
});
```

## **🔧 CODE QUALITY STANDARDS**
### **Function Size Limits**:
- **Functions**: 30 lines maximum
- **Methods**: 25 lines maximum
- **Arrow Functions**: 15 lines maximum

### **Complexity Limits**:
- **Cyclomatic Complexity**: Maximum 10
- **Nesting Depth**: Maximum 3 levels
- **Parameter Count**: Maximum 5 parameters

### **Naming Conventions**:
- **Classes**: PascalCase (`DashboardManager`)
- **Functions/Methods**: camelCase (`initializeDashboard`)
- **Constants**: UPPER_SNAKE_CASE (`API_ENDPOINTS`)
- **Private Methods**: Leading underscore (`_internalMethod`)

## **📝 DOCUMENTATION REQUIREMENTS**
### **JSDoc Standards**:
```javascript
/**
 * Initialize the dashboard with provided configuration
 * @param {Object} config - Dashboard configuration object
 * @param {string} config.theme - Theme name ('dark' | 'light')
 * @param {boolean} config.enableRealTime - Enable real-time updates
 * @param {Object} dependencies - Injected dependencies
 * @param {DataService} dependencies.dataService - Data service instance
 * @returns {Promise<void>} Promise that resolves when initialization is complete
 * @throws {Error} When configuration is invalid
 * @example
 * await dashboard.initialize({
 *   theme: 'dark',
 *   enableRealTime: true
 * }, { dataService: mockDataService });
 */
async initialize(config, dependencies) {
    // Implementation
}
```

### **Required Documentation**:
- All public methods must have JSDoc comments
- Complex algorithms must include inline comments
- Configuration objects must be documented
- Error conditions must be documented

## **🚨 ERROR HANDLING REQUIREMENTS**
### **Error Handling Patterns**:
```javascript
// ✅ GOOD: Proper error handling with context
async loadData() {
    try {
        const data = await this.dataService.fetchData();
        return this.processData(data);
    } catch (error) {
        this.logger.error('Failed to load data', {
            error: error.message,
            context: 'DashboardDataManager.loadData',
            timestamp: new Date().toISOString()
        });
        throw new DataLoadError('Failed to load dashboard data', { originalError: error });
    }
}

// ❌ BAD: Silent error handling
async loadData() {
    try {
        return await this.dataService.fetchData();
    } catch (error) {
        // Silent failure - no logging or error propagation
        return null;
    }
}
```

### **Error Types**:
- Create specific error classes for different error types
- Include context and original error information
- Implement proper error logging and monitoring

## **🔄 STATE MANAGEMENT**
### **State Management Patterns**:
```javascript
// ✅ GOOD: Immutable state updates
class StateManager {
    updateState(updates) {
        this.state = { ...this.state, ...updates };
        this.notifyStateChange();
    }

    getState() {
        return { ...this.state }; // Return copy to prevent mutation
    }
}

// ❌ BAD: Direct state mutation
class StateManager {
    updateState(updates) {
        Object.assign(this.state, updates); // Direct mutation
    }
}
```

## **📱 ACCESSIBILITY REQUIREMENTS**
### **ARIA Standards**:
- All interactive elements must have proper ARIA labels
- Implement keyboard navigation support
- Ensure screen reader compatibility
- Provide focus management

### **Accessibility Testing**:
- Use automated accessibility testing tools
- Manual testing with screen readers
- Keyboard-only navigation testing

## **🔒 SECURITY REQUIREMENTS**
### **Input Validation**:
- Validate all user inputs
- Sanitize data before DOM manipulation
- Use Content Security Policy (CSP)
- Implement proper XSS protection

### **Data Handling**:
- Never store sensitive data in localStorage
- Use secure communication protocols
- Implement proper authentication checks

## **📊 MONITORING & LOGGING**
### **Performance Monitoring**:
```javascript
// ✅ GOOD: Performance monitoring
class PerformanceMonitor {
    measureFunction(name, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        
        this.logger.info('Performance measurement', {
            function: name,
            duration: end - start,
            timestamp: new Date().toISOString()
        });
        
        return result;
    }
}
```

### **Logging Standards**:
- Use structured logging with context
- Include timestamps and correlation IDs
- Implement log levels (error, warn, info, debug)
- Avoid logging sensitive information

## **🚀 DEPLOYMENT REQUIREMENTS**
### **Build Optimization**:
- Minify and compress JavaScript files
- Implement tree shaking for unused code
- Use code splitting for large applications
- Optimize bundle loading order

### **Environment Configuration**:
- Use environment-specific configurations
- Implement feature flags for gradual rollouts
- Separate development and production builds

## **✅ COMPLIANCE CHECKLIST**
### **Before Deployment**:
- [ ] All files under line count limits
- [ ] ES6 modules used throughout
- [ ] Dependency injection implemented
- [ ] Test coverage ≥ 85%
- [ ] JSDoc documentation complete
- [ ] Error handling implemented
- [ ] Performance benchmarks met
- [ ] Accessibility standards met
- [ ] Security requirements satisfied
- [ ] Bundle size limits respected

### **Code Review Requirements**:
- [ ] Architecture compliance verified
- [ ] Performance impact assessed
- [ ] Security implications reviewed
- [ ] Accessibility compliance checked
- [ ] Test coverage validated
- [ ] Documentation completeness verified

## **🎯 ENFORCEMENT**
### **Automated Checks**:
- ESLint rules for code quality
- Bundle size monitoring
- Test coverage enforcement
- Performance regression detection

### **Manual Reviews**:
- Architecture compliance review
- Security assessment
- Accessibility audit
- Performance optimization review

---

**📋 V2 JavaScript Compliance Rules - Agent-7 Web Development Specialist**
**Version**: 1.0.0
**Last Updated**: 2025-01-14
**Status**: ACTIVE