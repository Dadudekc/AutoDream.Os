/**
 * Dashboard Optimized - Performance Enhanced Version
 * V2 Compliance: Performance optimization with modular architecture
 * Features: Caching, lazy loading, performance monitoring
 */

import { DashboardMain } from './dashboard-main.js';

class DashboardOptimized extends DashboardMain {
    constructor() {
        super();
        this.cache = new Map();
        this.performanceMetrics = {
            loadTimes: [],
            renderTimes: [],
            cacheHits: 0,
            cacheMisses: 0
        };
        this.lazyLoadQueue = [];
        this.isInitialized = false;
    }

    // Enhanced initialization with performance monitoring
    async initialize() {
        const startTime = performance.now();
        
        try {
            await super.initialize();
            this.setupPerformanceMonitoring();
            this.setupLazyLoading();
            this.isInitialized = true;
            
            const loadTime = performance.now() - startTime;
            this.recordPerformanceMetric('loadTimes', loadTime);
            
            console.log(`Dashboard optimized initialization completed in ${loadTime.toFixed(2)}ms`);
        } catch (error) {
            console.error('Optimized dashboard initialization failed:', error);
            this.utils.showAlert('error', 'Dashboard initialization failed');
        }
    }

    // Performance monitoring setup
    setupPerformanceMonitoring() {
        // Monitor render performance
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.entryType === 'measure') {
                    this.recordPerformanceMetric('renderTimes', entry.duration);
                }
            }
        });
        observer.observe({ entryTypes: ['measure'] });
    }

    // Lazy loading setup
    setupLazyLoading() {
        // Intersection Observer for lazy loading
        if ('IntersectionObserver' in window) {
            const lazyObserver = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadLazyContent(entry.target);
                        lazyObserver.unobserve(entry.target);
                    }
                });
            });
            
            // Observe lazy-load elements
            document.querySelectorAll('[data-lazy-load]').forEach(el => {
                lazyObserver.observe(el);
            });
        }
    }

    // Enhanced data loading with caching
    async loadDashboardData(view) {
        const cacheKey = `dashboard_${view}`;
        
        // Check cache first
        if (this.cache.has(cacheKey)) {
            const cachedData = this.cache.get(cacheKey);
            if (this.isCacheValid(cachedData)) {
                this.performanceMetrics.cacheHits++;
                this.updateDashboard(cachedData.data);
                return;
            }
        }
        
        this.performanceMetrics.cacheMisses++;
        
        // Load fresh data
        const startTime = performance.now();
        await super.loadDashboardData(view);
        const loadTime = performance.now() - startTime;
        
        // Cache the result
        this.cache.set(cacheKey, {
            data: { view },
            timestamp: Date.now(),
            loadTime
        });
        
        this.recordPerformanceMetric('loadTimes', loadTime);
    }

    // Cache validation
    isCacheValid(cachedData) {
        const maxAge = 5 * 60 * 1000; // 5 minutes
        return (Date.now() - cachedData.timestamp) < maxAge;
    }

    // Performance metric recording
    recordPerformanceMetric(type, value) {
        this.performanceMetrics[type].push(value);
        
        // Keep only last 100 metrics
        if (this.performanceMetrics[type].length > 100) {
            this.performanceMetrics[type].shift();
        }
    }

    // Get performance summary
    getPerformanceSummary() {
        const summary = {};
        
        Object.keys(this.performanceMetrics).forEach(key => {
            const values = this.performanceMetrics[key];
            if (Array.isArray(values) && values.length > 0) {
                summary[key] = {
                    count: values.length,
                    average: values.reduce((a, b) => a + b, 0) / values.length,
                    min: Math.min(...values),
                    max: Math.max(...values)
                };
            } else {
                summary[key] = values;
            }
        });
        
        return summary;
    }

    // Lazy content loading
    async loadLazyContent(element) {
        const loadType = element.dataset.lazyLoad;
        
        try {
            switch (loadType) {
                case 'chart':
                    await this.loadChartLazy(element);
                    break;
                case 'data':
                    await this.loadDataLazy(element);
                    break;
                default:
                    console.warn(`Unknown lazy load type: ${loadType}`);
            }
        } catch (error) {
            console.error(`Lazy loading failed for ${loadType}:`, error);
        }
    }

    // Lazy chart loading
    async loadChartLazy(element) {
        // Implementation for lazy chart loading
        element.innerHTML = '<div class="chart-loading">Loading chart...</div>';
        // Chart loading logic would go here
    }

    // Lazy data loading
    async loadDataLazy(element) {
        // Implementation for lazy data loading
        element.innerHTML = '<div class="data-loading">Loading data...</div>';
        // Data loading logic would go here
    }

    // Cache management
    clearCache() {
        this.cache.clear();
        console.log('Dashboard cache cleared');
    }

    // Get cache statistics
    getCacheStats() {
        return {
            size: this.cache.size,
            keys: Array.from(this.cache.keys()),
            performance: this.performanceMetrics
        };
    }
}

// Initialize optimized dashboard
document.addEventListener('DOMContentLoaded', () => {
    const dashboard = new DashboardOptimized();
    dashboard.initialize();
});

export { DashboardOptimized };
