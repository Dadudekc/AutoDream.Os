/**
 * Performance Test Orchestrator - V2 Compliant
 * Main orchestrator for performance testing
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createPerformanceTestRunnerModule } from './performance-test-runner-module.js';

// ================================
// PERFORMANCE TEST ORCHESTRATOR
// ================================

/**
 * Main orchestrator for performance testing
 */
export class PerformanceTestOrchestrator {
    constructor(systemHealth, testResults, performanceMetrics) {
        this.logger = console;

        // Initialize modules
        this.testRunner = createPerformanceTestRunnerModule(systemHealth, testResults, performanceMetrics);

        // Store references
        this.systemHealth = systemHealth;
        this.testResults = testResults;
        this.performanceMetrics = performanceMetrics;
    }

    /**
     * Run all performance tests
     */
    async runAllPerformanceTests() {
        this.logger.log('🚀 Starting Performance Test Suite...');

        try {
            const result = await this.testRunner.runPerformanceOptimization();

            if (this.testResults) {
                this.testResults.performance = result;
            }

            this.logger.log('✅ Performance Test Suite Completed');
            return result;
        } catch (error) {
            this.logger.error('❌ Performance Test Suite Failed:', error);

            if (this.testResults) {
                this.testResults.performance = {
                    name: 'Performance Test Suite',
                    success: false,
                    error: error.message
                };
            }

            return {
                name: 'Performance Test Suite',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Run specific performance test
     */
    async runSpecificTest(testName) {
        this.logger.log(`🎯 Running Specific Performance Test: ${testName}`);

        try {
            let result;

            switch (testName) {
                case 'initialization':
                    result = await this.testRunner.runInitializationTest();
                    break;
                case 'componentLoad':
                    result = await this.testRunner.runComponentLoadTest();
                    break;
                case 'memory':
                    result = await this.testRunner.runMemoryTest();
                    break;
                case 'caching':
                    result = await this.testRunner.runCachingTest();
                    break;
                case 'lazyLoading':
                    result = await this.testRunner.runLazyLoadingTest();
                    break;
                case 'bundle':
                    result = await this.testRunner.runBundleTest();
                    break;
                default:
                    throw new Error(`Unknown test: ${testName}`);
            }

            this.logger.log(`✅ Specific Test Completed: ${testName}`);
            return result;
        } catch (error) {
            this.logger.error(`❌ Specific Test Failed: ${testName}`, error);
            return {
                name: `${testName} Test`,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Run performance tests with custom configuration
     */
    async runPerformanceTestsWithConfig(config = {}) {
        this.logger.log('🔧 Running Performance Tests with Custom Configuration...');

        // Apply configuration
        if (config.testRunner) {
            Object.assign(this.testRunner, config.testRunner);
        }

        const result = await this.runAllPerformanceTests();

        // Reset configuration
        if (config.testRunner) {
            // Reset any modified properties
        }

        return result;
    }

    /**
     * Get performance test results
     */
    getPerformanceResults() {
        return {
            systemHealth: this.systemHealth,
            testResults: this.testResults,
            performanceMetrics: this.performanceMetrics,
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Generate performance test report
     */
    generatePerformanceReport() {
        const results = this.getPerformanceResults();

        return {
            title: 'Performance Test Report',
            generatedAt: results.timestamp,
            summary: {
                overallSuccess: results.testResults?.performance?.success || false,
                totalTests: results.testResults?.performance?.total || 0,
                passedTests: results.testResults?.performance?.passed || 0,
                systemHealth: results.systemHealth
            },
            metrics: results.performanceMetrics,
            details: results.testResults?.performance?.results || [],
            recommendations: this.generatePerformanceRecommendations(results)
        };
    }

    /**
     * Generate performance recommendations
     */
    generatePerformanceRecommendations(results) {
        const recommendations = [];

        if (results.performanceMetrics) {
            const metrics = results.performanceMetrics;

            if (metrics.initializationTime > 5000) {
                recommendations.push('Optimize application initialization time');
            }

            if (metrics.componentLoadTime > 3000) {
                recommendations.push('Improve component loading performance');
            }
        }

        if (results.testResults?.performance?.results) {
            const failedTests = results.testResults.performance.results.filter(r => !r.success);
            if (failedTests.length > 0) {
                recommendations.push(`Address ${failedTests.length} failed performance tests`);
            }
        }

        if (recommendations.length === 0) {
            recommendations.push('Performance is within acceptable thresholds');
        }

        return recommendations;
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            initialized: true,
            testRunnerAvailable: !!this.testRunner,
            systemHealthAvailable: !!this.systemHealth,
            testResultsAvailable: !!this.testResults,
            performanceMetricsAvailable: !!this.performanceMetrics,
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy PerformanceTests class for backward compatibility
 * @deprecated Use PerformanceTestOrchestrator instead
 */
export class PerformanceTests extends PerformanceTestOrchestrator {
    constructor(systemHealth, testResults, performanceMetrics) {
        super(systemHealth, testResults, performanceMetrics);
        console.warn('[DEPRECATED] PerformanceTests is deprecated. Use PerformanceTestOrchestrator instead.');
    }

    /**
     * Legacy method for backward compatibility
     */
    async testPerformanceOptimization() {
        return this.runAllPerformanceTests();
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create performance test orchestrator instance
 */
export function createPerformanceTestOrchestrator(systemHealth, testResults, performanceMetrics) {
    return new PerformanceTestOrchestrator(systemHealth, testResults, performanceMetrics);
}

/**
 * Create legacy performance tests (backward compatibility)
 */
export function createPerformanceTests(systemHealth, testResults, performanceMetrics) {
    return new PerformanceTests(systemHealth, testResults, performanceMetrics);
}

