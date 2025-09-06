/**
 * Bundle Optimizer - V2 Compliant
 * ===============================
 *
 * JavaScript bundle optimization and analysis.
 * Provides code splitting, lazy loading, and bundle size optimization.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class BundleOptimizer {
    constructor() {
        this.modules = new Map();
        this.loadedModules = new Set();
        this.loadingPromises = new Map();
        this.bundleMetrics = {
            totalSize: 0,
            loadedSize: 0,
            loadTime: 0,
            moduleCount: 0
        };
        this.logger = console;
    }

    /**
     * Register a module for lazy loading
     */
    registerModule(name, loader, dependencies = []) {
        this.modules.set(name, {
            loader,
            dependencies,
            loaded: false,
            size: 0
        });

        this.bundleMetrics.moduleCount++;
        this.logger.log(`📦 Registered module: ${name}`);
    }

    /**
     * Load module with dependencies
     */
    async loadModule(name) {
        if (this.loadedModules.has(name)) {
            return this.modules.get(name);
        }

        // Check if already loading
        if (this.loadingPromises.has(name)) {
            return this.loadingPromises.get(name);
        }

        const module = this.modules.get(name);
        if (!module) {
            throw new Error(`Module ${name} not found`);
        }

        // Create loading promise
        const loadingPromise = this.loadModuleWithDependencies(name);
        this.loadingPromises.set(name, loadingPromise);

        try {
            const result = await loadingPromise;
            this.loadedModules.add(name);
            module.loaded = true;
            this.bundleMetrics.loadedSize += module.size;
            this.logger.log(`✅ Module loaded: ${name}`);
            return result;
        } catch (error) {
            this.logger.error(`❌ Failed to load module ${name}:`, error);
            throw error;
        } finally {
            this.loadingPromises.delete(name);
        }
    }

    /**
     * Load module with its dependencies
     */
    async loadModuleWithDependencies(name) {
        const module = this.modules.get(name);
        const dependencies = module.dependencies;

        // Load dependencies first
        const dependencyPromises = dependencies.map(dep => this.loadModule(dep));
        await Promise.all(dependencyPromises);

        // Load the module itself
        const startTime = performance.now();
        const result = await module.loader();
        const loadTime = performance.now() - startTime;

        module.size = this.estimateModuleSize(result);
        this.bundleMetrics.loadTime += loadTime;

        return result;
    }

    /**
     * Estimate module size
     */
    estimateModuleSize(module) {
        if (typeof module === 'string') {
            return module.length * 2; // Rough estimate
        }

        if (typeof module === 'object' && module !== null) {
            return JSON.stringify(module).length * 2;
        }

        return 1000; // Default estimate
    }

    /**
     * Preload critical modules
     */
    async preloadCriticalModules(criticalModules) {
        const preloadPromises = criticalModules.map(name => this.loadModule(name));
        await Promise.all(preloadPromises);
        this.logger.log('🚀 Critical modules preloaded');
    }

    /**
     * Lazy load module when needed
     */
    createLazyLoader(name, trigger) {
        return async (...args) => {
            const module = await this.loadModule(name);

            if (typeof module[trigger] === 'function') {
                return module[trigger](...args);
            }

            return module;
        };
    }

    /**
     * Create code splitter for large modules
     */
    createCodeSplitter(moduleName, chunks) {
        return {
            loadChunk: async (chunkName) => {
                const fullName = `${moduleName}_${chunkName}`;
                return this.loadModule(fullName);
            },

            loadAllChunks: async () => {
                const chunkPromises = chunks.map(chunk =>
                    this.loadModule(`${moduleName}_${chunk}`)
                );
                return Promise.all(chunkPromises);
            }
        };
    }

    /**
     * Optimize bundle by removing unused modules
     */
    optimizeBundle(usedModules) {
        const unusedModules = [];

        this.modules.forEach((module, name) => {
            if (!usedModules.includes(name) && !module.loaded) {
                unusedModules.push(name);
            }
        });

        // Remove unused modules
        unusedModules.forEach(name => {
            this.modules.delete(name);
            this.bundleMetrics.moduleCount--;
        });

        this.logger.log(`🧹 Removed ${unusedModules.length} unused modules`);
        return unusedModules;
    }

    /**
     * Get bundle metrics
     */
    getBundleMetrics() {
        return {
            ...this.bundleMetrics,
            loadedModules: this.loadedModules.size,
            totalModules: this.modules.size,
            averageLoadTime: this.bundleMetrics.loadTime / this.loadedModules.size || 0
        };
    }

    /**
     * Analyze bundle performance
     */
    analyzeBundlePerformance() {
        const metrics = this.getBundleMetrics();
        const recommendations = [];

        // Check bundle size
        if (metrics.totalSize > 500 * 1024) { // 500KB
            recommendations.push({
                type: 'bundle_size',
                message: 'Bundle size is large',
                suggestion: 'Consider code splitting and lazy loading'
            });
        }

        // Check load time
        if (metrics.averageLoadTime > 100) { // 100ms
            recommendations.push({
                type: 'load_time',
                message: 'Module load time is slow',
                suggestion: 'Optimize module size and dependencies'
            });
        }

        // Check module count
        if (metrics.moduleCount > 50) {
            recommendations.push({
                type: 'module_count',
                message: 'Too many modules',
                suggestion: 'Consider consolidating related modules'
            });
        }

        return {
            metrics,
            recommendations
        };
    }

    /**
     * Create performance-optimized module loader
     */
    createOptimizedLoader() {
        return {
            load: async (name) => {
                const startTime = performance.now();
                const module = await this.loadModule(name);
                const loadTime = performance.now() - startTime;

                this.logger.log(`⚡ Module ${name} loaded in ${loadTime.toFixed(2)}ms`);
                return module;
            },

            preload: (names) => this.preloadCriticalModules(names),

            getMetrics: () => this.getBundleMetrics(),

            analyze: () => this.analyzeBundlePerformance()
        };
    }

    /**
     * Cleanup resources
     */
    cleanup() {
        this.modules.clear();
        this.loadedModules.clear();
        this.loadingPromises.clear();
        this.bundleMetrics = {
            totalSize: 0,
            loadedSize: 0,
            loadTime: 0,
            moduleCount: 0
        };

        this.logger.log('🧹 Bundle optimizer cleanup completed');
    }
}
