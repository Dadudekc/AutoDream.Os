/**
 * Utility String Service - V2 Compliant
 * String manipulation utilities extracted from utility-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// UTILITY STRING SERVICE
// ================================

/**
 * String manipulation utility functions
 */
class UtilityStringService {
    constructor() {
        this.logger = console;
    }

    /**
     * Format string with template replacement
     */
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

    /**
     * Sanitize input string
     */
    sanitizeInput(input, options = {}) {
        try {
            if (typeof input !== 'string') {
                return input;
            }

            const config = {
                maxLength: options.maxLength || 1000,
                allowHtml: options.allowHtml || false,
                allowScripts: options.allowScripts || false,
                ...options
            };

            let sanitized = input.trim();

            // Length limit
            if (sanitized.length > config.maxLength) {
                sanitized = sanitized.substring(0, config.maxLength);
            }

            // HTML removal (basic)
            if (!config.allowHtml) {
                sanitized = sanitized.replace(/<[^>]*>/g, '');
            }

            // Script removal
            if (!config.allowScripts) {
                sanitized = sanitized.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
                sanitized = sanitized.replace(/javascript:/gi, '');
                sanitized = sanitized.replace(/on\w+\s*=/gi, '');
            }

            return sanitized;

        } catch (error) {
            this.logError('Input sanitization failed', error);
            return input;
        }
    }

    /**
     * Capitalize first letter
     */
    capitalize(str) {
        if (!str || typeof str !== 'string') return str;
        return str.charAt(0).toUpperCase() + str.slice(1).toLowerCase();
    }

    /**
     * Convert to camelCase
     */
    toCamelCase(str) {
        if (!str || typeof str !== 'string') return str;
        return str.replace(/(?:^\w|[A-Z]|\b\w)/g, (word, index) =>
            index === 0 ? word.toLowerCase() : word.toUpperCase()
        ).replace(/\s+/g, '');
    }

    /**
     * Convert to kebab-case
     */
    toKebabCase(str) {
        if (!str || typeof str !== 'string') return str;
        return str
            .replace(/([a-z])([A-Z])/g, '$1-$2')
            .replace(/[\s_]+/g, '-')
            .toLowerCase();
    }

    /**
     * Convert to snake_case
     */
    toSnakeCase(str) {
        if (!str || typeof str !== 'string') return str;
        return str
            .replace(/([a-z])([A-Z])/g, '$1_$2')
            .replace(/[\s-]+/g, '_')
            .toLowerCase();
    }

    /**
     * Truncate string with ellipsis
     */
    truncate(str, maxLength = 100, suffix = '...') {
        if (!str || typeof str !== 'string' || str.length <= maxLength) {
            return str;
        }
        return str.substring(0, maxLength - suffix.length) + suffix;
    }

    /**
     * Remove extra whitespace
     */
    normalizeWhitespace(str) {
        if (!str || typeof str !== 'string') return str;
        return str.replace(/\s+/g, ' ').trim();
    }

    /**
     * Check if string is empty or whitespace
     */
    isEmpty(str) {
        return !str || typeof str !== 'string' || str.trim().length === 0;
    }

    /**
     * Generate random string
     */
    generateRandomString(length = 8) {
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
        let result = '';
        for (let i = 0; i < length; i++) {
            result += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        return result;
    }

    /**
     * Log error
     */
    logError(message, error) {
        this.logger.error(`[UtilityStringService] ${message}:`, error);
    }
}

// ================================
// GLOBAL STRING SERVICE INSTANCE
// ================================

/**
 * Global utility string service instance
 */
const utilityStringService = new UtilityStringService();

// ================================
// STRING SERVICE API FUNCTIONS
// ================================

/**
 * Format string
 */
export function formatString(template, data) {
    return utilityStringService.formatString(template, data);
}

/**
 * Sanitize input
 */
export function sanitizeInput(input, options = {}) {
    return utilityStringService.sanitizeInput(input, options);
}

/**
 * Capitalize string
 */
export function capitalize(str) {
    return utilityStringService.capitalize(str);
}

/**
 * Convert to camelCase
 */
export function toCamelCase(str) {
    return utilityStringService.toCamelCase(str);
}

/**
 * Convert to kebab-case
 */
export function toKebabCase(str) {
    return utilityStringService.toKebabCase(str);
}

// ================================
// EXPORTS
// ================================

export { UtilityStringService, utilityStringService };
export default utilityStringService;
