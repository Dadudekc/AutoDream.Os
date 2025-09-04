/**
 * Testing Report Generator - V2 Compliant
 * Core report generation functionality
 * V2 COMPLIANCE: Under 300-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

export class TestingReportGenerator {
    constructor() {
        this.reportHistory = new Map();
    }

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
            status: this._determineStatus(results),
            recommendations: this._generateRecommendations(results)
        };

        return report;
    }

    generateCompatibilityReport(results) {
        return {
            timestamp: new Date().toISOString(),
            compatibility: {
                browserSupport: results.browserSupport || [],
                apiCompatibility: results.apiCompatibility || false,
                legacySupport: results.legacySupport || false
            },
            issues: results.compatibilityIssues || [],
            recommendations: this._generateCompatibilityRecommendations(results)
        };
    }

    generateSummaryReport(results) {
        return {
            timestamp: new Date().toISOString(),
            overview: {
                totalTests: results.totalTests,
                passed: results.passed,
                failed: results.failed,
                duration: results.duration,
                successRate: results.successRate
            },
            trends: this._calculateTrends(results),
            insights: this._generateInsights(results)
        };
    }

    _determineStatus(results) {
        const successRate = results.totalTests > 0 ? (results.passed / results.totalTests) * 100 : 0;

        if (successRate >= 95) return 'excellent';
        if (successRate >= 80) return 'good';
        if (successRate >= 60) return 'needs_improvement';
        return 'critical';
    }

    _generateRecommendations(results) {
        const recommendations = [];
        const successRate = results.totalTests > 0 ? (results.passed / results.totalTests) * 100 : 0;

        if (successRate >= 95) {
            recommendations.push('Performance is excellent - maintain current standards');
        } else if (successRate >= 80) {
            recommendations.push('Performance is good - minor optimizations possible');
        } else if (successRate >= 60) {
            recommendations.push('Performance needs improvement - review failing tests');
        } else {
            recommendations.push('Critical performance issues - immediate action required');
            recommendations.push('Review test failures and fix critical issues');
            recommendations.push('Consider architecture improvements');
        }

        return recommendations;
    }

    _generateCompatibilityRecommendations(results) {
        const recommendations = [];

        if (!results.apiCompatibility) {
            recommendations.push('Address API compatibility issues');
        }

        if (!results.legacySupport) {
            recommendations.push('Improve legacy browser support');
        }

        if (results.compatibilityIssues?.length > 0) {
            recommendations.push('Resolve compatibility issues identified');
        }

        return recommendations;
    }

    _calculateTrends(results) {
        // Calculate performance trends
        return {
            improvement: results.previousResults ?
                ((results.successRate - results.previousResults.successRate) > 0 ? 'improving' : 'declining') : 'stable',
            consistency: this._calculateConsistency(results)
        };
    }

    _calculateConsistency(results) {
        // Calculate result consistency over time
        return results.successRate > 80 ? 'high' : 'variable';
    }

    _generateInsights(results) {
        const insights = [];

        if (results.failed > results.passed) {
            insights.push('More tests are failing than passing - focus on stability');
        }

        if (results.duration > 30000) { // 30 seconds
            insights.push('Test execution is slow - consider optimization');
        }

        return insights;
    }

    storeReport(reportId, report) {
        this.reportHistory.set(reportId, {
            ...report,
            storedAt: new Date().toISOString()
        });
    }

    getReport(reportId) {
        return this.reportHistory.get(reportId);
    }

    getReportHistory(limit = 10) {
        return Array.from(this.reportHistory.values())
            .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
            .slice(0, limit);
    }
}

export function createTestingReportGenerator() {
    return new TestingReportGenerator();
}
