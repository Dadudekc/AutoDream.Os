/**
 * System Integration Test Executor - V2 Compliant Test Execution Engine
 * Specialized test execution and orchestration methods
 * V2 COMPLIANCE: Under 100-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class SystemIntegrationTestExecutor {
    constructor() {
        this.executionStats = {
            totalTests: 0,
            passedTests: 0,
            failedTests: 0,
            skippedTests: 0,
            executionTime: 0
        };
    }

    async executeTestSuite(suiteName, tests, options = {}) {
        console.log(`🏃 Executing ${suiteName} test suite...`);
        const startTime = performance.now();

        const results = {
            suiteName,
            tests: [],
            summary: { passed: 0, failed: 0, skipped: 0, total: tests.length },
            executionTime: 0,
            success: false
        };

        for (const test of tests) {
            try {
                const testStartTime = performance.now();
                const testResult = await test();
                const testExecutionTime = performance.now() - testStartTime;

                testResult.executionTime = testExecutionTime;
                results.tests.push(testResult);

                if (testResult.success) {
                    results.summary.passed++;
                } else {
                    results.summary.failed++;
                }
            } catch (error) {
                console.error(`❌ Test execution failed:`, error);
                results.tests.push({
                    name: 'Unknown Test',
                    success: false,
                    error: error.message,
                    executionTime: 0
                });
                results.summary.failed++;
            }
        }

        results.executionTime = performance.now() - startTime;
        results.success = results.summary.failed === 0;

        this.updateExecutionStats(results);
        this.logExecutionResults(results);

        return results;
    }

    updateExecutionStats(results) {
        this.executionStats.totalTests += results.summary.total;
        this.executionStats.passedTests += results.summary.passed;
        this.executionStats.failedTests += results.summary.failed;
        this.executionStats.executionTime += results.executionTime;
    }

    logExecutionResults(results) {
        console.log(`📊 ${results.suiteName} Results:`);
        console.log(`   ✅ Passed: ${results.summary.passed}`);
        console.log(`   ❌ Failed: ${results.summary.failed}`);
        console.log(`   ⏱️  Time: ${results.executionTime.toFixed(2)}ms`);
        console.log(`   🎯 Success: ${results.success ? 'YES' : 'NO'}`);
    }

    getExecutionStats() {
        return { ...this.executionStats };
    }

    resetExecutionStats() {
        this.executionStats = {
            totalTests: 0,
            passedTests: 0,
            failedTests: 0,
            skippedTests: 0,
            executionTime: 0
        };
    }
}

// Factory function
export function createTestExecutor() {
    return new SystemIntegrationTestExecutor();
}
