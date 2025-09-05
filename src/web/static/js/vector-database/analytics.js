/**
 * Vector Database Analytics - V2 Compliant Module
 * ==============================================
 * 
 * Analytics and metrics collection for vector database operations.
 * Handles performance monitoring, usage statistics, and reporting.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class VectorDatabaseAnalytics {
    constructor() {
        this.metrics = {
            totalDocuments: 0,
            searchQueries: 0,
            averageResponseTime: 0,
            topSearches: [],
            performanceHistory: [],
            errorCount: 0,
            lastUpdate: Date.now()
        };
        this.logger = console;
    }

    /**
     * Initialize analytics
     */
    initialize() {
        this.startPerformanceMonitoring();
        this.logger.log('✅ Vector Database Analytics initialized');
    }

    /**
     * Record search query
     */
    recordSearchQuery(query, resultCount, responseTime) {
        this.metrics.searchQueries++;
        
        // Update average response time
        this.updateAverageResponseTime(responseTime);
        
        // Update top searches
        this.updateTopSearches(query, resultCount);
        
        // Record performance
        this.recordPerformance('search', responseTime);
        
        this.logger.log(`📊 Search recorded: "${query}" (${resultCount} results, ${responseTime}ms)`);
    }

    /**
     * Record document operation
     */
    recordDocumentOperation(operation, documentId, success = true) {
        if (operation === 'add') {
            this.metrics.totalDocuments++;
        } else if (operation === 'delete') {
            this.metrics.totalDocuments = Math.max(0, this.metrics.totalDocuments - 1);
        }
        
        if (!success) {
            this.metrics.errorCount++;
        }
        
        this.logger.log(`📊 Document ${operation} recorded: ${documentId} (${success ? 'success' : 'error'})`);
    }

    /**
     * Record error
     */
    recordError(error, context = '') {
        this.metrics.errorCount++;
        
        const errorEntry = {
            error: error.message || error,
            context,
            timestamp: Date.now()
        };
        
        this.logger.error(`📊 Error recorded: ${errorEntry.error} (${context})`);
    }

    /**
     * Update average response time
     */
    updateAverageResponseTime(responseTime) {
        const currentAvg = this.metrics.averageResponseTime;
        const queryCount = this.metrics.searchQueries;
        
        if (queryCount === 1) {
            this.metrics.averageResponseTime = responseTime;
        } else {
            // Calculate exponential moving average
            const alpha = 0.1;
            this.metrics.averageResponseTime = alpha * responseTime + (1 - alpha) * currentAvg;
        }
    }

    /**
     * Update top searches
     */
    updateTopSearches(query, resultCount) {
        const existingIndex = this.metrics.topSearches.findIndex(item => item.query === query);
        
        if (existingIndex >= 0) {
            this.metrics.topSearches[existingIndex].count++;
            this.metrics.topSearches[existingIndex].lastUsed = Date.now();
        } else {
            this.metrics.topSearches.push({
                query,
                count: 1,
                resultCount,
                lastUsed: Date.now()
            });
        }
        
        // Sort by count and keep top 10
        this.metrics.topSearches.sort((a, b) => b.count - a.count);
        this.metrics.topSearches = this.metrics.topSearches.slice(0, 10);
    }

    /**
     * Record performance metric
     */
    recordPerformance(operation, responseTime) {
        const performanceEntry = {
            operation,
            responseTime,
            timestamp: Date.now()
        };
        
        this.metrics.performanceHistory.push(performanceEntry);
        
        // Keep only last 100 performance entries
        if (this.metrics.performanceHistory.length > 100) {
            this.metrics.performanceHistory = this.metrics.performanceHistory.slice(-100);
        }
    }

    /**
     * Start performance monitoring
     */
    startPerformanceMonitoring() {
        // Monitor page load performance
        if (window.performance) {
            window.addEventListener('load', () => {
                const loadTime = window.performance.timing.loadEventEnd - window.performance.timing.navigationStart;
                this.recordPerformance('page_load', loadTime);
            });
        }
        
        // Monitor memory usage
        if (window.performance && window.performance.memory) {
            setInterval(() => {
                const memoryUsage = window.performance.memory.usedJSHeapSize;
                this.recordPerformance('memory_usage', memoryUsage);
            }, 30000); // Every 30 seconds
        }
    }

    /**
     * Get analytics metrics
     */
    getMetrics() {
        return {
            ...this.metrics,
            lastUpdate: Date.now()
        };
    }

    /**
     * Get performance summary
     */
    getPerformanceSummary() {
        const recentPerformance = this.metrics.performanceHistory.slice(-20);
        
        if (recentPerformance.length === 0) {
            return {
                averageResponseTime: 0,
                minResponseTime: 0,
                maxResponseTime: 0,
                totalOperations: 0
            };
        }
        
        const responseTimes = recentPerformance.map(entry => entry.responseTime);
        
        return {
            averageResponseTime: responseTimes.reduce((sum, time) => sum + time, 0) / responseTimes.length,
            minResponseTime: Math.min(...responseTimes),
            maxResponseTime: Math.max(...responseTimes),
            totalOperations: recentPerformance.length
        };
    }

    /**
     * Get usage statistics
     */
    getUsageStats() {
        return {
            totalDocuments: this.metrics.totalDocuments,
            searchQueries: this.metrics.searchQueries,
            errorCount: this.metrics.errorCount,
            successRate: this.metrics.searchQueries > 0 
                ? ((this.metrics.searchQueries - this.metrics.errorCount) / this.metrics.searchQueries) * 100 
                : 100,
            topSearches: this.metrics.topSearches.slice(0, 5)
        };
    }

    /**
     * Get error analysis
     */
    getErrorAnalysis() {
        const recentErrors = this.metrics.performanceHistory
            .filter(entry => entry.operation === 'error')
            .slice(-10);
        
        return {
            totalErrors: this.metrics.errorCount,
            recentErrors: recentErrors,
            errorRate: this.metrics.searchQueries > 0 
                ? (this.metrics.errorCount / this.metrics.searchQueries) * 100 
                : 0
        };
    }

    /**
     * Export analytics data
     */
    exportAnalytics() {
        return {
            metrics: this.getMetrics(),
            performance: this.getPerformanceSummary(),
            usage: this.getUsageStats(),
            errors: this.getErrorAnalysis(),
            exportedAt: new Date().toISOString()
        };
    }

    /**
     * Reset analytics
     */
    resetAnalytics() {
        this.metrics = {
            totalDocuments: 0,
            searchQueries: 0,
            averageResponseTime: 0,
            topSearches: [],
            performanceHistory: [],
            errorCount: 0,
            lastUpdate: Date.now()
        };
        
        this.logger.log('📊 Analytics reset');
    }

    /**
     * Generate analytics report
     */
    generateReport() {
        const report = {
            summary: {
                totalDocuments: this.metrics.totalDocuments,
                totalSearches: this.metrics.searchQueries,
                averageResponseTime: Math.round(this.metrics.averageResponseTime),
                errorRate: this.metrics.searchQueries > 0 
                    ? Math.round((this.metrics.errorCount / this.metrics.searchQueries) * 100) 
                    : 0
            },
            topSearches: this.metrics.topSearches.slice(0, 5),
            performance: this.getPerformanceSummary(),
            recommendations: this.generateRecommendations()
        };
        
        return report;
    }

    /**
     * Generate recommendations based on analytics
     */
    generateRecommendations() {
        const recommendations = [];
        
        if (this.metrics.averageResponseTime > 1000) {
            recommendations.push('Consider optimizing search algorithms - average response time is high');
        }
        
        if (this.metrics.errorCount > this.metrics.searchQueries * 0.1) {
            recommendations.push('Error rate is high - investigate and fix common issues');
        }
        
        if (this.metrics.topSearches.length > 0) {
            const mostPopular = this.metrics.topSearches[0];
            if (mostPopular.count > 10) {
                recommendations.push(`Consider creating a quick access feature for "${mostPopular.query}"`);
            }
        }
        
        return recommendations;
    }
}
