/**
 * Validation Service Module - V2 Compliant
 * Handles data validation and form validation
 * V2 COMPLIANCE: <200 lines, single responsibility
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - MODULAR COMPONENT
 * @license MIT
 */

class ValidationService {
    constructor(config = {}) {
        this.config = { strictMode: false, maxErrors: 10, ...config };
        this.errors = [];
        this.rules = new Map();
        this.isInitialized = false;
    }

    async initialize() {
        if (this.isInitialized) return;
        console.log('✅ Initializing Validation Service...');
        this.setupDefaultRules();
        this.isInitialized = true;
    }

    setupDefaultRules() {
        this.addRule('required', (value) => value !== null && value !== undefined && value !== '');
        this.addRule('email', (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value));
        this.addRule('minLength', (value, param) => value.length >= param);
        this.addRule('maxLength', (value, param) => value.length <= param);
        this.addRule('numeric', (value) => !isNaN(value) && !isNaN(parseFloat(value)));
        this.addRule('url', (value) => /^https?:\/\/.+/.test(value));
    }

    addRule(name, validator) {
        this.rules.set(name, validator);
    }

    validate(data, rules = {}) {
        this.errors = [];

        for (const [field, fieldRules] of Object.entries(rules)) {
            const value = data[field];
            const fieldErrors = this.validateField(value, fieldRules, field);

            if (fieldErrors.length > 0) {
                this.errors.push(...fieldErrors);
                if (this.errors.length >= this.config.maxErrors) break;
            }
        }

        return this.errors.length === 0;
    }

    validateField(value, rules, fieldName = 'field') {
        const errors = [];

        if (!Array.isArray(rules)) {
            rules = [rules];
        }

        for (const rule of rules) {
            if (typeof rule === 'string') {
                if (!this.applyRule(rule, value)) {
                    errors.push(`${fieldName} is invalid (${rule})`);
                }
            } else if (typeof rule === 'object') {
                const { type, param, message } = rule;
                if (!this.applyRule(type, value, param)) {
                    errors.push(message || `${fieldName} is invalid (${type})`);
                }
            }
        }

        return errors;
    }

    applyRule(ruleName, value, param) {
        const rule = this.rules.get(ruleName);
        if (!rule) {
            console.warn(`Validation rule '${ruleName}' not found`);
            return true;
        }

        try {
            return rule(value, param);
        } catch (error) {
            console.error(`Error applying validation rule '${ruleName}':`, error);
            return false;
        }
    }

    validateForm(formData) {
        const errors = {};

        for (const [field, value] of Object.entries(formData)) {
            const fieldErrors = this.validateField(value, ['required'], field);
            if (fieldErrors.length > 0) {
                errors[field] = fieldErrors;
            }
        }

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    validateEmail(email) {
        return this.validateField(email, ['required', 'email'], 'email').length === 0;
    }

    validatePassword(password, minLength = 8) {
        const rules = [
            'required',
            { type: 'minLength', param: minLength, message: `Password must be at least ${minLength} characters` },
            { type: 'maxLength', param: 128, message: 'Password is too long' }
        ];
        return this.validateField(password, rules, 'password').length === 0;
    }

    validateURL(url) {
        return this.validateField(url, ['required', 'url'], 'url').length === 0;
    }

    validateNumeric(value, min = null, max = null) {
        const rules = ['required', 'numeric'];

        if (min !== null) {
            rules.push({ type: 'min', param: min, message: `Value must be at least ${min}` });
        }
        if (max !== null) {
            rules.push({ type: 'max', param: max, message: `Value must be at most ${max}` });
        }

        return this.validateField(value, rules, 'number').length === 0;
    }

    getErrors() {
        return [...this.errors];
    }

    clearErrors() {
        this.errors = [];
    }

    hasErrors() {
        return this.errors.length > 0;
    }

    getErrorCount() {
        return this.errors.length;
    }

    getStats() {
        return {
            rulesCount: this.rules.size,
            errorsCount: this.errors.length,
            initialized: this.isInitialized
        };
    }

    async destroy() {
        this.clearErrors();
        this.rules.clear();
        this.isInitialized = false;
        console.log('🧹 Validation service cleaned up');
    }
}

export { ValidationService };
export default ValidationService;
