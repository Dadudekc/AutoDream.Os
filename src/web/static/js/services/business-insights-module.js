/**
 * Business Insights Module - V2 Compliant
 * Business insights generation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// BUSINESS INSIGHTS MODULE
// ================================

/**
 * Business insights generation functionality
 */
export class BusinessInsightsModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Generate business insights
     */
    generateBusinessInsights(metrics, trends) {
        const insights = [];

        try {
            // Success rate analysis
            if (metrics.successRate < 80) {
                insights.push({
                    type: 'warning',
                    message: 'Test success rate below acceptable threshold',
                    impact: 'high',
                    recommendation: 'Review and fix failing tests immediately'
                });
            }

            // Trend analysis
            if (trends && trends.direction === 'degrading') {
                insights.push({
                    type: 'critical',
                    message: 'Performance trending downward',
                    impact: 'high',
                    recommendation: 'Investigate root cause of performance degradation'
                });
            }

            // Duration analysis
            if (metrics.averageDuration > 1000) {
                insights.push({
                    type: 'warning',
                    message: 'Average test duration above recommended threshold',
                    impact: 'medium',
                    recommendation: 'Optimize test execution time'
                });
            }

            // Failure rate analysis
            if (metrics.totalFailed > metrics.totalTests * 0.2) {
                insights.push({
                    type: 'critical',
                    message: 'High failure rate detected',
                    impact: 'high',
                    recommendation: 'Address critical test failures immediately'
                });
            }

            // Performance insights
            if (metrics.successRate >= 95 && trends && trends.direction === 'improving') {
                insights.push({
                    type: 'success',
                    message: 'Excellent performance with improving trends',
                    impact: 'low',
                    recommendation: 'Maintain current testing practices'
                });
            }

            // Default insight if no specific issues
            if (insights.length === 0) {
                insights.push({
                    type: 'success',
                    message: 'All metrics within acceptable ranges',
                    impact: 'low',
                    recommendation: 'Continue monitoring performance'
                });
            }

        } catch (error) {
            this.logger.error('Business insights generation failed:', error);
            insights.push({
                type: 'error',
                message: 'Unable to generate business insights',
                impact: 'medium',
                recommendation: 'Review error logs for insight generation issues'
            });
        }

        return insights;
    }

    /**
     * Generate actionable insights
     */
    generateActionableInsights(metrics, trends) {
        const insights = this.generateBusinessInsights(metrics, trends);
        return insights.map(insight => ({
            ...insight,
            priority: this.calculatePriority(insight),
            timeline: this.estimateTimeline(insight),
            effort: this.estimateEffort(insight)
        }));
    }

    /**
     * Calculate priority score
     */
    calculatePriority(insight) {
        const impactScores = { low: 1, medium: 2, high: 3 };
        const typeScores = { success: 0, warning: 2, critical: 3, error: 3 };

        return impactScores[insight.impact] * typeScores[insight.type];
    }

    /**
     * Estimate timeline for insight
     */
    estimateTimeline(insight) {
        switch (insight.type) {
            case 'critical': return 'immediate';
            case 'warning': return 'short-term';
            case 'error': return 'immediate';
            default: return 'medium-term';
        }
    }

    /**
     * Estimate effort for insight
     */
    estimateEffort(insight) {
        if (insight.message.includes('review') || insight.message.includes('optimize')) {
            return 'medium';
        } else if (insight.message.includes('immediate') || insight.message.includes('critical')) {
            return 'high';
        } else {
            return 'low';
        }
    }

    /**
     * Generate insights summary
     */
    generateInsightsSummary(insights) {
        const summary = {
            total: insights.length,
            byType: {},
            byImpact: {},
            criticalCount: 0,
            warningCount: 0,
            successCount: 0
        };

        insights.forEach(insight => {
            // Count by type
            summary.byType[insight.type] = (summary.byType[insight.type] || 0) + 1;

            // Count by impact
            summary.byImpact[insight.impact] = (summary.byImpact[insight.impact] || 0) + 1;

            // Count critical insights
            if (insight.type === 'critical' || insight.type === 'error') {
                summary.criticalCount++;
            } else if (insight.type === 'warning') {
                summary.warningCount++;
            } else if (insight.type === 'success') {
                summary.successCount++;
            }
        });

        summary.overallStatus = this.determineOverallStatus(summary);
        return summary;
    }

    /**
     * Determine overall status from summary
     */
    determineOverallStatus(summary) {
        if (summary.criticalCount > 0) return 'critical';
        if (summary.warningCount > summary.successCount) return 'warning';
        if (summary.successCount > 0) return 'good';
        return 'neutral';
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create business insights module instance
 */
export function createBusinessInsightsModule() {
    return new BusinessInsightsModule();
}

