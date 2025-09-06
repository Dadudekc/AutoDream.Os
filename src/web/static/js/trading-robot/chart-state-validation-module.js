/**
 * Chart State Validation Module - V2 Compliant Module
 * ==================================================
 *
 * Main chart state validation module that coordinates all validation components.
 *
 * V2 Compliance: < 300 lines, single responsibility.
 *
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

import { ChartStateValidator } from './validator.js';
import { ChartStateRules } from './rules.js';
import { ChartStateLogger } from './logger.js';

export class ChartStateValidationModule {
    constructor() {
        this.validator = new ChartStateValidator();
        this.rules = new ChartStateRules();
        this.logger = new ChartStateLogger();

        this.initializeRules();
    }

    /**
     * Initialize validation rules
     */
    initializeRules() {
        const allRules = this.rules.getAllRules();

        // Add all rules to validator
        Object.values(allRules).forEach(category => {
            Object.entries(category).forEach(([name, rule]) => {
                this.validator.addRule(name, rule);
            });
        });

        this.logger.info('Chart state validation rules initialized', {
            ruleCount: this.validator.getRuleCount()
        });
    }

    /**
     * Validate chart state
     */
    validateState(state) {
        this.logger.debug('Starting chart state validation', { state });

        const startTime = Date.now();
        const result = this.validator.validateState(state);
        const validationTime = Date.now() - startTime;

        this.logger.info('Chart state validation completed', {
            isValid: result.isValid,
            errorCount: result.errors.length,
            warningCount: result.warnings.length,
            validationTime
        });

        if (!result.isValid) {
            this.logger.warn('Chart state validation failed', {
                errors: result.errors,
                warnings: result.warnings
            });
        }

        return result;
    }

    /**
     * Validate specific field
     */
    validateField(state, fieldName) {
        this.logger.debug('Validating chart state field', { fieldName });

        const result = this.validator.validateField(state, fieldName);

        this.logger.info('Field validation completed', {
            field: fieldName,
            isValid: result.isValid,
            errorCount: result.errors.length,
            warningCount: result.warnings.length
        });

        return result;
    }

    /**
     * Get validation rules
     */
    getValidationRules() {
        return this.validator.getRules();
    }

    /**
     * Add custom rule
     */
    addCustomRule(name, rule) {
        const validation = this.rules.validateRuleDefinition(rule);

        if (!validation.isValid) {
            this.logger.error('Failed to add custom rule', {
                name,
                error: validation.message
            });
            return false;
        }

        this.validator.addRule(name, rule);
        this.logger.info('Custom rule added', { name });
        return true;
    }

    /**
     * Remove custom rule
     */
    removeCustomRule(name) {
        this.validator.removeRule(name);
        this.logger.info('Custom rule removed', { name });
    }

    /**
     * Get validation statistics
     */
    getValidationStats() {
        return {
            ruleCount: this.validator.getRuleCount(),
            logStats: this.logger.getLogStats(),
            recentLogs: this.logger.getRecentLogs(10)
        };
    }

    /**
     * Get validation errors
     */
    getValidationErrors() {
        return this.logger.getErrorLogs();
    }

    /**
     * Get validation warnings
     */
    getValidationWarnings() {
        return this.logger.getWarningLogs();
    }

    /**
     * Clear validation logs
     */
    clearValidationLogs() {
        this.logger.clearLogs();
    }

    /**
     * Export validation data
     */
    exportValidationData() {
        return {
            rules: this.getValidationRules(),
            stats: this.getValidationStats(),
            logs: this.logger.exportLogs(),
            exportedAt: new Date().toISOString()
        };
    }

    /**
     * Reset validation module
     */
    reset() {
        this.validator.clearRules();
        this.logger.clearLogs();
        this.initializeRules();

        this.logger.info('Chart state validation module reset');
    }

    /**
     * Set log level
     */
    setLogLevel(level) {
        this.logger.setLogLevel(level);
    }

    /**
     * Get log level
     */
    getLogLevel() {
        return this.logger.getLogLevel();
    }
}
