/**
 * @fileoverview Unified Time Utilities - JavaScript Adapter for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * JavaScript adapter that uses the shared TimeCore implementation.
 * Provides a simplified API for JavaScript environments.
 */

import { TimeCore } from '../../../../core/utilities/shared/time-core.js';

/**
 * Unified Time Utilities Class
 * JavaScript adapter around the shared TimeCore
 */
export class UnifiedTimeUtils {
  constructor(config = {}) {
    this.core = new TimeCore(config);
  }

  /**
   * Initialize the time utility with configuration
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

  // === TIME CREATION & PARSING ===

  /**
   * Create date from input
   */
  create(input, options = {}) {
    return this.core.create(input, options);
  }

  /**
   * Parse date string with format
   */
  parse(dateString, options = {}) {
    return this.core.parse(dateString, options);
  }

  /**
   * Get current time
   */
  now(options = {}) {
    return this.core.now(options);
  }

  /**
   * Get UTC time
   */
  utc(options = {}) {
    return this.core.utc(options);
  }

  // === TIME FORMATTING ===

  /**
   * Format date with options
   */
  format(date, options = {}) {
    return this.core.format(date, options);
  }

  /**
   * Format relative time
   */
  formatRelative(date, options = {}) {
    return this.core.formatRelative(date, options);
  }

  // === TIME CALCULATIONS ===

  /**
   * Add time to date
   */
  add(date, amount, options = {}) {
    return this.core.add(date, amount, options);
  }

  /**
   * Subtract time from date
   */
  subtract(date, amount, options = {}) {
    return this.core.subtract(date, amount, options);
  }

  /**
   * Calculate difference between dates
   */
  difference(date1, date2, options = {}) {
    return this.core.difference(date1, date2, options);
  }

  // === TIME VALIDATION ===

  /**
   * Validate date
   */
  validate(date, options = {}) {
    return this.core.validate(date, options);
  }

  /**
   * Check if date is valid
   */
  isValid(date) {
    return this.core.isValid(date);
  }

  /**
   * Check if date is in the past
   */
  isPast(date, options = {}) {
    return this.core.isPast(date, options);
  }

  /**
   * Check if date is in the future
   */
  isFuture(date, options = {}) {
    return this.core.isFuture(date, options);
  }

  /**
   * Check if date is today
   */
  isToday(date, options = {}) {
    return this.core.isToday(date, options);
  }

  /**
   * Check if date is weekend
   */
  isWeekend(date, options = {}) {
    return this.core.isWeekend(date, options);
  }

  /**
   * Check if date is business day
   */
  isBusinessDay(date, options = {}) {
    return this.core.isBusinessDay(date, options);
  }

  // === TIME COMPARISONS ===

  /**
   * Compare two dates
   */
  compare(date1, date2, options = {}) {
    return this.core.compare(date1, date2, options);
  }

  // === PERFORMANCE & MONITORING ===

  /**
   * Get performance metrics
   */
  getMetrics() {
    return this.core.getMetrics();
  }

  /**
   * Clear performance cache
   */
  clearCache() {
    this.core.clearCache();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics() {
    this.core.resetMetrics();
  }

  // === CONVENIENCE METHODS ===

  /**
   * Simple date formatting (backward compatibility)
   */
  formatDate(date, format = 'YYYY-MM-DD') {
    const result = this.format(date, { format });
    return result.success ? result.data : '';
  }

  /**
   * Simple time formatting (backward compatibility)
   */
  formatTime(date, format = 'HH:mm:ss') {
    const result = this.format(date, { format });
    return result.success ? result.data : '';
  }

  /**
   * Simple datetime formatting (backward compatibility)
   */
  formatDateTime(date, format = 'YYYY-MM-DD HH:mm:ss') {
    const result = this.format(date, { format });
    return result.success ? result.data : '';
  }

  /**
   * Simple relative time formatting (backward compatibility)
   */
  formatRelativeTime(date, baseDate = new Date()) {
    const result = this.formatRelative(date, { baseDate });
    return result.success ? result.data : '';
  }

  /**
   * Simple date validation (backward compatibility)
   */
  isValidDate(date) {
    return this.isValid(date);
  }

  /**
   * Simple date comparison (backward compatibility)
   */
  compareDates(date1, date2) {
    return this.compare(date1, date2);
  }

  /**
   * Simple date addition (backward compatibility)
   */
  addDays(date, days) {
    const result = this.add(date, days, { unit: 'days' });
    return result.success ? result.data : date;
  }

  /**
   * Simple date subtraction (backward compatibility)
   */
  subtractDays(date, days) {
    const result = this.subtract(date, days, { unit: 'days' });
    return result.success ? result.data : date;
  }

  /**
   * Simple date difference (backward compatibility)
   */
  getDaysDifference(date1, date2) {
    const result = this.difference(date1, date2, { unit: 'days' });
    return result.success ? result.data : 0;
  }

  /**
   * Simple date parsing (backward compatibility)
   */
  parseDate(dateString, format) {
    const result = this.parse(dateString, { format });
    return result.success ? result.data : null;
  }

  /**
   * Simple current date (backward compatibility)
   */
  getCurrentDate() {
    const result = this.now();
    return result.success ? result.data : new Date();
  }

  /**
   * Simple current time (backward compatibility)
   */
  getCurrentTime() {
    const result = this.now();
    return result.success ? result.data : new Date();
  }

  /**
   * Simple UTC date (backward compatibility)
   */
  getUtcDate() {
    const result = this.utc();
    return result.success ? result.data : new Date();
  }

  /**
   * Simple business day check (backward compatibility)
   */
  isBusinessDay(date) {
    return this.isBusinessDay(date);
  }

  /**
   * Simple weekend check (backward compatibility)
   */
  isWeekend(date) {
    return this.isWeekend(date);
  }

  /**
   * Simple today check (backward compatibility)
   */
  isToday(date) {
    return this.isToday(date);
  }

  /**
   * Simple past check (backward compatibility)
   */
  isPast(date) {
    return this.isPast(date);
  }

  /**
   * Simple future check (backward compatibility)
   */
  isFuture(date) {
    return this.isFuture(date);
  }
}

// Factory function for creating time utils instance
export function createUnifiedTimeUtils(config = {}) {
  return new UnifiedTimeUtils(config);
}

// Export default
export default UnifiedTimeUtils;