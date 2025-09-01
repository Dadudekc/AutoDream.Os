/**
 * Utility Cache Service - V2 Compliant
 * Caching utilities extracted from utility-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// UTILITY CACHE SERVICE
// ================================

/**
 * Caching utility functions
 */
class UtilityCacheService {
    constructor() {
        this.cache = new Map();
        this.config = {
            cacheTimeout: 30000, // 30 seconds
            maxCacheSize: 1000,
            enableLogging: true
        };
        this.logger = console;
    }

    /**
     * Get cached value
     */
    getCached(key) {
        try {
            const cached = this.cache.get(key);

            if (cached && Date.now() - cached.timestamp < this.config.cacheTimeout) {
                if (this.config.enableLogging) {
                    this.logger.debug(`Cache hit for key: ${key}`);
                }
                return cached.data;
            }

            // Remove expired entry
            if (cached) {
                this.cache.delete(key);
                if (this.config.enableLogging) {
                    this.logger.debug(`Expired cache entry removed: ${key}`);
                }
            }

            return null;
        } catch (error) {
            this.logError('Cache retrieval failed', error);
            return null;
        }
    }

    /**
     * Set cached value
     */
    setCached(key, data) {
        try {
            // Check cache size limit
            if (this.cache.size >= this.config.maxCacheSize) {
                this.clearOldestCache();
            }

            this.cache.set(key, {
                data: data,
                timestamp: Date.now()
            });

            if (this.config.enableLogging) {
                this.logger.debug(`Cache set for key: ${key}`);
            }
        } catch (error) {
            this.logError('Cache storage failed', error);
        }
    }

    /**
     * Clear all cache
     */
    clearCache() {
        try {
            const size = this.cache.size;
            this.cache.clear();

            if (this.config.enableLogging) {
                this.logger.info(`Cache cleared: ${size} entries removed`);
            }
        } catch (error) {
            this.logError('Cache clearing failed', error);
        }
    }

    /**
     * Clear expired cache entries
     */
    clearExpiredCache() {
        try {
            const now = Date.now();
            const expiredKeys = [];

            for (const [key, value] of this.cache.entries()) {
                if (now - value.timestamp >= this.config.cacheTimeout) {
                    expiredKeys.push(key);
                }
            }

            expiredKeys.forEach(key => this.cache.delete(key));

            if (this.config.enableLogging && expiredKeys.length > 0) {
                this.logger.debug(`Cleared ${expiredKeys.length} expired cache entries`);
            }

            return expiredKeys.length;
        } catch (error) {
            this.logError('Expired cache clearing failed', error);
            return 0;
        }
    }

    /**
     * Clear oldest cache entry
     */
    clearOldestCache() {
        try {
            let oldestKey = null;
            let oldestTime = Date.now();

            for (const [key, value] of this.cache.entries()) {
                if (value.timestamp < oldestTime) {
                    oldestTime = value.timestamp;
                    oldestKey = key;
                }
            }

            if (oldestKey) {
                this.cache.delete(oldestKey);
                if (this.config.enableLogging) {
                    this.logger.debug(`Removed oldest cache entry: ${oldestKey}`);
                }
            }
        } catch (error) {
            this.logError('Oldest cache clearing failed', error);
        }
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        try {
            const now = Date.now();
            const stats = {
                totalEntries: this.cache.size,
                maxSize: this.config.maxCacheSize,
                timeout: this.config.cacheTimeout,
                expiredEntries: 0,
                activeEntries: 0
            };

            for (const [key, value] of this.cache.entries()) {
                if (now - value.timestamp >= this.config.cacheTimeout) {
                    stats.expiredEntries++;
                } else {
                    stats.activeEntries++;
                }
            }

            return stats;
        } catch (error) {
            this.logError('Cache stats retrieval failed', error);
            return {
                totalEntries: 0,
                maxSize: this.config.maxCacheSize,
                timeout: this.config.cacheTimeout,
                expiredEntries: 0,
                activeEntries: 0
            };
        }
    }

    /**
     * Has cached value
     */
    hasCached(key) {
        try {
            const cached = this.cache.get(key);
            return cached && Date.now() - cached.timestamp < this.config.cacheTimeout;
        } catch (error) {
            this.logError('Cache check failed', error);
            return false;
        }
    }

    /**
     * Remove specific cache entry
     */
    removeCached(key) {
        try {
            const existed = this.cache.delete(key);
            if (this.config.enableLogging) {
                this.logger.debug(`Cache entry removed: ${key} (existed: ${existed})`);
            }
            return existed;
        } catch (error) {
            this.logError('Cache removal failed', error);
            return false;
        }
    }

    /**
     * Update cache configuration
     */
    updateConfig(newConfig) {
        try {
            this.config = { ...this.config, ...newConfig };

            if (this.config.enableLogging) {
                this.logger.info('Cache configuration updated');
            }
        } catch (error) {
            this.logError('Cache configuration update failed', error);
        }
    }

    /**
     * Get cache configuration
     */
    getConfig() {
        return { ...this.config };
    }

    /**
     * Log error
     */
    logError(message, error) {
        this.logger.error(`[UtilityCacheService] ${message}:`, error);
    }
}

// ================================
// GLOBAL CACHE SERVICE INSTANCE
// ================================

/**
 * Global utility cache service instance
 */
const utilityCacheService = new UtilityCacheService();

// ================================
// CACHE SERVICE API FUNCTIONS
// ================================

/**
 * Get cached value
 */
export function getCached(key) {
    return utilityCacheService.getCached(key);
}

/**
 * Set cached value
 */
export function setCached(key, data) {
    utilityCacheService.setCached(key, data);
}

/**
 * Clear all cache
 */
export function clearCache() {
    utilityCacheService.clearCache();
}

/**
 * Get cache statistics
 */
export function getCacheStats() {
    return utilityCacheService.getCacheStats();
}

/**
 * Has cached value
 */
export function hasCached(key) {
    return utilityCacheService.hasCached(key);
}

/**
 * Remove cached value
 */
export function removeCached(key) {
    return utilityCacheService.removeCached(key);
}

// ================================
// EXPORTS
// ================================

export { UtilityCacheService, utilityCacheService };
export default utilityCacheService;
