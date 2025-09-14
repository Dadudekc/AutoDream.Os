/**
 * @fileoverview Unified Time Utility - TypeScript Wrapper for Shared Core
 * @version 3.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 * 
 * TypeScript wrapper around the shared TimeCore implementation.
 * Provides type safety while using the universal JavaScript core.
 */

import { TimeCore } from '../shared/time-core.js';
import { 
  ITimeUtility, ITimeResult, ITimeFormatOptions, ITimeCalculationOptions, 
  ITimeValidationOptions, ITimeRangeOptions 
} from '../../interfaces/ITimeUtility';

/**
 * Unified Time Utility Implementation
 * TypeScript wrapper around the shared TimeCore
 */
export class TimeUtility implements ITimeUtility {
  private core: TimeCore;

  constructor(config: any = {}) {
    this.core = new TimeCore(config);
  }

  /**
   * Initialize the time utility with configuration
   */
  async initialize(config: any = {}): Promise<void> {
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

  // === TIME CREATION & PARSING ===

  /**
   * Create date from input
   */
  create(input?: any, options?: {
    timezone?: string;
    locale?: string;
    format?: string;
  }): ITimeResult {
    return this.core.create(input, options);
  }

  /**
   * Parse date string with format
   */
  parse(dateString: string, options?: {
    format?: string;
    timezone?: string;
    locale?: string;
    strict?: boolean;
  }): ITimeResult {
    return this.core.parse(dateString, options);
  }

  /**
   * Get current time
   */
  now(options?: {
    timezone?: string;
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  }): ITimeResult {
    return this.core.now(options);
  }

  /**
   * Get UTC time
   */
  utc(options?: {
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  }): ITimeResult {
    return this.core.utc(options);
  }

  // === TIME FORMATTING ===

  /**
   * Format date with options
   */
  format(date: Date | string, options?: ITimeFormatOptions): ITimeResult {
    return this.core.format(date, options);
  }

  /**
   * Format relative time
   */
  formatRelative(date: Date | string, options?: {
    baseDate?: Date | string;
    locale?: string;
    precision?: 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years';
    includeSuffix?: boolean;
  }): ITimeResult {
    return this.core.formatRelative(date, options);
  }

  // === TIME CALCULATIONS ===

  /**
   * Add time to date
   */
  add(date: Date | string, amount: number, options?: ITimeCalculationOptions): ITimeResult {
    return this.core.add(date, amount, options);
  }

  /**
   * Subtract time from date
   */
  subtract(date: Date | string, amount: number, options?: ITimeCalculationOptions): ITimeResult {
    return this.core.subtract(date, amount, options);
  }

  /**
   * Calculate difference between dates
   */
  difference(date1: Date | string, date2: Date | string, options?: ITimeCalculationOptions): ITimeResult {
    return this.core.difference(date1, date2, options);
  }

  // === TIME VALIDATION ===

  /**
   * Validate date
   */
  validate(date: any, options?: ITimeValidationOptions): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
    normalizedDate?: Date;
  } {
    return this.core.validate(date, options);
  }

  /**
   * Check if date is valid
   */
  isValid(date: any): boolean {
    return this.core.isValid(date);
  }

  /**
   * Check if date is in the past
   */
  isPast(date: Date | string, options?: {
    includeToday?: boolean;
    timezone?: string;
  }): boolean {
    return this.core.isPast(date, options);
  }

  /**
   * Check if date is in the future
   */
  isFuture(date: Date | string, options?: {
    includeToday?: boolean;
    timezone?: string;
  }): boolean {
    return this.core.isFuture(date, options);
  }

  /**
   * Check if date is today
   */
  isToday(date: Date | string, options?: {
    timezone?: string;
  }): boolean {
    return this.core.isToday(date, options);
  }

  /**
   * Check if date is weekend
   */
  isWeekend(date: Date | string, options?: {
    timezone?: string;
  }): boolean {
    return this.core.isWeekend(date, options);
  }

  /**
   * Check if date is business day
   */
  isBusinessDay(date: Date | string, options?: {
    timezone?: string;
    excludeHolidays?: boolean;
  }): boolean {
    return this.core.isBusinessDay(date, options);
  }

  // === TIME COMPARISONS ===

  /**
   * Compare two dates
   */
  compare(date1: Date | string, date2: Date | string, options?: {
    precision?: 'milliseconds' | 'seconds' | 'minutes' | 'hours' | 'days';
    timezone?: string;
  }): number {
    return this.core.compare(date1, date2, options);
  }

  // === PERFORMANCE & MONITORING ===

  /**
   * Get performance metrics
   */
  getMetrics(): {
    totalOperations: number;
    averageProcessingTime: number;
    cacheHitRate: number;
    memoryUsage: number;
    errorRate: number;
  } {
    return this.core.getMetrics();
  }

  /**
   * Clear performance cache
   */
  clearCache(): void {
    this.core.clearCache();
  }

  /**
   * Reset performance metrics
   */
  resetMetrics(): void {
    this.core.resetMetrics();
  }
}

// Export for both CommonJS and ES modules
export default TimeUtility;