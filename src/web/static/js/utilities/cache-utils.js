/**
 * Cache Utilities Module - V2 Compliant
 * Intelligent caching with TTL and size management
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class CacheUtils {
    constructor(options = {}) {
        this.cache = new Map();
        this.logger = options.logger || console;
        this.config = {
            defaultTimeout: options.defaultTimeout || 30000, // 30 seconds
            maxSize: options.maxSize || 1000,
            enableStats: options.enableStats || true,
            ...options
        };
        this.stats = {
            hits: 0,
            misses: 0,
            evictions: 0,
            sets: 0
        };
    }

    /**
     * Set cache entry with optional TTL
     */
    set(key, value, ttl = null) {
        try {
            // Check cache size limit
            if (this.cache.size >= this.config.maxSize) {
                this.evictOldest();
            }

            const timeout = ttl || this.config.defaultTimeout;
            const entry = {
                value,
                timestamp: Date.now(),
                ttl: timeout,
                expires: Date.now() + timeout
            };

            this.cache.set(key, entry);
            this.stats.sets++;

            if (this.config.enableStats) {
                this.logger.debug(`Cache set: ${key}, expires: ${new Date(entry.expires).toISOString()}`);
            }

            return true;
        } catch (error) {
            this.logger.error('Cache set failed', error);
            return false;
        }
    }

    /**
     * Get cache entry with TTL validation
     */
    get(key) {
        try {
            const entry = this.cache.get(key);

            if (!entry) {
                this.stats.misses++;
                return null;
            }

            // Check if entry has expired
            if (Date.now() > entry.expires) {
                this.cache.delete(key);
                this.stats.misses++;
                this.stats.evictions++;
                return null;
            }

            this.stats.hits++;
            return entry.value;
        } catch (error) {
            this.logger.error('Cache get failed', error);
            return null;
        }
    }

    /**
     * Delete cache entry
     */
    delete(key) {
        try {
            const deleted = this.cache.delete(key);
            if (deleted && this.config.enableStats) {
                this.logger.debug(`Cache deleted: ${key}`);
            }
            return deleted;
        } catch (error) {
            this.logger.error('Cache delete failed', error);
            return false;
        }
    }

    /**
     * Clear entire cache
     */
    clear() {
        try {
            const size = this.cache.size;
            this.cache.clear();
            this.resetStats();
            if (this.config.enableStats) {
                this.logger.debug(`Cache cleared: ${size} entries removed`);
            }
            return true;
        } catch (error) {
            this.logger.error('Cache clear failed', error);
            return false;
        }
    }

    /**
     * Check if key exists and is not expired
     */
    has(key) {
        try {
            const entry = this.cache.get(key);
            if (!entry) return false;

            if (Date.now() > entry.expires) {
                this.cache.delete(key);
                this.stats.evictions++;
                return false;
            }

            return true;
        } catch (error) {
            this.logger.error('Cache has check failed', error);
            return false;
        }
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
        const total = this.stats.hits + this.stats.misses;
        const hitRate = total > 0 ? (this.stats.hits / total * 100).toFixed(2) : 0;

        return {
            ...this.stats,
            size: this.cache.size,
            hitRate: `${hitRate}%`,
            maxSize: this.config.maxSize
        };
    }

    /**
     * Clean expired entries
     */
    clean() {
        try {
            const now = Date.now();
            let cleaned = 0;

            for (const [key, entry] of this.cache.entries()) {
                if (now > entry.expires) {
                    this.cache.delete(key);
                    cleaned++;
                    this.stats.evictions++;
                }
            }

            if (this.config.enableStats && cleaned > 0) {
                this.logger.debug(`Cache cleaned: ${cleaned} expired entries removed`);
            }

            return cleaned;
        } catch (error) {
            this.logger.error('Cache clean failed', error);
            return 0;
        }
    }

    /**
     * Evict oldest entry (LRU-style)
     */
    evictOldest() {
        try {
            let oldestKey = null;
            let oldestTime = Date.now();

            for (const [key, entry] of this.cache.entries()) {
                if (entry.timestamp < oldestTime) {
                    oldestTime = entry.timestamp;
                    oldestKey = key;
                }
            }

            if (oldestKey) {
                this.cache.delete(oldestKey);
                this.stats.evictions++;
                if (this.config.enableStats) {
                    this.logger.debug(`Cache eviction: ${oldestKey} (oldest entry)`);
                }
            }
        } catch (error) {
            this.logger.error('Cache eviction failed', error);
        }
    }

    /**
     * Reset statistics
     */
    resetStats() {
        this.stats = {
            hits: 0,
            misses: 0,
            evictions: 0,
            sets: 0
        };
    }

    /**
     * Set cache configuration
     */
    setConfig(options = {}) {
        this.config = { ...this.config, ...options };
    }
}

// Factory function for creating cache utils instance
export function createCacheUtils(options = {}) {
    return new CacheUtils(options);
}
