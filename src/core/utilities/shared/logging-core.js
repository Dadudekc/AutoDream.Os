/**
 * @fileoverview Shared Logging Utilities Core - Universal JavaScript Implementation
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * Universal logging utility functions that work in both Node.js and browser environments.
 * This is the core implementation that both TypeScript and JavaScript utilities will use.
 */

/**
 * Universal Logging Utilities Core
 * Provides comprehensive logging, monitoring, and analytics capabilities
 * Works in both Node.js and browser environments
 */
export class LoggingCore {
  constructor(config = {}) {
    this.config = {
      level: 'INFO',
      enableConsole: true,
      enableFile: false,
      enableRemote: false,
      format: 'json',
      includeStackTrace: true,
      enableMetrics: true,
      enablePerformance: true,
      ...config
    };
    
    this.logs = [];
    this.performanceOperations = new Map();
    this.metrics = {
      totalLogs: 0,
      logsByLevel: {},
      averageLogSize: 0,
      errorRate: 0,
      performanceOverhead: 0,
      memoryUsage: 0
    };
    
    this.transports = [];
    this.defaultContext = {};
    this.defaultMetadata = {};
  }

  /**
   * Initialize the logging utility with configuration
   */
  async initialize(config = {}) {
    try {
      this.config = { ...this.config, ...config };
      this.initializeTransports();
    } catch (error) {
      throw new Error(`LoggingCore initialization failed: ${error}`);
    }
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup() {
    try {
      this.logs = [];
      this.performanceOperations.clear();
      this.transports = [];
    } catch (error) {
      throw new Error(`LoggingCore cleanup failed: ${error}`);
    }
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return {
      name: 'LoggingCore',
      version: '3.0.0',
      capabilities: [
        'logging', 'monitoring', 'analytics', 'performance', 'filtering',
        'aggregation', 'export', 'health', 'diagnostics'
      ],
      dependencies: []
    };
  }

  // === BASIC LOGGING METHODS ===

  /**
   * Log trace message
   */
  trace(message, context, metadata) {
    this.log('TRACE', message, context, metadata);
  }

  /**
   * Log debug message
   */
  debug(message, context, metadata) {
    this.log('DEBUG', message, context, metadata);
  }

  /**
   * Log info message
   */
  info(message, context, metadata) {
    this.log('INFO', message, context, metadata);
  }

  /**
   * Log warning message
   */
  warn(message, context, metadata) {
    this.log('WARN', message, context, metadata);
  }

  /**
   * Log error message
   */
  error(message, error, context, metadata) {
    this.log('ERROR', message, { ...context, error: error?.message, stack: error?.stack }, metadata);
  }

  /**
   * Log fatal message
   */
  fatal(message, error, context, metadata) {
    this.log('FATAL', message, { ...context, error: error?.message, stack: error?.stack }, metadata);
  }

  /**
   * Core logging method
   */
  log(level, message, context, metadata) {
    try {
      if (this.getLevelValue(level) < this.getLevelValue(this.config.level)) {
        return;
      }

      const logEntry = {
        timestamp: new Date(),
        level,
        message,
        context: { ...this.defaultContext, ...context },
        metadata: { ...this.defaultMetadata, ...metadata }
      };

      this.processLogEntry(logEntry);
      this.updateMetrics(logEntry);
    } catch (error) {
      console.error('Logging error:', error);
    }
  }

  // === ADVANCED LOGGING ===

  /**
   * Time an operation
   */
  async time(level, message, operation, context) {
    const startTime = performance.now();
    const operationId = this.generateOperationId();
    
    try {
      this.performanceOperations.set(operationId, { startTime, context: context || {} });
      
      const result = await operation();
      const executionTime = performance.now() - startTime;
      
      this.log(level, `${message} completed in ${executionTime.toFixed(2)}ms`, {
        ...context,
        executionTime,
        operationId
      });
      
      this.performanceOperations.delete(operationId);
      return result;
    } catch (error) {
      const executionTime = performance.now() - startTime;
      this.error(`${message} failed after ${executionTime.toFixed(2)}ms`, error, {
        ...context,
        executionTime,
        operationId
      });
      this.performanceOperations.delete(operationId);
      throw error;
    }
  }

  /**
   * Log method execution
   */
  logMethod(level, methodName, args, result, executionTime, context) {
    this.log(level, `Method ${methodName} executed`, {
      ...context,
      methodName,
      args: this.sanitizeArgs(args),
      result: this.sanitizeResult(result),
      executionTime
    });
  }

  /**
   * Log API call
   */
  logApiCall(level, method, url, statusCode, requestBody, responseBody, executionTime, context) {
    this.log(level, `API ${method} ${url} - ${statusCode}`, {
      ...context,
      method,
      url,
      statusCode,
      requestBody: this.sanitizeData(requestBody),
      responseBody: this.sanitizeData(responseBody),
      executionTime
    });
  }

  /**
   * Log user action
   */
  logUserAction(level, action, userId, context, metadata) {
    this.log(level, `User action: ${action}`, {
      ...context,
      action,
      userId
    }, { ...metadata, userId });
  }

  /**
   * Log business event
   */
  logBusinessEvent(level, event, data, context, metadata) {
    this.log(level, `Business event: ${event}`, {
      ...context,
      event,
      data: this.sanitizeData(data)
    }, metadata);
  }

  // === LOG MANAGEMENT ===

  /**
   * Get logs with filtering
   */
  async getLogs(filter, limit, offset) {
    try {
      let filteredLogs = this.logs;

      if (filter) {
        filteredLogs = this.filterLogs(filteredLogs, filter);
      }

      if (offset) {
        filteredLogs = filteredLogs.slice(offset);
      }

      if (limit) {
        filteredLogs = filteredLogs.slice(0, limit);
      }

      return filteredLogs;
    } catch (error) {
      this.error('Failed to get logs', error);
      return [];
    }
  }

  /**
   * Clear logs
   */
  async clearLogs(filter) {
    try {
      if (filter) {
        this.logs = this.logs.filter(log => !this.matchesFilter(log, filter));
      } else {
        this.logs = [];
      }
    } catch (error) {
      this.error('Failed to clear logs', error);
    }
  }

  /**
   * Export logs
   */
  async exportLogs(filter, format = 'json', options = {}) {
    try {
      const logs = await this.getLogs(filter);
      
      switch (format) {
        case 'json':
          return JSON.stringify(logs, null, 2);
        case 'csv':
          return this.exportToCSV(logs, options);
        case 'txt':
          return this.exportToText(logs, options);
        default:
          throw new Error(`Unsupported export format: ${format}`);
      }
    } catch (error) {
      this.error('Failed to export logs', error);
      return '';
    }
  }

  // === LOG ANALYSIS ===

  /**
   * Get log statistics
   */
  async getStatistics(filter, timeRange) {
    try {
      let filteredLogs = this.logs;

      if (filter) {
        filteredLogs = this.filterLogs(filteredLogs, filter);
      }

      if (timeRange) {
        filteredLogs = filteredLogs.filter(log => 
          log.timestamp >= timeRange.start && log.timestamp <= timeRange.end
        );
      }

      const logsByLevel = {};
      const logsBySource = {};
      let totalSize = 0;
      let errorCount = 0;

      filteredLogs.forEach(log => {
        logsByLevel[log.level] = (logsByLevel[log.level] || 0) + 1;
        
        const source = log.metadata?.source || 'unknown';
        logsBySource[source] = (logsBySource[source] || 0) + 1;
        
        totalSize += JSON.stringify(log).length;
        
        if (this.getLevelValue(log.level) >= this.getLevelValue('ERROR')) {
          errorCount++;
        }
      });

      return {
        totalLogs: filteredLogs.length,
        logsByLevel,
        logsBySource,
        errorRate: filteredLogs.length > 0 ? errorCount / filteredLogs.length : 0,
        averageLogSize: filteredLogs.length > 0 ? totalSize / filteredLogs.length : 0,
        timeRange: timeRange || {
          start: filteredLogs.length > 0 ? filteredLogs[0].timestamp : new Date(),
          end: filteredLogs.length > 0 ? filteredLogs[filteredLogs.length - 1].timestamp : new Date()
        }
      };
    } catch (error) {
      this.error('Failed to get statistics', error);
      return {
        totalLogs: 0,
        logsByLevel: {},
        logsBySource: {},
        errorRate: 0,
        averageLogSize: 0,
        timeRange: { start: new Date(), end: new Date() }
      };
    }
  }

  /**
   * Search logs
   */
  async searchLogs(query, options = {}) {
    try {
      const { caseSensitive = false, regex = false, fields = ['message'], limit, offset } = options;
      
      let filteredLogs = this.logs;
      
      if (regex) {
        const regexObj = new RegExp(query, caseSensitive ? 'g' : 'gi');
        filteredLogs = filteredLogs.filter(log => 
          fields.some(field => {
            const value = this.getFieldValue(log, field);
            return regexObj.test(String(value));
          })
        );
      } else {
        const searchQuery = caseSensitive ? query : query.toLowerCase();
        filteredLogs = filteredLogs.filter(log => 
          fields.some(field => {
            const value = this.getFieldValue(log, field);
            return String(value).toLowerCase().includes(searchQuery);
          })
        );
      }

      if (offset) {
        filteredLogs = filteredLogs.slice(offset);
      }

      if (limit) {
        filteredLogs = filteredLogs.slice(0, limit);
      }

      return filteredLogs;
    } catch (error) {
      this.error('Failed to search logs', error);
      return [];
    }
  }

  // === PERFORMANCE MONITORING ===

  /**
   * Get performance metrics
   */
  getPerformanceMetrics() {
    return { ...this.metrics };
  }

  /**
   * Start performance monitoring
   */
  startPerformanceMonitoring(operation, context) {
    const operationId = this.generateOperationId();
    this.performanceOperations.set(operationId, {
      startTime: performance.now(),
      context: { operation, ...context }
    });
    return operationId;
  }

  /**
   * End performance monitoring
   */
  endPerformanceMonitoring(operationId, result) {
    const operation = this.performanceOperations.get(operationId);
    if (operation) {
      const executionTime = performance.now() - operation.startTime;
      this.info(`Performance monitoring: ${operation.context.operation}`, {
        ...operation.context,
        executionTime,
        result: this.sanitizeResult(result)
      });
      this.performanceOperations.delete(operationId);
    }
  }

  // === CONFIGURATION & MANAGEMENT ===

  /**
   * Update configuration
   */
  async updateConfig(config) {
    this.config = { ...this.config, ...config };
    this.initializeTransports();
  }

  /**
   * Get configuration
   */
  getConfig() {
    return { ...this.config };
  }

  /**
   * Set log level
   */
  setLogLevel(level) {
    this.config.level = level;
  }

  /**
   * Set outputs
   */
  setOutputs(outputs) {
    if (outputs.console !== undefined) this.config.enableConsole = outputs.console;
    if (outputs.file !== undefined) this.config.enableFile = outputs.file;
    if (outputs.remote !== undefined) this.config.enableRemote = outputs.remote;
  }

  // === UTILITY METHODS ===

  /**
   * Create child logger
   */
  createChild(context, metadata) {
    const child = new LoggingCore();
    child.config = { ...this.config };
    child.defaultContext = { ...this.defaultContext, ...context };
    child.defaultMetadata = { ...this.defaultMetadata, ...metadata };
    return child;
  }

  /**
   * Create logger with correlation ID
   */
  withCorrelation(correlationId, context) {
    return this.createChild({ ...context, correlationId }, { correlationId });
  }

  /**
   * Create logger with user ID
   */
  withUser(userId, context) {
    return this.createChild({ ...context, userId }, { userId });
  }

  /**
   * Create logger with session ID
   */
  withSession(sessionId, context) {
    return this.createChild({ ...context, sessionId }, { sessionId });
  }

  // === HEALTH & MONITORING ===

  /**
   * Get health status
   */
  getHealthStatus() {
    const issues = [];
    let status = 'healthy';

    if (this.metrics.errorRate > 0.1) {
      issues.push('High error rate detected');
      status = 'warning';
    }

    if (this.metrics.memoryUsage > 1000000) { // 1MB
      issues.push('High memory usage');
      status = 'warning';
    }

    if (this.transports.some(t => t.status === 'error')) {
      issues.push('Transport errors detected');
      status = 'error';
    }

    return {
      status,
      issues,
      metrics: this.getPerformanceMetrics()
    };
  }

  /**
   * Test logging
   */
  async testLogging(level = 'INFO') {
    try {
      this.log(level, 'Test log message', { test: true });
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * Get diagnostics
   */
  getDiagnostics() {
    return {
      configuration: this.getConfig(),
      transports: [...this.transports],
      performance: this.getPerformanceMetrics(),
      errors: [] // Would be populated from actual error tracking
    };
  }

  // === PRIVATE HELPER METHODS ===

  processLogEntry(logEntry) {
    this.logs.push(logEntry);
    
    if (this.config.enableConsole) {
      this.logToConsole(logEntry);
    }
    
    if (this.config.enableFile) {
      this.logToFile(logEntry);
    }
    
    if (this.config.enableRemote) {
      this.logToRemote(logEntry);
    }
  }

  logToConsole(logEntry) {
    const timestamp = logEntry.timestamp.toISOString();
    const message = `[${timestamp}] ${logEntry.level}: ${logEntry.message}`;
    
    switch (logEntry.level) {
      case 'TRACE':
      case 'DEBUG':
        console.debug(message, logEntry.context);
        break;
      case 'INFO':
        console.info(message, logEntry.context);
        break;
      case 'WARN':
        console.warn(message, logEntry.context);
        break;
      case 'ERROR':
      case 'FATAL':
        console.error(message, logEntry.context);
        break;
    }
  }

  logToFile(logEntry) {
    // File logging implementation would go here
    // This is a placeholder for the actual file system operations
  }

  logToRemote(logEntry) {
    // Remote logging implementation would go here
    // This is a placeholder for the actual remote API calls
  }

  updateMetrics(logEntry) {
    this.metrics.totalLogs++;
    
    this.metrics.logsByLevel[logEntry.level] = (this.metrics.logsByLevel[logEntry.level] || 0) + 1;
    
    const logSize = JSON.stringify(logEntry).length;
    this.metrics.averageLogSize = (this.metrics.averageLogSize + logSize) / 2;
    
    if (this.getLevelValue(logEntry.level) >= this.getLevelValue('ERROR')) {
      this.metrics.errorRate = (this.metrics.errorRate + 1) / this.metrics.totalLogs;
    }
    
    this.metrics.memoryUsage = this.logs.length * this.metrics.averageLogSize;
  }

  filterLogs(logs, filter) {
    return logs.filter(log => this.matchesFilter(log, filter));
  }

  matchesFilter(log, filter) {
    if (filter.level !== undefined && log.level !== filter.level) {
      return false;
    }
    
    if (filter.source && log.metadata?.source !== filter.source) {
      return false;
    }
    
    if (filter.message) {
      if (typeof filter.message === 'string') {
        if (!log.message.includes(filter.message)) {
          return false;
        }
      } else if (filter.message instanceof RegExp) {
        if (!filter.message.test(log.message)) {
          return false;
        }
      }
    }
    
    if (filter.timeRange) {
      if (log.timestamp < filter.timeRange.start || log.timestamp > filter.timeRange.end) {
        return false;
      }
    }
    
    if (filter.userId && log.metadata?.userId !== filter.userId) {
      return false;
    }
    
    if (filter.sessionId && log.metadata?.sessionId !== filter.sessionId) {
      return false;
    }
    
    return true;
  }

  getFieldValue(log, field) {
    const fields = field.split('.');
    let value = log;
    
    for (const f of fields) {
      value = value?.[f];
    }
    
    return value;
  }

  sanitizeArgs(args) {
    return args.map(arg => this.sanitizeData(arg));
  }

  sanitizeResult(result) {
    return this.sanitizeData(result);
  }

  sanitizeData(data) {
    if (data === null || data === undefined) {
      return data;
    }
    
    if (typeof data === 'string') {
      return data.length > 1000 ? data.substring(0, 1000) + '...' : data;
    }
    
    if (typeof data === 'object') {
      try {
        const serialized = JSON.stringify(data);
        if (serialized.length > 1000) {
          return { ...data, _truncated: true };
        }
        return data;
      } catch {
        return '[Circular or non-serializable object]';
      }
    }
    
    return data;
  }

  exportToCSV(logs, options) {
    const headers = ['timestamp', 'level', 'message', 'source', 'userId'];
    const rows = logs.map(log => [
      log.timestamp.toISOString(),
      log.level,
      log.message,
      log.metadata?.source || '',
      log.metadata?.userId || ''
    ]);
    
    return [headers.join(','), ...rows.map(row => row.join(','))].join('\n');
  }

  exportToText(logs, options) {
    return logs.map(log => {
      const timestamp = log.timestamp.toISOString();
      return `[${timestamp}] ${log.level}: ${log.message}`;
    }).join('\n');
  }

  generateOperationId() {
    return `op_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  initializeTransports() {
    // Initialize logging transports based on configuration
    this.transports = [];
    
    if (this.config.enableConsole) {
      this.transports.push({
        id: 'console',
        type: 'console',
        config: {},
        status: 'active'
      });
    }
    
    if (this.config.enableFile) {
      this.transports.push({
        id: 'file',
        type: 'file',
        config: { path: this.config.filePath },
        status: 'active'
      });
    }
    
    if (this.config.enableRemote) {
      this.transports.push({
        id: 'remote',
        type: 'remote',
        config: { endpoint: this.config.remoteEndpoint },
        status: 'active'
      });
    }
  }

  getLevelValue(level) {
    const levels = {
      'TRACE': 0,
      'DEBUG': 1,
      'INFO': 2,
      'WARN': 3,
      'ERROR': 4,
      'FATAL': 5
    };
    return levels[level] || 2;
  }
}

// Export for both CommonJS and ES modules
export default LoggingCore;