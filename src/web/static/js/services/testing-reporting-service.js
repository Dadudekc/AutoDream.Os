/**
 * Testing Reporting Service - V2 Compliant
 * Report generation functionality extracted from testing-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// TESTING REPORTING SERVICE
// ================================

/**
 * Report generation functionality for testing
 */
class TestingReportingService {
    constructor() {
        this.reportHistory = new Map();
    }

    /**
     * Generate performance report
     */
    generatePerformanceReport(results) {
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                totalTests: results.totalTests,
                passed: results.passed,
                failed: results.failed,
                skipped: results.skipped,
                duration: results.duration,
                successRate: results.totalTests > 0 ? (results.passed / results.totalTests) * 100 : 0
            },
            status: 'unknown',
            recommendations: []
        };

        // Determine status based on success rate
        if (report.summary.successRate >= 95) {
            report.status = 'excellent';
            report.recommendations.push('Performance is excellent - maintain current standards');
        } else if (report.summary.successRate >= 80) {
            report.status = 'good';
            report.recommendations.push('Performance is good - minor optimizations possible');
        } else if (report.summary.successRate >= 60) {
            report.status = 'needs_improvement';
            report.recommendations.push('Performance needs improvement - review failing tests');
        } else {
            report.status = 'critical';
            report.recommendations.push('Critical performance issues - immediate attention required');
        }

        // Duration analysis
        if (report.summary.duration > 5000) {
            report.recommendations.push('Test execution time is high - consider parallelization');
        }

        // Failure analysis
        if (report.summary.failed > 0) {
            report.recommendations.push(`${report.summary.failed} tests failed - review error logs`);
        }

        return report;
    }

    /**
     * Generate business insights
     */
    generateBusinessInsights(metrics, trends) {
        const insights = [];

        if (metrics.successRate < 80) {
            insights.push({
                type: 'warning',
                message: 'Test success rate below acceptable threshold',
                impact: 'high',
                recommendation: 'Review and fix failing tests immediately'
            });
        }

        if (trends.direction === 'degrading') {
            insights.push({
                type: 'critical',
                message: 'Performance trending downward',
                impact: 'high',
                recommendation: 'Investigate root cause of performance degradation'
            });
        }

        if (metrics.averageDuration > 1000) {
            insights.push({
                type: 'warning',
                message: 'Average test duration above recommended threshold',
                impact: 'medium',
                recommendation: 'Optimize test execution time'
            });
        }

        if (insights.length === 0) {
            insights.push({
                type: 'success',
                message: 'All metrics within acceptable ranges',
                impact: 'low',
                recommendation: 'Continue monitoring performance'
            });
        }

        return insights;
    }

    /**
     * Store report in history
     */
    storeReport(suiteName, report) {
        if (!this.reportHistory.has(suiteName)) {
            this.reportHistory.set(suiteName, []);
        }

        const history = this.reportHistory.get(suiteName);
        history.push({
            ...report,
            storedAt: new Date().toISOString()
        });

        // Keep only last 10 reports
        if (history.length > 10) {
            history.shift();
        }
    }

    /**
     * Get report history
     */
    getReportHistory(suiteName, limit = 5) {
        const history = this.reportHistory.get(suiteName) || [];
        return history.slice(-limit);
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
    }

    /**
     * Filter results by time range
     */
    filterResultsByTimeRange(results, timeRange) {
        const now = new Date();
        const timeLimit = this.parseTimeRange(timeRange);

        return results.filter(result => {
            const resultTime = new Date(result.timestamp);
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
     * Generate summary report
     */
    generateSummaryReport(suiteName, timeRange = '24h') {
        const history = this.getReportHistory(suiteName, 20);
        const filteredResults = this.filterResultsByTimeRange(history, timeRange);
        const aggregated = this.calculateAggregateMetrics(filteredResults);
        const trends = this.generateTrendAnalysis(filteredResults);
        const insights = this.generateBusinessInsights(aggregated, trends);

        return {
            suiteName: suiteName,
            timeRange: timeRange,
            generatedAt: new Date().toISOString(),
            summary: aggregated,
            trends: trends,
            insights: insights,
            dataPoints: filteredResults.length
        };
    }
}

// ================================
// GLOBAL REPORTING SERVICE INSTANCE
// ================================

/**
 * Global testing reporting service instance
 */
const testingReportingService = new TestingReportingService();

// ================================
// REPORTING SERVICE API FUNCTIONS
// ================================

/**
 * Generate performance report
 */
export function generatePerformanceReport(results) {
    return testingReportingService.generatePerformanceReport(results);
}

/**
 * Generate business insights
 */
export function generateBusinessInsights(metrics, trends) {
    return testingReportingService.generateBusinessInsights(metrics, trends);
}

/**
 * Generate trend analysis
 */
export function generateTrendAnalysis(results) {
    return testingReportingService.generateTrendAnalysis(results);
}

/**
 * Calculate aggregate metrics
 */
export function calculateAggregateMetrics(results) {
    return testingReportingService.calculateAggregateMetrics(results);
}

/**
 * Generate summary report
 */
export function generateSummaryReport(suiteName, timeRange = '24h') {
    return testingReportingService.generateSummaryReport(suiteName, timeRange);
}

// ================================
// EXPORTS
// ================================

export { TestingReportingService, testingReportingService };
export default testingReportingService;
