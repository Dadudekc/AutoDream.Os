/**
 * Cache Utilities - V2 Compliant Module
 * ====================================
 * 
 * Caching utilities with LRU eviction and performance optimization.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class CacheUtils {
    constructor(maxSize = 1000) {
        this.maxSize = maxSize;
        this.cache = new Map();
        this.accessOrder = new Map();
        this.logger = console;
    }

    /**
     * Set cache entry
     */
    set(key, value, ttl = null) {
        // Remove oldest entries if cache is full
        if (this.cache.size >= this.maxSize) {
            this.evictOldest();
        }

        const entry = {
            value,
            ttl,
            createdAt: Date.now()
        };

        this.cache.set(key, entry);
        this.updateAccessOrder(key);
    }

    /**
     * Get cache entry
     */
    get(key) {
        const entry = this.cache.get(key);
        
        if (!entry) {
            return null;
        }

        // Check TTL
        if (entry.ttl && Date.now() - entry.createdAt > entry.ttl) {
            this.delete(key);
            return null;
        }

        this.updateAccessOrder(key);
        return entry.value;
    }

    /**
     * Check if key exists in cache
     */
    has(key) {
        return this.get(key) !== null;
    }

    /**
     * Delete cache entry
     */
    delete(key) {
        this.cache.delete(key);
        this.accessOrder.delete(key);
    }

    /**
     * Clear all cache entries
     */
    clear() {
        this.cache.clear();
        this.accessOrder.clear();
        this.logger.log('🧹 Cache cleared');
    }

    /**
     * Get cache size
     */
    size() {
        return this.cache.size;
    }

    /**
     * Get cache statistics
     */
    getStats() {
        const now = Date.now();
        let expiredCount = 0;
        let totalAge = 0;

        for (const [key, entry] of this.cache.entries()) {
            if (entry.ttl && now - entry.createdAt > entry.ttl) {
                expiredCount++;
            }
            totalAge += now - entry.createdAt;
        }

        return {
            size: this.cache.size,
            maxSize: this.maxSize,
            utilization: (this.cache.size / this.maxSize) * 100,
            expiredCount,
            averageAge: this.cache.size > 0 ? totalAge / this.cache.size : 0
        };
    }

    /**
     * Update access order for LRU
     */
    updateAccessOrder(key) {
        this.accessOrder.set(key, Date.now());
    }

    /**
     * Evict oldest entry
     */
    evictOldest() {
        let oldestKey = null;
        let oldestTime = Infinity;

        for (const [key, time] of this.accessOrder.entries()) {
            if (time < oldestTime) {
                oldestTime = time;
                oldestKey = key;
            }
        }

        if (oldestKey) {
            this.delete(oldestKey);
        }
    }

    /**
     * Clean expired entries
     */
    cleanExpired() {
        const now = Date.now();
        const expiredKeys = [];

        for (const [key, entry] of this.cache.entries()) {
            if (entry.ttl && now - entry.createdAt > entry.ttl) {
                expiredKeys.push(key);
            }
        }

        expiredKeys.forEach(key => this.delete(key));
        
        if (expiredKeys.length > 0) {
            this.logger.log(`🧹 Cleaned ${expiredKeys.length} expired cache entries`);
        }
    }

    /**
     * Get all cache keys
     */
    keys() {
        return Array.from(this.cache.keys());
    }

    /**
     * Get all cache values
     */
    values() {
        return Array.from(this.cache.values()).map(entry => entry.value);
    }

    /**
     * Get all cache entries
     */
    entries() {
        const result = [];
        for (const [key, entry] of this.cache.entries()) {
            result.push([key, entry.value]);
        }
        return result;
    }

    /**
     * Set multiple entries
     */
    setMultiple(entries, ttl = null) {
        entries.forEach(([key, value]) => {
            this.set(key, value, ttl);
        });
    }

    /**
     * Get multiple entries
     */
    getMultiple(keys) {
        const result = {};
        keys.forEach(key => {
            const value = this.get(key);
            if (value !== null) {
                result[key] = value;
            }
        });
        return result;
    }

    /**
     * Delete multiple entries
     */
    deleteMultiple(keys) {
        keys.forEach(key => this.delete(key));
    }

    /**
     * Export cache data
     */
    export() {
        const data = {};
        for (const [key, entry] of this.cache.entries()) {
            data[key] = {
                value: entry.value,
                ttl: entry.ttl,
                createdAt: entry.createdAt
            };
        }
        return data;
    }

    /**
     * Import cache data
     */
    import(data) {
        this.clear();
        Object.entries(data).forEach(([key, entry]) => {
            this.cache.set(key, entry);
            this.updateAccessOrder(key);
        });
    }
}