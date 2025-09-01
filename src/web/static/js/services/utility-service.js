/**
 * Utility Service - V2 Compliance Implementation
 * Centralized utility functions with dependency injection
 * V2 Compliance: Eliminates duplicate utility implementations
 */

export class UtilityService {
    constructor() {
        this.cache = new Map();
        this.logger = console;
        this.config = {
            cacheTimeout: 30000,
            maxCacheSize: 1000,
            enableLogging: true
        };
    }

    // String manipulation utilities
    formatString(template, data) {
        try {
            if (!template || typeof template !== 'string') {
                throw new Error('Invalid template provided');
            }

            return template.replace(/\{(\w+)\}/g, (match, key) => {
                return data[key] !== undefined ? data[key] : match;
            });
        } catch (error) {
            this.logError('String formatting failed', error);
            return template;
        }
    }

    sanitizeInput(input, options = {}) {
        const defaultOptions = {
            maxLength: 1000,
            allowHtml: false,
            allowScripts: false
        };
        
        const config = { ...defaultOptions, ...options };
        
        if (typeof input !== 'string') {
            return '';
        }

        let sanitized = input.trim();
        
        if (sanitized.length > config.maxLength) {
            sanitized = sanitized.substring(0, config.maxLength);
        }

        if (!config.allowHtml) {
            sanitized = sanitized.replace(/<[^>]*>/g, '');
        }

        if (!config.allowScripts) {
            sanitized = sanitized.replace(/javascript:/gi, '');
            sanitized = sanitized.replace(/on\w+\s*=/gi, '');
        }

        return sanitized;
    }

    // Date and time utilities
    formatDate(date, format = 'ISO') {
        try {
            const dateObj = new Date(date);
            
            if (isNaN(dateObj.getTime())) {
                throw new Error('Invalid date provided');
            }

            switch (format) {
                case 'ISO':
                    return dateObj.toISOString();
                case 'short':
                    return dateObj.toLocaleDateString();
                case 'long':
                    return dateObj.toLocaleDateString('en-US', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                    });
                case 'timestamp':
                    return dateObj.getTime();
                default:
                    return dateObj.toISOString();
            }
        } catch (error) {
            this.logError('Date formatting failed', error);
            return new Date().toISOString();
        }
    }

    calculateTimeDifference(startDate, endDate, unit = 'milliseconds') {
        try {
            const start = new Date(startDate);
            const end = new Date(endDate);
            
            if (isNaN(start.getTime()) || isNaN(end.getTime())) {
                throw new Error('Invalid date provided');
            }

            const diff = end.getTime() - start.getTime();

            switch (unit) {
                case 'seconds':
                    return Math.floor(diff / 1000);
                case 'minutes':
                    return Math.floor(diff / (1000 * 60));
                case 'hours':
                    return Math.floor(diff / (1000 * 60 * 60));
                case 'days':
                    return Math.floor(diff / (1000 * 60 * 60 * 24));
                default:
                    return diff;
            }
        } catch (error) {
            this.logError('Time difference calculation failed', error);
            return 0;
        }
    }

    // Array and object utilities
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
            this.logError('Deep clone failed', error);
            return obj;
        }
    }

    mergeObjects(target, ...sources) {
        try {
            if (!target || typeof target !== 'object') {
                target = {};
            }

            sources.forEach(source => {
                if (source && typeof source === 'object') {
                    Object.keys(source).forEach(key => {
                        if (source[key] && typeof source[key] === 'object' && !Array.isArray(source[key])) {
                            target[key] = this.mergeObjects(target[key] || {}, source[key]);
                        } else {
                            target[key] = source[key];
                        }
                    });
                }
            });

            return target;
        } catch (error) {
            this.logError('Object merge failed', error);
            return target;
        }
    }

    filterArrayByCriteria(array, criteria) {
        try {
            if (!Array.isArray(array)) {
                return [];
            }

            return array.filter(item => {
                for (const [key, value] of Object.entries(criteria)) {
                    if (item[key] !== value) {
                        return false;
                    }
                }
                return true;
            });
        } catch (error) {
            this.logError('Array filtering failed', error);
            return [];
        }
    }

    // Validation utilities
    validateEmail(email) {
        try {
            if (!email || typeof email !== 'string') {
                return false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        } catch (error) {
            this.logError('Email validation failed', error);
            return false;
        }
    }

    validateUrl(url) {
        try {
            if (!url || typeof url !== 'string') {
                return false;
            }

            try {
                new URL(url);
                return true;
            } catch {
                return false;
            }
        } catch (error) {
            this.logError('URL validation failed', error);
            return false;
        }
    }

    validateRequiredFields(data, requiredFields) {
        try {
            if (!data || typeof data !== 'object') {
                return false;
            }

            if (!Array.isArray(requiredFields)) {
                return false;
            }

            return requiredFields.every(field => {
                const value = data[field];
                return value !== undefined && value !== null && value !== '';
            });
        } catch (error) {
            this.logError('Required fields validation failed', error);
            return false;
        }
    }

    // Caching utilities
    getCached(key) {
        try {
            const cached = this.cache.get(key);
            if (cached && Date.now() - cached.timestamp < this.config.cacheTimeout) {
                return cached.data;
            }
            return null;
        } catch (error) {
            this.logError('Cache retrieval failed', error);
            return null;
        }
    }

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
        } catch (error) {
            this.logError('Cache setting failed', error);
        }
    }

    clearCache() {
        try {
            this.cache.clear();
        } catch (error) {
            this.logError('Cache clearing failed', error);
        }
    }

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
            }
        } catch (error) {
            this.logError('Oldest cache clearing failed', error);
        }
    }

    // Performance utilities
    debounce(func, delay) {
        try {
            let timeoutId;
            
            return function (...args) {
                clearTimeout(timeoutId);
                timeoutId = setTimeout(() => func.apply(this, args), delay);
            };
        } catch (error) {
            this.logError('Debounce creation failed', error);
            return func;
        }
    }

    throttle(func, limit) {
        try {
            let inThrottle;
            
            return function (...args) {
                if (!inThrottle) {
                    func.apply(this, args);
                    inThrottle = true;
                    setTimeout(() => inThrottle = false, limit);
                }
            };
        } catch (error) {
            this.logError('Throttle creation failed', error);
            return func;
        }
    }

    // Error handling utilities
    logError(message, error) {
        if (this.config.enableLogging) {
            this.logger.error(`[UtilityService] ${message}:`, error);
        }
    }

    logInfo(message, data) {
        if (this.config.enableLogging) {
            this.logger.info(`[UtilityService] ${message}:`, data);
        }
    }

    // Configuration utilities
    updateConfig(newConfig) {
        try {
            this.config = { ...this.config, ...newConfig };
        } catch (error) {
            this.logError('Config update failed', error);
        }
    }

    getConfig() {
        return { ...this.config };
    }

    // Math utilities
    roundToDecimal(value, decimals = 2) {
        try {
            if (typeof value !== 'number') {
                throw new Error('Invalid number provided');
            }

            const multiplier = Math.pow(10, decimals);
            return Math.round(value * multiplier) / multiplier;
        } catch (error) {
            this.logError('Decimal rounding failed', error);
            return value;
        }
    }

    calculatePercentage(part, total) {
        try {
            if (typeof part !== 'number' || typeof total !== 'number') {
                throw new Error('Invalid numbers provided');
            }

            if (total === 0) {
                return 0;
            }

            return (part / total) * 100;
        } catch (error) {
            this.logError('Percentage calculation failed', error);
            return 0;
        }
    }

    // File utilities
    getFileExtension(filename) {
        try {
            if (!filename || typeof filename !== 'string') {
                return '';
            }

            const parts = filename.split('.');
            return parts.length > 1 ? parts[parts.length - 1].toLowerCase() : '';
        } catch (error) {
            this.logError('File extension extraction failed', error);
            return '';
        }
    }

    formatFileSize(bytes) {
        try {
            if (typeof bytes !== 'number' || bytes < 0) {
                throw new Error('Invalid bytes provided');
            }

            const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
            if (bytes === 0) return '0 Bytes';

            const i = Math.floor(Math.log(bytes) / Math.log(1024));
            return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
        } catch (error) {
            this.logError('File size formatting failed', error);
            return '0 Bytes';
        }
    }

    // Network utilities
    async checkConnectivity(url = 'https://www.google.com') {
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);

            const response = await fetch(url, {
                method: 'HEAD',
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            return response.ok;
        } catch (error) {
            this.logError('Connectivity check failed', error);
            return false;
        }
    }

    // Browser utilities
    isMobileDevice() {
        try {
            return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
        } catch (error) {
            this.logError('Mobile device detection failed', error);
            return false;
        }
    }

    getBrowserInfo() {
        try {
            const userAgent = navigator.userAgent;
            let browser = 'Unknown';
            let version = 'Unknown';

            if (userAgent.includes('Chrome')) {
                browser = 'Chrome';
                version = userAgent.match(/Chrome\/(\d+)/)?.[1] || 'Unknown';
            } else if (userAgent.includes('Firefox')) {
                browser = 'Firefox';
                version = userAgent.match(/Firefox\/(\d+)/)?.[1] || 'Unknown';
            } else if (userAgent.includes('Safari')) {
                browser = 'Safari';
                version = userAgent.match(/Version\/(\d+)/)?.[1] || 'Unknown';
            } else if (userAgent.includes('Edge')) {
                browser = 'Edge';
                version = userAgent.match(/Edge\/(\d+)/)?.[1] || 'Unknown';
            }

            return { browser, version, userAgent };
        } catch (error) {
            this.logError('Browser info extraction failed', error);
            return { browser: 'Unknown', version: 'Unknown', userAgent: 'Unknown' };
        }
    }
}
