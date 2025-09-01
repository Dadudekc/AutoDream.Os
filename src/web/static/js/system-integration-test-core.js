/**
 * System Integration Test Core - V2 Compliant Orchestrator
 * Core orchestrator for system integration test modules
 * V2 COMPLIANCE: Under 100-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

import { createErrorTests } from './system-integration-error-tests.js';
import { createCompatibilityTests } from './system-integration-compatibility-tests.js';
import { createComplianceTests } from './system-integration-compliance-tests.js';
import { createDeploymentTests } from './system-integration-deployment-tests.js';
import { createTestExecutor } from './system-integration-test-executor.js';
import { createTestReporter } from './system-integration-test-reporter.js';

export class SystemIntegrationTestCore {
    constructor() {
        this.testResults = { passed: 0, failed: 0, total: 0, details: [] };
        this.systemHealth = {
            componentIntegration: false,
            performanceOptimization: false,
            errorHandling: false,
            backwardCompatibility: false,
            v2Compliance: false,
            deploymentReadiness: false
        };
        this.performanceMetrics = {
            initializationTime: 0,
            componentLoadTime: 0,
            integrationTime: 0,
            totalSystemTime: 0
        };

        // Initialize modular components
        this.errorTests = createErrorTests(this.systemHealth, this.testResults);
        this.compatibilityTests = createCompatibilityTests(this.systemHealth, this.testResults);
        this.complianceTests = createComplianceTests(this.systemHealth, this.testResults);
        this.deploymentTests = createDeploymentTests(this.systemHealth, this.testResults);
        this.testExecutor = createTestExecutor();
        this.testReporter = createTestReporter(this.systemHealth, this.testResults, this.performanceMetrics);
    }

    async runSystemIntegrationTest() {
        console.log('🚀 Starting System Integration Test Core...');
        const startTime = performance.now();

        try {
            // Execute all test suites
            await this.errorTests.runErrorTests();
            await this.compatibilityTests.runCompatibilityTests();
            await this.complianceTests.runComplianceTests();
            await this.deploymentTests.runDeploymentTests();

            this.performanceMetrics.totalSystemTime = performance.now() - startTime;
            await this.testReporter.generateReport();
        } catch (error) {
            console.error('❌ System integration test failed:', error);
        }

        console.log(`⏱️ Testing completed in ${(performance.now() - startTime).toFixed(2)}ms`);
    }

    getSystemHealth() {
        return { ...this.systemHealth };
    }

    getTestResults() {
        return { ...this.testResults };
    }

    getPerformanceMetrics() {
        return { ...this.performanceMetrics };
    }
}

// Factory function for backward compatibility
export function createSystemIntegrationTestCore() {
    return new SystemIntegrationTestCore();
}
