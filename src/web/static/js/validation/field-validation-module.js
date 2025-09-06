/**
 * Field Validation Module - V2 Compliant
 * Handles basic field-level validation functions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// FIELD VALIDATION MODULE
// ================================

/**
 * Field validation module for basic data validation
 */
export class FieldValidationModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate email address format
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
     * Validate URL format
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
     * Validate numeric range
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
     * Validate required fields in object
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
     * Log error with context
     */
    logError(message, error) {
        this.logger.error(`[FieldValidationModule] ${message}:`, error);
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create field validation module instance
 */
export function createFieldValidationModule() {
    return new FieldValidationModule();
}
