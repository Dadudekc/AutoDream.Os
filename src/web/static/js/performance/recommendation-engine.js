/**
 * Recommendation Engine Module - V2 Compliant
 * Generates performance optimization recommendations
 * V2 COMPLIANCE: < 200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0
 * @license MIT
 */

export class RecommendationEngine {
    constructor() {
        this.recommendations = [];
        this.priorityLevels = {
            critical: [],
            high: [],
            medium: [],
            low: []
        };
    }

    /**
     * Generate performance recommendations
     */
    generateRecommendations(metrics) {
        this.analyzeBundleMetrics(metrics.bundle || {});
        this.analyzeDOMMetrics(metrics.dom || {});
        this.analyzeNetworkMetrics(metrics.network || {});
        this.analyzeMemoryMetrics(metrics.memory || {});

        return this.categorizeRecommendations();
    }

    /**
     * Analyze bundle-related metrics
     */
    analyzeBundleMetrics(bundle) {
        if (bundle.totalSize > 2000000) { // 2MB
            this.addRecommendation('critical',
                'Bundle size exceeds 2MB - implement code splitting',
                'Use dynamic imports to split large bundles into smaller chunks'
            );
        }

        if (bundle.moduleCount > 200) {
            this.addRecommendation('high',
                'High module count detected - optimize dependencies',
                'Remove unused dependencies and implement tree shaking'
            );
        }
    }

    /**
     * Analyze DOM-related metrics
     */
    analyzeDOMMetrics(dom) {
        if (dom.queryCount > 300) {
            this.addRecommendation('high',
                'Excessive DOM queries detected',
                'Cache DOM elements and use event delegation'
            );
        }

        if (dom.mutationCount > 500) {
            this.addRecommendation('medium',
                'Frequent DOM mutations may cause layout thrashing',
                'Batch DOM updates and use CSS transforms for animations'
            );
        }
    }

    /**
     * Analyze network-related metrics
     */
    analyzeNetworkMetrics(network) {
        if (network.requestCount > 50) {
            this.addRecommendation('medium',
                'High number of network requests',
                'Implement HTTP/2, use resource hints, and optimize asset loading'
            );
        }
    }

    /**
     * Analyze memory-related metrics
     */
    analyzeMemoryMetrics(memory) {
        if (memory.leakCount > 10) {
            this.addRecommendation('critical',
                'Memory leaks detected',
                'Remove unused event listeners and clear references'
            );
        }
    }

    /**
     * Add recommendation with priority
     */
    addRecommendation(priority, title, description) {
        const recommendation = {
            id: `rec_${this.recommendations.length + 1}`,
            priority,
            title,
            description,
            impact: this.calculateImpact(priority),
            effort: this.calculateEffort(priority),
            timestamp: new Date().toISOString()
        };

        this.recommendations.push(recommendation);
        this.priorityLevels[priority].push(recommendation);
    }

    /**
     * Calculate impact score
     */
    calculateImpact(priority) {
        const impacts = { critical: 9, high: 7, medium: 5, low: 3 };
        return impacts[priority] || 3;
    }

    /**
     * Calculate effort score
     */
    calculateEffort(priority) {
        const efforts = { critical: 8, high: 6, medium: 4, low: 2 };
        return efforts[priority] || 2;
    }

    /**
     * Categorize recommendations by priority
     */
    categorizeRecommendations() {
        return {
            all: this.recommendations,
            byPriority: this.priorityLevels,
            summary: {
                total: this.recommendations.length,
                critical: this.priorityLevels.critical.length,
                high: this.priorityLevels.high.length,
                medium: this.priorityLevels.medium.length,
                low: this.priorityLevels.low.length
            }
        };
    }

    /**
     * Get top recommendations
     */
    getTopRecommendations(limit = 5) {
        return this.recommendations
            .sort((a, b) => b.impact - a.impact)
            .slice(0, limit);
    }

    /**
     * Get quick wins (low effort, high impact)
     */
    getQuickWins() {
        return this.recommendations
            .filter(rec => rec.effort <= 3 && rec.impact >= 7)
            .sort((a, b) => b.impact - a.impact);
    }
}

export default RecommendationEngine;
