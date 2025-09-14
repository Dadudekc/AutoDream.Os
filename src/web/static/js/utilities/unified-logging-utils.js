/**
 * @fileoverview Unified Logging Utilities - JavaScript Adapter for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * JavaScript adapter that uses the shared LoggingCore implementation.
 * Provides a simplified API for JavaScript environments.
 */

import { LoggingCore } from '../../../../core/utilities/shared/logging-core.js';

/**
 * Unified Logging Utilities Class
 * JavaScript adapter around the shared LoggingCore
 */
export class UnifiedLoggingUtils {
  constructor(config = {}) {
    this.core = new LoggingCore(config);
  }

  /**
   * Initialize the logging utility with configuration
   */
  async initialize(config = {}) {
    return this.core.initialize(config);
  }

  /**
   * Clean up resources and reset state
   */
  async cleanup() {
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
  trace(message, context, metadata) {
    this.core.trace(message, context, metadata);
  }

  /**
   * Log debug message
   */
  debug(message, context, metadata) {
    this.core.debug(message, context, metadata);
  }

  /**
   * Log info message
   */
  info(message, context, metadata) {
    this.core.info(message, context, metadata);
  }

  /**
   * Log warning message
   */
  warn(message, context, metadata) {
    this.core.warn(message, context, metadata);
  }

  /**
   * Log error message
   */
  error(message, error, context, metadata) {
    this.core.error(message, error, context, metadata);
  }

  /**
   * Log fatal message
   */
  fatal(message, error, context, metadata) {
    this.core.fatal(message, error, context, metadata);
  }

  /**
   * Core logging method
   */
  log(level, message, context, metadata) {
    this.core.log(level, message, context, metadata);
  }

  // === ADVANCED LOGGING ===

  /**
   * Time an operation
   */
  async time(level, message, operation, context) {
    return this.core.time(level, message, operation, context);
  }

  /**
   * Log method execution
   */
  logMethod(level, methodName, args, result, executionTime, context) {
    this.core.logMethod(level, methodName, args, result, executionTime, context);
  }

  /**
   * Log API call
   */
  logApiCall(level, method, url, statusCode, requestBody, responseBody, executionTime, context) {
    this.core.logApiCall(level, method, url, statusCode, requestBody, responseBody, executionTime, context);
  }

  /**
   * Log user action
   */
  logUserAction(level, action, userId, context, metadata) {
    this.core.logUserAction(level, action, userId, context, metadata);
  }

  /**
   * Log business event
   */
  logBusinessEvent(level, event, data, context, metadata) {
    this.core.logBusinessEvent(level, event, data, context, metadata);
  }

  // === LOG MANAGEMENT ===

  /**
   * Get logs with filtering
   */
  async getLogs(filter, limit, offset) {
    return this.core.getLogs(filter, limit, offset);
  }

  /**
   * Clear logs
   */
  async clearLogs(filter) {
    return this.core.clearLogs(filter);
  }

  /**
   * Export logs
   */
  async exportLogs(filter, format, options) {
    return this.core.exportLogs(filter, format, options);
  }

  // === LOG ANALYSIS ===

  /**
   * Get log statistics
   */
  async getStatistics(filter, timeRange) {
    return this.core.getStatistics(filter, timeRange);
  }

  /**
   * Search logs
   */
  async searchLogs(query, options) {
    return this.core.searchLogs(query, options);
  }

  // === PERFORMANCE MONITORING ===

  /**
   * Get performance metrics
   */
  getPerformanceMetrics() {
    return this.core.getPerformanceMetrics();
  }

  /**
   * Start performance monitoring
   */
  startPerformanceMonitoring(operation, context) {
    return this.core.startPerformanceMonitoring(operation, context);
  }

  /**
   * End performance monitoring
   */
  endPerformanceMonitoring(operationId, result) {
    this.core.endPerformanceMonitoring(operationId, result);
  }

  // === CONFIGURATION & MANAGEMENT ===

  /**
   * Update configuration
   */
  async updateConfig(config) {
    return this.core.updateConfig(config);
  }

  /**
   * Get configuration
   */
  getConfig() {
    return this.core.getConfig();
  }

  /**
   * Set log level
   */
  setLogLevel(level) {
    this.core.setLogLevel(level);
  }

  /**
   * Set outputs
   */
  setOutputs(outputs) {
    this.core.setOutputs(outputs);
  }

  // === UTILITY METHODS ===

  /**
   * Create child logger
   */
  createChild(context, metadata) {
    return this.core.createChild(context, metadata);
  }

  /**
   * Create logger with correlation ID
   */
  withCorrelation(correlationId, context) {
    return this.core.withCorrelation(correlationId, context);
  }

  /**
   * Create logger with user ID
   */
  withUser(userId, context) {
    return this.core.withUser(userId, context);
  }

  /**
   * Create logger with session ID
   */
  withSession(sessionId, context) {
    return this.core.withSession(sessionId, context);
  }

  // === HEALTH & MONITORING ===

  /**
   * Get health status
   */
  getHealthStatus() {
    return this.core.getHealthStatus();
  }

  /**
   * Test logging
   */
  async testLogging(level) {
    return this.core.testLogging(level);
  }

  /**
   * Get diagnostics
   */
  getDiagnostics() {
    return this.core.getDiagnostics();
  }

  // === CONVENIENCE METHODS ===

  /**
   * Simple logging (backward compatibility)
   */
  logMessage(level, message, data) {
    this.log(level, message, data);
  }

  /**
   * Simple error logging (backward compatibility)
   */
  logError(message, error, data) {
    this.error(message, error, data);
  }

  /**
   * Simple info logging (backward compatibility)
   */
  logInfo(message, data) {
    this.info(message, data);
  }

  /**
   * Simple warning logging (backward compatibility)
   */
  logWarning(message, data) {
    this.warn(message, data);
  }

  /**
   * Simple debug logging (backward compatibility)
   */
  logDebug(message, data) {
    this.debug(message, data);
  }

  /**
   * Simple trace logging (backward compatibility)
   */
  logTrace(message, data) {
    this.trace(message, data);
  }

  /**
   * Simple performance timing (backward compatibility)
   */
  async timeOperation(operation, context) {
    return this.time('INFO', 'Operation', operation, context);
  }

  /**
   * Simple method logging (backward compatibility)
   */
  logMethodCall(methodName, args, result, executionTime) {
    this.logMethod('DEBUG', methodName, args, result, executionTime);
  }

  /**
   * Simple API logging (backward compatibility)
   */
  logApiRequest(method, url, statusCode, requestBody, responseBody, executionTime) {
    this.logApiCall('INFO', method, url, statusCode, requestBody, responseBody, executionTime);
  }

  /**
   * Simple user action logging (backward compatibility)
   */
  logUserAction(action, userId, data) {
    this.logUserAction('INFO', action, userId, data);
  }

  /**
   * Simple business event logging (backward compatibility)
   */
  logBusinessEvent(event, data) {
    this.logBusinessEvent('INFO', event, data);
  }

  /**
   * Simple log level setting (backward compatibility)
   */
  setLevel(level) {
    this.setLogLevel(level);
  }

  /**
   * Simple log output setting (backward compatibility)
   */
  setOutput(console, file, remote) {
    this.setOutputs({ console, file, remote });
  }

  /**
   * Simple log statistics (backward compatibility)
   */
  async getStats() {
    return this.getStatistics();
  }

  /**
   * Simple log search (backward compatibility)
   */
  async searchLogs(query) {
    return this.searchLogs(query);
  }

  /**
   * Simple log export (backward compatibility)
   */
  async exportLogs(format = 'json') {
    return this.exportLogs(undefined, format);
  }

  /**
   * Simple log clearing (backward compatibility)
   */
  async clearAllLogs() {
    return this.clearLogs();
  }

  /**
   * Simple health check (backward compatibility)
   */
  getHealth() {
    return this.getHealthStatus();
  }

  /**
   * Simple diagnostics (backward compatibility)
   */
  getDiagnostics() {
    return this.getDiagnostics();
  }
}

// Factory function for creating logging utils instance
export function createUnifiedLoggingUtils(config = {}) {
  return new UnifiedLoggingUtils(config);
}

// Export default
export default UnifiedLoggingUtils;