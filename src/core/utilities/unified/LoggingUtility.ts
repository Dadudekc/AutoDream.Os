/**
 * @fileoverview Unified Logging Utility - TypeScript Wrapper for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * TypeScript wrapper around the shared LoggingCore implementation.
 * Provides type safety while using the universal JavaScript core.
 */

import { LoggingCore } from '../shared/logging-core.js';
import { 
  ILoggingUtility, ILogEntry, ILoggingConfig, LogLevel, ILogFilter, 
  ILogAggregation, IPerformanceMetrics 
} from '../../interfaces/ILoggingUtility';

/**
 * Unified Logging Utility Implementation
 * TypeScript wrapper around the shared LoggingCore
 */
export class LoggingUtility implements ILoggingUtility {
  private core: LoggingCore;

  constructor(config: ILoggingConfig = {}) {
    this.core = new LoggingCore(config);
  }

  /**
   * Initialize the logging utility with configuration
   */
  async initialize(config: ILoggingConfig = {}): Promise<void> {
    return this.core.initialize(config);
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup(): Promise<void> {
    return this.core.cleanup();
  }

  /**
   * Get utility metadata and capabilities
   */
  getMetadata() {
    return this.core.getMetadata();
  }

  // === BASIC LOGGING METHODS ===

  /**
   * Log trace message
   */
  trace(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.trace(message, context, metadata);
  }

  /**
   * Log debug message
   */
  debug(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.debug(message, context, metadata);
  }

  /**
   * Log info message
   */
  info(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.info(message, context, metadata);
  }

  /**
   * Log warning message
   */
  warn(message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.warn(message, context, metadata);
  }

  /**
   * Log error message
   */
  error(message: string, error?: Error, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.error(message, error, context, metadata);
  }

  /**
   * Log fatal message
   */
  fatal(message: string, error?: Error, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.fatal(message, error, context, metadata);
  }

  /**
   * Core logging method
   */
  log(level: LogLevel, message: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.log(level, message, context, metadata);
  }

  // === ADVANCED LOGGING ===

  /**
   * Time an operation
   */
  async time<T>(level: LogLevel, message: string, operation: () => T | Promise<T>, context?: Record<string, any>): Promise<T> {
    return this.core.time(level, message, operation, context);
  }

  /**
   * Log method execution
   */
  logMethod(level: LogLevel, methodName: string, args: any[], result: any, executionTime: number, context?: Record<string, any>): void {
    this.core.logMethod(level, methodName, args, result, executionTime, context);
  }

  /**
   * Log API call
   */
  logApiCall(level: LogLevel, method: string, url: string, statusCode: number, requestBody?: any, responseBody?: any, executionTime?: number, context?: Record<string, any>): void {
    this.core.logApiCall(level, method, url, statusCode, requestBody, responseBody, executionTime, context);
  }

  /**
   * Log user action
   */
  logUserAction(level: LogLevel, action: string, userId: string, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.logUserAction(level, action, userId, context, metadata);
  }

  /**
   * Log business event
   */
  logBusinessEvent(level: LogLevel, event: string, data: Record<string, any>, context?: Record<string, any>, metadata?: ILogEntry['metadata']): void {
    this.core.logBusinessEvent(level, event, data, context, metadata);
  }

  // === LOG MANAGEMENT ===

  /**
   * Get logs with filtering
   */
  async getLogs(filter?: ILogFilter, limit?: number, offset?: number): Promise<ILogEntry[]> {
    return this.core.getLogs(filter, limit, offset);
  }

  /**
   * Clear logs
   */
  async clearLogs(filter?: ILogFilter): Promise<void> {
    return this.core.clearLogs(filter);
  }

  /**
   * Export logs
   */
  async exportLogs(filter?: ILogFilter, format?: 'json' | 'csv' | 'txt', options?: {
    includeHeaders?: boolean;
    dateFormat?: string;
  }): Promise<string> {
    return this.core.exportLogs(filter, format, options);
  }

  // === LOG ANALYSIS ===

  /**
   * Get log statistics
   */
  async getStatistics(filter?: ILogFilter, timeRange?: {
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
  }> {
    return this.core.getStatistics(filter, timeRange);
  }

  /**
   * Search logs
   */
  async searchLogs(query: string, options?: {
    caseSensitive?: boolean;
    regex?: boolean;
    fields?: string[];
    limit?: number;
    offset?: number;
  }): Promise<ILogEntry[]> {
    return this.core.searchLogs(query, options);
  }

  // === PERFORMANCE MONITORING ===

  /**
   * Get performance metrics
   */
  getPerformanceMetrics(): IPerformanceMetrics {
    return this.core.getPerformanceMetrics();
  }

  /**
   * Start performance monitoring
   */
  startPerformanceMonitoring(operation: string, context?: Record<string, any>): string {
    return this.core.startPerformanceMonitoring(operation, context);
  }

  /**
   * End performance monitoring
   */
  endPerformanceMonitoring(operationId: string, result?: any): void {
    this.core.endPerformanceMonitoring(operationId, result);
  }

  // === CONFIGURATION & MANAGEMENT ===

  /**
   * Update configuration
   */
  async updateConfig(config: Partial<ILoggingConfig>): Promise<void> {
    return this.core.updateConfig(config);
  }

  /**
   * Get configuration
   */
  getConfig(): ILoggingConfig {
    return this.core.getConfig();
  }

  /**
   * Set log level
   */
  setLogLevel(level: LogLevel): void {
    this.core.setLogLevel(level);
  }

  /**
   * Set outputs
   */
  setOutputs(outputs: {
    console?: boolean;
    file?: boolean;
    remote?: boolean;
  }): void {
    this.core.setOutputs(outputs);
  }

  // === UTILITY METHODS ===

  /**
   * Create child logger
   */
  createChild(context?: Record<string, any>, metadata?: ILogEntry['metadata']): ILoggingUtility {
    return this.core.createChild(context, metadata);
  }

  /**
   * Create logger with correlation ID
   */
  withCorrelation(correlationId: string, context?: Record<string, any>): ILoggingUtility {
    return this.core.withCorrelation(correlationId, context);
  }

  /**
   * Create logger with user ID
   */
  withUser(userId: string, context?: Record<string, any>): ILoggingUtility {
    return this.core.withUser(userId, context);
  }

  /**
   * Create logger with session ID
   */
  withSession(sessionId: string, context?: Record<string, any>): ILoggingUtility {
    return this.core.withSession(sessionId, context);
  }

  // === HEALTH & MONITORING ===

  /**
   * Get health status
   */
  getHealthStatus(): {
    status: 'healthy' | 'warning' | 'error';
    issues: string[];
    metrics: IPerformanceMetrics;
  } {
    return this.core.getHealthStatus();
  }

  /**
   * Test logging
   */
  async testLogging(level?: LogLevel): Promise<boolean> {
    return this.core.testLogging(level);
  }

  /**
   * Get diagnostics
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
  } {
    return this.core.getDiagnostics();
  }
}

// Export for both CommonJS and ES modules
export default LoggingUtility;