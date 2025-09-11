/**
 * Utilities Consolidated Module - V2 Compliant
 * Consolidates all utility functions into unified system
 * Combines array, DOM, logging, string, time, and general utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - PHASE 2 CONSOLIDATION
 * @license MIT
 */

// ================================
// UTILITIES CONSOLIDATION
// ================================

/**
 * Unified Utilities Module
 * Consolidates all utility functions into a single V2-compliant module
 */
export class UtilitiesConsolidated {
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
     * Initialize the consolidated utilities system
     */
    async initialize() {
        try {
            this.logger.log('🚀 Initializing Utilities Consolidated...');

            // Initialize core utility components
            this.initializeCoreUtils();

            // Setup caches
            this.setupCaches();

            this.isInitialized = true;
            this.logger.log('✅ Utilities Consolidated initialized successfully');

        } catch (error) {
            this.logger.error('❌ Utilities Consolidated initialization failed:', error);
            throw error;
        }
    }

    /**
     * Initialize core utility components
     */
    initializeCoreUtils() {
        // Array Utilities
        this.arrayUtils = new ArrayUtils(this.logger);

        // DOM Utilities
        this.domUtils = new DOMUtils(this.logger);

        // Logging Utilities
        this.loggingUtils = new LoggingUtils(this.logger, this.config.logLevel);

        // String Utilities
        this.stringUtils = new StringUtils(this.logger);

        // Time Utilities
        this.timeUtils = new TimeUtils(this.logger);

        // Validation Utilities
        this.validationUtils = new ValidationUtils(this.logger);
    }

    /**
     * Setup caching systems
     */
    setupCaches() {
        // Setup cleanup intervals
        setInterval(() => {
            this.cleanupCaches();
        }, 300000); // Clean every 5 minutes

        this.logger.log('Utility caches initialized');
    }

    // ================================
    // ARRAY UTILITIES
    // ================================

    /**
     * Chunk array into smaller arrays
     */
    chunkArray(array, size) {
        return this.arrayUtils.chunk(array, size);
    }

    /**
     * Remove duplicates from array
     */
    uniqueArray(array) {
        return this.arrayUtils.unique(array);
    }

    /**
     * Shuffle array elements
     */
    shuffleArray(array) {
        return this.arrayUtils.shuffle(array);
    }

    /**
     * Find intersection of arrays
     */
    intersectArrays(...arrays) {
        return this.arrayUtils.intersect(...arrays);
    }

    /**
     * Group array by key function
     */
    groupBy(array, keyFn) {
        return this.arrayUtils.groupBy(array, keyFn);
    }

    /**
     * Sort array by multiple criteria
     */
    sortBy(array, criteria) {
        return this.arrayUtils.sortBy(array, criteria);
    }

    // ================================
    // DOM UTILITIES
    // ================================

    /**
     * Unified element selection with caching
     */
    selectElement(selector, context = document) {
        return this.domUtils.select(selector, context);
    }

    /**
     * Create DOM element with attributes
     */
    createElement(tagName, attributes = {}, content = '') {
        return this.domUtils.create(tagName, attributes, content);
    }

    /**
     * Add event listener with cleanup tracking
     */
    addEvent(element, event, handler, options = {}) {
        return this.domUtils.addEvent(element, event, handler, options);
    }

    /**
     * Remove event listener
     */
    removeEvent(element, event, handler) {
        return this.domUtils.removeEvent(element, event, handler);
    }

    /**
     * Add CSS class
     */
    addClass(element, className) {
        return this.domUtils.addClass(element, className);
    }

    /**
     * Remove CSS class
     */
    removeClass(element, className) {
        return this.domUtils.removeClass(element, className);
    }

    /**
     * Toggle CSS class
     */
    toggleClass(element, className) {
        return this.domUtils.toggleClass(element, className);
    }

    /**
     * Check if element has class
     */
    hasClass(element, className) {
        return this.domUtils.hasClass(element, className);
    }

    /**
     * Get element dimensions
     */
    getDimensions(element) {
        return this.domUtils.getDimensions(element);
    }

    /**
     * Check if element is in viewport
     */
    isInViewport(element) {
        return this.domUtils.isInViewport(element);
    }

    /**
     * Animate element
     */
    animate(element, properties, duration = 300, easing = 'ease') {
        return this.domUtils.animate(element, properties, duration, easing);
    }

    // ================================
    // STRING UTILITIES
    // ================================

    /**
     * Capitalize first letter
     */
    capitalize(str) {
        return this.stringUtils.capitalize(str);
    }

    /**
     * Convert to camelCase
     */
    camelCase(str) {
        return this.stringUtils.camelCase(str);
    }

    /**
     * Convert to kebab-case
     */
    kebabCase(str) {
        return this.stringUtils.kebabCase(str);
    }

    /**
     * Convert to snake_case
     */
    snakeCase(str) {
        return this.stringUtils.snakeCase(str);
    }

    /**
     * Truncate string with ellipsis
     */
    truncate(str, length, suffix = '...') {
        return this.stringUtils.truncate(str, length, suffix);
    }

    /**
     * Remove HTML tags from string
     */
    stripHtml(str) {
        return this.stringUtils.stripHtml(str);
    }

    /**
     * Escape HTML entities
     */
    escapeHtml(str) {
        return this.stringUtils.escapeHtml(str);
    }

    /**
     * Generate random string
     */
    randomString(length = 8) {
        return this.stringUtils.random(length);
    }

    /**
     * Format string template
     */
    format(template, ...args) {
        return this.stringUtils.format(template, ...args);
    }

    // ================================
    // TIME UTILITIES
    // ================================

    /**
     * Format timestamp
     */
    formatTimestamp(timestamp, format = 'YYYY-MM-DD HH:mm:ss') {
        return this.timeUtils.format(timestamp, format);
    }

    /**
     * Get relative time (e.g., "2 hours ago")
     */
    relativeTime(timestamp) {
        return this.timeUtils.relative(timestamp);
    }

    /**
     * Add time duration
     */
    addTime(date, amount, unit) {
        return this.timeUtils.add(date, amount, unit);
    }

    /**
     * Subtract time duration
     */
    subtractTime(date, amount, unit) {
        return this.timeUtils.subtract(date, amount, unit);
    }

    /**
     * Get difference between dates
     */
    timeDifference(date1, date2, unit = 'milliseconds') {
        return this.timeUtils.diff(date1, date2, unit);
    }

    /**
     * Check if date is valid
     */
    isValidDate(date) {
        return this.timeUtils.isValid(date);
    }

    /**
     * Parse date string
     */
    parseDate(dateString, format) {
        return this.timeUtils.parse(dateString, format);
    }

    // ================================
    // LOGGING UTILITIES
    // ================================

    /**
     * Log info message
     */
    logInfo(message, context = {}) {
        this.loggingUtils.info(message, context);
    }

    /**
     * Log warning message
     */
    logWarning(message, context = {}) {
        this.loggingUtils.warn(message, context);
    }

    /**
     * Log error message
     */
    logError(message, context = {}) {
        this.loggingUtils.error(message, context);
    }

    /**
     * Log debug message
     */
    logDebug(message, context = {}) {
        this.loggingUtils.debug(message, context);
    }

    /**
     * Start performance timer
     */
    startTimer(label) {
        return this.loggingUtils.startTimer(label);
    }

    /**
     * End performance timer
     */
    endTimer(label) {
        return this.loggingUtils.endTimer(label);
    }

    /**
     * Create child logger
     */
    createLogger(name) {
        return this.loggingUtils.createChild(name);
    }

    // ================================
    // VALIDATION UTILITIES
    // ================================

    /**
     * Validate email address
     */
    isValidEmail(email) {
        return this.validationUtils.email(email);
    }

    /**
     * Validate URL
     */
    isValidUrl(url) {
        return this.validationUtils.url(url);
    }

    /**
     * Validate phone number
     */
    isValidPhone(phone) {
        return this.validationUtils.phone(phone);
    }

    /**
     * Validate required field
     */
    isRequired(value) {
        return this.validationUtils.required(value);
    }

    /**
     * Validate string length
     */
    isValidLength(str, min = 0, max = Infinity) {
        return this.validationUtils.length(str, min, max);
    }

    /**
     * Validate number range
     */
    isValidRange(number, min = -Infinity, max = Infinity) {
        return this.validationUtils.range(number, min, max);
    }

    /**
     * Validate against pattern
     */
    matchesPattern(str, pattern) {
        return this.validationUtils.pattern(str, pattern);
    }

    /**
     * Run comprehensive validation
     */
    validate(data, rules) {
        return this.validationUtils.validate(data, rules);
    }

    // ================================
    // GENERAL UTILITIES
    // ================================

    /**
     * Deep clone object
     */
    deepClone(obj) {
        if (obj === null || typeof obj !== 'object') return obj;
        if (obj instanceof Date) return new Date(obj.getTime());
        if (obj instanceof Array) return obj.map(item => this.deepClone(item));

        const cloned = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                cloned[key] = this.deepClone(obj[key]);
            }
        }
        return cloned;
    }

    /**
     * Debounce function
     */
    debounce(func, wait, immediate = false) {
        let timeout;
        return (...args) => {
            const later = () => {
                timeout = null;
                if (!immediate) func.apply(this, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(this, args);
        };
    }

    /**
     * Throttle function
     */
    throttle(func, limit) {
        let inThrottle;
        return (...args) => {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Generate UUID
     */
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }

    /**
     * Sleep/delay function
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Retry function with exponential backoff
     */
    async retry(fn, maxAttempts = 3, baseDelay = 1000) {
        for (let attempt = 1; attempt <= maxAttempts; attempt++) {
            try {
                return await fn();
            } catch (error) {
                if (attempt === maxAttempts) {
                    throw error;
                }
                const delay = baseDelay * Math.pow(2, attempt - 1);
                await this.sleep(delay);
            }
        }
    }

    /**
     * Get cached value or compute and cache it
     */
    getCached(key, computeFn, ttl = 300000) { // 5 minutes default
        const cached = this.cache.get(key);
        if (cached && Date.now() - cached.timestamp < ttl) {
            return cached.value;
        }

        const value = computeFn();
        this.cache.set(key, {
            value,
            timestamp: Date.now()
        });

        return value;
    }

    /**
     * Cleanup expired cache entries
     */
    cleanupCaches() {
        const now = Date.now();
        const caches = [this.cache, this.domCache, this.stringCache];

        caches.forEach(cache => {
            const expiredKeys = [];
            for (const [key, value] of cache.entries()) {
                if (now - value.timestamp > 300000) { // 5 minutes
                    expiredKeys.push(key);
                }
            }
            expiredKeys.forEach(key => cache.delete(key));
        });

        if (this.cache.size > this.config.cacheSize) {
            // Remove oldest entries if cache is too large
            const entries = Array.from(this.cache.entries());
            entries.sort((a, b) => a[1].timestamp - b[1].timestamp);
            const toRemove = entries.slice(0, entries.length - this.config.cacheSize);
            toRemove.forEach(([key]) => this.cache.delete(key));
        }
    }

    /**
     * Get utilities status
     */
    getUtilitiesStatus() {
        return {
            isInitialized: this.isInitialized,
            cacheSize: this.cache.size,
            domCacheSize: this.domCache.size,
            stringCacheSize: this.stringCache.size,
            components: {
                arrayUtils: !!this.arrayUtils,
                domUtils: !!this.domUtils,
                loggingUtils: !!this.loggingUtils,
                stringUtils: !!this.stringUtils,
                timeUtils: !!this.timeUtils,
                validationUtils: !!this.validationUtils
            }
        };
    }

    /**
     * Destroy utilities and cleanup
     */
    destroy() {
        this.logger.log('Destroying Utilities Consolidated...');

        // Clear caches
        this.cache.clear();
        this.domCache.clear();
        this.stringCache.clear();

        // Reset components
        this.arrayUtils = null;
        this.domUtils = null;
        this.loggingUtils = null;
        this.stringUtils = null;
        this.timeUtils = null;
        this.validationUtils = null;

        this.isInitialized = false;
        this.logger.log('Utilities Consolidated destroyed');
    }
}

// ================================
// COMPONENT CLASSES
// ================================

/**
 * Array Utilities - Consolidated array manipulation functions
 */
class ArrayUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    chunk(array, size) {
        if (!Array.isArray(array)) {
            throw new Error('First argument must be an array');
        }
        if (size <= 0) {
            throw new Error('Size must be greater than 0');
        }

        const chunks = [];
        for (let i = 0; i < array.length; i += size) {
            chunks.push(array.slice(i, i + size));
        }
        return chunks;
    }

    unique(array) {
        return [...new Set(array)];
    }

    shuffle(array) {
        const shuffled = [...array];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    intersect(...arrays) {
        if (arrays.length === 0) return [];
        return arrays.reduce((acc, arr) =>
            acc.filter(item => arr.includes(item))
        );
    }

    groupBy(array, keyFn) {
        return array.reduce((groups, item) => {
            const key = keyFn(item);
            if (!groups[key]) {
                groups[key] = [];
            }
            groups[key].push(item);
            return groups;
        }, {});
    }

    sortBy(array, criteria) {
        return [...array].sort((a, b) => {
            for (const criterion of criteria) {
                const aVal = a[criterion.key];
                const bVal = b[criterion.key];
                const order = criterion.order === 'desc' ? -1 : 1;

                if (aVal < bVal) return -1 * order;
                if (aVal > bVal) return 1 * order;
            }
            return 0;
        });
    }
}

/**
 * DOM Utilities - Consolidated DOM manipulation functions
 */
class DOMUtils {
    constructor(logger = console) {
        this.logger = logger;
        this.cache = new Map();
        this.eventListeners = new Map();
    }

    select(selector, context = document) {
        const cacheKey = `${selector}_${context}`;
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }

        const element = context.querySelector(selector);
        if (element) {
            this.cache.set(cacheKey, element);
        }
        return element;
    }

    create(tagName, attributes = {}, content = '') {
        const element = document.createElement(tagName);

        // Set attributes
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'style' && typeof value === 'object') {
                Object.assign(element.style, value);
            } else {
                element.setAttribute(key, value);
            }
        });

        // Set content
        if (content) {
            element.textContent = content;
        }

        return element;
    }

    addEvent(element, event, handler, options = {}) {
        element.addEventListener(event, handler, options);

        // Track for cleanup
        const key = `${element}_${event}`;
        if (!this.eventListeners.has(key)) {
            this.eventListeners.set(key, []);
        }
        this.eventListeners.get(key).push({ handler, options });

        return () => this.removeEvent(element, event, handler);
    }

    removeEvent(element, event, handler) {
        element.removeEventListener(event, handler);

        // Remove from tracking
        const key = `${element}_${event}`;
        const listeners = this.eventListeners.get(key);
        if (listeners) {
            const index = listeners.findIndex(l => l.handler === handler);
            if (index > -1) {
                listeners.splice(index, 1);
            }
        }
    }

    addClass(element, className) {
        element.classList.add(className);
    }

    removeClass(element, className) {
        element.classList.remove(className);
    }

    toggleClass(element, className) {
        element.classList.toggle(className);
    }

    hasClass(element, className) {
        return element.classList.contains(className);
    }

    getDimensions(element) {
        const rect = element.getBoundingClientRect();
        return {
            width: rect.width,
            height: rect.height,
            top: rect.top,
            left: rect.left,
            bottom: rect.bottom,
            right: rect.right
        };
    }

    isInViewport(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    }

    animate(element, properties, duration = 300, easing = 'ease') {
        return new Promise(resolve => {
            const start = {};
            const change = {};

            // Get starting values
            Object.keys(properties).forEach(prop => {
                if (prop === 'scrollTop' || prop === 'scrollLeft') {
                    start[prop] = element[prop];
                } else {
                    start[prop] = parseFloat(getComputedStyle(element)[prop]) || 0;
                }
                change[prop] = properties[prop] - start[prop];
            });

            const startTime = performance.now();

            const animateFrame = (currentTime) => {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);

                // Apply easing
                let easedProgress;
                switch (easing) {
                    case 'ease-in':
                        easedProgress = progress * progress;
                        break;
                    case 'ease-out':
                        easedProgress = progress * (2 - progress);
                        break;
                    case 'ease-in-out':
                        easedProgress = progress < 0.5 ? 2 * progress * progress : -1 + (4 - 2 * progress) * progress;
                        break;
                    default:
                        easedProgress = progress;
                }

                // Apply properties
                Object.keys(properties).forEach(prop => {
                    const value = start[prop] + change[prop] * easedProgress;
                    if (prop === 'scrollTop' || prop === 'scrollLeft') {
                        element[prop] = value;
                    } else {
                        element.style[prop] = `${value}${typeof properties[prop] === 'number' ? 'px' : ''}`;
                    }
                });

                if (progress < 1) {
                    requestAnimationFrame(animateFrame);
                } else {
                    resolve();
                }
            };

            requestAnimationFrame(animateFrame);
        });
    }
}

/**
 * String Utilities - Consolidated string manipulation functions
 */
class StringUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    capitalize(str) {
        if (!str) return str;
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }

    camelCase(str) {
        return str
            .replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) =>
                index === 0 ? word.toLowerCase() : word.toUpperCase()
            )
            .replace(/\s+/g, '');
    }

    kebabCase(str) {
        return str
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[\s_]+/g, '-')
            .toLowerCase();
    }

    snakeCase(str) {
        return str
            .replace(/([a-z])([A-Z])/g, '$1_$2')
            .replace(/[\s-]+/g, '_')
            .toLowerCase();
    }

    truncate(str, length, suffix = '...') {
        if (str.length <= length) return str;
        return str.slice(0, length - suffix.length) + suffix;
    }

    stripHtml(str) {
        return str.replace(/<[^>]*>/g, '');
    }

    escapeHtml(str) {
        const htmlEscapes = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        };
        return str.replace(/[&<>"']/g, match => htmlEscapes[match]);
    }

    random(length = 8) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    format(template, ...args) {
        return template.replace(/{(\d+)}/g, (match, number) => {
            return typeof args[number] !== 'undefined' ? args[number] : match;
        });
    }
}

/**
 * Time Utilities - Consolidated time manipulation functions
 */
class TimeUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    format(timestamp, format = 'YYYY-MM-DD HH:mm:ss') {
        const date = new Date(timestamp);

        const year = date.getFullYear();
        const month = String(date.getMonth() + 1).padStart(2, '0');
        const day = String(date.getDate()).padStart(2, '0');
        const hours = String(date.getHours()).padStart(2, '0');
        const minutes = String(date.getMinutes()).padStart(2, '0');
        const seconds = String(date.getSeconds()).padStart(2, '0');

        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    }

    relative(timestamp) {
        const now = Date.now();
        const diff = now - timestamp;
        const absDiff = Math.abs(diff);

        const intervals = [
            { label: 'year', seconds: 31536000 },
            { label: 'month', seconds: 2592000 },
            { label: 'week', seconds: 604800 },
            { label: 'day', seconds: 86400 },
            { label: 'hour', seconds: 3600 },
            { label: 'minute', seconds: 60 },
            { label: 'second', seconds: 1 }
        ];

        for (const interval of intervals) {
            const count = Math.floor(absDiff / (interval.seconds * 1000));
            if (count >= 1) {
                const suffix = diff > 0 ? 'ago' : 'from now';
                return `${count} ${interval.label}${count > 1 ? 's' : ''} ${suffix}`;
            }
        }

        return 'just now';
    }

    add(date, amount, unit) {
        const result = new Date(date);
        switch (unit) {
            case 'year':
            case 'years':
                result.setFullYear(result.getFullYear() + amount);
                break;
            case 'month':
            case 'months':
                result.setMonth(result.getMonth() + amount);
                break;
            case 'week':
            case 'weeks':
                result.setDate(result.getDate() + amount * 7);
                break;
            case 'day':
            case 'days':
                result.setDate(result.getDate() + amount);
                break;
            case 'hour':
            case 'hours':
                result.setHours(result.getHours() + amount);
                break;
            case 'minute':
            case 'minutes':
                result.setMinutes(result.getMinutes() + amount);
                break;
            case 'second':
            case 'seconds':
                result.setSeconds(result.getSeconds() + amount);
                break;
        }
        return result;
    }

    subtract(date, amount, unit) {
        return this.add(date, -amount, unit);
    }

    diff(date1, date2, unit = 'milliseconds') {
        const diff = date2.getTime() - date1.getTime();

        switch (unit) {
            case 'seconds':
                return Math.floor(diff / 1000);
            case 'minutes':
                return Math.floor(diff / (1000 * 60));
            case 'hours':
                return Math.floor(diff / (1000 * 60 * 60));
            case 'days':
                return Math.floor(diff / (1000 * 60 * 60 * 24));
            case 'weeks':
                return Math.floor(diff / (1000 * 60 * 60 * 24 * 7));
            case 'months':
                return Math.floor(diff / (1000 * 60 * 60 * 24 * 30));
            case 'years':
                return Math.floor(diff / (1000 * 60 * 60 * 24 * 365));
            default:
                return diff;
        }
    }

    isValid(date) {
        return date instanceof Date && !isNaN(date.getTime());
    }

    parse(dateString, format) {
        // Simple date parsing - in production, use a proper date library
        if (format === 'YYYY-MM-DD') {
            return new Date(dateString + 'T00:00:00');
        }
        return new Date(dateString);
    }
}

/**
 * Logging Utilities - Consolidated logging functions
 */
class LoggingUtils {
    constructor(logger = console, level = 'info') {
        this.logger = logger;
        this.level = level;
        this.timers = new Map();
        this.levels = {
            debug: 0,
            info: 1,
            warn: 2,
            error: 3
        };
    }

    shouldLog(level) {
        return this.levels[level] >= this.levels[this.level];
    }

    debug(message, context = {}) {
        if (this.shouldLog('debug')) {
            this.logger.debug(this.formatMessage('DEBUG', message, context));
        }
    }

    info(message, context = {}) {
        if (this.shouldLog('info')) {
            this.logger.info(this.formatMessage('INFO', message, context));
        }
    }

    warn(message, context = {}) {
        if (this.shouldLog('warn')) {
            this.logger.warn(this.formatMessage('WARN', message, context));
        }
    }

    error(message, context = {}) {
        if (this.shouldLog('error')) {
            this.logger.error(this.formatMessage('ERROR', message, context));
        }
    }

    formatMessage(level, message, context) {
        const timestamp = new Date().toISOString();
        const contextStr = Object.keys(context).length > 0 ?
            ` ${JSON.stringify(context)}` : '';
        return `[${timestamp}] ${level}: ${message}${contextStr}`;
    }

    startTimer(label) {
        this.timers.set(label, performance.now());
        return label;
    }

    endTimer(label) {
        const start = this.timers.get(label);
        if (!start) {
            this.warn(`Timer '${label}' does not exist`);
            return null;
        }

        const duration = performance.now() - start;
        this.timers.delete(label);
        this.info(`Timer '${label}' completed in ${duration.toFixed(2)}ms`);

        return duration;
    }

    createChild(name) {
        return new LoggingUtils({
            ...this.logger,
            name: this.logger.name ? `${this.logger.name}:${name}` : name
        }, this.level);
    }
}

/**
 * Validation Utilities - Consolidated validation functions
 */
class ValidationUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    email(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    url(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    phone(phone) {
        const phoneRegex = /^\+?[\d\s\-\(\)]+$/;
        return phoneRegex.test(phone) && phone.replace(/\D/g, '').length >= 10;
    }

    required(value) {
        return value !== null && value !== undefined && value !== '';
    }

    length(str, min = 0, max = Infinity) {
        if (typeof str !== 'string') return false;
        return str.length >= min && str.length <= max;
    }

    range(number, min = -Infinity, max = Infinity) {
        if (typeof number !== 'number' || isNaN(number)) return false;
        return number >= min && number <= max;
    }

    pattern(str, pattern) {
        if (typeof str !== 'string') return false;
        return pattern.test(str);
    }

    validate(data, rules) {
        const errors = [];
        const result = { isValid: true, errors: [] };

        Object.entries(rules).forEach(([field, rule]) => {
            const value = data[field];

            if (rule.required && !this.required(value)) {
                errors.push(`${field} is required`);
            }

            if (value !== undefined && value !== null) {
                if (rule.type && typeof value !== rule.type) {
                    errors.push(`${field} must be of type ${rule.type}`);
                }

                if (rule.email && !this.email(value)) {
                    errors.push(`${field} must be a valid email`);
                }

                if (rule.url && !this.url(value)) {
                    errors.push(`${field} must be a valid URL`);
                }

                if (rule.min !== undefined && value < rule.min) {
                    errors.push(`${field} must be at least ${rule.min}`);
                }

                if (rule.max !== undefined && value > rule.max) {
                    errors.push(`${field} must be at most ${rule.max}`);
                }

                if (rule.pattern && !this.pattern(value, rule.pattern)) {
                    errors.push(`${field} format is invalid`);
                }
            }
        });

        if (errors.length > 0) {
            result.isValid = false;
            result.errors = errors;
        }

        return result;
    }
}

// ================================
// EXPORTS
// ================================

export {
    UtilitiesConsolidated,
    ArrayUtils,
    DOMUtils,
    StringUtils,
    TimeUtils,
    LoggingUtils,
    ValidationUtils
};
