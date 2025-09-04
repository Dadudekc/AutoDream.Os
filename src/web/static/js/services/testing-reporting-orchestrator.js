/**
 * Testing Reporting Orchestrator - V2 Compliant
 * Main orchestrator for testing reporting service
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createReportGenerationModule } from './report-generation-module.js';
import { createBusinessInsightsModule } from './business-insights-module.js';
import { createTrendAnalysisModule } from './trend-analysis-module.js';
import { createMetricsAggregationModule } from './metrics-aggregation-module.js';
import { createReportHistoryModule } from './report-history-module.js';

// ================================
// TESTING REPORTING ORCHESTRATOR
// ================================

/**
 * Main orchestrator for testing reporting service
 */
export class TestingReportingOrchestrator {
    constructor() {
        this.logger = console;

        // Initialize modules
        this.reportGeneration = createReportGenerationModule();
        this.businessInsights = createBusinessInsightsModule();
        this.trendAnalysis = createTrendAnalysisModule();
        this.metricsAggregation = createMetricsAggregationModule();
        this.reportHistory = createReportHistoryModule();
    }

    /**
     * Generate performance report
     */
    generatePerformanceReport(results) {
        return this.reportGeneration.generatePerformanceReport(results);
    }

    /**
     * Generate business insights
     */
    generateBusinessInsights(metrics, trends) {
        return this.businessInsights.generateBusinessInsights(metrics, trends);
    }

    /**
     * Generate trend analysis
     */
    generateTrendAnalysis(results) {
        return this.trendAnalysis.generateTrendAnalysis(results);
    }

    /**
     * Calculate aggregate metrics
     */
    calculateAggregateMetrics(results) {
        return this.metricsAggregation.calculateAggregateMetrics(results);
    }

    /**
     * Generate summary report
     */
    generateSummaryReport(suiteName, timeRange = '24h') {
        try {
            const history = this.reportHistory.getReportHistory(suiteName, 20);
            const filteredResults = this.filterResultsByTimeRange(history, timeRange);
            const aggregated = this.calculateAggregateMetrics(filteredResults);
            const trends = this.generateTrendAnalysis(filteredResults);
            const insights = this.generateBusinessInsights(aggregated, trends);

            return this.reportGeneration.generateSummaryReport(
                suiteName, timeRange, filteredResults, aggregated, trends, insights
            );
        } catch (error) {
            this.logger.error(`Summary report generation failed for ${suiteName}:`, error);
            return {
                suiteName: suiteName,
                error: error.message,
                generatedAt: new Date().toISOString()
            };
        }
    }

    /**
     * Store report in history
     */
    storeReport(suiteName, report) {
        return this.reportHistory.storeReport(suiteName, report);
    }

    /**
     * Get report history
     */
    getReportHistory(suiteName, limit = 5) {
        return this.reportHistory.getReportHistory(suiteName, limit);
    }

    /**
     * Filter results by time range
     */
    filterResultsByTimeRange(results, timeRange) {
        const now = new Date();
        const timeLimit = this.parseTimeRange(timeRange);

        return results.filter(result => {
            const resultTime = new Date(result.timestamp || result.storedAt);
            return (now - resultTime) <= timeLimit;
        });
    }

    /**
     * Parse time range string
     */
    parseTimeRange(timeRange) {
        const timeMultipliers = {
            '1h': 60 * 60 * 1000,
            '6h': 6 * 60 * 60 * 1000,
            '12h': 12 * 60 * 60 * 1000,
            '24h': 24 * 60 * 60 * 1000,
            '7d': 7 * 24 * 60 * 60 * 1000,
            '30d': 30 * 24 * 60 * 60 * 1000
        };

        return timeMultipliers[timeRange] || timeMultipliers['24h'];
    }

    /**
     * Generate detailed test report
     */
    generateDetailedTestReport(results, options = {}) {
        return this.reportGeneration.generateDetailedTestReport(results, options);
    }

    /**
     * Generate actionable insights
     */
    generateActionableInsights(metrics, trends) {
        return this.businessInsights.generateActionableInsights(metrics, trends);
    }

    /**
     * Generate trend report
     */
    generateTrendReport(results, options = {}) {
        return this.trendAnalysis.generateTrendReport(results, options);
    }

    /**
     * Calculate detailed metrics
     */
    calculateDetailedMetrics(results) {
        return this.metricsAggregation.calculateDetailedMetrics(results);
    }

    /**
     * Get history statistics
     */
    getHistoryStatistics() {
        return this.reportHistory.getHistoryStatistics();
    }

    /**
     * Export history
     */
    exportHistory() {
        return this.reportHistory.exportHistory();
    }

    /**
     * Import history
     */
    importHistory(jsonData) {
        return this.reportHistory.importHistory(jsonData);
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: ['reportGeneration', 'businessInsights', 'trendAnalysis', 'metricsAggregation', 'reportHistory'],
            historyStatistics: this.getHistoryStatistics(),
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy TestingReportingService class for backward compatibility
 * @deprecated Use TestingReportingOrchestrator instead
 */
export class TestingReportingService extends TestingReportingOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] TestingReportingService is deprecated. Use TestingReportingOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create testing reporting orchestrator instance
 */
export function createTestingReportingOrchestrator() {
    return new TestingReportingOrchestrator();
}

/**
 * Create legacy testing reporting service (backward compatibility)
 */
export function createTestingReportingService() {
    return new TestingReportingService();
}

