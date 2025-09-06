/**
 * Form Validation Module - V2 Compliant
 * Handles form input validation and type checking utilities
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// FORM VALIDATION MODULE
// ================================

/**
 * Form validation module for user input validation
 */
export class FormValidationModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate form input with custom rules
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

            // Numeric range validation
            if (rules.min !== undefined && typeof value === 'number' && value < rules.min) {
                errors.push(`Must be at least ${rules.min}`);
            }

            if (rules.max !== undefined && typeof value === 'number' && value > rules.max) {
                errors.push(`Must be at most ${rules.max}`);
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
     * Validate multiple form fields
     */
    validateFormFields(fields) {
        try {
            const results = {};
            let hasErrors = false;

            for (const [fieldName, config] of Object.entries(fields)) {
                const { value, rules } = config;
                const validation = this.validateFormInput(value, rules);

                results[fieldName] = validation;
                if (!validation.isValid) {
                    hasErrors = true;
                }
            }

            return {
                isValid: !hasErrors,
                fieldResults: results,
                error: hasErrors ? 'Form validation failed' : null
            };
        } catch (error) {
            this.logError('Form fields validation failed', error);
            return {
                isValid: false,
                fieldResults: {},
                error: 'Form fields validation error'
            };
        }
    }

    /**
     * Create type validation utilities
     */
    createTypeValidationUtils() {
        return {
            isEmail: (email) => {
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                return typeof email === 'string' && emailRegex.test(email);
            },
            isNumber: (value) => !isNaN(value) && isFinite(value),
            isString: (value) => typeof value === 'string',
            isObject: (value) => typeof value === 'object' && value !== null,
            isArray: (value) => Array.isArray(value),
            isBoolean: (value) => typeof value === 'boolean',
            isUrl: (url) => {
                try {
                    new URL(url);
                    return true;
                } catch {
                    return false;
                }
            },
            isPositiveNumber: (value) => this.createTypeValidationUtils().isNumber(value) && value > 0,
            isNonEmptyString: (value) => this.createTypeValidationUtils().isString(value) && value.trim().length > 0,
            isValidDate: (value) => {
                const date = new Date(value);
                return !isNaN(date.getTime());
            }
        };
    }

    /**
     * Sanitize form input
     */
    sanitizeInput(value, type = 'string') {
        try {
            if (value === null || value === undefined) {
                return value;
            }

            switch (type) {
                case 'string':
                    return typeof value === 'string' ? value.trim() : String(value);
                case 'number':
                    const num = Number(value);
                    return isNaN(num) ? 0 : num;
                case 'boolean':
                    return Boolean(value);
                case 'email':
                    return typeof value === 'string' ? value.trim().toLowerCase() : '';
                default:
                    return value;
            }
        } catch (error) {
            this.logError('Input sanitization failed', error);
            return value;
        }
    }

    /**
     * Log error with context
     */
    logError(message, error) {
        this.logger.error(`[FormValidationModule] ${message}:`, error);
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create form validation module instance
 */
export function createFormValidationModule() {
    return new FormValidationModule();
}

/**
 * Create type validation utilities
 */
export function createTypeValidationUtils() {
    const module = new FormValidationModule();
    return module.createTypeValidationUtils();
}
