/**
 * @fileoverview Logging Utility Interface - Enterprise-grade logging interface
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

/**
 * Log level enumeration
 */
export enum LogLevel {
  TRACE = 0,
  DEBUG = 1,
  INFO = 2,
  WARN = 3,
  ERROR = 4,
  FATAL = 5
}

/**
 * Log entry interface
 */
export interface ILogEntry {
  timestamp: Date;
  level: LogLevel;
  message: string;
  context?: Record<string, any>;
  error?: Error;
  metadata?: {
    source?: string;
    userId?: string;
    sessionId?: string;
    requestId?: string;
    correlationId?: string;
  };
}

/**
 * Logging configuration options
 */
export interface ILoggingConfig {
  level?: LogLevel;
  enableConsole?: boolean;
  enableFile?: boolean;
  enableRemote?: boolean;
  filePath?: string;
  maxFileSize?: number;
  maxFiles?: number;
  remoteEndpoint?: string;
  remoteApiKey?: string;
  format?: 'json' | 'text' | 'structured';
  includeStackTrace?: boolean;
  enableMetrics?: boolean;
  enablePerformance?: boolean;
}

/**
 * Log filtering options
 */
export interface ILogFilter {
  level?: LogLevel;
  source?: string;
  message?: string | RegExp;
  context?: Record<string, any>;
  timeRange?: {
    start: Date;
    end: Date;
  };
  userId?: string;
  sessionId?: string;
}

/**
 * Log aggregation options
 */
export interface ILogAggregation {
  groupBy?: 'level' | 'source' | 'hour' | 'day' | 'user';
  timeWindow?: number; // in milliseconds
  metrics?: ('count' | 'average' | 'sum' | 'min' | 'max')[];
}

/**
 * Performance metrics interface
 */
export interface IPerformanceMetrics {
  totalLogs: number;
  logsByLevel: Record<string, number>;
  averageLogSize: number;
  errorRate: number;
  performanceOverhead: number;
  memoryUsage: number;
}

/**
 * Enterprise Logging Utility Interface
 * Provides comprehensive logging, monitoring, and analytics capabilities
 */
export interface ILoggingUtility {
  /**
   * Initialize the logging utility with configuration
   * @param config - Logging configuration
   */
  initialize(config?: ILoggingConfig): Promise<void>;

  /**
   * Clean up resources and reset state
   */
  cleanup(): Promise<void>;

  /**
   * Get utility metadata and capabilities
   */
  getMetadata(): {
    name: string;
    version: string;
    capabilities: string[];
    dependencies: string[];
  };

  // === BASIC LOGGING METHODS ===

  /**
   * Log trace message
   * @param message - Log message
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  trace(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log debug message
   * @param message - Log message
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  debug(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log info message
   * @param message - Log message
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  info(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log warning message
   * @param message - Log message
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  warn(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log error message
   * @param message - Log message
   * @param error - Error object
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  error(message: string, error?: Error, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log fatal message
   * @param message - Log message
   * @param error - Error object
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  fatal(message: string, error?: Error, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Generic log method
   * @param level - Log level
   * @param message - Log message
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  log(level: LogLevel, message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  // === ADVANCED LOGGING ===

  /**
   * Log with performance timing
   * @param level - Log level
   * @param message - Log message
   * @param operation - Operation to time
   * @param context - Additional context
   */
  time<T>(level: LogLevel, message: string, operation: () => T | Promise<T>, context?: Record<string, any>): Promise<T>;

  /**
   * Log method execution
   * @param level - Log level
   * @param methodName - Method name
   * @param args - Method arguments
   * @param result - Method result
   * @param executionTime - Execution time
   * @param context - Additional context
   */
  logMethod(level: LogLevel, methodName: string, args: any[], result: any, executionTime: number, context?: Record<string, any>): void;

  /**
   * Log API request/response
   * @param level - Log level
   * @param method - HTTP method
   * @param url - Request URL
   * @param statusCode - Response status code
   * @param requestBody - Request body
   * @param responseBody - Response body
   * @param executionTime - Request execution time
   * @param context - Additional context
   */
  logApiCall(level: LogLevel, method: string, url: string, statusCode: number, requestBody?: any, responseBody?: any, executionTime?: number, context?: Record<string, any>): void;

  /**
   * Log user action
   * @param level - Log level
   * @param action - User action
   * @param userId - User identifier
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  logUserAction(level: LogLevel, action: string, userId: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  /**
   * Log business event
   * @param level - Log level
   * @param event - Business event
   * @param data - Event data
   * @param context - Additional context
   * @param metadata - Log metadata
   */
  logBusinessEvent(level: LogLevel, event: string, data: Record<string, any>, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void;

  // === LOG MANAGEMENT ===

  /**
   * Get logs with filtering
   * @param filter - Log filter options
   * @param limit - Maximum number of logs
   * @param offset - Offset for pagination
   */
  getLogs(filter?: ILogFilter, limit?: number, offset?: number): Promise<ILogEntry[]>;

  /**
   * Clear logs
   * @param filter - Filter for logs to clear
   */
  clearLogs(filter?: ILogFilter): Promise<void>;

  /**
   * Export logs
   * @param filter - Log filter options
   * @param format - Export format
   * @param options - Export options
   */
  exportLogs(filter?: ILogFilter, format?: 'json' | 'csv' | 'txt', options?: {
    includeHeaders?: boolean;
    dateFormat?: string;
  }): Promise<string>;

  /**
   * Archive logs
   * @param filter - Log filter options
   * @param archivePath - Archive file path
   */
  archiveLogs(filter?: ILogFilter, archivePath?: string): Promise<void>;

  // === LOG ANALYSIS ===

  /**
   * Get log statistics
   * @param filter - Log filter options
   * @param timeRange - Time range for statistics
   */
  getStatistics(filter?: ILogFilter, timeRange?: {
    start: Date;
    end: Date;
  }): Promise<{
    totalLogs: number;
    logsByLevel: Record<string, number>;
    logsBySource: Record<string, number>;
    errorRate: number;
    averageLogSize: number;
    timeRange: {
      start: Date;
      end: Date;
    };
  }>;

  /**
   * Get log aggregation
   * @param filter - Log filter options
   * @param aggregation - Aggregation options
   */
  getAggregation(filter?: ILogFilter, aggregation?: ILogAggregation): Promise<Record<string, any>>;

  /**
   * Search logs
   * @param query - Search query
   * @param options - Search options
   */
  searchLogs(query: string, options?: {
    caseSensitive?: boolean;
    regex?: boolean;
    fields?: string[];
    limit?: number;
    offset?: number;
  }): Promise<ILogEntry[]>;

  /**
   * Get error patterns
   * @param filter - Log filter options
   * @param timeRange - Time range for analysis
   */
  getErrorPatterns(filter?: ILogFilter, timeRange?: {
    start: Date;
    end: Date;
  }): Promise<Array<{
    pattern: string;
    count: number;
    firstOccurrence: Date;
    lastOccurrence: Date;
    examples: ILogEntry[];
  }>>;

  // === PERFORMANCE MONITORING ===

  /**
   * Get performance metrics
   */
  getPerformanceMetrics(): IPerformanceMetrics;

  /**
   * Start performance monitoring
   * @param operation - Operation name
   * @param context - Additional context
   */
  startPerformanceMonitoring(operation: string, context?: Record<string, any>): string;

  /**
   * End performance monitoring
   * @param operationId - Operation identifier
   * @param result - Operation result
   */
  endPerformanceMonitoring(operationId: string, result?: any): void;

  /**
   * Get performance report
   * @param timeRange - Time range for report
   */
  getPerformanceReport(timeRange?: {
    start: Date;
    end: Date;
  }): Promise<{
    totalOperations: number;
    averageExecutionTime: number;
    slowestOperations: Array<{
      operation: string;
      executionTime: number;
      timestamp: Date;
    }>;
    errorRate: number;
    throughput: number;
  }>;

  // === CONFIGURATION & MANAGEMENT ===

  /**
   * Update logging configuration
   * @param config - New configuration
   */
  updateConfig(config: Partial<ILoggingConfig>): Promise<void>;

  /**
   * Get current configuration
   */
  getConfig(): ILoggingConfig;

  /**
   * Set log level
   * @param level - New log level
   */
  setLogLevel(level: LogLevel): void;

  /**
   * Enable/disable specific log outputs
   * @param outputs - Output configuration
   */
  setOutputs(outputs: {
    console?: boolean;
    file?: boolean;
    remote?: boolean;
  }): void;

  /**
   * Add log transport
   * @param transport - Log transport configuration
   */
  addTransport(transport: {
    type: 'file' | 'remote' | 'database' | 'custom';
    config: any;
  }): Promise<void>;

  /**
   * Remove log transport
   * @param transportId - Transport identifier
   */
  removeTransport(transportId: string): Promise<void>;

  // === UTILITY METHODS ===

  /**
   * Create child logger
   * @param context - Default context for child logger
   * @param metadata - Default metadata for child logger
   */
  createChild(context?: Record<string, any>, metadata?: ILogEntry['metadata']): ILoggingUtility;

  /**
   * Create logger with correlation ID
   * @param correlationId - Correlation identifier
   * @param context - Additional context
   */
  withCorrelation(correlationId: string, context?: Record<string, any>): ILoggingUtility;

  /**
   * Create logger with user context
   * @param userId - User identifier
   * @param context - Additional context
   */
  withUser(userId: string, context?: Record<string, any>): ILoggingUtility;

  /**
   * Create logger with session context
   * @param sessionId - Session identifier
   * @param context - Additional context
   */
  withSession(sessionId: string, context?: Record<string, any>): ILoggingUtility;

  // === HEALTH & MONITORING ===

  /**
   * Get logger health status
   */
  getHealthStatus(): {
    status: 'healthy' | 'warning' | 'error';
    issues: string[];
    metrics: IPerformanceMetrics;
  };

  /**
   * Test logging functionality
   * @param level - Test log level
   */
  testLogging(level?: LogLevel): Promise<boolean>;

  /**
   * Get logger diagnostics
   */
  getDiagnostics(): {
    configuration: ILoggingConfig;
    transports: Array<{
      id: string;
      type: string;
      status: 'active' | 'inactive' | 'error';
      lastActivity?: Date;
    }>;
    performance: IPerformanceMetrics;
    errors: Array<{
      timestamp: Date;
      error: string;
      context?: Record<string, any>;
    }>;
  };
}