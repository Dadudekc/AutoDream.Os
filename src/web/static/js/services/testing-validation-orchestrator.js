/**
 * Testing Validation Orchestrator - V2 Compliant
 * Main orchestrator for testing validation service
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { createComponentValidationModule } from './component-validation-module.js';
import { createRuleEvaluationModule } from './rule-evaluation-module.js';
import { createBusinessValidationModule } from './business-validation-module.js';
import { createValidationReportingModule } from './validation-reporting-module.js';
import { createScenarioValidationModule } from './scenario-validation-module.js';

// ================================
// TESTING VALIDATION ORCHESTRATOR
// ================================

/**
 * Main orchestrator for testing validation service
 */
export class TestingValidationOrchestrator {
    constructor() {
        this.logger = console;

        // Initialize modules
        this.componentValidation = createComponentValidationModule();
        this.ruleEvaluation = createRuleEvaluationModule();
        this.businessValidation = createBusinessValidationModule();
        this.validationReporting = createValidationReportingModule();
        this.scenarioValidation = createScenarioValidationModule();
    }

    /**
     * Validate component with rules
     */
    async validateComponent(componentName, validationRules = []) {
        return this.componentValidation.validateComponent(componentName, validationRules);
    }

    /**
     * Apply custom validation rules
     */
    applyCustomValidationRules(validationData, customRules) {
        return this.componentValidation.applyCustomValidationRules(validationData, customRules);
    }

    /**
     * Evaluate validation rule
     */
    evaluateValidationRule(data, rule) {
        return this.ruleEvaluation.evaluateValidationRule(data, rule);
    }

    /**
     * Perform business validation
     */
    performBusinessValidation(validationData) {
        return this.businessValidation.performBusinessValidation(validationData);
    }

    /**
     * Generate validation report
     */
    generateValidationReport(validationData, customValidation, businessValidation) {
        return this.validationReporting.generateValidationReport(validationData, customValidation, businessValidation);
    }

    /**
     * Generate business validation report
     */
    generateBusinessValidationReport(validationData) {
        return this.businessValidation.generateBusinessValidationReport(validationData);
    }

    /**
     * Validate test scenario
     */
    validateTestScenario(scenario) {
        return this.scenarioValidation.validateTestScenario(scenario);
    }

    /**
     * Generate actionable insights
     */
    generateActionableInsights(validationData, trends) {
        const businessValidation = this.performBusinessValidation(validationData);
        return this.businessValidation.generateActionableInsights(businessValidation, trends);
    }

    /**
     * Export validation report
     */
    exportValidationReport(report, format = 'json') {
        return this.validationReporting.exportReport(report, format);
    }

    /**
     * Register custom rule type
     */
    registerCustomRuleType(type, validator) {
        return this.ruleEvaluation.registerRuleType(type, validator);
    }

    /**
     * Register custom business rule
     */
    registerCustomBusinessRule(name, validator) {
        return this.businessValidation.registerBusinessRule(name, validator);
    }

    /**
     * Register scenario type
     */
    registerScenarioType(type, validator) {
        return this.scenarioValidation.registerScenarioType(type, validator);
    }

    /**
     * Generate scenario template
     */
    generateScenarioTemplate(type) {
        return this.scenarioValidation.generateScenarioTemplate(type);
    }

    /**
     * Validate scenario compatibility
     */
    validateScenarioCompatibility(scenarios) {
        return this.scenarioValidation.validateScenarioCompatibility(scenarios);
    }

    /**
     * Get validation metrics
     */
    getValidationMetrics() {
        return {
            ruleTypes: this.ruleEvaluation.getAvailableRuleTypes(),
            businessRules: this.businessValidation.getBusinessValidationMetrics(),
            scenarioTypes: this.scenarioValidation.getAvailableScenarioTypes(),
            reportTemplates: Array.from(this.validationReporting.reportTemplates.keys())
        };
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: ['componentValidation', 'ruleEvaluation', 'businessValidation', 'validationReporting', 'scenarioValidation'],
            metrics: this.getValidationMetrics(),
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy TestingValidationService class for backward compatibility
 * @deprecated Use TestingValidationOrchestrator instead
 */
export class TestingValidationService extends TestingValidationOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] TestingValidationService is deprecated. Use TestingValidationOrchestrator instead.');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create testing validation orchestrator instance
 */
export function createTestingValidationOrchestrator() {
    return new TestingValidationOrchestrator();
}

/**
 * Create legacy testing validation service (backward compatibility)
 */
export function createTestingValidationService() {
    return new TestingValidationService();
}

