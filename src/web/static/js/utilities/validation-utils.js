/**
 * Validation Utilities - V2 Compliant Module
 * =========================================
 * 
 * Input validation and data sanitization utilities.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class ValidationUtils {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate email address
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate URL
     */
    isValidURL(url) {
        try {
            new URL(url);
            return true;
        } catch {
            return false;
        }
    }

    /**
     * Validate phone number
     */
    isValidPhone(phone) {
        const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
        return phoneRegex.test(phone.replace(/[\s\-\(\)]/g, ''));
    }

    /**
     * Validate password strength
     */
    validatePassword(password) {
        const result = {
            isValid: false,
            score: 0,
            errors: []
        };

        if (password.length < 8) {
            result.errors.push('Password must be at least 8 characters long');
        } else {
            result.score += 1;
        }

        if (!/[a-z]/.test(password)) {
            result.errors.push('Password must contain at least one lowercase letter');
        } else {
            result.score += 1;
        }

        if (!/[A-Z]/.test(password)) {
            result.errors.push('Password must contain at least one uppercase letter');
        } else {
            result.score += 1;
        }

        if (!/\d/.test(password)) {
            result.errors.push('Password must contain at least one number');
        } else {
            result.score += 1;
        }

        if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
            result.errors.push('Password must contain at least one special character');
        } else {
            result.score += 1;
        }

        result.isValid = result.errors.length === 0;
        return result;
    }

    /**
     * Validate required fields
     */
    validateRequired(data, requiredFields) {
        const errors = [];
        
        requiredFields.forEach(field => {
            if (!data[field] || (typeof data[field] === 'string' && data[field].trim() === '')) {
                errors.push(`${field} is required`);
            }
        });

        return {
            isValid: errors.length === 0,
            errors
        };
    }

    /**
     * Validate string length
     */
    validateLength(value, min = 0, max = Infinity) {
        if (typeof value !== 'string') {
            return { isValid: false, error: 'Value must be a string' };
        }

        if (value.length < min) {
            return { isValid: false, error: `Value must be at least ${min} characters long` };
        }

        if (value.length > max) {
            return { isValid: false, error: `Value must be no more than ${max} characters long` };
        }

        return { isValid: true };
    }

    /**
     * Validate number range
     */
    validateNumber(value, min = -Infinity, max = Infinity) {
        const num = Number(value);
        
        if (isNaN(num)) {
            return { isValid: false, error: 'Value must be a number' };
        }

        if (num < min) {
            return { isValid: false, error: `Value must be at least ${min}` };
        }

        if (num > max) {
            return { isValid: false, error: `Value must be no more than ${max}` };
        }

        return { isValid: true };
    }

    /**
     * Sanitize HTML
     */
    sanitizeHTML(html) {
        const div = document.createElement('div');
        div.textContent = html;
        return div.innerHTML;
    }

    /**
     * Sanitize string
     */
    sanitizeString(str) {
        return str
            .replace(/[<>]/g, '') // Remove < and >
            .replace(/javascript:/gi, '') // Remove javascript: protocol
            .replace(/on\w+=/gi, '') // Remove event handlers
            .trim();
    }

    /**
     * Validate form data
     */
    validateForm(formData, rules) {
        const errors = {};
        let isValid = true;

        Object.entries(rules).forEach(([field, rule]) => {
            const value = formData[field];
            const fieldErrors = [];

            // Required validation
            if (rule.required && (!value || (typeof value === 'string' && value.trim() === ''))) {
                fieldErrors.push(`${field} is required`);
            }

            // Type validation
            if (value && rule.type) {
                switch (rule.type) {
                    case 'email':
                        if (!this.isValidEmail(value)) {
                            fieldErrors.push(`${field} must be a valid email address`);
                        }
                        break;
                    case 'url':
                        if (!this.isValidURL(value)) {
                            fieldErrors.push(`${field} must be a valid URL`);
                        }
                        break;
                    case 'phone':
                        if (!this.isValidPhone(value)) {
                            fieldErrors.push(`${field} must be a valid phone number`);
                        }
                        break;
                    case 'number':
                        if (isNaN(Number(value))) {
                            fieldErrors.push(`${field} must be a number`);
                        }
                        break;
                }
            }

            // Length validation
            if (value && rule.minLength !== undefined) {
                const lengthResult = this.validateLength(value, rule.minLength, rule.maxLength);
                if (!lengthResult.isValid) {
                    fieldErrors.push(lengthResult.error);
                }
            }

            // Number range validation
            if (value && rule.type === 'number' && (rule.min !== undefined || rule.max !== undefined)) {
                const numberResult = this.validateNumber(value, rule.min, rule.max);
                if (!numberResult.isValid) {
                    fieldErrors.push(numberResult.error);
                }
            }

            // Custom validation
            if (value && rule.custom) {
                const customResult = rule.custom(value, formData);
                if (!customResult.isValid) {
                    fieldErrors.push(customResult.error);
                }
            }

            if (fieldErrors.length > 0) {
                errors[field] = fieldErrors;
                isValid = false;
            }
        });

        return { isValid, errors };
    }

    /**
     * Validate JSON data
     */
    validateJSON(jsonString) {
        try {
            const data = JSON.parse(jsonString);
            return { isValid: true, data };
        } catch (error) {
            return { isValid: false, error: error.message };
        }
    }

    /**
     * Validate date
     */
    validateDate(dateString) {
        const date = new Date(dateString);
        return !isNaN(date.getTime());
    }

    /**
     * Validate credit card number
     */
    validateCreditCard(cardNumber) {
        // Remove spaces and dashes
        const cleaned = cardNumber.replace(/[\s\-]/g, '');
        
        // Check if it's all digits
        if (!/^\d+$/.test(cleaned)) {
            return { isValid: false, error: 'Card number must contain only digits' };
        }

        // Check length
        if (cleaned.length < 13 || cleaned.length > 19) {
            return { isValid: false, error: 'Card number must be between 13 and 19 digits' };
        }

        // Luhn algorithm
        let sum = 0;
        let isEven = false;
        
        for (let i = cleaned.length - 1; i >= 0; i--) {
            let digit = parseInt(cleaned[i]);
            
            if (isEven) {
                digit *= 2;
                if (digit > 9) {
                    digit -= 9;
                }
            }
            
            sum += digit;
            isEven = !isEven;
        }
        
        return { isValid: sum % 10 === 0 };
    }
}
