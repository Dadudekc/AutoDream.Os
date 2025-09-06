/**
 * Dashboard Data Service - V2 Compliant
 * Handles dashboard data loading, processing, and caching
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class DashboardDataService {
    constructor(dashboardRepository, utilityService) {
        this.dashboardRepository = dashboardRepository;
        this.utilityService = utilityService;
        this.dataCache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Load dashboard data with caching
     */
    async loadDashboardData(view, options = {}) {
        try {
            const cacheKey = `dashboard_${view}_${JSON.stringify(options)}`;
            const cached = this.getCachedData(cacheKey);

            if (cached && !options.forceRefresh) {
                return cached;
            }

            const data = await this.dashboardRepository.getDashboardData(view, options);
            const processedData = await this.processDashboardData(data, options);

            this.setCachedData(cacheKey, processedData);
            return processedData;
        } catch (error) {
            this.utilityService.logError(`Failed to load dashboard data for view: ${view}`, error);
            throw error;
        }
    }

    /**
     * Process dashboard data with transformations
     */
    async processDashboardData(data, options = {}) {
        try {
            let processed = { ...data };

            // Apply data transformations
            if (options.includeMetrics) {
                processed.metrics = this.calculateMetrics(processed.items || []);
            }

            if (options.sortBy) {
                processed.items = this.sortItems(processed.items || [], options.sortBy);
            }

            if (options.filterBy) {
                processed.items = this.filterItems(processed.items || [], options.filterBy);
            }

            if (options.groupBy) {
                processed.groups = this.groupItems(processed.items || [], options.groupBy);
            }

            processed.processedAt = this.utilityService.formatDate(new Date(), 'ISO');
            processed.processingOptions = options;

            return processed;
        } catch (error) {
            this.utilityService.logError('Dashboard data processing failed', error);
            return data;
        }
    }

    /**
     * Calculate dashboard metrics
     */
    calculateMetrics(items) {
        try {
            if (!Array.isArray(items)) return {};

            return {
                total: items.length,
                active: items.filter(item => item.active).length,
                inactive: items.filter(item => !item.active).length,
                completed: items.filter(item => item.status === 'completed').length,
                pending: items.filter(item => item.status === 'pending').length,
                failed: items.filter(item => item.status === 'failed').length,
                averageValue: this.calculateAverage(items, 'value'),
                lastUpdated: this.utilityService.formatDate(new Date(), 'ISO')
            };
        } catch (error) {
            this.utilityService.logError('Metrics calculation failed', error);
            return {};
        }
    }

    /**
     * Sort items by specified field
     */
    sortItems(items, sortBy) {
        try {
            if (!Array.isArray(items)) return items;

            return [...items].sort((a, b) => {
                const aValue = this.getNestedValue(a, sortBy);
                const bValue = this.getNestedValue(b, sortBy);

                if (aValue < bValue) return -1;
                if (aValue > bValue) return 1;
                return 0;
            });
        } catch (error) {
            this.utilityService.logError('Item sorting failed', error);
            return items;
        }
    }

    /**
     * Filter items by criteria
     */
    filterItems(items, filterBy) {
        try {
            if (!Array.isArray(items)) return items;

            return items.filter(item => {
                return Object.entries(filterBy).every(([key, value]) => {
                    const itemValue = this.getNestedValue(item, key);
                    return itemValue === value;
                });
            });
        } catch (error) {
            this.utilityService.logError('Item filtering failed', error);
            return items;
        }
    }

    /**
     * Group items by field
     */
    groupItems(items, groupBy) {
        try {
            if (!Array.isArray(items)) return {};

            return items.reduce((groups, item) => {
                const key = this.getNestedValue(item, groupBy);
                if (!groups[key]) {
                    groups[key] = [];
                }
                groups[key].push(item);
                return groups;
            }, {});
        } catch (error) {
            this.utilityService.logError('Item grouping failed', error);
            return {};
        }
    }

    /**
     * Get nested object value
     */
    getNestedValue(obj, path) {
        try {
            return path.split('.').reduce((current, key) => current?.[key], obj);
        } catch (error) {
            return undefined;
        }
    }

    /**
     * Calculate average of numeric field
     */
    calculateAverage(items, field) {
        try {
            if (!Array.isArray(items) || items.length === 0) return 0;

            const values = items
                .map(item => this.getNestedValue(item, field))
                .filter(value => typeof value === 'number' && !isNaN(value));

            if (values.length === 0) return 0;

            return values.reduce((sum, value) => sum + value, 0) / values.length;
        } catch (error) {
            this.utilityService.logError('Average calculation failed', error);
            return 0;
        }
    }

    /**
     * Get cached data
     */
    getCachedData(key) {
        try {
            const cached = this.dataCache.get(key);
            if (!cached) return null;

            if (Date.now() - cached.timestamp > this.cacheTimeout) {
                this.dataCache.delete(key);
                return null;
            }

            return cached.data;
        } catch (error) {
            this.utilityService.logError('Cache retrieval failed', error);
            return null;
        }
    }

    /**
     * Set cached data
     */
    setCachedData(key, data) {
        try {
            this.dataCache.set(key, {
                data,
                timestamp: Date.now()
            });
        } catch (error) {
            this.utilityService.logError('Cache storage failed', error);
        }
    }

    /**
     * Clear data cache
     */
    clearCache() {
        try {
            this.dataCache.clear();
            this.utilityService.logInfo('Dashboard data cache cleared');
        } catch (error) {
            this.utilityService.logError('Cache clearing failed', error);
        }
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        try {
            const now = Date.now();
            let validEntries = 0;
            let expiredEntries = 0;

            for (const [key, entry] of this.dataCache.entries()) {
                if (now - entry.timestamp > this.cacheTimeout) {
                    expiredEntries++;
                } else {
                    validEntries++;
                }
            }

            return {
                totalEntries: this.dataCache.size,
                validEntries,
                expiredEntries,
                cacheTimeout: this.cacheTimeout
            };
        } catch (error) {
            this.utilityService.logError('Cache statistics retrieval failed', error);
            return {};
        }
    }
}

// Factory function for creating dashboard data service
export function createDashboardDataService(dashboardRepository, utilityService) {
    return new DashboardDataService(dashboardRepository, utilityService);
}
