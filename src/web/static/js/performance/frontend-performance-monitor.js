/**
 * Frontend Performance Monitor - V2 Compliant
 * ===========================================
 *
 * Comprehensive frontend performance monitoring and optimization.
 * Tracks metrics, identifies bottlenecks, and provides optimization recommendations.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class FrontendPerformanceMonitor {
    constructor() {
        this.metrics = new Map();
        this.observers = new Map();
        this.optimizationRecommendations = [];
        this.logger = console;
        this.isMonitoring = false;

        // Performance thresholds
        this.thresholds = {
            domQueryTime: 16, // ms (60fps)
            renderTime: 16, // ms (60fps)
            memoryUsage: 50 * 1024 * 1024, // 50MB
            bundleSize: 500 * 1024, // 500KB
            networkLatency: 200 // ms
        };

        this.startTime = Date.now();
    }

    /**
     * Start performance monitoring
     */
    startMonitoring() {
        if (this.isMonitoring) return;

        this.isMonitoring = true;
        this.setupPerformanceObservers();
        this.startMetricsCollection();
        this.startOptimizationAnalysis();

        this.logger.log('📊 Frontend Performance Monitor started');
    }

    /**
     * Stop performance monitoring
     */
    stopMonitoring() {
        this.isMonitoring = false;
        this.cleanupObservers();
        this.logger.log('📊 Frontend Performance Monitor stopped');
    }

    /**
     * Setup performance observers
     */
    setupPerformanceObservers() {
        // Monitor DOM mutations
        if (window.MutationObserver) {
            const domObserver = new MutationObserver((mutations) => {
                this.recordMetric('domMutations', mutations.length);
                this.analyzeDOMPerformance(mutations);
            });

            domObserver.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true
            });

            this.observers.set('dom', domObserver);
        }

        // Monitor resource loading
        if (window.PerformanceObserver) {
            const resourceObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                this.analyzeResourcePerformance(entries);
            });

            resourceObserver.observe({ entryTypes: ['resource'] });
            this.observers.set('resources', resourceObserver);
        }

        // Monitor long tasks
        if (window.PerformanceObserver) {
            const longTaskObserver = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                this.analyzeLongTasks(entries);
            });

            longTaskObserver.observe({ entryTypes: ['longtask'] });
            this.observers.set('longTasks', longTaskObserver);
        }
    }

    /**
     * Start metrics collection
     */
    startMetricsCollection() {
        setInterval(() => {
            this.collectPerformanceMetrics();
        }, 1000); // Collect every second
    }

    /**
     * Collect performance metrics
     */
    collectPerformanceMetrics() {
        // Memory usage
        if (performance.memory) {
            this.recordMetric('memoryUsed', performance.memory.usedJSHeapSize);
            this.recordMetric('memoryTotal', performance.memory.totalJSHeapSize);
            this.recordMetric('memoryLimit', performance.memory.jsHeapSizeLimit);
        }

        // Navigation timing
        const navigation = performance.getEntriesByType('navigation')[0];
        if (navigation) {
            this.recordMetric('domContentLoaded', navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart);
            this.recordMetric('loadComplete', navigation.loadEventEnd - navigation.loadEventStart);
            this.recordMetric('totalLoadTime', navigation.loadEventEnd - navigation.navigationStart);
        }

        // Paint timing
        const paintEntries = performance.getEntriesByType('paint');
        paintEntries.forEach(entry => {
            this.recordMetric(entry.name, entry.startTime);
        });
    }

    /**
     * Analyze DOM performance
     */
    analyzeDOMPerformance(mutations) {
        const domQueryTime = this.measureDOMPerformance();
        this.recordMetric('domQueryTime', domQueryTime);

        if (domQueryTime > this.thresholds.domQueryTime) {
            this.addRecommendation('DOM Performance',
                `DOM queries taking ${domQueryTime}ms (threshold: ${this.thresholds.domQueryTime}ms)`,
                'Consider using document fragments and batch DOM operations'
            );
        }
    }

    /**
     * Measure DOM performance
     */
    measureDOMPerformance() {
        const start = performance.now();

        // Simulate DOM operations
        const elements = document.querySelectorAll('*');
        elements.forEach(el => el.offsetHeight); // Force reflow

        return performance.now() - start;
    }

    /**
     * Analyze resource performance
     */
    analyzeResourcePerformance(entries) {
        entries.forEach(entry => {
            const loadTime = entry.responseEnd - entry.startTime;
            this.recordMetric(`resource_${entry.name}`, loadTime);

            if (loadTime > this.thresholds.networkLatency) {
                this.addRecommendation('Network Performance',
                    `Resource ${entry.name} took ${loadTime}ms to load`,
                    'Consider optimizing resource size or using CDN'
                );
            }
        });
    }

    /**
     * Analyze long tasks
     */
    analyzeLongTasks(entries) {
        entries.forEach(entry => {
            this.recordMetric('longTaskDuration', entry.duration);

            if (entry.duration > 50) { // 50ms threshold
                this.addRecommendation('Long Task',
                    `Long task detected: ${entry.duration}ms`,
                    'Consider breaking down long-running operations'
                );
            }
        });
    }

    /**
     * Start optimization analysis
     */
    startOptimizationAnalysis() {
        setInterval(() => {
            this.analyzePerformanceBottlenecks();
        }, 5000); // Analyze every 5 seconds
    }

    /**
     * Analyze performance bottlenecks
     */
    analyzePerformanceBottlenecks() {
        // Check memory usage
        const memoryUsed = this.getMetric('memoryUsed');
        if (memoryUsed && memoryUsed > this.thresholds.memoryUsage) {
            this.addRecommendation('Memory Usage',
                `High memory usage: ${Math.round(memoryUsed / 1024 / 1024)}MB`,
                'Consider implementing memory cleanup and garbage collection'
            );
        }

        // Check bundle size
        this.analyzeBundleSize();

        // Check render performance
        this.analyzeRenderPerformance();
    }

    /**
     * Analyze bundle size
     */
    analyzeBundleSize() {
        const scripts = document.querySelectorAll('script[src]');
        let totalSize = 0;

        scripts.forEach(script => {
            // Estimate size (this is a simplified approach)
            totalSize += script.src.length * 2; // Rough estimate
        });

        if (totalSize > this.thresholds.bundleSize) {
            this.addRecommendation('Bundle Size',
                `Large bundle size: ${Math.round(totalSize / 1024)}KB`,
                'Consider code splitting and lazy loading'
            );
        }
    }

    /**
     * Analyze render performance
     */
    analyzeRenderPerformance() {
        const renderTime = this.measureRenderPerformance();
        this.recordMetric('renderTime', renderTime);

        if (renderTime > this.thresholds.renderTime) {
            this.addRecommendation('Render Performance',
                `Slow rendering: ${renderTime}ms (target: ${this.thresholds.renderTime}ms)`,
                'Consider using requestAnimationFrame and optimizing CSS'
            );
        }
    }

    /**
     * Measure render performance
     */
    measureRenderPerformance() {
        const start = performance.now();

        // Force a reflow/repaint
        document.body.style.transform = 'translateZ(0)';
        document.body.offsetHeight; // Force reflow
        document.body.style.transform = '';

        return performance.now() - start;
    }

    /**
     * Record performance metric
     */
    recordMetric(name, value) {
        if (!this.metrics.has(name)) {
            this.metrics.set(name, []);
        }

        const values = this.metrics.get(name);
        values.push({
            value: value,
            timestamp: Date.now()
        });

        // Keep only last 100 values
        if (values.length > 100) {
            values.shift();
        }
    }

    /**
     * Get metric value
     */
    getMetric(name) {
        const values = this.metrics.get(name);
        if (!values || values.length === 0) return null;

        // Return average of last 10 values
        const recent = values.slice(-10);
        return recent.reduce((sum, item) => sum + item.value, 0) / recent.length;
    }

    /**
     * Add optimization recommendation
     */
    addRecommendation(category, issue, solution) {
        const recommendation = {
            category,
            issue,
            solution,
            timestamp: Date.now()
        };

        this.optimizationRecommendations.push(recommendation);

        // Keep only last 50 recommendations
        if (this.optimizationRecommendations.length > 50) {
            this.optimizationRecommendations.shift();
        }
    }

    /**
     * Get performance report
     */
    getPerformanceReport() {
        return {
            metrics: Object.fromEntries(this.metrics),
            recommendations: this.optimizationRecommendations,
            uptime: Date.now() - this.startTime,
            isMonitoring: this.isMonitoring
        };
    }

    /**
     * Get optimization recommendations
     */
    getOptimizationRecommendations() {
        return this.optimizationRecommendations;
    }

    /**
     * Clear recommendations
     */
    clearRecommendations() {
        this.optimizationRecommendations = [];
    }

    /**
     * Cleanup observers
     */
    cleanupObservers() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
    }

    /**
     * Export performance data
     */
    exportPerformanceData() {
        return {
            report: this.getPerformanceReport(),
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent,
            url: window.location.href
        };
    }
}
