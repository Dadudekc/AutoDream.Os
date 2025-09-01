/**
 * Unified Validation System - V2 Compliant
 * Consolidates all duplicate validation functions across web development modules
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @license MIT
 */

// ================================
// UNIFIED VALIDATION SYSTEM
// ================================

/**
 * Unified validation system that consolidates all duplicate validation functions
 * from dashboard validation utilities, utility validation service, and dashboard utils
 */
class UnifiedValidationSystem {
    constructor() {
        this.logger = console;
        this.cache = new Map();
    }

    /**
     * Validate email address - consolidated from multiple sources
     */
    validateEmail(email) {
        try {
            if (!email || typeof email !== 'string') {
                return { isValid: false, error: 'Email must be a valid string' };
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValid = emailRegex.test(email);

            return {
                isValid: isValid,
                error: isValid ? null : 'Invalid email format'
            };
        } catch (error) {
            this.logError('Email validation failed', error);
            return { isValid: false, error: 'Email validation error' };
        }
    }

    /**
     * Validate URL - consolidated from utility validation service
     */
    validateUrl(url) {
        try {
            if (!url || typeof url !== 'string') {
                return { isValid: false, error: 'URL must be a valid string' };
            }

            try {
                new URL(url);
                return { isValid: true, error: null };
            } catch (urlError) {
                return { isValid: false, error: 'Invalid URL format' };
            }
        } catch (error) {
            this.logError('URL validation failed', error);
            return { isValid: false, error: 'URL validation error' };
        }
    }

    /**
     * Validate required fields in object - consolidated from utility validation service
     */
    validateRequiredFields(data, requiredFields) {
        try {
            if (!data || typeof data !== 'object') {
                return {
                    isValid: false,
                    missingFields: requiredFields,
                    error: 'Data object is required'
                };
            }

            if (!Array.isArray(requiredFields)) {
                return {
                    isValid: false,
                    missingFields: [],
                    error: 'Required fields must be an array'
                };
            }

            const missingFields = [];
            const invalidFields = [];

            for (const field of requiredFields) {
                if (!(field in data)) {
                    missingFields.push(field);
                } else if (data[field] === null || data[field] === undefined || data[field] === '') {
                    invalidFields.push(field);
                }
            }

            const isValid = missingFields.length === 0 && invalidFields.length === 0;

            return {
                isValid: isValid,
                missingFields: missingFields,
                invalidFields: invalidFields,
                error: isValid ? null : `Missing: ${missingFields.join(', ')}, Invalid: ${invalidFields.join(', ')}`
            };
        } catch (error) {
            this.logError('Required fields validation failed', error);
            return {
                isValid: false,
                missingFields: requiredFields,
                error: 'Required fields validation error'
            };
        }
    }

    /**
     * Validate numeric range - consolidated from utility validation service
     */
    validateNumericRange(value, min = null, max = null) {
        try {
            const numValue = Number(value);
            
            if (isNaN(numValue) || !isFinite(numValue)) {
                return { isValid: false, error: 'Value must be a valid number' };
            }

            if (min !== null && numValue < min) {
                return { isValid: false, error: `Value must be at least ${min}` };
            }

            if (max !== null && numValue > max) {
                return { isValid: false, error: `Value must be at most ${max}` };
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Numeric range validation failed', error);
            return { isValid: false, error: 'Numeric range validation error' };
        }
    }

    /**
     * Validate dashboard configuration - consolidated from dashboard validation utilities
     */
    validateDashboardConfig(config) {
        try {
            if (!config || typeof config !== 'object') {
                return { isValid: false, error: 'Dashboard configuration must be a valid object' };
            }

            const requiredFields = ['id', 'title'];
            const missingFields = requiredFields.filter(field => !config[field]);

            if (missingFields.length > 0) {
                return {
                    isValid: false,
                    error: `Dashboard configuration missing required fields: ${missingFields.join(', ')}`
                };
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Dashboard config validation failed', error);
            return { isValid: false, error: 'Dashboard config validation error' };
        }
    }

    /**
     * Validate chart data - consolidated from dashboard validation utilities
     */
    validateChartData(data) {
        try {
            if (!data || !Array.isArray(data)) {
                return { isValid: false, error: 'Chart data must be a valid array' };
            }

            if (data.length === 0) {
                return { isValid: false, error: 'Chart data cannot be empty' };
            }

            // Validate data structure
            const requiredFields = ['label', 'value'];
            for (let i = 0; i < data.length; i++) {
                const item = data[i];
                if (!item || typeof item !== 'object') {
                    return { isValid: false, error: `Chart data item ${i} must be an object` };
                }

                const missingFields = requiredFields.filter(field => !(field in item));
                if (missingFields.length > 0) {
                    return {
                        isValid: false,
                        error: `Chart data item ${i} missing required fields: ${missingFields.join(', ')}`
                    };
                }
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('Chart data validation failed', error);
            return { isValid: false, error: 'Chart data validation error' };
        }
    }

    /**
     * Validate API response - consolidated from dashboard validation utilities
     */
    validateApiResponse(response, expectedStructure = {}) {
        try {
            if (!response || typeof response !== 'object') {
                return { isValid: false, error: 'API response must be a valid object' };
            }

            // Check expected structure if provided
            if (Object.keys(expectedStructure).length > 0) {
                for (const [key, expectedType] of Object.entries(expectedStructure)) {
                    if (!(key in response)) {
                        return { isValid: false, error: `API response missing required field: ${key}` };
                    }

                    if (typeof response[key] !== expectedType) {
                        return { isValid: false, error: `API response field ${key} must be of type ${expectedType}` };
                    }
                }
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logError('API response validation failed', error);
            return { isValid: false, error: 'API response validation error' };
        }
    }

    /**
     * Validate form input - consolidated from dashboard validation utilities
     */
    validateFormInput(value, rules = {}) {
        try {
            const errors = [];

            // Required validation
            if (rules.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
                errors.push('This field is required');
            }

            // Type validation
            if (rules.type && typeof value !== rules.type) {
                errors.push(`Must be of type ${rules.type}`);
            }

            // Length validation
            if (rules.minLength && typeof value === 'string' && value.length < rules.minLength) {
                errors.push(`Must be at least ${rules.minLength} characters`);
            }

            if (rules.maxLength && typeof value === 'string' && value.length > rules.maxLength) {
                errors.push(`Must be at most ${rules.maxLength} characters`);
            }

            // Pattern validation
            if (rules.pattern && typeof value === 'string' && !rules.pattern.test(value)) {
                errors.push('Invalid format');
            }

            return {
                isValid: errors.length === 0,
                error: errors.length > 0 ? errors[0] : null,
                allErrors: errors
            };
        } catch (error) {
            this.logError('Form input validation failed', error);
            return {
                isValid: false,
                error: 'Form input validation error',
                allErrors: ['Form input validation error']
            };
        }
    }

    /**
     * Type validation utilities - consolidated from dashboard utils
     */
    createTypeValidationUtils() {
        return {
            isEmail: (email) => this.validateEmail(email).isValid,
            isNumber: (value) => !isNaN(value) && isFinite(value),
            isString: (value) => typeof value === 'string',
            isObject: (value) => typeof value === 'object' && value !== null,
            isArray: (value) => Array.isArray(value),
            isBoolean: (value) => typeof value === 'boolean'
        };
    }

    /**
     * Log error with context
     */
    logError(message, error) {
        this.logger.error(`[UnifiedValidationSystem] ${message}:`, error);
    }

    /**
     * Clear validation cache
     */
    clearCache() {
        this.cache.clear();
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create unified validation system instance
 */
export function createUnifiedValidationSystem() {
    return new UnifiedValidationSystem();
}

/**
 * Create type validation utilities
 */
export function createTypeValidationUtils() {
    const system = new UnifiedValidationSystem();
    return system.createTypeValidationUtils();
}

// ================================
// EXPORTS
// ================================

export { UnifiedValidationSystem };
export default UnifiedValidationSystem;
