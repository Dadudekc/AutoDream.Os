/**
 * Chart State Logger - V2 Compliant Module
 * =======================================
 * 
 * Logging utilities for chart state validation.
 * 
 * V2 Compliance: < 300 lines, single responsibility.
 * 
 * Author: Agent-7 - Web Development Specialist
 * License: MIT
 */

export class ChartStateLogger {
    constructor() {
        this.logs = [];
        this.maxLogs = 1000;
        this.logLevel = 'info';
    }

    /**
     * Set log level
     */
    setLogLevel(level) {
        const validLevels = ['debug', 'info', 'warn', 'error'];
        if (validLevels.includes(level)) {
            this.logLevel = level;
        }
    }

    /**
     * Get log level
     */
    getLogLevel() {
        return this.logLevel;
    }

    /**
     * Log message
     */
    log(level, message, context = {}) {
        const timestamp = new Date().toISOString();
        const logEntry = {
            timestamp,
            level,
            message,
            context,
            id: this.generateLogId()
        };

        this.logs.push(logEntry);

        // Keep only recent logs
        if (this.logs.length > this.maxLogs) {
            this.logs = this.logs.slice(-this.maxLogs);
        }

        // Output to console if level is appropriate
        if (this.shouldLog(level)) {
            this.outputToConsole(level, message, context);
        }
    }

    /**
     * Debug log
     */
    debug(message, context = {}) {
        this.log('debug', message, context);
    }

    /**
     * Info log
     */
    info(message, context = {}) {
        this.log('info', message, context);
    }

    /**
     * Warning log
     */
    warn(message, context = {}) {
        this.log('warn', message, context);
    }

    /**
     * Error log
     */
    error(message, context = {}) {
        this.log('error', message, context);
    }

    /**
     * Check if should log based on level
     */
    shouldLog(level) {
        const levels = { debug: 0, info: 1, warn: 2, error: 3 };
        return levels[level] >= levels[this.logLevel];
    }

    /**
     * Output to console
     */
    outputToConsole(level, message, context) {
        const timestamp = new Date().toISOString();
        const prefix = `[${timestamp}] CHART-VALIDATION-${level.toUpperCase()}:`;
        
        switch (level) {
            case 'debug':
                console.debug(prefix, message, context);
                break;
            case 'info':
                console.info(prefix, message, context);
                break;
            case 'warn':
                console.warn(prefix, message, context);
                break;
            case 'error':
                console.error(prefix, message, context);
                break;
        }
    }

    /**
     * Generate unique log ID
     */
    generateLogId() {
        return `log_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    /**
     * Get logs by level
     */
    getLogsByLevel(level) {
        return this.logs.filter(log => log.level === level);
    }

    /**
     * Get logs by time range
     */
    getLogsByTimeRange(startTime, endTime) {
        return this.logs.filter(log => {
            const logTime = new Date(log.timestamp).getTime();
            return logTime >= startTime && logTime <= endTime;
        });
    }

    /**
     * Get recent logs
     */
    getRecentLogs(count = 50) {
        return this.logs.slice(-count);
    }

    /**
     * Get all logs
     */
    getAllLogs() {
        return [...this.logs];
    }

    /**
     * Clear logs
     */
    clearLogs() {
        this.logs = [];
    }

    /**
     * Get log statistics
     */
    getLogStats() {
        const stats = {
            total: this.logs.length,
            byLevel: {},
            oldest: null,
            newest: null
        };

        this.logs.forEach(log => {
            stats.byLevel[log.level] = (stats.byLevel[log.level] || 0) + 1;
        });

        if (this.logs.length > 0) {
            stats.oldest = this.logs[0].timestamp;
            stats.newest = this.logs[this.logs.length - 1].timestamp;
        }

        return stats;
    }

    /**
     * Export logs
     */
    exportLogs() {
        return {
            logs: this.getAllLogs(),
            stats: this.getLogStats(),
            exportedAt: new Date().toISOString()
        };
    }

    /**
     * Search logs
     */
    searchLogs(query) {
        const lowerQuery = query.toLowerCase();
        return this.logs.filter(log => 
            log.message.toLowerCase().includes(lowerQuery) ||
            log.level.toLowerCase().includes(lowerQuery) ||
            JSON.stringify(log.context).toLowerCase().includes(lowerQuery)
        );
    }

    /**
     * Get error logs
     */
    getErrorLogs() {
        return this.getLogsByLevel('error');
    }

    /**
     * Get warning logs
     */
    getWarningLogs() {
        return this.getLogsByLevel('warn');
    }

    /**
     * Get validation logs
     */
    getValidationLogs() {
        return this.logs.filter(log => 
            log.message.includes('validation') || 
            log.message.includes('rule') ||
            log.message.includes('error')
        );
    }
}
