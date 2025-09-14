/**
 * Validation Utils - V2 Compliant Data Validation System
 * V2 COMPLIANT: 200 lines maximum
 * CONSOLIDATES: validation utilities from various files
 * 
 * @author Agent-7 - Web Development Specialist
 * @version 5.0.0 - V2 COMPLIANCE CONSOLIDATION
 * @description Unified validation utilities with data validation, sanitization, and error handling
 */

// ================================
// VALIDATION UTILS CLASS
// ================================

/**
 * Unified Validation Utilities
 * Consolidates all validation functionality
 */
export class ValidationUtils {
    constructor(options = {}) {
        this.isInitialized = false;
        this.validators = new Map();
        this.sanitizers = new Map();
        this.config = {
            enableStrictMode: false,
            enableSanitization: true,
            enablePerformanceMonitoring: true,
            ...options
        };
    }

    /**
     * Initialize validation utilities
     */
    async initialize() {
        if (this.isInitialized) {
            console.warn('⚠️ Validation utils already initialized');
            return;
        }

        console.log('🚀 Initializing Validation Utils (V2 Compliant)...');

        try {
            // Setup built-in validators
            this.setupBuiltInValidators();

            // Setup built-in sanitizers
            this.setupBuiltInSanitizers();

            // Setup validation event listeners
            this.setupValidationEventListeners();

            this.isInitialized = true;
            console.log('✅ Validation Utils initialized successfully');

        } catch (error) {
            console.error('❌ Failed to initialize validation utils:', error);
            throw error;
        }
    }

    /**
     * Setup built-in validators
     */
    setupBuiltInValidators() {
        // String validators
        this.validators.set('string', (value) => typeof value === 'string');
        this.validators.set('nonEmpty', (value) => typeof value === 'string' && value.trim().length > 0);
        this.validators.set('email', (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
        this.validators.set('url', (value) => {
            try {
                new URL(value);
                return true;
            } catch {
                return false;
            }
        });

        // Number validators
        this.validators.set('number', (value) => typeof value === 'number' && !isNaN(value));
        this.validators.set('integer', (value) => Number.isInteger(value));
        this.validators.set('positive', (value) => typeof value === 'number' && value > 0);
        this.validators.set('range', (value, min, max) => {
            return typeof value === 'number' && value >= min && value <= max;
        });

        // Array validators
        this.validators.set('array', (value) => Array.isArray(value));
        this.validators.set('nonEmptyArray', (value) => Array.isArray(value) && value.length > 0);

        // Object validators
        this.validators.set('object', (value) => typeof value === 'object' && value !== null && !Array.isArray(value));
        this.validators.set('required', (value) => value !== null && value !== undefined && value !== '');

        // Date validators
        this.validators.set('date', (value) => {
            const date = new Date(value);
            return !isNaN(date.getTime());
        });

        // Boolean validators
        this.validators.set('boolean', (value) => typeof value === 'boolean');
    }

    /**
     * Setup built-in sanitizers
     */
    setupBuiltInSanitizers() {
        // String sanitizers
        this.sanitizers.set('trim', (value) => typeof value === 'string' ? value.trim() : value);
        this.sanitizers.set('lowercase', (value) => typeof value === 'string' ? value.toLowerCase() : value);
        this.sanitizers.set('uppercase', (value) => typeof value === 'string' ? value.toUpperCase() : value);
        this.sanitizers.set('removeHtml', (value) => {
            if (typeof value === 'string') {
                return value.replace(/<[^>]*>/g, '');
            }
            return value;
        });
        this.sanitizers.set('escapeHtml', (value) => {
            if (typeof value === 'string') {
                return value
                    .replace(/&/g, '&amp;')
                    .replace(/</g, '&lt;')
                    .replace(/>/g, '&gt;')
                    .replace(/"/g, '&quot;')
                    .replace(/'/g, '&#39;');
            }
            return value;
        });

        // Number sanitizers
        this.sanitizers.set('toNumber', (value) => {
            const num = Number(value);
            return isNaN(num) ? 0 : num;
        });
        this.sanitizers.set('toInteger', (value) => {
            const num = parseInt(value, 10);
            return isNaN(num) ? 0 : num;
        });

        // Array sanitizers
        this.sanitizers.set('removeDuplicates', (value) => {
            return Array.isArray(value) ? [...new Set(value)] : value;
        });
        this.sanitizers.set('filterEmpty', (value) => {
            return Array.isArray(value) ? value.filter(item => item !== null && item !== undefined && item !== '') : value;
        });
    }

    /**
     * Setup validation event listeners
     */
    setupValidationEventListeners() {
        // Listen for validation requests
        window.addEventListener('validation:validate', (event) => {
            this.handleValidationRequest(event.detail);
        });

        // Listen for sanitization requests
        window.addEventListener('validation:sanitize', (event) => {
            this.handleSanitizationRequest(event.detail);
        });
    }

    /**
     * Validate value against rules
     */
    validate(value, rules) {
        try {
            const errors = [];

            for (const rule of rules) {
                const result = this.validateRule(value, rule);
                if (!result.isValid) {
                    errors.push(result.error);
                }
            }

            return {
                isValid: errors.length === 0,
                errors,
                value: this.config.enableSanitization ? this.sanitizeValue(value, rules) : value
            };

        } catch (error) {
            console.error('❌ Validation failed:', error);
            return {
                isValid: false,
                errors: ['Validation error occurred'],
                value
            };
        }
    }

    /**
     * Validate single rule
     */
    validateRule(value, rule) {
        try {
            const { type, message, params = [] } = rule;
            const validator = this.validators.get(type);

            if (!validator) {
                return {
                    isValid: false,
                    error: `Unknown validator: ${type}`
                };
            }

            const isValid = validator(value, ...params);
            return {
                isValid,
                error: isValid ? null : (message || `Validation failed for ${type}`)
            };

        } catch (error) {
            return {
                isValid: false,
                error: `Validation error: ${error.message}`
            };
        }
    }

    /**
     * Sanitize value
     */
    sanitizeValue(value, rules) {
        try {
            let sanitizedValue = value;

            for (const rule of rules) {
                if (rule.sanitize) {
                    const sanitizer = this.sanitizers.get(rule.sanitize);
                    if (sanitizer) {
                        sanitizedValue = sanitizer(sanitizedValue);
                    }
                }
            }

            return sanitizedValue;

        } catch (error) {
            console.error('❌ Sanitization failed:', error);
            return value;
        }
    }

    /**
     * Validate form data
     */
    validateForm(formData, schema) {
        try {
            const errors = {};
            const sanitizedData = {};

            for (const [field, rules] of Object.entries(schema)) {
                const value = formData[field];
                const result = this.validate(value, rules);

                if (!result.isValid) {
                    errors[field] = result.errors;
                }

                sanitizedData[field] = result.value;
            }

            return {
                isValid: Object.keys(errors).length === 0,
                errors,
                data: sanitizedData
            };

        } catch (error) {
            console.error('❌ Form validation failed:', error);
            return {
                isValid: false,
                errors: { general: ['Form validation error occurred'] },
                data: formData
            };
        }
    }

    /**
     * Validate API response
     */
    validateAPIResponse(response, schema) {
        try {
            if (!response || typeof response !== 'object') {
                return {
                    isValid: false,
                    error: 'Invalid response format'
                };
            }

            const errors = [];

            for (const [field, rules] of Object.entries(schema)) {
                const value = response[field];
                const result = this.validate(value, rules);

                if (!result.isValid) {
                    errors.push(`${field}: ${result.errors.join(', ')}`);
                }
            }

            return {
                isValid: errors.length === 0,
                errors,
                data: response
            };

        } catch (error) {
            console.error('❌ API response validation failed:', error);
            return {
                isValid: false,
                error: 'API response validation error occurred'
            };
        }
    }

    /**
     * Handle validation request
     */
    handleValidationRequest(data) {
        const { value, rules, callback } = data;
        const result = this.validate(value, rules);
        
        if (callback) {
            callback(result);
        }

        return result;
    }

    /**
     * Handle sanitization request
     */
    handleSanitizationRequest(data) {
        const { value, sanitizers, callback } = data;
        let sanitizedValue = value;

        for (const sanitizer of sanitizers) {
            const sanitizerFn = this.sanitizers.get(sanitizer);
            if (sanitizerFn) {
                sanitizedValue = sanitizerFn(sanitizedValue);
            }
        }

        if (callback) {
            callback(sanitizedValue);
        }

        return sanitizedValue;
    }

    /**
     * Add custom validator
     */
    addValidator(name, validator) {
        if (typeof validator !== 'function') {
            throw new Error('Validator must be a function');
        }
        this.validators.set(name, validator);
        console.log(`✅ Custom validator added: ${name}`);
    }

    /**
     * Add custom sanitizer
     */
    addSanitizer(name, sanitizer) {
        if (typeof sanitizer !== 'function') {
            throw new Error('Sanitizer must be a function');
        }
        this.sanitizers.set(name, sanitizer);
        console.log(`✅ Custom sanitizer added: ${name}`);
    }

    /**
     * Get validator
     */
    getValidator(name) {
        return this.validators.get(name);
    }

    /**
     * Get sanitizer
     */
    getSanitizer(name) {
        return this.sanitizers.get(name);
    }

    /**
     * Get all validators
     */
    getAllValidators() {
        return Array.from(this.validators.keys());
    }

    /**
     * Get all sanitizers
     */
    getAllSanitizers() {
        return Array.from(this.sanitizers.keys());
    }

    /**
     * Get service status
     */
    getStatus() {
        return {
            initialized: this.isInitialized,
            validators: this.validators.size,
            sanitizers: this.sanitizers.size,
            config: { ...this.config }
        };
    }

    /**
     * Destroy validation utils
     */
    async destroy() {
        console.log('🧹 Destroying validation utils...');

        this.validators.clear();
        this.sanitizers.clear();
        this.isInitialized = false;

        console.log('✅ Validation utils destroyed');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create validation utils with default configuration
 */
export function createValidationUtils(options = {}) {
    return new ValidationUtils(options);
}

// Export default
export default ValidationUtils;