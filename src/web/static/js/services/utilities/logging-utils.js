/**
 * Unified Logging System - V2 Compliant Module
 * Centralized logging system for JavaScript utilities
 * Eliminates duplicate logging patterns across all modules
 * MODULAR: ~80 lines (V2 compliant)
 *
 * @author Agent-8 - Integration & Performance Specialist
 * @version 2.0.0 - V2 COMPLIANCE UNIFIED LOGGING
 * @license MIT
 */

export class UnifiedLoggingSystem {
    constructor(name = "UnifiedLogger") {
        this.name = name;
        this.operationTimers = new Map();
    }

    logOperationStart(operationName, extra = {}) {
        const message = `Starting ${operationName}`;
        console.info(`[${this.name}] ${message}`, extra);
        this.operationTimers.set(operationName, Date.now());
    }

    logOperationComplete(operationName, extra = {}) {
        const message = `Completed ${operationName}`;
        console.info(`[${this.name}] ${message}`, extra);

        if (this.operationTimers.has(operationName)) {
            const duration = Date.now() - this.operationTimers.get(operationName);
            this.logPerformanceMetric(`${operationName}_duration`, duration);
            this.operationTimers.delete(operationName);
        }
    }

    logOperationFailed(operationName, error, extra = {}) {
        const message = `Failed to ${operationName}: ${error}`;
        console.error(`[${this.name}] ${message}`, extra);
        this.operationTimers.delete(operationName);
    }

    logPerformanceMetric(metricName, metricValue, extra = {}) {
        const message = `Performance metric: ${metricName} = ${metricValue}`;
        console.info(`[${this.name}] ${message}`, extra);
    }

    logErrorGeneric(moduleName, error, extra = {}) {
        const message = `Error in ${moduleName}: ${error}`;
        console.error(`[${this.name}] ${message}`, extra);
    }

    logValidationStart(itemType, itemId, extra = {}) {
        const message = `Starting validation of ${itemType}: ${itemId}`;
        console.info(`[${this.name}] ${message}`, extra);
    }

    logValidationPassed(itemType, itemId, extra = {}) {
        const message = `Validation passed for ${itemType}: ${itemId}`;
        console.info(`[${this.name}] ${message}`, extra);
    }

    logValidationFailed(itemType, itemId, error, extra = {}) {
        const message = `Validation failed for ${itemType}: ${itemId} - ${error}`;
        console.error(`[${this.name}] ${message}`, extra);
    }
}


