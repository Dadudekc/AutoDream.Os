/**
 * Metrics Aggregation Module - V2 Compliant
 * Metrics calculation and aggregation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// METRICS AGGREGATION MODULE
// ================================

/**
 * Metrics calculation and aggregation functionality
 */
export class MetricsAggregationModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Calculate aggregate metrics
     */
    calculateAggregateMetrics(results) {
        if (results.length === 0) {
            return {
                totalTests: 0,
                totalPassed: 0,
                totalFailed: 0,
                totalSkipped: 0,
                successRate: 0,
                averageDuration: 0
            };
        }

        try {
            const aggregated = results.reduce((acc, result) => {
                acc.totalTests += result.totalTests || 0;
                acc.totalPassed += result.passed || 0;
                acc.totalFailed += result.failed || 0;
                acc.totalSkipped += result.skipped || 0;
                acc.totalDuration += result.duration || 0;
                return acc;
            }, {
                totalTests: 0,
                totalPassed: 0,
                totalFailed: 0,
                totalSkipped: 0,
                totalDuration: 0
            });

            aggregated.successRate = aggregated.totalTests > 0 ?
                (aggregated.totalPassed / aggregated.totalTests) * 100 : 0;
            aggregated.averageDuration = results.length > 0 ?
                aggregated.totalDuration / results.length : 0;

            return aggregated;
        } catch (error) {
            this.logger.error('Metrics aggregation failed:', error);
            return {
                totalTests: 0,
                totalPassed: 0,
                totalFailed: 0,
                totalSkipped: 0,
                successRate: 0,
                averageDuration: 0,
                error: error.message
            };
        }
    }

    /**
     * Calculate detailed metrics
     */
    calculateDetailedMetrics(results) {
        const basic = this.calculateAggregateMetrics(results);

        try {
            const detailed = {
                ...basic,
                standardDeviation: this.calculateStandardDeviation(results, 'duration'),
                percentiles: this.calculatePercentiles(results, 'duration'),
                failureRate: basic.totalTests > 0 ? (basic.totalFailed / basic.totalTests) * 100 : 0,
                skipRate: basic.totalTests > 0 ? (basic.totalSkipped / basic.totalTests) * 100 : 0,
                testEfficiency: this.calculateTestEfficiency(results),
                reliabilityScore: this.calculateReliabilityScore(basic)
            };

            return detailed;
        } catch (error) {
            this.logger.error('Detailed metrics calculation failed:', error);
            return basic;
        }
    }

    /**
     * Calculate standard deviation
     */
    calculateStandardDeviation(results, field) {
        if (results.length < 2) return 0;

        const values = results.map(r => r[field] || 0);
        const mean = values.reduce((sum, value) => sum + value, 0) / values.length;

        const squaredDifferences = values.map(value => Math.pow(value - mean, 2));
        const variance = squaredDifferences.reduce((sum, diff) => sum + diff, 0) / values.length;

        return Math.sqrt(variance);
    }

    /**
     * Calculate percentiles
     */
    calculatePercentiles(results, field, percentiles = [25, 50, 75, 95]) {
        if (results.length === 0) return {};

        const values = results.map(r => r[field] || 0).sort((a, b) => a - b);
        const result = {};

        percentiles.forEach(percentile => {
            const index = Math.ceil((percentile / 100) * values.length) - 1;
            result[`p${percentile}`] = values[Math.max(0, Math.min(index, values.length - 1))];
        });

        return result;
    }

    /**
     * Calculate test efficiency
     */
    calculateTestEfficiency(results) {
        if (results.length === 0) return 0;

        const totalDuration = results.reduce((sum, r) => sum + (r.duration || 0), 0);
        const totalTests = results.reduce((sum, r) => sum + (r.totalTests || 0), 0);

        if (totalDuration === 0 || totalTests === 0) return 0;

        // Efficiency = tests per second
        return totalTests / (totalDuration / 1000);
    }

    /**
     * Calculate reliability score
     */
    calculateReliabilityScore(metrics) {
        let score = 100;

        // Deduct points for failures
        score -= (metrics.totalFailed / Math.max(metrics.totalTests, 1)) * 50;

        // Deduct points for skips (less severe)
        score -= (metrics.totalSkipped / Math.max(metrics.totalTests, 1)) * 20;

        // Bonus for high success rate
        if (metrics.successRate > 95) score += 10;
        else if (metrics.successRate > 90) score += 5;

        return Math.max(0, Math.min(100, score));
    }

    /**
     * Aggregate metrics by category
     */
    aggregateMetricsByCategory(results, categoryField) {
        const categories = {};

        results.forEach(result => {
            const category = result[categoryField] || 'uncategorized';

            if (!categories[category]) {
                categories[category] = [];
            }

            categories[category].push(result);
        });

        const aggregated = {};
        Object.entries(categories).forEach(([category, categoryResults]) => {
            aggregated[category] = this.calculateAggregateMetrics(categoryResults);
        });

        return aggregated;
    }

    /**
     * Calculate metrics comparison
     */
    calculateMetricsComparison(current, baseline) {
        if (!baseline) return { comparison: 'no_baseline' };

        const comparison = {
            successRateChange: current.successRate - baseline.successRate,
            durationChange: current.averageDuration - baseline.averageDuration,
            testsChange: current.totalTests - baseline.totalTests,
            trend: this.determineComparisonTrend(current, baseline)
        };

        return comparison;
    }

    /**
     * Determine comparison trend
     */
    determineComparisonTrend(current, baseline) {
        let improving = 0;
        let degrading = 0;

        if (current.successRate > baseline.successRate) improving++;
        else if (current.successRate < baseline.successRate) degrading++;

        if (current.averageDuration < baseline.averageDuration) improving++;
        else if (current.averageDuration > baseline.averageDuration) degrading++;

        if (improving > degrading) return 'improving';
        if (degrading > improving) return 'degrading';
        return 'stable';
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create metrics aggregation module instance
 */
export function createMetricsAggregationModule() {
    return new MetricsAggregationModule();
}
