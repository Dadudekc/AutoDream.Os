/**
 * System Integration Test V2 - V2 Compliant Modular Architecture
 * Main orchestrator for system integration testing using modular components
 * REFACTORED: 530 lines → ~250 lines (53% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved through modular design
 *
 * @author Agent-8 - Integration & Performance Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { SystemIntegrationTestCore } from './system-integration-test-core.js';
import { SystemIntegrationTestMethods } from './system-integration-test-methods.js';
import { SystemIntegrationTestReporting } from './system-integration-test-reporting.js';

// ================================
// SYSTEM INTEGRATION TEST V2
// ================================

/**
 * Main system integration test orchestrator
 * COORDINATES modular test components for V2 compliance
 */
export class SystemIntegrationTestV2 {
    constructor() {
        this.core = new SystemIntegrationTestCore();
        this.testMethods = new SystemIntegrationTestMethods(this.core);
        this.reporting = new SystemIntegrationTestReporting(this.core);
        this.isInitialized = false;
    }

    /**
     * Initialize the system integration test system
     */
    async initialize() {
        if (this.isInitialized) return;
        
        console.log('🚀 Initializing System Integration Test V2...');
        
        await this.core.initialize();
        await this.testMethods.initialize();
        await this.reporting.initialize();
        
        this.isInitialized = true;
        console.log('✅ System Integration Test V2 initialized');
    }

    /**
     * Run all integration tests
     */
    async runAllTests() {
        if (!this.isInitialized) {
            await this.initialize();
        }

        console.log('🚀 STARTING SYSTEM INTEGRATION TEST SUITE V2...');
        const startTime = performance.now();

        try {
            // Run all test methods
            await this.testMethods.runAllTestMethods();
            
            // Generate comprehensive report
            const results = this.reporting.generateTestReport();
            
            // Update performance metrics
            this.core.updatePerformanceMetrics('totalSystemTime', performance.now() - startTime);
            
            return results;
            
        } catch (error) {
            console.error('❌ CRITICAL TEST FAILURE:', error);
            this.core.recordTestResult('CRITICAL_ERROR', false, error.message);
            throw error;
        }
    }

    /**
     * Run specific test category
     */
    async runTestCategory(category) {
        if (!this.isInitialized) {
            await this.initialize();
        }

        console.log(`🎯 Running test category: ${category}`);
        
        switch (category) {
            case 'components':
                return await this.testMethods.testComponentIntegration();
            case 'performance':
                return await this.testMethods.testPerformanceValidation();
            case 'compatibility':
                return await this.testMethods.testBackwardCompatibility();
            case 'error_handling':
                return await this.testMethods.testErrorHandling();
            case 'cross_component':
                return await this.testMethods.testCrossComponentIntegration();
            default:
                throw new Error(`Unknown test category: ${category}`);
        }
    }

    /**
     * Get test results summary
     */
    getTestResultsSummary() {
        return this.reporting.getTestResultsSummary();
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return this.core.getPerformanceMetrics();
    }

    /**
     * Get system status
     */
    getSystemStatus() {
        return {
            initialized: this.isInitialized,
            core: this.core.getStatus(),
            testMethods: this.testMethods.getStatus(),
            reporting: this.reporting.getStatus()
        };
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.core.cleanup();
        this.testMethods.cleanup();
        this.reporting.cleanup();
        this.isInitialized = false;
        console.log('🧹 System Integration Test V2 cleaned up');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create system integration test instance
 */
export function createSystemIntegrationTestV2() {
    return new SystemIntegrationTestV2();
}

/**
 * Create and initialize system integration test
 */
export async function createAndInitializeSystemIntegrationTestV2() {
    const testSuite = new SystemIntegrationTestV2();
    await testSuite.initialize();
    return testSuite;
}

// ================================
// GLOBAL INSTANCE
// ================================

let globalSystemIntegrationTestV2 = null;

/**
 * Get global system integration test instance
 */
export function getSystemIntegrationTestV2() {
    if (!globalSystemIntegrationTestV2) {
        globalSystemIntegrationTestV2 = new SystemIntegrationTestV2();
    }
    return globalSystemIntegrationTestV2;
}

/**
 * Initialize global system integration test
 */
export async function initializeGlobalSystemIntegrationTestV2() {
    const testSuite = getSystemIntegrationTestV2();
    await testSuite.initialize();
    return testSuite;
}

// ================================
// AUTO-INITIALIZATION
// ================================

// Auto-run tests when loaded in browser environment
if (typeof window !== 'undefined') {
    window.SystemIntegrationTestV2 = SystemIntegrationTestV2;
    window.createSystemIntegrationTestV2 = createSystemIntegrationTestV2;
    window.getSystemIntegrationTestV2 = getSystemIntegrationTestV2;

    // Auto-run if this script is loaded directly
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('🔄 System Integration Test V2 loaded. Run: new SystemIntegrationTestV2().runAllTests()');
        });
    } else {
        console.log('🔄 System Integration Test V2 loaded. Run: new SystemIntegrationTestV2().runAllTests()');
    }
}

// ================================
// EXPORTS
// ================================

export default SystemIntegrationTestV2;
