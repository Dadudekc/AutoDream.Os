/**
 * Utility Validation Service - V2 Compliant
 * Validation utilities extracted from utility-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// UTILITY VALIDATION SERVICE
// ================================

/**
 * Validation utility functions
 */
class UtilityValidationService {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate email address
     */
    validateEmail(email) {
        try {
            if (!email || typeof email !== 'string') {
                return { valid: false, message: 'Email is required and must be a string' };
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            const isValid = emailRegex.test(email.trim());

            return {
                valid: isValid,
                message: isValid ? 'Email is valid' : 'Invalid email format'
            };
        } catch (error) {
            this.logError('Email validation failed', error);
            return { valid: false, message: 'Email validation error' };
        }
    }

    /**
     * Validate URL
     */
    validateUrl(url) {
        try {
            if (!url || typeof url !== 'string') {
                return { valid: false, message: 'URL is required and must be a string' };
            }

            try {
                new URL(url);
                return { valid: true, message: 'URL is valid' };
            } catch {
                return { valid: false, message: 'Invalid URL format' };
            }
        } catch (error) {
            this.logError('URL validation failed', error);
            return { valid: false, message: 'URL validation error' };
        }
    }

    /**
     * Validate required fields in object
     */
    validateRequiredFields(data, requiredFields) {
        try {
            if (!data || typeof data !== 'object') {
                return {
                    valid: false,
                    missingFields: requiredFields,
                    message: 'Data object is required'
                };
            }

            if (!Array.isArray(requiredFields)) {
                return {
                    valid: false,
                    missingFields: [],
                    message: 'Required fields must be an array'
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

            const valid = missingFields.length === 0 && invalidFields.length === 0;

            return {
                valid: valid,
                missingFields: missingFields,
                invalidFields: invalidFields,
                message: valid ? 'All required fields are present and valid' :
                         `Missing: ${missingFields.join(', ')}, Invalid: ${invalidFields.join(', ')}`
            };
        } catch (error) {
            this.logError('Required fields validation failed', error);
            return {
                valid: false,
                missingFields: requiredFields,
                message: 'Required fields validation error'
            };
        }
    }

    /**
     * Validate numeric range
     */
    validateNumericRange(value, min = null, max = null) {
        try {
            if (typeof value !== 'number' || isNaN(value)) {
                return {
                    valid: false,
                    message: 'Value must be a valid number'
                };
            }

            if (min !== null && value < min) {
                return {
                    valid: false,
                    message: `Value must be at least ${min}`
                };
            }

            if (max !== null && value > max) {
                return {
                    valid: false,
                    message: `Value must be at most ${max}`
                };
            }

            return {
                valid: true,
                message: 'Value is within valid range'
            };
        } catch (error) {
            this.logError('Numeric range validation failed', error);
            return { valid: false, message: 'Numeric range validation error' };
        }
    }

    /**
     * Validate string length
     */
    validateStringLength(str, minLength = null, maxLength = null) {
        try {
            if (typeof str !== 'string') {
                return {
                    valid: false,
                    message: 'Value must be a string'
                };
            }

            const length = str.length;

            if (minLength !== null && length < minLength) {
                return {
                    valid: false,
                    message: `String must be at least ${minLength} characters long`
                };
            }

            if (maxLength !== null && length > maxLength) {
                return {
                    valid: false,
                    message: `String must be at most ${maxLength} characters long`
                };
            }

            return {
                valid: true,
                message: 'String length is valid'
            };
        } catch (error) {
            this.logError('String length validation failed', error);
            return { valid: false, message: 'String length validation error' };
        }
    }

    /**
     * Validate phone number (basic)
     */
    validatePhoneNumber(phone) {
        try {
            if (!phone || typeof phone !== 'string') {
                return { valid: false, message: 'Phone number is required and must be a string' };
            }

            // Remove all non-digit characters
            const digitsOnly = phone.replace(/\D/g, '');

            // Basic length check (10-15 digits for international)
            const isValid = digitsOnly.length >= 10 && digitsOnly.length <= 15;

            return {
                valid: isValid,
                message: isValid ? 'Phone number format is valid' : 'Invalid phone number format'
            };
        } catch (error) {
            this.logError('Phone number validation failed', error);
            return { valid: false, message: 'Phone number validation error' };
        }
    }

    /**
     * Validate password strength
     */
    validatePasswordStrength(password) {
        try {
            if (!password || typeof password !== 'string') {
                return {
                    valid: false,
                    strength: 'none',
                    message: 'Password is required and must be a string'
                };
            }

            const length = password.length;
            let score = 0;
            const checks = {
                length: length >= 8,
                uppercase: /[A-Z]/.test(password),
                lowercase: /[a-z]/.test(password),
                numbers: /\d/.test(password),
                specialChars: /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)
            };

            // Calculate score
            Object.values(checks).forEach(check => {
                if (check) score++;
            });

            let strength = 'weak';
            if (score >= 4) strength = 'strong';
            else if (score >= 3) strength = 'medium';

            const valid = strength !== 'weak';

            return {
                valid: valid,
                strength: strength,
                score: score,
                checks: checks,
                message: valid ? `Password strength: ${strength}` : 'Password is too weak'
            };
        } catch (error) {
            this.logError('Password strength validation failed', error);
            return {
                valid: false,
                strength: 'unknown',
                message: 'Password validation error'
            };
        }
    }

    /**
     * Log error
     */
    logError(message, error) {
        this.logger.error(`[UtilityValidationService] ${message}:`, error);
    }
}

// ================================
// GLOBAL VALIDATION SERVICE INSTANCE
// ================================

/**
 * Global utility validation service instance
 */
const utilityValidationService = new UtilityValidationService();

// ================================
// VALIDATION SERVICE API FUNCTIONS
// ================================

/**
 * Validate email
 */
export function validateEmail(email) {
    return utilityValidationService.validateEmail(email);
}

/**
 * Validate URL
 */
export function validateUrl(url) {
    return utilityValidationService.validateUrl(url);
}

/**
 * Validate required fields
 */
export function validateRequiredFields(data, requiredFields) {
    return utilityValidationService.validateRequiredFields(data, requiredFields);
}

/**
 * Validate numeric range
 */
export function validateNumericRange(value, min = null, max = null) {
    return utilityValidationService.validateNumericRange(value, min, max);
}

/**
 * Validate string length
 */
export function validateStringLength(str, minLength = null, maxLength = null) {
    return utilityValidationService.validateStringLength(str, minLength, maxLength);
}

// ================================
// EXPORTS
// ================================

export { UtilityValidationService, utilityValidationService };
export default utilityValidationService;
