/**
 * Trend Analysis Module - V2 Compliant
 * Trend analysis functionality for test results
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// TREND ANALYSIS MODULE
// ================================

/**
 * Trend analysis functionality for test results
 */
export class TrendAnalysisModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Generate trend analysis
     */
    generateTrendAnalysis(results) {
        if (results.length < 2) {
            return {
                direction: 'stable',
                confidence: 0,
                message: 'Insufficient data for trend analysis'
            };
        }

        try {
            const recentResults = results.slice(-5);
            const olderResults = results.slice(-10, -5);

            if (olderResults.length === 0) {
                return {
                    direction: 'stable',
                    confidence: 0,
                    message: 'Need more historical data'
                };
            }

            const recentAvg = recentResults.reduce((sum, r) => sum + r.successRate, 0) / recentResults.length;
            const olderAvg = olderResults.reduce((sum, r) => sum + r.successRate, 0) / olderResults.length;

            let direction = 'stable';
            let confidence = 0;

            if (recentAvg < olderAvg * 0.9) {
                direction = 'degrading';
                confidence = Math.min(100, (olderAvg - recentAvg) / olderAvg * 100);
            } else if (recentAvg > olderAvg * 1.1) {
                direction = 'improving';
                confidence = Math.min(100, (recentAvg - olderAvg) / olderAvg * 100);
            }

            return {
                direction: direction,
                confidence: Math.round(confidence),
                recentAverage: Math.round(recentAvg * 100) / 100,
                olderAverage: Math.round(olderAvg * 100) / 100,
                message: `Performance is ${direction} with ${Math.round(confidence)}% confidence`
            };
        } catch (error) {
            this.logger.error('Trend analysis failed:', error);
            return {
                direction: 'error',
                confidence: 0,
                message: 'Trend analysis failed due to error'
            };
        }
    }

    /**
     * Analyze performance trends
     */
    analyzePerformanceTrends(results, metric = 'successRate') {
        if (!results || results.length < 3) {
            return { trend: 'insufficient_data', periods: [] };
        }

        const periods = this.divideIntoPeriods(results, 3);

        return {
            trend: this.calculateOverallTrend(periods, metric),
            periods: periods.map(period => ({
                period: period.label,
                average: this.calculatePeriodAverage(period.results, metric),
                count: period.results.length
            })),
            confidence: this.calculateTrendConfidence(periods, metric)
        };
    }

    /**
     * Divide results into periods
     */
    divideIntoPeriods(results, numPeriods) {
        const periodSize = Math.ceil(results.length / numPeriods);
        const periods = [];

        for (let i = 0; i < numPeriods; i++) {
            const start = i * periodSize;
            const end = Math.min((i + 1) * periodSize, results.length);
            const periodResults = results.slice(start, end);

            periods.push({
                label: `Period ${i + 1}`,
                results: periodResults,
                start: start,
                end: end - 1
            });
        }

        return periods;
    }

    /**
     * Calculate period average
     */
    calculatePeriodAverage(results, metric) {
        if (!results || results.length === 0) return 0;

        const sum = results.reduce((acc, result) => {
            return acc + (result[metric] || 0);
        }, 0);

        return sum / results.length;
    }

    /**
     * Calculate overall trend
     */
    calculateOverallTrend(periods, metric) {
        if (periods.length < 2) return 'stable';

        const firstPeriod = this.calculatePeriodAverage(periods[0].results, metric);
        const lastPeriod = this.calculatePeriodAverage(periods[periods.length - 1].results, metric);

        const change = lastPeriod - firstPeriod;
        const threshold = firstPeriod * 0.05; // 5% change threshold

        if (Math.abs(change) < threshold) return 'stable';
        return change > 0 ? 'improving' : 'degrading';
    }

    /**
     * Calculate trend confidence
     */
    calculateTrendConfidence(periods, metric) {
        if (periods.length < 2) return 0;

        const values = periods.map(period => this.calculatePeriodAverage(period.results, metric));
        const changes = [];

        for (let i = 1; i < values.length; i++) {
            changes.push(values[i] - values[i - 1]);
        }

        const avgChange = changes.reduce((sum, change) => sum + change, 0) / changes.length;
        const variance = changes.reduce((sum, change) => sum + Math.pow(change - avgChange, 2), 0) / changes.length;

        // Lower variance = higher confidence
        const confidence = Math.max(0, Math.min(100, 100 - (variance * 100)));

        return Math.round(confidence);
    }

    /**
     * Generate trend report
     */
    generateTrendReport(results, options = {}) {
        const trends = this.generateTrendAnalysis(results);
        const performanceTrends = this.analyzePerformanceTrends(results, options.metric || 'successRate');

        return {
            generatedAt: new Date().toISOString(),
            dataPoints: results.length,
            primaryTrend: trends,
            performanceTrends: performanceTrends,
            recommendations: this.generateTrendRecommendations(trends, performanceTrends),
            summary: this.summarizeTrends(trends, performanceTrends)
        };
    }

    /**
     * Generate trend recommendations
     */
    generateTrendRecommendations(primaryTrend, performanceTrends) {
        const recommendations = [];

        if (primaryTrend.direction === 'degrading') {
            recommendations.push('Investigate root cause of performance degradation');
            recommendations.push('Review recent changes and deployments');
        }

        if (performanceTrends.trend === 'improving') {
            recommendations.push('Continue current optimization practices');
        }

        if (primaryTrend.confidence < 50) {
            recommendations.push('Collect more data for reliable trend analysis');
        }

        return recommendations;
    }

    /**
     * Summarize trends
     */
    summarizeTrends(primaryTrend, performanceTrends) {
        return {
            overallDirection: primaryTrend.direction,
            confidence: primaryTrend.confidence,
            performanceDirection: performanceTrends.trend,
            keyInsight: this.generateKeyInsight(primaryTrend, performanceTrends),
            actionable: this.isTrendActionable(primaryTrend, performanceTrends)
        };
    }

    /**
     * Generate key insight
     */
    generateKeyInsight(primaryTrend, performanceTrends) {
        if (primaryTrend.direction === 'degrading' && primaryTrend.confidence > 70) {
            return 'Significant performance degradation detected - immediate action recommended';
        } else if (primaryTrend.direction === 'improving' && primaryTrend.confidence > 70) {
            return 'Strong positive performance trend - continue optimization efforts';
        } else {
            return 'Performance trends are stable or require more data for clear analysis';
        }
    }

    /**
     * Check if trend is actionable
     */
    isTrendActionable(primaryTrend, performanceTrends) {
        return primaryTrend.confidence > 60 || Math.abs(performanceTrends.confidence - 50) > 20;
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create trend analysis module instance
 */
export function createTrendAnalysisModule() {
    return new TrendAnalysisModule();
}
