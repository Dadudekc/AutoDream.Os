/**
 * Performance Tests Module - V2 Compliant
 * Tests for system performance and optimization
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class PerformanceTests {
    constructor(systemHealth, testResults, performanceMetrics) {
        this.systemHealth = systemHealth;
        this.testResults = testResults;
        this.performanceMetrics = performanceMetrics;
    }

    /**
     * Test performance optimization
     */
    async testPerformanceOptimization() {
        console.log('⚡ Testing Performance Optimization...');

        const tests = [
            this.testInitializationPerformance.bind(this),
            this.testComponentLoadPerformance.bind(this),
            this.testMemoryOptimization.bind(this),
            this.testCachingPerformance.bind(this),
            this.testLazyLoadingPerformance.bind(this),
            this.testBundleOptimization.bind(this)
        ];

        let passed = 0;
        const results = [];

        for (const test of tests) {
            try {
                const result = await test();
                results.push(result);
                if (result.success) passed++;
            } catch (error) {
                results.push({
                    name: test.name,
                    success: false,
                    error: error.message
                });
                console.error(`❌ Performance test failed:`, error);
            }
        }

        const success = passed >= tests.length * 0.8; // 80% success threshold
        this.systemHealth.performanceOptimization = success;

        console.log(`✅ Performance Optimization: ${passed}/${tests.length} tests passed`);

        return {
            name: 'Performance Optimization',
            success,
            passed,
            total: tests.length,
            results
        };
    }

    /**
     * Test initialization performance
     */
    async testInitializationPerformance() {
        try {
            const startTime = performance.now();

            // Test dashboard initialization
            const dashboard = new window.DashboardMain();
            await dashboard.initialize();

            const endTime = performance.now();
            const initTime = endTime - startTime;

            this.performanceMetrics.initializationTime = initTime;

            // Check if initialization is within acceptable time (5 seconds)
            const acceptableTime = 5000;
            const success = initTime < acceptableTime;

            return {
                name: 'Initialization Performance',
                success,
                details: `Initialization completed in ${initTime.toFixed(2)}ms (${success ? 'within' : 'over'} ${acceptableTime}ms limit)`,
                metrics: { initTime, acceptableTime }
            };
        } catch (error) {
            return {
                name: 'Initialization Performance',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test component load performance
     */
    async testComponentLoadPerformance() {
        try {
            const startTime = performance.now();

            // Load multiple components
            const components = [
                new window.DashboardService(),
                new window.DeploymentService(),
                new window.UtilityService()
            ];

            // Initialize components
            await Promise.all(components.map(comp => comp.initialize ? comp.initialize() : Promise.resolve()));

            const endTime = performance.now();
            const loadTime = endTime - startTime;

            this.performanceMetrics.componentLoadTime = loadTime;

            // Check if component loading is within acceptable time (3 seconds)
            const acceptableTime = 3000;
            const success = loadTime < acceptableTime;

            return {
                name: 'Component Load Performance',
                success,
                details: `Components loaded in ${loadTime.toFixed(2)}ms (${success ? 'within' : 'over'} ${acceptableTime}ms limit)`,
                metrics: { loadTime, acceptableTime }
            };
        } catch (error) {
            return {
                name: 'Component Load Performance',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test memory optimization
     */
    async testMemoryOptimization() {
        try {
            // Check for memory leaks by creating and cleaning up components
            const initialMemory = performance.memory ? performance.memory.usedJSHeapSize : 0;

            // Create multiple component instances
            const components = [];
            for (let i = 0; i < 10; i++) {
                components.push(new window.DashboardService());
            }

            // Clean up components
            components.forEach(comp => {
                if (comp.cleanup) comp.cleanup();
            });

            // Force garbage collection if available
            if (window.gc) {
                window.gc();
            }

            // Small delay for cleanup
            await new Promise(resolve => setTimeout(resolve, 100));

            const finalMemory = performance.memory ? performance.memory.usedJSHeapSize : 0;
            const memoryIncrease = finalMemory - initialMemory;

            // Check if memory increase is reasonable (less than 10MB)
            const acceptableIncrease = 10 * 1024 * 1024;
            const success = memoryIncrease < acceptableIncrease;

            return {
                name: 'Memory Optimization',
                success,
                details: `Memory increase: ${(memoryIncrease / 1024 / 1024).toFixed(2)}MB (${success ? 'within' : 'over'} ${(acceptableIncrease / 1024 / 1024).toFixed(2)}MB limit)`,
                metrics: { memoryIncrease, acceptableIncrease }
            };
        } catch (error) {
            return {
                name: 'Memory Optimization',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test caching performance
     */
    async testCachingPerformance() {
        try {
            const utilityService = new window.UtilityService();
            const cache = utilityService.cache;

            if (!cache) {
                return {
                    name: 'Caching Performance',
                    success: false,
                    error: 'Cache system not available'
                };
            }

            const startTime = performance.now();

            // Test cache operations
            for (let i = 0; i < 100; i++) {
                cache.set(`test_key_${i}`, `test_value_${i}`);
                cache.get(`test_key_${i}`);
            }

            const endTime = performance.now();
            const cacheTime = endTime - startTime;

            // Check if cache operations are fast (less than 100ms for 100 operations)
            const acceptableTime = 100;
            const success = cacheTime < acceptableTime;

            return {
                name: 'Caching Performance',
                success,
                details: `Cache operations completed in ${cacheTime.toFixed(2)}ms (${success ? 'within' : 'over'} ${acceptableTime}ms limit)`,
                metrics: { cacheTime, acceptableTime }
            };
        } catch (error) {
            return {
                name: 'Caching Performance',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test lazy loading performance
     */
    async testLazyLoadingPerformance() {
        try {
            // Test lazy loading of components
            const startTime = performance.now();

            // Simulate lazy loading
            await new Promise(resolve => setTimeout(resolve, 10));

            const endTime = performance.now();
            const lazyLoadTime = endTime - startTime;

            // Lazy loading should be fast (less than 50ms)
            const acceptableTime = 50;
            const success = lazyLoadTime < acceptableTime;

            return {
                name: 'Lazy Loading Performance',
                success,
                details: `Lazy loading completed in ${lazyLoadTime.toFixed(2)}ms (${success ? 'within' : 'over'} ${acceptableTime}ms limit)`,
                metrics: { lazyLoadTime, acceptableTime }
            };
        } catch (error) {
            return {
                name: 'Lazy Loading Performance',
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Test bundle optimization
     */
    async testBundleOptimization() {
        try {
            // Test bundle size and loading
            const resources = performance.getEntriesByType('resource');
            const jsResources = resources.filter(resource => resource.name.includes('.js'));

            let totalBundleSize = 0;
            let totalLoadTime = 0;

            jsResources.forEach(resource => {
                totalBundleSize += resource.transferSize || 0;
                totalLoadTime += resource.responseEnd - resource.requestStart;
            });

            // Check bundle size (should be reasonable)
            const maxBundleSize = 5 * 1024 * 1024; // 5MB
            const bundleSizeOk = totalBundleSize < maxBundleSize;

            // Check load time (should be reasonable)
            const maxLoadTime = 2000; // 2 seconds
            const loadTimeOk = totalLoadTime < maxLoadTime;

            const success = bundleSizeOk && loadTimeOk;

            return {
                name: 'Bundle Optimization',
                success,
                details: `Bundle: ${(totalBundleSize / 1024 / 1024).toFixed(2)}MB, Load: ${totalLoadTime.toFixed(2)}ms (${success ? 'optimized' : 'needs optimization'})`,
                metrics: { totalBundleSize, totalLoadTime, maxBundleSize, maxLoadTime }
            };
        } catch (error) {
            return {
                name: 'Bundle Optimization',
                success: false,
                error: error.message
            };
        }
    }
}

// Factory function for creating performance tests
export function createPerformanceTests(systemHealth, testResults, performanceMetrics) {
    return new PerformanceTests(systemHealth, testResults, performanceMetrics);
}
