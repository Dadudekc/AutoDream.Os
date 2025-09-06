/**
 * Performance Configuration Module - V2 Compliant
 * Performance thresholds and baselines management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// PERFORMANCE CONFIGURATION MODULE
// ================================

/**
 * Performance thresholds and baselines management
 */
export class PerformanceConfigurationModule {
    constructor() {
        this.logger = console;
        this.performanceThresholds = new Map();
        this.baselineMetrics = new Map();
        this.defaultThresholds = this.getDefaultThresholds();
    }

    /**
     * Set performance threshold
     */
    setPerformanceThreshold(componentName, threshold) {
        try {
            this.validateThreshold(threshold);
            this.performanceThresholds.set(componentName, threshold);
            return true;
        } catch (error) {
            this.logger.error(`Failed to set performance threshold for ${componentName}:`, error);
            return false;
        }
    }

    /**
     * Get performance threshold
     */
    getPerformanceThreshold(componentName) {
        return this.performanceThresholds.get(componentName) || this.defaultThresholds;
    }

    /**
     * Set baseline metrics
     */
    setBaselineMetrics(componentName, metrics) {
        try {
            this.validateMetrics(metrics);
            this.baselineMetrics.set(componentName, metrics);
            return true;
        } catch (error) {
            this.logger.error(`Failed to set baseline metrics for ${componentName}:`, error);
            return false;
        }
    }

    /**
     * Get baseline metrics
     */
    getBaselineMetrics(componentName) {
        return this.baselineMetrics.get(componentName);
    }

    /**
     * Update baseline metrics
     */
    updateBaselineMetrics(componentName, newMetrics) {
        try {
            const currentBaseline = this.getBaselineMetrics(componentName);
            if (!currentBaseline) {
                return this.setBaselineMetrics(componentName, newMetrics);
            }

            // Calculate rolling average
            const updatedMetrics = {};
            Object.keys(newMetrics).forEach(key => {
                if (typeof newMetrics[key] === 'number' && typeof currentBaseline[key] === 'number') {
                    updatedMetrics[key] = (currentBaseline[key] + newMetrics[key]) / 2;
                } else {
                    updatedMetrics[key] = newMetrics[key];
                }
            });

            return this.setBaselineMetrics(componentName, updatedMetrics);
        } catch (error) {
            this.logger.error(`Failed to update baseline metrics for ${componentName}:`, error);
            return false;
        }
    }

    /**
     * Get default thresholds
     */
    getDefaultThresholds() {
        return {
            loadTime: 1000, // 1 second
            memoryUsage: 200, // 200MB
            cpuUsage: 30, // 30%
            networkRequests: 40, // 40 requests
            domNodes: 1000, // 1000 nodes
            jsHeapSize: 50 // 50MB
        };
    }

    /**
     * Get all configured components
     */
    getConfiguredComponents() {
        const components = new Set();

        // Add components with thresholds
        this.performanceThresholds.forEach((_, componentName) => {
            components.add(componentName);
        });

        // Add components with baselines
        this.baselineMetrics.forEach((_, componentName) => {
            components.add(componentName);
        });

        return Array.from(components);
    }

    /**
     * Export configuration
     */
    exportConfiguration() {
        return {
            thresholds: Object.fromEntries(this.performanceThresholds),
            baselines: Object.fromEntries(this.baselineMetrics),
            configuredComponents: this.getConfiguredComponents(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Import configuration
     */
    importConfiguration(config) {
        try {
            if (config.thresholds) {
                Object.entries(config.thresholds).forEach(([component, threshold]) => {
                    this.setPerformanceThreshold(component, threshold);
                });
            }

            if (config.baselines) {
                Object.entries(config.baselines).forEach(([component, baseline]) => {
                    this.setBaselineMetrics(component, baseline);
                });
            }

            return true;
        } catch (error) {
            this.logger.error('Failed to import configuration:', error);
            return false;
        }
    }

    /**
     * Clear all configuration
     */
    clearConfiguration() {
        this.performanceThresholds.clear();
        this.baselineMetrics.clear();
        return true;
    }

    /**
     * Validate threshold object
     */
    validateThreshold(threshold) {
        if (!threshold || typeof threshold !== 'object') {
            throw new Error('Threshold must be a valid object');
        }

        const requiredFields = ['loadTime', 'memoryUsage', 'cpuUsage'];
        for (const field of requiredFields) {
            if (typeof threshold[field] !== 'number') {
                throw new Error(`Threshold field ${field} must be a number`);
            }
        }
    }

    /**
     * Validate metrics object
     */
    validateMetrics(metrics) {
        if (!metrics || typeof metrics !== 'object') {
            throw new Error('Metrics must be a valid object');
        }

        const requiredFields = ['loadTime', 'memoryUsage', 'cpuUsage'];
        for (const field of requiredFields) {
            if (typeof metrics[field] !== 'number') {
                throw new Error(`Metrics field ${field} must be a number`);
            }
        }
    }

    /**
     * Get configuration summary
     */
    getConfigurationSummary() {
        return {
            thresholdCount: this.performanceThresholds.size,
            baselineCount: this.baselineMetrics.size,
            configuredComponents: this.getConfiguredComponents(),
            defaultThresholds: this.defaultThresholds
        };
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create performance configuration module instance
 */
export function createPerformanceConfigurationModule() {
    return new PerformanceConfigurationModule();
}
