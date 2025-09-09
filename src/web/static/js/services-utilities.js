/**
 * Utilities Service Module - V2 Compliant
 * Provides common utility functions and helpers
 * V2 COMPLIANCE: <200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR COMPONENT
 * @license MIT
 */

class UtilityService {
    constructor(config = {}) {
        this.config = { enableLogging: true, ...config };
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;
        console.log('🔧 Initializing Utility Service...');
        this.isInitialized = true;
    }

    // String utilities
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }

    camelCase(str) {
        return str.replace(/[-_](.)/g, (_, letter) => letter.toUpperCase());
    }

    kebabCase(str) {
        return str.replace(/([a-z0-9]|(?=[A-Z]))([A-Z])/g, '$1-$2').toLowerCase();
    }

    truncate(str, length = 50) {
        return str.length > length ? str.substring(0, length) + '...' : str;
    }

    // Array utilities
    unique(arr) {
        return [...new Set(arr)];
    }

    chunk(arr, size) {
        const chunks = [];
        for (let i = 0; i < arr.length; i += size) {
            chunks.push(arr.slice(i, i + size));
        }
        return chunks;
    }

    shuffle(arr) {
        const shuffled = [...arr];
        for (let i = shuffled.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
        }
        return shuffled;
    }

    // Object utilities
    deepClone(obj) {
        try {
            return JSON.parse(JSON.stringify(obj));
        } catch (error) {
            return obj;
        }
    }

    isEmpty(obj) {
        if (obj === null || obj === undefined) return true;
        if (typeof obj === 'string' || Array.isArray(obj)) return obj.length === 0;
        if (typeof obj === 'object') return Object.keys(obj).length === 0;
        return false;
    }

    pick(obj, keys) {
        return keys.reduce((result, key) => {
            if (key in obj) result[key] = obj[key];
            return result;
        }, {});
    }

    omit(obj, keys) {
        const result = { ...obj };
        keys.forEach(key => delete result[key]);
        return result;
    }

    // Date utilities
    formatDate(date, format = 'ISO') {
        const d = new Date(date);
        if (isNaN(d.getTime())) return date;

        switch (format) {
            case 'ISO': return d.toISOString();
            case 'local': return d.toLocaleString();
            case 'date': return d.toLocaleDateString();
            case 'time': return d.toLocaleTimeString();
            default: return d.toString();
        }
    }

    timeAgo(date) {
        const now = new Date();
        const past = new Date(date);
        const diff = now - past;

        const minutes = Math.floor(diff / 60000);
        const hours = Math.floor(diff / 3600000);
        const days = Math.floor(diff / 86400000);

        if (days > 0) return `${days} day${days > 1 ? 's' : ''} ago`;
        if (hours > 0) return `${hours} hour${hours > 1 ? 's' : ''} ago`;
        if (minutes > 0) return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
        return 'Just now';
    }

    // Number utilities
    formatNumber(num, options = {}) {
        const { decimals = 2, locale = 'en-US' } = options;
        return new Intl.NumberFormat(locale, { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(num);
    }

    clamp(num, min, max) {
        return Math.min(Math.max(num, min), max);
    }

    random(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    // ID generation
    generateId(prefix = '') {
        const timestamp = Date.now().toString(36);
        const random = Math.random().toString(36).substr(2, 9);
        return `${prefix}${timestamp}${random}`;
    }

    // Debounce and throttle
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

    throttle(func, wait) {
        let inThrottle;
        return function executedFunction(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, wait);
            }
        };
    }

    // DOM utilities
    createElement(tag, attributes = {}, text = '') {
        const element = document.createElement(tag);
        Object.entries(attributes).forEach(([key, value]) => {
            element.setAttribute(key, value);
        });
        if (text) element.textContent = text;
        return element;
    }

    // Logging utilities
    log(level, message, data = null) {
        if (!this.config.enableLogging) return;

        const timestamp = this.formatDate(new Date());
        const logMessage = `[${timestamp}] ${level.toUpperCase()}: ${message}`;

        if (data) {
            console[level](logMessage, data);
        } else {
            console[level](logMessage);
        }
    }

    // Async utilities
    sleep(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

    timeout(promise, ms) {
        return Promise.race([
            promise,
            new Promise((_, reject) => setTimeout(() => reject(new Error('Operation timed out')), ms))
        ]);
    }

    // Validation utilities
    isEmail(str) { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(str); }

    isURL(str) { try { new URL(str); return true; } catch { return false; } }

    getStats() { return { initialized: this.isInitialized }; }

    async destroy() { this.isInitialized = false; }
}

export { UtilityService };
export default UtilityService;
