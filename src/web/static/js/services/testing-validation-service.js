/**
 * Testing Validation Service - V2 Compliant
 * Validation and rule evaluation functionality extracted from testing-service.js
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE CORRECTION
 * @license MIT
 */

// ================================
// TESTING VALIDATION SERVICE
// ================================

/**
 * Validation and rule evaluation functionality
 */
class TestingValidationService {
    constructor() {
        this.validationRules = new Map();
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
            console.error(`Component validation failed for ${componentName}:`, error);
            return {
                componentName: componentName,
                success: false,
                error: error.message
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

    /**
     * Evaluate validation rule
     */
    evaluateValidationRule(data, rule) {
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
     * Perform business validation
     */
    performBusinessValidation(validationData) {
        const issues = [];

        // V2 Compliance validation
        if (validationData.v2Compliant === false) {
            issues.push('Component is not V2 compliant');
        }

        // Performance validation
        if (validationData.validationScore < 80) {
            issues.push(`Validation score too low: ${validationData.validationScore}/100`);
        }

        // Code quality validation
        if (validationData.complexity > 10) {
            issues.push(`Code complexity too high: ${validationData.complexity}`);
        }

        return {
            valid: issues.length === 0,
            issues: issues,
            score: validationData.validationScore || 0
        };
    }

    /**
     * Generate validation report
     */
    generateValidationReport(validationData, customValidation, businessValidation) {
        return {
            componentName: validationData.componentName,
            timestamp: new Date().toISOString(),
            overallStatus: validationData.success && customValidation.passed && businessValidation.valid,
            validationBreakdown: {
                basicValidation: validationData.success,
                customValidation: customValidation.passed,
                businessValidation: businessValidation.valid
            },
            issues: [
                ...(validationData.errors || []),
                ...(customValidation.failedRule ? [customValidation.failedRule.message] : []),
                ...businessValidation.issues
            ],
            recommendations: this.generateValidationRecommendations(validationData, businessValidation)
        };
    }

    /**
     * Generate validation recommendations
     */
    generateValidationRecommendations(validationData, businessValidation) {
        const recommendations = [];

        if (businessValidation.score < 80) {
            recommendations.push('Improve validation score by addressing identified issues');
        }

        if (!businessValidation.valid) {
            recommendations.push('Address business validation issues for V2 compliance');
        }

        if (validationData.complexity > 10) {
            recommendations.push('Reduce code complexity through refactoring');
        }

        return recommendations;
    }

    /**
     * Validate test scenario
     */
    validateTestScenario(scenario) {
        if (!scenario || typeof scenario !== 'object') {
            return false;
        }

        // Required fields validation
        const requiredFields = ['name', 'type', 'configuration'];
        for (const field of requiredFields) {
            if (!scenario[field]) {
                return false;
            }
        }

        // Type validation
        const validTypes = ['unit', 'integration', 'performance', 'e2e'];
        if (!validTypes.includes(scenario.type)) {
            return false;
        }

        return true;
    }
}

// ================================
// GLOBAL VALIDATION SERVICE INSTANCE
// ================================

/**
 * Global testing validation service instance
 */
const testingValidationService = new TestingValidationService();

// ================================
// VALIDATION SERVICE API FUNCTIONS
// ================================

/**
 * Validate component
 */
export function validateComponent(componentName, validationRules = []) {
    return testingValidationService.validateComponent(componentName, validationRules);
}

/**
 * Apply custom validation rules
 */
export function applyCustomValidationRules(validationData, customRules) {
    return testingValidationService.applyCustomValidationRules(validationData, customRules);
}

/**
 * Evaluate validation rule
 */
export function evaluateValidationRule(data, rule) {
    return testingValidationService.evaluateValidationRule(data, rule);
}

/**
 * Perform business validation
 */
export function performBusinessValidation(validationData) {
    return testingValidationService.performBusinessValidation(validationData);
}

/**
 * Generate validation report
 */
export function generateValidationReport(validationData, customValidation, businessValidation) {
    return testingValidationService.generateValidationReport(validationData, customValidation, businessValidation);
}

/**
 * Validate test scenario
 */
export function validateTestScenario(scenario) {
    return testingValidationService.validateTestScenario(scenario);
}

// ================================
// EXPORTS
// ================================

export { TestingValidationService, testingValidationService };
export default testingValidationService;
