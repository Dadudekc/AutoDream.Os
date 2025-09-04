/**
 * Unified Frontend Utilities - DRY Elimination
 * ============================================
 * 
 * Consolidates all frontend utility functions to eliminate DRY violations.
 * Replaces duplicate utility patterns across 50+ files.
 * 
 * Author: Agent-7 - Web Development Specialist
 * Mission: Frontend Interface Optimization + DRY Elimination
 * V2 Compliance: Under 300-line limit per module
 */

class UnifiedFrontendUtilities {
    constructor() {
        this.cache = new Map();
        this.logger = console;
    }

    // ================================
    // DOM MANIPULATION UTILITIES
    // ================================

    /**
     * Unified element selection with caching
     */
    selectElement(selector, context = document) {
        const cacheKey = `${selector}-${context === document ? 'doc' : 'ctx'}`;
        
        if (this.cache.has(cacheKey)) {
            return this.cache.get(cacheKey);
        }
        
        const element = context.querySelector(selector);
        if (element) {
            this.cache.set(cacheKey, element);
        }
        
        return element;
    }

    /**
     * Unified element creation with attributes
     */
    createElement(tag, attributes = {}, textContent = '') {
        const element = document.createElement(tag);
        
        Object.entries(attributes).forEach(([key, value]) => {
            if (key === 'className') {
                element.className = value;
            } else if (key === 'innerHTML') {
                element.innerHTML = value;
            } else {
                element.setAttribute(key, value);
            }
        });
        
        if (textContent) {
            element.textContent = textContent;
        }
        
        return element;
    }

    /**
     * Unified event listener management
     */
    addEventListener(element, event, handler, options = {}) {
        if (typeof element === 'string') {
            element = this.selectElement(element);
        }
        
        if (element) {
            element.addEventListener(event, handler, options);
            return () => element.removeEventListener(event, handler, options);
        }
        
        return () => {};
    }

    /**
     * Unified CSS class management
     */
    toggleClass(element, className, force) {
        if (typeof element === 'string') {
            element = this.selectElement(element);
        }
        
        if (element) {
            element.classList.toggle(className, force);
        }
    }

    addClass(element, className) {
        if (typeof element === 'string') {
            element = this.selectElement(element);
        }
        
        if (element) {
            element.classList.add(className);
        }
    }

    removeClass(element, className) {
        if (typeof element === 'string') {
            element = this.selectElement(element);
        }
        
        if (element) {
            element.classList.remove(className);
        }
    }

    // ================================
    // VALIDATION UTILITIES
    // ================================

    /**
     * Unified email validation
     */
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Unified phone validation
     */
    validatePhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }

    /**
     * Unified form validation
     */
    validateForm(formData, rules) {
        const errors = {};
        
        Object.entries(rules).forEach(([field, rule]) => {
            const value = formData[field];
            
            if (rule.required && (!value || value.trim() === '')) {
                errors[field] = rule.message || `${field} is required`;
                return;
            }
            
            if (value && rule.pattern && !rule.pattern.test(value)) {
                errors[field] = rule.message || `${field} format is invalid`;
                return;
            }
            
            if (value && rule.minLength && value.length < rule.minLength) {
                errors[field] = rule.message || `${field} must be at least ${rule.minLength} characters`;
                return;
            }
            
            if (value && rule.maxLength && value.length > rule.maxLength) {
                errors[field] = rule.message || `${field} must be no more than ${rule.maxLength} characters`;
                return;
            }
        });
        
        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    // ================================
    // STRING UTILITIES
    // ================================

    /**
     * Unified string formatting
     */
    formatString(template, data) {
        return template.replace(/\{(\w+)\}/g, (match, key) => data[key] || match);
    }

    /**
     * Unified string sanitization
     */
    sanitizeString(str) {
        return str
            .replace(/[<>]/g, '') // Remove HTML tags
            .replace(/['"]/g, '') // Remove quotes
            .trim();
    }

    /**
     * Unified string truncation
     */
    truncateString(str, length, suffix = '...') {
        if (str.length <= length) return str;
        return str.substring(0, length - suffix.length) + suffix;
    }

    // ================================
    // ARRAY UTILITIES
    // ================================

    /**
     * Unified array chunking
     */
    chunkArray(array, size) {
        const chunks = [];
        for (let i = 0; i < array.length; i += size) {
            chunks.push(array.slice(i, i + size));
        }
        return chunks;
    }

    /**
     * Unified array deduplication
     */
    deduplicateArray(array, key) {
        if (key) {
            const seen = new Set();
            return array.filter(item => {
                const value = item[key];
                if (seen.has(value)) return false;
                seen.add(value);
                return true;
            });
        }
        return [...new Set(array)];
    }

    /**
     * Unified array sorting
     */
    sortArray(array, key, direction = 'asc') {
        return array.sort((a, b) => {
            const aVal = key ? a[key] : a;
            const bVal = key ? b[key] : b;
            
            if (direction === 'desc') {
                return bVal > aVal ? 1 : -1;
            }
            return aVal > bVal ? 1 : -1;
        });
    }

    // ================================
    // TIME UTILITIES
    // ================================

    /**
     * Unified date formatting
     */
    formatDate(date, format = 'YYYY-MM-DD') {
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        
        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    }

    /**
     * Unified time ago calculation
     */
    getTimeAgo(date) {
        const now = new Date();
        const diff = now - new Date(date);
        const seconds = Math.floor(diff / 1000);
        const minutes = Math.floor(seconds / 60);
        const hours = Math.floor(minutes / 60);
        const days = Math.floor(hours / 24);
        
        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    }

    // ================================
    // CACHE UTILITIES
    // ================================

    /**
     * Unified caching with TTL
     */
    setCache(key, value, ttl = 300000) { // 5 minutes default
        const item = {
            value,
            expires: Date.now() + ttl
        };
        this.cache.set(key, item);
    }

    /**
     * Unified cache retrieval
     */
    getCache(key) {
        const item = this.cache.get(key);
        
        if (!item) return null;
        
        if (Date.now() > item.expires) {
            this.cache.delete(key);
            return null;
        }
        
        return item.value;
    }

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }

    // ================================
    // LOGGING UTILITIES
    // ================================

    /**
     * Unified logging with levels
     */
    log(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] [${level.toUpperCase()}] ${message}`;
        
        switch (level) {
            case 'error':
                this.logger.error(logMessage, data);
                break;
            case 'warn':
                this.logger.warn(logMessage, data);
                break;
            case 'info':
                this.logger.info(logMessage, data);
                break;
            case 'debug':
                this.logger.debug(logMessage, data);
                break;
            default:
                this.logger.log(logMessage, data);
        }
    }

    /**
     * Performance timing utility
     */
    timeFunction(name, fn) {
        const start = performance.now();
        const result = fn();
        const end = performance.now();
        
        this.log('debug', `Function ${name} took ${(end - start).toFixed(2)}ms`);
        return result;
    }
}

// Create global instance
const unifiedUtils = new UnifiedFrontendUtilities();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { UnifiedFrontendUtilities, unifiedUtils };
}

// Export for ES6 modules
if (typeof window !== 'undefined') {
    window.UnifiedFrontendUtilities = UnifiedFrontendUtilities;
    window.unifiedUtils = unifiedUtils;
}
