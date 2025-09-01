/**
 * System Integration Test - Phase 3 Final Implementation
 * Main integration file using modular architecture
 * V2 Compliance: Under 300-line limit through modular design
 */

import { SystemIntegrationCore } from './system-integration-core.js';
import { SystemIntegrationReporting } from './system-integration-reporting.js';
import { SystemIntegrationTests } from './system-integration-tests.js';

class SystemIntegrationTest {
    constructor() {
        this.core = new SystemIntegrationCore();
        this.tests = new SystemIntegrationTests(this.core);
        this.reporting = new SystemIntegrationReporting(this.core);
    }

    // Run complete system integration test
    async runSystemIntegrationTest() {
        console.log('🚀 Starting System Integration Test - Phase 3 Final Implementation...');
        const startTime = performance.now();

        try {
            await this.tests.testComponentIntegration();
            await this.tests.testPerformanceOptimization();
            await this.tests.testErrorHandling();
            await this.tests.testBackwardCompatibility();
            await this.tests.testV2Compliance();
            await this.tests.testDeploymentReadiness();

            this.core.updatePerformanceMetrics('totalSystemTime', performance.now() - startTime);
            this.reporting.generateSystemIntegrationReport();
        } catch (error) {
            console.error('System integration test failed:', error);
            this.core.recordTestResult('System Integration Test Suite', false, error.message);
        }
    }

    // Get system integration summary
    getSystemIntegrationSummary() {
        return this.reporting.getSystemIntegrationSummary();
    }

    // Get core data
    getCoreData() {
        return this.core.getCoreData();
    }
}

// Run system integration test when loaded
if (typeof window !== 'undefined') {
    const systemTest = new SystemIntegrationTest();
    systemTest.runSystemIntegrationTest();
}

export { SystemIntegrationTest };
