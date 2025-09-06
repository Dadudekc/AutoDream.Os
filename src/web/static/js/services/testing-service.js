/**
 * Testing Service - V2 Compliant Orchestrator
 * Orchestrator for testing operations using modular components
 * REFACTORED: 456 lines → ~80 lines (82% reduction)
 * Now uses modular components for V2 compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { TestingRepository } from '../repositories/testing-repository.js';
import { executeTestSuite, getTestSuiteStatus } from './testing-execution-service.js';
import { validateComponent } from './testing-validation-service.js';
import { runPerformanceTest } from './testing-performance-service.js';
import { generateSummaryReport } from './testing-reporting-service.js';

// ================================
// TESTING SERVICE ORCHESTRATOR
// ================================

/**
 * Testing service orchestrator using modular components
 */
export class TestingService {
    constructor(testingRepository = null) {
        // Dependency injection with fallback
        this.testingRepository = testingRepository || new TestingRepository();
    }

    /**
     * Execute test suite
     */
    async executeTestSuite(suiteName, options = {}) {
        return executeTestSuite(suiteName, options);
    }

    /**
     * Validate component
     */
    async validateComponent(componentName, validationRules = []) {
        return validateComponent(componentName, validationRules);
    }

    /**
     * Run performance test
     */
    async runPerformanceTest(componentName, testScenario) {
        return runPerformanceTest(componentName, testScenario);
    }

    /**
     * Generate summary report
     */
    generateSummaryReport(suiteName, timeRange = '24h') {
        return generateSummaryReport(suiteName, timeRange);
    }

    /**
     * Get test suite status
     */
    getTestSuiteStatus(suiteName) {
        return getTestSuiteStatus(suiteName);
    }

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: true,
            repository: this.testingRepository ? 'connected' : 'disconnected',
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// GLOBAL TESTING SERVICE INSTANCE
// ================================

/**
 * Global testing service instance
 */
const testingService = new TestingService();

// ================================
// SERVICE API FUNCTIONS
// ================================

/**
 * Get testing service instance
 */
export function getTestingService(testingRepository = null) {
    if (testingRepository) {
        return new TestingService(testingRepository);
    }
    return testingService;
}

// ================================
// EXPORTS
// ================================

export { TestingService, testingService };
export default testingService;
