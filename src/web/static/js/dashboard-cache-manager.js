/**
 * Dashboard Cache Manager Module - V2 Compliant
 * Cache management functionality extracted from dashboard-data-manager.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// DASHBOARD CACHE MANAGER
// ================================

/**
 * Cache management for dashboard data
 */
class DashboardCacheManager {
    constructor() {
        this.dataCache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
    }

    /**
     * Cache data with timestamp
     */
    cacheData(key, data, isOptimistic = false) {
        const entry = {
            data: data,
            timestamp: Date.now(),
            isOptimistic: isOptimistic
        };
        this.dataCache.set(key, entry);
    }

    /**
     * Get cached data
     */
    getCachedData(key) {
        return this.dataCache.get(key);
    }

    /**
     * Check if cache entry is valid
     */
    isCacheValid(key) {
        const cached = this.getCachedData(key);
        if (!cached) return false;

        const age = Date.now() - cached.timestamp;
        return age < this.cacheTimeout;
    }

    /**
     * Clean up expired cache entries
     */
    cleanupExpiredCache() {
        const expiredKeys = [];
        const now = Date.now();

        for (const [key, entry] of this.dataCache) {
            const age = now - entry.timestamp;
            if (age > this.cacheTimeout) {
                expiredKeys.push(key);
            }
        }

        expiredKeys.forEach(key => this.dataCache.delete(key));

        if (expiredKeys.length > 0) {
            console.log(`🧹 Cleaned up ${expiredKeys.length} expired cache entries`);
        }
    }

    /**
     * Clear all cache
     */
    clearCache() {
        const size = this.dataCache.size;
        this.dataCache.clear();
        console.log(`🗑️ Cleared ${size} cache entries`);
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.dataCache.size,
            entries: Array.from(this.dataCache.keys())
        };
    }
}

// ================================
// GLOBAL CACHE MANAGER INSTANCE
// ================================

/**
 * Global cache manager instance
 */
const dashboardCacheManager = new DashboardCacheManager();

// ================================
// CACHE MANAGER API FUNCTIONS
// ================================

/**
 * Cache data
 */
export function cacheDashboardData(key, data, isOptimistic = false) {
    dashboardCacheManager.cacheData(key, data, isOptimistic);
}

/**
 * Get cached data
 */
export function getCachedDashboardData(key) {
    return dashboardCacheManager.getCachedData(key);
}

/**
 * Check cache validity
 */
export function isDashboardCacheValid(key) {
    return dashboardCacheManager.isCacheValid(key);
}

/**
 * Clean up expired cache
 */
export function cleanupExpiredDashboardCache() {
    dashboardCacheManager.cleanupExpiredCache();
}

/**
 * Clear data cache
 */
export function clearDashboardDataCache() {
    dashboardCacheManager.clearCache();
}

/**
 * Get cache statistics
 */
export function getDashboardCacheStats() {
    return dashboardCacheManager.getCacheStats();
}

// ================================
// EXPORTS
// ================================

export { DashboardCacheManager, dashboardCacheManager };
export default dashboardCacheManager;






