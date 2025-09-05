/**
 * Chart State Validator - V2 Compliant Module
 * ==========================================
 * 
 * Core chart state validation logic.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class ChartStateValidator {
    constructor() {
        this.rules = new Map();
        this.logger = console;
    }

    /**
     * Add validation rule
     */
    addRule(name, rule) {
        this.rules.set(name, rule);
    }

    /**
     * Remove validation rule
     */
    removeRule(name) {
        this.rules.delete(name);
    }

    /**
     * Validate chart state
     */
    validateState(state) {
        const results = {
            isValid: true,
            errors: [],
            warnings: []
        };

        for (const [ruleName, rule] of this.rules.entries()) {
            try {
                const result = rule(state);
                
                if (!result.isValid) {
                    results.isValid = false;
                    if (result.severity === 'error') {
                        results.errors.push({
                            rule: ruleName,
                            message: result.message,
                            field: result.field
                        });
                    } else {
                        results.warnings.push({
                            rule: ruleName,
                            message: result.message,
                            field: result.field
                        });
                    }
                }
            } catch (error) {
                results.isValid = false;
                results.errors.push({
                    rule: ruleName,
                    message: `Rule execution error: ${error.message}`,
                    field: 'unknown'
                });
            }
        }

        return results;
    }

    /**
     * Validate specific field
     */
    validateField(state, fieldName) {
        const results = {
            isValid: true,
            errors: [],
            warnings: []
        };

        for (const [ruleName, rule] of this.rules.entries()) {
            try {
                const result = rule(state);
                
                if (!result.isValid && result.field === fieldName) {
                    results.isValid = false;
                    if (result.severity === 'error') {
                        results.errors.push({
                            rule: ruleName,
                            message: result.message,
                            field: result.field
                        });
                    } else {
                        results.warnings.push({
                            rule: ruleName,
                            message: result.message,
                            field: result.field
                        });
                    }
                }
            } catch (error) {
                results.isValid = false;
                results.errors.push({
                    rule: ruleName,
                    message: `Rule execution error: ${error.message}`,
                    field: fieldName
                });
            }
        }

        return results;
    }

    /**
     * Get validation rules
     */
    getRules() {
        return Array.from(this.rules.keys());
    }

    /**
     * Clear all rules
     */
    clearRules() {
        this.rules.clear();
    }

    /**
     * Get rule count
     */
    getRuleCount() {
        return this.rules.size;
    }
}
