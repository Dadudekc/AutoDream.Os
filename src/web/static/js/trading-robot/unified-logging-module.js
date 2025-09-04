/**
 * Unified Logging Module - V2 Compliant
 * Centralized logging system for trading robot components
 *
 * @author Agent-7 - Web Development Specialist, Agent-1 - Integration & Core Systems
 * @version 1.0.0 - V2 COMPLIANCE MODULARIZATION
 * @license MIT
 */

// ================================
// UNIFIED LOGGING SYSTEM
// ================================

/**
 * Enhanced Unified Logging System - Agent-1 Integration & Core Systems
 * Eliminates duplicate logging patterns across trading robot services
 * Integrates with unified-logging-system.py patterns for cross-agent coordination
 */
export class UnifiedLoggingSystem {
    constructor(name = "TradingRobotComponent") {
        this.name = name;
        this.operationTimers = new Map();
        this.correlationContext = new Map();
        this.performanceMetrics = new Map();
        this.agentId = "Agent-1";
        this.integrationStatus = "ACTIVE";
        this.logger = console;
    }

    /**
     * Log operation start
     */
    logOperationStart(operationName, extra = {}) {
        const correlationId = this._generateCorrelationId(operationName);
        const message = `Starting ${operationName}`;

        this.logger.info(`[${this.name}] ${message}`, {
            ...extra,
            correlationId,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            operation: operationName,
            level: 'INFO'
        });

        this.operationTimers.set(operationName, Date.now());
        this.correlationContext.set(operationName, { correlationId });
    }

    /**
     * Log operation completion
     */
    logOperationComplete(operationName, extra = {}) {
        const correlationId = this.correlationContext.get(operationName)?.correlationId;
        const message = `Completed ${operationName}`;

        this.logger.info(`[${this.name}] ${message}`, {
            ...extra,
            correlationId,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            operation: operationName,
            level: 'INFO'
        });

        if (this.operationTimers.has(operationName)) {
            const duration = Date.now() - this.operationTimers.get(operationName);
            this.logPerformanceMetric(`${operationName}_duration`, duration, { correlationId });
            this.operationTimers.delete(operationName);
            this.correlationContext.delete(operationName);
        }
    }

    /**
     * Log operation failure
     */
    logOperationFailed(operationName, error, extra = {}) {
        const correlationId = this.correlationContext.get(operationName)?.correlationId;
        const message = `Failed to ${operationName}: ${error}`;

        this.logger.error(`[${this.name}] ${message}`, {
            ...extra,
            correlationId,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            operation: operationName,
            error: error.toString(),
            level: 'ERROR'
        });

        this.operationTimers.delete(operationName);
        this.correlationContext.delete(operationName);
    }

    /**
     * Log performance metric
     */
    logPerformanceMetric(metricName, metricValue, extra = {}) {
        const message = `Performance metric: ${metricName} = ${metricValue}`;

        this.logger.info(`[${this.name}] ${message}`, {
            ...extra,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            metric: metricName,
            value: metricValue,
            level: 'INFO'
        });

        this.performanceMetrics.set(metricName, {
            value: metricValue,
            timestamp: new Date().toISOString(),
            agentId: this.agentId
        });
    }

    /**
     * Log unified systems deployment
     */
    logUnifiedSystemsDeployment(deploymentType, status, extra = {}) {
        const message = `Unified systems deployment: ${deploymentType} - ${status}`;

        this.logger.info(`[${this.name}] ${message}`, {
            ...extra,
            agentId: this.agentId,
            timestamp: new Date().toISOString(),
            deploymentType,
            status,
            level: 'INFO',
            deploymentCategory: 'unified_systems'
        });
    }

    /**
     * Get performance metrics
     */
    getPerformanceMetrics() {
        return Object.fromEntries(this.performanceMetrics);
    }

    /**
     * Get correlation context
     */
    getCorrelationContext() {
        return Object.fromEntries(this.correlationContext);
    }

    /**
     * Clear performance metrics
     */
    clearPerformanceMetrics() {
        this.performanceMetrics.clear();
    }

    /**
     * Clear correlation context
     */
    clearCorrelationContext() {
        this.correlationContext.clear();
        this.operationTimers.clear();
    }

    /**
     * Generate correlation ID
     */
    _generateCorrelationId(operationName) {
        return `${this.agentId}_${operationName}_${Date.now()}`;
    }

    /**
     * Set logger instance
     */
    setLogger(logger) {
        this.logger = logger;
    }

    /**
     * Get logger statistics
     */
    getStatistics() {
        return {
            name: this.name,
            agentId: this.agentId,
            integrationStatus: this.integrationStatus,
            activeOperations: this.operationTimers.size,
            performanceMetrics: this.performanceMetrics.size,
            correlationContexts: this.correlationContext.size
        };
    }

    /**
     * Cleanup logging system
     */
    cleanup() {
        this.clearPerformanceMetrics();
        this.clearCorrelationContext();
        this.logger.log('🧹 Unified Logging System cleanup complete');
    }
}

// ================================
// FACTORY FUNCTIONS
// ================================

/**
 * Create unified logging system instance
 */
export function createUnifiedLoggingSystem(name) {
    return new UnifiedLoggingSystem(name);
}

/**
 * Get default logging system
 */
export function getDefaultLoggingSystem() {
    return createUnifiedLoggingSystem("TradingRobotDefault");
}

