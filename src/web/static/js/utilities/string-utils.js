/**
 * String Utilities Module - V2 Compliant
 * Specialized string manipulation functions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class StringUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    /**
     * Format string template with data
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
            this.logger.error('String formatting failed', error);
            return template;
        }
    }

    /**
     * Sanitize input string
     */
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
            sanitized = sanitized.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
            sanitized = sanitized.replace(/javascript:/gi, '');
            sanitized = sanitized.replace(/on\w+\s*=/gi, '');
        }

        return sanitized;
    }

    /**
     * Generate slug from string
     */
    generateSlug(text) {
        try {
            return text
                .toLowerCase()
                .trim()
                .replace(/[^\w\s-]/g, '')
                .replace(/[\s_-]+/g, '-')
                .replace(/^-+|-+$/g, '');
        } catch (error) {
            this.logger.error('Slug generation failed', error);
            return '';
        }
    }

    /**
     * Capitalize first letter
     */
    capitalize(text) {
        if (typeof text !== 'string' || text.length === 0) {
            return text;
        }
        return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    }

    /**
     * Truncate text with ellipsis
     */
    truncate(text, maxLength = 100, suffix = '...') {
        if (typeof text !== 'string' || text.length <= maxLength) {
            return text;
        }
        return text.substring(0, maxLength - suffix.length) + suffix;
    }
}

// Factory function for creating string utils instance
export function createStringUtils(logger = console) {
    return new StringUtils(logger);
}


