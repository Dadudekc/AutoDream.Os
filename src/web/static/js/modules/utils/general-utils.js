/**
 * General Utils - V2 Compliant General Utility System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: general utility functions from various files
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified general utilities with helpers, formatters, and common functions
 */

// ================================
// GENERAL UTILS CLASS
// ================================

/**
 * Unified General Utilities
 * Consolidates all general utility functionality
 */
export class GeneralUtils {
    constructor(options = {}) {
        this.isInitialized = false;
        this.cache = new Map();
        this.config = {
            enableCaching: true,
            cacheTimeout: 300000, // 5 minutes
            enablePerformanceMonitoring: true,
            ...options
        };
    }

    /**
     * Initialize general utilities
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ General utils already initialized');
            return;
        }

        console.log('🚀 Initializing General Utils (V2 Compliant)...');

        try {
            // Setup utility event listeners
            this.setupUtilityEventListeners();

            // Initialize cache cleanup
            this.startCacheCleanup();

            this.isInitialized = true;
            console.log('✅ General Utils initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize general utils:', error);
            throw error;
        }
    }

    /**
     * Setup utility event listeners
     */
    setupUtilityEventListeners() {
        // Listen for utility requests
        window.addEventListener('utils:format', (event) => {
            this.handleFormatRequest(event.detail);
        });

        // Listen for cache requests
        window.addEventListener('utils:cache', (event) => {
            this.handleCacheRequest(event.detail);
        });
    }

    /**
     * Format number with locale
     */
    formatNumber(number, options = {}) {
        try {
            const defaultOptions = {
                locale: 'en-US',
                minimumFractionDigits: 0,
                maximumFractionDigits: 2,
                ...options
            };

            return new Intl.NumberFormat(defaultOptions.locale, defaultOptions).format(number);
        } catch (error) {
            console.error('❌ Number formatting failed:', error);
            return number.toString();
        }
    }

    /**
     * Format currency
     */
    formatCurrency(amount, currency = 'USD', options = {}) {
        try {
            const defaultOptions = {
                locale: 'en-US',
                style: 'currency',
                currency,
                ...options
            };

            return new Intl.NumberFormat(defaultOptions.locale, defaultOptions).format(amount);
        } catch (error) {
            console.error('❌ Currency formatting failed:', error);
            return `${currency} ${amount}`;
        }
    }

    /**
     * Format percentage
     */
    formatPercentage(value, options = {}) {
        try {
            const defaultOptions = {
                locale: 'en-US',
                style: 'percent',
                minimumFractionDigits: 0,
                maximumFractionDigits: 2,
                ...options
            };

            return new Intl.NumberFormat(defaultOptions.locale, defaultOptions).format(value / 100);
        } catch (error) {
            console.error('❌ Percentage formatting failed:', error);
            return `${value}%`;
        }
    }

    /**
     * Format file size
     */
    formatFileSize(bytes, options = {}) {
        try {
            if (bytes === 0) return '0 Bytes';

            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));

            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        } catch (error) {
            console.error('❌ File size formatting failed:', error);
            return `${bytes} bytes`;
        }
    }

    /**
     * Generate unique ID
     */
    generateId(prefix = 'id') {
        return `${prefix}_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Generate UUID
     */
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Deep clone object
     */
    deepClone(obj) {
        try {
            if (obj === null || typeof obj !== 'object') {
                return obj;
            }

            if (obj instanceof Date) {
                return new Date(obj.getTime());
            }

            if (obj instanceof Array) {
                return obj.map(item => this.deepClone(item));
            }

            if (typeof obj === 'object') {
                const cloned = {};
                for (const key in obj) {
                    if (obj.hasOwnProperty(key)) {
                        cloned[key] = this.deepClone(obj[key]);
                    }
                }
                return cloned;
            }

            return obj;
        } catch (error) {
            console.error('❌ Deep clone failed:', error);
            return obj;
        }
    }

    /**
     * Merge objects
     */
    mergeObjects(target, ...sources) {
        try {
            if (!sources.length) return target;
            const source = sources.shift();

            if (this.isObject(target) && this.isObject(source)) {
                for (const key in source) {
                    if (this.isObject(source[key])) {
                        if (!target[key]) Object.assign(target, { [key]: {} });
                        this.mergeObjects(target[key], source[key]);
                    } else {
                        Object.assign(target, { [key]: source[key] });
                    }
                }
            }

            return this.mergeObjects(target, ...sources);
        } catch (error) {
            console.error('❌ Object merge failed:', error);
            return target;
        }
    }

    /**
     * Check if value is object
     */
    isObject(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    }

    /**
     * Debounce function
     */
    debounce(func, wait, immediate = false) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    }

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Sleep function
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Retry function
     */
    async retry(fn, maxAttempts = 3, delay = 1000) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return await fn();
            } catch (error) {
                if (attempt === maxAttempts) {
                    throw error;
                }
                await this.sleep(delay * attempt);
            }
        }
    }

    /**
     * Handle format request
     */
    handleFormatRequest(data) {
        const { type, value, options, callback } = data;
        let result;

        switch (type) {
            case 'number':
                result = this.formatNumber(value, options);
                break;
            case 'currency':
                result = this.formatCurrency(value, options.currency, options);
                break;
            case 'percentage':
                result = this.formatPercentage(value, options);
                break;
            case 'fileSize':
                result = this.formatFileSize(value, options);
                break;
            default:
                result = value;
        }

        if (callback) {
            callback(result);
        }

        return result;
    }

    /**
     * Handle cache request
     */
    handleCacheRequest(data) {
        const { action, key, value, callback } = data;
        let result;

        switch (action) {
            case 'get':
                result = this.getCached(key);
                break;
            case 'set':
                result = this.setCached(key, value);
                break;
            case 'delete':
                result = this.deleteCached(key);
                break;
            case 'clear':
                result = this.clearCache();
                break;
            default:
                result = null;
        }

        if (callback) {
            callback(result);
        }

        return result;
    }

    /**
     * Set cached value
     */
    setCached(key, value) {
        if (!this.config.enableCaching) return false;

        this.cache.set(key, {
            value,
            timestamp: Date.now()
        });

        return true;
    }

    /**
     * Get cached value
     */
    getCached(key) {
        if (!this.config.enableCaching) return null;

        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < this.config.cacheTimeout) {
            return cached.value;
        }

        this.cache.delete(key);
        return null;
    }

    /**
     * Delete cached value
     */
    deleteCached(key) {
        return this.cache.delete(key);
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
        return true;
    }

    /**
     * Start cache cleanup
     */
    startCacheCleanup() {
        if (!this.config.enableCaching) return;

        setInterval(() => {
            this.cleanupExpiredCache();
        }, 60000); // Cleanup every minute
    }

    /**
     * Cleanup expired cache
     */
    cleanupExpiredCache() {
        const now = Date.now();
        for (const [key, cached] of this.cache) {
            if (now - cached.timestamp >= this.config.cacheTimeout) {
                this.cache.delete(key);
            }
        }
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            size: this.cache.size,
            entries: Array.from(this.cache.entries()).map(([key, value]) => ({
                key,
                age: Date.now() - value.timestamp
            }))
        };
    }

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            cacheSize: this.cache.size,
            config: { ...this.config }
        };
    }

    /**
     * Destroy general utils
     */
    async destroy() {
        console.log('🧹 Destroying general utils...');

        this.cache.clear();
        this.isInitialized = false;

        console.log('✅ General utils destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create general utils with default configuration
 */
export function createGeneralUtils(options = {}) {
    return new GeneralUtils(options);
}

// Export default
export default GeneralUtils;