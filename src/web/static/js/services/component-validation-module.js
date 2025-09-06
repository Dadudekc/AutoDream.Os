/**
 * Component Validation Module - V2 Compliant
 * Core component validation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// COMPONENT VALIDATION MODULE
// ================================

/**
 * Core component validation functionality
 */
export class ComponentValidationModule {
    constructor() {
        this.logger = console;
    }

    /**
     * Validate component with rules
     */
    async validateComponent(componentName, validationRules = []) {
        try {
            const results = {
                componentName: componentName,
                totalRules: validationRules.length,
                passed: 0,
                failed: 0,
                ruleResults: []
            };

            for (const rule of validationRules) {
                const ruleResult = await this.evaluateValidationRule({}, rule);
                results.ruleResults.push(ruleResult);

                if (ruleResult.passed) {
                    results.passed++;
                } else {
                    results.failed++;
                }
            }

            results.success = results.failed === 0;
            return results;

        } catch (error) {
            this.logger.error(`Component validation failed for ${componentName}:`, error);
            return {
                componentName: componentName,
                success: false,
                error: error.message
            };
        }
    }

    /**
     * Evaluate validation rule
     */
    async evaluateValidationRule(data, rule) {
        try {
            switch (rule.type) {
                case 'required':
                    if (!data[rule.field]) {
                        return {
                            passed: false,
                            rule: rule,
                            message: `${rule.field} is required`
                        };
                    }
                    break;

                case 'min':
                    if (data[rule.field] < rule.value) {
                        return {
                            passed: false,
                            rule: rule,
                            message: `${rule.field} must be at least ${rule.value}`
                        };
                    }
                    break;

                case 'max':
                    if (data[rule.field] > rule.value) {
                        return {
                            passed: false,
                            rule: rule,
                            message: `${rule.field} must be at most ${rule.value}`
                        };
                    }
                    break;

                case 'regex':
                    const regex = new RegExp(rule.pattern);
                    if (!regex.test(data[rule.field])) {
                        return {
                            passed: false,
                            rule: rule,
                            message: `${rule.field} does not match required pattern`
                        };
                    }
                    break;

                default:
                    return {
                        passed: false,
                        rule: rule,
                        message: `Unknown validation rule type: ${rule.type}`
                    };
            }

            return {
                passed: true,
                rule: rule,
                message: 'Validation passed'
            };

        } catch (error) {
            return {
                passed: false,
                rule: rule,
                message: `Validation error: ${error.message}`
            };
        }
    }

    /**
     * Apply custom validation rules
     */
    applyCustomValidationRules(validationData, customRules) {
        if (!customRules || customRules.length === 0) {
            return { passed: true, results: [] };
        }

        const results = [];

        for (const rule of customRules) {
            const ruleResult = this.evaluateValidationRule(validationData, rule);
            results.push(ruleResult);

            if (!ruleResult.passed) {
                return {
                    passed: false,
                    failedRule: rule,
                    results: results
                };
            }
        }

        return {
            passed: true,
            results: results
        };
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create component validation module instance
 */
export function createComponentValidationModule() {
    return new ComponentValidationModule();
}
