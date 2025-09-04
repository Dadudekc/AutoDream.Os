/**
 * Testing Performance Orchestrator - V2 Compliant
 * Main orchestrator for performance testing service
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createPerformanceTestExecutionModule } from './performance-test-execution-module.js';
import { createPerformanceAnalysisModule } from './performance-analysis-module.js';
import { createPerformanceRecommendationModule } from './performance-recommendation-module.js';
import { createPerformanceConfigurationModule } from './performance-configuration-module.js';

// ================================
// TESTING PERFORMANCE ORCHESTRATOR
// ================================

/**
 * Main orchestrator for performance testing service
 */
export class TestingPerformanceOrchestrator {
    constructor() {
        this.logger = console;

        // Initialize modules
        this.execution = createPerformanceTestExecutionModule();
        this.analysis = createPerformanceAnalysisModule();
        this.recommendations = createPerformanceRecommendationModule();
        this.configuration = createPerformanceConfigurationModule();
    }

    /**
     * Run performance test
     */
    async runPerformanceTest(componentName, testScenario) {
        try {
            if (!this.execution.validateTestScenario(testScenario)) {
                throw new Error('Invalid performance test scenario');
            }

            console.log(`Running performance test for ${componentName}...`);

            // Execute performance test
            const testResults = await this.execution.executePerformanceTest(componentName, testScenario);

            // Analyze results against baseline
            const baselineMetrics = this.configuration.getBaselineMetrics(componentName);
            const analysis = this.analysis.analyzePerformanceResults(testResults, baselineMetrics);

            // Generate recommendations
            const recommendations = this.recommendations.generatePerformanceRecommendations(analysis);

            // Update baseline if results are good
            if (analysis.performance === 'good' && testResults.performanceScore > 80) {
                this.configuration.updateBaselineMetrics(componentName, testResults);
            }

            return {
                componentName: componentName,
                scenario: testScenario,
                results: testResults,
                analysis: analysis,
                recommendations: recommendations,
                timestamp: new Date().toISOString()
            };

        } catch (error) {
            this.logger.error(`Performance test failed for ${componentName}:`, error);
            return {
                componentName: componentName,
                success: false,
                error: error.message,
                timestamp: new Date().toISOString()
            };
        }
    }

    /**
     * Execute performance test (direct)
     */
    async executePerformanceTest(componentName, scenario) {
        return this.execution.executePerformanceTest(componentName, scenario);
    }

    /**
     * Analyze performance results
     */
    analyzePerformanceResults(testResults, baselineMetrics) {
        return this.analysis.analyzePerformanceResults(testResults, baselineMetrics);
    }

    /**
     * Generate performance recommendations
     */
    generatePerformanceRecommendations(analysis) {
        return this.recommendations.generatePerformanceRecommendations(analysis);
    }

    /**
     * Set performance threshold
     */
    setPerformanceThreshold(componentName, threshold) {
        return this.configuration.setPerformanceThreshold(componentName, threshold);
    }

    /**
     * Get performance threshold
     */
    getPerformanceThreshold(componentName) {
        return this.configuration.getPerformanceThreshold(componentName);
    }

    /**
     * Set baseline metrics
     */
    setBaselineMetrics(componentName, metrics) {
        return this.configuration.setBaselineMetrics(componentName, metrics);
    }

    /**
     * Get baseline metrics
     */
    getBaselineMetrics(componentName) {
        return this.configuration.getBaselineMetrics(componentName);
    }

    /**
     * Get performance configuration summary
     */
    getConfigurationSummary() {
        return this.configuration.getConfigurationSummary();
    }

    /**
     * Export configuration
     */
    exportConfiguration() {
        return this.configuration.exportConfiguration();
    }

    /**
     * Import configuration
     */
    importConfiguration(config) {
        return this.configuration.importConfiguration(config);
    }

    /**
     * Generate actionable recommendations
     */
    generateActionableRecommendations(analysis) {
        return this.recommendations.generateActionableRecommendations(analysis);
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: ['execution', 'analysis', 'recommendations', 'configuration'],
            configurationSummary: this.getConfigurationSummary(),
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy TestingPerformanceService class for backward compatibility
 * @deprecated Use TestingPerformanceOrchestrator instead
 */
export class TestingPerformanceService extends TestingPerformanceOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] TestingPerformanceService is deprecated. Use TestingPerformanceOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create testing performance orchestrator instance
 */
export function createTestingPerformanceOrchestrator() {
    return new TestingPerformanceOrchestrator();
}

/**
 * Create legacy testing performance service (backward compatibility)
 */
export function createTestingPerformanceService() {
    return new TestingPerformanceService();
}

