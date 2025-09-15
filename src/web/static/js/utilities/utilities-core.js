/**
 * Utilities Core Module - V2 Compliant
 * Core utility functions extracted from utilities-consolidated.js
 * V2 Compliance: ≤400 lines for compliance
 *
 * @author Agent-7 - Web Development Specialist
 * @version 3.0.0 - V2 COMPLIANCE REFACTORED
 * @license MIT
 */

/**
 * Core Utilities Module
 * V2 Compliance: Extracted from monolithic 1263-line file
 */
export class UtilitiesCore {
    constructor(options = {}) {
        this.logger = console;
        this.isInitialized = false;

        // Core utility components
        this.arrayUtils = null;
        this.domUtils = null;
        this.loggingUtils = null;
        this.stringUtils = null;
        this.timeUtils = null;
        this.validationUtils = null;

        // Configuration
        this.config = {
            enableCaching: true,
            enableLogging: true,
            cacheSize: 1000,
            logLevel: 'info',
            ...options
        };

        // Caches
        this.cache = new Map();
        this.domCache = new Map();
        this.stringCache = new Map();
    }

    /**
     * Initialize the core utilities system
     */
    async initialize() {
        if (this.isInitialized) {
            return this;
        }

        try {
            // Initialize core components
            this.arrayUtils = new ArrayUtils();
            this.domUtils = new DOMUtils();
            this.loggingUtils = new LoggingUtils(this.config);
            this.stringUtils = new StringUtils();
            this.timeUtils = new TimeUtils();
            this.validationUtils = new ValidationUtils();

            this.isInitialized = true;
            this.logger.log('✅ Utilities Core initialized successfully');
            return this;
        } catch (error) {
            this.logger.error('❌ Failed to initialize Utilities Core:', error);
            throw error;
        }
    }

    /**
     * Get array utilities
     */
    getArrayUtils() {
        return this.arrayUtils;
    }

    /**
     * Get DOM utilities
     */
    getDOMUtils() {
        return this.domUtils;
    }

    /**
     * Get logging utilities
     */
    getLoggingUtils() {
        return this.loggingUtils;
    }

    /**
     * Get string utilities
     */
    getStringUtils() {
        return this.stringUtils;
    }

    /**
     * Get time utilities
     */
    getTimeUtils() {
        return this.timeUtils;
    }

    /**
     * Get validation utilities
     */
    getValidationUtils() {
        return this.validationUtils;
    }

    /**
     * Clear all caches
     */
    clearCaches() {
        this.cache.clear();
        this.domCache.clear();
        this.stringCache.clear();
        this.logger.log('🧹 All caches cleared');
    }

    /**
     * Get cache statistics
     */
    getCacheStats() {
        return {
            cache: this.cache.size,
            domCache: this.domCache.size,
            stringCache: this.stringCache.size,
            total: this.cache.size + this.domCache.size + this.stringCache.size
        };
    }
}

/**
 * Array Utilities Class
 */
class ArrayUtils {
    constructor() {
        this.name = 'ArrayUtils';
    }

    /**
     * Remove duplicates from array
     */
    unique(array) {
        return [...new Set(array)];
    }

    /**
     * Chunk array into smaller arrays
     */
    chunk(array, size) {
        const chunks = [];
        for (let i = 0; i < array.length; i += size) {
            chunks.push(array.slice(i, i + size));
        }
        return chunks;
    }

    /**
     * Flatten nested arrays
     */
    flatten(array) {
        return array.reduce((flat, item) => {
            return flat.concat(Array.isArray(item) ? this.flatten(item) : item);
        }, []);
    }

    /**
     * Group array by key
     */
    groupBy(array, key) {
        return array.reduce((groups, item) => {
            const group = item[key];
            groups[group] = groups[group] || [];
            groups[group].push(item);
            return groups;
        }, {});
    }

    /**
     * Sort array by key
     */
    sortBy(array, key, direction = 'asc') {
        return array.sort((a, b) => {
            const aVal = a[key];
            const bVal = b[key];
            if (direction === 'desc') {
                return bVal > aVal ? 1 : -1;
            }
            return aVal > bVal ? 1 : -1;
        });
    }
}

/**
 * DOM Utilities Class
 */
class DOMUtils {
    constructor() {
        this.name = 'DOMUtils';
    }

    /**
     * Find element by selector
     */
    find(selector) {
        return document.querySelector(selector);
    }

    /**
     * Find all elements by selector
     */
    findAll(selector) {
        return document.querySelectorAll(selector);
    }

    /**
     * Create element with attributes
     */
    createElement(tag, attributes = {}, textContent = '') {
        const element = document.createElement(tag);
        
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
        
        if (textContent) {
            element.textContent = textContent;
        }
        
        return element;
    }

    /**
     * Add event listener with cleanup
     */
    addEventListener(element, event, handler, options = {}) {
        element.addEventListener(event, handler, options);
        return () => element.removeEventListener(event, handler, options);
    }

    /**
     * Toggle class on element
     */
    toggleClass(element, className) {
        element.classList.toggle(className);
        return element.classList.contains(className);
    }

    /**
     * Show/hide element
     */
    toggleVisibility(element, show = null) {
        if (show === null) {
            show = element.style.display === 'none';
        }
        element.style.display = show ? '' : 'none';
        return show;
    }
}

/**
 * Logging Utilities Class
 */
class LoggingUtils {
    constructor(config = {}) {
        this.config = config;
        this.logs = [];
        this.maxLogs = config.maxLogs || 1000;
    }

    /**
     * Log message with level
     */
    log(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            level,
            message,
            data
        };

        this.logs.push(logEntry);
        
        // Keep only recent logs
        if (this.logs.length > this.maxLogs) {
            this.logs = this.logs.slice(-this.maxLogs);
        }

        // Console output based on level
        if (this.config.enableLogging) {
            switch (level) {
                case 'error':
                    console.error(`[${timestamp}] ${message}`, data);
                    break;
                case 'warn':
                    console.warn(`[${timestamp}] ${message}`, data);
                    break;
                case 'info':
                    console.info(`[${timestamp}] ${message}`, data);
                    break;
                default:
                    console.log(`[${timestamp}] ${message}`, data);
            }
        }
    }

    /**
     * Log error
     */
    error(message, data = null) {
        this.log('error', message, data);
    }

    /**
     * Log warning
     */
    warn(message, data = null) {
        this.log('warn', message, data);
    }

    /**
     * Log info
     */
    info(message, data = null) {
        this.log('info', message, data);
    }

    /**
     * Get recent logs
     */
    getLogs(level = null, limit = 100) {
        let filteredLogs = this.logs;
        
        if (level) {
            filteredLogs = this.logs.filter(log => log.level === level);
        }
        
        return filteredLogs.slice(-limit);
    }
}

/**
 * String Utilities Class
 */
class StringUtils {
    constructor() {
        this.name = 'StringUtils';
    }

    /**
     * Capitalize first letter
     */
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    /**
     * Convert to camelCase
     */
    toCamelCase(str) {
        return str.replace(/-([a-z])/g, (g) => g[1].toUpperCase());
    }

    /**
     * Convert to kebab-case
     */
    toKebabCase(str) {
        return str.replace(/([A-Z])/g, '-$1').toLowerCase();
    }

    /**
     * Truncate string with ellipsis
     */
    truncate(str, length, suffix = '...') {
        if (str.length <= length) {
            return str;
        }
        return str.substring(0, length - suffix.length) + suffix;
    }

    /**
     * Generate random string
     */
    random(length = 8) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }
}

/**
 * Time Utilities Class
 */
class TimeUtils {
    constructor() {
        this.name = 'TimeUtils';
    }

    /**
     * Format timestamp
     */
    formatTimestamp(timestamp, format = 'YYYY-MM-DD HH:mm:ss') {
        const date = new Date(timestamp);
        return format
            .replace('YYYY', date.getFullYear())
            .replace('MM', String(date.getMonth() + 1).padStart(2, '0'))
            .replace('DD', String(date.getDate()).padStart(2, '0'))
            .replace('HH', String(date.getHours()).padStart(2, '0'))
            .replace('mm', String(date.getMinutes()).padStart(2, '0'))
            .replace('ss', String(date.getSeconds()).padStart(2, '0'));
    }

    /**
     * Get time ago string
     */
    timeAgo(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);

        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return `${seconds} second${seconds > 1 ? 's' : ''} ago`;
    }

    /**
     * Debounce function
     */
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
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
}

/**
 * Validation Utilities Class
 */
class ValidationUtils {
    constructor() {
        this.name = 'ValidationUtils';
    }

    /**
     * Validate email
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate URL
     */
    isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    /**
     * Validate required fields
     */
    validateRequired(obj, requiredFields) {
        const missing = [];
        requiredFields.forEach(field => {
            if (!obj[field] || obj[field].toString().trim() === '') {
                missing.push(field);
            }
        });
        return {
            isValid: missing.length === 0,
            missingFields: missing
        };
    }

    /**
     * Sanitize HTML
     */
    sanitizeHTML(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    }
}

// Export default instance
export default new UtilitiesCore();
