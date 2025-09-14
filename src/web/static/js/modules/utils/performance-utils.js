/**
 * Performance Utilities - V2 Compliant Performance Monitoring
 * V2 COMPLIANT: 150 lines maximum
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Performance monitoring and optimization utilities
 */

// ================================
// PERFORMANCE MONITOR CLASS
// ================================

/**
 * Performance Monitor
 * Handles performance measurement and optimization
 */
export class PerformanceMonitor {
    constructor(options = {}) {
        this.metrics = new Map();
        this.observers = new Map();
        this.isMonitoring = false;
        this.sampleRate = options.sampleRate || 0.1;
        this.maxMetrics = options.maxMetrics || 1000;
    }

    /**
     * Start performance monitoring
     */
    start() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        this.setupPerformanceObservers();
        console.log('📊 Performance monitoring started');
    }

    /**
     * Stop performance monitoring
     */
    stop() {
        this.isMonitoring = false;
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
        console.log('📊 Performance monitoring stopped');
    }

    /**
     * Setup performance observers
     */
    setupPerformanceObservers() {
        if (!('PerformanceObserver' in window)) return;

        // Largest Contentful Paint
        try {
            const lcpObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                const lastEntry = entries[entries.length - 1];
                this.record('lcp', lastEntry.startTime);
            });
            lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });
            this.observers.set('lcp', lcpObserver);
        } catch (error) {
            console.warn('LCP observer setup failed:', error);
        }

        // First Input Delay
        try {
            const fidObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                entries.forEach(entry => {
                    const delay = entry.processingStart - entry.startTime;
                    this.record('fid', delay);
                });
            });
            fidObserver.observe({ entryTypes: ['first-input'] });
            this.observers.set('fid', fidObserver);
        } catch (error) {
            console.warn('FID observer setup failed:', error);
        }
    }

    /**
     * Record a performance metric
     */
    record(name, value, context = {}) {
        if (!this.isMonitoring || Math.random() > this.sampleRate) return;

        const metric = {
            name,
            value,
            timestamp: Date.now(),
            context
        };

        if (!this.metrics.has(name)) {
            this.metrics.set(name, []);
        }

        const metrics = this.metrics.get(name);
        metrics.push(metric);

        // Limit metrics size
        if (metrics.length > this.maxMetrics) {
            metrics.shift();
        }

        // Dispatch performance event
        window.dispatchEvent(new CustomEvent('performance:measure', {
            detail: metric
        }));
    }

    /**
     * Measure function execution time
     */
    measureFunction(name, fn, context = {}) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        
        this.record(name, end - start, context);
        return result;
    }

    /**
     * Measure async function execution time
     */
    async measureAsyncFunction(name, fn, context = {}) {
        const start = performance.now();
        const result = await fn();
        const end = performance.now();
        
        this.record(name, end - start, context);
        return result;
    }

    /**
     * Get performance metrics
     */
    getMetrics() {
        const result = {};
        for (const [name, metrics] of this.metrics) {
            if (metrics.length > 0) {
                const values = metrics.map(m => m.value);
                result[name] = {
                    count: values.length,
                    average: values.reduce((a, b) => a + b, 0) / values.length,
                    min: Math.min(...values),
                    max: Math.max(...values),
                    latest: values[values.length - 1]
                };
            }
        }
        return result;
    }

    /**
     * Get specific metric
     */
    getMetric(name) {
        const metrics = this.metrics.get(name);
        if (!metrics || metrics.length === 0) return null;

        const values = metrics.map(m => m.value);
        return {
            count: values.length,
            average: values.reduce((a, b) => a + b, 0) / values.length,
            min: Math.min(...values),
            max: Math.max(...values),
            latest: values[values.length - 1]
        };
    }

    /**
     * Clear metrics
     */
    clearMetrics(name = null) {
        if (name) {
            this.metrics.delete(name);
        } else {
            this.metrics.clear();
        }
    }
}

// ================================
// PERFORMANCE UTILITIES
// ================================

/**
 * Measure DOM operation performance
 */
export function measureDOMOperation(name, operation) {
    const start = performance.now();
    const result = operation();
    const end = performance.now();
    
    console.log(`📊 DOM Operation '${name}': ${(end - start).toFixed(2)}ms`);
    return result;
}

/**
 * Measure memory usage
 */
export function measureMemoryUsage() {
    if ('memory' in performance) {
        const memInfo = performance.memory;
        return {
            used: memInfo.usedJSHeapSize,
            total: memInfo.totalJSHeapSize,
            limit: memInfo.jsHeapSizeLimit,
            usage: (memInfo.usedJSHeapSize / memInfo.totalJSHeapSize) * 100
        };
    }
    return null;
}

/**
 * Check if performance is within acceptable limits
 */
export function isPerformanceAcceptable(metric, threshold) {
    const monitor = new PerformanceMonitor();
    const metricData = monitor.getMetric(metric);
    
    if (!metricData) return true;
    
    return metricData.average <= threshold;
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create performance monitor with default settings
 */
export function createPerformanceMonitor(options = {}) {
    return new PerformanceMonitor(options);
}

// Export default
export default PerformanceMonitor;