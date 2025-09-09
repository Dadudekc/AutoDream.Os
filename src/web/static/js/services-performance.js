/**
 * Performance Service Module - V2 Compliant
 * Handles performance monitoring and metrics collection
 * V2 COMPLIANCE: <200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR COMPONENT
 * @license MIT
 */

class PerformanceService {
    constructor(config = {}) {
        this.config = { enableMonitoring: true, metricsInterval: 5000, maxMetrics: 100, ...config };
        this.metrics = [];
        this.isMonitoring = false;
        this.monitorInterval = null;
        this.eventListeners = new Map();
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;
        console.log('📊 Initializing Performance Service...');
        this.isInitialized = true;
    }

    startMonitoring() {
        if (this.isMonitoring) return;
        this.isMonitoring = true;
        this.monitorInterval = setInterval(() => this.collectMetrics(), this.config.metricsInterval);
        console.log('📊 Performance monitoring started');
    }

    stopMonitoring() {
        if (!this.isMonitoring) return;
        this.isMonitoring = false;
        if (this.monitorInterval) clearInterval(this.monitorInterval);
        console.log('📊 Performance monitoring stopped');
    }

    collectMetrics() {
        try {
            const metrics = {
                timestamp: Date.now(),
                memory: this.getMemoryUsage(),
                timing: this.getTimingMetrics(),
                network: this.getNetworkMetrics()
            };

            this.metrics.push(metrics);
            if (this.metrics.length > this.config.maxMetrics) {
                this.metrics.shift();
            }

            this.emit('metricsCollected', metrics);
        } catch (error) {
            console.error('❌ Error collecting metrics:', error);
        }
    }

    getMemoryUsage() {
        if (typeof performance !== 'undefined' && performance.memory) {
            return {
                used: performance.memory.usedJSHeapSize,
                total: performance.memory.totalJSHeapSize,
                limit: performance.memory.jsHeapSizeLimit
            };
        }
        return null;
    }

    getTimingMetrics() {
        if (typeof performance !== 'undefined' && performance.timing) {
            const timing = performance.timing;
            return {
                loadTime: timing.loadEventEnd - timing.navigationStart,
                domReady: timing.domContentLoadedEventEnd - timing.navigationStart,
                firstPaint: timing.domContentLoadedEventStart - timing.navigationStart
            };
        }
        return null;
    }

    getNetworkMetrics() {
        if (typeof performance !== 'undefined' && performance.getEntriesByType) {
            const resources = performance.getEntriesByType('resource');
            return {
                requests: resources.length,
                totalSize: resources.reduce((sum, r) => sum + (r.transferSize || 0), 0),
                failedRequests: resources.filter(r => r.transferSize === 0).length
            };
        }
        return null;
    }

    getPerformanceReport() {
        const report = {
            summary: this.getSummary(),
            trends: this.getTrends(),
            recommendations: this.getRecommendations()
        };
        return report;
    }

    getSummary() {
        if (this.metrics.length === 0) return { message: 'No metrics available' };

        const latest = this.metrics[this.metrics.length - 1];
        return {
            memoryUsage: latest.memory,
            averageLoadTime: this.metrics.reduce((sum, m) => sum + (m.timing?.loadTime || 0), 0) / this.metrics.length,
            totalRequests: this.metrics.reduce((sum, m) => sum + (m.network?.requests || 0), 0),
            metricsCollected: this.metrics.length
        };
    }

    getTrends() {
        if (this.metrics.length < 2) return { message: 'Insufficient data for trends' };

        const recent = this.metrics.slice(-10);
        const older = this.metrics.slice(-20, -10);

        return {
            memoryTrend: this.calculateTrend(recent, older, 'memory.used'),
            loadTimeTrend: this.calculateTrend(recent, older, 'timing.loadTime'),
            networkTrend: this.calculateTrend(recent, older, 'network.requests')
        };
    }

    calculateTrend(recent, older, path) {
        const getValue = (metric) => {
            const keys = path.split('.');
            return keys.reduce((obj, key) => obj?.[key], metric);
        };

        const recentAvg = recent.reduce((sum, m) => sum + (getValue(m) || 0), 0) / recent.length;
        const olderAvg = older.reduce((sum, m) => sum + (getValue(m) || 0), 0) / older.length;

        if (olderAvg === 0) return 'stable';
        const change = ((recentAvg - olderAvg) / olderAvg) * 100;

        if (change > 10) return 'increasing';
        if (change < -10) return 'decreasing';
        return 'stable';
    }

    getRecommendations() {
        const summary = this.getSummary();
        const recommendations = [];

        if (summary.memoryUsage && summary.memoryUsage.used > summary.memoryUsage.limit * 0.8) {
            recommendations.push('High memory usage detected - consider optimization');
        }

        if (summary.averageLoadTime > 3000) {
            recommendations.push('Slow load times detected - optimize assets and requests');
        }

        if (summary.totalRequests > 100) {
            recommendations.push('High number of network requests - consider bundling');
        }

        return recommendations;
    }

    on(event, callback) {
        if (!this.eventListeners.has(event)) this.eventListeners.set(event, []);
        this.eventListeners.get(event).push(callback);
    }

    emit(event, data) {
        const listeners = this.eventListeners.get(event);
        if (listeners) listeners.forEach(callback => { try { callback(data); } catch (error) { console.error('Performance event callback error:', error); } });
    }

    getStats() {
        return {
            isMonitoring: this.isMonitoring,
            metricsCount: this.metrics.length,
            maxMetrics: this.config.maxMetrics,
            initialized: this.isInitialized
        };
    }

    async destroy() {
        this.stopMonitoring();
        this.metrics = [];
        this.eventListeners.clear();
        this.isInitialized = false;
        console.log('🧹 Performance service cleaned up');
    }
}

export { PerformanceService };
export default PerformanceService;
