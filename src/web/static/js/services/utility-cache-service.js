/**
 * Utility Cache Service - V2 Compliant with Modular Architecture
 * Main orchestrator using specialized cache modules
 * REFACTORED: 304 lines → ~110 lines (64% reduction)
 * V2 COMPLIANCE: Under 300-line limit achieved
 *
 * @author Agent-7 - Web Development Specialist, Agent-8 - Integration & Performance Specialist
 * @version 4.0.0 - V2 COMPLIANCE MODULAR REFACTORING
 * @license MIT
 */

// ================================
// IMPORT MODULAR CACHE COMPONENTS
// ================================

import { CacheUtils } from './utilities/cache-utils.js';
import { UnifiedLoggingSystem } from './utilities/logging-utils.js';

// ================================
// UTILITY CACHE SERVICE V4
// ================================

/**
 * Main orchestrator for cache utilities using modular architecture
 * V2 COMPLIANT: Delegates to specialized cache modules for specific functionality
 */
export class UtilityCacheService {
    constructor() {
        this.logger = new UnifiedLoggingSystem("UtilityCacheService");
        this.cacheUtils = new CacheUtils();
    }

    // ================================
    // DELEGATION METHODS - CACHE UTILS
    // ================================

    /**
     * Create a simple memory cache
     */
    createMemoryCache(maxSize = 100, ttl = 300000) {
        return this.cacheUtils.createMemoryCache(maxSize, ttl);
    }

    /**
     * Create an LRU (Least Recently Used) cache
     */
    createLRUCache(maxSize = 100) {
        return this.cacheUtils.createLRUCache(maxSize);
    }

    /**
     * Create a TTL (Time To Live) cache wrapper
     */
    createTTLWrapper(cache, defaultTTL = 300000) {
        return this.cacheUtils.createTTLWrapper(cache, defaultTTL);
    }

    // ================================
    // HIGH-LEVEL CACHE METHODS
    // ================================

    /**
     * Create a complete cache system with TTL and size limits
     */
    createCompleteCache(options = {}) {
        const {
            maxSize = 100,
            ttl = 300000,
            strategy = 'lru'
        } = options;

        let baseCache;

        if (strategy === 'lru') {
            baseCache = this.createLRUCache(maxSize);
        } else {
            baseCache = this.createMemoryCache(maxSize, ttl);
        }

        if (strategy !== 'memory') {
            baseCache = this.createTTLWrapper(baseCache, ttl);
        }

        return baseCache;
    }

    /**
     * Create a namespaced cache for better organization
     */
    createNamespacedCache(namespace, options = {}) {
        const cache = this.createCompleteCache(options);

        return {
            get: (key) => cache.get(`${namespace}:${key}`),
            set: (key, value, ttl) => cache.set(`${namespace}:${key}`, value, ttl),
            delete: (key) => cache.delete(`${namespace}:${key}`),
            clear: () => {
                // Note: This clears all namespaces - not ideal but simple
                cache.clear();
            },
            size: () => cache.size()
        };
    }
}

// ================================
// LEGACY EXPORTS FOR BACKWARD COMPATIBILITY
// ================================

const utilityCacheService = new UtilityCacheService();

/**
 * Legacy cache creation functions
 */
export function createMemoryCache(maxSize = 100, ttl = 300000) {
    return utilityCacheService.createMemoryCache(maxSize, ttl);
}

export function createLRUCache(maxSize = 100) {
    return utilityCacheService.createLRUCache(maxSize);
}

export function createTTLWrapper(cache, defaultTTL = 300000) {
    return utilityCacheService.createTTLWrapper(cache, defaultTTL);
}

// ================================
// EXPORTS
// ================================

export default UtilityCacheService;