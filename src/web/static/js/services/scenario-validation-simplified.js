/**
 * Scenario Validation Simplified - V2 Compliant
 * Simplified orchestrator for scenario validation functionality
 *
 * @author Agent-7 - Web Development Specialist
 * @version 2.0.0 - V2 COMPLIANCE SIMPLIFICATION
 * @license MIT
 */

import { createUnifiedLoggingSystem } from '../trading-robot/unified-logging-module.js';

// ================================
// SCENARIO VALIDATION SIMPLIFIED
// ================================

/**
 * Simplified scenario validation functionality
 */
export class ScenarioValidationSimplified {
    constructor() {
        // Initialize unified logging
        this.logger = createUnifiedLoggingSystem("ScenarioValidationSimplified");

        // Log unified systems deployment
        this.logger.logUnifiedSystemsDeployment('scenario_validation_simplified', 'active', {
            version: '2.0.0',
            agentId: 'Agent-7',
            integrationStatus: 'ACTIVE'
        });

        // Initialize validation state
        this.scenarioTypes = new Map([
            ['unit', { description: 'Unit test scenarios', requiredFields: ['name', 'type'] }],
            ['integration', { description: 'Integration test scenarios', requiredFields: ['name', 'type', 'services'] }],
            ['performance', { description: 'Performance test scenarios', requiredFields: ['name', 'type', 'metrics'] }],
            ['e2e', { description: 'End-to-end test scenarios', requiredFields: ['name', 'type', 'steps'] }]
        ]);

        this.validationRules = new Map([
            ['name', { type: 'string', minLength: 1, maxLength: 100 }],
            ['type', { type: 'string', enum: Array.from(this.scenarioTypes.keys()) }],
            ['configuration', { type: 'object', required: true }],
            ['timeout', { type: 'number', min: 1000, max: 300000 }],
            ['retries', { type: 'number', min: 0, max: 10 }]
        ]);
    }

    /**
     * Initialize simplified scenario validation
     */
    initialize() {
        this.logger.logOperationStart('scenarioValidationSimplifiedInitialization');
        this.logger.logOperationComplete('scenarioValidationSimplifiedInitialization', {
            scenarioTypes: this.scenarioTypes.size,
            validationRules: this.validationRules.size
        });
    }

    /**
     * Validate test scenario
     */
    validateTestScenario(scenario) {
        try {
            if (!scenario || typeof scenario !== 'object') {
                return {
                    valid: false,
                    errors: ['Scenario must be a valid object']
                };
            }

            const errors = [];

            // Required fields validation
            const requiredFields = ['name', 'type', 'configuration'];
            for (const field of requiredFields) {
                if (!scenario[field]) {
                    errors.push(`Required field '${field}' is missing`);
                }
            }

            // Type validation
            if (scenario.type) {
                const validTypes = Array.from(this.scenarioTypes.keys());
                if (!validTypes.includes(scenario.type)) {
                    errors.push(`Invalid scenario type '${scenario.type}'. Valid types: ${validTypes.join(', ')}`);
                }
            }

            // Field validation
            for (const [field, value] of Object.entries(scenario)) {
                const rule = this.validationRules.get(field);
                if (rule) {
                    const fieldErrors = this.validateField(field, value, rule);
                    errors.push(...fieldErrors);
                }
            }

            // Type-specific validation
            if (scenario.type && this.scenarioTypes.has(scenario.type)) {
                const typeConfig = this.scenarioTypes.get(scenario.type);
                const typeErrors = this.validateTypeSpecific(scenario, typeConfig);
                errors.push(...typeErrors);
            }

            return {
                valid: errors.length === 0,
                errors,
                warnings: this.generateWarnings(scenario),
                metadata: {
                    validatedAt: new Date().toISOString(),
                    scenarioType: scenario.type,
                    fieldCount: Object.keys(scenario).length
                }
            };
        } catch (error) {
            this.logger.logOperationFailed('validateTestScenario', error);
            return {
                valid: false,
                errors: [`Validation error: ${error.message}`]
            };
        }
    }

    /**
     * Validate individual field
     */
    validateField(field, value, rule) {
        const errors = [];

        // Type validation
        if (rule.type && typeof value !== rule.type) {
            errors.push(`Field '${field}' must be of type ${rule.type}`);
        }

        // String validations
        if (rule.type === 'string') {
            if (rule.minLength && value.length < rule.minLength) {
                errors.push(`Field '${field}' must be at least ${rule.minLength} characters`);
            }
            if (rule.maxLength && value.length > rule.maxLength) {
                errors.push(`Field '${field}' must be at most ${rule.maxLength} characters`);
            }
        }

        // Number validations
        if (rule.type === 'number') {
            if (rule.min !== undefined && value < rule.min) {
                errors.push(`Field '${field}' must be at least ${rule.min}`);
            }
            if (rule.max !== undefined && value > rule.max) {
                errors.push(`Field '${field}' must be at most ${rule.max}`);
            }
        }

        // Enum validation
        if (rule.enum && !rule.enum.includes(value)) {
            errors.push(`Field '${field}' must be one of: ${rule.enum.join(', ')}`);
        }

        // Required validation
        if (rule.required && (value === undefined || value === null)) {
            errors.push(`Field '${field}' is required`);
        }

        return errors;
    }

    /**
     * Validate type-specific requirements
     */
    validateTypeSpecific(scenario, typeConfig) {
        const errors = [];

        // Check type-specific required fields
        if (typeConfig.requiredFields) {
            for (const field of typeConfig.requiredFields) {
                if (!scenario[field]) {
                    errors.push(`Field '${field}' is required for ${scenario.type} scenarios`);
                }
            }
        }

        // Type-specific validations
        switch (scenario.type) {
            case 'performance':
                if (scenario.metrics && !Array.isArray(scenario.metrics)) {
                    errors.push('Performance scenarios must have metrics as an array');
                }
                break;
            case 'e2e':
                if (scenario.steps && !Array.isArray(scenario.steps)) {
                    errors.push('E2E scenarios must have steps as an array');
                }
                break;
        }

        return errors;
    }

    /**
     * Generate warnings for scenario
     */
    generateWarnings(scenario) {
        const warnings = [];

        // Check for potentially problematic configurations
        if (scenario.timeout && scenario.timeout > 120000) {
            warnings.push('Timeout is set to a high value, consider reducing for better performance');
        }

        if (scenario.retries && scenario.retries > 3) {
            warnings.push('High retry count may indicate unreliable test, consider improving stability');
        }

        if (scenario.name && scenario.name.length < 5) {
            warnings.push('Scenario name is very short, consider using a more descriptive name');
        }

        return warnings;
    }

    /**
     * Add custom scenario type
     */
    addScenarioType(type, config) {
        this.scenarioTypes.set(type, config);
        this.logger.log(`Added custom scenario type: ${type}`);
    }

    /**
     * Add custom validation rule
     */
    addValidationRule(field, rule) {
        this.validationRules.set(field, rule);
        this.logger.log(`Added custom validation rule for field: ${field}`);
    }

    /**
     * Get scenario types
     */
    getScenarioTypes() {
        return Object.fromEntries(this.scenarioTypes);
    }

    /**
     * Get validation rules
     */
    getValidationRules() {
        return Object.fromEntries(this.validationRules);
    }

    /**
     * Get statistics
     */
    getStatistics() {
        return {
            scenarioTypes: this.scenarioTypes.size,
            validationRules: this.validationRules.size,
            loggerStats: this.logger.getStatistics(),
            timestamp: new Date().toISOString()
        };
    }

    /**
     * Cleanup simplified validation
     */
    cleanup() {
        this.scenarioTypes.clear();
        this.validationRules.clear();
        this.logger.cleanup();
        this.logger.log('🧹 Scenario Validation Simplified cleanup complete');
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy ScenarioValidationModule class for backward compatibility
 * @deprecated Use ScenarioValidationSimplified instead
 */
export class ScenarioValidationModule extends ScenarioValidationSimplified {
    constructor() {
        super();
        console.warn('[DEPRECATED] ScenarioValidationModule is deprecated. Use ScenarioValidationSimplified instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create simplified scenario validation instance
 */
export function createScenarioValidationSimplified() {
    const validation = new ScenarioValidationSimplified();
    validation.initialize();
    return validation;
}

/**
 * Create legacy scenario validation module (backward compatibility)
 */
export function createScenarioValidationModule() {
    const module = new ScenarioValidationModule();
    module.initialize();
    return module;
}

