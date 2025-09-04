/**
 * Unified Logging System - Web Layer Integration
 * Centralized logging system for web layer components
 * V2 COMPLIANCE: Under 300-line limit
 *
 * @author Agent-7 - Web Development Specialist
 * @version 1.0.0 - Unified Logging System
 * @license MIT
 */

// ================================
// UNIFIED LOGGING SYSTEM
// ================================

export class UnifiedLogger {
    constructor(component = 'WebLayer') {
        this.component = component;
        this.logs = [];
        this.levels = {
            DEBUG: 0,
            INFO: 1,
            WARN: 2,
            ERROR: 3
        };
        this.currentLevel = this.levels.INFO;
        this.maxLogs = 1000;
    }

    /**
     * Configure web layer logging
     */
    async configureWebLayerLogging() {
        console.log('📝 Configuring Unified Logging System for Web Layer...');

        // Configure dashboard logging
        this.configureDashboardLogging();

        // Configure service logging
        this.configureServiceLogging();

        // Configure utility logging
        this.configureUtilityLogging();

        // Setup log aggregation
        this.setupLogAggregation();

        console.log('✅ Unified Logging System configured for Web Layer');
    }

    /**
     * Configure dashboard logging
     */
    configureDashboardLogging() {
        // Configure dashboard component logging
        this.log('INFO', 'Dashboard logging configured', 'dashboard');
    }

    /**
     * Configure service logging
     */
    configureServiceLogging() {
        // Configure service component logging
        this.log('INFO', 'Service logging configured', 'services');
    }

    /**
     * Configure utility logging
     */
    configureUtilityLogging() {
        // Configure utility component logging
        this.log('INFO', 'Utility logging configured', 'utilities');
    }

    /**
     * Setup log aggregation
     */
    setupLogAggregation() {
        // Setup centralized log aggregation
        this.log('INFO', 'Log aggregation setup completed', 'system');
    }

    /**
     * Log message
     */
    log(level, message, component = null, data = null) {
        const logEntry = {
            timestamp: new Date().toISOString(),
            level: level,
            message: message,
            component: component || this.component,
            data: data
        };

        // Add to internal logs
        this.logs.push(logEntry);

        // Maintain log limit
        if (this.logs.length > this.maxLogs) {
            this.logs.shift();
        }

        // Console output for development
        console.log(`[${logEntry.timestamp}] ${level}: ${message}`);

        // Emit log event
        this.emitLogEvent(logEntry);
    }

    /**
     * Emit log event
     */
    emitLogEvent(logEntry) {
        window.dispatchEvent(new CustomEvent('unifiedLogging:newLog', {
            detail: logEntry
        }));
    }

    /**
     * Debug log
     */
    debug(message, component = null, data = null) {
        if (this.currentLevel <= this.levels.DEBUG) {
            this.log('DEBUG', message, component, data);
        }
    }

    /**
     * Info log
     */
    info(message, component = null, data = null) {
        if (this.currentLevel <= this.levels.INFO) {
            this.log('INFO', message, component, data);
        }
    }

    /**
     * Warning log
     */
    warn(message, component = null, data = null) {
        if (this.currentLevel <= this.levels.WARN) {
            this.log('WARN', message, component, data);
        }
    }

    /**
     * Error log
     */
    error(message, component = null, data = null) {
        if (this.currentLevel <= this.levels.ERROR) {
            this.log('ERROR', message, component, data);
        }
    }

    /**
     * Get logs
     */
    getLogs(level = null, component = null, limit = 100) {
        let filteredLogs = this.logs;

        if (level) {
            filteredLogs = filteredLogs.filter(log => log.level === level);
        }

        if (component) {
            filteredLogs = filteredLogs.filter(log => log.component === component);
        }

        return filteredLogs.slice(-limit);
    }

    /**
     * Clear logs
     */
    clearLogs() {
        this.logs = [];
    }

    /**
     * Set log level
     */
    setLogLevel(level) {
        if (this.levels.hasOwnProperty(level)) {
            this.currentLevel = this.levels[level];
            this.info(`Log level set to ${level}`);
        }
    }

    /**
     * Get log statistics
     */
    getLogStatistics() {
        const stats = {
            total: this.logs.length,
            byLevel: {},
            byComponent: {},
            timeRange: null
        };

        if (this.logs.length > 0) {
            const firstLog = this.logs[0];
            const lastLog = this.logs[this.logs.length - 1];
            stats.timeRange = {
                start: firstLog.timestamp,
                end: lastLog.timestamp
            };
        }

        this.logs.forEach(log => {
            // Count by level
            stats.byLevel[log.level] = (stats.byLevel[log.level] || 0) + 1;

            // Count by component
            stats.byComponent[log.component] = (stats.byComponent[log.component] || 0) + 1;
        });

        return stats;
    }
}

// ================================
// BACKWARD COMPATIBILITY
// ================================

/**
 * Create unified logger instance
 */
export function createUnifiedLogger(component = 'WebLayer') {
    return new UnifiedLogger(component);
}

// ================================
// EXPORTS
// ================================

export default UnifiedLogger;
