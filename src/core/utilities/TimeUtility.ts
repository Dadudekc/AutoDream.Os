/**
 * @fileoverview Time Utility Implementation - Enterprise-grade time manipulation utility
 * @version 2.0.0
 * @author Agent-7 (Web Development Specialist)
 * @created 2024-01-01
 * @updated 2024-01-01
 */

import { 
  ITimeUtility, ITimeResult, ITimeFormatOptions, ITimeCalculationOptions, 
  ITimeValidationOptions, ITimeRangeOptions 
} from '../interfaces/ITimeUtility';

/**
 * Enterprise Time Utility Implementation
 * Provides comprehensive time manipulation, formatting, and calculation capabilities
 */
export class TimeUtility implements ITimeUtility {
  private config: any = {};
  private metrics = {
    totalOperations: 0,
    totalProcessingTime: 0,
    cacheHits: 0,
    cacheMisses: 0,
    errors: 0,
    memoryUsage: 0
  };
  private cache = new Map<string, any>();
  private maxCacheSize = 1000;

  async initialize(config: any = {}): Promise<void> {
    try {
      this.config = {
        defaultTimezone: 'UTC',
        defaultLocale: 'en-US',
        maxCacheSize: 1000,
        enableMetrics: true,
        enableCaching: true,
        ...config
      };
      this.maxCacheSize = this.config.maxCacheSize;
    } catch (error) {
      this.metrics.errors++;
      throw new Error(`TimeUtility initialization failed: ${error}`);
    }
  }

  async cleanup(): Promise<void> {
    try {
      this.cache.clear();
      this.resetMetrics();
    } catch (error) {
      throw new Error(`TimeUtility cleanup failed: ${error}`);
    }
  }

  getMetadata() {
    return {
      name: 'TimeUtility',
      version: '2.0.0',
      capabilities: [
        'creation', 'parsing', 'formatting', 'calculation', 'validation',
        'comparison', 'conversion', 'ranges', 'business', 'performance'
      ],
      dependencies: []
    };
  }

  // === TIME CREATION & PARSING ===

  create(input?: any, options: {
    timezone?: string;
    locale?: string;
    format?: string;
  } = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      let result: Date;
      
      if (!input) {
        result = new Date();
      } else if (input instanceof Date) {
        result = new Date(input);
      } else if (typeof input === 'string') {
        result = new Date(input);
      } else if (typeof input === 'number') {
        result = new Date(input);
      } else {
        return this.createErrorResult('Invalid input type');
      }

      if (isNaN(result.getTime())) {
        return this.createErrorResult('Invalid date');
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date creation failed: ${error}`);
    }
  }

  parse(dateString: string, options: {
    format?: string;
    timezone?: string;
    locale?: string;
    strict?: boolean;
  } = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      if (!dateString || typeof dateString !== 'string') {
        return this.createErrorResult('Invalid date string');
      }

      const { strict = false } = options;
      let result: Date;

      if (options.format) {
        result = this.parseWithFormat(dateString, options.format);
      } else {
        result = new Date(dateString);
      }

      if (isNaN(result.getTime())) {
        if (strict) {
          return this.createErrorResult('Invalid date format');
        }
        // Try alternative parsing methods
        result = this.tryAlternativeParsing(dateString);
        if (isNaN(result.getTime())) {
          return this.createErrorResult('Unable to parse date');
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date parsing failed: ${error}`);
    }
  }

  now(options: {
    timezone?: string;
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  } = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const { precision = 'milliseconds' } = options;
      const now = new Date();
      
      let result = now;
      if (precision === 'seconds') {
        result = new Date(Math.floor(now.getTime() / 1000) * 1000);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Now operation failed: ${error}`);
    }
  }

  utc(options: {
    format?: string;
    precision?: 'milliseconds' | 'seconds';
  } = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const { precision = 'milliseconds' } = options;
      const now = new Date();
      const utc = new Date(now.getTime() + (now.getTimezoneOffset() * 60000));
      
      let result = utc;
      if (precision === 'seconds') {
        result = new Date(Math.floor(utc.getTime() / 1000) * 1000);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`UTC operation failed: ${error}`);
    }
  }

  // === TIME FORMATTING ===

  format(date: Date | string, options: ITimeFormatOptions = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const {
        locale = 'en-US',
        timeZone = 'UTC',
        format = 'medium',
        customFormat,
        includeTime = true,
        includeDate = true,
        includeTimezone = false
      } = options;

      let result: string;

      if (customFormat) {
        result = this.formatWithCustomFormat(dateObj, customFormat);
      } else {
        const formatOptions: Intl.DateTimeFormatOptions = this.getFormatOptions(format, includeTime, includeDate);
        result = new Intl.DateTimeFormat(locale, {
          ...formatOptions,
          timeZone
        }).format(dateObj);
      }

      if (includeTimezone) {
        result += ` (${timeZone})`;
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date formatting failed: ${error}`);
    }
  }

  formatRelative(date: Date | string, options: {
    baseDate?: Date | string;
    locale?: string;
    precision?: 'seconds' | 'minutes' | 'hours' | 'days' | 'weeks' | 'months' | 'years';
    includeSuffix?: boolean;
  } = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      const baseDate = this.toDate(options.baseDate) || new Date();
      
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const diffMs = dateObj.getTime() - baseDate.getTime();
      const diffSeconds = Math.floor(diffMs / 1000);
      const diffMinutes = Math.floor(diffSeconds / 60);
      const diffHours = Math.floor(diffMinutes / 60);
      const diffDays = Math.floor(diffHours / 24);
      const diffWeeks = Math.floor(diffDays / 7);
      const diffMonths = Math.floor(diffDays / 30);
      const diffYears = Math.floor(diffDays / 365);

      const { precision = 'days', includeSuffix = true } = options;
      let result: string;

      if (Math.abs(diffYears) >= 1 && ['years', 'months', 'days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffYears)} year${Math.abs(diffYears) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffMonths) >= 1 && ['months', 'days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffMonths)} month${Math.abs(diffMonths) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffWeeks) >= 1 && ['days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffWeeks)} week${Math.abs(diffWeeks) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffDays) >= 1 && ['days', 'hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffDays)} day${Math.abs(diffDays) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffHours) >= 1 && ['hours', 'minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffHours)} hour${Math.abs(diffHours) !== 1 ? 's' : ''}`;
      } else if (Math.abs(diffMinutes) >= 1 && ['minutes', 'seconds'].includes(precision)) {
        result = `${Math.abs(diffMinutes)} minute${Math.abs(diffMinutes) !== 1 ? 's' : ''}`;
      } else {
        result = `${Math.abs(diffSeconds)} second${Math.abs(diffSeconds) !== 1 ? 's' : ''}`;
      }

      if (includeSuffix) {
        if (diffMs > 0) {
          result += ' from now';
        } else if (diffMs < 0) {
          result += ' ago';
        } else {
          result = 'now';
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Relative formatting failed: ${error}`);
    }
  }

  // === TIME CALCULATIONS ===

  add(date: Date | string, amount: number, options: ITimeCalculationOptions = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const dateObj = this.toDate(date);
      if (!dateObj) {
        return this.createErrorResult('Invalid date');
      }

      const { unit = 'days', businessDays = false } = options;
      let result = new Date(dateObj);

      if (businessDays && unit === 'days') {
        result = this.addBusinessDays(result, amount);
      } else {
        switch (unit) {
          case 'milliseconds':
            result.setTime(result.getTime() + amount);
            break;
          case 'seconds':
            result.setTime(result.getTime() + (amount * 1000));
            break;
          case 'minutes':
            result.setTime(result.getTime() + (amount * 60 * 1000));
            break;
          case 'hours':
            result.setTime(result.getTime() + (amount * 60 * 60 * 1000));
            break;
          case 'days':
            result.setDate(result.getDate() + amount);
            break;
          case 'weeks':
            result.setDate(result.getDate() + (amount * 7));
            break;
          case 'months':
            result.setMonth(result.getMonth() + amount);
            break;
          case 'years':
            result.setFullYear(result.getFullYear() + amount);
            break;
          default:
            return this.createErrorResult(`Unsupported unit: ${unit}`);
        }
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date addition failed: ${error}`);
    }
  }

  subtract(date: Date | string, amount: number, options: ITimeCalculationOptions = {}): ITimeResult {
    return this.add(date, -amount, options);
  }

  difference(date1: Date | string, date2: Date | string, options: ITimeCalculationOptions = {}): ITimeResult {
    const startTime = performance.now();
    
    try {
      const dateObj1 = this.toDate(date1);
      const dateObj2 = this.toDate(date2);
      
      if (!dateObj1 || !dateObj2) {
        return this.createErrorResult('Invalid dates');
      }

      const { unit = 'milliseconds', absolute = true } = options;
      let diffMs = dateObj2.getTime() - dateObj1.getTime();
      
      if (absolute) {
        diffMs = Math.abs(diffMs);
      }

      let result: number;
      switch (unit) {
        case 'milliseconds':
          result = diffMs;
          break;
        case 'seconds':
          result = Math.floor(diffMs / 1000);
          break;
        case 'minutes':
          result = Math.floor(diffMs / (1000 * 60));
          break;
        case 'hours':
          result = Math.floor(diffMs / (1000 * 60 * 60));
          break;
        case 'days':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24));
          break;
        case 'weeks':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 7));
          break;
        case 'months':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 30));
          break;
        case 'years':
          result = Math.floor(diffMs / (1000 * 60 * 60 * 24 * 365));
          break;
        default:
          return this.createErrorResult(`Unsupported unit: ${unit}`);
      }

      this.updateMetrics(startTime);
      return this.createSuccessResult(result);
    } catch (error) {
      this.metrics.errors++;
      return this.createErrorResult(`Date difference calculation failed: ${error}`);
    }
  }

  // === TIME VALIDATION ===

  validate(date: any, options: ITimeValidationOptions = {}): {
    isValid: boolean;
    errors: string[];
    warnings: string[];
    normalizedDate?: Date;
  } {
    try {
      const errors: string[] = [];
      const warnings: string[] = [];
      
      const dateObj = this.toDate(date);
      if (!dateObj || isNaN(dateObj.getTime())) {
        errors.push('Invalid date');
        return { isValid: false, errors, warnings };
      }

      const { minDate, maxDate, allowFuture = true, allowPast = true } = options;
      const now = new Date();

      if (minDate) {
        const minDateObj = this.toDate(minDate);
        if (minDateObj && dateObj < minDateObj) {
          errors.push(`Date is before minimum date: ${minDate}`);
        }
      }

      if (maxDate) {
        const maxDateObj = this.toDate(maxDate);
        if (maxDateObj && dateObj > maxDateObj) {
          errors.push(`Date is after maximum date: ${maxDate}`);
        }
      }

      if (!allowFuture && dateObj > now) {
        errors.push('Future dates are not allowed');
      }

      if (!allowPast && dateObj < now) {
        errors.push('Past dates are not allowed');
      }

      return {
        isValid: errors.length === 0,
        errors,
        warnings,
        normalizedDate: dateObj
      };
    } catch (error) {
      return {
        isValid: false,
        errors: [`Validation error: ${error}`],
        warnings: []
      };
    }
  }

  isValid(date: any): boolean {
    const dateObj = this.toDate(date);
    return dateObj !== null && !isNaN(dateObj.getTime());
  }

  isPast(date: Date | string, options: {
    includeToday?: boolean;
    timezone?: string;
  } = {}): boolean {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const now = new Date();
    const { includeToday = false } = options;

    if (includeToday) {
      return dateObj <= now;
    }
    return dateObj < now;
  }

  isFuture(date: Date | string, options: {
    includeToday?: boolean;
    timezone?: string;
  } = {}): boolean {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const now = new Date();
    const { includeToday = false } = options;

    if (includeToday) {
      return dateObj >= now;
    }
    return dateObj > now;
  }

  isToday(date: Date | string, options: {
    timezone?: string;
  } = {}): boolean {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const today = new Date();
    return dateObj.toDateString() === today.toDateString();
  }

  isWeekend(date: Date | string, options: {
    timezone?: string;
  } = {}): boolean {
    const dateObj = this.toDate(date);
    if (!dateObj) return false;

    const day = dateObj.getDay();
    return day === 0 || day === 6; // Sunday or Saturday
  }

  isBusinessDay(date: Date | string, options: {
    timezone?: string;
    excludeHolidays?: boolean;
  } = {}): boolean {
    return !this.isWeekend(date, options);
  }

  // === TIME COMPARISONS ===

  compare(date1: Date | string, date2: Date | string, options: {
    precision?: 'milliseconds' | 'seconds' | 'minutes' | 'hours' | 'days';
    timezone?: string;
  } = {}): number {
    const dateObj1 = this.toDate(date1);
    const dateObj2 = this.toDate(date2);
    
    if (!dateObj1 || !dateObj2) return 0;

    const { precision = 'milliseconds' } = options;
    
    switch (precision) {
      case 'milliseconds':
        return dateObj1.getTime() - dateObj2.getTime();
      case 'seconds':
        return Math.floor(dateObj1.getTime() / 1000) - Math.floor(dateObj2.getTime() / 1000);
      case 'minutes':
        return Math.floor(dateObj1.getTime() / (1000 * 60)) - Math.floor(dateObj2.getTime() / (1000 * 60));
      case 'hours':
        return Math.floor(dateObj1.getTime() / (1000 * 60 * 60)) - Math.floor(dateObj2.getTime() / (1000 * 60 * 60));
      case 'days':
        return Math.floor(dateObj1.getTime() / (1000 * 60 * 60 * 24)) - Math.floor(dateObj2.getTime() / (1000 * 60 * 60 * 24));
      default:
        return dateObj1.getTime() - dateObj2.getTime();
    }
  }

  // === PERFORMANCE & MONITORING ===

  getMetrics() {
    return {
      totalOperations: this.metrics.totalOperations,
      averageProcessingTime: this.metrics.totalOperations > 0 
        ? this.metrics.totalProcessingTime / this.metrics.totalOperations 
        : 0,
      cacheHitRate: this.metrics.cacheHits + this.metrics.cacheMisses > 0
        ? this.metrics.cacheHits / (this.metrics.cacheHits + this.metrics.cacheMisses)
        : 0,
      memoryUsage: this.metrics.memoryUsage,
      errorRate: this.metrics.totalOperations > 0
        ? this.metrics.errors / this.metrics.totalOperations
        : 0
    };
  }

  clearCache(): void {
    this.cache.clear();
  }

  resetMetrics(): void {
    this.metrics = {
      totalOperations: 0,
      totalProcessingTime: 0,
      cacheHits: 0,
      cacheMisses: 0,
      errors: 0,
      memoryUsage: 0
    };
  }

  // === PRIVATE HELPER METHODS ===

  private createSuccessResult<T>(data: T): ITimeResult {
    return {
      success: true,
      data,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  private createErrorResult(error: string): ITimeResult {
    return {
      success: false,
      error,
      metrics: {
        processingTime: 0,
        memoryUsage: 0
      }
    };
  }

  private updateMetrics(startTime: number): void {
    const processingTime = performance.now() - startTime;
    this.metrics.totalOperations++;
    this.metrics.totalProcessingTime += processingTime;
    this.metrics.memoryUsage = this.cache.size;
  }

  private toDate(input: any): Date | null {
    if (!input) return null;
    if (input instanceof Date) return new Date(input);
    if (typeof input === 'string' || typeof input === 'number') {
      const date = new Date(input);
      return isNaN(date.getTime()) ? null : date;
    }
    return null;
  }

  private parseWithFormat(dateString: string, format: string): Date {
    // Basic format parsing - can be enhanced
    const patterns: Record<string, RegExp> = {
      'YYYY-MM-DD': /^(\d{4})-(\d{2})-(\d{2})$/,
      'MM/DD/YYYY': /^(\d{2})\/(\d{2})\/(\d{4})$/,
      'DD/MM/YYYY': /^(\d{2})\/(\d{2})\/(\d{4})$/,
      'YYYY-MM-DD HH:mm:ss': /^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})$/
    };

    const pattern = patterns[format];
    if (!pattern) {
      return new Date(dateString);
    }

    const match = dateString.match(pattern);
    if (!match) {
      return new Date(dateString);
    }

    // Parse based on format
    if (format === 'YYYY-MM-DD') {
      return new Date(parseInt(match[1]), parseInt(match[2]) - 1, parseInt(match[3]));
    } else if (format === 'MM/DD/YYYY') {
      return new Date(parseInt(match[3]), parseInt(match[1]) - 1, parseInt(match[2]));
    } else if (format === 'DD/MM/YYYY') {
      return new Date(parseInt(match[3]), parseInt(match[2]) - 1, parseInt(match[1]));
    }

    return new Date(dateString);
  }

  private tryAlternativeParsing(dateString: string): Date {
    // Try common date formats
    const formats = [
      /^(\d{4})-(\d{2})-(\d{2})$/,
      /^(\d{2})\/(\d{2})\/(\d{4})$/,
      /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/
    ];

    for (const format of formats) {
      const match = dateString.match(format);
      if (match) {
        if (format.source.includes('\\d{4}-\\d{2}-\\d{2}')) {
          return new Date(parseInt(match[1]), parseInt(match[2]) - 1, parseInt(match[3]));
        } else {
          return new Date(parseInt(match[3]), parseInt(match[1]) - 1, parseInt(match[2]));
        }
      }
    }

    return new Date(dateString);
  }

  private getFormatOptions(format: string, includeTime: boolean, includeDate: boolean): Intl.DateTimeFormatOptions {
    const baseOptions: Intl.DateTimeFormatOptions = {};

    if (includeDate) {
      switch (format) {
        case 'short':
          baseOptions.dateStyle = 'short';
          break;
        case 'medium':
          baseOptions.dateStyle = 'medium';
          break;
        case 'long':
          baseOptions.dateStyle = 'long';
          break;
        case 'full':
          baseOptions.dateStyle = 'full';
          break;
      }
    }

    if (includeTime) {
      switch (format) {
        case 'short':
          baseOptions.timeStyle = 'short';
          break;
        case 'medium':
          baseOptions.timeStyle = 'medium';
          break;
        case 'long':
          baseOptions.timeStyle = 'long';
          break;
        case 'full':
          baseOptions.timeStyle = 'full';
          break;
      }
    }

    return baseOptions;
  }

  private formatWithCustomFormat(date: Date, format: string): string {
    // Basic custom format implementation
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return format
      .replace('YYYY', String(year))
      .replace('MM', month)
      .replace('DD', day)
      .replace('HH', hours)
      .replace('mm', minutes)
      .replace('ss', seconds);
  }

  private addBusinessDays(date: Date, days: number): Date {
    const result = new Date(date);
    let addedDays = 0;

    while (addedDays < Math.abs(days)) {
      result.setDate(result.getDate() + (days > 0 ? 1 : -1));
      if (!this.isWeekend(result)) {
        addedDays++;
      }
    }

    return result;
  }
}