/**
 * System Integration Test Core - V2 Compliant Core Module
 * Core functionality for system integration testing
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-8 - Integration & Performance Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// SYSTEM INTEGRATION TEST CORE
// ================================

/**
 * Core system integration test functionality
 */
export class SystemIntegrationTestCore {
    constructor() {
        this.testResults = [];
        this.passedTests = 0;
        this.failedTests = 0;
        this.testStartTime = null;
        this.testEndTime = null;
        this.performanceMetrics = new Map();
        this.isInitialized = false;
    }

    /**
     * Initialize core system
     */
    async initialize() {
        if (this.isInitialized) return;
        
        console.log('🔧 Initializing System Integration Test Core...');
        
        this.testResults = [];
        this.passedTests = 0;
        this.failedTests = 0;
        this.performanceMetrics.clear();
        
        this.isInitialized = true;
        console.log('✅ System Integration Test Core initialized');
    }

    /**
     * Start test execution
     */
    startTestExecution() {
        this.testStartTime = new Date();
        this.testResults = [];
        this.passedTests = 0;
        this.failedTests = 0;
        console.log('🚀 Test execution started');
    }

    /**
     * End test execution
     */
    endTestExecution() {
        this.testEndTime = new Date();
        console.log('🏁 Test execution completed');
    }

    /**
     * Record test result
     */
    recordTestResult(testName, passed, details = '') {
        const result = {
            testName,
            passed,
            details,
            timestamp: new Date().toISOString()
        };

        this.testResults.push(result);

        if (passed) {
            this.passedTests++;
            console.log(`✅ ${testName}: PASSED${details ? ' - ' + details : ''}`);
        } else {
            this.failedTests++;
            console.log(`❌ ${testName}: FAILED${details ? ' - ' + details : ''}`);
        }
    }

    /**
     * Update performance metrics
     */
    updatePerformanceMetrics(metricName, value) {
        this.performanceMetrics.set(metricName, {
            value,
            timestamp: new Date().toISOString()
        });
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return Object.fromEntries(this.performanceMetrics);
    }

    /**
     * Get test statistics
     */
    getTestStatistics() {
        const totalTests = this.testResults.length;
        const successRate = totalTests > 0 ? ((this.passedTests / totalTests) * 100).toFixed(2) : 0;
        const duration = this.testEndTime && this.testStartTime ? 
            this.testEndTime - this.testStartTime : 0;

        return {
            totalTests,
            passedTests: this.passedTests,
            failedTests: this.failedTests,
            successRate: parseFloat(successRate),
            duration,
            testResults: this.testResults
        };
    }

    /**
     * Get system status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            testExecutionActive: this.testStartTime !== null,
            totalTests: this.testResults.length,
            passedTests: this.passedTests,
            failedTests: this.failedTests
        };
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.testResults = [];
        this.passedTests = 0;
        this.failedTests = 0;
        this.testStartTime = null;
        this.testEndTime = null;
        this.performanceMetrics.clear();
        this.isInitialized = false;
        console.log('🧹 System Integration Test Core cleaned up');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create system integration test core instance
 */
export function createSystemIntegrationTestCore() {
    return new SystemIntegrationTestCore();
}

// ================================
// GLOBAL INSTANCE
// ================================

let globalSystemIntegrationTestCore = null;

/**
 * Get global system integration test core instance
 */
export function getSystemIntegrationTestCore() {
    if (!globalSystemIntegrationTestCore) {
        globalSystemIntegrationTestCore = new SystemIntegrationTestCore();
    }
    return globalSystemIntegrationTestCore;
}

// ================================
// EXPORTS
// ================================

export default SystemIntegrationTestCore;
