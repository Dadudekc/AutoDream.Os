/**
 * Rule Evaluation Module - V2 Compliant
 * Validation rule evaluation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// RULE EVALUATION MODULE
// ================================

/**
 * Validation rule evaluation functionality
 */
export class RuleEvaluationModule {
    constructor() {
        this.logger = console;
        this.ruleTypes = new Map();
        this.customRules = new Map();
    }

    /**
     * Register custom rule type
     */
    registerRuleType(type, validator) {
        try {
            this.ruleTypes.set(type, validator);
            return true;
        } catch (error) {
            this.logger.error(`Failed to register rule type ${type}:`, error);
            return false;
        }
    }

    /**
     * Evaluate validation rule
     */
    evaluateValidationRule(data, rule) {
        try {
            // Check for custom rule type first
            if (this.ruleTypes.has(rule.type)) {
                const customValidator = this.ruleTypes.get(rule.type);
                return customValidator(data, rule);
            }

            // Handle built-in rule types
            switch (rule.type) {
                case 'required':
                    return this.evaluateRequiredRule(data, rule);

                case 'min':
                    return this.evaluateMinRule(data, rule);

                case 'max':
                    return this.evaluateMaxRule(data, rule);

                case 'range':
                    return this.evaluateRangeRule(data, rule);

                case 'regex':
                    return this.evaluateRegexRule(data, rule);

                case 'type':
                    return this.evaluateTypeRule(data, rule);

                case 'length':
                    return this.evaluateLengthRule(data, rule);

                case 'custom':
                    return this.evaluateCustomRule(data, rule);

                default:
                    return {
                        passed: false,
                        rule: rule,
                        message: `Unknown validation rule type: ${rule.type}`
                    };
            }
        } catch (error) {
            return {
                passed: false,
                rule: rule,
                message: `Rule evaluation error: ${error.message}`
            };
        }
    }

    /**
     * Evaluate required rule
     */
    evaluateRequiredRule(data, rule) {
        const value = data[rule.field];
        const passed = value !== undefined && value !== null && value !== '';

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Required field is present' : `${rule.field} is required`
        };
    }

    /**
     * Evaluate minimum value rule
     */
    evaluateMinRule(data, rule) {
        const value = data[rule.field];
        const passed = value >= rule.value;

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Value meets minimum requirement' : `${rule.field} must be at least ${rule.value}`
        };
    }

    /**
     * Evaluate maximum value rule
     */
    evaluateMaxRule(data, rule) {
        const value = data[rule.field];
        const passed = value <= rule.value;

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Value meets maximum requirement' : `${rule.field} must be at most ${rule.value}`
        };
    }

    /**
     * Evaluate range rule
     */
    evaluateRangeRule(data, rule) {
        const value = data[rule.field];
        const passed = value >= rule.min && value <= rule.max;

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Value is within range' : `${rule.field} must be between ${rule.min} and ${rule.max}`
        };
    }

    /**
     * Evaluate regex rule
     */
    evaluateRegexRule(data, rule) {
        const value = data[rule.field];
        const regex = new RegExp(rule.pattern);
        const passed = regex.test(value);

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Value matches pattern' : `${rule.field} does not match required pattern`
        };
    }

    /**
     * Evaluate type rule
     */
    evaluateTypeRule(data, rule) {
        const value = data[rule.field];
        let passed = false;

        switch (rule.expectedType) {
            case 'string':
                passed = typeof value === 'string';
                break;
            case 'number':
                passed = typeof value === 'number' && !isNaN(value);
                break;
            case 'boolean':
                passed = typeof value === 'boolean';
                break;
            case 'object':
                passed = typeof value === 'object' && value !== null;
                break;
            case 'array':
                passed = Array.isArray(value);
                break;
            default:
                passed = typeof value === rule.expectedType;
        }

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Value has correct type' : `${rule.field} must be of type ${rule.expectedType}`
        };
    }

    /**
     * Evaluate length rule
     */
    evaluateLengthRule(data, rule) {
        const value = data[rule.field];
        const length = value ? value.length : 0;
        const passed = length >= (rule.min || 0) && length <= (rule.max || Infinity);

        return {
            passed: passed,
            rule: rule,
            message: passed ? 'Length is within limits' : `${rule.field} length must be between ${rule.min || 0} and ${rule.max || 'unlimited'}`
        };
    }

    /**
     * Evaluate custom rule
     */
    evaluateCustomRule(data, rule) {
        try {
            const customValidator = this.customRules.get(rule.validator);
            if (!customValidator) {
                return {
                    passed: false,
                    rule: rule,
                    message: `Custom validator '${rule.validator}' not found`
                };
            }

            return customValidator(data, rule);
        } catch (error) {
            return {
                passed: false,
                rule: rule,
                message: `Custom validation error: ${error.message}`
            };
        }
    }

    /**
     * Register custom rule
     */
    registerCustomRule(name, validator) {
        try {
            this.customRules.set(name, validator);
            return true;
        } catch (error) {
            this.logger.error(`Failed to register custom rule ${name}:`, error);
            return false;
        }
    }

    /**
     * Get available rule types
     */
    getAvailableRuleTypes() {
        return [
            'required', 'min', 'max', 'range', 'regex', 'type', 'length', 'custom',
            ...Array.from(this.ruleTypes.keys())
        ];
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create rule evaluation module instance
 */
export function createRuleEvaluationModule() {
    return new RuleEvaluationModule();
}

