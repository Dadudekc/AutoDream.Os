/**
 * Validation Utilities Module - V2 Compliant
 * Input validation and data verification functions
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE EXTRACTION
 * @license MIT
 */

export class ValidationUtils {
    constructor(logger = console) {
        this.logger = logger;
    }

    /**
     * Validate email format
     */
    validateEmail(email) {
        try {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!email || typeof email !== 'string') {
                return { isValid: false, error: 'Email is required and must be a string' };
            }
            const isValid = emailRegex.test(email.trim());
            return {
                isValid,
                error: isValid ? null : 'Invalid email format'
            };
        } catch (error) {
            this.logger.error('Email validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }

    /**
     * Validate URL format
     */
    validateUrl(url) {
        try {
            const urlRegex = /^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$/;
            if (!url || typeof url !== 'string') {
                return { isValid: false, error: 'URL is required and must be a string' };
            }
            const isValid = urlRegex.test(url.trim());
            return {
                isValid,
                error: isValid ? null : 'Invalid URL format'
            };
        } catch (error) {
            this.logger.error('URL validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }

    /**
     * Validate required fields
     */
    validateRequired(value, fieldName = 'field') {
        try {
            const isValid = value !== null && value !== undefined &&
                          (typeof value !== 'string' || value.trim().length > 0);
            return {
                isValid,
                error: isValid ? null : `${fieldName} is required`
            };
        } catch (error) {
            this.logger.error('Required field validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }

    /**
     * Validate number range
     */
    validateNumberRange(value, min = 0, max = Number.MAX_SAFE_INTEGER, fieldName = 'value') {
        try {
            if (typeof value !== 'number' || isNaN(value)) {
                return { isValid: false, error: `${fieldName} must be a valid number` };
            }
            if (value < min) {
                return { isValid: false, error: `${fieldName} must be at least ${min}` };
            }
            if (value > max) {
                return { isValid: false, error: `${fieldName} must be at most ${max}` };
            }
            return { isValid: true, error: null };
        } catch (error) {
            this.logger.error('Number range validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }

    /**
     * Validate string length
     */
    validateStringLength(value, minLength = 0, maxLength = Number.MAX_SAFE_INTEGER, fieldName = 'text') {
        try {
            if (typeof value !== 'string') {
                return { isValid: false, error: `${fieldName} must be a string` };
            }
            if (value.length < minLength) {
                return { isValid: false, error: `${fieldName} must be at least ${minLength} characters` };
            }
            if (value.length > maxLength) {
                return { isValid: false, error: `${fieldName} must be at most ${maxLength} characters` };
            }
            return { isValid: true, error: null };
        } catch (error) {
            this.logger.error('String length validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }

    /**
     * Validate object structure
     */
    validateObjectStructure(obj, requiredFields = [], fieldName = 'object') {
        try {
            if (!obj || typeof obj !== 'object') {
                return { isValid: false, error: `${fieldName} must be a valid object` };
            }

            const missingFields = requiredFields.filter(field => !obj.hasOwnProperty(field));
            if (missingFields.length > 0) {
                return {
                    isValid: false,
                    error: `${fieldName} is missing required fields: ${missingFields.join(', ')}`
                };
            }

            return { isValid: true, error: null };
        } catch (error) {
            this.logger.error('Object structure validation failed', error);
            return { isValid: false, error: 'Validation error occurred' };
        }
    }
}

// Factory function for creating validation utils instance
export function createValidationUtils(logger = console) {
    return new ValidationUtils(logger);
}


