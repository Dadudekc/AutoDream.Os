/**
 * Validation Orchestrator - V2 Compliant
 * Main orchestrator coordinating all validation modules
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

import { FieldValidationModule, createFieldValidationModule } from './field-validation-module.js';
import { DataValidationModule, createDataValidationModule } from './data-validation-module.js';
import { FormValidationModule, createFormValidationModule } from './form-validation-module.js';

// ================================
// VALIDATION ORCHESTRATOR
// ================================

/**
 * Main validation orchestrator that coordinates all validation modules
 * Provides the same interface as the original UnifiedValidationSystem
 */
export class ValidationOrchestrator {
    constructor() {
        this.logger = console;
        this.cache = new Map();

        // Initialize validation modules
        this.fieldValidator = createFieldValidationModule();
        this.dataValidator = createDataValidationModule();
        this.formValidator = createFormValidationModule();
    }

    // ================================
    // FIELD VALIDATION METHODS
    // ================================

    /**
     * Validate email address - delegated to field validator
     */
    validateEmail(email) {
        return this.fieldValidator.validateEmail(email);
    }

    /**
     * Validate URL - delegated to field validator
     */
    validateUrl(url) {
        return this.fieldValidator.validateUrl(url);
    }

    /**
     * Validate required fields - delegated to field validator
     */
    validateRequiredFields(data, requiredFields) {
        return this.fieldValidator.validateRequiredFields(data, requiredFields);
    }

    /**
     * Validate numeric range - delegated to field validator
     */
    validateNumericRange(value, min = null, max = null) {
        return this.fieldValidator.validateNumericRange(value, min, max);
    }

    // ================================
    // DATA VALIDATION METHODS
    // ================================

    /**
     * Validate dashboard configuration - delegated to data validator
     */
    validateDashboardConfig(config) {
        return this.dataValidator.validateDashboardConfig(config);
    }

    /**
     * Validate chart data - delegated to data validator
     */
    validateChartData(data) {
        return this.dataValidator.validateChartData(data);
    }

    /**
     * Validate API response - delegated to data validator
     */
    validateApiResponse(response, expectedStructure = {}) {
        return this.dataValidator.validateApiResponse(response, expectedStructure);
    }

    /**
     * Validate trading data - delegated to data validator
     */
    validateTradingData(data) {
        return this.dataValidator.validateTradingData(data);
    }

    /**
     * Validate portfolio data - delegated to data validator
     */
    validatePortfolioData(data) {
        return this.dataValidator.validatePortfolioData(data);
    }

    // ================================
    // FORM VALIDATION METHODS
    // ================================

    /**
     * Validate form input - delegated to form validator
     */
    validateFormInput(value, rules = {}) {
        return this.formValidator.validateFormInput(value, rules);
    }

    /**
     * Validate form fields - delegated to form validator
     */
    validateFormFields(fields) {
        return this.formValidator.validateFormFields(fields);
    }

    /**
     * Sanitize input - delegated to form validator
     */
    sanitizeInput(value, type = 'string') {
        return this.formValidator.sanitizeInput(value, type);
    }

    // ================================
    // UTILITY METHODS
    // ================================

    /**
     * Create type validation utilities - delegated to form validator
     */
    createTypeValidationUtils() {
        return this.formValidator.createTypeValidationUtils();
    }

    /**
     * Log error with context
     */
    logError(message, error) {
        this.logger.error(`[ValidationOrchestrator] ${message}:`, error);
    }

    /**
     * Clear validation cache
     */
    clearCache() {
        this.cache.clear();
        this.logger.info('[ValidationOrchestrator] Cache cleared');
    }

    /**
     * Get orchestrator status
     */
    getStatus() {
        return {
            modules: {
                fieldValidator: !!this.fieldValidator,
                dataValidator: !!this.dataValidator,
                formValidator: !!this.formValidator
            },
            cacheSize: this.cache.size,
            timestamp: new Date().toISOString()
        };
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create validation orchestrator instance
 */
export function createValidationOrchestrator() {
    return new ValidationOrchestrator();
}

/**
 * Create type validation utilities (backward compatibility)
 */
export function createTypeValidationUtils() {
    const orchestrator = new ValidationOrchestrator();
    return orchestrator.createTypeValidationUtils();
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Legacy UnifiedValidationSystem class for backward compatibility
 * @deprecated Use ValidationOrchestrator instead
 */
export class UnifiedValidationSystem extends ValidationOrchestrator {
    constructor() {
        super();
        console.warn('[DEPRECATED] UnifiedValidationSystem is deprecated. Use ValidationOrchestrator instead.');
    }
}

// ================================
// EXPORTS
// ================================

export { FieldValidationModule, DataValidationModule, FormValidationModule };
export { createFieldValidationModule, createDataValidationModule, createFormValidationModule };

export default ValidationOrchestrator;

