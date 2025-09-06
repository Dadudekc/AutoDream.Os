/**
 * System Integration Test V3 - V2 Compliant Modular Orchestrator
 * Main orchestrator using specialized modular components
 * REFACTORED: 446 lines → ~60 lines (87% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR COMPONENTS
// ================================

import { createSystemIntegrationTestCore } from './system-integration-test-core.js';

// ================================
// SYSTEM INTEGRATION TEST V3
// ================================

/**
 * Main system integration test orchestrator
 * COORDINATES modular test components for V2 compliance
 */
export class SystemIntegrationTest {
    constructor() {
        // Use the modular core orchestrator
        this.core = createSystemIntegrationTestCore();
    }

    /**
     * Run system integration test
     */
    async runSystemIntegrationTest() {
        console.log('🚀 Starting System Integration Test V3...');
        await this.core.runSystemIntegrationTest();
        console.log('✅ System Integration Test V3 completed successfully');
    }

    // Delegate methods to core for backward compatibility
    getSystemHealth() {
        return this.core.getSystemHealth();
    }

    getTestResults() {
        return this.core.getTestResults();
    }

    getPerformanceMetrics() {
        return this.core.getPerformanceMetrics();
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Factory function for SystemIntegrationTest
 */
export function createSystemIntegrationTest() {
    return new SystemIntegrationTest();
}

/**
 * Default export for backward compatibility
 */
export default SystemIntegrationTest;
