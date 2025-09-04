/**
 * Cache Utilities - V2 Compliant Module
 * Caching functions and memory management utilities
 * MODULAR: ~95 lines (V2 compliant)
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE MODULAR EXTRACTION
 * @license MIT
 */

export class CacheUtils {
    constructor() {
        this.logger = new UnifiedLoggingSystem("CacheUtils");
    }

    /**
     * Create a simple memory cache
     */
    createMemoryCache(maxSize = 100, ttl = 300000) { // 5 minutes default TTL
        const cache = new Map();

        return {
            get: (key) => {
                const item = cache.get(key);
                if (!item) return null;

                if (Date.now() > item.expiry) {
                    cache.delete(key);
                    return null;
                }

                return item.value;
            },

            set: (key, value) => {
                if (cache.size >= maxSize) {
                    const firstKey = cache.keys().next().value;
                    cache.delete(firstKey);
                }

                cache.set(key, {
                    value: value,
                    expiry: Date.now() + ttl
                });
            },

            delete: (key) => cache.delete(key),
            clear: () => cache.clear(),
            size: () => cache.size
        };
    }

    /**
     * Create an LRU (Least Recently Used) cache
     */
    createLRUCache(maxSize = 100) {
        const cache = new Map();

        return {
            get: (key) => {
                const item = cache.get(key);
                if (item) {
                    // Move to end (most recently used)
                    cache.delete(key);
                    cache.set(key, item);
                    return item;
                }
                return undefined;
            },

            set: (key, value) => {
                if (cache.has(key)) {
                    cache.delete(key);
                } else if (cache.size >= maxSize) {
                    const firstKey = cache.keys().next().value;
                    cache.delete(firstKey);
                }

                cache.set(key, value);
            },

            delete: (key) => cache.delete(key),
            clear: () => cache.clear(),
            size: () => cache.size
        };
    }

    /**
     * Create a TTL (Time To Live) cache
     */
    createTTLWrapper(cache, defaultTTL = 300000) {
        const wrappedCache = new Map();

        return {
            get: (key) => {
                const item = wrappedCache.get(key);
                if (!item) return cache.get(key);

                if (Date.now() > item.expiry) {
                    wrappedCache.delete(key);
                    return undefined;
                }

                return cache.get(key);
            },

            set: (key, value, ttl = defaultTTL) => {
                cache.set(key, value);
                wrappedCache.set(key, {
                    expiry: Date.now() + ttl
                });
            },

            delete: (key) => {
                wrappedCache.delete(key);
                return cache.delete(key);
            },

            clear: () => {
                wrappedCache.clear();
                return cache.clear();
            },

            size: () => cache.size
        };
    }
}

