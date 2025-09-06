/**
 * System Integration Test Methods - V2 Compliant Modular Orchestrator
 * Main orchestrator using specialized modular components
 * REFACTORED: 357 lines → ~80 lines (78% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { SystemIntegrationTestMethodsCore, createSystemIntegrationTestMethodsCore } from './system-integration-test-methods-core.js';
import { SystemIntegrationTestMethodsForms, createSystemIntegrationTestMethodsForms } from './system-integration-test-methods-forms.js';
import { SystemIntegrationTestMethodsUI, createSystemIntegrationTestMethodsUI } from './system-integration-test-methods-ui.js';

// ================================
// SYSTEM INTEGRATION TEST METHODS
// ================================

/**
 * Main system integration test methods orchestrator
 * COORDINATES modular test components for V2 compliance
 */
export class SystemIntegrationTestMethods {
    constructor(testCore) {
        this.testCore = testCore;

        // Initialize modular components
        this.core = createSystemIntegrationTestMethodsCore(testCore);
        this.ui = createSystemIntegrationTestMethodsUI(testCore);
        this.forms = createSystemIntegrationTestMethodsForms(testCore);
    }

    /**
     * Run all system integration tests
     */
    async runAllTests() {
        console.log('🚀 Starting System Integration Tests...');

        try {
            // Run core component tests
            await this.core.testComponentImports();
            await this.core.testNavigationModule();
            await this.core.testModalModule();

            // Run UI component tests
            await this.ui.testUIComponents();

            // Run form component tests
            await this.forms.testFormComponents();

            console.log('✅ All System Integration Tests completed successfully');

        } catch (error) {
            console.error('❌ System Integration Tests failed:', error);
            this.testCore.logTestResult('ALL_TESTS', false, `Test execution error: ${error.message}`);
        }
    }

    /**
     * Run core component tests only
     */
    async runCoreTests() {
        await this.core.testComponentImports();
        await this.core.testNavigationModule();
        await this.core.testModalModule();
    }

    /**
     * Run UI component tests only
     */
    async runUITests() {
        await this.ui.testUIComponents();
    }

    /**
     * Run form component tests only
     */
    async runFormTests() {
        await this.forms.testFormComponents();
    }

    // Delegate methods to core for backward compatibility
    async testComponentImports() {
        return this.core.testComponentImports();
    }

    async testNavigationModule() {
        return this.core.testNavigationModule();
    }

    async testModalModule() {
        return this.core.testModalModule();
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Factory function for SystemIntegrationTestMethods
 */
export function createSystemIntegrationTestMethods(testCore) {
    return new SystemIntegrationTestMethods(testCore);
}

/**
 * Default export for backward compatibility
 */
export default SystemIntegrationTestMethods;
