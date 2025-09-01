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

export class SystemIntegrationTest {
    constructor() {
        // Use the modular core orchestrator
        this.core = createSystemIntegrationTestCore();
    }

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

// Legacy factory function for existing code
export function createSystemIntegrationTest() {
    return new SystemIntegrationTest();
}

// ================================
// EXPORTS
// ================================

export default SystemIntegrationTest;
            const icon = status ? '✅' : '❌';
            console.log(`${icon} ${component.replace(/([A-Z])/g, ' $1').toLowerCase()}`);
        });

        console.log('\n⚡ Performance Metrics:');
        Object.entries(this.performanceMetrics).forEach(([metric, value]) => {
            console.log(`${metric}: ${typeof value === 'number' ? value.toFixed(2) + 'ms' : value}`);
        });

        const overallSuccess = Object.values(this.systemHealth).every(status => status);
        console.log(`\n🎯 Overall System Status: ${overallSuccess ? '✅ SUCCESS' : '❌ NEEDS ATTENTION'}`);
    }

    getTestResults() { return { ...this.testResults }; }
    getSystemHealth() { return { ...this.systemHealth }; }
    getPerformanceMetrics() { return { ...this.performanceMetrics }; }
}

export function createSystemIntegrationTest() {
    return new SystemIntegrationTest();
}

export default SystemIntegrationTest;